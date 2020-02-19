#!/usr/bin/python3

import cherrypy
import sqlite3
import os
import sys

class BlindShare(object):

    @cherrypy.expose
    def index(self):
        a = []
        a.append("<HTML><TITLE>Blind Share</TITLE>")
        a.append("<BODY>")
        a.append("<H1>Blind Share - ver 0.2</H1>")
        a.append("<HR>")
        a.append("<form action=\"getHash\" method=\"POST\">Please insert hash: <input type=\"text\" name=\"item\" /><input value=\"get\" type=\"submit\" /></form>")
        return a

    @cherrypy.expose
    def getHash(self, item=None):
        if item:
            print(str(len(item)) + "size")
            if (len(item) > 64):
                return self.error(404) 
            else:
                try:
                    with sqlite3.connect('blinds.db') as con:
                        file, = con.execute("SELECT url FROM hashtable WHERE hash=?", [item]).fetchone()
                        print("------------------")
                        path = os.path.join(cherrypy.request.app.config['file_path']['path'], file)
                        print("file:" + file)
                        return cherrypy.lib.static.serve_file(path, 'application/x-download', 'attachment', file)
#                        return self.download(item, file)
                except:
                    e = sys.exc_info()
                    print(e)
        else:
            return self.error(404)

#    @cherrypy.expose
#    def download(self, item, file):
#        if (file == ""):
#            return self.error(404)
#        else:
#            suffix = os.path.splitext(file)
#            newFileName = item + suffix[-1]
#            path = os.path.join(cherrypy.request.app.config['file_path']['path'], file) 
#            print(path)
#            return cherrypy.lib.static.serve_file(path, 'application/x-download', 'attachment', newFileName)


    @cherrypy.expose
    def error(self, err):
        if (err == 404):
            fnf = []
            fnf.append("<HTML><TITLE>Blind Share</TITLE>")
            fnf.append("<H1>404 - File not Found</H1>")
            fnf.append("<P>")
            fnf.append("Your item was not found or you link has expired")
            fnf.append("<HR>")
            fnf.append("<HTML><form action=\"index\" method=\"POST\"><input value=\"back\" type=\"submit\" /></form>")
            return fnf

    @cherrypy.expose
    def default(self):
      raise cherrypy.HTTPRedirect('index')
    default.exposed = True

if __name__ == '__main__':
    configfile = os.path.join(os.path.dirname(__file__),'config','server.conf')
    cherrypy.quickstart(BlindShare(),config=configfile)
