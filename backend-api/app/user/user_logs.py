# coding=utf-8

from app.user import user
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util
import sys

import importlib

importlib.reload(sys)




# 获取管理员登陆数据
@user.route('/admin/login_log_post', methods=['post'])
@login_required
def login_log_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        uname = request.values.get('uname')
        offset = (int(page) - 1) * limit
        sql_list = []
        if uname:
            sql_list.append(" username = '%s'" % uname)

        if stime:
            sql_list.append(" time >= '%s'" % stime)
        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append(" time <= '%s'" % e_str)
        sql_str = public_util.data_list_to_str(sql_list)
        sql = "select * FROM san_log_login %s  order by id desc limit %d, %d"% (sql_str,offset, limit)
        sql2 = "select count(*) con FROM san_log_login %s"%(sql_str)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['time'] = str(d['time'])
                d['log_str'] = d['country'] + d['province'] + d['city']
            data['data'] = res
            data['count'] = int(cont['con'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 获取用户登陆记录
@user.route('/admin/user_login_log_post', methods=['post'])
@login_required
def user_login_log_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        cid = request.values.get('cid')
        offset = (int(page) - 1) * limit
        sql_list = []
        if cid:
            sql_list.append(" cid = '%s'" % cid)
        if stime:
            sql_list.append("  login_time >= '%s'" % stime)

        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append(" login_time <= '%s'" % e_str)
        sql_str = public_util.data_list_to_str(sql_list)
        mysql = Mysql()
        sql = "select * from san_user_login %s order by login_time desc limit %d, %d" % (sql_str,offset, limit)
        sql2 = "select count(*) con from san_user_login %s "%sql_str
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['login_time'] = str(d['login_time'])
            data['data'] = res
            data['count'] = int(cont['con'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


