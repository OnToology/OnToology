sh scripts/migrate.sh
echo "RUN the Stiqueue Client"
.venv/bin/python OnToology/sqclient.py &
echo "update codecov"
.venv/bin/pip install --upgrade codecov # should be added later to the base docker
export PATH=.venv/bin/:$PATH
echo "run coverage tests"
.venv/bin/python -m coverage run manage.py test OnToology --settings=OnToology.settings-tests
coverage report
codecov -t $CODECOV_TOKEN