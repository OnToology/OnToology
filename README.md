# auton
A system to automate part of the collaborative ontology development process. Given a repository with an owl file, Auton will survey it and produce diagrams, a complete documentation and validation based on common pitfalls.

Creator: Ahmad Alobaid

Contributors: Daniel Garijo, Oscar Corcho, Maria Poveda

The description of the project and the live development are being documented here: https://docs.google.com/document/d/1q8YT9PsgD4aLC-M0HIf2epQ0G6z0sKQuyHahVjNQdCE/edit#heading=h.k152uv43uqte





##What the system does now:
* Add AutonUser as collaborator
* Add webhooks
* Fork project to AutonUser
* Update readme file
* Create a pull request


Currently the website link is http://54.172.63.231/

##How to use it 
1-From the website, you only have to put the repo as user/repo i.e. AutonTool/auton.
2-Update your repo and push
3-Go to your repo setting -> webhooks and service and you will see the webhook. you can also click on the webhook link to see the request sent and the server replies.
4-If pull requests are created successfully you can find them in the pull requests pool

**Please only use this with testing repos**







### used python libraries:
* django
* pygithub
* mongoengine


##Requirements guide (if you want to try in locally)
* python to be installed
* curl to be installed
* the above libraries to be installed (I recommed using pip to install them)

note: you may need to change some of the hardcoded variables, since the system still in early stange


##Take a peek on the system
* The system is currently host on the development server http://54.172.63.231/ 






