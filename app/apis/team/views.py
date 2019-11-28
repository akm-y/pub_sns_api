# coding: utf-8
import json
from app.models import Team, Member
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.db import transaction, connection
from app.libs.common import dictfetchall, getuniqueid
from app.apis.notification.views import NotificationViewSet

class TeamViewSet:

    # チームマスタを作成
    @classmethod
    def create_team(self, request,  *args, **kwargs):
        try:
            sid = transaction.savepoint()
            body = request.POST
            name = body['name']
            category = body['category']
            image_path = body['image_path']
            contents = body['contents']
            user_id = body['user_id']
            team_id = getuniqueid()

            # チームを作成
            nt = Team.objects.create(
                team_id=team_id
                , name=name
                # , category=category
                , image_path=image_path
                , contents=contents
            )

            # 作成者を管理人として登録
            nt2 = Member.objects.create(
                team_id=team_id
                ,user_id=user_id
                ,role=2
                ,approval=1
                ,approval_dt=timezone.now()
                ,create_dt=timezone.now()
            )

            nt.save()
            nt2.save()

            # result = NotificationViewSet.note_join(request,  *args, **kwargs)
            #
            # if not result:
            #     raise Exception(999, '【ERROR】お知らせ登録に失敗しました。。')

            response = JsonResponse(
                {"status": 200, "message": "ok", "team_id": team_id},
                safe=True,
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

    # チームマスタを作成
    @classmethod
    def update_team(self, request,  *args, **kwargs):
        try:
            sid = transaction.savepoint()
            body = request.POST
            name = body['name']
            category = body['category']
            image_path = body['image_path']
            contents = body['contents']
            team_id = body['team_id']

            # チームを更新
            nt = Team.objects.filter(team_id=team_id).update(
                name=name
                , image_path=image_path
                , contents=contents
            )

            response = JsonResponse(
                {"status": 200, "message": "ok", "team_id": team_id},
                safe=True,
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

    # チームマスタを削除
    @classmethod
    def delete_team(self, request,  *args, **kwargs):
        try:
            sid = transaction.savepoint()

            body = request.POST
            team_id = body.get('team_id')
            user_id = body.get('user_id')

            # 権限チェック
            if not TeamViewSet.is_owner(body):
                raise Exception(403, '権限がありありません')

            if TeamViewSet.is_delete(body):
                raise Exception(750, 'このチームは削除されています。')

            if Team.objects.filter(
                team_id=team_id
            ).update(
                del_flg=1
                , update_dt=timezone.now()
            ) == 0:
                raise Exception(999, '【ERROR】データがありません。')

            response = JsonResponse(
                {"status": 200, "message": "ok"},
                safe=True,
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

    # チームマスタを更新
    
    
    # 所属チームを取得
    @classmethod
    def get_my_team(self, request,  *args, **kwargs):
        try:
            # TODO バリデーションチェック
            param = request.GET
            print(param.get("user_id"))
            with connection.cursor() as cursor:
                user_id = param.get("user_id")
                cursor.execute('''
                SELECT
                 tmp1.*,
                 tmp2.*,
                CASE `role` WHEN '2' THEN 'true' ELSE 'false' END as is_owner
                FROM app_member as tmp1
                 INNER JOIN app_team as tmp2 ON tmp1.team_id = tmp2.team_id
                WHERE tmp1.user_id = '%s' AND 
                tmp1.approval = 1 AND 
                tmp1.del_flg = 0
                ''' % (user_id))
                my_team = dictfetchall(cursor)



            response = JsonResponse(
                {"status": 200, "message": "ok", "team": my_team},
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

    # おすすめのチームを取得
    @classmethod
    def get_recommend(self, request,  *args, **kwargs):
        try:
            get = request.GET

            # TODO バリデーションチェック
            recommend_list = []
            for obj in Team.objects.order_by('create_dt').filter(
                    del_flg=0,
                    approval=0,
                    reject=0,
                    request=0
            ).values()[:5]:
                recommend_list.append(obj)
            response = JsonResponse(
                {"status": 200, "message": "ok", "team": recommend_list},
                safe=True,
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

    # 参加申請を送る
    @classmethod
    def join(self, request,  *args, **kwargs):
        sid = transaction.savepoint()
        try:
            # TODO バリデーションチェック
            body = request.POST
            user_id = body["user_id"]
            team_id = body["team_id"]

            # チーム存在チェック
            if not TeamViewSet.team_exists(body):
                raise Exception(740, '存在しないチームです。')

            # 既にメンバーかチェック
            if TeamViewSet.is_joined(body):
                raise Exception(700, '既に参加しています。')

            # 既に参加申請しているかチェック
            if TeamViewSet.is_join(body):
                raise Exception(710, '既に参加申請中です。')

            # 参加(とりあえず申請制ではなく即参加)
            n = Member.objects.create(
                user_id=user_id
                , team_id=team_id
                , request_dt=timezone.now()
                , role=1
                , approval=1
            )
            n.save()

            # お知らせテーブルに登録

            response = JsonResponse(
                {'status': 200, "message": "ok", "team_id":n.team_id},
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
    @classmethod
    def approval(self, request,  *args, **kwargs):
        sid = transaction.savepoint()
        try:
            body = request.POST
            user_id = body.get("user_id")
            approval_user_id = body.get("user_id")
            team_id = body.get("team_id")

            if not TeamViewSet.is_owner(body):
                raise Exception(403,'管理者ではありません')

            if Member.objects.filter(
                user_id=approval_user_id
                , team_id=team_id
                , request=1
                , reject=0
                , brock=0
            ).update(
                approval=1
                , approval_dt=timezone.now()
                , update_user_id = user_id
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

    # 友達をやめる
    @classmethod
    def brock(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            body = request.POST
            user_id = body.get("user_id")
            brock_user_id = body.get("brock_user_id")
            team_id = body.get("team_id")

            if not TeamViewSet.is_owner(body):
                raise Exception(403,'管理者ではありません')

            if Member.objects.filter(
                    user_id=brock_user_id
                    , team_id=team_id
            ).update(
                brock=1
                , brock_dt=timezone.now()
                , update_user_id=user_id
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
            response = JsonResponse(
                {'status':  e.args[0], "message": e.args[1]},
                safe=False
            )
        return response

    # 参加申請を拒否する
    @classmethod
    def reject(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            body = request.POST
            user_id = body.get("user_id")
            reject_user_id = body.get("reject_user_id")
            team_id = body.get("team_id")

            if not TeamViewSet.is_owner(body):
                raise Exception(403,'管理者ではありません')

            if Member.objects.filter(
                    user_id=reject_user_id
                    , team_id=team_id
                    , request=1
                    , brock=0
            ).update(
                reject=1
                , reject_dt=timezone.now()
                , update_user_id=user_id
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

    # チームの詳細情報を取得
    @classmethod
    def get_detail(self, request,  *args, **kwargs):
        sid = transaction.savepoint()
        try:
            param = request.GET
            team_id = param.get("team_id")

            detail = {}
            with connection.cursor() as cursor:
                cursor.execute('''
                select 
                *
                 from 
                (
                select count(*) as member_cnt
                from  app_team as tmp1
                inner join app_member as tmp2 on tmp1.team_id = tmp2.team_id
                where
                 tmp1.team_id='%s' and
                 tmp2.del_flg=0 and
                 tmp2.brock=0
                ) as member_cnt,
                (
                select count(*) as entry_cnt
                 from app_team as tmp1
                inner join app_entry as tmp2 on tmp1.team_id = tmp2.team_id
                ) as entry_cnt,
                (
                select * from app_team as tmp3
                 where tmp3.team_id='%s' and
                  tmp3.del_flg =0
                ) as info''' % (team_id, team_id))
                info = dictfetchall(cursor)
                detail["info"] = info

                detail["is_joined"] = TeamViewSet.is_joined(param)
                detail["is_owner"] = TeamViewSet.is_owner(param)

            response = JsonResponse(
                {'status': 200, "message": "OK", "detail": detail},
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

    # チームの詳細情報を取得
    @classmethod
    def get_members(self, request,  *args, **kwargs):
        sid = transaction.savepoint()
        try:
            param = request.GET
            team_id = param.get("team_id")
            members = []
            with connection.cursor() as cursor:
                cursor.execute('''
                SELECT *
                    FROM app_member
                    INNER JOIN app_user ON app_member.user_id = app_user.user_id
                    WHERE app_member.team_id = '%s' AND app_member.approval = 1 AND app_user.del_flg = 0
                ''' % (team_id))
                rows = dictfetchall(cursor)

            for obj in rows:
                obj['profile'] = json.loads(obj['profile'])
                members.append(obj)

            response = JsonResponse(
                {'status': 200, "message": "OK", "members": members},
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

    # チーム参加申請ステータス
    @classmethod
    def getStatus(self, request,  *args, **kwargs):
        try:
            body = request.GET

            if not TeamViewSet.is_owner(body):
                raise Exception(750, 'このチームは削除されています。')

            # 既にメンバー登録されているかチェック
            if TeamViewSet.is_delete(body):
                raise Exception(750, 'このチームは削除されています。')

            # 既にメンバー登録されているかチェック
            if TeamViewSet.is_joined(body):
                raise Exception(700, '既にチーム登録されています。')

            # 申請が拒否されているかチェック
            if TeamViewSet.is_reject(body):
                raise Exception(720, '既に参加申請されています。')

            # ブロックされているかチェック
            if TeamViewSet.is_brock(body):
                raise Exception(730, 'ブロックされています。')

            # 既にメンバー登録されているかチェック
            if TeamViewSet.is_join(body):
                raise Exception(700, '既に参加申請されています。')

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

    def is_join(body):
        try:
            user_id = body['user_id']
            team_id = body['team_id']

            # 既に友達申請している（されている）かチェック
            if Member.objects.filter(
                user_id=user_id
                , team_id=team_id
                , reject=0
                , approval=0
                , request=1
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

    def is_joined(body):
        try:
            user_id = body['user_id']
            team_id = body['team_id']

            if Member.objects.filter(
                user_id=user_id
                , team_id=team_id
                , reject=0
                , approval=1
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

    def is_reject(request):
        try:
            body = request.POST
            user_id = body['user_id']
            team_id = body['team_id']

            if Member.objects.filter(
                user_id=user_id
                , team_id=team_id
                , request=1
                , reject=1
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

    def is_brock(request):
        try:
            body = request.POST
            user_id = body['user_id']
            team_id = body['team_id']

            if Member.objects.filter(
                user_id=user_id
                , team_id=team_id
                , request=1
                , approval=1
                , brock=1
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

    def is_owner(body):
        try:
            user_id = body['user_id']
            team_id = body['team_id']

            if Member.objects.filter(
                    user_id=user_id
                    , team_id=team_id
                    , role=2
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

    def is_delete(body):
        try:
            user_id = body['user_id']
            team_id = body['team_id']

            if Team.objects.filter(
                    team_id=team_id
                    , del_flg=1
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

    def team_exists(body):
        try:
            team_id = body['team_id']

            if Team.objects.filter(
                     team_id=team_id
                    , del_flg=0
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
