# coding: utf-8

from django.urls import include, path
from .views import FriendViewSet
from django.views.decorators.csrf import csrf_exempt

friend = FriendViewSet()
urlpatterns = [
    # 友達情報取得
    path('/get/', csrf_exempt(friend.get_friends)),
    # おすすめ友達情報取得
    path('/recommend/', csrf_exempt(friend.get_recommend)),
    # 友達申請
    path('/follow/', csrf_exempt(friend.follow)),
    # 友達申請承認
    path('/approval/', csrf_exempt(friend.approval)),
    # 友達をブロック
    path('/brock/', csrf_exempt(friend.brock)),
    # 友達紹介を拒否
    path('/reject/', csrf_exempt(friend.reject)),
    # 友達ステータスを取得
    path('/status/', csrf_exempt(friend.getStatus))
]