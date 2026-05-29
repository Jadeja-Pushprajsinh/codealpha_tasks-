"""
URL configuration for project_manager project.

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
     path('',dashboard,name='dashboard'),
    path('register/',register,name='register'),
    path('create-project/',create_project,name='create_project'),
    path('project/<int:project_id>/',project_board,name='project_board'),
    path('project/<int:project_id>/create-task/',create_task,name='create_task'),
    path('task/<int:task_id>/comment/',add_comment,name='add_comment'),
    path('task/<int:task_id>/',task_detail,name='task_detail'),
    path('task/<int:task_id>/<str:status>/',update_task_status,name='update_task_status'),
    path('', include('django.contrib.auth.urls')),
    
]

