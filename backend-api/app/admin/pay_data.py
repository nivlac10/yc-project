#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022/5/19 14:59
# @Author : 78957
import importlib
import time

from . import admin
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util
import sys

importlib.reload(sys)



# 获取支付分析数据
@admin.route('/admin/pay_day_data_post', methods=['post'])
@login_required
def pay_day_data_post():
    data = dict()
    data['code'] = 0
    data['count'] = 0
    data['data'] = []
    data['total'] = dict()
    data['total']['num'] = 0
    data['total']['or_num'] = 0
    data['total']['res_num'] = 0
    data['total']['money'] = 0
    try:
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        pay_id = request.values.get('pay_id')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql = "select date_format(a.add_time,'%Y-%m-%d') day, a.pay_id, b.pay_name, count(*) num, " \
              "count(if(a.status = 3, true, null )) err_num, count(if(a.status = 1, true, null)) res_num," \
              "sum(if(a.status=1,money,0)) money from " \
              "san_order_list a left join san_pay_list b on a.pay_id = b.pay_id where 1=1"
        sql2 = "select count(*) con from (select pay_id, date_format(add_time,'%Y-%m-%d') day from " \
               "san_order_list where 1=1"
        if pay_id:
            sql += " and a.pay_id = '%s'" % pay_id
            sql2 += " and pay_id = '%s'" % pay_id
        if stime:
            sql += " and date_format(a.add_time,'%%Y-%%m-%%d') >= '%s'" % stime
            sql2 += " and date_format(add_time,'%%Y-%%m-%%d') >= '%s'" % stime
        if etime:
            sql += " and date_format(a.add_time,'%%Y-%%m-%%d') <= '%s'" % etime
            sql2 += " and date_format(add_time,'%%Y-%%m-%%d') <= '%s'" % etime
        sql += " group by day, a.pay_id order by day desc, num desc limit %d, %d" % (c_num, limit)
        sql2 += " group by day, pay_id) aa"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        print(res)
        if res:
            for d in res:
                d['day'] = str(d['day'])
                d['num'] = float(d['num'])
                d['err_num'] = float(d['err_num'])
                d['res_num'] = float(d['res_num'])
                d['or_num'] = d['num'] - d['err_num']
                data['total']['num'] += d['num']
                data['total']['or_num'] += d['or_num']
                data['total']['res_num'] += d['res_num']
                data['total']['money'] += d['money']
                d['order_ratio'] = str(round(d['or_num'] * 100 / d['num'], 2)) + '%' if d['num'] > 0 else '0'
                d['res_ratio'] = str(round(d['res_num'] * 100 / d['or_num'], 2)) + '%' if d['or_num'] > 0 else '0'
                d['or_num'] = str(int(d['or_num'])) + '(' + d['order_ratio'] + ')'
                d['res_num'] = str(int(d['res_num'])) + '(' + d['res_ratio'] + ')'
            data['total']['order_ratio'] = str(round(data['total']['or_num'] * 100 / data['total']['num'], 2)) + '%' if \
                data['total']['num'] > 0 else '0'
            data['total']['res_ratio'] = str(round(data['total']['res_num'] * 100 / data['total']['or_num'],
                                                   2)) + '%' if data['total']['or_num'] > 0 else '0'
            data['total']['or_num'] = str(int(data['total']['or_num'])) + '(' + data['total']['order_ratio'] + ')'
            data['total']['res_num'] = str(int(data['total']['res_num'])) + '(' + data['total']['res_ratio'] + ')'
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


