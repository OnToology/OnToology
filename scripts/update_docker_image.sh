#!/bin/bash
read -p 'This will update the docker image on docker hub, are you sure? (y/N) ' execflag
if [[ $execflag == y* || $execflag == Y* ]]
then
    echo Preparing to push ontoology image to docker hub
    docker image build -t ahmad88me/ontoology:alpine -f Dockerfile.base . --no-cache
    docker image push ahmad88me/ontoology:alpine
else
    echo The docker image will not be updated in docker hub
fi
#echo Your answer is $execflag