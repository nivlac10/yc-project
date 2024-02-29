#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-03-04
import codecs
import importlib
import json
import sys

from flask import request, jsonify

from app import public_util, common, util_update_redis
from app.util import login_required
from SqlConntion.MySqlConn import Mysql
from . import activity

importlib.reload(sys)


# 获取充值活动列表
@activity.route('/admin/recharge_activity_list_post', methods=['post'])
@login_required
def recharge_activity_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        status = request.values.get('status')
        type = request.values.get('type')
        page = request.values.get('page', '1')
        limit = int(request.values.get('limit', '20'))
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        name = request.values.get('name')
        offset = (int(page) - 1) * limit
        sql_list = []
        if status:
            sql_list.append(" status = %s " % status)
        if type:
            sql_list.append(" recharge_activity_type = %s " % type)
        if name:
            sql_list.append(" recharge_activity_name like '%%%s%%' " % (name))
        if stime:
            sql_list.append(" add_time>='%s' " % (stime))
        if etime:
            etime = etime + " 23:59:59"
            sql_list.append(" add_time<='%s' " % (etime))
        sql_str = public_util.data_list_to_str(sql_list)
        sql = "select * from san_recharge_activity_list %s order by recharge_activity_id desc limit %s, %s" \
              "" % (sql_str, offset, limit)
        sql2 = "select count(*) count from san_recharge_activity_list %s" % sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        con = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['start_time'] = str(d['start_time'])
                d['add_time'] = str(d['add_time'])
                d['over_time'] = str(d['over_time'])
                d['ladder_list'] = []
                sql3 = "select * from san_recharge_activity_ladder_list where recharge_activity_id = %s order by id"
                mysql = Mysql()
                ladder = mysql.getAll(sql3, [d['recharge_activity_id']])
                mysql.dispose()
                d['recharge_activity_ladder'] = ""
                if ladder:
                    for i in ladder:
                        d['ladder_list'].append(i)
                    symbol = '%'
                    key = 'send_rate'
                    if i['recharge_amount'] > 0:
                        d['recharge_activity_ladder'] = "充" + str(i['recharge_amount']) + ', 赠送' + str(
                            i[key]) + symbol
                    elif i['min_recharge'] > 0:
                        d['recharge_activity_ladder'] = "充" + str(i['min_recharge']) + '~' + str(
                            i['max_recharge']) + ', 赠送' + str(i[key]) + symbol
                for item in common.RECHARGE_ACTIVITY_CONF:
                    if str(d['recharge_activity_type']) == str(item['type']):
                        d['recharge_activity_type_name'] = item['type_name']
            data['count'] = con['count']
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取充值活动简介列表
@activity.route('/admin/recharge_activity_slogan_post', methods=['post'])
@login_required
def recharge_activity_slogan_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        page = request.values.get('page', '1')
        limit = int(request.values.get('limit', '20'))
        offset = (int(page) - 1) * limit
        sql = "select * from san_recharge_activity_slogan order by sort_index desc limit %s, %s"
        sql2 = "select count(*) count from san_recharge_activity_slogan"
        mysql = Mysql()
        res = mysql.getAll(sql, [offset, limit])
        con = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for item in res:
                item['add_time'] = str(item['add_time'])
            data['count'] = con['count']
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加充值活动简介
@activity.route('/admin/add_slogan_post', methods=['post'])
@login_required
def add_slogan_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '添加失败'
    try:
        info = request.values.get('info')
        sort_index = request.values.get('sort_index')
        sql = "insert  into san_recharge_activity_slogan (info, add_time, sort_index) values (%s, NOW(), %s)"
        mysql = Mysql()
        res = mysql.insertOne(sql, [info, sort_index])
        mysql.dispose()
        if res:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = "添加成功！"
            util_update_redis.san_recharge_activity_slogan()
    except Exception as e:
        print(e)
    return jsonify(data)


