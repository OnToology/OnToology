echo "in compose run"
pwd
cat OnToology/localwsgi.py
echo "Show $PLAYGROUND/OnToology/.venv/bin/activate"
echo "cat $PLAYGROUND/OnToology/.venv/bin/activate"
echo "tests within: MIGRATION SCRIPT"
sh scripts/migrate.sh
echo "list"
ls OnToology -ltr
echo "RUN the Stiqueue Client"
.venv/bin/python OnToology/sqclient.py &
echo " STARTING TEST FROM DOCKER TESTS SCRIPT"
export mock_id=success

export test_local="true"
export test_fork="false"
export test_clone="true"
export test_push="false"
export test_pull="false"


#.venv/bin/python manage.py test --pattern="test_direct_magic.py" --settings=OnToology.settings-tests
.venv/bin/python manage.py test OnToology --settings=OnToology.settings-tests