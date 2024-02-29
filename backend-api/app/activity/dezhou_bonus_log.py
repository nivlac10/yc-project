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
@activity.route('/admin/dezhou_bonus_log_post', methods=['post'])
@login_required
def dezhou_bonus_log_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['count_money'] = 0
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
            sql_list.append(" (a.uid like '%%%s%%' or u.nickname like '%%%s%%') " % (uid , uid))
        if cid:
            sql_list.append(" a.cid = '%s' " % (cid))
        if stime:
            sql_list.append(" a.add_time>='%s' " % (stime))
        if etime:
            etime = etime + " 23:59:59"
            sql_list.append(" a.add_time<='%s' " % (etime))
        sql_str = public_util.data_list_to_str(sql_list)
        # san_user_download_bonus_log | san_user_bet_dezhou_bonus_log
        sql = "select a.id,a.cid,a.uid,a.money,a.add_time,u.nickname,g.username from san_user_download_bonus_log a " \
              "left join  san_users u on a.uid=u.uid " \
              "left join  san_agent g on g.cid=a.cid %s order by a.add_time desc limit %s, %s" % (sql_str,  offset, limit)
        sql2 = "select count(*) con,sum(a.money) money from san_user_download_bonus_log a left join  san_users u on a.uid=u.uid %s" % sql_str
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
