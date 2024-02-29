#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-04-26
import importlib
import sys
import time

from flask import render_template, request, jsonify

from app import public_util
from app.util import login_required
from SqlConntion.MySqlConn import Mysql
from app.game import game

importlib.reload(sys)



# 获取游戏平台数据
@game.route('/admin/game_day_data_post', methods=['post'])
@login_required
def game_day_data_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['total'] = []
    try:
        day = time.strftime('%Y-%m-%d')
        stime = request.values.get('stime', day)
        etime = request.values.get('etime', day)
        cid = request.values.get('cid')
        game_id = request.values.get('game_id')
        sort_index = request.values.get('sort_index')
        sql_list = []
        if game_id:
            sql_list.append(" a.game_id = '%s'" % game_id)
        if cid:
            sql_list.append(" a.cid = '%s'" % cid)
        if stime:
            sql_list.append(" a.day >= '%s'" % stime)
        if etime:
            sql_list.append(" a.day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)

        sql3 = "select sum(IFNULL(a.total_bet,0)) total_bet,sum(IFNULL(a.total_shu_ying,0)) total_shu_ying," \
               "sum(IFNULL(a.total_real_shu_ying,0)) total_real_shu_ying,sum(IFNULL(a.total_num,0)) total_num," \
               "Round(sum(a.total_shu_ying)-sum(a.total_bet),2) sys_num,case when IFNULL(sum(a.total_bet),0)!=0 " \
               "then Round((sum(a.total_bet)+sum(a.total_real_shu_ying))/sum(a.total_bet),4) else 0 end gl," \
               "(SELECT COUNT(cur_gameid)  FROM san_users where san_users.cur_gameid=a.game_id) user_num,b.game_name " \
               "from san_game_day_total a LEFT JOIN san_game_list b ON a.game_id = b.game_id %s  " \
               "group by a.game_id order by a.%s desc " % (sql_str,sort_index)

        sql = "select sum(IFNULL(a.total_bet,0)) total_bet,sum(IFNULL(a.total_shu_ying,0)) total_shu_ying," \
               "sum(IFNULL(a.total_real_shu_ying,0)) total_real_shu_ying,sum(IFNULL(a.total_num,0)) total_num," \
               "Round(sum(a.total_shu_ying)-sum(a.total_bet),2) sys_num,case when IFNULL(sum(a.total_bet),0)!=0 " \
               "then Round((sum(a.total_bet+total_real_shu_ying))/sum(a.total_bet),4) else 0 end gl," \
               "(SELECT COUNT(cur_gameid)  FROM san_users where san_users.cur_gameid=a.game_id) user_num " \
               "from san_game_day_total a %s "%sql_str
        mysql = Mysql()
        list_res = mysql.getAll(sql3, None)
        res = mysql.getOne(sql, None)
        mysql.dispose()
        if list_res:
            num = 0
            gl_num = 0
            for d in list_res:
                d['total_num']=str(d['total_num'])
                num += d['user_num']
                gl_num += d['gl']
            res['gl'] = gl_num
            res['total_num'] = str(res['total_num'])
            res["num"] = num
            data['data'] = list_res
            data['total'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取获取德州扑克平台数据
@game.route('/admin/game_id_data_post', methods=['post'])
@login_required
def game_id_data_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        day = time.strftime('%Y-%m-%d')
        stime = request.values.get('stime', day)
        etime = request.values.get('etime', day)
        sort_index = request.values.get('sort_index')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql_list = []
        sql_list.append(" my_game = 5")
        if stime:
            sql_list.append(" day >= '%s'" % stime)
        if etime:
            sql_list.append(" day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)

        sql = "select day,IFNULL(total_bet,0) total_bet,IFNULL(total_shu_ying,0) total_shu_ying, " \
               "IFNULL(total_real_shu_ying,0) total_real_shu_ying,IFNULL(total_num,0) total_num, " \
               "Round(total_shu_ying-total_bet,2) sys_num,case when IFNULL(total_bet,0)!=0 " \
               "then Round((total_bet+total_real_shu_ying)/total_bet,4) else 0 end gl," \
               "IFNULL(total_real_shu_ying,0)*0.12  give_money " \
               "from san_game_wj_day_total  %s  " \
               "order by %s desc  limit %d, %d " % (sql_str, sort_index, c_num, limit)
        sql2 = "select count(*) con,sum(IFNULL(total_bet,0)) total_bet,sum(IFNULL(total_shu_ying,0)) total_shu_ying, " \
               "sum(IFNULL(total_real_shu_ying,0)) total_real_shu_ying,sum(IFNULL(total_num,0)) total_num, " \
               "sum(Round(total_shu_ying-total_bet,2)) sys_num," \
               "sum(IFNULL(total_real_shu_ying,0)*0.12)  give_money  from san_game_wj_day_total  %s  " % (sql_str)
        mysql = Mysql()
        list_res = mysql.getAll(sql, None)
        con_res = mysql.getOne(sql2, None)
        mysql.dispose()
        if list_res:
            for d in list_res:
                d['day'] = str(d['day'])
                d['total_num'] = str(d['total_num'])
                if d['give_money'] < 0:
                    d['give_money'] = str(d['give_money']/-1)
            data['data'] = list_res

            con_res['total_num'] = str(con_res['total_num'])
            if con_res['give_money'] < 0:
                con_res['give_money'] = str(con_res['give_money'] / -1)
            con_res['gl']=str(round((float(con_res['total_bet'])+float(con_res['total_real_shu_ying']))/float(con_res['total_bet']),4))
            data['count'] = con_res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取在线游戏用户数据
@game.route('/admin/game_user_list_post', methods=['post'])
@login_required
def game_user_list_post():
    data = dict()
    data['code'] = 0
    data['count'] = 0
    data['data'] = []
    try:
        my_game = request.values.get('my_game', '')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        type_flag = int(request.values.get('type_flag'))
        c_num = (int(page) - 1) * int(limit)
        if type_flag == 0:
            str_game = " my_game=" + my_game

        elif type_flag == 1:
            str_game = " game_id=" + my_game
        else:
            str_game = " gid=" + my_game
        sql = "select a.*, b.game_name, c.username cname from san_users a left join san_external_game_list b on " \
              "b.gid = a.cur_gameid left join san_agent c on c.cid = a.cid " \
              "where %s order by a.uid desc limit %d, %d" % (str_game, c_num, limit)

        sql2 = "select count(*) con from san_users left join san_external_game_list on cur_gameid=gid where %s" % str_game
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time']) if d['add_time'] else ''
                d['login_time'] = str(d['login_time']) if d['login_time'] else ''
                d['user_type_str'] = '否' if d['user_type'] == 1 else '是'
                d['sh_str'] = '正常用户' if d['sh'] == 0 else '审核用户'
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 获取用户游戏实际输赢数据
@game.route('/admin/game_user_detail_post', methods=['post'])
@login_required
def game_user_detail_post():
    data = dict()
    data['code'] = 0
    data['count'] = 0
    data['data'] = []
    try:
        gid = request.values.get('gid', '')
        cid = request.values.get('cid', '')
        stime = request.values.get('stime', '')
        etime = request.values.get('etime', '')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        if gid in ['', '0']:
            data['code'] = 0
            return jsonify(data)
        sql_list = []
        if gid:
            sql_list.append("  a.game_id = '%s'" % gid)
        if cid:
            sql_list.append("  a.cid = '%s'" % cid)
        if stime:
            sql_list.append(" a.day >= '%s'" % stime)
        if etime:
            sql_list.append(" a.day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)

        mysql = Mysql()
        sql = "select b.nickname, sum(ifnull(a.total_bet,0)) betting, sum(ifnull(a.total_cover_charge,0)) cover_charge, c.game_name, " \
              "a.uid, sum(ifnull(a.total_real_shu_ying,0)) real_shu_ying, sum(ifnull(a.total_num,0)) num" \
              ",sum(ifnull(a.total_real_shu_ying,0))-sum(ifnull(a.total_cover_charge,0)) sys_num," \
              "(sum(ifnull(a.total_bet,0))+sum(ifnull(a.total_real_shu_ying,0)))/sum(ifnull(a.total_bet,0)) gl, a.game_id from " \
              "san_user_day_game_total a left join san_users b on a.uid = b.uid left join san_game_list c" \
              " on c.game_id = a.game_id %s  group by a.uid order by real_shu_ying desc limit %d, %d"% (sql_str,c_num, limit)

        sql2 = "select count(*) con from (select uid from san_user_day_game_total as a %s group by uid) aa"% (sql_str)
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['num']=str(d['num'])
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)

