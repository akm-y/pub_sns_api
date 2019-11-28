# coding: utf-8

from rest_framework import routers
from . import views
from django.urls import include, path

# router = routers.DefaultRouter()
urlpatterns = [
    path('', views.index, name='hello_world')
]