#docker image build -t ontoology:alpine -f Dockerfile .
#docker-compose run -p "8000:8000" web .venv/bin/python manage.py runserver 0.0.0.0:8000
echo "Migration script -- START"
rm -Rf OnToology/migrations
rm -Rf *.db
.venv/bin/python manage.py makemigrations OnToology --settings=OnToology.settings-local
.venv/bin/python manage.py migrate --settings=OnToology.settings-local
echo "Migration script -- FINISHED"
export mock_id=""
export test_local="true"
export test_fork="true"
export test_clone="true"
export test_push="true"
export test_pull="true"
echo "RUN the Stiqueue Client"
.venv/bin/python OnToology/sqclient.py OnToology.settings-local &
echo "To run the web"
.venv/bin/python manage.py runserver 0.0.0.0:8000 --settings=OnToology.settings-local
