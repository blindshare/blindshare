#!/usr/bin/python3

import cherrypy
import sqlite3
import hashlib
import os

class BlindShareAdmin(object):

    @cherrypy.expose
    def index(self):
        a = []
        myDB = os.path.join(cherrypy.request.app.config['paths']['db'], 'blinds.db')
        with sqlite3.connect(myDB) as con:
            getAllItems = con.execute("SELECT * FROM hashtable ORDER BY url").fetchall()

        a.append("<!DOCTYPE html> \n <HTML>\n <HEAD>")
        a.append("<link rel=\"stylesheet\" href=\"static/admin.css\">\n")
        a.append("<TITLE>Blindshare</TITLE>\n")
        a.append("</HEAD>\n <BODY><H1> Welcom to BlindShare Web-Admin-Console - ver. 0.5</H1>\n")
        a.append("<p>\n")
#        a.append("<TABLE id=\"t1\" border=\"1\" > \n")
        a.append("<TABLE id=\"t1\"> \n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Add User</H3></td><td class=\"spacer\"></td><td colspan=\"6\"><H3>Remove User</H3></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"addUser\" method=\"POST\">Username:</td><td class=\"c1\"></td><td><input type=\"text\" name=\"user\"></td><td>Cert Hash:</td><td><input type=\"text\" name=\"certhash\"></td><td></td><td><input value=\"add\" type=\"submit\"></form></td><td class=\"spacer\"></td>\n")
        a.append("<td class=\"c2\"><form action=\"delUser\" method=\"POST\">User ID:</td><td class=\"c1\"></td><td><input class=\"ids\" type=\"text\" name=\"userID\"></td><td></td><td></td><td><input value=\"del\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></td></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Update visibility</H3></td><td class=\"spacer\"></td><td colspan=\"6\"><H3>Remove File</H3></td></tr>\n")
        a.append("<tr><td class=\"c2\">Show Files: <input type=\"checkbox\" name=\"view\" value=\"1\"></td><td class=\"c1\"></td><td>Upload:<input type=\"checkbox\" name=\"upload\" value=\"1\"></td><td></td><td></td><td></td><td><input value=\"update\" type=\"submit\"></form></td><td class=\"spacer\"></td>\n")
        a.append("<td class=\"c2\"><form action=\"delFile\" method=\"POST\">File ID:</td><td class=\"c1\"></td><td><input class=\"ids\" type=\"text\" name=\"fileID\"></td><td></td><td></td><td><input value=\"del\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"14\"><HR></tr>\n")
        a.append("<tr><td colspan=\"7\"><H3>Edit expiration date</H3></td><td class=\"spacer\"></td><td colspan=\"6\"></td></tr>\n")
        a.append("<tr><td class=\"c2\"><form action=\"expire\" method=\"POST\">Expiration date:</td><td class=\"c1\"></td><td><input type=\"text\" name=\"exp\"></td><td></td><td></td><td></td><td><input value=\"set\" type=\"submit\"></form></td><td class=\"spacer\"></td><td colspan=\"6\"></td></tr>\n")
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

        a.append("<TABLE id=\"t2\"> \n") 
        a.append("<tr><td class=\"c1\"><H3>Files:</H3></td><td colspan=\"3\"><td class=\"c1\"><H3>Users:</H3></td><td colspan=\"3\"></td></tr>\n")
        for line in getAllItems:
            a.append("<tr><td>" + str(line[0]) + "</td><td>" + str(line[1]) + "</td><td>" + str(line[2]) + "</td><td>" + str(line[3]) + "</td></tr>\n")

        a.append("</TABLE>\n")

        a.append("</BODY>\n</HTML>")
        return a

    @cherrypy.expose
    def putHash(self, file, exp=""):
        if (file == ""):
            return("<form action=\"index\">Field must no be empty<P><input value=\"back\" type=\"submit\" /></form>")

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

        myDB = os.path.join(cherrypy.request.app.config['paths']['db'], 'blinds.db')
        with sqlite3.connect(myDB) as con:
            con.execute("INSERT INTO hashtable (hash, url, expire_date) VALUES (?, ?, ?)", [hashX, file, exp])

        return self.index()

    @cherrypy.expose
    def delHash(self, hash):
        if (hash == ""):
            return("<form action=\"index\">Field must no be blank<P><input value=\"back\" type=\"submit\" /></form>")

        myDB = os.path.join(cherrypy.request.app.config['paths']['db'], 'blinds.db')
        print(myDB)
        with sqlite3.connect(myDB) as con:
            con.execute("DELETE FROM hashtable WHERE hash=?", [hash])

        return self.index()

    @cherrypy.expose
    def default(self):
      raise cherrypy.HTTPRedirect('index')
    default.exposed = True

if __name__ == '__main__':
    configfile = os.path.join(os.path.dirname(__file__),'config','admin.conf')
    cherrypy.quickstart(BlindShareAdmin(),config=configfile)
