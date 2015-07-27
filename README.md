# ![alt text](https://raw.githubusercontent.com/OnToology/OnToology/master/ontoology.png "OnToology")
A system to automate part of the collaborative ontology development process. Given a repository with an owl file, Auton will survey it and produce diagrams, a complete documentation and validation based on common pitfalls.

Creator: Ahmad Alobaid

Contributors: Daniel Garijo, Oscar Corcho, Maria Poveda

The description of the project and the live development are being documented here: https://docs.google.com/document/d/1q8YT9PsgD4aLC-M0HIf2epQ0G6z0sKQuyHahVjNQdCE/edit#heading=h.k152uv43uqte




###What the system does now:
* Ask user for permission.
* Add AutonUser as collaborator.
* Add webhooks.
* Fork project to AutonUser.
* Draw two kinds of diagrams from rdf files using ar2dtool (https://github.com/idafensp/ar2dtool).
* Create a documentation of the ontology using Widoco tool (https://github.com/dgarijo/Widoco).
* Validate the ontology using OOPS tool and generate a summary of the issues found by OOPS (http://oops-ws.oeg-upm.net/).
* Create a pull request.



###How to use it 
1. From the website, you only have to put the repo as user/repo i.e. myuser/myrepo (now it doesnot work with organization, for more technical info please refere to the issues section).
2. Update/create auton.cfg (will use default configurations otherwise)
3. Update your repo and push.
4. Go to your repo setting -> webhooks and service and you will see the webhook. you can also click on the webhook link to see the request sent and the server replies.
5. If pull requests are created successfully you can find them in the pull requests pool.

**Please only use this with testing repos**



### used python libraries:
* django
* pygithub
* mongoengine
* rdfxml (http://infomesh.net/2003/rdfparser/)
* requests


###Install the libraries using pip
```
pip install -r requirements.txt
```
Note: you must navigate to the requirements.txt using the "cd" command

rdfxml (can be downloaded from http://infomesh.net/2003/rdfparser/)
note: I modified rdfxml to return a dictionary rather than a string, to see 
the modification go the rdfxml.py file you will see the original Sink commented out
 and right beneath it is my Sink function

To install pip follow the instructions here https://pip.pypa.io/en/latest/installing.html


###Requirements guide (if you want to try in locally)
* python 2.7 to be installed.
* git to be installed.
* curl to be installed.
* AR2DTool to be installed https://github.com/idafensp/ar2dtool.
* Widoco to be installed https://github.com/dgarijo/Widoco.
* the above libraries to be installed (I recommend using pip to install them).
* linux/unix operating system (it may work on Windows with after some adjustments).
* You have to set environment variables.

note: you may need to change some of the hardcoded variables, since the system still in early stage

##Working with Multiple ssh keys
At some point, you may need to perform tests locally (django tests), you may need 
to have multiple ssh keys for github at the same time. If so there is good example on
how to do them 
 http://techamad.blogspot.com.es/2015/05/github-with-multiple-keys.html or
 https://gist.github.com/jexchan/2351996

##Take a peek on the system
* The system is currently host on the development server http://ontoology.linkeddata.es/ 

##How to deploy the on your server
(To be written later)




