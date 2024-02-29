import codecs
import hashlib

from flask import jsonify, request, abort
from functools import wraps

import time

from SqlConntion import ConnConfig
from app import redis, constant
from app.my_session import MySession
from SqlConntion.MySqlConn import Mysql

# api code 说明
"""
0   请求失败
1   请求成功
2   登陆认证不通过
3   清空账号
4   接口不存在
5   权限不足
6   密码错误
6   密码错误
6   密码错误
6   密码错误

"""


# 登陆验证
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = dict()
        # if request.host not in HOST_ARR:
        #     return abort(404)
        db_index = request.headers.get('DBIndex')
        if db_index:
            constant.DBINDEX = int(db_index)
        token = request.headers.get('Authorization')
        if token is None or not MySession.reactive(token):
            return abort(401)  # token过期直接强制退出页面
        admin_uid = redis.hget(token, 'n')
        # power = user_power(admin_uid)
        # if power['state'] != 1:
        #     data['code'] = power['code']
        #     return to_json(data)
        return func(*args, **kwargs)

    return wrapper


# 用户权限认证
def user_power(admin_uid):
    data = dict()
    data['state'] = 0
    data['code'] = 0
    path = request.path
    if int(admin_uid) != 1 and int(admin_uid) != 21:
        is_contain = get_interface_is_contain(path)
        if is_contain is None:
            data['code'] = 4
            return data
        ispower = get_user_power(path, admin_uid)
        if ispower is None:
            data['code'] = 5
            return data
    data['state'] = 1
    return data


# 查询接口是否存在
def get_interface_is_contain(interface_url):
    sql = "select * FROM san_power_interface WHERE interface_url = '%s'" % interface_url
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 查询接口是否有权限
def get_user_power(interface_url, uid):
    sql = "select * from san_administrator where find_in_set((select jid from san_power_interface WHERE " \
          "interface_url='%s'),interface_str) and id='%s'" % (
              interface_url, uid)
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 转化成json格式
def to_json(response):
    response_json = jsonify(response)
    response_json.headers['Access-Control-Allow-Origin'] = '*'
    return response_json


def days_int(day):
    dt = int(time.mktime(time.strptime(day, '%Y-%m-%d %H:%M:%S')))
    return dt


# md5加密
def md5(string):
    string = str(string)
    if isinstance(string, str):
        m = hashlib.md5()
        string = codecs.encode(string)
        m.update(string)
        return m.hexdigest()
    else:
        return ''
