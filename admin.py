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
        a.append("<TABLE id=\"t1\"> \n")
        a.append("<tr><td colspan=\"6\"><HR></td></tr>\n")
        a.append("<tr><td><H3>Add User</H3></td><td></td><td></td><td></td><td><H3>Remove User</H3></td><td></td></tr>\n")
        a.append("<tr class=\"line\"><td><form action=\"addUser\" method=\"POST\">User: <input type=\"text\" name=\"user\"></td><td>Cert Hash: <input type=\"text\" name=\"certhash\"></td><td><input value=\"add\" type=\"submit\"></form></td><td class=\"spacer\"></td>\n")
        a.append("<td><form action=\"delUser\" method=\"POST\">User ID: <input type=\"text\" name=\"userID\"></td><td><input value=\"del\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"6\"><HR></td></tr>\n")
        a.append("<tr><td><H3>Update visibility</H3></td><td></td><td></td><td></td><td><H3>Remove File</H3></td><td></td></tr>\n")
        a.append("<tr class=\"line\"><td>Show Files: <input type=\"checkbox\" name=\"view\" value=\"1\">Upload: <input type=\"checkbox\" name=\"upload\" value=\"1\"></td><td></td><td><input value=\"update\" type=\"submit\"></form></td><td></td>\n")
        a.append("<td><form action=\"delFile\" method=\"POST\">File ID: <input type=\"text\" name=\"fileID\"></td><td><input value=\"del\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"6\"><HR></tr>\n")
        a.append("<tr><td><H3>Edit expiration date</H3></td><td></td><td></td><td></td><td></td><td></td></tr>\n")
        a.append("<tr calss=\"line\"><td><form action=\"expire\" method=\"POST\">Expiration date: <input type=\"text\" name=\"exp\"></td><td></td><td><input value=\"set\" type=\"submit\"></form></td><td></td><td></td><td></td></tr>\n")
        a.append("<tr><td colspan=\"6\"><HR></td></tr>\n")
        a.append("<tr><td><H3>Update Hash</H3></td><td></td><td></td><td></td><td><H3>Upload File</H3></td><td></td></tr>\n")
        a.append("<tr id=\"line\"><td><form action=\"upHash\" method=\"POST\">File ID: <input type=\"text\" name=\"fileID\"></td><td>Hash: <input type=\"text\" name=\"hash\"></td><td><input value=\"update\" type=\"submit\"></form></td><td></td>\n")
        a.append("<td><form action=\"upFile\" method=\"POST\">Upload File: <input type=\"text\" name=\"upFile\"></td><td><input value=\"upload\" type=\"submit\"></form></td></tr>\n")
        a.append("<tr><td colspan=\"6\"><HR></td></tr>\n")
        a.append("<tr><td><H3>Files:</H3><td></td><td></td><td></td><td><H3>Users:</H3></td><td></td></tr>\n")
        a.append("</TABLE>\n")

        a.append("<TABLE id=\"t2\"> \n") 
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
