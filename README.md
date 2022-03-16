# ![alt text](https://raw.githubusercontent.com/OnToology/OnToology/main/media/icons/logoprop1_readme.png "OnToology")

[![Build Status](https://ahmad88me.semaphoreci.com/badges/OnToology/branches/main.svg)](https://ahmad88me.semaphoreci.com/projects/OnToology) 
[![codecov](https://codecov.io/gh/OnToology/OnToology/branch/main/graph/badge.svg?token=PJgHWaaa9l)](https://codecov.io/gh/OnToology/OnToology)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1317786.svg)](https://doi.org/10.5281/zenodo.1317786)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7e81902ad6044e72bbc6af11a5201e0e)](https://www.codacy.com/gh/OnToology/OnToology/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=OnToology/OnToology&amp;utm_campaign=Badge_Grade)
[![Twitter](https://img.shields.io/twitter/follow/OnToology.svg?style=social&label=@OnToology)](https://twitter.com/OnToology)

A system for collaborative ontology development process. Given a repository with an owl file, **OnToology** will survey it and produce diagrams, a complete documentation and validation based on common pitfalls. It also offers seamless publication of user ontologies with w3id using GitHub pages. 

You can find a live version of OnToology online: http://ontoology.linkeddata.es.

Team: Ahmad Alobaid, Daniel Garijo, Maria Poveda, Idafen Santa, Alba Fernandez Izquierdo, Oscar Corcho

License:  Apache License v2 (http://www.apache.org/licenses/LICENSE-2.0) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)



If you want to cite Ontoology in a scientific paper or technical report, you can use the following [Bibtex citation](/media/references/ontoology.bib) or directly this text: Alobaid A, Garijo D, Poveda-Villalón M, Santana-Pérez I, Fernández-Izquierdo A, Corcho O (2019) Automating ontology engineering support activities with OnToology. Journal of Web Semantics 57:100472, https://doi.org/10.1016/j.websem.2018.09.003

# Funding
The development of OnToology has been supported by the Spanish national project Datos 4.0 (TIN2016-78011-C4-4-R)

# Tools
Here is a list of tools being used by OnToology.
* [owl2jsonld](https://github.com/stain/owl2jsonld) ( [zenodo](http://dx.doi.org/10.5281/zenodo.10565) )
* [Widoco](https://github.com/dgarijo/Widoco) ( [zenodo](https://zenodo.org/badge/latestdoi/11427075) )
* [OOPS!](http://oops.linkeddata.es)
* [AR2DTool](https://github.com/idafensp/ar2dtool)
* [oops-report](https://github.com/OnToology/oops-report)
* [Themis](https://github.com/oeg-upm/Themis)


# Documentation for users
If you are an ontology engineer willing to use OnToology, you can check our [step by step documentation](http://ontoology.linkeddata.es/tutorial). You can also check our list of [Frequently Asked Questions](http://ontoology.linkeddata.es/faqs)


# Documentation for developers
We provide some documentation for developers who want to contribute to the development OnToology or for those who are interested in deploying OnToology locally or in their servers. Feel free to contact us if you are interested in contributing to the project.


## Test workflow
There are two kinds of tests:
1. Using mock. These kinds of tests use a list of stored requests expected from GitHub APIs. These are fast and do not need GitHub keys or setup.
2. Using real GitHub repos. These kinds of tests uses GitHub APIs. These tests can take some time and need special keys to access relevant test repos. For this reason, these are not available for the public. However, they are executed automatically after each *merge* to the `main` branch.

## Run Tests on Real GitHub Repo
*This is only available for certain people*
1. Copy the keys into the folder `ssh`
2. Create a file `scripts/secret_setup.sh`
3. Write the following and fill the missing values (currently the private app is not added in the tests, so it can be left empty). (see secret setup section below).
4. Run the tests on docker
```
sh scripts/run_docker_tests.sh
```
*Note:* If you made changes, you might need to rebuild the image `docker-compose build`


## Secret Setup
```
#!/bin/sh
export github_password=""
export github_email=""
export client_id_login=""
export client_id_public=""
export client_id_private=""
export client_secret_login=""
export client_secret_public=""
export client_secret_private=""
export test_user_token=""
export test_user_email=""
export github_username=""
```

## Run Locally
1. Setup (see Run Tests on Real GitHub Repo section [here](https://github.com/OnToology/OnToology/tree/main#run-tests-on-real-github-repo))
2. Run the following: `sh scripts/run_docker.sh`
3. Go to `127.0.0.1:8000` and start using OnToology.

<!--
## To run automated tests
1. You should have [docker](https://docs.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed
2. You need to have a GitHub user to act as "OnToologyUser" (you can choose any username you like).
3. Add the details as in the *secret setup* section below.
4. Run the automated tests script `sh scripts/run_tests.sh` 


## Run Locally
### via script
1. `sh scripts/run_web.sh`
### manual
1. `cp -Rf ~/.ssh/ ssh` (assuming you have a *nix and that you already have an ssh key)
1. `mkdir -p .git`
1. `docker-compose build --no-cache`
1. `docker-compose run -p 8000:8000 web .venv/bin/python manage.py runserver 0.0.0.0:8000`


## To access the command line
`sh scripts/run_docker.sh`


### Secret setup
This file should be added in `scripts/secret_setup.sh`
```
#!/bin/sh
export github_password=""
export github_email=""
export client_id_login=""
export client_id_public=""
export client_id_private=""
export client_secret_login=""
export client_secret_public=""
export client_secret_private=""
export test_user_token=""
export test_user_email=""
export rabbit_host=""
```

### Environment variables
Here we describe some of the main ones
* `rabbit_processes` : The number of rabbit processes to automatically run (0 means do not run it automatically).



### How to contribute
There are two workflows:


##### Case 1: If you are a contributor:
1. Create a new branch from the current live one (now it is `master`). Make sure to give it a presentive name. In case it is for a specific issue, include the issue number in the branch name, e.g. change-spinner-123.
2. Once you push your changes on the new branch, **create a pull request** and one of the admins will check your code base and will merge if it is ok.


##### Case 2: If you are not added as a contributor yet (or you are a contributor who prefers this workflow):
1. Fork from the current live branch (now it is `master`).
2. Create a pull request, we will review it and merge if it is ok.


### Dependency notice
* To run the tests, we use the `mock` option for github api. It was rejected by the `PyGithub` maintainers, so make sure to use
the version in `ahmad88me/PyGithub`.  (see below)


## Local Setup
### On Linux
(tested on ubuntu, debian, mint and fedora)
#### To install the tools
1. Open the terminal and `cd` to the location of choice.
2. `export PLAYGROUND=$PWD`.
3. Copy and paste the commands of choice to the terminal from `scripts/setup_docker_base.sh`


### Install Pygithub (not the upstream version)
#### either directly from github
`pip install git+https://github.com/ahmad88me/PyGithub.git`
#### or locally
1. `git clone https://github.com/ahmad88me/PyGithub.git`
1. `cd OnToology` (assuming both are on the same level/directory)
1. `pip install -e ../Pygithub` (change this to any directory you want)



### NEW: Running OnToology Locally
1. create a new github user (not your personal account, another account).
1. create ssh key for that user [here](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key).
1. copy the ssh key `id_ed25519` and `id_ed25519.pub` to `ssh` (*copy to the ssh folder located inside the OnToology folder*).


# To DEBUG 
docker ps
docker exec -it <container name> /bin/sh 


-->


# Deploy
1. Clone the repo.
2. Set up the variables in `OnToology/localwsgi.py` (see above for the details).
3. Create virtual env (optional).
4. Install dependencies using pip (`pip install -r requirements`).
5. Run the [stiqueue](https://github.com/ahmad88me/stiqueue) server (with the ip and port). 
6. Run `OnToology/sqclient.py`.