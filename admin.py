#!/usr/bin/python3

import cherrypy
import sqlite3
import hashlib
import os
from base64 import b64encode

class BlindShareAdmin(object):

    @cherrypy.expose
    def index(self):
        a = []
        a.append("<HTML><TITLE>Blindshare</TITLE>")
        a.append("<BODY><H1> Welcom to BlindShare Web-Admin-Console - ver. 0.1</H1>")
        a.append("<p>")
        a.append("<TABLE border=1>")
       
        with sqlite3.connect('blinds.db') as con:
            getAllItems = con.execute("SELECT * FROM hashtable ORDER BY url").fetchall()

        a.append("<H3>Add File</H3><P>")
        a.append("<form action=\"putHash\" method=\"POST\">File: <input type=\"text\" name=\"file\" /><P><input value=\"add\" type=\"submit\" /></form>")

        a.append("<HR>")
        a.append("<H3>Delete Hash</H3><P>")
        a.append("<form action=\"delHash\" method=\"POST\">Hash: <input type=\"text\" name=\"hash\" /><P><input type=\"submit\" /></form>")

        a.append("<HR>")
        for line in getAllItems:
            a.append("<tr><td>" + str(line[0]) + "</td><td>" + str(line[1]) + "</td><td>" + str(line[2]) + "</td></tr>")

        a.append("</TABLE>")

        a.append("</BODY></HTML>") 
        return a

    @cherrypy.expose
    def putHash(self, file):
        if (file == ""):
            return("<form action=\"index\">Field must no be empty<P><input value=\"back\" type=\"submit\" /></form>")

#        hashSHA256 = array.array('B', (hashlib.sha256(file).hexdigest()) )

        hashSHA256 = hashlib.sha256(file).hexdigest()
        salt = hashlib.sha256(os.urandom(32)).hexdigest()

#        salt = array.array('B', (os.urandom(64)) ) 

#        X = []
#        for i in range(64):
#            X.append(hex(hashSHA256[i] ^ salt[i])[2:] )
#
#        print(X)
#        hashX = ''.join(X)

#        hashX = hashSHA256 ^ salt

        hashX = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(hashSHA256, salt))
        print(hashX)

        with sqlite3.connect('blinds.db') as con:
            con.execute("INSERT INTO hashtable (hash, url) VALUES (?, ?)", [hashX, file])

        return("<form action=\"index\">New entry submitted<P><input value=\"back\" type=\"submit\" /></form>")

    @cherrypy.expose
    def delHash(self, hash):
        if (hash == ""):
            return("<form action=\"index\">Field must no be blank<P><input value=\"back\" type=\"submit\" /></form>")

        with sqlite3.connect('blinds.db') as con:
            con.execute("DELETE FROM hashtable WHERE hash=?", [hash])

        return("<form action=\"index\">Entry deleted<P><input value=\"back\" type=\"submit\" /></form>")

    @cherrypy.expose
    def default(self):
      raise cherrypy.HTTPRedirect('index')
    default.exposed = True

if __name__ == '__main__':
    configfile = os.path.join(os.path.dirname(__file__),'config','admin.conf')
    cherrypy.quickstart(BlindShareAdmin(),config=configfile)
