from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.handle_login, name='login'),
    path('logout/', views.handle_logout, name='logout'),
    path('api/post/', views.handle_post, name='api_post'),
    path('api/album/', views.handle_album, name='api_album'),
    path('api/post/<post_id>/', views.handle_post_by_id, name='api_post_id'),
    path('api/album/<album_id>/', views.handle_album_by_id, name='api_album_id'),
]