# 编辑充值活动简介
@activity.route('/admin/update_slogan_post', methods=['post'])
@login_required
def update_slogan_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '修改失败'
    try:
        id = request.values.get("id")
        info = request.values.get('info')
        sort_index = request.values.get('sort_index')
        sql = "update san_recharge_activity_slogan set info = %s , sort_index = %s where id = %s"
        mysql = Mysql()
        res = mysql.update(sql, [info, sort_index, id])
        mysql.dispose()
        if res:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = "修改成功！"
            util_update_redis.san_recharge_activity_slogan()
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加充值活动
@activity.route('/admin/add_recharge_activity_post', methods=['post'])
@login_required
def add_recharge_activity_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        recharge_activity_name = request.values.get("recharge_activity_name")
        if recharge_activity_name is None or recharge_activity_name == '':
            data['status'] = 0
            data['msg'] = '活动名称不能为空！'
            return jsonify(data)
        recharge_activity_type = request.values.get("recharge_activity_type")
        if recharge_activity_type is None or recharge_activity_type == '':
            data['status'] = 0
            data['msg'] = '活动类型不能为空！'
            return jsonify(data)
        start_time = request.values.get("start_time")
        if start_time is None or start_time == '':
            data['status'] = 0
            data['msg'] = '起始时间不能为空'
            return jsonify(data)
        over_time = request.values.get("over_time")
        if over_time is None or over_time == '':
            data['status'] = 0
            data['msg'] = '结束时间不能为空'
            return jsonify(data)
        status = request.values.get("status")
        if status is None or status == '':
            data['status'] = 0
            data['msg'] = '活动状态不能为空'
            return jsonify(data)
        bet_rate = request.values.get("bet_rate")
        if bet_rate is None or bet_rate == '':
            data['status'] = 0
            data['msg'] = '打码倍率不能为空'
            return jsonify(data)
        ladder_list = request.values.get("ladder_list")
        if ladder_list is None:
            data['status'] = 0
            data['msg'] = '充值阶梯不能为空！'
            return jsonify(data)
        if ladder_list:
            ladder_list = json.loads(ladder_list)
            if len(str(ladder_list)) == 0:
                data['status'] = 0
                data['msg'] = '充值阶梯不能为空！'
                return jsonify(data)
            # 判断是否有相同的数据
            news_ids = []
            for id in ladder_list:
                if id not in news_ids:
                    news_ids.append(id)
            if len(str(news_ids)) != len(str(ladder_list)):
                data['status'] = 0
                data['msg'] = '充值阶梯不能有重复数据！'
                return jsonify(data)
        for i, d in enumerate(ladder_list):
            if float(d['recharge_amount']) <= 0 and float(d['min_recharge']) <= 0 and float(d['max_recharge']) <= 0:
                data['status'] = 0
                data['msg'] = '充值金额不能为0！'
                return jsonify(data)

            if float(d['min_recharge']) == float(d['max_recharge']) and int(recharge_activity_type) != 1 and int(
                    recharge_activity_type) != 3:
                data['status'] = 0
                data['msg'] = '范围阶梯最小充值金额不能与最大充值金额相同！'
                return jsonify(data)
            if float(d['min_recharge']) >= float(d['max_recharge']) and int(recharge_activity_type) != 1 and int(
                    recharge_activity_type) != 3:
                data['status'] = 0
                data['msg'] = '范围阶梯最小充值金额不能大于最大充值金额！'
                return jsonify(data)
            if float(d['send_rate']) <= 0 or d['send_rate'] is None:
                data['status'] = 0
                data['msg'] = '范围阶梯赠送比例不可为零或为空！'
                return jsonify(data)
            if i != 0:
                if float(ladder_list[i - 1]['max_recharge']) >= float(ladder_list[i]['min_recharge']) and int(
                        recharge_activity_type) != 1:
                    data['status'] = 0
                    data['msg'] = '阶梯最小充值金额不可大于或等于上一阶梯最大充值金额！'
                    return jsonify(data)
        sql = "insert into san_recharge_activity_list ( recharge_activity_name," \
              " recharge_activity_type,  start_time, over_time, status, bet_rate,   add_time) values" \
              " ( %s, %s, %s, %s,%s, %s, Now()) "
        mysql = Mysql()
        res = mysql.insertOne(sql,
                              [recharge_activity_name, recharge_activity_type, start_time, over_time, status, bet_rate])
        mysql.dispose()
        if ladder_list:
            for d in ladder_list:
                sql_l = "insert into san_recharge_activity_ladder_list " \
                        "( recharge_activity_id, recharge_activity_type, recharge_amount, " \
                        "min_recharge, max_recharge, send_rate) values " \
                        "(%s, %s, %s, %s, %s, %s)" % (res, recharge_activity_type, d['recharge_amount']
                                                      , d['min_recharge'], d['max_recharge'], d['send_rate'])
                mysql = Mysql()
                res2 = mysql.insertOne(sql_l, None)
                mysql.dispose()
                if res2 > 0:
                    data['status'] = 1
                    data['code'] = 1
        if res > 0:
            util_update_redis.set_recharge_ladder_activity_list()
            util_update_redis.set_recharge_activity_conf()
            data['status'] = 1
            data['code'] = 1
        data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 编辑充值活动
