# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class List(models.Model):
    id = models.IntegerField(blank=True, null=True)
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
    id = models.AutoField()
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
    id = models.IntegerField(blank=True, null=True)
    page_title = models.CharField(max_length=600, blank=True, null=True)
    news_url = models.CharField(max_length=200, blank=True, null=True)
    news_part = models.TextField(blank=True, null=True)
    document = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'news'


class NewsSource(models.Model):
    id = models.IntegerField(blank=True, null=True)
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


class SpReqinfo(models.Model):
    id = models.AutoField()
    platform = models.CharField(max_length=100, blank=True, null=True)
    count_req = models.IntegerField(blank=True, null=True)
    count_suc = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp_reqinfo'
