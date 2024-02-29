#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-03-04
import codecs
import importlib
import json
import sys

from flask import request, jsonify
from app import public_util
from app.util import login_required
from SqlConntion.MySqlConn import Mysql
from . import activity

importlib.reload(sys)


# 转轮赠送金额日志列表
@activity.route('/admin/roller_money_log_post', methods=['post'])
@login_required
def roller_money_log_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['count_money'] = 0
    try:
        uid = request.values.get('uid')
        cid = request.values.get('cid')
        order = request.values.get('order','a.add_time')
        order_type = request.values.get('order_type','desc')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        page = request.values.get('page', '1')
        limit = int(request.values.get('limit', '20'))
        offset = (int(page) - 1) * limit
        sql_list = []
        if uid:
            sql_list.append(" (a.uid like '%%%s%%' or b.nickname like '%%%s%%') " % (uid,uid))
        if cid:
            sql_list.append(" a.cid = '%s' " % (cid))
        if stime:
            sql_list.append(" a.add_time>='%s' " % (stime))
        if etime:
            etime = etime + " 23:59:59"
            sql_list.append(" a.add_time<='%s' " % (etime))
        sql_str = public_util.data_list_to_str(sql_list)
        sql=''
        sql2=''
        if order=='a.add_time':
            sql = "select a.*,b.nickname,c.username,(select count(*) from san_roller_money_log where uid=a.uid) user_sum " \
                  " from san_roller_money_log a left join san_users b on a.uid=b.uid left join san_agent c on a.cid=c.cid %s order by %s %s limit %s, %s" % (
                  sql_str, order, order_type, offset, limit)
            sql2 = "select count(*) con,sum(ifnull(a.money,0)) money from san_roller_money_log a left join san_users b on a.uid=b.uid %s " % sql_str
        else:
           order = 'user_sum' if order=='user_sum' else 'sum(a.money)'
           sql = "select a.uid,a.cid,sum(a.money) money,a.add_time,b.nickname,c.username,(select count(*) from san_roller_money_log" \
                 " where uid=a.uid) user_sum  from san_roller_money_log a left join san_users b on a.uid=b.uid left join san_agent c" \
                 " on a.cid=c.cid  %s  group by a.uid order by %s %s limit %s, %s" % (
                     sql_str, order, order_type, offset, limit)
           sql2 = "select count(*) con,sum(money) money from (select sum(ifnull(a.money,0)) money from san_roller_money_log a left join san_users b on a.uid=b.uid %s GROUP BY a.uid) roller_money  " % sql_str

        mysql = Mysql()
        res = mysql.getAll(sql, None)
        con = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for item in res:
                item['add_time'] = str(item['add_time'])
            data['count'] = con['con']
            data['count_money'] = con['money']
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
