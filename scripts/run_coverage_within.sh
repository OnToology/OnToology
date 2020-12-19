echo "in compose run"
pwd
cat OnToology/localwsgi.py
echo "MIGRATION SCRIPT"
sh scripts/migrate.sh
echo " STARTING TEST FROM DOCKER TESTS SCRIPT"
source .venv/bin/activate
coverage run --source='.' manage.py test OnToology
coverage report
