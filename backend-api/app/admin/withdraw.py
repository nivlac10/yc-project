#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-04-22
import codecs
import importlib
import json
import sys

from flask import render_template, request, jsonify

from SqlConntion.RedisDB import Redis
from app import common, public_util, redis, RKEY,  constant
from app.util import login_required
from SqlConntion.MySqlConn import Mysql
from . import admin

importlib.reload(sys)


# 提现支付列表
@admin.route('/admin/withdraw_pay_list', methods=['post'])
@login_required
def withdraw_pay_list():
    data = dict()
    data['code'] = 1
    data['pay'] = get_all_pay()
    return jsonify(data)


# 获取充值列表数据
@admin.route('/admin/withdraw_list_post', methods=['post'])
@login_required
def withdraw_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    # data['total_money'] = 0
    data['send_money'] = 0
    data['rate'] = 0
    data['page'] = 1
    try:
        uid = request.values.get('uid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        status = request.values.get('status')
        money_type = request.values.get('money_type')
        min_money = request.values.get('min_money')
        max_money = request.values.get('max_money')
        pay_id = request.values.get('pay_id')
        sort_index = request.values.get('sort_index')
        order_index = request.values.get('order_index')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql = "select a.*, b.nickname, ifnull(b.total_money,0) total_money, ifnull(b.total_withdraw,0) total_withdraw, c.pay_name, b.aaid, b.register_ip, " \
              "d.username c_name from san_withdraw_list a left join san_users b on b.uid = a.uid left join " \
              "san_pay_list c on c.pay_id = a.pay_id left join san_agent d on d.cid = a.cid "
        sql2 = "select count(*) con,sum(a.money) money, sum(send_money) send_money, sum(rate) rate from san_withdraw_list a left join san_users b on b.uid = a.uid "
        # sql3 = "select sum(a.money) money, sum(send_money) send_money, sum(rate) rate from san_withdraw_list a " \
        #        "left join san_users b on b.uid = a.uid "
        sql_list = []
        if uid:
            sql_list.append(
                " ( locate('%s', a.uid) > 0 or locate('%s', b.nickname) > 0 or locate('%s', a.pay_order_number) > 0  or locate('%s', a.order_number) > 0 )" % (
                    uid, uid, uid, uid))
        if status:
            sql_list.append("  a.status = '%s'" % status)
        if pay_id:
            sql_list.append("  a.pay_id = '%s'" % pay_id)
        if money_type:
            sql_list.append("  a.money_type = '%s'" % money_type)
        if min_money:
            sql_list.append("  a.money >= '%s'" % min_money)
        if max_money:
            sql_list.append("  a.money <= '%s'" % max_money)
        if stime:
            sql_list.append("  a.add_time >= '%s'" % stime)
        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append(" a.add_time <= '%s'" % e_str)
        sql_str = public_util.data_list_to_str(sql_list)
        sql += sql_str
        sql2 += sql_str
        # sql3 += sql_str
        sql += " order by %s %s limit %d, %d" % (sort_index,order_index,c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        # total = mysql.getOne(sql3, None)
        mysql.dispose()
        status_list = ['下单成功', '提现成功', '提现失败', '人工审核', '成功后失败', '拒绝提现', '下单失败']
        if res:
            for d in res:
                d['withdraw_name'] = "余额提现"
                if d['money_type'] == 1:
                    d['withdraw_name'] = "佣金提现"
                if d['money_type'] == 2:
                    d['withdraw_name'] = "后台手动提现"
                d['add_time'] = str(d['add_time'])
                # d['time_int'] = public_util.days_int(d['add_time']) * 1000
                d['notify_time'] = str(d['notify_time'])
                d['status_str'] = status_list[d['status']]
                d['pay_name'] = d['pay_name'] if d['pay_name'] else ''
                # d['success_int'] = public_util.days_int(d['success_time']) * 1000 if d['success_time'] else 0
                # if d['status'] == 3:
                #     machine_num, ip_num = get_ip_num(d['aaid'], d['register_ip'])
                # else:
                #     machine_num, ip_num = 0, 0

                d['machine_num'] = '查看'
                d['ip_num'] = '查看'
                d['auto_flag_str'] = '人工干预' if d['auto_flag'] == 1 else '正常订单'
                d['r_w'] = d['total_money'] - d['total_withdraw']
            data['data'] = res
            data['total'] = cont
            # data['total_money'] = str(total['money']) if total['money'] else 0
            # data['send_money'] = str(total['send_money']) if total['send_money'] else 0
            # data['rate'] = str(total['rate']) if total['rate'] else 0
        data['code'] = 1
        data['page'] = page
    except Exception as e:
        print(e)
    return jsonify(data)


@admin.route('/admin/withdraw_order_detail_post', methods=['post'])
@login_required
def withdraw_order_detail_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    try:
        id = request.values.get('id', '0')
        sql = "select a.*, b.nickname, c.pay_name from san_withdraw_list a left join san_users b on b.uid = a.uid left " \
              "join san_pay_list c on c.pay_id = a.pay_id where a.id = '%s'" % id
        mysql = Mysql()
        res = mysql.getOne(sql, None)
        mysql.dispose()
        if res:
            data['code'] = 1
            data['data'] = res
    except Exception as e:
        print(e)
    return jsonify(data)


# 通过用户提现审核
@admin.route('/admin/adopt_user_withdraw_post', methods=['post'])
@login_required
def adopt_user_withdraw_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
    # if True:
        id = request.values.get('id')
        con = get_user_orders(id)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        flag_key = 'update_withdraw_order_' + str(con['id'])
        if redis.get(flag_key):
            data['msg'] = '操作频繁,请稍后'
            return public_util.to_json(data)
        redis.set(flag_key, '1', ex=30)
        if con['status'] not in [3, 4]:
            data['msg'] = '状态错误'
            redis.delete(flag_key)
            return jsonify(data)
        user = get_user_detail(con['uid'])
        if user is None:
            data['msg'] = '用户不存在'
            redis.delete(flag_key)
            return jsonify(data)
        pay_data = get_withdraw_pay(con['pay_id'])
        if pay_data is None:
            data['msg'] = '当前支付不存在或已关闭'
            redis.delete(flag_key)
            return jsonify(data)
        DBCONFIG = constant.DBCONFIG[constant.DBINDEX]
        if str(pay_data['pay_id']) in DBCONFIG["withdraw_conf"] is False:
            data['msg'] = '请添加当前支付手动配置'
            redis.delete(flag_key)
            return jsonify(data)
        # res = user_send_data_func(con, pay_data)
        vip_list = get_vip_lv_list_data()
        user['vip_lv'] = vip_list[user['vip_lv']]
        user_pay_data = dict()
        user_pay_data['money'] = con['money']
        user_pay_data['name'] = con['collection_name']
        user_pay_data['cpf'] = con['cpf']
        user_pay_data['pix'] = con['pix']
        user_pay_data['pix_num'] = con['pix_num']
        user_pay_data['phone'] = con['collection_mobile']
        user_pay_data['email'] = con['collection_email']
        user_pay_data['money_type'] = con['money_type']
        res = DBCONFIG["withdraw_conf"][str(pay_data['pay_id'])].http_post_withdraw_data(user_pay_data, con['order_number'],
                                                                             con['money'],
                                                                             pay_data, user['vip_lv'])
        if res['code'] == 1:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '下单成功'
            update_withdraw_order_status(id, 0)
        else:
            data['msg'] = res['msg']
            update_order_error_msg(con['id'], res['msg'])  # 下单失败
            if con['money_type'] == 0:
                after_money = float(user['money']) + float(con['money'])
                update_user_money(user['uid'], con['money'])
                common.user_money_log_func(user['uid'], con['money'], user['money'], after_money, 17)
            else:
                update_user_commission(user['uid'], con['money'])  # 更新佣金
                after_money = float(user['commission']) + con['money']
                common.user_commission_log_func(user['uid'], con['money'], user['commission'], after_money,
                                                101)  # 佣金变动记录
            send_user_email(user['uid'], res['msg'])
            data['status'] = 0
            data['code'] = 1
        redis.delete(flag_key)
    except Exception as e:
        print(e)
        data['msg'] = '通道请求错误'
    return jsonify(data)


# 拒绝用户提现
@admin.route('/admin/refuse_user_withdraw_post', methods=['post'])
@login_required
def refuse_user_withdraw_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        id = request.values.get('id')
        con = get_user_orders(id)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        if con['status'] not in [3, 4]:
            data['msg'] = '状态错误'
            return jsonify(data)
        res = update_withdraw_order_status(id, 5)
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 取消用户提现
@admin.route('/admin/cancel_user_withdraw_post', methods=['post'])
@login_required
def cancel_user_withdraw_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        id = request.values.get('id')
        value = ""
        # value = request.values.get('value')
        con = get_user_orders(id)
        print(con, id)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        if con['status'] not in [3, 4]:
            data['msg'] = '状态错误'
            return jsonify(data)
        user = get_user_detail(con['uid'])
        if user is None:
            data['msg'] = '用户不存在'
            return jsonify(data)
        res = update_withdraw_order_status(id, 2)
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
            if str(con['money_type']) == '0':
                after_money = float(user['money']) + float(con['money'])
                update_user_money(user['uid'], con['money'])
                common.user_money_log_func(user['uid'], con['money'], user['money'], after_money, 17)
                send_user_email(user['uid'], value)
            if str(con['money_type']) == '1':
                after_money = float(user['commission']) + float(con['money'])
                update_user_commission(user['uid'], con['money'])
                common.user_commission_log_func(user['uid'], con['money'], user['commission'], after_money, 101)
                send_user_email(user['uid'], value)
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取机器码用户列表数据
@admin.route('/admin/user_list_log_post', methods=['post'])
@login_required
def user_list_log_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        uid = request.values.get('uid', '')
        flag = request.values.get('flag', '')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        if str(flag) not in ['1', '2']:
            data['code'] = 0
            return jsonify(data)
        cos = 'aaid' if str(flag) == '1' else 'register_ip'
        sql = "select a.*, b.username bname from san_users a left join san_agent b on b.cid = a.cid where " \
              "a.user_gm = 0 and a.%s in (select %s from san_users where uid = '%s') order by a.uid desc " \
              "limit %d, %d" % (cos, cos, uid, c_num, limit)
        sql2 = "select count(*) con from(select * from san_users where user_gm = 0 and  %s in (select %s from " \
               "san_users where uid = '%s')) aa" % (cos, cos, uid)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time']) if d['add_time'] else ''
                d['login_time'] = str(d['login_time']) if d['login_time'] else ''
                d['user_type_str'] = '否' if d['user_type'] == 1 else '是'
                d['time_int'] = public_util.days_int(d['add_time']) * 1000
                d['sh_str'] = '正常用户' if d['sh'] == 0 else '审核用户'
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取用户设备数及ip注册数
def get_ip_num(aaid, register_ip):
    machine_num = 0
    ip_num = 0
    mysql = Mysql()
    try:
        sql = "select count(if(aaid = '%s', TRUE, NULL)) machine_num, count(if(register_ip = '%s', true, null)) ip_num " \
              "from san_users where user_type = 1" % (aaid, register_ip)
        res = mysql.getOne(sql, None)
        if res:
            machine_num = res['machine_num'] if res['machine_num'] else 0
            ip_num = res['ip_num'] if res['ip_num'] else 0
    except Exception as e:
        print(e)
    mysql.dispose()
    return machine_num, ip_num


# 更新订单信息
def update_order_error_msg(oid, msg):
    sql = "update san_withdraw_list set err_msg = %s, status = 6 where id = %s"
    mysql = Mysql()
    try:
        mysql.update(sql, [msg, oid])
    except Exception as e:
        print(e)
    mysql.dispose()


# 提现失败，发送通知
def send_user_email(uid, content):
    info = "Withdraw fail : " + content
    title = 'System notification'
    sql = "insert into san_user_message(uid, title, content, add_time) values (%s, %s, %s, now())"
    mysql = Mysql()
    res = mysql.insertOne(sql, [uid, title, info])
    mysql.dispose()
    return res


# 获取提现支付信息
def get_withdraw_pay(pay_id):
    sql = "select * from san_pay_list where pay_id = '%s' and with_flag = 1" % pay_id
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 更新用户余额
def update_user_money(uid, money):
    sql = "update san_users set money = money + '%s' where uid = '%s'" % (money, uid)
    mysql = Mysql()
    res = mysql.update(sql, None)
    mysql.dispose()
    return res


# 更新用户佣金
def update_user_commission(uid, money):
    sql = "update san_users set commission = commission + '%s' where uid = '%s'" % (money, uid)
    mysql = Mysql()
    res = mysql.update(sql, None)
    mysql.dispose()
    return res


# 获取用户信息
def get_user_detail(uid):
    sql = "select * from san_users where uid = '%s'" % uid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 更新订单状态
def update_withdraw_order_status(oid, status):
    sql = "update san_withdraw_list set status = '%s'" % status
    if status in [2, 5]:
        sql += ", auto_flag = 1"
    sql += " where id = '%s'" % oid
    mysql = Mysql()
    res = mysql.update(sql, None)
    mysql.dispose()
    return res


# 查询用户提现订单
def get_user_orders(oid):
    sql = "select * from san_withdraw_list where id = '%s'" % oid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 获取所有支付
def get_all_pay():
    sql = "select pay_id, pay_name from san_pay_list where status = 1"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


# 获取vip等级数据
def get_vip_lv_list_data():
    Redis_db = Redis()
    vip_lv_list = Redis_db.get(RKEY.SAN_GAME_VIP_LV_LIST)
    Redis_db.close()
    vip_list_data = []
    if vip_lv_list:
        vip_list_data = json.loads(vip_lv_list)
    return vip_list_data
