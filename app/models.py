from django.db import models
from datetime import datetime
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
import boto3
from django_mysql.models import JSONField, Model
from django.db import migrations, models
import uuid


class Log(models.Model):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = 'Log'

    def create_table(self):
        existing_tables = self.dynamodb.list_tables()['TableNames']
        if self.table_name not in existing_tables:
            print(self.table_name, 'を作成します')
            table = self.dynamodb.create_table(
                TableName='Log',
                KeySchema=[
                    {
                        'AttributeName': 'year',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'title',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'year',
                        'AttributeType': 'N'
                    },
                    {
                        'AttributeName': 'title',
                        'AttributeType': 'S'
                    },

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            return table
        else:
            print(self.table_name, 'は存在するためテーブル作成をスキップします')


class User(models.Model):
    verbose_name = 'ユーザ情報を管理するテーブル'
    db_table = 'user'
    user_id = models.CharField(auto_created=False, max_length=80, primary_key=True, serialize=False, verbose_name='ID', unique=True)
    auth_id = models.CharField(auto_created=False, max_length=80, serialize=False, unique=True, null=True)
    first_name = models.CharField(max_length=128, blank=False, null=True)
    last_name = models.CharField(max_length=128, blank=False, null=True)
    skill = JSONField(default=dict, null=True)
    profile = JSONField(default=dict, null=True)
    team = JSONField(default=dict, null=True)
    mail = models.EmailField(default='', null=True)
    unsubscribe = models.CharField(choices=[('active', '0'), ('negative', '1')], default='active', max_length=1, null=True)
    type = models.SmallIntegerField(default=1, null=True)
    status = models.SmallIntegerField(default=1, null=True)
    del_flg = models.SmallIntegerField(default=0, max_length=1)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)


class Friend(models.Model):
    verbose_name = '友達を管理するテーブル'
    db_table = 'friend'
    friend_id = models.CharField(primary_key=True, auto_created=False, max_length=80, serialize=False, verbose_name='テーブルID')
    request_user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='リクエストユーザID')
    follower_user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='リクエストを受けたユーザID')
    follow_dt = models.DateTimeField(null=True, auto_now=True)
    approval = models.SmallIntegerField(default=0)
    approval_dt = models.DateTimeField(null=True, auto_now=True)
    reject = models.SmallIntegerField(default=0)
    reject_dt = models.DateTimeField(null=True, auto_now=True)
    brock_user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ID',null=True)
    brock_dt = models.DateTimeField(null=True, auto_now=True)
    mediate = models.SmallIntegerField(default=0),
    del_flg = models.SmallIntegerField(default=0, max_length=1)
    updated_dt = models.DateTimeField(auto_now=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)


# done(完了)後はfriendテーブルへinsert
class Mediate(models.Model):
    db_table = 'mediate'
    verbose_name = '紹介を管理するトランザクションテーブル'
    mediate_user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ID')
    from_user_id = models.CharField(serialize=False, verbose_name='ID', max_length=40)
    from_approval = models.SmallIntegerField(default=0)
    from_approval_dt = models.DateTimeField(null=True, auto_now=True)
    from_reject = models.SmallIntegerField(default=0)
    from_reject_dt = models.DateTimeField(null=True, auto_now=True)
    to_user_id = models.CharField(serialize=False, verbose_name='ID', max_length=40)
    to_approval = models.SmallIntegerField(default=0)
    to_approval_dt = models.DateTimeField(null=True, auto_now=True)
    to_reject = models.SmallIntegerField(default=0)
    to_reject_dt = models.DateTimeField(null=True, auto_now=True)
    mediated = models.SmallIntegerField(default=0)
    mediated_dt = models.DateTimeField(null=True, auto_now=True)
    del_flg = models.SmallIntegerField(default=0, max_length=1)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)


class Team(models.Model):
    db_table = 'team'
    verbose_name = 'チーム情報を管理するテーブル'
    team_id = models.CharField(primary_key=True, auto_created=False, max_length=80, serialize=False, verbose_name='チームID')
    name = models.CharField(auto_created=False, max_length=80,serialize=False, verbose_name='名前')
    category = models.CharField(auto_created=False, max_length=124, serialize=False, default="", null=True, verbose_name='カテゴリ')
    image_path = models.TextField()
    contents = models.CharField(auto_created=False, max_length=124, serialize=False, default="", null=True, verbose_name='説明')
    del_flg = models.SmallIntegerField(default=0, max_length=1)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)


