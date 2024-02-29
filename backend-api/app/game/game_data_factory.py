#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022/12/3 11:41
# @Author : 78957
import importlib

from app.game import game
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util
import sys, time

importlib.reload(sys)



# 获取集成商汇总数据
@game.route('/admin/factory_game_total_post', methods=['post'])
@login_required
def factory_game_total_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['total'] = []
    try:
        day = time.strftime('%Y-%m-%d')
        stime = request.values.get('stime', day)
        etime = request.values.get('etime', day)
        cid = request.values.get('cid')

        sql_list = []
        if cid:
            sql_list.append("  a.cid = '%s'" % cid)
        if stime:
            sql_list.append("  a.day >= '%s'" % stime)
        if etime:
            sql_list.append("  a.day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)

        sql = "select b.factory_name,ifnull(sum(a.total_bet),0) total_bet,ifnull(sum(a.total_shu_ying),0) total_shu_ying," \
              "ifnull(sum(a.total_real_shu_ying),0) total_real_shu_ying,ifnull(sum(a.total_num),0) total_num ," \
              "round(ifnull(sum(a.total_shu_ying),0)/ifnull(sum(a.total_bet),0),4) gl,ifnull((SELECT  COUNT(u.cur_gameid) " \
              "num  FROM san_users u LEFT JOIN san_external_game_list as ea on ea.gid = u.cur_gameid WHERE" \
              " u.cur_gameid > 0 and ea.my_game=a.my_game GROUP BY ea.my_game),0) ol_num from san_game_wj_day_total a " \
              "left join san_factory_list b on a.my_game = b.factory_id  %s group by a.my_game"%sql_str

        sql2 = "select ifnull(sum(a.total_bet),0) total_bet,ifnull(sum(a.total_shu_ying),0) total_shu_ying," \
               "ifnull(sum(a.total_real_shu_ying),0) total_real_shu_ying,ifnull(sum(a.total_num),0) total_num ," \
               "round(ifnull(sum(a.total_shu_ying),0)/ifnull(sum(a.total_bet),0),4) gl,0 ol_num " \
               "from san_game_wj_day_total a %s"%sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        total = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            num = 0
            for d in res:
                d['total_num'] = str(d['total_num'])
                num += d['ol_num']
            total['total_num'] = str(total['total_num'])
            total['ol_num'] = num
            data['data'] = res
            data['total']=total
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


