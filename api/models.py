from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

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
    imageURLs = ArrayField(models.CharField(max_length=300, blank=True, null=True), blank=True, null=True, default=list)
    videoURLs = ArrayField(models.CharField(max_length=300, blank=True, null=True), blank=True, null=True, default=list)
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL)