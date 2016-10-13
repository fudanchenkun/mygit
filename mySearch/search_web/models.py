# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class List(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    platform = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    sum = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    limittime = models.IntegerField(blank=True, null=True)
    rate = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    process = models.CharField(max_length=10, blank=True, null=True)
    peoplenum = models.IntegerField(blank=True, null=True)
    heatvalue = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    decription = models.TextField(blank=True, null=True)
    indexsum = models.IntegerField(blank=True, null=True)
    indextime = models.IntegerField(blank=True, null=True)
    indexrate = models.IntegerField(blank=True, null=True)
    document = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'list'


class ListSource(models.Model):
    # id = models.AutoField()
    title = models.CharField(max_length=300, blank=True, null=True)
    platform = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    sum = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    limittime = models.IntegerField(blank=True, null=True)
    rate = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    process = models.CharField(max_length=10, blank=True, null=True)
    peoplenum = models.IntegerField(blank=True, null=True)
    heatvalue = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    decription = models.TextField(blank=True, null=True)
    indexsum = models.IntegerField(blank=True, null=True)
    indextime = models.IntegerField(blank=True, null=True)
    indexrate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'list_source'


class News(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    page_title = models.CharField(max_length=600, blank=True, null=True)
    news_url = models.CharField(max_length=200, blank=True, null=True)
    news_part = models.TextField(blank=True, null=True)
    document = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'news'


class NewsSource(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    page_title = models.CharField(max_length=600, blank=True, null=True)
    page_keywords = models.CharField(max_length=600, blank=True, null=True)
    page_description = models.TextField(blank=True, null=True)
    news_title = models.CharField(max_length=600, blank=True, null=True)
    news_time = models.TextField(blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_part = models.TextField(blank=True, null=True)
    news_url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_source'


class SearchWebListinfo(models.Model):
    title = models.CharField(max_length=50)
    platform = models.CharField(max_length=50)
    url = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'search_web_listinfo'


class SpReqinfo(models.Model):
    # id = models.AutoField()
    platform = models.CharField(max_length=100, blank=True, null=True)
    count_req = models.IntegerField(blank=True, null=True)
    count_suc = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp_reqinfo'
