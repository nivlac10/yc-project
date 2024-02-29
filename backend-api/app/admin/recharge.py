#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-03-04
import importlib
import json
import sys,time,requests

from flask import  render_template,request, jsonify

from app import public_util,  redis,public_game_api,common,constant
from app.util import login_required
from SqlConntion.MySqlConn import Mysql
from . import admin
from ..RKEY import SAN_EXTERNAL_GAME_LIST

importlib.reload(sys)



# 充值列表
@admin.route('/admin/recharge_conf_list_post',methods=['post'])
@login_required
def recharge_conf_list_post():
    data= dict()
    data['code']=1
    data['channel'] = get_channel_all()
    data['pay'] = get_all_pay()
    return jsonify(data)


# 获取充值列表数据
@admin.route('/admin/recharge_list_post', methods=['post'])
@login_required
def recharge_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total_money'] = 0
    try:
        uid = request.values.get('uid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        status = request.values.get('status')
        cid = request.values.get('cid')
        pay_id = request.values.get('pay_id')
        sort_index = request.values.get('sort_index', 'a.uid')
        order_index = request.values.get('order_index', 'desc')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql_list = []
        if uid:
            sql_list.append(
                " (locate('%s', a.uid)>0 or locate('%s', b.nickname) > 0 or locate('%s', a.pay_order_number)>0 or locate('%s', a.order_number)>0)" % (
                    uid, uid, uid, uid))
        if status:
            sql_list.append(" a.status = '%s'" % status)
        if cid:
            sql_list.append(" a.cid = '%s'" % cid)

        if pay_id:
            sql_list.append(" a.pay_id = '%s'" % pay_id)
        if stime:
            sql_list.append(" a.add_time >= '%s'" % stime)
        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append(" a.add_time <= '%s'" % e_str)
        sql_str = public_util.data_list_to_str(sql_list)

        sql = "select a.id,a.uid,a.order_number,ifnull(a.money,0) money,a.merchant_param,a.user_ip,a.add_time,ifnull(a.notify_time,'') notify_time," \
              "a.status, b.nickname, c.pay_name, d.username agent from san_order_list a left join san_users b " \
              "on b.uid = a.uid left join san_pay_list c on c.pay_id = a.pay_id left join san_agent d " \
              "on d.cid = a.cid %s order by %s %s limit %d, %d" % (sql_str, sort_index, order_index, offset, limit)
        sql2 = "select count(*) con,sum(ifnull(a.money,0)) money from san_order_list a left join san_users b on b.uid = a.uid %s"%sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        status_list = ['下单成功', '充值成功', '充值失败', '下单失败']
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                # d['time_int'] = public_util.days_int(d['add_time']) * 1000
                d['notify_time'] = str(d['notify_time'])
                d['status_str'] = status_list[d['status']]
                d['pay_name'] = d['pay_name'] if d['pay_name'] else ''
            data['data'] = res
            data['count'] = cont['con']
            data['total_money'] = str(cont['money'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 用户充值订单详情
@admin.route('/admin/user_order_detail_post',methods=['post'])
@login_required
def user_order_detail_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    try:
        id = request.values.get('id', '0')
        sql = "select a.*, b.nickname, c.pay_name from san_order_list a left join san_users b on a.uid = b.uid left " \
              "join san_pay_list c on c.pay_id = a.pay_id where a.id = '%s'" % id
        mysql = Mysql()
        res = mysql.getOne(sql, None)
        mysql.dispose()
        if res:
            res['add_time']=str(res['add_time'])
            res['notify_time']=str(res['notify_time'])
            res['err_msg'] = json.loads(res['err_msg'])
            res['send_data'] = res['err_msg']['send_data'] if 'send_data' in res['err_msg'] else ''
            if 'send_data' in res['err_msg']:
                del res['err_msg']['send_data']
            if res['first_pay'] == 1:
                res['first_pay'] = "新用户首充"
            elif res['first_pay'] == 2:
                res['first_pay'] = "用户日首充"
            else:
                res['first_pay'] = "否"
            data['data']=res
            data['code']=1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取所有支付
def get_all_pay():
    sql = "select pay_id, pay_name from san_pay_list where status = 1"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


# 获取所有渠道
def get_channel_all():
    sql = "select cid, username from san_agent "
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res








