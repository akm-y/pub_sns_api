# coding: utf-8

import json
from app.models import User,Friend, News, NewsTran, Team, Member
from django.http import JsonResponse
import sys
from django.db.models import Q
from django.utils import timezone
from django.db import transaction, connection
from app.libs.common import dictfetchall
from app.libs.common import dictfetchall, getuniqueid
from app.apis.user.views import UserViewSet
class NotificationViewSet:

    # すべての友達を取得
    # /users/friends/
    @classmethod
    def get_note(self, request,  *args, **kwargs):
        try:
            # TODO バリデーションチェック
            param = request.GET
            user_id = param.get("user_id")
            lists = []
            with connection.cursor() as cursor:
                cursor.execute("select * from app_newstran as t1 inner join app_news as t2 on t1.news_id = t2.id where t1.user_id ='%s' and t1.del_flg = 0 and t2.del_flg = 0 " % (user_id))
                my_note = dictfetchall(cursor)

            response = JsonResponse(
                {"status": 200, "message": "ok", "note": my_note},
                safe=False,
            )
        except KeyError as e:
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            response = JsonResponse(
                {'status': e.args[0], "message": e.args[1]},
                safe=False
            )
        return response

    @classmethod
    def note_follow(self, request, *args, **kwargs):
        try:
            query_param = request.GET
            print(query_param.get("user_id"))
            lists = []

            response = JsonResponse(
                {"status": 200, "message": "ok", "friends": lists},
                safe=False,
            )

        except KeyError as e:
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            response = JsonResponse(
                {'status': e.args[0], "message": e.args[1]},
                safe=False
            )
        return response

    @classmethod
    def note_approval(self, request,  *args, **kwargs):
        try:
            query_param = request.GET
            print(query_param.get("user_id"))
            lists = []

            response = JsonResponse(
                {"status": 200, "message": "ok", "friends": lists},
                safe=False,
            )

        except KeyError as e:
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            response = JsonResponse(
                {'status': e.args[0], "message": e.args[1]},
                safe=False
            )
        return response


    @classmethod
    def note_entry(self, request,  *args, **kwargs):
        try:
            query_param = request.GET
            print(query_param.get("user_id"))
            lists = []

            response = JsonResponse(
                {"status": 200, "message": "ok", "friends": lists},
                safe=False,
            )

        except KeyError as e:
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            response = JsonResponse(
                {'status': e.args[0], "message": e.args[1]},
                safe=False
            )
        return response

    @classmethod
    def note_join_team(self, request,  *args, **kwargs):
        try:
            sid = transaction.savepoint()

            query_param = request.POST
            # joinしたチームID
            team_id = query_param['team_id']
            # joinしたユーザID
            user_id = query_param['user_id']
            # お知らせに使用するユーザ情報取得
            user = User.objects.values('user_id', 'auth_id', 'skill', 'profile').filter(user_id=user_id)
            name = user[0]['profile']['basic_info']['first_name'] + ' ' + user[0]['profile']['basic_info']['last_name']

            news = News.objects.create(
                team_id=team_id,
                contents=name + "さんがチームにジョインしました。"
            )

            notice_target_user = Member.objects.values('join_user_id').filter(team_id=team_id).exclude(join_user_id=user_id)

            for user in notice_target_user:
                NewsTran.objects.create(
                    notice_user_id=user['join_user_id'],
                    news_id=news.id,
                    status=0
                )
            print(user)

            response = JsonResponse(
                {"status": 200, "message": "ok", "id": news.id},
                safe=False,
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
                {'status': e.args[0], "message": e.args[1]},
                safe=False
            )
        return response
