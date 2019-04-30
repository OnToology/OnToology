docker image build -t ontoologybase:latest -f Dockerfile.base .
docker container run --interactive --tty --rm --name ontoologybase ontoologybase:latest
