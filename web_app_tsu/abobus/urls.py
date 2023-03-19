"""web_app_tsu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.http import HttpResponse
from django.db import connection
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('projects/', projects, name='projects'),
    path('add_project/', add_project, name='add_project'),
    path('tables/', tables, name='tables'),
    path('register/', register, name='register'),
    path('personal_cabinet/', personal_cabinet, name='personal_cabinet'),
    path('create_project/', create_project_view, name='create_project'),
    path('login/', login_view, name = 'login'),
    path('investor_cabinet/',investor_cabinet, name='investor_cabinet')
]
