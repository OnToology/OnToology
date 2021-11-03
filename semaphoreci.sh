sh scripts/migrate.sh
.venv/bin/pip install --upgrade codecov # should be added later to the base docker
export PATH=.venv/bin/:$PATH
.venv/bin/python -m coverage run manage.py test OnToology --settings=OnToology.settings-tests
coverage report
codecov -version
codecov -t $CODECOV_TOKEN