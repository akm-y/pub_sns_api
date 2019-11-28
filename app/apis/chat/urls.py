# coding: utf-8

from django.urls import include, path
from .views import ChatViewSet
from django.views.decorators.csrf import csrf_exempt


chatViewSet = ChatViewSet()

urlpatterns = [
    path('/room',  csrf_exempt(chatViewSet.get_room)),
    path('/room/all',  csrf_exempt(chatViewSet.get_room_all)),
    path('/make/',  csrf_exempt(chatViewSet.make_room)),
    path('/message/post',  csrf_exempt(chatViewSet.post_message)),

]