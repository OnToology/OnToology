#coverage run --source='.' --omit='./OnToology/tests'  manage.py test OnToology
#coverage report  --omit='./OnToology/tests' 
coverage run manage.py test OnToology
coverage report
