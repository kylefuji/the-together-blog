from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.handle_login, name='login'),
    path('logout/', views.handle_logout, name='logout'),
    path('post/', views.handle_post, name='api_post'),
    path('album/', views.handle_album, name='api_album'),
    path('post/<post_id>/', views.handle_post_by_id, name='api_post_id'),
    path('album/<album_id>/', views.handle_album_by_id, name='api_album_id'),
]