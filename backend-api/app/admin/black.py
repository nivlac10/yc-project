#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-06-05
import importlib

from . import admin
from flask import request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from ..user import user_info
import sys

importlib.reload(sys)



# 黑名单用户列表数据
@admin.route('/admin/black_list_post', methods=['post'])
@login_required
def black_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        username = request.values.get('username')
        c_num = (int(page) - 1) * limit
        sql = "select a.*, b.nickname FROM san_user_black_log a left join san_users b on b.uid = a.uid WHERE a.status=0"
        sql2 = "select count(*) con FROM san_user_black_log a left join san_users b on b.uid = a.uid WHERE a.status=0"
        if username:
            sql += " and (a.uid like '%%%s%%' or locate('%s', b.nickname)>0)" % (username, username)
            sql2 += " and (a.uid like '%%%s%%' or locate('%s', b.nickname)>0)" % (username, username)
        sql += " order by id desc limit %d, %d" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
            data['data'] = res
            data['count'] = int(cont['con'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 获取黑名单ip列表数据
@admin.route('/admin/black_ip_list_post', methods=['post'])
@login_required
def black_ip_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        ip = request.values.get('ip')
        c_num = (int(page) - 1) * limit
        sql = "select id,ip, add_time, info FROM san_user_black_log WHERE status=1"
        sql2 = "select count(*) con FROM san_user_black_log WHERE status=1"
        if ip:
            sql += " and locate('%s', ip)" % ip
            sql2 += " and locate('%s', ip)" % ip
        sql += " order by id desc limit %d, %d" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
            data['data'] = res
            data['count'] = int(cont['con'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 获取黑名单卡号数据
@admin.route('/admin/black_account_list_post', methods=['post'])
@login_required
def black_account_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        account = request.values.get('account')
        c_num = (int(page) - 1) * limit
        sql = "select id,account, add_time, info FROM san_user_black_log WHERE status=2"
        sql2 = "select count(*) con FROM san_user_black_log WHERE status=2"
        if account:
            sql += " and locate('%s', account)" % account
            sql2 += " and locate('%s', account)" % account
        sql += " order by id desc limit %d, %d" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
            data['data'] = res
            data['count'] = int(cont['con'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 添加黑名单处理
@admin.route('/admin/add_black_post', methods=['post'])
@login_required
def add_black_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        uid = request.values.get('uid', '')
        ip = request.values.get('ip', '').strip()
        account = request.values.get('account', '')
        info = request.values.get('info', '')
        type = request.values.get('type', '')
        status = request.values.get('status', '')
        if str(status) not in ['0', '1', '2']:
            data['msg'] = '参数状态异常'
            return jsonify(data)
        if uid and status == '0':
            user = user_info.get_user_info(uid)
            if user is None:
                data['msg'] = '用户不存在'
                return jsonify(data)
            if user['user_type'] == 0 or user['user_gm'] == 1:
                data['msg'] = '用户身份错误'
                return jsonify(data)
            now_user = get_black_uid(uid,type)
            if now_user:
                data['msg'] = '当前用户已添加'
                return jsonify(data)
            res = add_black_funf(status,type, info, uid)
            if res > 0:
                data['code'] = 1
                data['status'] = 1
                data['msg'] = '操作成功'
                return jsonify(data)
        if ip and status == '1':
            ip_data = get_black_ip(ip)
            if ip_data:
                data['msg'] = '当前ip已添加黑名单'
                return jsonify(data)
            res = add_black_funf(status,0, info, ip)
            if res > 0:
                data['code'] = 1
                data['status'] = 1
                data['msg'] = '操- 作成功'
                return jsonify(data)
        if account and status == '2':
            account_data = get_black_account(account)
            if account_data:
                data['msg'] = '当前账号已添加黑名单'
                return jsonify(data)
            res = add_black_funf(status,0, info, account)
            if res > 0:
                data['code'] = 1
                data['status'] = 1
                data['msg'] = '操作成功'
                return jsonify(data)
        data['msg'] = '参数填写错误'
    except Exception as e:
        print(e)
    return jsonify(data)


# 异常列表表数据
@admin.route('/admin/unusual_user_log_post', methods=['post'])
@login_required
def unusual_user_log_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        uid = request.values.get('uid')
        c_num = (int(page) - 1) * limit
        sql = "select a.*, b.nickname FROM san_user_unusual_log a left join san_users b on b.uid = a.uid "
        sql2 = "select count(*) con FROM san_user_unusual_log as a  left join san_users b on b.uid = a.uid "
        sql_list = []
        if stime:
            sql_list.append(" a.add_time >= '%s'" % stime)
        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append(" a.add_time <= '%s'" % e_str)
        if uid:
            sql_list.append(" (a.uid  like '%%%s%%' or b.nickname like '%%%s%%') " % (uid, uid))
        if len(sql_list) > 0:
            if len(sql_list) > 1:
                sql_str = "where " + "and".join(sql_list)
            else:
                sql_str = "where " + sql_list[0]
            sql += sql_str
            sql2 += sql_str
        sql += " order by id desc limit %d, %d" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
            data['data'] = res
            data['count'] = int(cont['con'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除卡号黑名单
@admin.route('/admin/delete_unusual_user_post', methods=['post'])
@login_required
def delete_unusual_user_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        id = request.values.get('id')
        sql = " delete from san_user_black_log where id = %s "%id
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res:
            data['status'] = 1
            data['code'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)

# 获取用户黑名单信息
def get_black_uid(uid,type):
    sql = "select * from san_user_black_log where uid = '%s' and type='%s'" % (uid,type)
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 获取黑名单账号信息
def get_black_account(account):
    sql = "select * from san_user_black_log where account = '%s'" % account
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 获取黑名单ip信息
def get_black_ip(ip):
    sql = "select * from san_user_black_log where ip = '%s'" % ip
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 新增黑名单
def add_black_funf(status,type, info, data):
    key_list = ['uid', 'ip', 'account']
    sql = "insert into san_user_black_log (%s, status,type, info, add_time) value ('%s','%s', '%s', '%s', now())" % \
          (key_list[int(status)], data, status,type, info)
    mysql = Mysql()
    res = mysql.insertOne(sql, None)
    mysql.dispose()
    return res
