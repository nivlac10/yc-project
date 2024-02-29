#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/07/06 10:26
# @Author : 78957
import importlib

from app.game import game
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util, redis
import sys, json
importlib.reload(sys)



# 获取用户列表数据
@game.route('/admin/game_user_info_list_post', methods=['post'])
@login_required
def game_online_user_list_post():
    data = dict()
    data['data'] = []
    data['code'] = 0
    data['count'] = 0
    data['page'] = 1
    try:
        username = request.values.get('username')
        cid = request.values.get('cid')
        min_money = request.values.get('min_money', '10000')
        max_money = request.values.get('max_money')
        game_id = request.values.get('game_id')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql_list = []
        sql_list.append(" a.user_type = 1 and a.user_gm = 0")
        if username:
            sql_list.append(" (a.uid = '%s' or register_ip = '%s' or aaid = '%s' or locate('%s', a.nickname) > 0 or " \
                   "a.phone = '%s')" % (username, username, username, username, username))
        if game_id:
            sql_list.append(" a.cur_gameid = '%s'" % game_id)
        if cid:
            sql_list.append(" a.cid = '%s'" % cid)
        if min_money:
            sql_list.append(" a.total_money >= '%s'" % min_money)
        if max_money:
            sql_list.append(" a.total_money <= '%s'" % max_money)
        sql_str = public_util.data_list_to_str(sql_list)
        mysql = Mysql()

        sql = "select a.*, b.username bname, c.game_name from san_users a left join san_agent b on b.cid = a.cid " \
              "left join san_game_list c on a.cur_gameid = c.game_id   %s " \
              "order by a.cur_gameid desc, a.total_money desc limit %d, %d" % (sql_str,c_num, limit)
        sql2 = "select count(*) con from(select a.* from san_users a   %s ) aa"%sql_str
        print(sql)
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        rule_game = [6, 10, 11]
        rule_list = ['无', '吃', '送']
        rule_key = dict()
        rule_key['6'] = 'san_game_zjh_rule_conf'
        rule_key['10'] = 'san_game_lzzjh_rule_conf'
        rule_key['11'] = 'san_game_ak47zjh_rule_conf'
        if res:
            for d in res:
                d['rule_type'] = 0
                d['rule_money'] = 0
                d['add_time'] = str(d['add_time']) if d['add_time'] else ''
                d['login_time'] = str(d['login_time']) if d['login_time'] else ''
                d['game_name'] = d['game_name'] if d['game_name'] else '未在线'
                if d['cur_gameid'] in rule_game:
                    con = redis.hget(rule_key[str(d['cur_gameid'])], str(d['uid']))
                    print(con)
                    if con:
                        con = json.loads(con)
                        d['rule_type'] = int(con['type'])
                        d['rule_money'] = con['value']
                d['rule_type'] = rule_list[d['rule_type']] + str(d['rule_money']) if d['rule_type'] != 0 else rule_list[d['rule_type']]
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
        data['page'] = page
    except Exception as e:
        print(e)
    return jsonify(data)