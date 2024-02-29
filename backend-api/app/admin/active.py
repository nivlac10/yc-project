#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-06-08
import importlib

from . import admin
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util
import sys

importlib.reload(sys)




# 获取玩家活跃数据
@admin.route('/admin/user_active_post', methods=['post'])
@login_required
def user_active_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        cid = request.values.get('cid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)

        sql_list = []
        if cid:
            sql_list.append(" a.cid = '%s'" % cid)
        if stime:
            sql_list.append(" a.day >= '%s'" % stime)
        if etime:
            sql_list.append("  a.day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)
        sql = "select a.day, ifnull(sum(a.d1),0) d1, ifnull(sum(a.d2),0) d2, ifnull(sum(a.d3),0) d3, ifnull(sum(a.d4),0) d4, " \
              "ifnull(sum(a.d5),0) d5, ifnull(sum(a.d6),0) d6, ifnull(sum(a.d7),0) d7, if(b.user_num, b.user_num, 0) user_num," \
              " if(b.phone_num, b.phone_num, 0) phone_num from san_user_active_data a left join (san_day_money_total) b" \
              " on b.day = a.day %s group by a.day order by a.day desc limit %d, %d" % (sql_str,c_num, limit)

        sql2 = "select count(*) con from (select day from san_user_active_data as a  %s  " \
               "group by day order by day desc limit 100000) aa"%sql_str

        sql3 = "select day, cid, sum(phone_num + face_num + email_num) user_num, sum(phone_num) phone_num from " \
               "san_day_money_total as a  %s  group by day"%sql_str

        sql = sql.replace("san_day_money_total", sql3)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['phone_num'] = str(d['phone_num']) if d['phone_num'] else 0
                d['user_num'] = str(d['user_num']) if ['user_num'] else 0
                d['day'] = str(d['day'])
                d['d1'] = str(d['d1']) if d['d1'] else 0
                d['d2'] = str(d['d2']) if d['d2'] else 0
                d['d3'] = str(d['d3']) if d['d3'] else 0
                d['d4'] = str(d['d4']) if d['d4'] else 0
                d['d5'] = str(d['d5']) if d['d5'] else 0
                d['d6'] = str(d['d6']) if d['d6'] else 0
                d['d7'] = str(d['d7']) if d['d7'] else 0
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)




# 获取用户活跃数据
@admin.route('/admin/user_keep_post', methods=['post'])
@login_required
def user_keep_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        cid = request.values.get('cid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql_sum = get_days()
        sql_list = []
        if cid:
            sql_list.append(" cid = '%s'" % cid)
        if stime:
            sql_list.append(" day >= '%s'" % stime)
        if etime:
            sql_list.append(" day <= '%s'" % etime)
        sql_str=public_util.data_list_to_str(sql_list)


        sql = "select day, cid,  " + sql_sum + " from san_user_keep_data %s  group by day order by day " \
                                               "desc limit %d, %d" % (sql_str,c_num, limit)
        sql2 = "select count(*) con from (select day, sum(d1) d1 from san_user_keep_data %s " \
               "group by day order by day desc limit 100000) aa "%sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['day'] = str(d['day'])
                for k in range(1, 31):
                    d['d' + str(k)] = str(d['d' + str(k)]) if d['d' + str(k)] else 0
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


def get_days():
    a = ''
    for d in range(1, 31):
        a += 'sum(d%s) d%s,' % (str(d), str(d))
    return a[:-1]


# 获取所有的apk
def get_all_agent():
    sql = "select cid, username from san_agent where status = 1"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res
