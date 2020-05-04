# ![alt text](https://raw.githubusercontent.com/OnToology/OnToology/master/media/icons/logoprop1_readme.png "OnToology")
[![Build Status](https://semaphoreci.com/api/v1/ahmad88me/ontoology/branches/master/badge.svg)](https://semaphoreci.com/ahmad88me/ontoology)
[![codecov](https://codecov.io/gh/OnToology/OnToology/branch/master/graph/badge.svg)](https://codecov.io/gh/OnToology/OnToology)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1317786.svg)](https://doi.org/10.5281/zenodo.1317786)

A system for collaborative ontology development process. Given a repository with an owl file, **OnToology** will survey it and produce diagrams, a complete documentation and validation based on common pitfalls.

You can find a live version of OnToology online: http://ontoology.linkeddata.es.

Team: Ahmad Alobaid, Daniel Garijo, Maria Poveda, Idafen Santa, Oscar Corcho, Alba Fernandez Izquierdo

License: Apache License v2 (http://www.apache.org/licenses/LICENSE-2.0)


# To run automated tests
1. You should have [docker](https://docs.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed
2. You need to have a GitHub user to act as "OnToologyUser" (you can choose any username you like).
3. Add the details as in the *secret setup* section below.
4. Run the automated tests script `sh scripts/run_tests.sh` 


# Run Locally
1. `cp -Rf ~/.ssh/ ssh` (assuming you have a *nix and that you already have an ssh key)
2. `mkdir -p .git`
3. `docker-compose run -p 8000:8000 web .venv/bin/python manage.py runserver 0.0.0.0:8000`
4. Run the RabbitMQ server (consumers).
    - Locally: `python OnToology/rabbit.py` 
    - For a linux server: 
`nohup .venv/bin/python OnToology/rabbit.py &`
5. (Optional) you can run it multiple times (multiple consumers) to speed it up.


# Recover from a failure or a server restart


## Secret setup
This file should be added in `scripts/secret_setup.sh`
```
#!/bin/sh
export github_password=""
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


## How to contribute
There are two workflows:

#### Case 1: If you are a contributor:
1. Create a new branch from the current live one (now it is `master`). Make sure to give it a presentive name. In case it is for a specific issue, include the issue number in the branch name, e.g. change-spinner-123.
2. Once you push your changes on the new branch, **create a pull request** and one of the admins will check your code base and will merge if it is ok.

#### Case 2: If you are not added as a contributor yet (or you are a contributor who prefers this workflow):
1. Fork from the current live branch (now it is `master`).
2. Create a pull request, we will review it and merge if it is ok.


