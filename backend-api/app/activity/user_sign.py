import sys

import importlib
from . import activity
from flask import request,jsonify
from app import public_util
from app.util import login_required
from SqlConntion.MySqlConn import Mysql

importlib.reload(sys)


# 用户签到列表
@activity.route('/admin/user_sign_list_post', methods=['POST'])
@login_required
def user_sign_list_post():
    data = dict()
    data['code'] = 0
    data['count'] = 0
    data['count_money'] = 0
    data['data'] = []
    try:
        uid = request.values.get('uid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        continue_day = request.values.get('continue_day')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql_list = []
        if uid:
            sql_list.append(" (users.uid like '%%%s%%' or users.nickname like '%%%s%%') "%(uid,uid))
        if continue_day:
            sql_list.append(" user_sign.continue_day = '%s' "%continue_day)
        if stime:
            sql_list.append(" user_sign.day >= '%s' "%stime)
        if etime:
            sql_list.append(" user_sign.day <= '%s' "%etime)
        sql_str=public_util.data_list_to_str(sql_list)

        sql="select user_sign.*,users.nickname from san_user_sign_log user_sign " \
            "left join san_users users on user_sign.uid=users.uid %s order by  id desc " \
            " limit %d,%d" %(sql_str,offset,limit)

        sql_con = "select count(*) con,sum(user_sign.money) money from san_user_sign_log user_sign " \
                  "left join san_users users on user_sign.uid=users.uid %s "%sql_str
        mysql = Mysql()
        res = mysql.getAll(sql,None)
        res_con = mysql.getOne(sql_con,None)
        mysql.dispose()
        if res:
            for sign in res:
                sign['add_time'] = str(sign['add_time'])
                sign['day'] = str(sign['day'])
            data['count'] = res_con["con"]
            data['count_money'] = res_con["money"]
            data['data'] = res
        data['code'] =1
    except Exception as e:
        print(e)
    return jsonify(data)