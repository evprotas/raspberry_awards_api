"""raspberry_awards_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
import sys
import os
from raspberry_awards.utils import read_nominations

urlpatterns = [
    path('awards/', include('raspberry_awards.urls')),
    path('admin/', admin.site.urls),
]

if sys.argv[1] == 'runserver':
    filename = "movielist.csv"
    try:
        read_nominations(filename)
    except FileNotFoundError:
        print("Arquivo " + os.getcwd() + "/movielist.csv não encontrado.")
        exit()