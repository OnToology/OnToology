#.venv/bin/pip install codecov coverage # should be added later to the base docker
#export PATH=.venv/bin/:$PATH
coverage run manage.py test OnToology
coverage report
echo "CODECOV: "
echo $CODECOV_TOKEN
bash <(curl -s https://codecov.io/bash) -t $CODECOV_TOKEN
#codecov -t $CODECOV_TOKEN
#.venv/bin/coverage run manage.py test OnToology
#.venv/bin/coverage report
#.venv/bin/codecov -t $CODECOV_TOKEN
#bash <(curl -s https://codecov.io/bash)
