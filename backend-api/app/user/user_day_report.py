#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-04-22
import importlib
import sys

from flask import render_template, request, jsonify

from app import public_util
from app.util import login_required
from SqlConntion.MySqlConn import Mysql
from app.user import user

importlib.reload(sys)



# 用户日报表
@user.route('/admin/user_day_report_list_post', methods=['post'])
@login_required
def user_day_report_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        uid = request.values.get('uid')
        limit = int(request.values.get('limit', '20'))
        user_type = request.values.get('user_type', '0')
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql = "select a.*,b.nickname from san_user_team_day_report a left join san_users b " \
                  "on b.uid = a.uid"
        sql2 = "select count(*) con,sum(a.team_one_user_num) team_one_user_num,sum(a.team_two_user_num) team_two_user_num," \
               "sum(a.team_three_user_num) team_three_user_num,sum(a.team_one_recharge) team_one_recharge,sum(a.team_two_recharge) team_two_recharge," \
               "sum(a.team_three_recharge) team_three_recharge,sum(a.team_one_recharge_user_num) team_one_recharge_user_num," \
               "sum(a.team_two_recharge_user_num) team_two_recharge_user_num,sum(a.team_three_recharge_user_num) team_three_recharge_user_num," \
               "sum(a.team_one_withdraw) team_one_withdraw,sum(a.team_two_withdraw) team_two_withdraw,sum(a.team_three_withdraw) team_three_withdraw," \
               "sum(a.team_one_withdraw_user_num) team_one_withdraw_user_num,sum(a.team_two_withdraw_user_num) team_two_withdraw_user_num," \
               "sum(a.team_three_withdraw_user_num) team_three_withdraw_user_num,sum(a.team_one_bet) team_one_bet,sum(a.team_two_bet) team_two_bet," \
               "sum(a.team_three_bet) team_three_bet,sum(a.team_one_win) team_one_win,sum(a.team_two_win) team_two_win,sum(a.team_three_win) team_three_win," \
               "sum(a.team_one_real_win) team_one_real_win,sum(a.team_two_real_win) team_two_real_win,sum(a.team_three_real_win) team_three_real_win," \
               "sum(a.team_one_bet_num) team_one_bet_num,sum(a.team_two_bet_num) team_two_bet_num,sum(a.team_three_bet_num) team_three_bet_num," \
               "sum(a.team_one_bet_user_num) team_one_bet_user_num,sum(a.team_two_bet_user_num) team_two_bet_user_num," \
               "sum(a.team_three_bet_user_num) team_three_bet_user_num,sum(a.team_one_bet_brokerage) team_one_bet_brokerage," \
               "sum(a.team_two_bet_brokerage) team_two_bet_brokerage,sum(a.team_three_bet_brokerage) team_three_bet_brokerage," \
               "sum(a.team_recharge_brokerage) team_recharge_brokerage,sum(a.team_invite_task_brokerage) team_invite_task_brokerage,sum(a.total_bet) total_bet," \
               "sum(a.total_win) total_win,sum(a.total_num) total_num,sum(a.give_money) give_money,sum(a.vip_up) vip_up,sum(a.vip_day) vip_day," \
               "sum(a.vip_week) vip_week,sum(a.vip_month) vip_month,sum(a.first_recharge_give) first_recharge_give, " \
               "sum(a.day_first_recharge_give) day_first_recharge_give,sum(a.system_give) system_give,sum(a.vip_earnings) vip_earnings, " \
               "sum(a.slot_earnings) slot_earnings,sum(a.table_earnings) table_earnings,sum(a.live_earnings) live_earnings,sum(a.fish_earnings) fish_earnings, " \
               "sum(a.total_recharge) total_recharge,sum(a.recharge_num) recharge_num,sum(a.total_withdraw) total_withdraw,sum(a.withdraw_num) withdraw_num " \
               "from san_user_team_day_report a left join san_users b " \
                  "on b.uid = a.uid"
        where_sql = []
        if uid:
            where_sql.append(' (locate("%s", a.uid)>0 or locate("%s", b.nickname)>0) '%(uid,uid))
        if stime:
            where_sql.append(" a.day >= '%s'"%stime)
        if etime:
            where_sql.append(' a.day <= "%s"'%etime)
        where_str = public_util.data_list_to_str(where_sql)
        sql += where_str
        sql2 += where_str
        mysql = Mysql()
        cont = mysql.getOne(sql2, None)
        sort_list = ['day', 'team_one_user_num', 'team_one_recharge_user_num', 'first_recharge_give', 'total_recharge', 'total_bet']
        sql += ' order by %s desc limit %s, %s' % (sort_list[int(user_type)], offset, limit)
        res = mysql.getAll(sql, None)
        mysql.dispose()
        if res:
            for d in res:
                d['day'] = str(d['day'])
            cont['team_one_user_num'] = str(cont['team_one_user_num'])
            cont['team_two_user_num'] = str(cont['team_two_user_num'])
            cont['team_three_user_num'] = str(cont['team_three_user_num'])
            cont['team_one_recharge_user_num'] = str(cont['team_one_recharge_user_num'])
            cont['team_two_recharge_user_num'] = str(cont['team_two_recharge_user_num'])
            cont['team_three_recharge_user_num'] = str(cont['team_three_recharge_user_num'])
            cont['team_one_withdraw_user_num'] = str(cont['team_one_withdraw_user_num'])
            cont['team_two_withdraw_user_num'] = str(cont['team_two_withdraw_user_num'])
            cont['team_three_withdraw_user_num'] = str(cont['team_three_withdraw_user_num'])
            cont['team_one_bet_num'] = str(cont['team_one_bet_num'])
            cont['team_two_bet_num'] = str(cont['team_two_bet_num'])
            cont['team_three_bet_num'] = str(cont['team_three_bet_num'])
            cont['team_one_bet_user_num'] = str(cont['team_one_bet_user_num'])
            cont['team_two_bet_user_num'] = str(cont['team_two_bet_user_num'])
            cont['team_three_bet_user_num'] = str(cont['team_three_bet_user_num'])
            cont['total_num'] = str(cont['total_num'])
            cont['recharge_num'] = str(cont['recharge_num'])
            cont['withdraw_num'] = str(cont['withdraw_num'])
            data['data'] = res
            data['total'] = cont
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
