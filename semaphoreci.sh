#.venv/bin/pip install codecov  # should be added later to the base docker
.venv/bin/coverage run manage.py test OnToology
.venv/bin/coverage report
#.venv/bin/codecov -t $CODECOV_TOKEN
bash <(curl -s https://codecov.io/bash)
