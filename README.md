# blindshare

Ok folks this is just a very alpha state version of Blindshare  
The idea is to provide your friends/folks with just a Hash-String that represent a single file you want to share  
They will then be able to surf to a Blindshare site, enter the hash and receive the file.  

Blindshare consists of two CherryPy Python scriptst:
- admin.py  - The Administration dashboard
- server.py - The actual web serving process frontend you'll talk to to obtain any files.

 
##Prerequisites:##

Sqlite3
Python  
Cherrypy (either by OS rpm/dep or from github: https://github.com/cherrypy/cherrypy )

git (in case you use the github version)  
docker (in case you want to containerize)  

(The Docker stuff is currently missing ... sorry ... stay tuned)

##Usage:##

Use the mk to create a fresh and empty database. Place db in the db subfolder. Or you'll need to modify your config files to match your db's path.  

Make sure you've created some ssl cert's or use pre-existing ones by specifying their location in the config files. 

__Start the Blindshare-Web-Admin console:__
```python admin.py ```

The web console is now available under: https://<hostname>:9090
Place all file you like to share under the "files" dirctory. Or specify a different location within your config files.  
Use the Admin console to add files you like to share. The hash will be calculated automatically.  

__Launch the Blindshare-Server:__
```python server.py```

The Server is now available under https://<hostname>:8080  
Either surf to the website and enter your hash, or use a direct link: https://<hostname>:8080/getHash?item=<hash value>  
