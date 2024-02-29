#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-03-04
import importlib

from app.user import user
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util, redis
import sys, json

importlib.reload(sys)


# 用户游戏记录
@user.route('/admin/game_log_conf_post',methods=['post'])
@login_required
def game_log_list():
    data=dict()
    game_list = "select game_id, game_name,factory_id from san_game_list "
    factory_list = "select factory_id,factory_name from san_factory_list "
    external_game_list = "select gid,game_name value from san_external_game_list"
    mysql = Mysql()
    data['game_list'] = mysql.getAll(game_list, None)
    data['factory_list'] = mysql.getAll(factory_list, None)
    data['external_game_list'] = mysql.getAll(external_game_list, None)
    mysql.dispose()
    data['channel'] = get_channel_all()
    data['code']=1
    return jsonify(data)


# 获取用户游戏记录数据
@user.route('/admin/user_game_log_list_post', methods=['post'])
@login_required
def game_log_list_post():
    data = {}
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    if True:
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        gid = request.values.get('gid')
        uid = request.values.get('uid')
        cid = request.values.get('cid')
        game_id = request.values.get('game_id')
        my_game = request.values.get('my_game')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql_list = []
        if gid:
            sql_list.append(" a.gid = '%s' " % gid)
        if cid:
            sql_list.append(" a.cid = '%s' " % cid)
        if uid:
            sql_list.append(" (a.uid  like '%%%s%%' or a.nickname like '%%%s%%' or  a.game_number like '%%%s%%') " % (uid,uid,uid))
        if stime:
            sql_list.append(" a.add_time >= '%s' " % stime)
        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append(" a.add_time < '%s' " % e_str)
        if my_game:
            sql_list.append(" a.my_game = '%s' " % my_game)
        if game_id:
            sql_list.append(" a.game_id= '%s' " % game_id)
        sql_str = public_util.data_list_to_str(sql_list)
        sql = "select a.game_number,a.uid,a.nickname,a.game_name,a.game_id,ifnull(a.betting,0) betting,ifnull(a.shu_ying,0) shu_ying,a.real_shu_ying,a.code_size,a.add_time,a.my_game,a.`status` " \
              "from san_game_bet_log as a  %s " \
              "order by a.odd_number desc limit %d, %d" % (sql_str,offset, limit)

        sql2 = "select count(*) con from san_game_bet_log as a  %s "%(sql_str)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:

            for d in res:
                d['add_time'] = str(d['add_time'])
                d['gl'] = round(float(d['betting'])/float(d['shu_ying']),4) if float(d['shu_ying'])>0 else 0
            #     game_type_list = json.loads(redis.get("task_game_type_list")) if redis.get(
            #         "task_game_type_list") else []
            #     for type in game_type_list:
            #         if d['game_type'] == type['type']:
            #             d['game_type'] = type['type_name']
            # print(res)
            data['data'] = res
            data['count'] = int(cont['con'])
        data['code'] = 1
    # except Exception as e:
    #     print(e)
    return jsonify(data)


# 获取用户游戏数据
@user.route('/admin/user_game_log_post', methods=['post'])
@login_required
def user_game_log_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        gid = request.values.get('gid')
        uid = request.values.get('uid')
        cid = request.values.get('cid')
        suid = request.values.get('suid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        # token = request.headers.get('Authorization')
        # admin_uid = redis.hget(token, 'n')
        flags = 1 # if admin_uid == 1 else 0
        sql_list = []
        sql_list.append("a.uid = '%s'" % uid)
        if gid:
            sql_list.append(" a.gid = '%s'" % gid)
        if cid:
            sql_list.append(" a.cid = '%s'" % cid)
        if uid:
            sql_list.append(" (a.uid = '%s' or locate('%s', a.nickname) > 0 or a.odd_number = '%s' or a.game_number = '%s')" % (
                suid, suid, suid, suid))
        if stime:
            sql_list.append(" a.add_time >= '%s'" % stime)
        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append(" a.add_time <= '%s'" % e_str)
        sql_str = public_util.data_list_to_str(sql_list)
        mysql = Mysql()
        sql = "select a.* from san_game_bet_log as a  %s  order by a.odd_number desc limit %d, %d" % (sql_str,offset, limit)
        sql2 = "select count(*) con from san_game_bet_log a %s"%(sql_str)
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                d['flags'] = flags
            data['data'] = res
            data['count'] = int(cont['con'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 用户外接游戏记录
@user.route('/admin/user_one_game_post', methods=['post'])
@login_required
def game_total():
    data = dict()
    data['data'] = []
    data['code'] = 0
    data['total'] = []
    try:
        uid = request.values.get('uid')
        gid = request.values.get('gid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql = "select * from san_game_bet_log where gid = %s and uid = '%s'  order by odd_number desc limit %d, %d" % (gid, uid,offset, limit)

        sql_Sum = "select sum(ifnull(shu_ying,0)) total_win,sum(ifnull(betting,0)) total_bet," \
              "round(sum(ifnull(shu_ying,0))/sum(ifnull(betting,0)),3) rate " \
              "from san_game_bet_log where gid = %s and uid = '%s'" %(gid, uid)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        res_sum = mysql.getAll(sql_Sum, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
            data['total'] = res_sum
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)




# 获取所有apk包
def get_channel_all():
    sql = "select cid, username from san_agent"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res