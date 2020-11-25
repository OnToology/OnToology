rm -Rf OnToology/migrations
rm -Rf *.db
python manage.py makemigrations OnToology
python manage.py migrate
