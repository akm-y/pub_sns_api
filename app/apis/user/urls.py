# coding: utf-8

from django.urls import include, path
from .views import UserViewSet
from django.views.decorators.csrf import csrf_exempt


userViewSet = UserViewSet()

urlpatterns = [
    path('/',  userViewSet.get_user),

    path('/exists/',  userViewSet.get_user),

    # サインイン時ユーザ登録
    path('/register/', csrf_exempt(userViewSet.register)),

    # プロフィール情報を登録
    path('/profile/register/', csrf_exempt(userViewSet.profile_update)),

    # プロフィール情報を登録
    path('/skill/register/', csrf_exempt(userViewSet.skill_register)),

    # プロフィール画像を登録
    path('/photo/register/', csrf_exempt(userViewSet.photo_register)),
]