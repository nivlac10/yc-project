#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022/12/29 22:07
# @Author : 78957
import importlib

from flask import request
from app import util, common,redis
from SqlConntion.MySqlConn import Mysql
import sys, time, requests, json
importlib.reload(sys)
secret_key = 'd9f277be9ab27414e83ecdfa0a2b074c'
merchant = 'starslot'
request_url = 'https://apithkingpay.gcash.cash/api/daifu'


# 发起提现
def http_post_withdraw_data(collection_name, collection_account, pay_type, order_number, money, bank_code, pay_data, vip):
    data = dict()
    data['code'] = 0
    data['is_int'] = 0  # 提现金额是否是int
    data['data'] = dict()
    data['msg'] = 'error'
    data['send_data'] = dict()
    try:
        if str(pay_type) not in ['gcash']:  # 支付类型错误
            return data
        fee = vip['pay_fee']
        fee_ratio = (100 - float(fee)) / 100
        if fee_ratio < 0:
            fee_ratio = 1
        send_money = round(float(money) * fee_ratio, 2)
        maps = dict()
        maps['merchant'] = merchant
        maps['total_amount'] = send_money
        maps['callback_url'] = pay_data['withdraw_conf_url']
        maps['order_id'] = order_number
        maps['bank'] = 'gcash'
        maps['bank_card_name'] = collection_name
        maps['bank_card_account'] = collection_account
        maps['bank_card_remark'] = 'no'
        sign = get_sign(maps)
        maps['sign'] = sign
        print(json.dumps(maps))
        header = dict()
        header['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'
        content = requests.post(request_url, data=maps, headers=header, verify=False, timeout=10)
        content = json.loads(content.text)
        print(content)
        maps['pay_return_data'] = content
        if content['status'] == '1':
            data['code'] = 1
        data['data'] = content
        data['msg'] = content['message']
        data['send_data'] = maps
    except Exception as e:
        print(e)
        data['msg'] = 'Payment request failed'
    return data


# 支付回调
# @api.route('/api/yinhepay_withdraw_notify', methods=['post'])
def yinhepay_withdraw_notify():
    result_str = 'ERROR'
    merchant = request.values.get('merchant')
    order_id = request.values.get('order_id')
    amount = request.values.get('amount')
    status = request.values.get('status')
    message = request.values.get('message')
    sign = request.values.get('sign')
    print(merchant, order_id, amount, status)
    print(message, sign)
    order_data = get_user_withdraw_detail(str(order_id))  # 订单不存在
    if order_data is None:
        return 'SUCCESS'
    if order_data['status'] != 0:
        return 'SUCCESS'
    order_status = 1 if str(status) == '5' else 2
    success_time = time.strftime("%Y-%m-%d %H:%M:%S")
    email_msg = 'check your bank info and re-withdraw sir'  # 给用户发送邮件
    return_msg = str(message)
    res = update_order_info(order_data, str(amount), order_status, success_time, return_msg, email_msg, str(order_id))
    if res > 0:
        result_str = 'SUCCESS'
    return result_str


# 获取签名
def get_sign(data):
    m_list = data.keys()
    m_list = sorted(m_list)
    s_str = ''
    for d in m_list:
        s_str += d + '=' + str(data[d]) + '&'
    s_str += 'key=' + secret_key
    return util.md5(s_str)




# 获取用户提现订单
def get_user_withdraw_detail(order_number):
    sql = "select * from san_withdraw_list where order_number = '%s'" % order_number
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 更新提现订单状态
def update_order_info(order, money, status, success_time, return_msg, file_msg, order_number=''):
    sql = "update san_withdraw_list set status = '%s', amount = '%s', success_time = '%s', notify_time = now()" % \
          (status, money, success_time)
    if order_number:
        sql += ", pay_order_number = '%s'" % order_number
    sql += " where id = '%s'" % order['id']
    mysql = Mysql()
    res = mysql.update(sql, None)
    mysql.dispose()
    if str(status) != '1':
        update_order_error_msg(order['id'], return_msg)
    if res > 0 and status == 2:
        user = get_user_detail(order['uid'])
        if order['money_type'] == 0:
            after_money = float(user['money']) + float(order['money'])
            update_user_money(user['uid'], order['money'], 1)
            common.user_money_log_func(user['uid'], order['money'], user['money'], after_money, 17)
        else:
            update_user_commission(user['uid'], order['money'], 1)  # 更新佣金
            after_money = float(user['commission']) + order['money']
            common.user_commission_log_func(user['uid'], order['money'], user['commission'], after_money, 101)  # 佣金变动记录
            common.user_brokerage_log_func(user['uid'], 0, 0, money, 6)
        send_user_email(order['uid'], file_msg)
    if int(status) == 1:
        update_team_withdraw_data(order)
    return res


# 更新订单信息
def update_order_error_msg(oid, msg):
    sql = "update san_withdraw_list set err_msg = %s where id = %s"
    mysql = Mysql()
    try:
        mysql.update(sql, [msg, oid])
    except Exception as e:
        print(e)
    mysql.dispose()

# 获取用户信息
def get_user_detail(uid):
    sql = "select * from san_users where uid = '%s'" % uid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res

# 更新用户余额
def update_user_money(uid, money, flag):
    if flag == 0:
        sql = "update san_users set money = money - '%s' where uid = '%s'" % (money, uid)
    else:
        sql = "update san_users set money = money + '%s' where uid = '%s'" % (money, uid)
    mysql = Mysql()
    res = mysql.update(sql, None)
    mysql.dispose()
    return res


# 更新用户佣金
def update_user_commission(uid, money, flag):
    if flag == 0:
        sql = "update san_users set commission = commission - '%s' where uid = '%s'" % (money, uid)
    else:
        sql = "update san_users set commission = commission + '%s' where uid = '%s'" % (money, uid)
    print("扣除佣金", sql)
    mysql = Mysql()
    res = mysql.update(sql, None)
    print("扣除佣金", res)
    mysql.dispose()
    return res

# 提现失败，发送通知
def send_user_email(uid, content):
    info = "Withdraw fail : " + content
    title = 'System notification'
    sql = "insert into san_user_message(uid, title, content, add_time) values (%s, %s, %s, now())"
    mysql = Mysql()
    res = mysql.insertOne(sql, [uid, title, info])
    mysql.dispose()
    return res



# 提现成功用户数据及团队数据处理
def update_team_withdraw_data(order):
    user = get_user_detail(order['uid'])
    if user is None:
        return
    mysql = Mysql()
    try:
        day = str(order['add_time'])[:10]
        sql3 = "update san_users set total_withdraw = total_withdraw + '%s' where uid = '%s'" % \
               (order['money'], order['uid'])
        sql4 = "insert into san_user_team_day_report(uid, day, total_withdraw, withdraw_num) values ('%s', " \
               "'%s', '%s', 1) ON DUPLICATE KEY UPDATE total_withdraw = total_withdraw + '%s', " \
               "withdraw_num = withdraw_num + 1" % (order['uid'], day, order['money'], order['money'])
        mysql.update(sql3, None)
        mysql.insertOne(sql4, None)
        if user['parent_id'] > 0:
            team_key = 'slot_pub_team_one_withdraw_' + day
            user_num = 0 if redis.hget(team_key, str(order['uid'])) else 1
            sql_p = "insert into san_user_team_day_report(uid, day, team_one_withdraw, " \
                    "team_one_withdraw_user_num) values ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE " \
                    "team_one_withdraw = team_one_withdraw + '%s', " \
                    "team_one_withdraw_user_num = team_one_withdraw_user_num + '%s'" % \
                    (user['parent_id'], day, order['money'], user_num, order['money'], user_num)
            mysql.insertOne(sql_p, None)
            if user_num == 1:
                redis.hset(team_key, str(order['uid']), '1')
                redis.expire(team_key, 86400 * 3)
        if user['super_id'] > 0:
            team_key = 'slot_pub_team_two_withdraw_' + day
            user_num = 0 if redis.hget(team_key, str(order['uid'])) else 1
            sql_s = "insert into san_user_team_day_report(uid, day, team_two_withdraw, " \
                    "team_two_withdraw_user_num) values ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE " \
                    "team_two_withdraw = team_two_withdraw + '%s', " \
                    "team_two_withdraw_user_num = team_two_withdraw_user_num + '%s'" % \
                    (user['super_id'], day, order['money'], user_num, order['money'], user_num)
            mysql.insertOne(sql_s, None)
            if user_num == 1:
                redis.hset(team_key, str(order['uid']), '1')
                redis.expire(team_key, 86400 * 3)
        if user['super_parent_id'] > 0:
            team_key = 'slot_pub_team_three_withdraw_' + day
            user_num = 0 if redis.hget(team_key, str(order['uid'])) else 1
            sql_ps = "insert into san_user_team_day_report(uid, day, team_three_withdraw, " \
                     "team_three_withdraw_user_num) values ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE " \
                     "team_three_withdraw = team_three_withdraw + '%s', " \
                     "team_three_withdraw_user_num = team_three_withdraw_user_num + '%s'" % \
                     (user['super_parent_id'], day, order['money'], user_num, order['money'], user_num)
            mysql.insertOne(sql_ps, None)
            if user_num == 1:
                redis.hset(team_key, str(order['uid']), '1')
                redis.expire(team_key, 86400 * 3)
    except Exception as e:
        print(e)
        mysql.dispose(2)
        return
    mysql.dispose()