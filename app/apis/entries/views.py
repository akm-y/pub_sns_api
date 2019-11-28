# coding: utf-8

import json
from app.models import User, Friend, Entry
from django.http import JsonResponse
import random, string
from app.libs.myCrypt import get_decrypt_data,get_encrypt_data
from api.settings import common as common_settings
from django.core import serializers
from django.utils import timezone
from django.db import transaction, connection
from app.libs.common import dictfetchall, getuniqueid

class entryViewSet():

    @classmethod
    def get_all(self, request,  *args, **kwargs):
        try:
            query_param = request.GET

            entries = []
            #TODO とりあえずは全権取得 数が多くなったら要分析
            for obj in Entry.objects.values().exclude(status=0).exclude(status=99).filter(del_flg=0).prefetch_related("User"):
                entries.append(obj)
            response = JsonResponse(
                {"status": 200, "message": "OK", "entries": entries},
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
    def get(self, request,  *args, **kwargs):
        try:
            query_param = request.GET

            entries = []
            #TODO とりあえずは全権取得 数が多くなったら要分析
            for obj in Entry.objects.filter(entry_id=query_param['entry_id']).values():
                entries.append(obj)
            response = JsonResponse(
                {"status": 200, "message": "", "entries": entries},
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
    def get_users_entry(self, request,  *args, **kwargs):
        try:
            query_param = request.GET

            entries = []
            for obj in Entry.objects.filter(user_id=query_param['user_id']).values():
                entries.append(obj)
            response = JsonResponse(
                {"status": 200, "message": "", "entries": entries},
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
    def get_draft_list(self, request,  *args, **kwargs):
        try:
            query_param = request.GET

            draft = []
            #TODO とりあえずは全権取得 数が多くなったら要分析
            for obj in Entry.objects.filter(user_id=query_param['user_id'], status=0, del_flg=0).values():
                draft.append(obj)
            response = JsonResponse(
                {"status": 200, "message": "ok", "draft": draft},
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
    def register(self, request,  *args, **kwargs):
        try:
            sid = transaction.savepoint()
            post = request.POST
            entry_id = getuniqueid()
            if Entry.objects.create(
                entry_id=entry_id,
                user_id=post['user_id'],
                role=post['role'],
                contents=post['contents'],
                status=post['status'],
                team_id=post['team_id'],
                category=post['choice'],
                create_dt=timezone.now()
            ) == 0:
                raise Exception(999, '【ERROR】データがありません。')

            response = JsonResponse(
                {"message": "OK", 'status': 200},
                safe=False
            )
        except KeyError as e:
            transaction.savepoint_rollback(sid)
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            transaction.savepoint_rollback(sid)
            response = JsonResponse(
                {"message": e.args[0], 'status': 999},
                safe=False
            )
        response['Access-Control-Allow-Origin'] = 'http://localhost:1234'
        return response

    @classmethod
    def update(self, request,  *args, **kwargs):
        try:
            sid = transaction.savepoint()
            post = request.POST
            if Entry.objects.filter(entry_id=post['entry_id']).update(
                user_id=post['user_id'],
                role=post['role'],
                contents=post['contents'],
                status=post['status'],
                team_id=post['team_id'],
                category=post['category'],
                update_dt=timezone.now()
            ) == 0:
                raise Exception(999, '【ERROR】データがありません。')

            response = JsonResponse(
                {"message": "OK", 'status': 200},
                safe=False
            )
        except KeyError as e:
            transaction.savepoint_rollback(sid)
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            transaction.savepoint_rollback(sid)
            response = JsonResponse(
                {"message": e.args[0], 'status': 999},
                safe=False
            )
        response['Access-Control-Allow-Origin'] = 'http://localhost:1234'
        return response

    @classmethod
    # def register_draft(self, request,  *args, **kwargs):
    #     #一次保存を行う
    #     try:
    #         sid = transaction.savepoint()
    #         post = request.POST
    #         result = Entry.objects.create(
    #             user_id=post['user_id'],
    #             role=post['role'],
    #             title=post['title'],
    #             contents=post['contents'],
    #             category=post['category'],
    #             image_path=post['image_path'],
    #             status=Entry.STATUS_DRAFT,
    #             create_dt=timezone.datetime.now()
    #         )
    #         response = JsonResponse(
    #             {"message": "OK", 'status': 200},
    #             safe=False
    #         )
    #     except KeyError as e:
    #         transaction.savepoint_rollback(sid)
    #         response = JsonResponse(
    #             {'status': 980, "message": e.args[0] + "が存在しません。"},
    #             safe=False
    #         )
    #     except Exception as e:
    #         transaction.savepoint_rollback(sid)
    #         response = JsonResponse(
    #             {"message": e.args[0], 'status': 999},
    #             safe=False
    #         )
    #     response['Access-Control-Allow-Origin'] = 'http://localhost:1234'
    #     return response

    def delete(self, request,  *args, **kwargs):
        try:
            sid = transaction.savepoint()
            post = request.POST
            entry_id = post['entry_id']
            if Entry.objects.filter(entry_id=entry_id).update(
                del_flg=1,
                update_dt=timezone.now()
            ) == 0:
                raise Exception(999, '【ERROR】データがありません。')

            response = JsonResponse(
                {"message": "OK", 'status': 200},
                safe=False
            )
        except KeyError as e:
            transaction.savepoint_rollback(sid)
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            transaction.savepoint_rollback(sid)
            response = JsonResponse(
                {"message": e.args[0], 'status': 999},
                safe=False
            )
        response['Access-Control-Allow-Origin'] = 'http://localhost:1234'
        return response
