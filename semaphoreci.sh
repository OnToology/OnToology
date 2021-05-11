sleep 120
sh scripts/migrate.sh
.venv/bin/pip install --upgrade codecov # should be added later to the base docker
export PATH=.venv/bin/:$PATH
coverage run manage.py test OnToology
coverage report
codecov -version
codecov -t $CODECOV_TOKEN
