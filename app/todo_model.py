from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class ToDoModel(Model):
    class Meta:
        table_name = 'users'
        region = 'ap-northeast-1'
        write_capacity_units = 5
        read_capacity_units = 5

        # テーブル定義
        # id = UnicodeAttribute(hash_key=True, null=False)
        # createdBy = UnicodeAttribute(null=False)
        # createdAt = UTCDateTimeAttribute(range_key=True, null=False, default=datetime.now())
        # text = UnicodeAttribute(null=False)
        # checked = BooleanAttribute(null=False, default=False)
        # updatedAt = UTCDateTimeAttribute(null=False, default=datetime.now())
