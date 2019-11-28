# coding: utf-8

import django_filters
from rest_framework import viewsets, filters
from ..models import Log, Entry, User
from boto3.dynamodb.conditions import Key, Attr
from django.http.response import JsonResponse
import json
from decimal import Decimal
from ..JSONResponseMixin import JSONResponseMixin


def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError


class Apis(JSONResponseMixin):
    def get(self):
        log = Log()
        res = log.dynamodb.Table('Log').query(
            KeyConditionExpression=Key('year').eq(1985)
        )
        return json.dumps(res['Items'][0], default=decimal_default_proc)
