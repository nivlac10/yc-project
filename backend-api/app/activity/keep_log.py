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


# 每日活跃记录
@activity.route('/admin/user_keep_log_post', methods=['POST'])
@login_required
def user_keep_log_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        page = request.values.get('page', '1')
        limit = int(request.values.get('limit', '20'))
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        cid = request.values.get('cid')
        offset = (int(page) - 1) * limit
        sql_list = []
        if stime:
            sql_list.append("a.unlock_time >= '%s' " % stime)
        if etime:
            sql_list.append("a.unlock_time <= '%s' " % etime)
        if cid:
            sql_list.append("a.cid = '%s' " % cid)

        sql_str = public_util.data_list_to_str(sql_list)
        sql = "select a.*,b.username from san_user_week_month_keep a left join san_agent b on a.cid=b.cid %s " \
              "order by day desc limit %s,%s " % (sql_str, offset, limit)
        sql_con = "select count(*) con,sum(week_number) week_number,sum(month_number) month_number from san_user_week_month_keep a   %s " % sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        res_con = mysql.getOne(sql_con, None)
        mysql.dispose()
        if res:
            for item in res:
                item['day'] = str(item['day'])
            data['data'] = res
            res_con['week_number'] = str(res_con['week_number'])
            res_con['month_number'] = str(res_con['month_number'])
            data['count'] = res_con['con']
            data['total'] = res_con
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


