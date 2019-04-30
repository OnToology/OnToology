docker image build -t ontoology:latest -f Dockerfile .
docker container run --interactive --tty --rm --name ontoology ontoology:latest
#docker container run --rm --name ontoology ontoology:latest