class Member(models.Model):
    db_table = 'team_member'
    verbose_name = 'チーム所属メンバーを管理'
    user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ユーザID')
    team_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ID')
    role = models.SmallIntegerField(default=0) # 0:なし 1:一般 2:管理者
    request = models.SmallIntegerField(default=0, null=True)
    request_dt = models.DateTimeField(auto_now='true', null=True)
    approval = models.SmallIntegerField(default=0,null=True)
    approval_dt = models.DateTimeField(auto_now='true', null=True)
    reject = models.SmallIntegerField(default=0,null=True)
    reject_dt = models.DateTimeField(auto_now='true', null=True)
    brock = models.SmallIntegerField(default=0,null=True)
    brock_dt = models.DateTimeField(auto_now='true', null=True)
    del_flg = models.SmallIntegerField(default=0, max_length=1)
    update_user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ID', null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)


class News(models.Model):
    db_table = 'news'
    verbose_name = 'お知らせを管理するテーブル'
    user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ユーザID',unique=False, null=True)
    team_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='チームID',unique=False, null=True)
    category = models.SmallIntegerField(default=0, null=True)
    contents = models.TextField()
    del_flg = models.SmallIntegerField(default=0, max_length=1)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)


class NewsTran(models.Model):
    db_table = 'news_tran'
    verbose_name = 'ユーザ毎のお知らせを管理するテーブル'
    STATUS_UNREAD = 0
    STATUS_READ = 1
    STATUS_SET = (
        (STATUS_UNREAD, "未読"),
        (STATUS_READ, "既読")
    )
    user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ユーザID',unique=False, null=True)
    news_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='PushID',unique=False)
    push_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='PushID',unique=False, null=True)
    status = models.SmallIntegerField(choices=STATUS_SET, default=STATUS_UNREAD, max_length=2) # 0:未読 1:既読
    del_flg = models.SmallIntegerField(default=0, max_length=1)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)


class Entry(models.Model):
    db_table = 'entry'
    verbose_name = '投稿を管理するテーブル'
    ROLE_ME = 1
    ROLE_TEAM = 2
    ROLE_SET = (
        (ROLE_ME, "フルオープン"),
        (ROLE_TEAM, "指定チーム"),
    )
    STATUS_DRAFT = 0
    STATUS_PRIVATE = 1
    STATUS_TEAM_ONLY = 2
    STATUS_PUBLIC = 3
    STATUS_END = 99

    STATUS_SET = (
        (STATUS_DRAFT, "下書き"),
        (STATUS_PRIVATE, "非公開"), #今は使わない
        (STATUS_PUBLIC, "公開中"),
        (STATUS_END, "終了"),
    )
    entry_id = models.CharField(primary_key=True, auto_created=False, max_length=80, serialize=False, verbose_name='エントリID')
    user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ユーザID')
    team_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ID', null=True)
    # content = JSONField(default=dict, null=True)
    role = models.SmallIntegerField(choices=ROLE_SET, default=ROLE_ME, max_length=2)
    title = models.CharField(max_length=128, default='', null=True)
    contents = models.TextField(default=dict, null=False)
    comment = JSONField(default=dict, null=True)
    category = models.IntegerField(default=99, max_length=3,null=True)
    image_path = models.TextField(default='', null=True)
    status = models.IntegerField(choices=STATUS_SET, default=STATUS_DRAFT, max_length=2)
    entry_start = models.DateTimeField(auto_now=False, null=True)
    entry_end = models.DateTimeField(auto_now=False, null=True)
    del_flg = models.SmallIntegerField(default=0, max_length=1)
    open_dt = models.DateTimeField(auto_now=False, null=True)
    create_dt = models.DateTimeField(auto_now=True)
    update_dt = models.DateTimeField(auto_now=True, null=True)


class EntryCategory(models.Model):
    # CATE_10 = 10
    # CATE_20= 20
    # CATE_30 = 30
    # CATE_99 = 99
    #
    # STATUS_SET = (
    #     (CATE_1, "ブログ"),
    #     (CATE_2, "募集"), #今は使わない
    #     (CATE_3, "技術"),
    #     (CATE_99, "その他"),
    # )

    db_table = 'mst_entry_category'
    verbose_name = '投稿のカテゴリマスタ'
    category_id = models.IntegerField(range(0, 50), default=0)
    category_name = models.CharField(max_length=40)
    del_flg = models.SmallIntegerField(default=0, max_length=1)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)


class TranLikes(models.Model):
    db_table = 'likes'
    verbose_name = '投稿のいいねトランザクションテーブル'
    entry_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ID')
    like_user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='ID')
    unlike_dt = models.DateTimeField(auto_now='true')
    updated_at = models.DateTimeField(auto_now=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)


class Chats(models.Model):
    db_table = 'chats'
    by_user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='byUserId')
    to_user_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='toUserId')
    room_id = models.CharField(auto_created=False, max_length=80, serialize=False, verbose_name='roomId')
    logs = JSONField(default=dict, null=True)
    del_flg= models.SmallIntegerField(default=0, max_length=1)
    create_dt = models.DateTimeField(auto_now=True)