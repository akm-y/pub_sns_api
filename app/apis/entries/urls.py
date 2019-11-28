# coding: utf-8

from django.urls import include, path
from .views import entryViewSet
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url


entryViewSet = entryViewSet()

urlpatterns = [
    path('/',  entryViewSet.get_all),
    path('/draft/get', csrf_exempt(entryViewSet.get_draft_list)),
    path('/get', csrf_exempt(entryViewSet.get)),
    path('/user/', csrf_exempt(entryViewSet.get_users_entry)),
    path('/get/users/list', csrf_exempt(entryViewSet.get_users_entry)),

    path('/register', csrf_exempt(entryViewSet.register)),
    # path('/register/draft', csrf_exempt(entryViewSet.register_draft)),
    path('/update', csrf_exempt(entryViewSet.update)),
    path('/delete', csrf_exempt(entryViewSet.delete)),
]