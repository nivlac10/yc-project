#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022/12/3 11:41
# @Author : 78957
import importlib

from app.game import game
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util
import sys, time

importlib.reload(sys)



# 获取子游戏汇总数据
@game.route('/admin/external_game_total_post', methods=['post'])
@login_required
def external_game_total_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['total'] = []
    try:
        day = time.strftime('%Y-%m-%d')
        stime = request.values.get('stime', day)
        etime = request.values.get('etime', day)
        cid = request.values.get('cid')
        gid = request.values.get('gid')
        game_id = request.values.get('game_id')
        my_game = request.values.get('my_game')
        sort_index = request.values.get('sort_index', 'total_bet')
        sql_list = []
        if cid:
            sql_list.append(" a.cid = '%s'" % cid)
        if gid:
            sql_list.append(" a.gid = '%s'" % gid)
        if game_id:
            sql_list.append(' a.game_id ="%s"' % game_id)
        if my_game:
            sql_list.append(" a.my_game ='%s'" % my_game)
        if stime:
            sql_list.append(" a.day >= '%s'" % stime)
        if etime:
            sql_list.append(" a.day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)

        sql = "select " \
              "sum(if((e.cur_gameid <> 0),1,0)) AS ol_num," \
              "sum(ifnull(a.total_bet,0)) AS total_bet," \
              "sum(ifnull(a.total_shu_ying,0)) AS total_shu_ying," \
              "sum(ifnull(a.total_real_shu_ying,0)) AS total_real_shu_ying," \
              "sum(ifnull(a.total_num,0)) AS total_num," \
              "round((sum(ifnull(a.total_shu_ying,0)) / sum(ifnull(a.total_bet,0))),4) AS gl," \
              "(case when (a.game_id = 55) then 'AWC_GIVE_BONUS' else b.game_name end) AS game_name," \
              "a.cid AS cid,a.day AS day," \
              "a.game_id AS game_id," \
              "a.my_game AS my_game," \
              "a.gid AS gid," \
              "c.game_name AS platform_name," \
              "d.factory_name AS factory_name " \
              "from san_game_wj_day_total a left join san_external_game_list b" \
              " on b.gid = a.gid left join san_game_list c on c.game_id = a.game_id " \
              "left join san_factory_list d on d.factory_id= c.factory_id " \
              "left join san_users e on e.cur_gameid = b.gid  %s  group by a.game_id,a.gid  order by a.%s desc "%(sql_str,sort_index)
        sql2 = "select sum(ifnull(a.total_bet,0)) total_bet,sum(ifnull(a.total_shu_ying,0)) total_shu_ying," \
               "sum(ifnull(a.total_real_shu_ying,0)) total_real_shu_ying,sum(ifnull(a.total_num,0)) total_num ," \
               "round(sum(ifnull(a.total_shu_ying,0))/sum(ifnull(a.total_bet,0)),4) gl,0 ol_num " \
               "from san_game_wj_day_total a %s "%(sql_str)

        mysql = Mysql()
        res = mysql.getAll(sql, None)
        total = mysql.getOne(sql2, None)
        mysql.dispose()
        num = 0
        if res:
            for d in res:
                d['total_num']=str(d['total_num'])
                d['ol_num']=str(d['ol_num'])
                num += int(d['ol_num'])
            total['total_num'] = str(total['total_num'])
            total['ol_num'] = num
            data['data'] = res
            data['total'] = total
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取用户游戏数据
@game.route('/admin/external_game_user_detail_post', methods=['post'])
@login_required
def external_game_user_detail_post():
    data = dict()
    data['code'] = 0
    data['count'] = 0
    data['data'] = []
    try:
        # gid = request.values.get('gid', '')
        cid = request.values.get('cid', '')
        my_game = request.values.get('my_game', '')
        type_flag = int(request.values.get('type_flag'))
        stime = request.values.get('stime', '')
        etime = request.values.get('etime', '')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql_list = []
        if my_game:
            if type_flag == 0:
                sql_game_str = " a.my_game=" + my_game
            elif type_flag == 1:
                sql_game_str = " a.game_id=" + my_game
            else:
                sql_game_str = " a.gid=" + my_game
            sql_list.append(sql_game_str)
        if cid:
            sql_list.append(" a.cid = '%s'" % cid)
        if stime:
            sql_list.append(" a.day >= '%s'" % stime)
        if etime:
            sql_list.append(" a.day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)

        sql = "select b.nickname,ifnull(sum(a.total_bet),0) total_bet," \
              "ifnull(sum(a.total_shu_ying),0) total_shu_ying,ifnull" \
              "(sum(a.total_real_shu_ying),0) real_shu_ying,ifnull" \
              "(sum(a.total_num),0) total_num, ifnull(c.game_name,'')" \
              " game_name, round(ifnull(sum(a.total_shu_ying),0)/ifnull(sum(a.total_bet),0),4) gl," \
              "a.uid,a.game_id,a.gid from san_game_wj_user_day_total a left join san_users b " \
              "on a.uid = b.uid left join san_external_game_list c on c.gid = a.gid %s " \
              "group by a.uid,a.gid order by total_bet desc limit %d, %d" % (sql_str,c_num, limit)

        sql2 = "select count(*) con from (select uid from san_game_wj_user_day_total as a %s group by a.uid,a.gid ) aa"%sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['total_num'] = str(d['total_num'])

            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


    return res


