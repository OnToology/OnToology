#docker image build -t ontoology:alpine -f Dockerfile .
#docker container run --interactive --tty --rm --name ontoology ontoology:alpine
# To access it via docker-compose
# docker-compose run web
#docker-compose run web sh scripts/run_tests_within.sh
docker-compose run -p "8000:8000" web sh scripts/run_web.sh