@activity.route('/admin/update_recharge_activity_post', methods=['post'])
@login_required
def update_recharge_activity_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        recharge_activity_id = request.values.get("recharge_activity_id")
        if recharge_activity_id is None or recharge_activity_id == '':
            data['status'] = 0
            data['msg'] = '活动ID不能为空！'
            return jsonify(data)
        recharge_activity_name = request.values.get("recharge_activity_name")
        if recharge_activity_name is None or recharge_activity_name == '':
            data['status'] = 0
            data['msg'] = '活动名称不能为空！'
            return jsonify(data)
        recharge_activity_type = request.values.get("recharge_activity_type")
        if recharge_activity_type is None or recharge_activity_type == '':
            data['status'] = 0
            data['msg'] = '活动类型不能为空！'
            return jsonify(data)
        start_time = request.values.get("start_time")
        if start_time is None or start_time == '':
            data['status'] = 0
            data['msg'] = '起始时间不能为空'
            return jsonify(data)
        over_time = request.values.get("over_time")
        if over_time is None or over_time == '':
            data['status'] = 0
            data['msg'] = '结束时间不能为空'
            return jsonify(data)
        status = request.values.get("status")
        if status is None or status == '':
            data['status'] = 0
            data['msg'] = '活动状态不能为空'
            return jsonify(data)
        bet_rate = request.values.get("bet_rate")
        if bet_rate is None or bet_rate == '':
            data['status'] = 0
            data['msg'] = '打码倍率不能为空'
            return jsonify(data)
        ladder_list = request.values.get("ladder_list")
        if ladder_list is None:
            data['status'] = 0
            data['msg'] = '充值阶梯不能为空！'
            return jsonify(data)
        if ladder_list:
            ladder_list = json.loads(ladder_list)
            if len(ladder_list) == 0:
                data['status'] = 0
                data['msg'] = '充值阶梯不能为空！'
                return jsonify(data)
            # 判断是否有相同的数据
            news_ids = []
            for id in ladder_list:
                if id not in news_ids:
                    news_ids.append(id)
            if len(news_ids) != len(ladder_list):
                data['status'] = 0
                data['msg'] = '充值阶梯不能有重复数据！'
                return jsonify(data)
        for i, d in enumerate(ladder_list):
            if float(d['recharge_amount']) <= 0 and float(d['min_recharge']) <= 0 and float(d['max_recharge']) <= 0:
                data['status'] = 0
                data['msg'] = '充值金额不能为0！'
                return jsonify(data)
            if float(d['min_recharge']) == float(d['max_recharge']) and int(recharge_activity_type) != 1 and int(
                    recharge_activity_type) != 3:
                data['status'] = 0
                data['msg'] = '范围阶梯最小充值金额不能与最大充值金额相同！'
                return jsonify(data)
            if float(d['min_recharge']) >= float(d['max_recharge']) and int(recharge_activity_type) != 1 and int(
                    recharge_activity_type) != 3:
                data['status'] = 0
                data['msg'] = '范围阶梯最小充值金额不能大于最大充值金额！'
                return jsonify(data)
            if float(d['send_rate']) <= 0 or d['send_rate'] is None:
                data['status'] = 0
                data['msg'] = '范围阶梯赠送比例不可为零或为空！'
                return jsonify(data)
            if i != 0:
                if float(ladder_list[i - 1]['max_recharge']) >= float(ladder_list[i]['min_recharge']) and int(
                        recharge_activity_type) != 1:
                    data['status'] = 0
                    data['msg'] = '阶梯最小充值金额不可大于或等于上一阶梯最大充值金额！'
                    return jsonify(data)
        sql = "update  san_recharge_activity_list set recharge_activity_name = %s ,recharge_activity_type = %s " \
              ",start_time = %s ,over_time = %s ,status = %s " \
              ",bet_rate = %s  where recharge_activity_id = %s"
        sql2 = "delete from san_recharge_activity_ladder_list where recharge_activity_id = %s"
        mysql = Mysql()
        res = mysql.update(sql,
                           [recharge_activity_name, recharge_activity_type, start_time, over_time, status, bet_rate,
                            recharge_activity_id])
        res2 = mysql.delete(sql2, [recharge_activity_id])
        mysql.dispose()
        if ladder_list:
            for d in ladder_list:
                sql_l = "insert into san_recharge_activity_ladder_list " \
                        "( recharge_activity_id, recharge_activity_type, recharge_amount, " \
                        "min_recharge, max_recharge, send_rate) values " \
                        "(%s, %s, %s, %s, %s, %s)" % (
                            recharge_activity_id, recharge_activity_type, d['recharge_amount']
                            , d['min_recharge'], d['max_recharge'], d['send_rate'])
                mysql = Mysql()
                res2 = mysql.insertOne(sql_l, None)
                mysql.dispose()
                data['code'] = 1
                data['status'] = 1
            data['msg'] = '操作成功'
        if res2 or res:
            util_update_redis.set_recharge_ladder_activity_list()
            util_update_redis.set_recharge_activity_conf()
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除充值活动
@activity.route('/admin/delete_recharge_activity_post', methods=['post'])
@login_required
def delete_recharge_activity_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        recharge_activity_id = request.values.get("recharge_activity_id")
        sql = "delete from san_recharge_activity_list where recharge_activity_id = %s"
        sql2 = "delete from san_recharge_activity_ladder_list where recharge_activity_id = %s"
        mysql = Mysql()
        res = mysql.delete(sql, [recharge_activity_id])
        res2 = mysql.delete(sql2, [recharge_activity_id])
        mysql.dispose()
        if res2 and res:
            data['status'] = 1
            data['code'] = 1
            data['msg'] = '操作成功'
            util_update_redis.set_recharge_ladder_activity_list()
            util_update_redis.set_recharge_activity_conf()
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除充值简介
@activity.route('/admin/delete_slogan_post', methods=['post'])
@login_required
def delete_slogan_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        id = request.values.get("id")
        sql = "delete from san_recharge_activity_slogan where id = %s"
        mysql = Mysql()
        res = mysql.delete(sql, [id])
        mysql.dispose()
        if res:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
            util_update_redis.san_recharge_activity_slogan()
    except Exception as e:
        print(e)
    return jsonify(data)


