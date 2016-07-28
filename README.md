# ![alt text](https://raw.githubusercontent.com/OnToology/OnToology/master/ontoology.png "OnToology")
A system to automate part of the collaborative ontology development process. Given a repository with an owl file, **OnToology** will survey it and produce diagrams, a complete documentation and validation based on common pitfalls.

You can find a live version of OnToology online: http://ontoology.linkeddata.es.

Creator: Ahmad Alobaid

Contributors: Daniel Garijo, Oscar Corcho, Maria Poveda

License: Apache License v2 (http://www.apache.org/licenses/LICENSE-2.0)


###Project Plan
* Provide a better solution for handling private and public repos.
* Add new features (e.g. integrate with GitLab and Bitbucket)
* Deploy on the live server (now on a testing server)
* Prepare automated testing (in progress)



###What the system does now:
* Draw two kinds of diagrams from rdf files using ar2dtool (https://github.com/idafensp/ar2dtool).
* Create a documentation of the ontology using Widoco tool (https://github.com/dgarijo/Widoco).
* Validate the ontology using OOPS tool and generate a summary of the issues found by OOPS (http://oops-ws.oeg-upm.net/).
* Generate a landing page using vocabLite (https://github.com/dgarijo/vocabLite).
* Publish the ontology (content negotiation)


###How to use it 
1. From the website, you only have to put the repo as user/repo i.e. myuser/myrepo (now it doesnot work with organization, for more technical info please refere to the issues section).
2. Update/create OnToology.cfg (will use default configurations otherwise)
3. Update your repo and push.
4. Go to your repo setting -> webhooks and service and you will see the webhook. you can also click on the webhook link to see the request sent and the server replies.
5. If pull requests are created successfully you can find them in the pull requests pool.


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


##Tests
ID | Test Case | Expected Result  | Status
:--|:---------:|:---------------: | :----:
1  | Adding non-existing repo | shouldn't add the non-existing repo and should add an error page | :heavy_check_mark:
2  | Very large ontology | To show error message | :warning: (takes literally days to perform the test, we are going to ignore this)
3  | Ontology with syntax error | To show error message | :heavy_minus_sign:
4  | If a tool is not able to generate an output | should not stop, should proceed with the other tools | :heavy_minus_sign:  
5  | Add a new repo | should be added | :heavy_minus_sign:
6  | Adding a repo that already added | should be accepted | :heavy_minus_sign:
7  | Add a new repo, then delete this repo from github and try to do some actions e.g. generate previsualization | should run the action without problems | :heavy_minus_sign:
8  | Generate previsualization | should be regenerated | :heavy_minus_sign: 


Sign | Meaning
:---:| :-----:
:heavy_minus_sign: | Test automation is not implemented
:heavy_check_mark: | Test automation is completed
:warning:          | Warning



##How to deploy the on your server
On Ubuntu server: 

1. Python 2.7
2. Java
3. Install Git 2.*. [here](http://askubuntu.com/questions/571549/git-1-7-9-5-upgrade-to-current-release-of-git-2-x-on-ubuntu-12-04)
4. Install Apache2.
5. Install mod_wsgi and enable the site. [here](https://www.digitalocean.com/community/tutorials/installing-mod_wsgi-on-ubuntu-12-04)
6. Install mod-wsgi for apache ```sudo apt-get install libapache2-mod-wsgi```
7. Install pip ```sudo apt-get install python-pip```
8. Install mongodb ```sudo apt-get install mongodb```
9. Install app requirements ```pip install -r requirements.txt```
10. Add Widoco and Ar2dTool folders and fix the default configuration files

####Environment variables that need to be set

```
export github_username=xxxxxx
export github_password=xxxxxxx
export github_repos_dir=/xxx/xxx/xxx/temp/
export ar2dtool_dir=/xxxx/xxxx/xxxx/xxx/ar2dtool/bin/
export ar2dtool_config=/xxxx/xxxx/xxxx/config/
export widoco_dir=/xxxxx/xxxx/xxxx/Widoco/JAR/
export SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
export user_github_username=xxx@xxxxx.xxx
export user_github_password=xxxxxx
export test_repo=xxx/xxx
export test_folder=xxx/xxx/xxx
export test_ont_hl=xxx/xxx
export test_ont_nl=xxx/xxx
export tests_ssh_key=/xxx/.xxx/id_rsa_xxx
export test_github_username=xxx@xxx.xxx
export test_github_password=xxx
export client_id_login=xxxxxxx
export client_id_public=xxxxxxxxxx
export client_id_private=xxxxxxxxxx
export client_secret_login=xxxxxxxxxx
export client_secret_public=xxxxxxxxxxxx
export client_secret_private=xxxxxxxxxxx
```
Or you can set them in apache e.g. ``` SetEnv github_username OnToologyUser```


