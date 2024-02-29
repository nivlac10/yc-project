#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022/12/29 22:07
# @Author : 78957
import importlib
import sys, requests
import json
import time
from datetime import datetime, timedelta, timezone
import hashlib

importlib.reload(sys)
WithdrawUrl = ""
merchantID = 0
secretKey = ""


# 发起提现
def http_post_withdraw_data(user_pay_data, order_number, money, pay_data, vip):
    data = dict()
    data['code'] = 0
    data['is_int'] = 0  # 提现金额是否是int
    data['data'] = dict()
    data['msg'] = 'error'
    data['send_data'] = dict()
    try:
        # if True:
        fee = vip['pay_fee']
        fee_ratio = (100 - float(fee)) / 100
        if fee_ratio < 0:
            fee_ratio = 1
        send_money = int(round(float(money) * fee_ratio, 2)) * 100  # 体现最终金额
        maps = dict()
        maps['amount'] = send_money
        maps['merchantId'] = str(merchantID)
        maps['orderId'] = order_number
        maps['timestamp'] = int(time.time() * 1000)
        maps['notifyUrl'] = pay_data['withdraw_conf_url']
        maps['outType'] = 'IMPS'
        maps['accountNumber'] = user_pay_data['cpf']
        maps['ifsc'] = user_pay_data['pix']
        maps['accountHolder'] = user_pay_data['name']
        print(json.dumps(maps))
        maps['sign'] = pay_signature(maps['amount'], maps['merchantId'], order_number, maps['timestamp'], secretKey)
        content = requests.post(WithdrawUrl, json=maps, verify=False, timeout=10)
        content = json.loads(content.text)
        print(content)
        if str(content['code']) == '100':
            data['code'] = 1
        data['data'] = content
        data['msg'] = content['msg']
        data['send_data'] = maps
    except Exception as e:
        print(e)
        data['msg'] = 'Payment request failed'
    return data


def pay_signature(amount, merchant_id, order_id, timestamp, secret_key):
    data_string = f"{amount}{merchant_id}{order_id}{timestamp}{secret_key}"
    md5_hash = hashlib.md5(data_string.encode()).hexdigest()
    return md5_hash


def get_beijing_time():
    # 时区为东八区，即北京时间
    beijing_timezone = timezone(timedelta(hours=8))

    # 获取当前时间并加上北京时区的偏移量
    beijing_time = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(beijing_timezone)

    return beijing_time.strftime('%Y-%m-%d %H:%M:%S')
