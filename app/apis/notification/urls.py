# coding: utf-8

from django.urls import include, path
from .views import NotificationViewSet
from django.views.decorators.csrf import csrf_exempt

note = NotificationViewSet()
urlpatterns = [

    # 自分に関するお知らせ取得

    path('/', csrf_exempt(note.get_note)),

    # 友達・チーム申請時登録時
    path('/follow/', csrf_exempt(note.note_follow)),

    # 友達・チーム申請承認時登録時
    path('/approval/', csrf_exempt(note.note_approval)),

    # チームの投稿があった時
    path('/entry/post/', csrf_exempt(note.note_entry)),

    # チームにjoinした時
    path('/join', csrf_exempt(note.note_join_team)),
]