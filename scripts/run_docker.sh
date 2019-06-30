docker image build -t ontoology:alpine -f Dockerfile .
docker container run --interactive --tty --rm --name ontoology ontoology:alpine
# To access it via docker-compose
# docker-compose run web