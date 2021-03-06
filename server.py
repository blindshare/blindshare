#!/usr/bin/python3

import cherrypy
import hashlib
import sqlite3
import os
import sys

class BlindShare(object):

    @cherrypy.expose
    def index(self):
        cherrypy.session.load()
        headers = cherrypy.request.headers
        print(headers)

        ClientCertSha1Fingerprint = str(headers.get('X-Ssl-Cert')).upper()
#        ClientCertSha1Fingerprint = "123456"
        cherrypy.session['ClientCertSha1Fingerprint'] = ClientCertSha1Fingerprint
        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                helloUser, = con.execute("SELECT name FROM Identities where certFingerprint=?", [ClientCertSha1Fingerprint]).fetchone()
                downloadItems = con.execute("SELECT Files.hash, Files.fileObj, Access.expire_date, Files.origin FROM Files \
                                             INNER JOIN Identities on Identities.userID = Access.userID \
                                             INNER JOIN Access on Access.fileID = Files.fileID \
                                             WHERE Identities.certFingerprint = ?",[ClientCertSha1Fingerprint]).fetchall()
                isViewable, = con.execute("SELECT view FROM Identities where certFingerprint=?", [ClientCertSha1Fingerprint]).fetchone()
                isUploadable, = con.execute("SELECT upload FROM Identities where certFingerprint=?", [ClientCertSha1Fingerprint]).fetchone()
        except:
        #    pass
            cherrypy.session['ClientCertSha1Fingerprint'] = "Anonymous"
            return self.index2()

        a = []
        a.append("<!DOCTYPE html> \n")
        a.append("<link rel=\"stylesheet\" href=\"static/server.css\">\n")
        a.append("<HTML><TITLE>Blind Share</TITLE>\n")
        a.append("<BODY>\n")
        a.append("<H1>Blind Share - ver 0.6</H1>\n")
        a.append("<HR>\n")
        a.append("Clients Cert Fingerprint: " + ClientCertSha1Fingerprint + "\n")
        a.append("<HR>\n")
        a.append("<H2>Hallo " + helloUser + "</H2>\n")
        a.append("<BR>\n")
        if (isUploadable == 1):
            a.append("<form action=\"uploadFile\" method=\"POST\" enctype=\"multipart/form-data\">Upload File: <input type=\"file\" name=\"upFile\"><input value=\"upload\" type=\"submit\"></form></td></tr>\n")
            a.append("<BR>\n")
        a.append("<form action=\"getFileObj\" method=\"GET\">Please insert hash: <input type=\"text\" name=\"hashItem\"><input value=\"download\" type=\"submit\"></form>\n")
        a.append("<BR>\n")
        if (isViewable == 1):
            a.append("<TABLE border=1>\n")
            a.append("<TR><TH>File Hash</TH><TH>File</TH><TH>Expires on</TH><TH>Origin</TH></TR>\n")
            try:
                for dwnlItems in downloadItems:
                    a.append("<TR><TD>" + str(dwnlItems[0]) + "</TD><TD>" + str(dwnlItems[1]) + "</TD><TD>" + str(dwnlItems[2]) + "</TD><TD>" + str(dwnlItems[3]) + "</TD><TD><form action=\"upOrDel\" method=\"POST\"><select name=\"usrOps\"><option value=\"download\">Download</option><option value=\"delete\">Delete</option></select><input name=\"hashItem\" value=\"" + str(dwnlItems[0]) + "\" type=\"hidden\"><input value=\"Go\" type=\"submit\"></form></TD></TR>\n")     
            except:
                pass

            a.append("</TABLE>\n")
        a.append("</BODY></HTML>\n")

        return a


    @cherrypy.expose
    def index2(self):
        cherrypy.session.load()
        a = []
        a.append("<!DOCTYPE html> \n")
        a.append("<link rel=\"stylesheet\" href=\"static/server.css\">\n")
        a.append("<TITLE>Blind Share</TITLE>\n")
        a.append("<HEAD>\n<style>\n")
        a.append("DIV {\n")
        a.append("text-align: center;")
        a.append("}\n</style>\n")
        a.append("<BODY>\n")
        a.append("<H1>Blind Share - ver 0.6</H1>\n")
        a.append("<HR>\n")
        headers = cherrypy.request.headers
        print(headers)
        ClientCertSha1Fingerprint = headers.get('X-Ssl-Cert')
        a.append("Clients Cert Fingerprint: \n")
        a.append(str(ClientCertSha1Fingerprint))
        a.append("<HR>\n")
        a.append("<BR>\n")
        a.append("<DIV>\n")
        a.append("<H1>This is a private Content Management Service site NOT a one-click hoster</H1><BR>\n")
        a.append("<BR>\n")
        a.append("If you see this text, access to this site has not been granted or any sharing of public content has been disabled.\n")
        a.append("</DIV>\n")
        a.append("</BODY></HTML>\n")
        return a


    @cherrypy.expose
    def upOrDel(self, usrOps, hashItem):
        if (usrOps == "download"):
            return self.getFileObj(hashItem) 

        if (usrOps == "delete"):
            return self.delFileObj(hashItem) 


    @cherrypy.expose
    def delFileObj(self, hashItem=None):
        if (hashItem == "" or hashItem == None):
            return self.error(404)

        ClientCertSha1Fingerprint = str(cherrypy.session.get('ClientCertSha1Fingerprint'))

        with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
            origin, = con.execute("SELECT origin from Files WHERE hash = ?", [hashItem]).fetchone()

            isOriginator, = con.execute("SELECT CASE WHEN EXISTS ( SELECT origin FROM files \
                                         INNER JOIN Identities on Identities.userID = Files.origin \
                                         WHERE Files.hash = ? AND Identities.certFingerprint = ? \
                                         AND Files.origin = Identities.userID) \
                                           THEN CAST(1 AS BIT) \
                                           ELSE CAST(0 AS BIT) \
                                        END", [hashItem, ClientCertSha1Fingerprint]).fetchone()

            del_file, = con.execute("SELECT fileObj from Files \
                                     INNER JOIN Access on Access.fileID = Files.fileID \
                                     INNER JOIN Identities on Identities.userID = Access.userID \
                                     WHERE Files.hash = ? AND Identities.certFingerprint = ? ", [hashItem, ClientCertSha1Fingerprint]).fetchone()

            print("origin: " + str(origin) + " - is Originator: " + str(isOriginator) + " - File to delete: " + del_file)
        
            con.execute("DELETE FROM access WHERE (Access.fileID, Access.userID) in \
                         ( SELECT Access.fileID, Access.userID FROM Access \
                           INNER JOIN Files on Files.fileID = Access.fileID \
                           INNER JOIN Identities on Identities.userID = Access.userID \
                           WHERE Files.hash = ? AND Identities.certFingerprint = ? )", [hashItem, ClientCertSha1Fingerprint] \
                       )

        if (isOriginator == True):
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                con.execute("DELETE FROM Files WHERE hash = ?", [hashItem])
                u_path = cherrypy.request.app.config['cfg']['filesPath']
                rmPath = os.path.normpath(os.path.join(u_path, str(origin)))
                print("del file: " + rmPath +  del_file)
                os.remove(os.path.join(rmPath, del_file))

        return self.index()


    @cherrypy.expose
    def getFileObj(self, hashItem=None):
        if (hashItem == "" or hashItem == None):
            return self.error(404)

        if (len(hashItem) != 64):
            return self.error(404) 

        ClientCertSha1Fingerprint = cherrypy.session.get('ClientCertSha1Fingerprint')
        print("### Client: " + str(ClientCertSha1Fingerprint) + " downloading: " + hashItem)

        with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
            fileObj, = con.execute("SELECT Files.fileObj FROM Files \
                                    INNER JOIN Identities on Identities.userID = Access.userID \
                                    INNER JOIN Access on Access.fileID = Files.fileID \
                                    WHERE Identities.certFingerprint = ? \
                                    AND Files.hash = ? \
                                    AND (date('now') <= date(Access.expire_date) OR Access.expire_date IS NULL OR expire_date IS \"\")", [ClientCertSha1Fingerprint, hashItem]).fetchone()

            origin, = con.execute("SELECT origin from Files WHERE hash = ?", [hashItem]).fetchone()

            uri = os.path.join(cherrypy.request.app.config['cfg']['filesPath'], str(origin), fileObj)
            return cherrypy.lib.static.serve_file(uri, 'application/x-download', 'attachment', fileObj)


    @cherrypy.expose
    def uploadFile(self, upFile):
        if (upFile.filename == ""):
            return ("<form action=\"index\">Field must no be empty<P><input value=\"back\" type=\"submit\"></form>")

        ClientCertSha1Fingerprint = cherrypy.session.get('ClientCertSha1Fingerprint')
        if (ClientCertSha1Fingerprint == ""):
            return ("<form action=\"index\">User not authorized to upload any files<P><input value=\"back\" type=\"submit\"></form>")

        with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
            userID, = con.execute("SELECT userID from Identities where Identities.certFingerprint = ?", [ClientCertSha1Fingerprint]).fetchone()

        u_filename=upFile.filename
        u_path = cherrypy.request.app.config['cfg']['filesPath']
        upload_path = os.path.normpath(os.path.join(u_path, str(userID)) )

        if (os.path.exists(upload_path) == False ):
            return("<form action=\"index\">Upload Path does not exist<P><input value=\"back\" type=\"submit\"></form>")

        ### no, you will not inject some strange paths here !
        if ( "/" in u_filename or "\\" in u_filename ):
            return("<form action=\"index\">Invalid Filename<P><input value=\"back\" type=\"submit\"></form>")

        upload_file = os.path.normpath(os.path.join(upload_path, u_filename))

        size = 0
        with open(upload_file, 'wb') as out:
            while True:
                data = upFile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)

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
            con.execute("INSERT INTO Files (hash, fileObj, origin) VALUES (?, ?, ?)", [hashX, u_filename, userID])
            fileID, = con.execute("SELECT fileID from Files WHERE hash=?", [hashX]).fetchone()
            con.execute("INSERT INTO Access (fileID, userID) VALUES (?, ?)", [fileID, userID])

        return self.index()


    @cherrypy.expose
    def error(self, err):
        if (err == 404):
            erm = []
            erm.append("<HTML><TITLE>Blind Share</TITLE>")
            erm.append("<H1>404 - File not Found</H1>")
            erm.append("<P>")
            erm.append("Your item was not found or you link has expired")
            erm.append("<HR>")
            erm.append("<HTML><form action=\"index\" method=\"POST\"><input value=\"back\" type=\"submit\" /></form>")
            return erm

        if (err == 601):
            erm = []
            erm.append("<HTML><TITLE>Blind Share</TITLE>")
            erm.append("<H1>601 - Database Error</H1>")
            erm.append("<P>")
            erm.append("The Database you like to reach is currently not available or doesn't accept any new connections")
            erm.append("<P>")
            erm.append("<u>Please contact your DBA and try again later</u>")
            erm.append("<HR>")
            return erm


    @cherrypy.expose
    def default(self):
      raise cherrypy.HTTPRedirect('index')
    default.exposed = True

if __name__ == '__main__':
    configfile = os.path.join(os.path.dirname(__file__),'config','server.conf')
    cherrypy.quickstart(BlindShare(),config=configfile)
