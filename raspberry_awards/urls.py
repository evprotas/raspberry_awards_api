from django.urls import path

from . import views

urlpatterns = [
    path('intervals', views.Intervals.as_view(), name='intervals'),
]