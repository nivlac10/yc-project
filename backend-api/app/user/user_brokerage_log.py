#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-04-22
import importlib
import json

from app.user import user
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import common, public_util
import sys

importlib.reload(sys)



# 获取用户打码返佣记录数据
@user.route('/admin/brokerage_log_list_post', methods=['post'])
@login_required
def brokerage_log_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        game_type_list = common.HOME_GAME_TYPE
        game_type_conf = dict()
        for t in game_type_list:
            game_type_conf[str(t['game_type_id'])] = t['game_type_name']
        uid = request.values.get('uid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        lv_num = request.values.get('lv_num')
        limit = int(request.values.get('limit', '20'))
        status = request.values.get('status','')
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql_list = []
        if uid:
            sql_list.append(" (a.uid = '%s' or locate('%s', b.nickname) > 0)" % (uid, uid))
        if lv_num:
            sql_list.append(" a.lv_num = '%s'" % lv_num)
        if status != "":
            sql_list.append(" a.status = '%s'" % status)
        if stime:
            sql_list.append(" a.add_time >= '%s'" % stime)
        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append(" a.add_time <= '%s'" % e_str)
        sql_str = public_util.data_list_to_str(sql_list)
        sql = "select a.*, b.nickname from san_user_day_brokerage a left join san_users b on b.uid = a.uid" \
              " %s order by a.id desc limit %d, %d" % (sql_str,offset, limit)
        sql2 = "select count(*) con from san_user_day_brokerage a  %s"%sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                d['update_time'] = str(d['update_time'])
                d['status'] = "已结算" if d['status'] == 1 else "未结算"
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
