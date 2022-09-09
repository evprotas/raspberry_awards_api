from django.urls import path

from . import views

urlpatterns = [
    path('intervals', views.intervals, name='intervals'),
]