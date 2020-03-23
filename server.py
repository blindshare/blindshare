#!/usr/bin/python3

import cherrypy
import sqlite3
import os
import sys

class BlindShare(object):

    @cherrypy.expose
    def index(self):
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
        a.append("<form action=\"getHash\" method=\"GET\">Please insert hash: <input type=\"text\" name=\"item\" /><input value=\"get\" type=\"submit\" /></form>\n")
        a.append("</BODY></HTML>\n")

        with sqlite3.connect(cherrypy.request.app.config['cfg']['db']) as con:
            fItems = con.execute("SELECT eID=? AND userID=?", [fileID, userID])

        return a

    @cherrypy.expose
    def index2(self):
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
    def getID(self, ClientCertSha1Fingerprint=""):



    @cherrypy.expose
    def getHash(self, item=None):
        if item:
            if (len(item) > 64):
                return self.error(404) 
            else:
                try:
                    myDB = os.path.join(cherrypy.request.app.config['paths']['db'], 'blinds.db')
                    with sqlite3.connect(myDB) as con:
                        file = con.execute("SELECT url FROM hashtable where ( date('now') <= date(expire_date) OR expire_date IS NULL OR expire_date IS \"\" ) AND hash=?", [item]).fetchone()
                        print(file)
                        path = os.path.join(cherrypy.request.app.config['paths']['filesPath'], file)
                        return cherrypy.lib.static.serve_file(path, 'application/x-download', 'attachment', file)
                except TypeError:
#                    return TypeError
                    return self.error(404)
                except sqlite3.OperationalError:
#                    return sqlite3.OperationalError
                    return self.error(601)
        else:
            return self.error(404)

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
