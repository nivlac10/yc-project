#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022/6/6 16:51
# @Author : 78957
import importlib

from . import admin
from flask import render_template, request, jsonify, make_response
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import util
import time
import sys

importlib.reload(sys)



# 获取事件上报记录
@admin.route('/admin/event_report_list_post', methods=['post'])
@login_required
def event_report_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        cid = request.values.get('cid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        aaid = request.values.get('aaid')
        event_name = request.values.get('event_name')
        c_num = (int(page) - 1) * limit
        sql = "select a.*, b.username from san_app_event a left join san_agent b on a.cid = b.cid "
        sql2 = "select count(*) con from san_app_event as a "
        sql_list = []
        if cid:
            sql_list.append("  a.cid = '%s'" % cid)
        if aaid:
            sql_list.append("  a.aaid = '%s'" % aaid)
        if event_name:
            sql_list.append("  a.name = '%s'" % event_name)
        if stime:
            sql_list.append("  a.day >= '%s'" % stime)
        if etime:
            sql_list.append("  a.day <= '%s'" % etime)
        if len(sql_list) > 0:
            if len(sql_list) > 1:
                sql_str = " where  " + "and".join(sql_list)
            else:
                sql_str = "where " + sql_list[0]
            sql += sql_str
            sql2 += sql_str
        sql += " order by a.id desc limit %d, %d" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                d['username'] = d['username'] if d['username'] else ''
                del d['day']
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 导出事件上报数据
# @admin.route('/admin/export_event_report_list_post', methods=['post'])
# @login_required
# def export_event_report_list():
#     stime = request.args.get('stime')
#     etime = request.args.get('etime')
#     cid = request.args.get('cid')
#     aaid = request.args.get('aaid')
#     event_name = request.args.get('event_name')
#     sql = "select a.*, b.username from san_app_event a left join san_agent b on a.cid = b.cid "
#     sql_list = []
#     if cid:
#         sql_list.append(" a.cid = '%s'" % cid)
#     if aaid:
#         sql_list.append(" a.aaid = '%s'" % aaid)
#     if event_name:
#         sql_list.append(" a.name = '%s'" % event_name)
#     if stime:
#         sql_list.append(" a.day >= '%s'" % stime)
#     if etime:
#         sql_list.append(" a.day <= '%s'" % etime)
#     if len(sql_list) > 0:
#         if len(sql_list) > 1:
#             sql_str = " where " + "and".join(sql_list)
#         else:
#             sql_str = " where " + sql_list[0]
#         sql += sql_str
#     sql += " order by a.id desc"
#     mysql = Mysql()
#     res = mysql.getAll(sql, None)
#     mysql.dispose()
#     info = []
#     if res:
#         for d in res:
#             d['add_time'] = str(d['add_time'])
#             d['username'] = d['username'] if d['username'] else ''
#             del d['day']
#             arr = [d['add_time'], d['name'], d['username'], d['uid'], d['aaid'], d['ip']]
#             info.append(arr)
#     headers = (u"时间", u"事件", u"渠道", u"UID", u"aaid", u"IP")
#     filename = u'事件上报' + time.strftime("%Y-%m-%d")
#     filename = filename.encode('utf-8')
#     data = tablib.Dataset(*info, headers=headers)
#     resp = make_response(data.xls)
#     resp.headers["Content-Disposition"] = "attachment; filename=%s.xls" % filename.decode('latin-1')
#     return resp


# 获取事件统计数据
@admin.route('/admin/event_report_total_post', methods=['post'])
@login_required
def event_report_total_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    try:
        day = time.strftime("%Y-%m-%d")
        cid = request.values.get('cid')
        stime = request.values.get('stime', day)
        etime = request.values.get('etime', day)
        sql = "select name, sum(num) as num from san_event_day_report "
        sql_list = []
        if cid:
            sql_list.append(" cid = '%s'" % cid)
        if stime:
            sql_list.append(" day >= '%s'" % stime)
        if etime:
            sql_list.append("  day <= '%s'" % etime)
        if len(sql_list) > 0:
            if len(sql_list) > 1:
                sql_str = " where " + "and".join(sql_list)
            else:
                sql_str = " where " + sql_list[0]
            sql += sql_str
        sql += " group by name order by name asc"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        mysql.dispose()
        if res:
            for d in res:
                d['num'] = str(d['num'])
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取事件类型
def get_event_total():
    sql = "select name from san_event_day_report group by name order by name asc"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


# 获取事件类型
def get_event():
    sql = "select name from san_app_event group by name order by name asc"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


#  获取所有渠道
def get_agent():
    sql = "select cid, username from san_agent"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res
