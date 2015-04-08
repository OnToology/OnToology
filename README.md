# auton
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
1. From the website, you only have to put the repo as user/repo i.e. AutonTool/auton (now it doesnot work with organization, for more technical info please refere to the issues section).
2. Update/create auton.cfg (will use default configurations otherwise)
3. Update your repo and push.
4. Go to your repo setting -> webhooks and service and you will see the webhook. you can also click on the webhook link to see the request sent and the server replies.
5. If pull requests are created successfully you can find them in the pull requests pool.

**Please only use this with testing repos**



###The configuration file (the parameters in the configuration file is not finalized), if not included the system will use default configuration




### used python libraries:
* django
* pygithub
* mongoengine
* rdfxml (http://infomesh.net/2003/rdfparser/)
* requests


###Install the libraries using pip
```
pip install django
pip install pygithub
pip install mongoengine
pip install requests
```
rdfxml (can be downloaded from http://infomesh.net/2003/rdfparser/)


To install pip follow the instructions here https://pip.pypa.io/en/latest/installing.html


###Requirements guide (if you want to try in locally)
* python 2.7 to be installed.
* git to be installed.
* curl to be installed.
* ar2dtool to be installed https://github.com/idafensp/ar2dtool.
* Widoco to be installed https://github.com/dgarijo/Widoco.
* the above libraries to be installed (I recommend using pip to install them).
* linux/unix operating system (it may work on Windows with after some adjustments).
* You have to set environment variables.

note: you may need to change some of the hardcoded variables, since the system still in early stange



##Take a peek on the system
* The system is currently host on the development server http://54.172.63.231/ 






