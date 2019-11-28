# coding: utf-8

import json
from app.models import User, Friend,Chats
from django.http import JsonResponse
from django.db.models import Q
import random, string
from app.libs.myCrypt import get_decrypt_data,get_encrypt_data
from api.settings import common as common_settings
from django.core import serializers
from django.utils import timezone
from app.libs.common import dictfetchall, getuniqueid
from django.db import transaction, connection


class ChatViewSet:

    @classmethod
    def get_room(self, request,  *args, **kwargs):
        try:
            query_param = request.GET
            user_id = query_param['user_id']
            chat_user_id = query_param['chat_user_id']

            room = []
            for obj in Chats.objects.values().filter(
                (Q(by_user_id=user_id, to_user_id=chat_user_id) | Q(by_user_id=chat_user_id, to_user_id=user_id))):
                room.append(obj)

            response = JsonResponse(
                {"status": 200, "message": "", "room": obj},
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

    @classmethod
    def get_room_all(self, request,  *args, **kwargs):
        try:
            query_param = request.GET
            user_id = query_param['user_id']

            room = []
            for obj in Chats.objects.values().filter(
                    Q(by_user_id=user_id) | Q(to_user_id=user_id)):
                room.append(obj)

            response = JsonResponse(
                {"status": 200, "message": "", "room": room},
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
    @classmethod
    def make_room(self, request,  *args, **kwargs):
        try:
            sid = transaction.savepoint()

            query_param = request.POST
            user_id = query_param['user_id']
            chat_user_id = query_param['chat_user_id']

            room_id = getuniqueid()
            c = Chats.objects.create(
                by_user_id=user_id
                , to_user_id=chat_user_id
                , room_id=room_id
                , create_dt=timezone.datetime.now()
            )
            c.save()
            response = JsonResponse(
                {"status": 200, "message": "", "room_id": c.room_id},
                safe=False,
            )

        except KeyError as e:
            transaction.savepoint_rollback(sid)
            response = JsonResponse(
                {'status': 980, "message": "リクエストデータに" + e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            transaction.savepoint_rollback(sid)
            response = JsonResponse(
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response

    @classmethod
    def post_message(self, request,  *args, **kwargs):
        try:
            sid = transaction.savepoint()

            query_param = request.POST
            room_id = query_param['room_id']
            logs = query_param['logs']

            if Chats.objects.filter(
                room_id=room_id,
                del_flg=0
            ).update(
                logs=logs
            ) == 0:
                raise Exception(999, '【ERROR】データがありません。')

            response = JsonResponse(
                {"status": 200, "message": "OK"},
                safe=False,
            )

        except KeyError as e:
            transaction.savepoint_rollback(sid)
            response = JsonResponse(
                {'status': 980, "message": "リクエストデータに" + e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            transaction.savepoint_rollback(sid)
            response = JsonResponse(
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response

@classmethod
def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

