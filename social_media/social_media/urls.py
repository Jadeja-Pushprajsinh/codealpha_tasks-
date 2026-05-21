"""
URL configuration for social_media project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register,name='register'),
    path('',home,name='home'),
    path('create-post/',create_post,name='create_post'),
    path('like/<int:post_id>/',like_post,name='like_post'),
    path('comment/<int:post_id>/',add_comment,name='add_comment'),
    path('profile/<str:username>/',profile,name='profile'),
    path('' , include('django.contrib.auth.urls')), 
]
