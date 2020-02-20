# blindshare

Ok folks this is just a very alpha state version of Blindshare  
The idea is to provide your friends/folks with just a Hash-String that represent a single file you want to share  
They will then be able to surf to a Blindshare site, enter the hash and receive the file.  

Blindshare consists of two CherryPy Python scriptst:
- admin.py  - The Administration dashboard
- server.py - The actual web serving process frontend you'll talk to to obtain any files.

 
Prerequisites:

Sqlite3
Python  
Cherrypy (either by OS rpm/dep or from github: https://github.com/cherrypy/cherrypy )

git (in case you use the github version)  
docker (in case you want to containerize)  

(The Docker stuff is currently missin ... sorry ... stay tuned)
