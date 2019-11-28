# coding: utf-8

import json
from app.models import User, Friend
from django.http import JsonResponse
import random, string
from app.libs.myCrypt import get_decrypt_data,get_encrypt_data
from api.settings import common as common_settings
from django.core import serializers
from django.utils import timezone
import boto3
import base64
import uuid
import re

import environ
env = environ.Env()
BASE_DIR = environ.Path(__file__) - 3
env_file = str(BASE_DIR.path('.env'))
env.read_env(env_file)

class UserViewSet:

    @classmethod
    def get_user(self, request,  *args, **kwargs):
        try:
            bucket_name = env('DJANGO_AWS_S3_BUCKET_NAME')
            s3 = boto3.resource('s3')
            for b in s3.buckets.all():
                print(b)

            query_param = request.GET


            user = []
            for obj in User.objects.values('user_id', 'auth_id', 'skill', 'profile').filter(user_id=query_param.get("user_id")):
                # obj['image_path'] = image
                user.append(obj)

            if len(user) < 1:
                raise KeyError

            response = JsonResponse(
                {"status": 200, "message": "", "user": user[0]},
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
            post = request.POST
            user = User.objects.create(
                user_id=post['user_id'],
                auth_id=post['auth_id'],
                mail=post['email'],
                create_dt=timezone.datetime.now()
                # skill=json.loads(post['skill']) if ('skill' in post) else {},
                # profile=json.loads(post['profile']) if ('skill' in post) else {},
                # del_flg='0'
            )

            # decrypt_data = get_decrypt_data(user_id, common_settings.CRYPT_KEY, common_settings.CRYPT_IV).decode('utf-8')
            response = JsonResponse(
                {"message": "OK", 'status': 200, 'user_id': post['user_id']},
                safe=False
            )
        except KeyError as e:
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            response = JsonResponse(
                {"message": e.args[1], 'status': 999},
                safe=False
            )
        response['Access-Control-Allow-Origin'] = 'http://localhost:1234'
        return response

    @classmethod
    def profile_update(self, request,  *args, **kwargs):
        try:
            post = request.POST
            print(json.loads(post['profile']))
            user = User.objects.filter(
                user_id=post['user_id'],
            ).update(
                profile=json.loads(post['profile'])
            )
            response = JsonResponse(
                {"message": "OK", 'status': 200},
                safe=False
            )
        except KeyError as e:
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            response = JsonResponse(
                {"message": e.args[0], 'status': 999},
                safe=False
            )
        response['Access-Control-Allow-Origin'] = 'http://localhost:1234'
        return response

    @classmethod
    def skill_register(self, request,  *args, **kwargs):
        try:
            post = request.POST

            user = User.objects.filter(
                user_id=post['user_id'],
            ).update(
                skill=json.loads(post['skill'])
            )
            response = JsonResponse(
                {"message": "OK", 'status': 200},
                safe=False
            )
        except KeyError as e:
            response = JsonResponse(
                {'status': 980, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            response = JsonResponse(
                {"message": e.args[0], 'status': 999},
                safe=False
            )
        response['Access-Control-Allow-Origin'] = 'http://localhost:1234'
        return response

    @classmethod
    def photo_register(self, request,  *args, **kwargs):
        try:
            post = request.POST

            # print(json.loads(post['profile']))
            # user = User.objects.filter(
            #     user_id=post['user_id'],
            # ).update(
            #     profile=json.loads(post['profile'])
            # )

            # リクエストはbase64でエンコードされている
            base64_str = post['user_photo']

            # 拡張子を取得
            file_extention = base64_str[base64_str.find('/')+1:base64_str.find(';')]

            # Content-Typeを取得
            content_type = base64_str[base64_str.find(':')+1:base64_str.find(';')]

            # 余計な文字列を除去
            # file_data = re.sub("/^data:+;base64,/", '', base64_str)
            file_data = (base64_str.split(","))
            # base64をデコード
            dec_file = base64.b64decode(file_data[1])

            bucket_name = env('DJANGO_AWS_S3_BUCKET_NAME')
            s3 = boto3.resource('s3')
            print(list(s3.buckets.all()))
            res = s3.Bucket(bucket_name).put_object(
                # Key=f'{uuid.uuid4()}.jpg',
                Key=env('DJANGO_AWS_S3_USER_PHOTO_DIR') + '/' + post['user_id'] + "." + file_extention,
                Body=dec_file,
                ContentType=content_type
            ),
            # s3.Bucket(bucket_name).upload_file(post['user_photo'], 'User/' + post['user_id'] + ".jpeg")

            response = JsonResponse(
                {"message": "photoOK", 'status': 200},
                safe=False
            )

        except KeyError as e:
            response = JsonResponse(
                {'status': 981, "message": e.args[0] + "が存在しません。"},
                safe=False
            )
        except Exception as e:
            response = JsonResponse(
                {"message": e.args[0], 'status': 999},
                safe=False
            )
        response['Access-Control-Allow-Origin'] = 'http://localhost:1234'
        return response

    @classmethod
    def convert_b64_string_to_bynary(s):
        return base64.b64decode(s.encode("UTF-8"))

@classmethod
def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

