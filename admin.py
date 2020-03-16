#!/usr/bin/python3

import cherrypy
import sqlite3
import hashlib
import os

class BlindShareAdmin(object):

    @cherrypy.expose
    def index(self):
        a = []
        a.append("<!DOCTYPE html> \n <HTML>\n <HEAD>")
        a.append("<link rel=\"stylesheet\" href=\"static/admin.css\">\n")
        a.append("<TITLE>Blindshare</TITLE>\n")
        a.append("</HEAD>\n <BODY><H1> Welcom to BlindShare Web-Admin-Console - ver. 0.6</H1>\n")
        a.append("<p>\n")
#        a.append("<TABLE id=\"t1\" border=\"1\" > \n")
        a.append("<TABLE id=\"t1\"> \n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Add User</H3></td><td class=\"spacer\"></td><td colspan=\"6\"><H3>Remove User</H3></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"addUser\" method=\"POST\">Username:</td><td class=\"c1\"></td><td><input type=\"text\" name=\"user\"></td><td>Cert Hash:</td><td><input type=\"text\" name=\"certhash\"></td><td></td><td><input value=\"add\" type=\"submit\"></form></td><td class=\"spacer\"></td>\n")
        a.append("<td class=\"c2\"><form action=\"delUser\" method=\"POST\">User ID:</td><td></td><td class=\"c1\"></td><td><input class=\"ids\" type=\"text\" name=\"userID\"></td><td></td><td><input value=\"del\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Update visibility</H3></td><td class=\"spacer\"></td><td colspan=\"6\"><H3>Remove File</H3></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"upView\" method=\"POST\">Show Files: <input type=\"checkbox\" name=\"view\" value=\"1\"></td><td class=\"c1\"></td><td>Upload:<input type=\"checkbox\" name=\"upload\" value=\"1\"></td><td>User ID:</td><td><input class=\"ids\" type=\"text\" name=\"userID\"></td><td></td><td><input value=\"update\" type=\"submit\"></form></td><td class=\"spacer\"></td>\n")
        a.append("<td class=\"c2\"><form action=\"delFile\" method=\"POST\">File ID:</td><td></td><td class=\"c1\"></td><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td></td><td><input value=\"del\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Edit expiration date</H3></td><td class=\"spacer\"></td><td colspan=\"6\"></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"expire\" method=\"POST\">Expiration date:</td><td class=\"c1\"></td><td><input type=\"text\" name=\"exp\"></td><td>File ID:</td><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td></td><td><input value=\"set\" type=\"submit\"></form></td><td class=\"spacer\"></td><td colspan=\"6\"></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Update Hash</H3></td><td class=\"spacer\"></td><td colspan=\"6\"><H3>Upload File</H3></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"upHash\" method=\"POST\">File ID:</td><td class=\"c1\"><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td>Hash:</td><td><input type=\"text\" name=\"hash\"></td><td></td><td><input value=\"update\" type=\"submit\"></form></td><td class=\"spacer\"></td>\n")
        a.append("<td><form action=\"uplFile\" method=\"POST\" enctype=\"multipart/form-data\">Upload File:</td><td><input type=\"file\" name=\"upFile\"></td><td></td><td></td><td></td><td><input value=\"upload\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Grant User access to File</H3></td><td class=\"spacer\"></td><td colspan=\"6\"><H3>Remove User access</H3></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"grantAccess\" method=\"POST\">UserID:</td><td class=\"c1\"></td><td><input class=\"ids\" type=\"text\" name=\"userID\"></td><td>File ID:</td><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td></td><td><input value=\"set\" type=\"submit\"></form></td><td class=\"spacer\"></td>\n")
        a.append("<td class=\"c2\"><form action=\"rmAccess\" method=\"POST\">User ID:</td><td><input class=\"ids\" type=\"text\" name=\"userID\"></td><td>File ID:</td><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td></td><td><input value=\"remove\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")

        a.append("</TABLE>\n")
        a.append("<P>\n")

        with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
            getFileItems = con.execute("SELECT * FROM Files ORDER BY fileID").fetchall()
            getUserItems = con.execute("SELECT * FROM Identities ORDER BY userID").fetchall()
            getAccessItems = con.execute("SELECT Access.userID, Identities.name, Access.fileID, Files.url, Access.expire_date from Access INNER JOIN Identities on Access.userID = Identities.userID INNER JOIN Files on Access.fileID = Files.fileID").fetchall()

        a.append("<DIV>")
        a.append("<H3>Files:</H3>\n")
        a.append("<TABLE id=\"fil\" border=1> \n") 
        a.append("<tr><TH>File ID</TH><TH>Hash</TH><TH>Filename</TH></tr>\n")
        for line in getFileItems:
            a.append("<tr><td class=\"tc2\">" + str(line[0]) + "</td><td class=\"tc3\">" + str(line[1]) + "</td><td class=\"tc4\">" + str(line[2]) + "</td></tr>\n")

        a.append("</TABLE>\n")
        a.append("<P>\n")

        a.append("<H3>Users:</H3>\n")
        a.append("<TABLE id=\"ident\" border=1> \n")    
        a.append("<tr><TH>User ID</TH><TH>Username</TH><TH>Cert Fingerprint</TH><TH>View</TH><TH>Upload</TH></tr>\n")
        for line in getUserItems:
            a.append("<tr><td class=\"tc2\">" + str(line[0]) + "</td><td class=\"tc4\">" + str(line[1]) + "</td><td class=\"tc3\">" + str(line[2]) + "</td><td class=\"tc2\">" + str(bool(line[3])) + "</td><td class=\"tc2\">" + str(bool(line[4])) + "</td></tr>\n")

        a.append("</TABLE>\n")
        a.append("<P>\n")

        a.append("<H3>Access:</H3>\n")
        a.append("<TABLE id=\"acc\" border=1> \n")   
        a.append("<tr><TH>User ID</TH><TH>Username</TH><TH>File ID</TH><TH>Filename</TH><TH>Expire Date</TH></tr>\n") 
        for line in getAccessItems:
            a.append("<tr><td class=\"tc2\">" + str(line[0]) + "</td><td class=\"tc4\">" + str(line[1]) + "</td><td class=\"tc2\">" + str(line[2]) + "</td><td class=\"tc4\">" + str(line[3]) + "</td><td class=\"tc4\">" + str(line[4]) + "</td></tr>\n")

        a.append("</TABLE>\n")
        a.append("<P>\n")
        a.append("</DIV>")

        a.append("</BODY>\n</HTML>")
        return a

    @cherrypy.expose
    def putHash(self, u_filename):
        ut_filename=u_filename.encode('utf-8')
        hashSHA256 = hashlib.sha256(ut_filename).hexdigest()
        salt = hashlib.sha256(os.urandom(32)).hexdigest()

        ### Debug start ###
        print("uploaded File: " + u_filename)
        print("hashSHA256: ", hashSHA256)
        print("salt: ", salt)
        ### Debug end  ###

        d1 = int(hashSHA256,16)
        d2 = int(salt,16)

        hashX = hex(d1 ^ d2).rstrip("L").lstrip("0x")

        with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
            con.execute("INSERT INTO Files (hash, url) VALUES (?, ?)", [hashX, u_filename])

        return self.index()

    @cherrypy.expose
    def addUser(self, user, certhash):
        if (user == "" or certhash == ""):
    ### future use --> ###        return self.errorMsg("User and Cert Hash") 
            return("<form action=\"index\">Fields User nor CertHash must no be empty<P><input value=\"back\" type=\"submit\" /></form>")

        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                con.execute("INSERT INTO Identities (name, certFingerprint, view, upload) VALUES (?, ?, ?, ?)", [user, certhash, 0, 0])
        except Exception as e:
           return e

        return self.index()

    @cherrypy.expose
    def delUser(self, userID):
        if (userID == "" ):
            return("<form action=\"index\">Field UserID must no be empty<P><input value=\"back\" type=\"submit\" /></form>")

        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                con.execute("DELETE FROM Identities WHERE userID=?", [userID])
                con.execute("DELETE FROM Access WHERE userID=?", [userID])
        except:
           pass

        return self.index()

    @cherrypy.expose
    def upView(self, userID, view=0, upload=0):
        if (userID == "" ):
            return("<form action=\"index\">Field UserID must no be empty<P><input value=\"back\" type=\"submit\" /></form>")

        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                con.execute("UPDATE Identities SET view=?, upload=? WHERE userID=?", [view, upload, userID])
        except Exception as e:
           return e

        return self.index()

    @cherrypy.expose
    def expire(self, fileID, exp=""):
        if (fileID == "" ):
            return("<form action=\"index\">Field FileID nor Expire Date must no be empty<P><input value=\"back\" type=\"submit\" /></form>")

        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                con.execute("UPDATE Access SET expire_date=? WHERE fileID=?", [exp, fileID])
        except Exception as e:
           return e

        return self.index()

    @cherrypy.expose
    def delFile(self, fileID):
        if (fileID == "" ):
            return("<form action=\"index\">Field FileID must no be blank<P><input value=\"back\" type=\"submit\" /></form>")

        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                con.execute("DELETE FROM Files WHERE fileID=?", [fileID])
                con.execute("DELETE FROM Access WHERE fileID=?", [fileID])
        except Exception as e:
           return e
        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                del_file=con.execute("SELECT url FROM Files WHERE fileID=?", [fileID])
                upload_path = cherrypy.request.app.config['cfg']['uploadPath']
                os.remove(os.path.join(upload_path, 'del_file'))

        except Exception as e:
           return e


        return self.index()

    @cherrypy.expose
    def upHash(self, fileID, hash):
        if (fileID == "" or hash==""):
            return("<form action=\"index\">Fields FileID nor hash must no be blank<P><input value=\"back\" type=\"submit\" /></form>")

        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                con.execute("UPDATE Files SET hash=? WHERE fileID=?", [hash, fileID])
        except Exception as e:
           return e

        return self.index()

    @cherrypy.expose
    def uplFile(self, upFile):
        if (upFile == ""):
            return("<form action=\"index\">Field must no be blank<P><input value=\"back\" type=\"submit\"></form>")

        ### no, you will not inject some strange paths here !
        if ( "/" in upFile.filename or "\\" in upFile.filename ):
            return("<form action=\"index\">Invalid Filename<P><input value=\"back\" type=\"submit\"></form>")

        print(upFile)
        ### Upload File to Server ############################################################################################
        u_filename=upFile.filename
        upload_path = cherrypy.request.app.config['cfg']['uploadPath']
        upload_file = os.path.normpath(os.path.join(upload_path, u_filename))
