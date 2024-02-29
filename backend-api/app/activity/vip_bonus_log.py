# -*- coding: utf-8 - *-
# @Time: 2023/2/16
# @Author:Jack c

# ================================ vip等级列表========================
import time

from . import activity
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util, util
import sys

import importlib

importlib.reload(sys)


# VIP等级打码奖励领取记录列表
@activity.route('/admin/vip_bonus_log_list', methods=['POST'])
@login_required
def vip_bonus_log_list():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total_money'] = 0
    try:
        page = request.values.get('page', '1')
        limit = int(request.values.get('limit', '20'))
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        bonus_type = request.values.get('bonus_type')
        status = request.values.get('status')
        get_type = request.values.get('get_type')
        uid = request.values.get('uid')
        cid = request.values.get('cid')
        offset = (int(page) - 1) * limit
        sql_list = []
        if stime:
            sql_list.append("a.unlock_time >= '%s' " % stime)
        if etime:
            sql_list.append("a.unlock_time <= '%s' " % etime)
        if bonus_type:
            sql_list.append("a.bonus_type = '%s' " % bonus_type)
        if get_type:
            sql_list.append("a.get_type = '%s' " % get_type)
        if status:
            sql_list.append("a.status = '%s' " % status)
        if uid:
            sql_list.append("(b.nickname like '%%%s%%'  or a.uid like '%%%s%%') " % (uid, uid))
        if cid:
            sql_list.append("a.cid = '%s' " % cid)
        sql_str = public_util.data_list_to_str(sql_list)
        sql = "select a.*,b.nickname from san_user_vip_bonus_log a " \
              "inner join san_users b on a.uid=b.uid %s " \
              "order by get_time desc limit %s,%s " % (sql_str, offset, limit)
        sql_con = "select count(*) con,sum(ifnull(bonus,0)) money from san_user_vip_bonus_log a " \
                  "inner join san_users b on a.uid=b.uid  %s " % sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        res_con = mysql.getOne(sql_con, None)
        mysql.dispose()
        current_time = time.time()
        today = str(public_util.get_today_y_m_d())
        if res:
            for item in res:
                item['day'] = str(item['day'])
                item['get_time'] = str(item['get_time'])
                item['unlock_time'] = str(item['unlock_time'])
                item['status'] = item['status']
                unlock_time = util.days_int(str(item['unlock_time']))
                if current_time >= util.days_int(item['day'] + " 23:59:59") or today == item['day']:
                    if item['status'] != 1 and str(item['day']) != str(today):
                        end_time = int(str(unlock_time)) + 86400
                        if end_time < int(current_time):
                            item['status'] = 2
                elif str(item['day']) == str(today) and item['status'] != 1:
                    unlock_time = util.days_int(str(item['unlock_time']))
                    if unlock_time > int(current_time):
                        item['status'] = 3
            data['data'] = res
            data['count'] = res_con['con']
            data['total_money'] = res_con['money']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# VIP等级打码奖励分割领取记录列表
@activity.route('/admin/vip_splic_bonus_log_list', methods=['POST'])
@login_required
def vip_splic_bonus_log_list():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total_money'] = 0
    try:
        page = request.values.get('page', '1')
        limit = int(request.values.get('limit', '20'))
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        uid = request.values.get('uid')
        cid = request.values.get('cid')
        get_type = request.values.get('get_type')
        offset = (int(page) - 1) * limit
        sql_list = []
        if stime:
            sql_list.append("a.unlock_time >= '%s' " % stime)
        if etime:
            sql_list.append("a.unlock_time <= '%s' " % etime)
        if uid:
            sql_list.append("(b.nickname like '%%%s%%'  or a.uid like '%%%s%%') " % (uid, uid))
        if cid:
            sql_list.append("a.cid = '%s' " % cid)
        if get_type:
            sql_list.append("a.get_type = '%s' " % get_type)
        sql_str = public_util.data_list_to_str(sql_list)
        sql = "select a.*,b.nickname,c.username from san_user_vip_split_bonus_log a " \
              "inner join san_users b on a.uid=b.uid " \
              "inner join san_agent c on a.cid=c.cid %s order by unlock_time desc limit %s,%s " % (
              sql_str, offset, limit)
        sql_con = "select count(*) con,sum(ifnull(bonus,0)) money from san_user_vip_split_bonus_log a " \
                  "inner join san_users b on a.uid=b.uid %s " % sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        res_con = mysql.getOne(sql_con, None)
        mysql.dispose()
        if res:
            for item in res:
                item['day'] = str(item['day'])
                item['add_time'] = str(item['add_time'])
                item['unlock_time'] = str(item['unlock_time'])
            data['data'] = res
            data['count'] = res_con['con']
            data['total_money'] = res_con['money']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
