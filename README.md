# blindshare

Version: 0.1 - 19.02.2020

Ok folks this is just a very alpha state version of Blindshare  
The idea is to provide your friends/folks with just a Hash that represent a single file you want to share  
They will then be able to surf to a Blindshare site, enter the hash and receive the file.  
To add some additional security, the file you'll receive is composed from the hash value (as filename) plus the suffix of the original file  

Prerequisites:

Python3  
Cherrypy (either by OS rpm/dep or from github: https://github.com/cherrypy/cherrypy )

git (in case you use the github version)  
docker (in case you want to containerize)  

To do's:  
Fix code ;)  
Add TLS for the Server  
Add TLS Client Cert verification (maybe)  
Add checks for expire_date  
Add global config for the Python scripts  
Make the whole project "Docker ready"  
Testing  

