#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-03-03
import importlib
import json
import re

from . import data_report
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import RKEY, redis, public_util, util_update_redis
import pyotp
import qrcode, base64
from io import BytesIO
import sys, os, time
importlib.reload(sys)


# 获取列表
@data_report.route('/admin/hour_report', methods=['post'])
@login_required
def hour_report():
    data = dict()
    day = request.values.get('day', str(time.strftime("%Y-%m-%d")))
    cid = request.values.get('cid')
    data['recharge'] = []
    data['user_report'] = []
    data['loss_bonus_report'] = []
    data['sign_hour_report'] = []
    data['bet_task_report'] = []
    data['app_hour_report'] = []
    data['table'] = ["0时", "1时", "2时", "3时", "4时", "5时", "6时", "7时", "8时", "9时", "10时", "11时", "12时", "13时",
                     "14时", "15时", "16时", "17时", "18时", "19时", "20时", "21时", "22时", "23时"]
    data['code'] = 0
    try:
        data['recharge'] = order_hour_report(day, cid)
        data['user_report'] = user_hour_report(day, cid)
        data['loss_bonus_report'] = user_loss_bonus_hour_report(day)
        data['sign_hour_report'] = user_sign_hour_report(day)
        data['bet_task_report'] = user_bet_task_hour_report(day)
        data['app_hour_report'] = app_hour_report(day, cid)
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# app时段分析
def app_hour_report(day, cid):
    data = []
    try:
        sql = "select sum( a0 ) b0,SUM( a1 ) b1,SUM( a2 ) b2,SUM( a3 ) b3,SUM( a4 ) b4,SUM( a5 ) b5,SUM( a6 ) b6," \
              "SUM( a7 ) b7,SUM( a8 ) b8,SUM( a9 ) b9,SUM( a10 ) b10,SUM( a11 ) b11,sum( a12 ) b12,SUM( a13 ) b13," \
              "SUM( a14 ) b14,SUM( a15 ) b15,SUM( a16 ) b16,SUM( a17 ) b17,	SUM( a18 ) b18,SUM( a19 ) b19,	" \
              "SUM( a20 ) b20,	SUM( a21 ) b21,	SUM( a22 ) b22,	SUM( a23 ) b23,	sum( o0 ) r0,	SUM( o2 ) r2,	" \
              "SUM( o3 ) r3,	SUM( o4 ) r4,	SUM( o5 ) r5,	SUM( o6 ) r6,	SUM( o7 ) r7,	SUM( o8 ) r8,	" \
              "SUM( o9 ) r9,	SUM( o10 ) r10,	SUM( o11 ) r11,	sum( o12 ) r12,	SUM( o13 ) r13,	SUM( o14 ) r14,	" \
              "SUM( o15 ) r15,	SUM( o16 ) r16,SUM( o17 ) r17,SUM( o18 ) r18,SUM( o19 ) r19,SUM( o20 ) r20,SUM( o21 ) " \
              "r21,SUM( o22 ) r22,SUM( o23 ) r23  from san_user_day_hour_report where day = '%s'" % day
        if cid:
            sql += " and cid = '%s'" % cid
        mysql = Mysql()
        res = mysql.getOne(sql, None)
        mysql.dispose()
        if res:
            sorted_dict = {k: res[k] for k in sorted(res, key=custom_sort_key)}
            for d in sorted_dict:
                sorted_dict[d] = str(sorted_dict[d])
            array1 = []
            array2 = []
            maps1 = dict()
            maps2 = dict()
            # 根据键名的首字母将字典分配到不同的数组中
            for key in sorted_dict:
                if key[0] in ['b']:
                    array1.append(sorted_dict[key])
                elif key[0] in ['r']:
                    array2.append(sorted_dict[key])
            maps1['title'] = "安装人数"
            maps1['arr'] = array1
            maps2['title'] = "apk日活"
            maps2['arr'] = array2
            data.append(maps1)
            data.append(maps2)
    except Exception as e:
        print(e)
    return data


