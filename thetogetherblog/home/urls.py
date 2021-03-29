from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_redirect, name='login'),
    path('logout/', views.logout_redirect, name='login'),
]