#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022/8/1 11:37
# @Author : 78957
import importlib

from . import admin
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import  public_util
import  pyotp
import qrcode, base64
from io import BytesIO
import sys
importlib.reload(sys)


# 获取代理列表数据
@admin.route('/admin/proxy_list_post', methods=['post'])
@login_required
def proxy_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql = "select * from san_proxy_list order by aid desc limit %d, %d" % (offset, limit)
        sql2 = "select count(*) con from san_proxy_list"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                d['login_time'] = str(d['login_time']) if d['login_time'] else ''
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 添加代理处理方法
@admin.route('/admin/add_proxy_post', methods=['post'])
@login_required
def add_proxy_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        username = request.values.get('username')
        nickname = request.values.get('nickname')
        proxy = get_proxy_username(username)
        if proxy:
            data['msg'] = '账号已添加'
            return jsonify(data)
        res = add_proxy_func(username, nickname)
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 更新代理状态
@admin.route('/admin/update_proxy_list_post', methods=['post'])
@login_required
def update_proxy_list_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        aid = request.values.get('aid')
        status = request.values.get('status')
        if str(status) not in ['0', '1']:
            data['msg'] = '参数错误'
            return jsonify(data)
        proxy = get_proxy_detail(aid)
        if proxy is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        sql = "update san_proxy_list set status = %s where aid = %s"
        mysql = Mysql()
        res = mysql.update(sql, [status, aid])
        mysql.dispose()
        if res >= 0:
            data['msg'] = '操作成功'
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除代理
@admin.route('/admin/delete_proxy_post', methods=['post'])
@login_required
def delete_proxy_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        aid = request.values.get('aid')
        proxy = get_proxy_detail(aid)
        if proxy is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        sql = "delete from san_proxy_list where aid = %s"
        mysql = Mysql()
        res = mysql.delete(sql, [aid])
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)



# 更新代理信息
@admin.route('/admin/proxy_detail_post', methods=['post'])
@login_required
def proxy_detail_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作成功'
    try:
        nickname = request.values.get('nickname')
        aid = request.values.get('aid')
        proxy = get_proxy_detail(aid)
        if proxy is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        sql = "update san_proxy_list set nickname = %s where aid = %s"
        mysql = Mysql()
        res = mysql.update(sql, [nickname, aid])
        mysql.dispose()
        if res >= 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取二维码
@admin.route('/admin/proxy_user_code_img', methods=['post'])
@login_required
def proxy_user_code_img():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '获取失败'
    data['data'] = ''
    try:
        uid = request.values.get('uid')
        user = get_proxy_detail(uid)
        if user is None:
            data['msg'] = '代理人不存在'
            return jsonify(data)
        url = 'otpauth://totp/%s?secret=%s' % (user['username'], user['user_key'])
        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=15, border=1, )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        f = BytesIO()
        img.save(f, "png")
        data['data'] = u"data:image/png;base64," + base64.b64encode(f.getvalue()).decode('ascii')
        data['code'] = 1
        data['status'] = 1
        data['msg'] = '获取成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取渠道详细信息
def get_proxy_detail(aid):
    sql = "select * from san_proxy_list where aid = '%s'" % aid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 添加代理操作
def add_proxy_func(username, nickname):
    user_key = pyotp.random_base32(32)
    p_str = add_storage_pass(str(username), '123456')
    sql = "insert into san_proxy_list(username, nickname, password, user_key, add_time) values ('%s', '%s', '%s', " \
          "'%s', now())" % (username, nickname, p_str, user_key)
    mysql = Mysql()
    res = mysql.insertOne(sql, None)
    mysql.dispose()
    return res


# 生成储存的用户密码
def add_storage_pass(username, password):
    md_str = public_util.md5(str(username)) + public_util.md5(password)
    s_str = ''.join(sorted(public_util.md5(''.join(sorted(md_str)))))
    return s_str


# 查询代理账号是否已添加
def get_proxy_username(username):
    sql = "select * from san_proxy_list where username = '%s'" % username
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res
