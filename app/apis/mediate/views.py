# coding: utf-8

import json
from app.models import User, Friend, Mediate
from django.http import JsonResponse
import sys
from django.db.models import Q
from django.utils import timezone


class MediateViewSet:

    # 紹介情報を保存
    # /mediate/
    @classmethod
    def do_mediate(self, request, *args, **kwargs):
        try:
            post = request.POST
            # TODO バリデーション
            # お二人はすでに友達
            if Friend.objects.filter(
                    (Q(request_user_id=post['from_user_id'], follower_user_id=post['to_user_id']) |
                     Q(request_user_id=post['to_user_id'], follower_user_id=post['from_user_id'])),
                    approval=1).exists():
                response = JsonResponse(
                    {'status': 800, "message": "お二人は既に友達です。"},
                    safe=False
                )
                return response

            # お二人はすでに紹介済み
            if Mediate.objects.filter(
                    (Q(from_user_id=post['from_user_id'], to_user_id=post['to_user_id']) |
                     Q(from_user_id=post['to_user_id'], to_user_id=post['from_user_id']))
                    ).exists():
                response = JsonResponse(
                    {'status': 800, "message": "お二人は既に紹介済みです。"},
                    safe=False
                )
                return response

            result = Mediate.objects.create(
                    mediate_user_id=post['mediate_user_id'],
                    from_user_id=post['from_user_id'],
                    to_user_id=post['to_user_id'],
                    create_dt=timezone.now()
            )
            response = JsonResponse(
                {'status': 200, "id": result.id},
                safe=False
            )

        except KeyError as e:
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
             )
        except Exception as e:
            response = JsonResponse(
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response

    # fromユーザが紹介を承認
    # /mediate/approval/from/
    @classmethod
    def from_approval(self, request, *args, **kwargs):
        try:
            # TODO バリデーション
            post = request.POST

            obj = Mediate.objects.values('to_user_id') \
                .filter(id=post['id'], from_user_id=post['from_user_id'])

            to_user_id = obj[0]['to_user_id']
            from_user_id = post['from_user_id']

            # お二人はすでに友達
            if Friend.objects.filter(
                    (Q(request_user_id=from_user_id, follower_user_id=to_user_id) |
                     Q(request_user_id=to_user_id, follower_user_id=from_user_id)),
                    approval=1).exists():
                response = JsonResponse(
                    {'status': 800, "message": "お二人は既に友達です。"},
                    safe=False
                )
                return response

            result = Mediate.objects.filter(
                id=post['id'],
                from_user_id=from_user_id,
                to_reject=0
            ).update(
                from_approval=1,
                from_approval_dt=timezone.now()
            )
            if result < 1:
                response = JsonResponse(
                    {'status': 981, "message": "Mediate create NG"},
                    safe=False
                )
                return response
            if Mediate.objects.filter(id=post['id'], from_approval=1, to_approval=1).exists():
                # TODO FriendsのAPIへ
                Friend.objects.create(
                    request_user_id=from_user_id,
                    follower_user_id=to_user_id,
                    approval=1,
                    approval_dt=timezone.now(),
                    create_dt=timezone.now(),
                    del_flg=0
                )
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
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response

    # toユーザが紹介を承認
    # fromユーザが承認済みの場合は友達マッチ
    # /mediate/approval/to/
    @classmethod
    def to_approval(self, request, *args, **kwargs):
        try:
            # TODO バリデーション
            post = request.POST

            obj = Mediate.objects.values('from_user_id')\
                .filter(id=post['id'], to_user_id=post['to_user_id'])

            from_user_id = obj[0]['from_user_id']
            to_user_id = post['to_user_id']

            # お二人はすでに友達
            if Friend.objects.filter(
                    (Q(request_user_id=from_user_id, follower_user_id=to_user_id) |
                     Q(request_user_id=to_user_id, follower_user_id=from_user_id)),
                    approval=1).exists():
                response = JsonResponse(
                    {'status': 800, "message": "お二人は既に友達です。"},
                    safe=False
                )
                return response

            result = Mediate.objects.filter(
                id=post['id'],
                to_user_id = to_user_id,
                to_reject = 0
            ).update(
                to_approval=1,
                to_approval_dt=timezone.now()
            )
            if result < 1:
                response = JsonResponse(
                    {'status': 981, "message": "Mediate create NG"},
                    safe=False
                )
                return response

            if Mediate.objects.filter(id=post['id'], from_approval=1, to_approval=1).exists():
                # TODO FriendsのAPIへ
                Friend.objects.create(
                    request_user_id=from_user_id,
                    follower_user_id=to_user_id,
                    approval=1,
                    approval_dt=timezone.now(),
                    create_dt=timezone.now(),
                    del_flg=0
                )
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
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response

    # fromユーザが紹介を拒否
    # /mediate/approval/reject/
    @classmethod
    def from_reject(self, request, *args, **kwargs):
        try:
            # TODO バリデーション
            post = request.POST

            # お二人はすでに紹介済み
            if Mediate.objects.filter(
                    id=post['id'],
                    from_user_id=post['from_user_id'],
                    from_reject=1
            ).exists():
                response = JsonResponse(
                    {'status': 800, "message": "既に拒否しています。"},
                    safe=False
                )
                return response

            result = Mediate.objects.filter(
                id=post['id'],
                from_user_id=post['from_user_id']
            ).update(
                from_reject=1,
                from_reject_dt=timezone.now()
            )

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
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response

    # fromユーザが紹介を拒否
    # /mediate/approval/reject/
    @classmethod
    def to_reject(self, request, *args, **kwargs):
        try:
            # TODO バリデーション
            post = request.POST

            # お二人はすでに紹介済み
            if Mediate.objects.filter(
                    id=post['id'],
                    to_user_id=post['to_user_id'],
                    to_reject=1
            ).exists():
                response = JsonResponse(
                    {'status': 800, "message": "既に拒否しています。"},
                    safe=False
                )
                return response

            result = Mediate.objects.filter(
                id=post['id'],
                to_user_id=post['to_user_id']
            ).update(
                to_reject=1,
                to_reject_dt=timezone.now()
            )

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
                {'status': 999, "message": e.args[0]},
                safe=False
            )
        return response
