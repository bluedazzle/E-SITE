# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'password', 'last_login', 'oilcard', 'vid',
    )


class ShopAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'image', 'link', 'enable',
    )


class OilCardAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'card',
    )


class StationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'address', 'longitude', 'latitude', 'tel', 'is_recharge',
    )


class OilPriceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'kind', 'price',
    )


class SignInAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'year', 'month', 'day',
    )


class IntroAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'image', 'is_show',
    )


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'que', 'ans', 'is_show',
    )


admin.site.register(Account, AccountAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(OilCard, OilCardAdmin)
admin.site.register(Station, StationAdmin)
# admin.site.register(OilType, OilTypeAdmin)
admin.site.register(OilPrice, OilPriceAdmin)
admin.site.register(SignIn, SignInAdmin)
admin.site.register(Intro, IntroAdmin)
admin.site.register(Question, QuestionAdmin)
