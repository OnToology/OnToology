#!/bin/sh
echo "Migration script -- START"
rm -Rf OnToology/migrations
rm -Rf *.db
.venv/bin/python manage.py makemigrations OnToology
.venv/bin/python manage.py migrate
echo "Migration script -- FINISHED"