# coding: utf-8

import json
from app.models import User,Friend
from django.http import JsonResponse
import sys
from django.db.models import Q
from django.utils import timezone
from django.db import transaction, connection
from app.libs.common import dictfetchall
from app.libs.common import dictfetchall, getuniqueid

class FriendViewSet:

    # すべての友達を取得
    # /users/friends/
    @classmethod
    def get_friends(self, request,  *args, **kwargs):
        try:
            # TODO バリデーションチェック
            query_param = request.GET
            print(query_param.get("user_id"))
            lists = []

            # 自分からフォロー申請
            with connection.cursor() as cursor1:
                cursor1.execute('''
                    select * 
                    from app_user as t1
                    where t1.user_id in(
                        select t2.follower_user_id
                        from app_friend as t2
                        where t2.request_user_id=%s AND 
                        t2.del_flg = 0 AND 
                        t2.reject = 0 AND 
                        t2.brock_user_id IS NULL
                    ) AND t1.del_flg = 0''', [query_param.get("user_id")])
                obj1 = dictfetchall(cursor1)
                if len(list(obj1)) != 0:
                    lists.extend(list(obj1))

            # 相手からフォロー申請
            with connection.cursor() as cursor2:
                cursor2.execute(
                    '''
                        select * 
                        from app_user as t1
                        where t1.user_id in(
                        select t2.request_user_id
                        from app_friend as t2
                        where t2.follower_user_id =%s AND 
                        t2.del_flg = 0 AND 
                        t2.reject = 0 AND 
                        t2.brock_user_id IS NULL
                        ) AND t1.del_flg = 0'''
                            , [query_param.get("user_id")])
                obj2 = dictfetchall(cursor2)
                if len(list(obj2)) != 0:
                    lists.extend(list(obj2))

            for obj in lists:
                obj['profile'] = json.loads(obj['profile'])

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

    # おすすめのユーザを取得
    # /users/friends/
    @classmethod
    def get_recommend(self, request,  *args, **kwargs):
        try:

            # TODO バリデーションチェック
            query_param = request.GET
            with connection.cursor() as cursor:
                recommend_users = []
                str = "Python"
                # cursor.execute('''SELECT * FROM app_user WHERE user_id !='%s' and json_contains(skill,'["%s"]', '$.lang')''' % (query_param["user_id"], str))
                cursor.execute('''SELECT * FROM app_user WHERE user_id !=%s''' ,[query_param.get("user_id")])
                rows = dictfetchall(cursor)
                print(rows)
            for obj in rows:
                obj['profile'] = json.loads(obj['profile'])
                recommend_users.append(obj)

            response = JsonResponse(
                {"status": 200, "message": "ok", "friends": recommend_users},
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


    # 友達申請を送る
    # /users/follow/
    @classmethod
    def follow(self, request,  *args, **kwargs):
        try:
            sid = transaction.savepoint()
            # TODO バリデーションチェック
            post = request.POST
            request_user_id = post['request_user_id']
            follower_user_id = post['follower_user_id']
            # 既に友達かどうかチェック
            if Friend.objects.filter(
                    (Q(request_user_id=request_user_id, follower_user_id=follower_user_id) |
                    Q(follower_user_id=request_user_id, request_user_id=follower_user_id)),
                    approval=1).exists():
                raise Exception(700, '既に友達登録されています。')

            # 既に友達申請している（されている）かチェック
            if Friend.objects.filter(
                    (Q(request_user_id=request_user_id, follower_user_id=follower_user_id) |
                    Q(follower_user_id=request_user_id, request_user_id=follower_user_id))
            ).exists():
                raise Exception(710, '既に友達申請中です。')

            # 友達申請
            friend_id = getuniqueid()
            f = Friend.objects.create(
                friend_id=friend_id
                , request_user_id=request_user_id
                , follower_user_id=follower_user_id
                , follow_dt=timezone.datetime.now()
                , create_dt=timezone.datetime.now()

            )
            f.save()
            response = JsonResponse(
                {'status': 200, "message": "OK"},
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
                {'status': e.args[0], "message": e.args[1]},
                safe=False
            )
        return response

    # 友達申請を許可する
    # /friends/approval/
    @classmethod
    def approval(self, request,  *args, **kwargs):
        sid = transaction.savepoint()
        try:
            post = request.POST

            if Friend.objects.filter(
                    request_user_id=post['request_user_id']
                    , follower_user_id=post['follower_user_id'])\
                .update(
                    approval=1
                    , approval_dt=timezone.datetime.now()
            ) == 0:
                raise Exception(999, '【ERROR】データがありません。')

            response = JsonResponse(
                {'status': 200, "message": "OK"},
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
                {'status': 999, "message": e.args[1]},
                safe=False
            )
        return response

    # 友達申請を拒否する
    # /friends/reject/
    @classmethod
    def reject(self, request, *args, **kwargs):
        try:
            sid = transaction.savepoint()
            post = request.POST

            if Friend.objects.filter(
                    id=post['friend_id'],
                    follower_user_id=post['follower_user_id'],) \
                    .update(reject=1, reject_dt=timezone.now()) == 0:
                raise Exception(999, '【ERROR】データがありません。')

            response = JsonResponse(
                {'status': 200, "message": "OK"},
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
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response

    # 友達をやめる
    # /friends/brock/
    @classmethod
    def brock(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            post = request.POST

            Friend.objects.filter(
                Q(request_user_id=post['brock_user_id']) | Q(follower_user_id=post['brock_user_id'])).update(brock_user_id=post['brock_user_id'], brock_dt=timezone.now())

            response = JsonResponse(
                {'status': 200, "message": "OK"},
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
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response

    # 友達申請ステータス
    # /friends/approval/
    @classmethod
    def getStatus(self, request,  *args, **kwargs):
        try:

            # 既に友達登録されているかチェック
            if FriendViewSet.check_follow(request):
                raise Exception(700, '既に友達登録されています。')

            # 申請が拒否されているかチェック
            if FriendViewSet.check_reject(request):
                raise Exception(720, '友達申請が拒否されました。')

            # ブロックされているかチェック
            if FriendViewSet.check_brock(request):
                raise Exception(730, 'ブロックされています。')

            # 既に友達申請しているかチェック
            check_request = FriendViewSet.check_request(request)
            if check_request:
                raise Exception(710, '既に友達申請しています。')

            # 既に友達申請されているかチェック
            check_request = FriendViewSet.check_requested(request)
            if check_request:
                raise Exception(711, '既に友達申請されています。')

            response = JsonResponse(
                {'status': 200, "message": "OK"},
                safe=False
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

    def check_request(request):
        try:
            post = request.POST
            request_user_id = post['request_user_id']
            follower_user_id = post['follower_user_id']

            # 既に友達申請している（されている）かチェック
            if Friend.objects.filter(
                (Q(request_user_id=request_user_id, follower_user_id=follower_user_id,reject=0, approval=0, brock_user_id__isnull=True))
            ).exists():
                return True
            else:
                return False
        except Exception as e:
            response = JsonResponse(
                {'status': 999, "message": e.args[1]},
                safe=False
            )
        return response

    def check_requested(request):
        try:
            post = request.POST
            request_user_id = post['request_user_id']
            follower_user_id = post['follower_user_id']

            # 既に友達申請されているかチェック
            if Friend.objects.filter(
                    (Q(request_user_id=follower_user_id, follower_user_id=request_user_id,reject=0, approval=0, brock_user_id__isnull=True))
            ).exists():
                return True
            else:
                return False
        except Exception as e:
            response = JsonResponse(
                {'status': 999, "message": e.args[1]},
                safe=False
            )
        return response


    def check_follow(request):
        try:
            post = request.POST
            request_user_id = post['request_user_id']
            follower_user_id = post['follower_user_id']

            if Friend.objects.filter(
                    (Q(request_user_id=request_user_id, follower_user_id=follower_user_id) |
                     Q(follower_user_id=request_user_id, request_user_id=follower_user_id)),
                    approval=1).exists():
                return True
            else:
                return False
        except Exception as e:
            response = JsonResponse(
                {'status': 999, "message": e.args[1]},
                safe=False
            )
        return response

    def check_reject(request):
        try:
            post = request.POST
            request_user_id = post['request_user_id']
            follower_user_id = post['follower_user_id']

            if Friend.objects.filter(
                    (Q(request_user_id=request_user_id, follower_user_id=follower_user_id) |
                     Q(follower_user_id=request_user_id, request_user_id=follower_user_id)),
                    approval=1, reject=1).exists():
                return True
            else:
                return False
        except Exception as e:
            response = JsonResponse(
                {'status': 999, "message": e.args[1]},
                safe=False
            )
        return response

    def check_brock(request):
        try:
            post = request.POST
            request_user_id = post['request_user_id']
            follower_user_id = post['follower_user_id']

            if Friend.objects.filter(
                    (Q(request_user_id=request_user_id, follower_user_id=follower_user_id) |
                     Q(follower_user_id=request_user_id, request_user_id=follower_user_id)),
                    approval=1, brock_user_id__isnull=False).exists():
                return True
            else:
                return False
        except Exception as e:
            response = JsonResponse(
                {'status': 999, "message": e.args[1]},
                safe=False
            )
        return response
