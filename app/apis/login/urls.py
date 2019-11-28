# coding: utf-8

from django.urls import include, path
from .views import LoginViewSet
from django.views.decorators.csrf import csrf_exempt


userViewSet = LoginViewSet()

urlpatterns = [
    # loginチェック
    path('login/', csrf_exempt(userViewSet.login)),

    # ログアウト
    path('logput/', csrf_exempt(userViewSet.logout)),
]