# 充值时段更新
def order_hour_report(day, cid):
    data = []
    try:
        sql = "select sum(b0) b0,SUM(b1) b1,SUM(b2) b2,SUM(b3) b3,SUM(b4) b4,SUM(b5) b5,SUM(b6) b6,SUM(b7) b7,SUM(b8) b8" \
              ",SUM(b9) b9,SUM(b10) b10,SUM(b11) b11,sum(b12) b12,SUM(b13) b13,SUM(b14) b14,SUM(b15) b15,SUM(b16) b16," \
              "SUM(b17) b17,SUM(b18) b18,SUM(b19) b19,SUM(b20) b20,SUM(b21) b21,SUM(b22) b22,SUM(b23) b23," \
              "sum(r0) r0,SUM(r2) r2,SUM(r3) r3,SUM(r4) r4,SUM(r5) r5,SUM(r6) r6,SUM(r7) r7,SUM(r8) r8,SUM(r9) r9," \
              "SUM(r10) r10,SUM(r11) r11,sum(r12) r12,SUM(r13) r13,SUM(r14) r14,SUM(r15) r15,SUM(r16) r16,SUM(r17)" \
              " r17,SUM(r18) r18,SUM(r19) r19,SUM(r20) r20,SUM(r21) r21,SUM(r22) r22,SUM(r23) r23,sum(m0) m0,SUM(m1)" \
              " m1,SUM(m2) m2,SUM(m3) m3,SUM(m4) m4,SUM(m5) m5,SUM(m6) m6,SUM(m7) m7,SUM(m8) m8,SUM(m9) m9,SUM(m10)" \
              " m10,SUM(m11) m11,sum(m12) m12,SUM(m13) m13,SUM(m14) m14,SUM(m15) m15,SUM(m16) m16,SUM(m17) m17,SUM(m18)" \
              " m18,SUM(m19) m19,SUM(m20) m20,SUM(m21) m21,SUM(m22) m22,SUM(m23) m23" \
              " from san_user_day_hour_report where day = '%s'" % day
        if cid:
            sql += " and cid = '%s'" % cid
        mysql = Mysql()
        res = mysql.getOne(sql, None)
        mysql.dispose()
        if res:
            sorted_dict = {k: res[k] for k in sorted(res, key=custom_sort_key)}
            for d in sorted_dict:
                sorted_dict[d] = str(sorted_dict[d])
            array1 = []
            array2 = []
            array3 = []
            maps1 = dict()
            maps2 = dict()
            maps3 = dict()
            # 根据键名的首字母将字典分配到不同的数组中
            for key in sorted_dict:
                if key[0] in ['b']:
                    array1.append(sorted_dict[key])
                elif key[0] in ['m']:
                    array2.append(sorted_dict[key])
                else:
                    array3.append(sorted_dict[key])
            maps1['title'] = "充值笔数"
            maps1['arr'] = array1
            maps2['title'] = "充值金额"
            maps2['arr'] = array2
            maps3['title'] = "充值人数"
            maps3['arr'] = array3
            data.append(maps1)
            data.append(maps2)
            data.append(maps3)
    except Exception as e:
        print(e)
    return data


