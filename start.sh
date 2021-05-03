#!/bin/sh

python manage.py makemigrations api
python manage.py migrate

DJANGO_SUPERUSER_PASSWORD=${SU_PASSWORD} \
DJANGO_SUPERUSER_USERNAME=${SU_ADMIN} \
DJANGO_SUPERUSER_EMAIL=${SU_EMAIL} \
python manage.py createsuperuser \
--no-input
python manage.py runserver 0.0.0.0:8000