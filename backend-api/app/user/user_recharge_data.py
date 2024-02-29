#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022/4/6 17:43
# @Author : 78957
import importlib

from app.user import user
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util
import sys

importlib.reload(sys)



# 获取付费分析数据
@user.route('/admin/user_payment_detail_post', methods=['post'])
@login_required
def user_payment_detail_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total'] = dict()
    field = ['user_num','install_num','d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13', 'd14', 'd15',
              'd20', 'd25', 'd30','dother']
    for val in field:
        data['total'][val] = 0
    try:
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        cid = request.values.get('cid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql_m = "select day, cid, bid, sum(d1) d1, sum(d2) d2, sum(d3) d3, sum(d4) d4, sum(d5) d5, sum(d6) d6, " \
                "sum(d7) d7, sum(d8) d8, sum(d9) d9, sum(d10) d10, sum(d11) d11, sum(d12) d12, sum(d13) d13, " \
                "sum(d14) d14, sum(d15) d15, sum(d20) d20, sum(d25) d25, sum(d30) d30, sum(dother) dother from " \
                "san_user_day_recharge as a "
        sql_t = "select day, cid, bid, sum(d1) d1, sum(d2) d2, sum(d3) d3, sum(d4) d4, sum(d5) d5, sum(d6) d6, " \
                "sum(d7) d7, sum(d8) d8, sum(d9) d9, sum(d10) d10, sum(d11) d11, sum(d12) d12, sum(d13) d13, " \
                "sum(d14) d14, sum(d15) d15, sum(d20) d20, sum(d25) d25, sum(d30) d30, sum(dother) dother from " \
                "san_user_day_recharge as a "
        sql = "select a.day, sum(a.phone_num + a.face_num) user_num, sum(a.install_num) install_num, " \
              "if(b.d1, b.d1, 0) d1, if(b.d2, b.d2, 0) d2, if(b.d3, b.d3, 0) d3, if(b.d4, b.d4, 0) d4, " \
              "if(b.d5, b.d5, 0) d5, if(b.d6, b.d6, 0) d6, if(b.d7, b.d7, 0) d7, if(b.d8, b.d8, 0) d8, " \
              "if(b.d9, b.d9, 0) d9, if(b.d10, b.d10, 0) d10, if(b.d11, b.d11, 0) d11, if(b.d12, b.d12, 0) d12, " \
              "if(b.d13, b.d13, 0) d13, if(b.d14, b.d14, 0) d14,  if(b.d15, b.d15, 0) d15, " \
              "if(b.d20, b.d20, 0) d20, if(b.d25, b.d25, 0) d25, if(b.d30, b.d30, 0) d30, " \
              "if(b.dother, b.dother, 0) dother from " \
              "san_day_money_total a left join (san_user_day_recharge) b on b.day = a.day "
        sql2 = "select count(*) con from "
        sql3 = "select sum(a.phone_num + a.face_num) user_num, sum(a.install_num) install_num, if(b.d1, b.d1, 0) d1, " \
               "if(b.d2, b.d2, 0) d2, if(b.d3, b.d3, 0) d3, if(b.d4, b.d4, 0) d4, if(b.d5, b.d5, 0) d5, " \
               "if(b.d6, b.d6, 0) d6, if(b.d7, b.d7, 0) d7, if(b.d8, b.d8, 0) d8, if(b.d9, b.d9, 0) d9, " \
               "if(b.d10, b.d10, 0) d10, if(b.d11, b.d11, 0) d11, if(b.d12, b.d12, 0) d12, if(b.d13, b.d13, 0) d13, " \
               "if(b.d14, b.d14, 0) d14, if(b.d15, b.d15, 0) d15, if(b.d20, b.d20, 0) d20, " \
               "if(b.d25, b.d25, 0) d25, if(b.d30, b.d30, 0) d30, if(b.dother, b.dother, 0) dother from " \
               "san_day_money_total a left join (san_user_day_recharge) b on b.day = a.day "
        sql2 += " (select day, sum(install_num) recharge_money from san_day_money_total as a "
        sql_list = []
        if cid:
            sql_list.append(" a.cid = '%s'" % cid)
        if stime:
            sql_list.append(" a.day >= '%s'" % stime)
        if etime:
            sql_list.append(" a.day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)
        sql += sql_str
        sql2 += sql_str
        sql3 += sql_str
        sql_m += sql_str
        sql_t += sql_str
        sql += " group by a.day order by a.day desc, a.total_bet desc limit %d, %d" % (offset, limit)
        sql2 += " group by day order by day desc limit 100000) aa "
        sql_m += " group by day"
        sql = sql.replace("san_user_day_recharge", sql_m)
        sql3 = sql3.replace("san_user_day_recharge", sql_t)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        total = mysql.getOne(sql3, None)
        mysql.dispose()
        arr = []
        if res:
            for d in res:
                arr_list = dict()
                arr_list['day'] = str(d['day'])
                for val in field:
                    value = str(d[val]) if d[val] else '0'
                    arr_list[val] = value
                arr.append(arr_list)
            for val in field:
                value = str(total[val]) if total[val] else '0'
                data['total'][val]=value
            data['data'] = arr
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 获取付费留存数据
@user.route('/admin/user_keep_pay_post', methods=['post'])
@login_required
def user_keep_pay_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total'] = dict()
    data['total']['user_num'] = 0
    data['total']['install_num'] = 0
    field = ['d1','d2','d3','d4','d5','d6','d7','d8','d9','d10','d11','d12','d13','d14','d15'
        ,'d20','d25','d30']
    for val in field:
        data['total'][val] = 0
    try:
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        cid = request.values.get('cid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset  = (int(page) - 1) * int(limit)
        sql_sum = get_days(field)
        sql_m = "select day, cid,  " + sql_sum + " from san_user_day_recharge "
        sql_t = "select day, cid,  " + sql_sum + " from san_user_day_recharge "
        sql2 = "select count(*) con from "
        sql2 += " (select day, sum(d1) d1 from san_user_day_recharge"
        sql_list = []
        if cid:
            sql_list.append("  cid = '%s'" % cid)
        if stime:
            sql_list.append("  day >= '%s'" % stime)
        if etime:
            sql_list.append(" day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)
        sql_m += sql_str
        sql_t += sql_str
        sql2 += sql_str
        sql_m += " group by day order by day desc limit %d, %d" % (offset, limit)
        sql2 += " group by day order by day desc limit 100000) aa "
        mysql = Mysql()
        res = mysql.getAll(sql_m, None)
        cont = mysql.getOne(sql2, None)
        total = mysql.getOne(sql_t, None)
        mysql.dispose()
        arr = []
        if res:
            for d in res:
                arr_list = dict()
                arr_list['day'] =str(d['day'])
                for val in field:
                    value=str(d[val]) if d[val] else '0'
                    arr_list[val] = value
                arr.append(arr_list)
            for val in field:
                value = str(total[val]) if total[val] else '0'
                data['total'][val]=value
            # data['total']['d1'] = str(total['d1']) if total['d1'] else 0
            # data['total']['d2'] = str(total['d2']) if total['d2'] else 0
            # data['total']['d3'] = str(total['d3']) if total['d3'] else 0
            # data['total']['d4'] = str(total['d4']) if total['d4'] else 0
            # data['total']['d5'] = str(total['d5']) if total['d5'] else 0
            # data['total']['d6'] = str(total['d6']) if total['d6'] else 0
            # data['total']['d7'] = str(total['d7']) if total['d7'] else 0
            # data['total']['d8'] = str(total['d8']) if total['d8'] else 0
            # data['total']['d9'] = str(total['d9']) if total['d9'] else 0
            # data['total']['d10'] = str(total['d10']) if total['d10'] else 0
            # data['total']['d11'] = str(total['d11']) if total['d11'] else 0
            # data['total']['d12'] = str(total['d12']) if total['d12'] else 0
            # data['total']['d13'] = str(total['d13']) if total['d13'] else 0
            # data['total']['d14'] = str(total['d14']) if total['d14'] else 0
            # data['total']['d15'] = str(total['d15']) if total['d15'] else 0
            # data['total']['d16'] = str(total['d16']) if total['d16'] else 0
            # data['total']['d17'] = str(total['d17']) if total['d17'] else 0
            # data['total']['d18'] = str(total['d18']) if total['d18'] else 0
            # data['total']['d19'] = str(total['d19']) if total['d19'] else 0
            # data['total']['d20'] = str(total['d20']) if total['d20'] else 0
            # data['total']['d21'] = str(total['d21']) if total['d21'] else 0
            # data['total']['d22'] = str(total['d22']) if total['d22'] else 0
            # data['total']['d23'] = str(total['d23']) if total['d23'] else 0
            # data['total']['d24'] = str(total['d24']) if total['d24'] else 0
            # data['total']['d25'] = str(total['d25']) if total['d25'] else 0
            # data['total']['d26'] = str(total['d26']) if total['d26'] else 0
            # data['total']['d27'] = str(total['d27']) if total['d27'] else 0
            # data['total']['d28'] = str(total['d28']) if total['d28'] else 0
            # data['total']['d29'] = str(total['d29']) if total['d29'] else 0
            # data['total']['d30'] = str(total['d30']) if total['d30'] else 0
            data['data'] = arr
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


def get_days(field):
    a = ''
    for d in field:
        a += 'ifnull(sum(%s),0) %s,' % (str(d), str(d))
    return a[:-1]





