# coding: utf-8

from django.urls import include, path
from .views import TeamViewSet
from django.views.decorators.csrf import csrf_exempt

team = TeamViewSet()
urlpatterns = [

    # チームを作る
    path('/create', csrf_exempt(team.create_team)),
    # チーム情報を更新する
    path('/update', csrf_exempt(team.update_team)),
    # チームを削除する
    path('/delete', csrf_exempt(team.delete_team)),
    # 所属チーム情報取得
    path('/belong', csrf_exempt(team.get_my_team)),
    # おすすめチーム情報取得
    path('/recommend', csrf_exempt(team.get_recommend)),
    # チーム参加申請
    path('/join', csrf_exempt(team.join)),
    # チーム参加承認
    path('/approval', csrf_exempt(team.approval)),
    # チーム参加ブロック
    path('/brock', csrf_exempt(team.brock)),
    # チーム参加を拒否
    path('/reject', csrf_exempt(team.reject)),
    # チーム参加ステータスを取得
    path('/status', csrf_exempt(team.getStatus)),
    # チームの詳細情報取得
    path('/detail', csrf_exempt(team.get_detail)),
    # チームに所属するメンバー一覧
    path('/members', csrf_exempt(team.get_members))
    # チーム
]