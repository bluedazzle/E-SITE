# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from DjangoUeditor.models import UEditorField


class OilCard(models.Model):
    card = models.CharField(help_text="oil card id", max_length=32, verbose_name='加油卡')

    class Meta:
        verbose_name = '加油卡'
        verbose_name_plural = '加油卡'
        ordering = ['id']

    def __unicode__(self):
        return self.card


class Account(AbstractUser):
    oilcard = models.ForeignKey('OilCard', help_text='Oil Card ID', null=True, verbose_name='加油卡')
    vid = models.CharField(help_text='Vip Card ID', max_length=32, unique=True, verbose_name='VIP卡号')

    def __unicode__(self):
        return self.username


class Shop(models.Model):
    link = models.CharField(max_length=512, blank=True, null=True, verbose_name='活动链接')
    name = models.CharField(max_length=256, unique=True, verbose_name='活动名称')
    image = models.ImageField(upload_to='static/site/img', verbose_name='活动图片')
    enable = models.BooleanField(default=True, verbose_name='活动开启')

    class Meta:
        verbose_name = '优惠活动'
        verbose_name_plural = '优惠活动'
        ordering = ['id']

    def __unicode__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=50, verbose_name='加油站')
    address = models.CharField(max_length=512, verbose_name='地址')
    longitude = models.CharField(max_length=20, verbose_name='经度')
    latitude = models.CharField(max_length=20, verbose_name='纬度')
    tel = models.CharField(max_length=20, null=True, default=None, verbose_name='联系电话')
    is_recharge = models.BooleanField(default=True, verbose_name='充值站点')

    class Meta:
        verbose_name = '加油站'
        verbose_name_plural = '加油站'
        ordering = ['id']

    def __unicode__(self):
        return self.name


class OilPrice(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='Oil Type Name', verbose_name='石油类型')
    kind = models.CharField(max_length=30, verbose_name='分类')
    price = models.FloatField(verbose_name='价格')

    class Meta:
        verbose_name = '油价'
        verbose_name_plural = '油价'
        ordering = ['id']

    def __unicode__(self):
        return self.name


class SignIn(models.Model):
    user = models.ForeignKey('Account',  help_text='Account Id', verbose_name='用户')
    year = models.IntegerField(verbose_name='年')
    month = models.IntegerField(verbose_name='月')
    day = models.IntegerField(verbose_name='日')

    class Meta:
        verbose_name = '签到'
        verbose_name_plural = '签到'
        ordering = ['id']

    def __unicode__(self):
        return self.user


class Intro(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    image = models.ImageField(upload_to='static/site/img', verbose_name='图片')
    content = UEditorField(verbose_name='内容', imagePath='static/intro/img')
    is_show = models.BooleanField(default=False, verbose_name='显示')

    class Meta:
        verbose_name = '加油卡介绍'
        verbose_name_plural = '加油卡介绍'
        ordering = ['id']

    def __unicode__(self):
        return self.title


class Question(models.Model):
    que = models.CharField(max_length=200, verbose_name='问题')
    ans = UEditorField(verbose_name='解答', imagePath='static/intro/img')
    is_show = models.BooleanField(default=False, verbose_name='显示')

    class Meta:
        verbose_name = '在线答疑'
        verbose_name_plural = '在线答疑'
        ordering = ['id']

    def __unicode__(self):
        return self.que
