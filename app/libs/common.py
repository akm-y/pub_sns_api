import datetime
from uuid import getnode as get_mac
import uuid
from django.utils import timezone
import boto3


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def getuniqueid():
    (dt, micro) = timezone.now().strftime('%Y%m%d%H%M%S.%f').split('.')
    dt = "%s%03d" % (dt, int(micro) / 1000)
    mac_addr = hex(uuid.getnode()).replace('0x', '')

    return dt + mac_addr


def upload2S3():
    s3 = boto3.client('s3',
        aws_access_key_id='',
        aws_secret_access_key='',
        region_name='ap-northeast-1'
    )