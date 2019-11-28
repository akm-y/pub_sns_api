# coding: utf-8

from rest_framework.response import Response
from django.http import HttpResponse
from .apis import Apis
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets
from ..models import User

# @api_view(['GET', 'POST'])
@csrf_exempt#本番ではトークンを利用する
def index(request):
    print(request.method)
    if request.method == 'POST':
        request_data = request.POST
        return HttpResponse(
            json.dumps(
                {"message": "Got some data!", "data": request_data.get('name')}
            )
        )

    elif request.method == 'GET':
        apis = Apis()
        result = apis.get()
        print(result)
        return HttpResponse(result)
