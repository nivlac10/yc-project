# -*- coding: utf-8 - *-
# @Time: 2023/2/16
# @Author:Jack c

# ================================ vip等级列表========================
from . import activity
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import  util_update_redis
import sys

import importlib

importlib.reload(sys)


# VIPhtml界面
@activity.route('/admin/vip_lv_list', methods=['POST'])
@login_required
def admin_vip_lv_list():
        data = dict()
        data['code'] = 0
        data['data'] = []
        try:
            sql = "select * from san_vip_lv_list order by vip_id asc "
            mysql = Mysql()
            res = mysql.getAll(sql, None)
            mysql.dispose()
            if res:
                data['data'] = res
            data['code'] = 1
        except Exception as e:
            print(e)
        return jsonify(data)


# VIP等级打码奖励列表
@activity.route('/admin/vip_lv_low_list', methods=['POST'])
@login_required
def vip_lv_low_list():
        data = dict()
        data['code'] = 0
        data['data'] = []
        try:
            vip_lv=request.values.get('vip_lv')
            where=''
            if vip_lv:
                where = "where vip_lv = '%s'"%vip_lv
            sql = "select * from san_vip_low_vip_list %s order by id asc "%where
            mysql = Mysql()
            res = mysql.getAll(sql, None)
            mysql.dispose()
            if res:
                data['data'] = res
            data['code'] = 1
        except Exception as e:
            print(e)
        return jsonify(data)


# 编辑VIP
@activity.route('/admin/edit_vip_lv', methods=['POST'])
@login_required
def admin_edit_vip_lv():
        data = dict()
        data['code'] = 0
        data['status'] = 0
        data['msg'] = '修改失败!'
        try:
            key_list = ['vip_lv', 'recharge', 'bet', 'withdraw_num', 'max_withdraw', 'pay_fee',
                        'day_max_withdraw', 'lv_reward_split_day','lv_reward_now_rate','lv_reward_split_rate',
                        'bet_bonus_rate','bet_bonus_rate','bet_bonus_split_day','bet_bonus_now_rate',
                        'bet_bonus_split_rate','bet_bonus_save_time','day_bet_bonus_rate','day_bet_bonus_split_day',
                        'day_bet_bonus_now_rate','day_bet_bonus_split_rate','day_bet_bonus_save_time',
                        'week_bet_bonus_rate','week_bet_bonus_split_day','week_bet_bonus_now_rate','week_bet_bonus_split_rate',
                        'week_bet_bonus_save_time','month_bet_bonus_rate','month_bet_bonus_split_day','month_bet_bonus_now_rate',
                        'month_bet_bonus_split_rate','month_bet_bonus_save_time','slot', 'table', 'live',
                        'fish', 'day_bonus', 'week_bonus','month_bonus', 'vip_id']
            maps = dict()
            for d in key_list:
                maps[d] = request.values.get(d)
            sql = "update san_vip_lv_list set "
            params = []
            key_list_len = len(key_list) - 1
            for k in range(key_list_len):
                if key_list[k] == "table":
                    sql += "`table` = %s,"
                else:
                    sql += key_list[k] + " = %s,"
                params.append(maps[key_list[k]])
            params.append(maps[key_list[key_list_len]])
            sql = sql[:-1]
            sql += " where vip_id=%s"
            mysql = Mysql()
            res = mysql.update(sql, params)
            mysql.dispose()
            if res:
                util_update_redis.save_vip_lv_to_redis()
                data['status'] = 1
                data['msg'] = '修改成功！'
                data['code'] = 1
        except Exception as e:
            print(e)
        return jsonify(data)

# 编辑VIP
@activity.route('/admin/edit_vip_lv_low', methods=['POST'])
@login_required
def edit_vip_lv_low():
        data = dict()
        data['code'] = 0
        data['status'] = 0
        data['msg'] = '修改失败!'
        try:
            key_list = ['vip_lv', 'lv', 'bonus', 'need_code_amount','id']
            maps = dict()
            for d in key_list:
                maps[d] = request.values.get(d)
            sql = "update san_vip_low_vip_list set "
            params = []
            key_list_len = len(key_list) - 1
            for k in range(key_list_len):
                if key_list[k] == "table":
                    sql += "`table` = %s,"
                else:
                    sql += key_list[k] + " = %s,"
                params.append(maps[key_list[k]])
            params.append(maps[key_list[key_list_len]])
            sql = sql[:-1]
            sql += " where id=%s"
            mysql = Mysql()
            res = mysql.update(sql, params)
            mysql.dispose()
            if res:
                util_update_redis.save_vip_lv_to_redis()
                data['status'] = 1
                data['msg'] = '修改成功！'
                data['code'] = 1
        except Exception as e:
            print(e)
        return jsonify(data)
