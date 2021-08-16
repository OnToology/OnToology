echo "in compose run"
pwd
cat OnToology/localwsgi.py
echo "Show $PLAYGROUND/OnToology/.venv/bin/activate"
echo "cat $PLAYGROUND/OnToology/.venv/bin/activate"
echo "MIGRATION SCRIPT"
sh scripts/migrate.sh
echo " STARTING TEST FROM DOCKER TESTS SCRIPT"
.venv/bin/python manage.py test OnToology --settings=OnToology.settings-tests