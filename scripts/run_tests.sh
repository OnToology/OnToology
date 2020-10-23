#!/bin/bash
sh scripts/migrate.sh
python manage.py test OnToology
coverage report
