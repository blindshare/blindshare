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
        a.append("<td class=\"c2\"><form action=\"delUser\" method=\"POST\">User ID:</td><td class=\"c1\"></td><td><input class=\"ids\" type=\"text\" name=\"userID\"></td><td></td><td></td><td><input value=\"del\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Update visibility</H3></td><td class=\"spacer\"></td><td colspan=\"6\"><H3>Remove File</H3></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"upView\" method=\"POST\">Show Files: <input type=\"checkbox\" name=\"view\" value=\"1\"></td><td class=\"c1\"></td><td>Upload:<input type=\"checkbox\" name=\"upload\" value=\"1\"></td><td>User ID:</td><td><input class=\"ids\" type=\"text\" name=\"userID\"></td><td></td><td><input value=\"update\" type=\"submit\"></form></td><td class=\"spacer\"></td>\n")
        a.append("<td class=\"c2\"><form action=\"delFile\" method=\"POST\">File ID:</td><td class=\"c1\"></td><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td></td><td></td><td><input value=\"del\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Edit expiration date</H3></td><td class=\"spacer\"></td><td colspan=\"6\"></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"expire\" method=\"POST\">Expiration date:</td><td class=\"c1\"></td><td><input type=\"text\" name=\"exp\"></td><td>File ID:</td><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td></td><td><input value=\"set\" type=\"submit\"></form></td><td class=\"spacer\"></td><td colspan=\"6\"></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Update Hash</H3></td><td class=\"spacer\"></td><td colspan=\"6\"><H3>Upload File</H3></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"upHash\" method=\"POST\">File ID:</td><td class=\"c1\"><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td>Hash:</td><td><input type=\"text\" name=\"hash\"></td><td></td><td><input value=\"update\" type=\"submit\"></form></td><td class=\"spacer\"></td>\n")
        a.append("<td class=\"c2\"><form action=\"upFile\" method=\"POST\">Upload File:</td><td class=\"c1\"></td><td><input type=\"file\" name=\"upFile\"></td><td></td><td></td><td><input value=\"upload\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Grant User access to File</H3></td><td class=\"spacer\"></td><td colspan=\"6\"><H3>Remove User access</H3></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"grantAccess\" method=\"POST\">UserID:</td><td class=\"c1\"></td><td><input class=\"ids\" type=\"text\" name=\"userID\"></td><td>File ID:</td><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td></td><td><input value=\"set\" type=\"submit\"></form></td><td class=\"spacer\"></td>\n")
        a.append("<td class=\"c2\"><form action=\"rmAccess\" method=\"POST\">User ID:</td><td class=\"c1\"></td><td><input class=\"ids\" type=\"text\" name=\"userID\"></td><td>File ID:</td><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td><input value=\"remove\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")

        a.append("</TABLE>\n")
        a.append("<P>\n")

        with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
            getFileItems = con.execute("SELECT * FROM Files ORDER BY fileID").fetchall()
            getUserItems = con.execute("SELECT * FROM Identities ORDER BY userID").fetchall()
            getAccessItems = con.execute("SELECT * FROM Access ORDER  BY userID").fetchall()

        a.append("<DIV>")
        a.append("<TABLE id=\"fil\" border=1> \n") 
        a.append("<tr><td class=\"c1\"><H3>Files:</H3></td><td colspan=\"2\"></td></tr>\n")
        for line in getFileItems:
            a.append("<tr><td>" + str(line[0]) + "</td><td>" + str(line[1]) + "</td><td>" + str(line[2]) + "</td></tr>\n")

        a.append("</TABLE>\n")
        a.append("<P>\n")

        a.append("<TABLE id=\"ident\" border=1> \n")    
        a.append("<tr><td class=\"c1\"><H3>Users:</H3></td><td colspan=\"5\"></td></tr>\n")
        for line in getUserItems:
            a.append("<tr><td>" + str(line[0]) + "</td><td>" + str(line[1]) + "</td><td>" + str(line[2]) + "</td><td>" + str(bool(line[3])) + "</td><td>" + str(bool(line[4])) + "</td></tr>\n")

        a.append("</TABLE>\n")
        a.append("<P>\n")

        a.append("<TABLE id=\"acc\" border=1> \n")    
        a.append("<tr><td class=\"c1\"><H3>Access:</H3></td><td colspan=\"2\"></td></tr>\n")
        for line in getAccessItems:
            a.append("<tr><td>" + str(line[0]) + "</td><td>" + str(line[1]) + "</td><td>" + str(line[2]) + "</td></tr>\n")

        a.append("</TABLE>\n")
        a.append("<P>\n")
        a.append("</DIV>")

        a.append("</BODY>\n</HTML>")
        return a

    @cherrypy.expose
    def putHash(self, file):
        if (file == ""):
            return("<form action=\"index\">Field File must no be empty<P><input value=\"back\" type=\"submit\" /></form>")

        hashSHA256 = hashlib.sha256(file).hexdigest()
        salt = hashlib.sha256(os.urandom(32)).hexdigest()

        ### Debug start ###
        print("hashSHA256: ", hashSHA256)
        print("salt: ", salt)
        ### Debug end  ###

        d1 = long(hashSHA256,16)
        d2 = long(salt,16)

        hashX = hex(d1 ^ d2).rstrip("L").lstrip("0x")
        print(file, hashX)

        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                con.execute("INSERT INTO Files (hash, url) VALUES (?, ?)", [hashX, file])
        except Exception as e:
           return e

        return self.index()

    @cherrypy.expose
    def addUser(self, user, certhash):
        if (user == "" or certhash == ""):
            return self.errorMsg("User and Cert Hash") 

#            return("<form action=\"index\">Fields User nor CertHash must no be empty<P><input value=\"back\" type=\"submit\" /></form>")

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
    def upFile(self, upFile=""):
        if (upFile == ""):
            return("<form action=\"index\">Field must no be blank<P><input value=\"back\" type=\"submit\" /></form>")

        ### no, you will not inject some strange paths here !
        if ( upFile.find("/") or upFile.find("\\") ):
            return("<form action=\"index\">Invalid Filename<P><input value=\"back\" type=\"submit\" /></form>")

        ### Upload File to Server ############################################################################################
        upload_path = os.path.join(os.path.dirname(__file__),"/files/")
        upload_file = os.path.normpath(os.path.join(upload_path, upFile))
        size = 0
        try:
            with open(upload_file, 'wb') as out:
                while True:
                    data = ufile.file.read(8192)
                    if not data:
                        break
                    out.write(data)
                    size += len(data)
        except Exception as e:
            return e

        return self.putHash(upFile)

    @cherrypy.expose
    def grantAccess(self, userID, fileID):
        if (userID=="" or fileID == "" ):
            return("<form action=\"index\">Fields UserID nor FileID must no be blank<P><input value=\"back\" type=\"submit\" /></form>")

        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                cred=con.execute("GET expire_date FROM Access where fileID=?", [fileID]).fetchone()
                con.execute("INSERT INTO Access (fileID, userID, expire_date) VALUES (?, ?, ?)", [fileID, userID, cred[0]])
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
