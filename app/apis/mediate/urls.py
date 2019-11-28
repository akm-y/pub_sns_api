# coding: utf-8

from django.urls import include, path
from .views import MediateViewSet
from django.views.decorators.csrf import csrf_exempt

mediate = MediateViewSet()
urlpatterns = [
    # 友達を紹介するよ
    path('', csrf_exempt(mediate.do_mediate)),
    # 友達紹介を承認
    path('approval/from/', csrf_exempt(mediate.from_approval)),
    # 友達紹介を承認
    path('approval/to/', csrf_exempt(mediate.to_approval)),
    # 友達紹介を拒否
    path('reject/from/', csrf_exempt(mediate.from_reject)),
    # 友達紹介を拒否
    path('reject/to/', csrf_exempt(mediate.to_reject)),

]