.venv/bin/coverage run manage.py test OnToology
.venv/bin/coverage report
codecov -t $CODECOV_TOKEN