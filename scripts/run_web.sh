docker image build -t ontoology:alpine -f Dockerfile .
docker-compose run -p "8000:8000" web .venv/bin/python manage.py runserver 0.0.0.0:8000
