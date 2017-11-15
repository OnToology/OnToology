# ![alt text](https://raw.githubusercontent.com/OnToology/OnToology/master/media/icons/logoprop1_readme.png "OnToology")

A system for collaborative ontology development process. Given a repository with an owl file, **OnToology** will survey it and produce diagrams, a complete documentation and validation based on common pitfalls.

You can find a live version of OnToology online: http://ontoology.linkeddata.es.

Team: Ahmad Alobaid, Daniel Garijo, Maria Poveda, Idafen Santa, Oscar Corcho, Alba Fernandez Izquierdo

License: Apache License v2 (http://www.apache.org/licenses/LICENSE-2.0)

![Configuration Status](http://ontoology.linkeddata.es/deploy/conf-pass.png)

<!--


### Project Plan
* Provide a better solution for handling private and public repos.
* Add new features (e.g. integrate with GitLab and Bitbucket)
* Deploy on the live server (now on a testing server)
* Prepare automated testing (in progress)
* Automated tests for pull requests.
* Use decorators for input validation.
* Use profilers.


### What the system does now:
* Draw two kinds of diagrams from rdf files using ar2dtool (https://github.com/idafensp/ar2dtool).
* Create a documentation of the ontology using Widoco tool (https://github.com/dgarijo/Widoco).
* Validate the ontology using OOPS tool and generate a summary of the issues found by OOPS (http://oops-ws.oeg-upm.net/).
* Generate a landing page using vocabLite (https://github.com/dgarijo/vocabLite).
* Publish the ontology (content negotiation)


### How to use it 
1. From the website, you only have to put the repo as user/repo i.e. myuser/myrepo (now it doesnot work with organization, for more technical info please refere to the issues section).
2. Update/create OnToology.cfg (will use default configurations otherwise)
3. Update your repo and push.
4. Go to your repo setting -> webhooks and service and you will see the webhook. you can also click on the webhook link to see the request sent and the server replies.
5. If pull requests are created successfully you can find them in the pull requests pool.

-->


### Install the libraries using pip (or use automatic deployment script)
```
pip install -r requirements.txt
```
Note: you must navigate to the requirements.txt using the "cd" command

rdfxml (can be downloaded from http://infomesh.net/2003/rdfparser/)
note: I modified rdfxml to return a dictionary rather than a string, to see 
the modification go the rdfxml.py file you will see the original Sink commented out
 and right beneath it is my Sink function

To install pip follow the instructions here https://pip.pypa.io/en/latest/installing.html


## Tests (under refactoring)
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




## Auto deployment script

1. Before you run the script check the below variables that most probably you need to change to adapt to your

Things that you might want to change the username and email of git
```
git config --global user.name
git config --global user.email
```

And maybe you want to use the https url instead of git url
```
git clone https://github.com/OnToology/OnToology.git
```

and in the case of git keys, make sure to generate one and add it to OnToologyUser

2. Install git if not installed
```
sudo apt-get install git
```

3. Using the deployment script
```
sudo sh OnToology/deploy.sh
```

4. You may need to fix the permission for www-data (or another user).
This one is kinda trick and there are different ways to do it.
    * Ubuntu and www-data to have the same group number and user number (e.g. /etc/passwd and you can set it there)
    but this might not be the best, but the easiest.
    * Configure a separate user for the application and provide it with the permission of all necessary directories
    things like logs folder, temp folder, ssh key for GitHub.


5. Append environment variables (Below) to virtual environment venv/bin/activate (note: this won't work with apache)

#### Environment variables that you need to set

```
export github_username=OnToologyUser
export github_password=
export github_repos_dir=/home/ubuntu/temp/
export ar2dtool_dir=/home/ubuntu/ar2dtool/bin/
export ar2dtool_config=/home/ubuntu/config/
export widoco_dir=/home/ubuntu/widoco/
export owl2jsonld_dir=/home/ubuntu/owl2jsonld
export SECRET_KEY=
export tools_config_dir=/home/ubuntu/config
export previsual_dir=/home/ubuntu/vocabLite/jar
export wget_dir /home/ubuntu/wget_dir
export client_id_login=
export client_secret_login=
export client_id_public=
export client_secret_public=
export client_id_private=
export client_secret_private=
export publish_dir=/home/ubuntu/publish/

export db_username=
export db_password=
export db_host=
export db_port=

export email_server=""
export email_from=""
export email_username=""
export email_password=""
```

or in the local WSGI file `localwsgi.py`
```
import os
environ = os.environ
environ['github_username']="OnToologyUser"
environ['github_password']=""
environ['github_repos_dir']="/home/ubuntu/temp/"
environ['ar2dtool_dir']="/home/ubuntu/ar2dtool/bin/"
environ['ar2dtool_config']="/home/ubuntu/config/"
environ['widoco_dir']="/home/ubuntu/widoco/"
environ['owl2jsonld_dir']="/home/ubuntu/owl2jsonld"
environ['SECRET_KEY']=""
environ['tools_config_dir']="/home/ubuntu/config"
environ['previsual_dir']="/home/ubuntu/vocabLite/jar"
environ['wget_dir']="/home/ubuntu/temp/wget_dir"
environ['client_id_login']=""
environ['client_secret_login']=""
environ['client_id_public']=""
environ['client_secret_public']=""
environ['client_id_private']=""
environ['client_secret_private']=""
environ['publish_dir']="/home/ubuntu/publish/"

environ['db_username']=""
environ['db_password']=""
environ['db_host']=""
environ['db_port']=""

environ['email_server'] = ""
environ['email_from'] = ""
environ['email_username'] = ""
environ['email_password'] = ""
```



#### External tools used by OnToology
1. [Widoco](http://github.com/dgarijo/Widoco/) 
2. [AR2DTool](http://github.com/idafensp/ar2dtool)
3. [vocabLite](http://github.com/dgarijo/vocabLite/)

Make sure the are located in the same dir as the environment variable e.g. (ar2dtool_dir, widoco_dir) and they can be
executed (x permission is given).

#### Set default configuration files
In the folder that specified in the environment variable ```ar2dtool_config```, include default configuration files for
AR2DTool .


## How to contribute
There are two workflows:

#### Case 1: If you are a contributor:
1. Create a new branch from the current live one (now it is `master`). Make sure to give it a presentive name. In case it is for a specific issue, include the issue number in the branch name, e.g. change-spinner-123.
2. Once you push your changes on the new branch, **create a pull request** and one of the admins will check your code base and will merge if it is ok.

#### Case 2: If you are not added as a contributor yet (or you are a contributor who prefers this workflow):
1. Fork from the current live branch (now it is `master`).
2. Create a pull request, we will review it and merge if it is ok.


