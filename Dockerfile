FROM python:3.9
WORKDIR /app
COPY . .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
ENV DEPLOY 1
RUN pip install --upgrade pip  
RUN chmod +x start.sh
RUN pip install -r requirements.txt  
RUN rm -rf api/migrations
EXPOSE 1337
CMD start.sh