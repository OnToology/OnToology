kill -9 $(ps aux | grep -e rabbit.py | awk '{ print $2 }')
