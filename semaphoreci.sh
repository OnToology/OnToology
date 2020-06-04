.venv/bin/pip install codecov # should be added later to the base docker
export PATH=.venv/bin/:$PATH
coverage run manage.py test OnToology
coverage report
#codecov -t $CODECOV_TOKEN
bash <(curl -s https://codecov.io/env)
#curl -s https://codecov.io/bash > .codecov
#chmod +x .codecov
#./.codecov -t $CODECOV_TOKEN
#.venv/bin/coverage run manage.py test OnToology
#.venv/bin/coverage report
#.venv/bin/codecov -t $CODECOV_TOKEN
#bash <(curl -s https://codecov.io/bash)
