# -*- coding: utf-8 - *-
# @Time: 2023/2/20
# @Author:Jack c

import importlib
import sys
import time


from flask import render_template, request, jsonify
from app import  public_util
from app.util import login_required
from SqlConntion.MySqlConn import Mysql
from . import admin

importlib.reload(sys)



# 提现分析
@admin.route('/admin/withdraw_day_data_post', methods=['POST'])
@login_required
def withdraw_day_data_post():
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
            sql = "select date_format(a.add_time,'%Y-%m-%d') day, a.pay_id, b.pay_name, count(*) num, " \
                  "count(if(a.status = 6, true, null )) err_num, count(if(a.status = 1, true, null)) res_num, " \
                  "sum(if(a.status = 1, money, 0)) money from " \
                  "san_withdraw_list a left join san_pay_list b on a.pay_id = b.pay_id "
            sql2 = "select count(*) con from "
            sql2 += " (select pay_id, date_format(add_time,'%Y-%m-%d') day from san_withdraw_list as a  "
            sql_list = []
            if pay_id:
                sql_list.append("  a.pay_id = '%s'" % pay_id)
            if stime:
                sql_list.append(" date_format(a.add_time,'%%Y-%%m-%%d') >= '%s'" % stime)
            if etime:
                sql_list.append(" date_format(a.add_time,'%%Y-%%m-%%d') <= '%s'" % etime)
            sql_str = public_util.data_list_to_str(sql_list)
            sql += sql_str
            sql2 += sql_str
            sql += " group by day, a.pay_id order by day desc, num desc limit 10000"
            sql2 += " group by day, pay_id) aa"
            mysql = Mysql()
            res = mysql.getAll(sql, None)
            cont = mysql.getOne(sql2, None)
            mysql.dispose()
            if res:
                for d in res:
                    d['day'] = str(d['day'])
                    d['num'] = float(d['num'])
                    d['err_num'] = float(d['err_num'])
                    d['res_num'] = float(d['res_num'])
                    d['or_num'] = d['num'] - d['err_num']
                    d['money'] = float(d['money'])
                    data['total']['num'] += d['num']
                    data['total']['or_num'] += d['or_num']
                    data['total']['res_num'] += d['res_num']
                    data['total']['money'] += d['money']
                    d['order_ratio'] = str(round(d['or_num'] * 100 / d['num'], 2)) + '%' if d['num'] > 0 else '0'
                    d['res_ratio'] = str(round(d['res_num'] * 100 / d['or_num'], 2)) + '%' if d['or_num'] > 0 else '0'
                    d['or_num'] = str(int(d['or_num'])) + '(' + d['order_ratio'] + ')'
                    d['res_num'] = str(int(d['res_num'])) + '(' + d['res_ratio'] + ')'
                data['total']['order_ratio'] = str(
                    round(data['total']['or_num'] * 100 / data['total']['num'], 2)) + '%' if \
                    data['total']['num'] > 0 else '0'
                data['total']['res_ratio'] = str(
                    round(data['total']['res_num'] * 100 / data['total']['or_num'], 2)) + '%' if data['total'][
                                                                                                     'or_num'] > 0 else '0'
                data['total']['or_num'] = str(int(data['total']['or_num'])) + '(' + data['total']['order_ratio'] + ')'
                data['total']['res_num'] = str(int(data['total']['res_num'])) + '(' + data['total']['res_ratio'] + ')'
                data['data'] = res
                data['count'] = cont['con']
            data['code'] = 1
        except Exception as e:
            print(e)
        return jsonify(data)


# 获取支付列表
def get_pay():
    sql = "select pay_id, pay_name from san_pay_list"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res