# 获取列表
def user_hour_report(day, cid):
    data = []
    try:
        sql = "select sum(t0) b0,SUM(t1) b1,SUM(t2) b2,SUM(t3) b3,SUM(t4) b4,SUM(t5) b5,SUM(t6) b6,SUM(t7) b7,SUM(t8) b8" \
              ",SUM(t9) b9,SUM(t10) b10,SUM(t11) b11,sum(t12) b12,SUM(t13) b13,SUM(t14) b14,SUM(t15) b15,SUM(t16) b16," \
              "SUM(t17) b17,SUM(t18) b18,SUM(t19) b19,SUM(t20) b20,SUM(t21) b21,SUM(t22) b22,SUM(t23) b23," \
              "sum(v0) r0,SUM(v2) r2,SUM(v3) r3,SUM(v4) r4,SUM(v5) r5,SUM(v6) r6,SUM(v7) r7,SUM(v8) r8,SUM(v9) r9," \
              "SUM(v10) r10,SUM(v11) r11,sum(v12) r12,SUM(v13) r13,SUM(v14) r14,SUM(v15) r15,SUM(v16) r16,SUM(v17)" \
              " r17,SUM(v18) r18,SUM(v19) r19,SUM(v20) r20,SUM(v21) r21,SUM(v22) r22,SUM(v23) r23" \
              " from san_user_day_hour_report where day = '%s'" % day
        if cid:
            sql += " and cid = '%s'" % cid
        mysql = Mysql()
        res = mysql.getOne(sql, None)
        mysql.dispose()
        if res:
            sorted_dict = {k: res[k] for k in sorted(res, key=custom_sort_key)}
            for d in sorted_dict:
                sorted_dict[d] = str(sorted_dict[d])
            array1 = []
            array2 = []
            maps1 = dict()
            maps2 = dict()
            # 根据键名的首字母将字典分配到不同的数组中
            for key in sorted_dict:
                if key[0] in ['b']:
                    array1.append(sorted_dict[key])
                elif key[0] in ['r']:
                    array2.append(sorted_dict[key])
            maps1['title'] = "活跃人数"
            maps1['arr'] = array1
            maps2['title'] = "注册人数"
            maps2['arr'] = array2
            data.append(maps1)
            data.append(maps2)
    except Exception as e:
        print(e)
    return data



# 获取破产补贴时段分析列表
def user_loss_bonus_hour_report(day):
    data=[]
    try:
        mysql = Mysql()
        sql="SELECT a.hour hour, ifnull(b.count, 0) count,ifnull(b.loss_money,0) loss_money," \
            "ifnull(b.give_money,0) give_money FROM (SELECT 0 hour UNION ALL SELECT 1 hour UNION ALL SELECT 2 hour " \
            "UNION ALL SELECT 3 hour UNION ALL SELECT 4 hour UNION ALL SELECT 5 hour UNION ALL SELECT 6 hour UNION " \
            "ALL SELECT 7 hour UNION ALL SELECT 8 hour UNION ALL SELECT 9 hour UNION ALL SELECT 10 hour UNION ALL " \
            "SELECT 11 hour UNION ALL SELECT 12 hour UNION ALL SELECT 13 hour UNION ALL SELECT 14 hour UNION ALL " \
            "SELECT 15 hour UNION ALL SELECT 16 hour UNION ALL SELECT 17 hour UNION ALL SELECT 18 hour UNION ALL " \
            "SELECT 19 hour UNION ALL SELECT 20 hour UNION ALL SELECT 21 hour UNION ALL SELECT 22 hour UNION ALL " \
            "SELECT 23 hour ) a LEFT JOIN  ( SELECT	 hour(add_time)  hour, " \
            " count(add_time) count,      sum(loss_money) loss_money,      sum(give_money) give_money    " \
            "FROM san_user_loss_money_bonus_log  where day='%s'   GROUP BY day, hour  ) b " \
            "  ON a.hour=b.hour ORDER BY hour"%(day)
        res = mysql.getAll(sql,None)
        mysql.dispose()
        if res:
            number = []
            money = []
            numbers = dict()
            moneys = dict()
            # 根据键名的首字母将字典分配到不同的数组中
            for key in res:
                number.append(key['count'])
                money.append(key['give_money'])
            numbers['title'] = "领取人数"
            numbers['arr'] = number
            moneys['title'] = "领取金额"
            moneys['arr'] = money
            data.append(numbers)
            data.append(moneys)
    except Exception as e:
        print(e)
    return data


