#!/usr/bin/python3

import cherrypy
import sqlite3
import hashlib
import os

class BlindShareAdmin(object):

    @cherrypy.expose
    def index(self):
        a = []
        a.append("<HTML><TITLE>Blindshare</TITLE>")
        a.append("<BODY><H1> Welcom to BlindShare Web-Admin-Console - ver. 0.3</H1>")
        a.append("<p>")
        a.append("<TABLE border=1>")
       
        myDB = os.path.join(cherrypy.request.app.config['paths']['db'], 'blinds.db')        
        with sqlite3.connect(myDB) as con:
            getAllItems = con.execute("SELECT * FROM hashtable ORDER BY url").fetchall()

        a.append("<H3>Add File</H3><P>")
        a.append("<form action=\"putHash\" method=\"POST\">File: <input type=\"file\" name=\"file\" />Expiration date: <input type=\"text\" name=\"exp\" /><P><input value=\"add\" type=\"submit\" /></form>")

        a.append("<HR>")
        a.append("<H3>Delete Hash</H3><P>")
        a.append("<form action=\"delHash\" method=\"POST\">Hash: <input type=\"text\" name=\"hash\" /><P><input type=\"submit\" /></form>")

        a.append("<HR>")
        for line in getAllItems:
            a.append("<tr><td>" + str(line[0]) + "</td><td>" + str(line[1]) + "</td><td>" + str(line[2]) + "</td><td>" + str(line[3]) + "</td></tr>")

        a.append("</TABLE>")

        a.append("</BODY></HTML>") 
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
