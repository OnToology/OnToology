.venv/bin/pip install codecov  # should be added later to the base docker
.venv/bin/coverage run manage.py test OnToology
.venv/bin/coverage report
codecov -t $CODECOV_TOKEN