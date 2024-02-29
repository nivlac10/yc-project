#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-04-26
import importlib

from . import data_report
from flask import render_template, request, jsonify, make_response
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util
import sys, time

importlib.reload(sys)


# 获取每日数据
@data_report.route('/admin/day_data_list_post', methods=['post'])
@login_required
def day_data_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total'] = dict()
    data['total']['recharge_money'] = 0
    data['total']['withdraw_money'] = 0
    data['total']['total_bet'] = 0
    data['total']['total_real_shu_ying'] = 0
    data['total']['total_give_money'] = 0
    data['total']['total_cover_charge'] = 0
    data['total']['win'] = 0
    data['total']['new_user_recharge'] = 0
    data['total']['new_user_num'] = 0
    data['total']['old_user_recharge'] = 0
    data['total']['old_user_num'] = 0
    data['total']['b_num'] = 0
    data['total']['user_num'] = 0
    data['total']['game_num'] = 0
    data['total']['new_game_num'] = 0
    data['total']['old_game_num'] = 0
    data['total']['result_num'] = 0
    data['total']['rw'] = 0
    data['total']['r_num'] = 0
    data['total']['pj_money'] = 0
    data['total']['recharge_ratio'] = 0
    data['total']['xk_pj_money'] = 0
    data['total']['lk_pj_money'] = 0
    data['total']['install_num'] = 0
    data['total']['num'] = 0
    data['total']['re_user_num'] = 0
    data['total']['total_up'] = 0  # 总up值
    data['total']['new_up'] = 0  # 新客up值
    data['total']['old_up'] = 0  # 老客up值
    data['total']['old_user_life'] = 0  # 老客进入大厅日活
    data['total']['total_user_life'] = 0  # 总用户日活(注册数+老客日活)
    data['total']['register_ratio'] = 0  # 注册率
    data['total']['new_user_withdraw_num'] = 0  # 新客提现人数
    data['total']['old_user_withdraw_num'] = 0  # 老客提现人数
    data['total']['total_user_withdraw_num'] = 0  # 提现总人数
    data['total']['new_user_withdraw'] = 0  # 新客提现金额
    data['total']['old_user_withdraw'] = 0  # 老客提现金额
    data['total']['new_r_w'] = 0  # 新用户充提差
    data['total']['old_r_w'] = 0  # 老用户充提差
    data['total']['new_w_ratio'] = 0  # 新用户提现率
    data['total']['old_w_ratio'] = 0  # 老用户提现率
    data['total']['total_w_ratio'] = 0  # 整体提现率
    data['total']['recharge_fee'] = 0  # 充值手续费
    data['total']['withdraw_fee'] = 0  # 提现手续费
    data['total']['vip_up'] = 0
    data['total']['vip_week'] = 0
    data['total']['vip_month'] = 0
    data['total']['user_rebate'] = 0
    data['total']['user_first_recharge'] = 0
    data['total']['user_day_first_recharge'] = 0
    data['total']['system_give'] = 0
    data['total']['total_brokerage_money'] = 0
    data['total']['first_recharge_brokerage'] = 0
    data['total']['invite_task_brokerage'] = 0
    data['total']['one_bet_brokerage'] = 0
    data['total']['two_bet_brokerage'] = 0
    data['total']['three_bet_brokerage'] = 0
    try:
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        cid = request.values.get('cid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql = "select a.day, sum(a.recharge_money) as recharge_money, " \
              "sum(a.withdraw_money) as withdraw_money, sum(a.total_bet) as " \
              "total_bet, sum(a.total_real_shu_ying) as total_real_shu_ying, sum(a.tem_num) b_num, " \
              "sum(a.game_num) as game_num, sum(a.new_user_recharge) as new_user_recharge, sum(a.num) num, " \
              "sum(a.user_num) re_user_num, sum(a.new_user_num) new_user_num," \
              " sum(a.old_user_recharge) old_user_recharge, " \
              "sum(a.old_user_num) old_user_num, sum(a.new_game_num) new_game_num, sum(a.old_game_num) old_game_num, " \
              "sum(a.result_num) result_num, sum(phone_num + face_num + email_num) user_num, sum(a.total_give_money) " \
              "total_give_money, sum(a.total_cover_charge) total_cover_charge, sum(a.install_num) install_num, " \
              "sum(a.old_user_life) old_user_life, sum(a.recharge_fee) recharge_fee, sum(a.withdraw_fee) withdraw_fee," \
              "sum(a.new_user_withdraw_num) new_user_withdraw_num, sum(a.old_user_withdraw_num) old_user_withdraw_num, " \
              "sum(a.new_user_withdraw) new_user_withdraw, sum(a.old_user_withdraw) old_user_withdraw ," \
              "sum(a.vip_up) as vip_up,sum(a.vip_week) vip_week,sum(a.vip_month) vip_month," \
              "sum(a.user_rebate) user_rebate," \
              "sum(a.user_first_recharge) user_first_recharge,sum(a.user_day_first_recharge) user_day_first_recharge," \
              "sum(a.system_give) system_give," \
              "sum(a.first_recharge_brokerage) first_recharge_brokerage," \
              "sum(invite_task_brokerage) invite_task_brokerage," \
              "sum(a.one_bet_brokerage) one_bet_brokerage,sum(a.two_bet_brokerage) two_bet_brokerage," \
              "sum(a.three_bet_brokerage) three_bet_brokerage from " \
              "san_day_money_total a "
        sql2 = "select count(*) con from "
        sql3 = "select sum(a.recharge_money) recharge_money, sum(a.withdraw_money) withdraw_money, sum(a.total_bet) " \
               "total_bet,  sum(a.total_real_shu_ying) total_real_shu_ying, sum(a.tem_num) b_num, " \
               "sum(a.game_num) game_num, sum(a.new_user_recharge) new_user_recharge, sum(a.num) num, " \
               "sum(a.user_num) re_user_num, sum(a.new_user_num) new_user_num," \
               " sum(a.old_user_recharge) old_user_recharge, " \
               "sum(a.old_user_num) old_user_num, sum(a.new_game_num) new_game_num, sum(a.old_game_num) old_game_num, " \
               "sum(a.result_num) result_num, sum(phone_num+face_num+email_num) user_num, sum(a.total_give_money) " \
               "total_give_money, sum(a.total_cover_charge) total_cover_charge, sum(a.install_num) install_num, " \
               "sum(a.old_user_life) old_user_life, sum(a.recharge_fee) recharge_fee, sum(a.withdraw_fee) withdraw_fee," \
               "sum(a.new_user_withdraw_num) new_user_withdraw_num," \
               " sum(a.old_user_withdraw_num) old_user_withdraw_num, " \
               "sum(a.new_user_withdraw) new_user_withdraw, sum(a.old_user_withdraw) old_user_withdraw," \
               "sum(a.vip_up) as vip_up,sum(a.vip_week) vip_week,sum(a.vip_month) vip_month," \
               "sum(a.user_rebate) user_rebate," \
               "sum(a.user_first_recharge) user_first_recharge,sum(a.user_day_first_recharge) user_day_first_recharge," \
               "sum(a.system_give) system_give," \
               "sum(a.first_recharge_brokerage) first_recharge_brokerage," \
               "sum(invite_task_brokerage) invite_task_brokerage," \
               "sum(a.one_bet_brokerage) one_bet_brokerage,sum(a.two_bet_brokerage) two_bet_brokerage," \
               "sum(a.three_bet_brokerage) three_bet_brokerage from " \
               "san_day_money_total a "
        sql2 += "(select day, sum(recharge_money) recharge_money from san_day_money_total as a "
        sql_list = []
        if cid:
            sql_list.append(" a.cid = '%s'" % cid)
        if stime:
            sql_list.append("  a.day >= '%s'" % stime)
        if etime:
            sql_list.append("  a.day <= '%s'" % etime)
        if len(sql_list) > 0:
            if len(sql_list) > 1:
                sql_str = " where " + "and".join(sql_list)
            else:
                sql_str = " where " + sql_list[0]
            sql += sql_str
            sql2 += sql_str
            sql3 += sql_str
        sql += " group by a.day order by a.day desc, a.total_bet desc limit %d, %d" % (c_num, limit)
        sql2 += " group by day order by day desc limit 100000) aa "
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        total = mysql.getOne(sql3, None)
        mysql.dispose()
        if res:
            for d in res:
                d['day'] = str(d['day'])
                d['recharge_money'] = str(d['recharge_money']) if d['recharge_money'] else 0
                d['withdraw_money'] = str(d['withdraw_money']) if d['withdraw_money'] else 0
                d['total_bet'] = str(d['total_bet']) if d['total_bet'] else 0
                d['total_real_shu_ying'] = str(d['total_real_shu_ying']) if d['total_real_shu_ying'] else 0
                d['total_give_money'] = str(d['total_give_money']) if d['total_give_money'] else 0
                d['total_cover_charge'] = str(d['total_cover_charge']) if d['total_cover_charge'] else 0
                d['win'] = float(d['total_bet']) + float(d['total_real_shu_ying']) + float(d['total_cover_charge'])
                d['win'] = round(d['win'], 2)
                d['new_user_recharge'] = str(d['new_user_recharge']) if d['new_user_recharge'] else 0
                d['new_user_num'] = str(d['new_user_num']) if d['new_user_num'] else 0
                d['old_user_recharge'] = str(d['old_user_recharge']) if d['old_user_recharge'] else 0
                d['old_user_num'] = str(d['old_user_num']) if d['old_user_num'] else 0
                d['new_game_num'] = str(d['new_game_num']) if d['new_game_num'] else 0
                d['old_game_num'] = str(d['old_game_num']) if d['old_game_num'] else 0
                d['result_num'] = str(d['result_num']) if d['result_num'] else 0
                d['b_num'] = str(d['b_num']) if d['b_num'] else 0
                d['user_num'] = str(d['user_num']) if d['user_num'] else 0
                d['game_num'] = str(d['game_num']) if d['game_num'] else 0
                d['total_brokerage_money'] = float(d['first_recharge_brokerage']) + float(d['one_bet_brokerage']) + \
                                             float(d['two_bet_brokerage']) + float(d['three_bet_brokerage']) + \
                                             float(d['invite_task_brokerage'])
                d['total_brokerage_money'] = round(d['total_brokerage_money'], 2)
                d['new_user_ratio'] = round(float(d['new_user_num']) / float(d['user_num']) * 100, 2) if float(
                    d['user_num']) > 0 else 0
                d['new_user_ratio'] = str(d['new_user_ratio']) + '%' if d['new_user_ratio'] != 0 else 0
                d['rw'] = round(float(d['recharge_money']) - float(d['withdraw_money']), 2)  # 总充值减去提现
                d['r_num'] = float(d['new_user_num']) + float(d['old_user_num'])  # 总充值人数
                d['pj_money'] = round(float(d['recharge_money']) / float(d['r_num'])) if d['r_num'] > 0 else 0  # 平均充值
                d['xk_pj_money'] = round(float(d['new_user_recharge']) / float(d['new_user_num']), 2) if float(
                    d['new_user_num']) > 0 else 0  # 新客平均充值
                d['lk_pj_money'] = round(float(d['old_user_recharge']) / float(d['old_user_num']), 2) if float(
                    d['old_user_num']) > 0 else 0  # 老客平均充值
                d['install_num'] = str(d['install_num']) if d['install_num'] else 0
                d['num'] = str(d['num']) if d['num'] else 0
                d['re_user_num'] = str(d['re_user_num']) if d['re_user_num'] else 0

                d['old_user_life'] = str(d['old_user_life']) if d['old_user_life'] else 0  # 老客日活
                d['total_user_life'] = float(d['user_num']) + float(d['old_user_life'])  # 用户总日活
                d['recharge_ratio'] = round(float(d['r_num']) / float(d['total_user_life']) * 100, 2) if float(
                    d['total_user_life']) > 0 else 0  # 充值率
                d['recharge_ratio'] = str(d['recharge_ratio']) + '%' if d['recharge_ratio'] != 0 else 0
                d['total_up'] = round(float(d['recharge_money']) / float(d['total_user_life']), 2) if float(
                    d['total_user_life']) > 0 else 0  # 活跃ARPU
                d['new_up'] = round(float(d['new_user_recharge']) / float(d['user_num']), 2) if float(
                    d['user_num']) > 0 else 0  # 新客up值
                d['old_up'] = round(float(d['old_user_recharge']) / float(d['old_user_life']), 2) if float(
                    d['old_user_life']) > 0 else 0  # 老客up值
                d['register_ratio'] = round(float(d['user_num']) / float(d['install_num']) * 100, 2) if float(
                    d['install_num']) > 0 else 0  # 安装率
                d['register_ratio'] = str(d['register_ratio']) + '%' if d['register_ratio'] != 0 else 0
                d['old_user_ratio'] = round(float(d['old_user_num']) / float(d['old_user_life']) * 100, 2) if float(
                    d['old_user_life']) > 0 else 0
                d['old_user_ratio'] = str(d['old_user_ratio']) + '%' if d['old_user_ratio'] != 0 else 0
                d['new_user_withdraw_num'] = str(d['new_user_withdraw_num']) if d[
                    'new_user_withdraw_num'] else 0  # 新客提现人数
                d['old_user_withdraw_num'] = str(d['old_user_withdraw_num']) if d[
                    'old_user_withdraw_num'] else 0  # 老客提现人数
                d['total_user_withdraw_num'] = float(d['new_user_withdraw_num']) + float(
                    d['old_user_withdraw_num'])  # 总提现人数
                d['new_user_withdraw'] = str(d['new_user_withdraw']) if d['new_user_withdraw'] else 0  # 新客提现金额
                d['old_user_withdraw'] = str(d['old_user_withdraw']) if d['old_user_withdraw'] else 0  # 老客提现金额
                d['new_r_w'] = float(d['new_user_recharge']) - float(d['new_user_withdraw'])  # 新用户充提差
                d['old_r_w'] = float(d['old_user_recharge']) - float(d['old_user_withdraw'])  # 老用户充提差
                d['new_w_ratio'] = round(float(d['new_user_withdraw']) / float(d['new_user_recharge']) * 100,
                                         2) if float(d['new_user_recharge']) > 0 else 0  # 新用户提现率
                d['old_w_ratio'] = round(float(d['old_user_withdraw']) / float(d['old_user_recharge']) * 100,
                                         2) if float(d['old_user_recharge']) > 0 else 0  # 老用户提现率
                d['total_w_ratio'] = round(float(d['withdraw_money']) / float(d['recharge_money']) * 100, 2) if float(
                    d['recharge_money']) > 0 else 0  # 总提现率
                d['new_w_ratio'] = str(d['new_w_ratio']) + '%' if d['new_w_ratio'] != 0 else 0
                d['old_w_ratio'] = str(d['old_w_ratio']) + '%' if d['old_w_ratio'] != 0 else 0
                d['total_w_ratio'] = str(d['total_w_ratio']) + '%' if d['total_w_ratio'] != 0 else 0
                d['withdraw_fee'] = str(d['withdraw_fee']) if d['withdraw_fee'] else 0
                d['recharge_fee'] = str(d['recharge_fee']) if d['recharge_fee'] else 0
            data['total']['recharge_money'] = str(total['recharge_money']) if total['recharge_money'] else 0
            data['total']['withdraw_money'] = str(total['withdraw_money']) if total['withdraw_money'] else 0
            data['total']['total_bet'] = str(total['total_bet']) if total['total_bet'] else 0
            data['total']['total_real_shu_ying'] = str(total['total_real_shu_ying']) if total[
                'total_real_shu_ying'] else 0
            data['total']['total_give_money'] = str(total['total_give_money']) if total['total_give_money'] else 0
            data['total']['total_cover_charge'] = str(total['total_cover_charge']) if total['total_cover_charge'] else 0
            data['total']['win'] = float(data['total']['total_bet']) + float(
                data['total']['total_real_shu_ying']) + float(data['total']['total_cover_charge'])
            data['total']['win'] = round(data['total']['win'], 2)
            data['total']['new_user_recharge'] = str(total['new_user_recharge']) if total['new_user_recharge'] else 0
            data['total']['new_user_num'] = str(total['new_user_num']) if total['new_user_num'] else 0
            data['total']['old_user_recharge'] = str(total['old_user_recharge']) if total['old_user_recharge'] else 0
            data['total']['old_user_num'] = str(total['old_user_num']) if total['old_user_num'] else 0
            data['total']['b_num'] = str(total['b_num']) if total['b_num'] else 0
            data['total']['user_num'] = str(total['user_num']) if total['user_num'] else 0
            data['total']['game_num'] = str(total['game_num']) if total['game_num'] else 0
            data['total']['new_game_num'] = str(total['new_game_num']) if total['new_game_num'] else 0
            data['total']['old_game_num'] = str(total['old_game_num']) if total['old_game_num'] else 0
            data['total']['result_num'] = str(total['result_num']) if total['result_num'] else 0
            data['total']['new_user_ratio'] = round(
                float(data['total']['new_user_num']) / float(data['total']['user_num']) * 100, 2) if float(
                data['total']['user_num']) > 0 else 0
            data['total']['new_user_ratio'] = str(data['total']['new_user_ratio']) + '%' if data['total'][
                                                                                                'new_user_ratio'] != 0 else 0
            data['total']['rw'] = round(float(data['total']['recharge_money']) - float(data['total']['withdraw_money']),
                                        2)  # 总充值减去提现
            data['total']['r_num'] = float(data['total']['new_user_num']) + float(
                data['total']['old_user_num'])  # 总充值人数
            data['total']['pj_money'] = round(float(data['total']['recharge_money']) / float(data['total']['r_num'])) if \
                data['total']['r_num'] > 0 else 0  # 平均充值
            data['total']['xk_pj_money'] = round(
                float(data['total']['new_user_recharge']) / float(data['total']['new_user_num']), 2) if float(
                data['total']['new_user_num']) > 0 else 0  # 新客平均充值
            data['total']['lk_pj_money'] = round(
                float(data['total']['old_user_recharge']) / float(data['total']['old_user_num']), 2) if float(
                data['total']['old_user_num']) > 0 else 0  # 老客平均充值
            data['total']['install_num'] = str(total['install_num']) if total['install_num'] else 0
            data['total']['num'] = str(total['num']) if total['num'] else 0
            data['total']['re_user_num'] = str(total['re_user_num']) if total['re_user_num'] else 0
            data['total']['old_user_life'] = str(total['old_user_life']) if total['old_user_life'] else 0  # 老客日活
            data['total']['total_user_life'] = float(data['total']['user_num']) + float(
                data['total']['old_user_life'])  # 总用户日活
            data['total']['recharge_ratio'] = round(
                float(data['total']['r_num']) / float(data['total']['total_user_life']) * 100, 2) if float(
                data['total']['total_user_life']) > 0 else 0  # 充值率
            data['total']['recharge_ratio'] = str(data['total']['recharge_ratio']) + '%' if data['total'][
                                                                                                'recharge_ratio'] != 0 else 0
            data['total']['total_up'] = round(
                float(data['total']['recharge_money']) / float(data['total']['total_user_life']), 2) if float(
                data['total']['total_user_life']) > 0 else 0  # 总up值
            data['total']['new_up'] = round(
                float(data['total']['new_user_recharge']) / float(data['total']['user_num']), 2) if float(
                data['total']['user_num']) > 0 else 0  # 新客up值
            data['total']['old_up'] = round(
                float(data['total']['old_user_recharge']) / float(data['total']['old_user_life']), 2) if float(
                data['total']['old_user_life']) > 0 else 0  # 老客up值
            data['total']['register_ratio'] = round(
                float(data['total']['user_num']) / float(data['total']['install_num']) * 100, 2) if float(
                data['total']['install_num']) > 0 else 0  # 注册率
            data['total']['register_ratio'] = str(data['total']['register_ratio']) + '%' if data['total'][
                                                                                                'register_ratio'] != 0 else 0
            data['total']['old_user_ratio'] = round(
                float(data['total']['old_user_num']) / float(data['total']['old_user_life']) * 100, 2) if float(
                data['total']['old_user_life']) > 0 else 0
            data['total']['old_user_ratio'] = str(data['total']['old_user_ratio']) + '%' if data['total'][
                                                                                                'old_user_ratio'] != 0 else 0
            data['total']['new_user_withdraw_num'] = str(total['new_user_withdraw_num']) if total[
                'new_user_withdraw_num'] else 0  # 新客提现人数
            data['total']['old_user_withdraw_num'] = str(total['old_user_withdraw_num']) if total[
                'old_user_withdraw_num'] else 0  # 老客提现人数
            data['total']['total_user_withdraw_num'] = float(data['total']['new_user_withdraw_num']) + float(
                data['total']['old_user_withdraw_num'])  # 总提现人数
            data['total']['new_user_withdraw'] = str(total['new_user_withdraw']) if total[
                'new_user_withdraw'] else 0  # 新客提现金额
            data['total']['old_user_withdraw'] = str(total['old_user_withdraw']) if total[
                'old_user_withdraw'] else 0  # 老客提现金额
            data['total']['new_r_w'] = float(data['total']['new_user_recharge']) - float(
                data['total']['new_user_withdraw'])  # 新用户充提差
            data['total']['old_r_w'] = float(data['total']['old_user_recharge']) - float(
                data['total']['old_user_withdraw'])  # 老用户充提差
            data['total']['new_w_ratio'] = round(
                float(data['total']['new_user_withdraw']) / float(data['total']['new_user_recharge']) * 100,
                2) if float(data['total']['new_user_recharge']) > 0 else 0  # 新用户提现率
            data['total']['old_w_ratio'] = round(
                float(data['total']['old_user_withdraw']) / float(data['total']['old_user_recharge']) * 100,
                2) if float(data['total']['old_user_recharge']) > 0 else 0  # 老用户提现率
            data['total']['total_w_ratio'] = round(
                float(data['total']['withdraw_money']) / float(data['total']['recharge_money']) * 100, 2) if float(
                data['total']['recharge_money']) > 0 else 0  # 总提现率
            data['total']['new_w_ratio'] = str(data['total']['new_w_ratio']) + '%' if data['total'][
                                                                                          'new_w_ratio'] != 0 else 0
            data['total']['old_w_ratio'] = str(data['total']['old_w_ratio']) + '%' if data['total'][
                                                                                          'old_w_ratio'] != 0 else 0
            data['total']['total_w_ratio'] = str(data['total']['total_w_ratio']) + '%' if data['total'][
                                                                                              'total_w_ratio'] != 0 else 0
            data['total']['recharge_fee'] = str(total['recharge_fee']) if total['recharge_fee'] else 0
            data['total']['withdraw_fee'] = str(total['withdraw_fee']) if total['withdraw_fee'] else 0
            data['total']['vip_up'] = str(total['vip_up'])
            data['total']['vip_week'] = str(total['vip_week'])
            data['total']['vip_month'] = str(total['vip_month'])
            data['total']['user_rebate'] = str(total['user_rebate'])
            data['total']['user_first_recharge'] = str(total['user_first_recharge'])
            data['total']['user_day_first_recharge'] = str(total['user_day_first_recharge'])
            data['total']['system_give'] = str(total['system_give'])
            data['total']['total_brokerage_money'] = float(total['first_recharge_brokerage']) + float(
                total['one_bet_brokerage']) + \
                                                     float(total['two_bet_brokerage']) + float(
                total['three_bet_brokerage']) + \
                                                     float(total['invite_task_brokerage'])
            data['total']['total_brokerage_money'] = round(data['total']['total_brokerage_money'], 2)
            data['total']['first_recharge_brokerage'] = str(total['first_recharge_brokerage'])
            data['total']['invite_task_brokerage'] = str(total['invite_task_brokerage'])
            data['total']['one_bet_brokerage'] = str(total['one_bet_brokerage'])
            data['total']['two_bet_brokerage'] = str(total['two_bet_brokerage'])
            data['total']['three_bet_brokerage'] = str(total['three_bet_brokerage'])
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取用户每日报表数据
@data_report.route('/admin/user_day_report_post', methods=['post'])
@login_required
def user_day_report_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total'] = dict()
    data['total']['num'] = 0
    data['total']['phone_num'] = 0
    data['total']['face_num'] = 0
    data['total']['email_num'] = 0
    data['total']['phone_ratio'] = 0
    data['total']['face_ratio'] = 0
    data['total']['email_ratio'] = 0
    try:
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        cid = request.values.get('cid')
        # bid = request.values.get('bid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql = "select day, sum(phone_num) phone_num, sum(face_num) face_num, sum(email_num) email_num from " \
              "san_day_money_total "
        sql2 = "select count(*) con from "
        sql3 = "select sum(phone_num) phone_num, sum(face_num) face_num, sum(email_num) email_num from " \
               "san_day_money_total "
        sql2 += "(select day, sum(num) num from san_day_money_total "
        sql_list = []
        if cid:
            sql_list.append(" cid = '%s'" % cid)

        # if bid:
        #     sql_list.append(" bid = '%s'" % bid)

        if stime:
            sql_list.append("  day >= '%s'" % stime)
        if etime:
            sql_list.append(" day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)
        sql += sql_str
        sql2 += sql_str
        sql3 += sql_str
        sql += " group by day order by day desc, num desc limit %d, %d" % (offset, limit)
        sql2 += " group by day order by day desc limit 100000) aa "
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        total = mysql.getOne(sql3, None)
        mysql.dispose()
        if res:
            for d in res:
                d['day'] = str(d['day'])
                d['phone_num'] = str(d['phone_num']) if d['phone_num'] else 0
                d['face_num'] = str(d['face_num']) if d['face_num'] else 0
                d['email_num'] = str(d['email_num']) if d['email_num'] else 0
                d['num'] = float(d['phone_num']) + float(d['face_num']) + float(d['email_num'])
                d['phone_ratio'] = round(float(d['phone_num']) / float(d['num']) * 100, 2) if float(d['num']) > 0 else 0
                d['face_ratio'] = round(float(d['face_num']) / float(d['num']) * 100, 2) if float(d['num']) > 0 else 0
                d['email_ratio'] = round(float(d['email_num']) / float(d['num']) * 100, 2) if float(d['num']) > 0 else 0
            data['total']['phone_num'] = str(total['phone_num']) if total['phone_num'] else 0
            data['total']['face_num'] = str(total['face_num']) if total['face_num'] else 0
            data['total']['email_num'] = str(total['email_num']) if total['email_num'] else 0
            data['total']['num'] = float(data['total']['phone_num']) + float(data['total']['face_num']) + float(
                data['total']['email_num'])
            data['total']['phone_ratio'] = round(float(data['total']['phone_num']) / float(data['total']['num']) * 100,
                                                 2) if float(data['total']['num']) > 0 else 0
            data['total']['face_ratio'] = round(float(data['total']['face_num']) / float(data['total']['num']) * 100,
                                                2) if float(data['total']['num']) > 0 else 0
            data['total']['email_ratio'] = round(float(data['total']['email_num']) / float(data['total']['num']) * 100,
                                                 2) if float(data['total']['num']) > 0 else 0
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)








# 获取所有渠道
def get_channel_all():
    sql = "select cid, username from san_agent where status = 1"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res
