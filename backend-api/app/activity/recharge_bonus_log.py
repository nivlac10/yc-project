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


# 获取充值奖金列表
@activity.route('/admin/recharge_bonus_log_post', methods=['post'])
@login_required
def recharge_bonus_log_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['count_money'] = 0
    data['count_recharge_money'] = 0
    try:
        uid = request.values.get('uid')
        cid = request.values.get('cid')
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
        sql = "select a.*,b.nickname,c.username from san_recharge_bonus_log a left join san_users b on a.uid=b.uid  left join san_agent c on c.cid=a.cid %s order by a.id desc limit %s, %s"%(sql_str,offset, limit)
        sql2 = "select count(*) count,sum(a.money) money,sum(a.recharge_money) recharge_money from san_recharge_bonus_log a left join san_users b on a.uid=b.uid %s "%sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        con = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for item in res:
                item['add_time'] = str(item['add_time'])
            data['count'] = con['count']
            data['count_money'] = con['money']
            data['count_recharge_money'] = con['recharge_money']
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
