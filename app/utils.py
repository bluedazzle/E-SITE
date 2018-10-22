# -*- coding: utf-8 -*-
import urllib
import json
import random
import re
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from .models import OilCard, Account
from time import time


class SMS(object):
    def __init__(self, mobile):
        self._url = 'https://sms.yunpian.com/v2/sms/single_send.json'
        self._apikey = '8d0642003dc438871ffb484ea978bcb7'
        self._mobile = mobile
        self._tplid = "2042342"

    @staticmethod
    def generate_params():
        timeout = 180
        code = random.randint(1000, 9999)
        return code, timeout

    def send(self):
        params = self.generate_params()

        client = YunpianClient(apikey=self._apikey)
        param = {
            YC.MOBILE: self._mobile,
            YC.TPL_ID: self._tplid,
            YC.TPL_VALUE: urllib.urlencode({"#code#": str(params[0])})
        }
        data = client.sms().tpl_single_send(param)
        print data.code()
        if data.code() == 0:
            return params
        return None


def serializer_data(request):
    return json.loads(request.body.encode("UTF8"))


def create_vid(prev_vid=None):
    new_vid = "00000001"
    if not prev_vid:
        return new_vid
    end_zero_index = prev_vid.rfind("0")
    number = int(prev_vid[end_zero_index+1:])+1
    new_vid = prev_vid[:end_zero_index+1] + str(number)
    return new_vid


def return_data(status="ERROR", code=1, msg=None, url=None):
    data = {
        "status": status,
        "code": code,
        "msg": msg,
    }
    if url:
        data["url"] = url
    return data


def verify_mobile(mobile):
    pat = re.compile('^(13\d|14[5|7]|15\d|166|17\d|18\d)\d{8}$')
    try:
        res = re.search(pat, mobile)
        if not res:
            return False
        return True
    except TypeError:
        return False


def verify_req_params(req, is_register=False):
    mobile = req.POST.get('mobile', None)
    code = req.POST.get('code', None)
    cid = req.POST.get('cid', None)

    obj = OilCard.objects.filter(card=cid).first()

    if is_register:
        if not cid or not obj:
            msg = "请正确填写油卡号!"
            return return_data(msg=msg)
        is_bind = Account.objects.filter(oilcard=obj).first()
        if is_bind and is_bind.username != mobile:
            msg = "油卡号已绑定!"
            return return_data(msg=msg)

    res = verify_mobile(mobile)
    if not res:
        msg = "请正确填写手机号!"
        return return_data(msg=msg)
    try:
        param = req.session[mobile]
        if time() > param['expired_at']:
            raise KeyError
    except KeyError:
        msg = "验证码过期!"
        return return_data(msg=msg)
    if not code or int(code) != param['code']:
        msg = "验证码错误!"
        return return_data(msg=msg)
    # Verify Success
    msg = {
        "mobile": mobile,
        "cid": obj
    }
    return return_data(status="OK", code=0, msg=msg)
