#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-04-22
import importlib

from app.user import user
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import common, public_util
import sys

importlib.reload(sys)


# 获取用户金额类型
@user.route('/admin/money_type_list_post', methods=['post'])
@login_required
def money_type_list_post():
    data = dict()
    data['code']=1
    conf = common.MONEY_TYPE_CONF
    conf_list = []
    for d in conf:
        conf_list.append(conf[d])
    data['data'] = conf_list
    return jsonify(data)

# 获取用户金额变动记录数据
@user.route('/admin/money_log_list_post', methods=['post'])
@login_required
def money_log_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        uid = request.values.get('uid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        money_type = request.values.get('money_type')
        limit = int(request.values.get('limit', '20'))
        log_type = request.values.get('log_type')
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql_list = []
        if uid:
            sql_list.append(" (a.uid like '%%%s%%' or b.nickname like '%%%s%%')" % (uid, uid))

        if log_type:
            sql_list.append(" a.log_type = '%s'" % log_type)

        if money_type:
            sql_list.append(" a.money_type = '%s'" % money_type)

        if stime:
            sql_list.append(" a.add_time >= '%s'" % stime)
        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append(" a.add_time <= '%s'" % e_str)
        sql_str = public_util.data_list_to_str(sql_list)
        mysql = Mysql()
        sql = "select a.*, b.nickname from san_user_money_log a left join san_users b on b.uid = a.uid" \
              " %s order by a.id desc limit %d, %d" % (sql_str,offset, limit)
        sql2 = "select count(*) con from san_user_money_log a left join san_users b on b.uid = a.uid %s "%sql_str
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                d['log_type'] = "余额" if d['log_type'] == 0 else "佣金"
                d['money_type_str'] = common.MONEY_TYPE_CONF[str(d['money_type'])]['name'] if common.MONEY_TYPE_CONF[
                    str(d['money_type'])] else '未知'
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print (e)
    return jsonify(data)
