from django.contrib import admin

from .models import Post, Album

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 
                    'title', 
                    'user',
                    'content',
                    'imageURLs',
                    'videoURLs',
                    'album',
                    'created')

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description',
                    'imageURL',
                    'created',
                    'reference')

admin.site.register(Post, PostAdmin)
admin.site.register(Album, AlbumAdmin)