# 禁用简介
@activity.route('/admin/update_slogan_status_post', methods=['post'])
@login_required
def update_slogan_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        status = request.values.get('status')
        id = request.values.get('id')
        sql = "update san_recharge_activity_slogan set status = %s where id = %s"
        mysql = Mysql()
        res = mysql.update(sql, [status, id])
        mysql.dispose()
        if res:
            util_update_redis.san_recharge_activity_slogan()
            data['msg'] = "成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取列表邀请任务记录列表
@activity.route('/admin/recharge_activity_log_list_post', methods=['post'])
@login_required
def recharge_activity_log_list_post():
    data = dict()
    data['code'] = 0
    data['total_money'] = 0
    data['count'] = 0
    data['data'] = []
    try:
        page = request.values.get('page', '1')
        limit = request.values.get('limit', '20')
        uid = request.values.get('uid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        recharge_activity_id = request.values.get('recharge_activity_id')
        offset = (int(page) - 1) * int(limit)
        sql_list = []
        if uid:
            uid_list = uid.split(',')
            if (len(uid_list) > 0):
                sql_l_uid = ""
                for d in uid_list:
                    if d:
                        sql_l_uid += " a.uid = '%s' or" % d
                sql_l_uid = sql_l_uid[:-2]
                sql_list.append(sql_l_uid)
            else:
                sql_list.append("  a.uid = '%s'" % uid)
        if recharge_activity_id:
            sql_list.append("  a.recharge_activity_id = '%s'" % recharge_activity_id)
        if stime:
            sql_list.append("  a.add_time >= '%s'" % stime)
        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append("  a.add_time <= '%s'" % e_str)
        sql_str = public_util.data_list_to_str(sql_list)
        sql = "select a.*,su.nickname,srall.recharge_activity_name from san_recharge_activity_log a left join san_users" \
              " su on a.uid = su.uid  left join san_recharge_activity_list srall on a.recharge_activity_id = " \
              "srall.recharge_activity_id %s order by add_time desc limit %s, %s" % (sql_str, offset, limit)
        sql2 = "select count(*) count, sum(send_amount) total_money from san_recharge_activity_log a %s " % sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
            data['total_money'] = float(cont['total_money'])
            data['count'] = int(cont['count'])
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


@activity.route('/admin/recharge_activity_type_list_post', methods=['post'])
@login_required
def recharge_activity_type_list_post():
    data = dict()
    data['code'] = 0
    data['pay_money_list'] = []
    data['type_list'] = []
    try:
        pay_money_list = util_update_redis.get_single_conf("pay_money_list")
        if pay_money_list:
            pay_money_list_str = pay_money_list.split(",")
            pay_money_list = []
            for s in pay_money_list_str:
                pay_money_list.append(int(s))
        data['pay_money_list'] = pay_money_list
        data['type_list'] = common.RECHARGE_ACTIVITY_CONF
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
