# coding=utf-8
import json
import random
import string
import time

from SqlConntion.MySqlConn import Mysql
from . import activity
from flask import render_template, request, jsonify
from app.util import login_required
from app import RKEY, common, util_update_redis, redis, public_util
import sys

import importlib

from ..util_update_redis import set_gift_code

importlib.reload(sys)


# 获取优惠券列表
@activity.route('/admin/give_code_post', methods=['post'])
@login_required
def give_code_post():
    data = dict()
    data['code'] = 0
    try:
        page = request.values.get('page', '1')
        limit = request.values.get('limit', '20')
        offset = (int(page) - 1) * int(limit)
        sql = "select * from san_give_code order by status desc, code_id asc limit %s, %s" % (offset, limit)
        sql2 = "select count(*) count from san_give_code"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            data['count'] = int(cont['count'])
            for item in res:
                item['add_time'] = str(item['add_time'])
                item['end_time'] = item['end_time'] * 1000
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取领取优惠券日志列表
@activity.route('/admin/give_code_log_list_post', methods=['post'])
@login_required
def give_code_log_list_post():
    data = dict()
    data['code'] = 0
    data['total_money'] = 0
    try:
        start_time = request.values.get('start_time')
        end_time = request.values.get('end_time')
        page = request.values.get('page', '1')
        limit = request.values.get('limit', '20')
        code_id = request.values.get('code_id')
        uid = request.values.get('uid')
        cid = request.values.get('cid')
        offset = (int(page) - 1) * int(limit)
        sql_list=[]
        if cid:
            sql_list.append(" a.cid = '%s'" % cid)
        if code_id:
            sql_list.append(" a.code_id = '%s'" % code_id)
        if uid:
            sql_list.append("(b.nickname like '%%%s%%'  or a.uid like '%%%s%%') " % (uid, uid))
        if start_time:
            sql_list.append(" a.add_time >= '%s'" % start_time)
        if end_time:
            sql_list.append(" a.add_time <= '%s'" % str(end_time + ' 23:59:59'))
        sql_str=public_util.data_list_to_str(sql_list)

        sql = "select a.*,b.nickname,c.username from san_give_code_log a left join san_users b on a.uid=b.uid left join san_agent c on a.cid=c.cid %s order by add_time desc, code_id asc limit %s, %s"%(sql_str,offset, limit)
        sql2 = "select count(*) count, sum(a.give_money) total_money from san_give_code_log a left join san_users b on a.uid=b.uid %s" %sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            data['count'] = int(cont['count'])
            data['total_money'] = float(cont['total_money'])
            for item in res:
                item['add_time'] = str(item['add_time'])
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改优惠券状态
@activity.route('/admin/update_give_code_status_post', methods=['post'])
@login_required
def update_give_code_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        status = request.values.get('status')
        code_id = request.values.get('code_id')
        sql = "update san_give_code set status = '%s' where code_id = '%s'" % (status, code_id)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            set_gift_code()
            data['msg'] = "成功！！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 新增礼包处理
@activity.route('/admin/add_gift_post', methods=['post'])
@login_required
def add_gift_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        code_name = request.values.get('code_name')
        code_num = request.values.get('code_num')
        is_recharge = request.values.get('is_recharge')
        is_random = request.values.get('is_random')
        min_money = request.values.get('min_money')
        max_money = request.values.get('max_money')
        fixed_money = request.values.get('fixed_money')
        end_time = request.values.get('end_time')
        code = add_gift_code()
        end_time = public_util.day_int(str(end_time))
        sql = "insert into san_give_code(code_name, code, code_num, is_recharge, " \
              "is_random, min_money, max_money, fixed_money, end_time , add_time) values " \
              "(%s, %s, %s, %s, %s,%s, %s, %s, %s, NOW())"
        parms = [code_name, code, code_num, is_recharge, is_random, min_money, max_money, fixed_money, end_time]
        mysql = Mysql()
        res = mysql.insertOne(sql, parms)
        mysql.dispose()
        if res > 0:
            set_gift_code()
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改公告
@activity.route('/admin/detail_give_code_post', methods=['post'])
@login_required
def detail_give_code_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        code_name = request.values.get('code_name')
        code_num = request.values.get('code_num')
        is_recharge = request.values.get('is_recharge')
        is_random = request.values.get('is_random')
        min_money = request.values.get('min_money')
        max_money = request.values.get('max_money')
        fixed_money = request.values.get('fixed_money')
        end_time = request.values.get("end_time")
        code_id = request.values.get('code_id')
        end_time = public_util.day_int(str(end_time))
        sql = "update  san_give_code set  code_name = %s, code_num = %s, is_recharge = %s, is_random = %s, " \
              "min_money = %s,max_money=%s , fixed_money = %s, end_time= %s where code_id = %s "
        params = [code_name, code_num, is_recharge, is_random, min_money, max_money, fixed_money, end_time, code_id]
        mysql = Mysql()
        res = mysql.update(sql, params)
        mysql.dispose()
        if res:
            set_gift_code()
            data['msg'] = "成功！！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除code
@activity.route('/admin/delete_give_code_post', methods=['post'])
@login_required
def delete_give_code_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        code_id = request.values.get('code_id')
        sql = "delete from san_give_code where code_id = '%s'" % code_id
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res:
            set_gift_code()
            data['msg'] = "成功！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 查询当前礼包名称是否存在
def get_gift_name(code_name):
    sql = "select * from san_give_code where code_name = '%s'" % code_name
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 生成礼包码
def add_gift_code():
    code = ''
    while True:
        if code:
            break
        # new_code = random_gift_code()
        new_code = 'BG' + str(random_gift_code())
        res = get_gift_code(new_code)
        if res is None:
            code = new_code
    return code


# 查询礼包码
def get_gift_code(code):
    sql = "select * from san_give_code where code = '%s'" % code
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


def random_gift_code():
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return ''.join(random.choice(chars) for x in range(6))



