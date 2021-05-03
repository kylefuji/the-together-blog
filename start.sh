#!/bin/sh

python manage.py makemigrations api
python manage.py migrate
<<<<<<< HEAD

DJANGO_SUPERUSER_PASSWORD=$2 \
DJANGO_SUPERUSER_USERNAME=$1 \
DJANGO_SUPERUSER_EMAIL=$3 \
./manage.py createsuperuser \
--no-input
=======
>>>>>>> c4e7634831733612d3a8773cf2e059960d02c8f3
python manage.py runserver 0.0.0.0:8000