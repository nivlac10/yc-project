#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022/4/16 15:44
# @Author : 78957
import importlib

from app.user import user
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util
import sys

importlib.reload(sys)



# 获取支付通道分析数据
@user.route('/admin/pay_day_detail_post', methods=['post'])
@login_required
def user_pay_day_detail_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total'] = dict()
    data['total']['new_num'] = 0  # 点击付费按钮次数-新
    data['total']['old_num'] = 0  # 点击付费按钮次数-老
    data['total']['total_num'] = 0  # 点击付费按钮次数-总
    data['total']['new_user_xd_num'] = 0  # 点击付费按钮人数-新
    data['total']['old_user_xd_num'] = 0  # 点击付费按钮人数-老
    data['total']['total_user_xd_num'] = 0  # 点击付费按钮人数-总
    data['total']['new_order_num'] = 0  # 支付通道拉起次数-新
    data['total']['old_order_num'] = 0  # 支付通道拉起次数-老
    data['total']['total_order_num'] = 0  # 支付通道拉起次数-总
    data['total']['new_user_order_num'] = 0  # 支付通道拉起人数-新
    data['total']['old_user_order_num'] = 0  # 支付通道拉起人数-老
    data['total']['total_user_order_num'] = 0  # 支付通道拉起人数-总
    data['total']['new_ratio'] = 0  # 支付通道拉起率-新   支付通道拉起人数-新/点击付费按钮人数-新
    data['total']['old_ratio'] = 0  # 支付通道拉起率-老   支付通道拉起人数-老/点击付费按钮人数-老
    data['total']['total_ratio'] = 0  # 支付通道拉起率-总   支付通道拉起人数-总/点击付费按钮人数-总
    data['total']['new_user_num'] = 0  # 支付成功人数-新
    data['total']['old_user_num'] = 0  # 支付成功人数-老
    data['total']['total_user_num'] = 0  # 支付成功人数-总
    data['total']['new_result_ratio'] = 0  # 支付成功率-新   支付成功人数-新/支付通道拉起人数-新
    data['total']['old_result_ratio'] = 0  # 支付成功率-老   支付成功人数-老/支付通道拉起人数-老
    data['total']['total_result_ratio'] = 0  # 支付成功率-总   支付成功人数-总/支付通道拉起人数-总
    data['total']['new_result_num'] = 0  # 充值成功笔数-新
    data['total']['old_result_num'] = 0  # 充值成功笔数-老
    data['total']['total_result_num'] = 0  # 充值成功笔数-总
    try:
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        cid = request.values.get('cid')

        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)

        sql = "select day, sum(new_num) new_num, sum(old_num) old_num, sum(new_user_xd_num) new_user_xd_num, " \
              "sum(old_user_xd_num) old_user_xd_num, sum(new_order_num) new_order_num, sum(old_order_num) old_order_num, " \
              "sum(new_user_order_num) new_user_order_num, sum(old_user_order_num) old_user_order_num, " \
              "sum(new_user_num) new_user_num, sum(old_user_num) old_user_num, sum(new_result_num) new_result_num, " \
              "sum(old_result_num) old_result_num from san_day_money_total "
        sql2 = "select count(*) con from "
        sql2 += " (select day, sum(new_num) new_num from san_day_money_total"
        sql_list = []
        if cid:
            sql_list.append(" cid = '%s'" % cid)
        if stime:
            sql_list.append(" day >= '%s'" % stime)
        if etime:
            sql_list.append(" day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)
        sql += sql_str
        sql2 += sql_str
        sql += " group by day order by day desc limit %d, %d" % (offset, limit)
        sql2 += " group by day order by day desc limit 100000) aa "
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['day'] = str(d['day'])
                d['new_num'] = str(d['new_num']) if d['new_num'] else 0
                d['old_num'] = str(d['old_num']) if d['old_num'] else 0
                d['total_num'] = float(d['new_num']) + float(d['old_num'])
                d['new_user_xd_num'] = str(d['new_user_xd_num']) if d['new_user_xd_num'] else 0
                d['old_user_xd_num'] = str(d['old_user_xd_num']) if d['old_user_xd_num'] else 0
                d['total_user_xd_num'] = float(d['new_user_xd_num']) + float(d['old_user_xd_num'])
                d['new_order_num'] = str(d['new_order_num']) if d['new_order_num'] else 0
                d['old_order_num'] = str(d['old_order_num']) if d['old_order_num'] else 0
                d['total_order_num'] = float(d['new_order_num']) + float(d['old_order_num'])
                d['new_user_order_num'] = str(d['new_user_order_num']) if d['new_user_order_num'] else 0
                d['old_user_order_num'] = str(d['old_user_order_num']) if d['old_user_order_num'] else 0
                d['total_user_order_num'] = float(d['new_user_order_num']) + float(d['old_user_order_num'])
                d['new_ratio'] = round(float(d['new_user_order_num']) / float(d['new_user_xd_num']), 4) if float(
                    d['new_user_xd_num']) > 0 else 0
                d['old_ratio'] = round(float(d['old_user_order_num']) / float(d['old_user_xd_num']), 4) if float(
                    d['old_user_xd_num']) > 0 else 0
                d['total_ratio'] = round(float(d['total_user_order_num']) / float(d['total_user_xd_num']), 4) if float(
                    d['total_user_xd_num']) > 0 else 0
                d['new_user_num'] = str(d['new_user_num']) if d['new_user_num'] else 0
                d['old_user_num'] = str(d['old_user_num']) if d['old_user_num'] else 0
                d['total_user_num'] = float(d['new_user_num']) + float(d['old_user_num'])
                d['new_result_ratio'] = round(float(d['new_user_num']) / float(d['new_user_order_num']), 4) if float(
                    d['new_user_order_num']) > 0 else 0
                d['old_result_ratio'] = round(float(d['old_user_num']) / float(d['old_user_order_num']), 4) if float(
                    d['old_user_order_num']) > 0 else 0
                d['total_result_ratio'] = round(float(d['total_user_num']) / float(d['total_user_order_num']),
                                                4) if float(d['total_user_order_num']) > 0 else 0
                d['new_result_num'] = str(d['new_result_num']) if d['new_result_num'] else 0
                d['old_result_num'] = str(d['old_result_num']) if d['old_result_num'] else 0
                d['total_result_num'] = float(d['new_result_num']) + float(d['old_result_num'])
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


