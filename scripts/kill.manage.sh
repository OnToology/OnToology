kill -9 $(ps aux | grep -e manage.py | awk '{ print $2 }')
