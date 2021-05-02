FROM python:3.9
ENV DockerHOME=/home/app/webapp
RUN mkdir -p ${DockerHOME}
WORKDIR ${DockerHOME}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
ENV DEPLOY 1
RUN pip install --upgrade pip  
COPY . ${DockerHOME}
RUN pip install -r requirements.txt  
RUN python manage.py makemigrations
RUN python manage.py migrate
EXPOSE 1337
CMD python manage.py runserver 1337