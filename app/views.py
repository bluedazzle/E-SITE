# -*- coding: utf-8 -*-
from datetime import date
from time import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import *
from utils import SMS, create_vid, return_data, verify_mobile, verify_req_params


def send_code(request):
    """ Send SMS Code """
    if request.method == 'POST':
        req_data = request.POST
        mobile = req_data.get('mobile', None)
        res = verify_mobile(mobile)
        if not res:
            msg = "请填写正确手机号!"
            return JsonResponse(return_data(msg=msg))

        # 发送短信验证码
        sms = SMS(mobile)
        result = sms.send()
        if not result:
            msg = "短信验证码发送失败!"
            return JsonResponse(return_data(msg=msg))

        # 避免设置session过期时间造成登录总是超时的问题
        session_data = {
            "expired_at": time() + result[1],
            "code": result[0]
        }

        request.session[mobile] = session_data
        # request.session[mobile] = result[0]
        # request.session.set_expiry(result[1])
        msg = "短信验证码发送成功!"
        return JsonResponse(return_data(status="OK", code=0, msg=msg))
    return JsonResponse(return_data())


def register(request):
    """ Register Page """
    if request.method == 'POST':
        result = verify_req_params(request, is_register=True)
        if result['code'] != 0:
            return render(
                request, 'fail.html',
                {"type": "注册", "msg": result['msg']}
            )

        users = Account.objects.all().order_by('-id')
        account = users.filter(username=result['msg']['mobile']).first()
        vid = create_vid(users[0].vid)
        # Create User Object If Not Register
        if not account:
            account = Account.objects.create_user(username=result['msg']['mobile'],
                                                  oilcard=result['msg']['cid'],
                                                  vid=vid)
            account.save()
        # Login
        login(request, account)
        return render(request, 'success.html', {"vid": account.vid})
    return render(request, 'register.html')


def site_login(request):
    """ Login Page """
    if request.method == 'POST':
        result = verify_req_params(request, is_register=False)
        if result['code'] != 0:
            return render(
                request, 'fail.html',
                {"type": "注册", "msg": result['msg']}
            )

        account = Account.objects.filter(username=result['msg']['mobile']).first()
        if not account:
            msg = "请先注册!"
            return render(
                request, 'fail.html',
                {"type": "登录", "msg": msg}
            )
        # Login
        login(request, account)
        return redirect('/index/')
    return render(request, 'login.html')


@login_required(login_url='/login/')
def index(request):
    """ Index Page """
    return render(request, 'index.html')


@login_required(login_url='/login/')
def intro(request):
    """ Oil Card Intro Page """
    intros = Intro.objects.filter(is_show=True)
    if not intros:
        return render(request, 'intro.html')
    content = intros.values()
    return render(request, 'intro.html', {"content": content})


@login_required(login_url='/login/')
def question(request):
    """ Talk Online Page """
    qs = Question.objects.filter(is_show=True)
    if not qs:
        return render(request, 'question.html')
    return render(request, 'question.html', {"data": qs.values()})


@login_required(login_url='/login/')
def shop(request):
    """ Shop Page """
    shops = Shop.objects.filter(enable=True)
    return render(request, 'query.html', {"shops": shops})


@login_required(login_url='/login/')
def station(request):
    """ Station Page """
    return render(request, 'list.html')


@login_required(login_url='/login/')
def signin(request):
    """ Signin Page """
    if request.method == 'POST':
        today = date.today()
        search_opts = {
            "user": request.user,
            "year": today.year,
            "month": today.month,
            "day": today.day
        }
        is_exists = SignIn.objects.filter(**search_opts).exists()
        if not is_exists:
            obj = SignIn.objects.create(**search_opts)
            obj.save()
            msg = "签到成功!"
            return JsonResponse(return_data(status="OK", code=0, msg=msg))
        msg = "请勿重复签到!"
        return JsonResponse(return_data(msg=msg))
    days = SignIn.objects.filter(user=request.user).count()
    days = days % 30
    return render(request, 'signin.html', {"days": days})


@login_required(login_url='/login/')
def detail(request):
    """ Detail Page """

    if request.method == 'GET':
        sid = request.GET.get('id', None)
        distance = request.GET.get('distance', None)
        query = Station.objects.filter(id=sid)
        if not query:
            return render(request, 'detail.html', {"msg": "不存在的站点!"})
        gas_price = OilPrice.objects.filter(kind='gas').order_by('id').values()
        diesel_price = OilPrice.objects.filter(kind='diesel').order_by('id').values()
        try:
            return render(request, 'detail.html', {
                "gas_list": gas_price,
                "diesel_list": diesel_price,
                "name": query.first().name,
                "address": query.first().address,
                "distance": distance,
                "is_recharge": query.first().is_recharge
            })
        except Exception as ex:
            print ex.message
    return render(request, 'detail.html', {"msg": "请求错误!"})

@login_required(login_url='/login/')
def map_data(request):
    """ Map Data """
    if request.method == 'GET':
        queries = Station.objects.all().values()
        print "Success"
        return JsonResponse(return_data(status="OK", code=0, msg=list(queries)))
    msg = "请求错误!"
    print "Faield"
    return JsonResponse(return_data(msg=msg))
    

def crt(request):
    base = "91301800016"

    for i in xrange(22001, 42001):
        obj = OilCard.objects.create(card=base+str(i))
        obj.save()

    return JsonResponse(return_data(status="OK", code=0, msg="Insert Success!"))
