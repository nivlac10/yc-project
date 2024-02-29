# -*- coding: utf-8 - *-
# @Time: 2023/2/17
# @Author:Jack c


import importlib
from app import public_util
from app.user import user
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
import sys

importlib.reload(sys)


@user.route('/admin/email_list_post', methods=['POST'])
@login_required
def email_list_post():
        data = dict()
        data['code'] = 0
        data['data'] = []
        data['count'] = 0
        try:
            page = request.values.get('page', '1')
            limit = int(request.values.get('limit', '20'))
            stime = request.values.get('stime')
            etime = request.values.get('etime')
            uid = request.values.get('uid','')
            receive_status = request.values.get("receive_status")
            offset = (int(page) - 1) * limit
            sql = "select a.*,b.nickname from san_user_message as a left join san_users as b " \
                  "on a.uid=b.uid "
            sql2 = "select count(*) `count` from san_user_message as a left join san_users" \
                   " as b on a.uid=b.uid "
            sql_list = []
            if uid:
                sql_list.append(" (a.uid like '%%%s%%' or b.nickname like '%%%s%%' )"%(uid,uid))
            if receive_status:
                sql_list.append(" receive_status= '%s'"%receive_status)
            if stime:
                sql_list.append(" a.add_time >= '%s' "%stime)
            if etime:
                sql_list.append(" a.add_time <= '%s' "%etime)
            sql_str=public_util.data_list_to_str(sql_list)
            sql+=sql_str
            sql2+=sql_str
            sql += " order by a.id desc limit %s, %s "%(offset,limit)
            mysql = Mysql()
            cont = mysql.getOne(sql2, None)
            res = mysql.getAll(sql, None)
            mysql.dispose()
            if res:
                status_list = ['无', '未领取', '已领取']
                for d in res:
                    d['add_time'] = str(d['add_time'])
                    d['receive_status'] = status_list[d['receive_status']]
                data['data'] = res
                data['count'] = int(cont['count'])
            data['code'] = 1
        except Exception as e:
            print(e)
        return jsonify(data)
