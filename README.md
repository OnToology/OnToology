# ![alt text](https://raw.githubusercontent.com/OnToology/OnToology/master/ontoology.png "OnToology")
A system to automate part of the collaborative ontology development process. Given a repository with an owl file, Auton will survey it and produce diagrams, a complete documentation and validation based on common pitfalls.

Creator: Ahmad Alobaid

Contributors: Daniel Garijo, Oscar Corcho, Maria Poveda


###Project Plan
* Provide a better solution for handling private and public repos.
* Docker setup
* Use front-end framework (e.g. AngularJS)
* Add new features (e.g. integrate with GitLab)
* Deploy on the live server (now on a testing server)
* Prepare automated testing



###What the system does now:
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


##Working with Multiple ssh keys
At some point, you may need to perform tests locally (django tests), you may need 
to have multiple ssh keys for github at the same time. If so there is good example on
how to do them 
 http://techamad.blogspot.com.es/2015/05/github-with-multiple-keys.html or
 https://gist.github.com/jexchan/2351996

##Take a peek on the system
* The system is currently host on the development server http://ontoology.linkeddata.es/ 

##Tests
ID | Test Case | Expected Result  | Status
:--|:---------:|:---------------: | :----:
1  | Adding non-existing repo | shouldn't add the non-existing repo and should add an error page | :heavy_check_mark:
2  | Very large ontology | To provide an error message | :heavy_minus_sign:
3  | Ontology with syntax error | To provide an error message | :heavy_minus_sign:
 

Sign | Meaning
:---:| :-----:
:heavy_minus_sign: | Test is not implemented
:heavy_check_mark: | Test is completed
:exclamation:      | Not working perfectly


##How to deploy the on your server
(To be written later)




