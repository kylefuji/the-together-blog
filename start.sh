#!/bin/sh

python manage.py makemigrations api
python manage.py migrate

DJANGO_SUPERUSER_PASSWORD=$2 \
DJANGO_SUPERUSER_USERNAME=$1 \
DJANGO_SUPERUSER_EMAIL=$3 \
./manage.py createsuperuser \
--no-input
python manage.py runserver 0.0.0.0:8000