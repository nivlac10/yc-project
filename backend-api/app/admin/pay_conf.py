#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-05-26
import importlib

from . import admin
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import  util_update_redis
import sys

importlib.reload(sys)



# 获取支付数据
@admin.route('/admin/pay_list_post', methods=['post'])
@login_required
def pay_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    try:
        sort_index = request.values.get('sort_index', '0')
        status = request.values.get('status')
        s_key = 'status' if str(sort_index) == '0' else 'with_flag'
        qz = 'sort_index' if str(sort_index) == '0' else 'withdraw_index'
        sql = "select * from san_pay_list where 1=1 "
        if status:
            sql += " and %s = '%s'" % (s_key, status)
        sql += " order by %s desc, %s desc" % (s_key, qz)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        mysql.dispose()
        # pay_type = get_pay_type_all()
        if res:
            # for d in res:
            #     d['pay_type'] = pay_type[str(d['tid'])] if str(d['tid']) in pay_type else ''
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)




# 添加支付处理
@admin.route('/admin/add_pay_post', methods=['post'])
@login_required
def add_pay_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:

        pay_name = request.values.get('pay_name', '')
        sort_index = request.values.get('sort_index', '0')
        recharge_url = request.values.get('recharge_url')
        callback_url = request.values.get('callback_url')
        withdraw_conf_url = request.values.get('withdraw_conf_url')
        pay_ratio = request.values.get('pay_ratio')
        withdraw_ratio = request.values.get('withdraw_ratio')
        min_payment_money = request.values.get('min_payment_money')
        max_payment_money = request.values.get('max_payment_money')
        min_transfer_money = request.values.get('min_transfer_money')
        max_transfer_money = request.values.get('max_transfer_money')
        withdraw_index = request.values.get('withdraw_index')
        with_flag = request.values.get('with_flag')
        status = request.values.get('status', '')
        pay_type = request.values.get('pay_type', '1')
        con = get_pay_name(pay_name)
        if con:
            data['msg'] = '支付名称已存在'
            return jsonify(data)
        sql = "insert into san_pay_list (pay_name,sort_index, recharge_url, callback_url,  withdraw_conf_url ,pay_ratio,withdraw_ratio,min_payment_money," \
              "max_payment_money,min_transfer_money,max_transfer_money,withdraw_index,with_flag,status,pay_type) values (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s,%s) "
        mysql = Mysql()
        res = mysql.insertOne(sql, [pay_name, sort_index, recharge_url, callback_url,  withdraw_conf_url, pay_ratio, withdraw_ratio, min_payment_money,
                                    max_payment_money, min_transfer_money, max_transfer_money, withdraw_index, with_flag, status,pay_type])
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '添加成功'
    except Exception as e:
        print(e)
    return jsonify(data)




# 更新支付信息
@admin.route('/admin/pay_detail_post', methods=['post'])
@login_required
def pay_detail_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        pay_name = request.values.get('pay_name', '')
        sort_index = request.values.get('sort_index', '0')
        recharge_url = request.values.get('recharge_url')
        callback_url = request.values.get('callback_url')
        withdraw_conf_url = request.values.get('withdraw_conf_url')
        pay_id = request.values.get('pay_id')
        pay_ratio = request.values.get('pay_ratio')
        withdraw_ratio = request.values.get('withdraw_ratio')
        min_payment_money = request.values.get('min_payment_money')
        max_payment_money = request.values.get('max_payment_money')
        min_transfer_money = request.values.get('min_transfer_money')
        max_transfer_money = request.values.get('max_transfer_money')
        withdraw_index = request.values.get('withdraw_index')
        with_flag = request.values.get('with_flag')
        status = request.values.get('status', '')
        pay_type = request.values.get('pay_type')
        con = get_pay_detail(pay_id)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        # pay_type = get_pay_type_detail(tid)
        # if pay_type is None:
        #     data['msg'] = '支付类型不存在'
        #     return jsonify(data)
        # if pay_type['status'] == 0:
        #     data['msg'] = '支付类型已禁用'
        #     return jsonify(data)
        sql = "update san_pay_list set pay_name = %s, recharge_url = %s, callback_url =%s, " \
              "withdraw_conf_url = %s,  sort_index = %s, pay_ratio = %s, " \
              "withdraw_ratio = %s, min_payment_money = %s, max_payment_money = %s, min_transfer_money = %s, " \
              "max_transfer_money = %s, withdraw_index = %s, with_flag = %s, status = %s,pay_type = %s  where pay_id = %s"
        parame=[pay_name, recharge_url, callback_url, withdraw_conf_url, sort_index, pay_ratio,
               withdraw_ratio, min_payment_money, max_payment_money, min_transfer_money, max_transfer_money,
               withdraw_index, with_flag, status, pay_type, pay_id]
        mysql = Mysql()
        res = mysql.update(sql, parame)
        mysql.dispose()
        if res >= 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
            util_update_redis.add_game_withdraw_conf()
    except Exception as e:
        print(e)
    return jsonify(data)


# 启用支付
@admin.route('/admin/update_pay_statue_post', methods=['post'])
@login_required
def update_pay_statue_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        pay_id = request.values.get('pay_id')
        status = request.values.get('status')
        if status not in ['0', '1']:
            data['msg'] = '参数错误'
            return jsonify(data)
        con = get_pay_detail(pay_id)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        sql = "update san_pay_list set status = %s where pay_id = %s"
        mysql = Mysql()
        res = mysql.update(sql, [status, pay_id])
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = "操作成功"
            util_update_redis.add_game_withdraw_conf()
    except Exception as e:
        print(e)
    return jsonify(data)


# 启用提现
@admin.route('/admin/open_withdraw_channel_post', methods=['post'])
@login_required
def open_withdraw_channel_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        pay_id = request.values.get('pay_id')
        status = request.values.get('status')
        if status not in ['0', '1']:
            data['msg'] = '参数错误'
            return jsonify(data)
        con = get_pay_detail(pay_id)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        sql = "update san_pay_list set with_flag = %s where pay_id = %s"
        mysql = Mysql()
        res = mysql.update(sql, [status, pay_id])
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = "操作成功"
            util_update_redis.add_game_withdraw_conf()
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除支付处理
@admin.route('/admin/delete_pay_channel_post', methods=['post'])
@login_required
def delete_pay_channel_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        pay_id = request.values.get('pay_id')
        con = get_pay_detail(pay_id)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        sql = "delete from san_pay_list where pay_id = %s"
        mysql = Mysql()
        res = mysql.delete(sql, [pay_id])
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
            util_update_redis.add_game_withdraw_conf()
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取类型详情
def get_pay_type_detail(tid):
    sql = "select * from san_pay_type where tid = '%s'" % tid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res




# 获取所有类型
def get_pay_type_all():
    sql = "select * from san_pay_type"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    maps = dict()
    if res:
        for d in res:
            maps[str(d['tid'])] = d['type_name']
    return maps


# 获取支付详情
def get_pay_detail(pay_id):
    sql = "select * from san_pay_list where pay_id = '%s'" % pay_id
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 获取支付名称
def get_pay_name(pay_name):
    sql = "select * from san_pay_list where pay_name = '%s'" % pay_name
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


