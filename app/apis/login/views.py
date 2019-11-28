# coding: utf-8

import json
from app.models import User, Friend
from django.http import JsonResponse
import random, string
from app.libs.myCrypt import get_decrypt_data,get_encrypt_data
from api.settings import common as common_settings
from django.core import serializers


class LoginViewSet():

    def login(self, request,  *args, **kwargs):
        try:
            query_param = request.GET

            user = []
            for obj in User.objects.values('user_id', 'skill', 'profile').filter(auth_id=query_param.get("user_id")):
                if 'user_id' in obj:
                    obj['user_id'] = get_encrypt_data(obj['user_id'], common_settings.CRYPT_KEY, common_settings.CRYPT_IV).decode('utf-8')
                user.append(obj)

            if len(user) < 1:
                raise KeyError

            response = JsonResponse(
                {"status": 200, "message": "", "login": "ok"},
                safe=False,
            )

        except KeyError as e:
            response = JsonResponse(
                {'status': 980, "message": "リクエストデータに" + e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            response = JsonResponse(
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response


    def logout(self, request,  *args, **kwargs):
        try:
            query_param = request.GET

            user = []
            for obj in User.objects.values('user_id', 'skill', 'profile').filter(auth_id=query_param.get("user_id")):
                if 'user_id' in obj:
                    obj['user_id'] = get_encrypt_data(obj['user_id'], common_settings.CRYPT_KEY, common_settings.CRYPT_IV).decode('utf-8')
                user.append(obj)

            if len(user) < 1:
                raise KeyError

            response = JsonResponse(
                {"status": 200, "message": "", "login": "ok"},
                safe=False,
            )

        except KeyError as e:
            response = JsonResponse(
                {'status': 980, "message": "リクエストデータに" + e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            response = JsonResponse(
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response


def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

