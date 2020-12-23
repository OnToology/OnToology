#docker-compose build --no-cache
#docker-compose run web .venv/bin/python manage.py test OnToology
#docker-compose run web sh scripts/migrate.sh & .venv/bin/python OnToology/rabbit.py 1 &;.venv/bin/python manage.py test OnToology
#docker-compose run web bash -c "cd /playground/OnToology ; .venv/bin/pip install -r requirements.txt ; sh scripts/migrate.sh ; .venv/bin/python OnToology/rabbit.py 1 \& ; .venv/bin/python manage.py test OnToology"
#docker-compose run web bash -c "cd /playground/OnToology ; .venv/bin/pip install -r requirements.txt ; sh scripts/migrate.sh ; .venv/bin/python OnToology/rabbit.py 1 \& ; .venv/bin/python manage.py test OnToology"
#docker-compose run web bash -c "cd /playground/OnToology; .venv/bin/pip install -r requirements.txt; sh scripts/migrate.sh; .venv/bin/python OnToology/rabbit.py 1 \& ; .venv/bin/python manage.py test OnToology"
#docker-compose run web cd /playground/OnToology; .venv/bin/pip install -r requirements.txt; sh scripts/migrate.sh; .venv/bin/python OnToology/rabbit.py 1 \& ; .venv/bin/python manage.py test OnToology
#docker-compose run web cd /playground/OnToology; (.venv/bin/pip install -r requirements.txt; sh scripts/migrate.sh ); (.venv/bin/python OnToology/rabbit.py 1 & ) ; ( .venv/bin/python manage.py test OnToology)
#docker-compose run web cd /playground/OnToology; .venv/bin/pip install -r requirements.txt; sh scripts/migrate.sh  ;  .venv/bin/python manage.py test OnToology
#docker-compose run --rm web echo "in compose run"; pwd; cat OnToology/localwsgi.py; sh scripts/migrate.sh; .venv/bin/python manage.py test OnToology
#docker-compose run --rm web sh scripts/migrate.sh; .venv/bin/python manage.py test OnToology
#docker-compose run --rm web echo "in compose run"; pwd; cat OnToology/localwsgi.py; echo "MIGRATION SCRIPT"; sh scripts/migrate.sh; echo " STARTING TEST FROM DOCKER TESTS SCRIPT"; .venv/bin/python manage.py test OnToology
#docker-compose run --rm web sh /playground/OnToology/scripts/load_environ.sh; cat /playground/OnToology/OnToology/localwsgi.py
#docker-compose run web (pwd; ls -ltra;cat /playground/OnToology/OnToology/localwsgi.py)
docker-compose run web sh scripts/run_tests_within.sh

