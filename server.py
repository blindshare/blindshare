#!/usr/bin/python3

import cherrypy
import sqlite3
import os
import sys

class BlindShare(object):

    @cherrypy.expose
    def index(self):
        cherrypy.session.load()
        headers = cherrypy.request.headers
        print(headers)
        ClientCertSha1Fingerprint = str(headers.get('X-Ssl-Cert'))
        ClientCertSha1Fingerprint = "123456"
        cherrypy.session['ClientCertSha1Fingerprint'] = ClientCertSha1Fingerprint
        try:
            with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
                helloUser, = con.execute("SELECT name FROM Identities where certFingerprint=?", [ClientCertSha1Fingerprint]).fetchone()
                userID, = con.execute("SELECT userID FROM Identities where certFingerprint=?", [ClientCertSha1Fingerprint]).fetchone()
                cherrypy.session['userID'] = userID
                downloadItems = con.execute("SELECT Files.hash, Files.fileObj, Access.expire_date, Identities.name as origin FROM Files \
                                             INNER JOIN Identities on Identities.userID = Access.userID \
                                             INNER JOIN Access on Access.fileID = Files.fileID").fetchall()
        except:
            pass

        a = []
        a.append("<!DOCTYPE html> \n")
        a.append("<HTML><TITLE>Blind Share</TITLE>\n")
        a.append("<BODY>\n")
        a.append("<H1>Blind Share - ver 0.5</H1>\n")
        a.append("<HR>\n")
        a.append("Clients Cert sha1 Fingerprint: " + ClientCertSha1Fingerprint + "\n")
        a.append("<HR>\n")
        a.append("<H2>Hallo " + helloUser + "</H2><BR>\n")
        a.append("<form action=\"getFileObj\" method=\"GET\">Please insert hash: <input type=\"text\" name=\"hashItem\"><input value=\"download\" type=\"submit\"></form>\n")
        a.append("<P>\n")
        a.append("<P>\n")
        a.append("<TABLE border=1>")
        a.append("<TR><TH>File Hash</TH><TH>File</TH><TH>Expires on</TH><TH>Origin</TH></TR>")
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
        a.append("<HTML><TITLE>Blind Share</TITLE>\n")
        a.append("<BODY>\n")
        a.append("<H1>Blind Share - ver 0.5</H1>\n")
        a.append("<HR>\n")
        headers = cherrypy.request.headers
        print(headers)
        ClientCertSha1Fingerprint = headers.get('X-Ssl-Cert')
        a.append("Clients Cert sha1 Fingerprint: \n")
        a.append(ClientCertSha1Fingerprint)
        a.append("<HR>\n")
        a.append("This is a private Content Management Service site NOT a one-click hoster<P>\n")
        a.append("If you see this text, access to this site has not been granted or any sharing of public content has been disabled.\n")
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

        with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
            isOriginator, = con.execute("SELECT CASE WHEN EXISTS ( SELECT origin FROM files where hash =? ) \
                                        THEN CAST(1 AS BIT) \
                                        ELSE CAST(0 AS BIT) \
                                        END", [hashItem]).fetchone()

        userID = str(cherrypy.session.get('userID'))

        with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
#            con.execute("DELETE FROM Access WHERE fileID=? AND userID=?", [fileID, userID])






        print(isOriginator)
        if (isOriginator == True):
           return "you are the originator"

        if (isOriginator == False):
           return "you NOT are the originator"



    @cherrypy.expose
    def getFileObj(self, hashItem=None):
        if (hashItem == "" or hashItem == None):
            return self.error(404)

#        if (len(hashItem) > 64 or len(hashItem <= 63)):
#           return self.error(404) 

        ClientCertSha1Fingerprint = cherrypy.session.get('ClientCertSha1Fingerprint')
        print("Client: " + str(ClientCertSha1Fingerprint) + " downloading: " + hashItem)

        with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
            fileObj, = con.execute("SELECT Files.fileObj FROM Files \
                                    INNER JOIN Identities on Identities.userID = Access.userID \
                                    INNER JOIN Access on Access.fileID = Files.fileID \
                                    WHERE Identities.certFingerprint = ? \
                                    AND Files.hash = ? \
                                    AND (date('now') <= date(Access.expire_date)) OR Access.expire_date IS NULL OR expire_date IS \"\"", [ClientCertSha1Fingerprint, hashItem]).fetchone()


            userID = str(cherrypy.session.get('userID'))
            d_path = cherrypy.request.app.config['cfg']['filesPath']

            uri = os.path.join(cherrypy.request.app.config['cfg']['filesPath'], userID, fileObj)
            return cherrypy.lib.static.serve_file(uri, 'application/x-download', 'attachment', fileObj)

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
