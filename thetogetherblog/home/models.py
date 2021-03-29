from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    imageURL = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=50, blank=True, null=True)

class Post(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=250)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    imageURLs = models.TextField(blank=True, null=True)
    videoURLs = models.TextField(blank=True, null=True)
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL)