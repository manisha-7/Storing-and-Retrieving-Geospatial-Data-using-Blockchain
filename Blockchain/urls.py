from atexit import register
from django.urls import path
from re import template
from . import views
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    
    path('upload', views.upload, name="upload"),
    path('login', views.userlogin, name="login"),
    path('', views.homepage, name="homepage"),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('view', views.view, name='view'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('resetpass', views.resetpass, name='resetpass'),
    path('search', views.search, name='search'),
    path('downloads', views.downloads, name='downloads'),
    path('about', views.about, name='about'),
    path('modify_permissions', views.modify_permissions, name='modify_permissions'),
    path('ppermission', views.ppermission, name='ppermission'),

]