#        print("uploading file: " + upFile.filename)

        size = 0
        with open(upload_file, 'wb') as out:
            while True:
                data = upFile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)

        return self.putHash(u_filename)

    @cherrypy.expose
    def grantAccess(self, userID, fileID):
        if (userID=="" or fileID == "" ):
            return("<form action=\"index\">Fields UserID nor FileID must no be blank<P><input value=\"back\" type=\"submit\" /></form>")

        exp_date=""
        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                exp_date,=con.execute("SELECT expire_date FROM Access where fileID=?", [fileID]).fetchone()
        except:
           exp_date=""

        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                con.execute("INSERT INTO Access (fileID, userID, expire_date) VALUES (?, ?, ?)", [fileID, userID, exp_date])
        except Exception as e:
           return e

        return self.index()

    @cherrypy.expose
    def rmAccess(self, userID, fileID):
        if (userID=="" or fileID == "" ):
            return("<form action=\"index\">Fields UserID nor FileID must no be blank<P><input value=\"back\" type=\"submit\" /></form>")

        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                con.execute("DELETE FROM Access WHERE fileID=? AND userID=?", [fileID, userID])
        except Exception as e:
           return e

        return self.index()


    @cherrypy.expose
    def errorMsg(self, message):
        b = []
        b.append("<!DOCTYPE html> \n")
        b.append("<P>\n")
        b.append("<script type=\"text/javascript\">alert(\"")
        b.append(message)
        b.append(" field must no be empty\").back()</script>\n")
        b.append("<noscript><form action=\"index\">")
        b.append(message)
        b.append(" field must no be empty<P>\n")
        b.append("<input value=\"back\" type=\"submit\"></form></noscript>\n")

        return b


    @cherrypy.expose
    def default(self):
      raise cherrypy.HTTPRedirect('index')
    default.exposed = True

if __name__ == '__main__':
    configfile = os.path.join(os.path.dirname(__file__),'config','admin.conf')
    cherrypy.quickstart(BlindShareAdmin(),config=configfile)