# 获取用户签到时段分析列表
def user_sign_hour_report(day):
    data=[]
    try:
        mysql = Mysql()
        sql="SELECT a.hour hour, ifnull(b.count, 0) count,ifnull(b.money,0) money" \
            " FROM (SELECT 0 hour UNION ALL SELECT 1 hour UNION ALL SELECT 2 hour " \
            "UNION ALL SELECT 3 hour UNION ALL SELECT 4 hour UNION ALL SELECT 5 hour UNION ALL SELECT 6 hour UNION " \
            "ALL SELECT 7 hour UNION ALL SELECT 8 hour UNION ALL SELECT 9 hour UNION ALL SELECT 10 hour UNION ALL " \
            "SELECT 11 hour UNION ALL SELECT 12 hour UNION ALL SELECT 13 hour UNION ALL SELECT 14 hour UNION ALL " \
            "SELECT 15 hour UNION ALL SELECT 16 hour UNION ALL SELECT 17 hour UNION ALL SELECT 18 hour UNION ALL " \
            "SELECT 19 hour UNION ALL SELECT 20 hour UNION ALL SELECT 21 hour UNION ALL SELECT 22 hour UNION ALL " \
            "SELECT 23 hour ) a LEFT JOIN  ( SELECT	 hour(add_time)  hour, count(add_time) count,sum(money) money " \
            "FROM san_user_sign_log  where day='%s'   GROUP BY day, hour  ) b " \
            "ON a.hour=b.hour ORDER BY hour"%(day)
        res = mysql.getAll(sql,None)
        mysql.dispose()
        if res:
            number = []
            money = []
            numbers = dict()
            moneys = dict()
            # 根据键名的首字母将字典分配到不同的数组中
            for key in res:
                number.append(key['count'])
                money.append(key['money'])
            numbers['title'] = "领取人数"
            numbers['arr'] = number
            moneys['title'] = "领取金额"
            moneys['arr'] = money
            data.append(numbers)
            data.append(moneys)
    except Exception as e:
        print(e)
    return data

# 获取打码量奖励领取时段分析列表
def user_bet_task_hour_report(day):
    data=[]
    try:
        mysql = Mysql()
        sql="SELECT a.hour hour, ifnull(b.count, 0) count,ifnull(b.money,0) money," \
            "ifnull(b.bet,0) bet FROM (SELECT 0 hour UNION ALL SELECT 1 hour UNION ALL SELECT 2 hour " \
            "UNION ALL SELECT 3 hour UNION ALL SELECT 4 hour UNION ALL SELECT 5 hour UNION ALL SELECT 6 hour UNION " \
            "ALL SELECT 7 hour UNION ALL SELECT 8 hour UNION ALL SELECT 9 hour UNION ALL SELECT 10 hour UNION ALL " \
            "SELECT 11 hour UNION ALL SELECT 12 hour UNION ALL SELECT 13 hour UNION ALL SELECT 14 hour UNION ALL " \
            "SELECT 15 hour UNION ALL SELECT 16 hour UNION ALL SELECT 17 hour UNION ALL SELECT 18 hour UNION ALL " \
            "SELECT 19 hour UNION ALL SELECT 20 hour UNION ALL SELECT 21 hour UNION ALL SELECT 22 hour UNION ALL " \
            "SELECT 23 hour ) a LEFT JOIN  ( SELECT	hour(add_time)  hour, count(add_time) count,sum(money) money," \
            "sum(bet) bet  FROM san_user_bet_day_task_log  where day='%s'   GROUP BY day, hour  ) b " \
            "ON a.hour=b.hour ORDER BY hour"%(day)
        res = mysql.getAll(sql,None)
        mysql.dispose()
        if res:
            number = []
            money = []
            numbers = dict()
            moneys = dict()
            # 根据键名的首字母将字典分配到不同的数组中
            for key in res:
                number.append(key['count'])
                money.append(key['money'])
            numbers['title'] = "领取人数"
            numbers['arr'] = number
            moneys['title'] = "领取金额"
            moneys['arr'] = money
            data.append(numbers)
            data.append(moneys)
    except Exception as e:
        print(e)
    return data


def custom_sort_key(key):
    # 使用正则表达式将键名拆分为字母部分和数字部分
    match = re.match(r"([a-zA-Z]+)(\d+)", key)
    if match:
        letters = match.group(1)
        numbers = int(match.group(2))
        return letters, numbers
    else:
        return key
