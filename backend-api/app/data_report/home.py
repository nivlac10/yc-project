#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import json
import sys
import time

import pandas as pd
from flask import jsonify, request, send_file
from io import BytesIO

from app import public_util
from app.util import login_required
from SqlConntion.MySqlConn import Mysql
from . import data_report

importlib.reload(sys)


@data_report.route('/admin/admin_home', methods=['post'])
@login_required
def admin_home():
    cid = request.values.get('cid')
    day = request.values.get('day', str(time.strftime("%Y-%m-%d")))
    data = dict()
    data['code'] = 0
    data['r_w_money_list'] = dict()
    data['give_data'] = dict()
    data['bet_data'] = dict()
    data['profit_list'] = dict()
    data['recharge_Data'] = dict()
    data['withdraw_Data'] = dict()
    data1 = get_total_data(day, cid)
    data2 = get_month_data(cid)

    # 获取充值|提现数据
    data['recharge_Data'] = get_recharge_Data(cid, day)
    # 获取充值|提现数据
    data['withdraw_Data'] = get_withdraw_Data(cid, day)
    if data1:
        # 获取今日打码数据
        data['bet_data'] = get_bet_data(data1)
        # 今日获取赠送数据
        data['give_data'] = get_give_data(data1)
        # 获取卡片数据
        data['card'] = get_card_data(data1)
    if data2:
        # 获取毛利折现图
        data['profit_list'] = get_profit_list(data2)
        # 获取充值提现数据
        data['r_w_money_list'] = get_recharge_list(data2)
    data['code'] = 1
    # except Exception as e:
    #     print(e)
    return jsonify(data)


@data_report.route('/admin/home_data_post', methods=['post'])
@login_required
def home_data_post():
    data = dict()
    # try:
    if True:
        cid = request.values.get('cid')
        is_show = request.values.get('is_show')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        c_num = (int(page) - 1) * int(limit)
        data = get_home_data(cid, is_show, stime, etime, limit, c_num)

        data['code'] = 1
    # except Exception as e:
    #     print(e)
    return jsonify(data)


# 导出首页数据
@data_report.route('/admin/export_home_data_post', methods=['post', 'get'])
# @login_required
def export_home_data_postW():
    maps = None
    data = request.get_json()
    cid = data.get('cid')
    is_show = data.get('is_show')
    stime = data.get('stime')
    etime = data.get('etime')
    field_headers_list = data.get('field_headers_list')
        # db_index = request.headers.get('DBIndex')
    try:
        field_headers_list = json.loads(field_headers_list)
        field_list = []
        headers = []
        for item in field_headers_list:
            field_list.append(item.get('val', ''))
            headers.append(item.get('label', ''))
        # field_list = ['day', 'username', 'user_num', 'old_user_life', 'totals_num', 'game_num', 'new_game_num', 'old_game_num', 'recharge_money', 'recharge_fee', 'total_user_num', 'recharge_ratio', 'new_user_recharge'
        #               , 'new_user_num', 'new_user_ratio', 'old_user_recharge', 'old_user_num', 'old_user_ratio', 'new_user_withdraw_num', 'old_user_withdraw_num', 'total_withdraw_num', 'new_user_withdraw', 'old_user_withdraw',
        #               'withdraw_money', 'withdraw_fee', 'new_r_w', 'old_r_w', 'total_r_w', 'new_w_ratio', 'old_w_ratio', 'total_w_ratio', 'total_give_money', 'recharge_achieve', 'vip_up', 'vip_now', 'vip_split', 'vip_day', 'vip_week', 'vip_month', 'roller_money'
        #               , 'download_bonus', 'sign_bonus', 'loss_bonus', 'user_rebate', 'give_code_money', 'user_first_recharge', 'user_day_first_recharge', 'system_give', 'total_brokerage_money', 'first_recharge_brokerage',
        #               'invite_task_brokerage', 'one_bet_brokerage', 'two_bet_brokerage', 'three_bet_brokerage', 'total_bet', 'total_shu_ying', 'total_cover_charge', 'total_real_shu_ying']

        home_data = get_home_data(cid, is_show, stime, etime, 99999,0)
        # headers = [u"日期", u"渠道", u"新增注册用户", u"老用户日活", u"总用户日活", u"总玩家日活", u"新玩家日活", u"老玩家日活", u"当日付费总额", u"充值手续费", u"当日付费总人数", u"当日整体付费率", u"新增付费金额", u"新增付费人数", u"新增付费率", u"老用户付费金额"
        #            , u"老用户付费人数", u"老用户付费率", u"新增提现人数", u"老用户提现人数", u"当日提现总人数", u"新增提现金额", u"老用户提现金额", u"当日提现总额", u"提现手续费", u"新用户充提差", u"老用户充提差", u"当日总充提差", u"新用户提现率", u"老用户提现率", u"整体提现率"
        #            , u"赠送金额", u"充值成就", u"VIP晋级", u"VIP立即返水", u"vip拆分返水", u"VIP每日", u"VIP每周", u"VIP每月", u"转轮赠送", u"下载奖励", u"用户签到", u"用户破产补助", u"用户返水", u"兑换码赠送", u"用户首充", u"用户每日首充", u"系统赠送", u"总佣金",
        #            u"首充佣金", u"任务佣金", u"一级返佣", u"二级返佣", u"三级返佣", u"总押", u"总赢", u"游戏抽水", u"用户输赢"]
        # if is_show != 'true':
        #     del field_list[1]
        #     del headers[1]
        info = []
        total = []

        if home_data["data"]:
            for d in home_data["data"]:
                d["new_r_w"] = str(round(float(d["new_r_w"]), 2))
                d["old_r_w"] = str(round(float(d["old_r_w"]), 2))
                d["total_r_w"] = str(round(float(d["total_r_w"]), 2))
                d["total_brokerage_money"] = round(float(d["total_brokerage_money"]), 2)
                arr = []
                for field in field_list:
                    arr.append(str(d[field]))
                info.append(arr)

        if home_data["total"]:
            home_data["total"]["new_r_w"] = str(round(float(home_data["total"]["new_r_w"]), 2))
            home_data["total"]["old_r_w"] = str(round(float(home_data["total"]["old_r_w"]), 2))
            home_data["total"]["total_r_w"] = str(round(float(home_data["total"]["total_r_w"]), 2))
            home_data["total"]["total_brokerage_money"] = str(
                round(float(home_data["total"]["total_brokerage_money"]), 2))
            total = []
            for field in field_list:
                if field == 'day':
                    total.append(u"总计")
                if field != 'day' and field != 'username':
                    total.append(str(d[field]))
        info.append(total)
        filename = u'数据总览' + time.strftime("%Y-%m-%d")
        # 创建 DataFrame 对象
        df = pd.DataFrame(info)

        # 创建 BytesIO 对象
        excel_data = BytesIO()

        # 将数据写入 BytesIO 中
        df.to_excel(excel_data, index=False, header=headers)

        # 设置 BytesIO 指针到开头
        excel_data.seek(0)

        # 返回 Excel 数据至前端
        maps = send_file(excel_data, as_attachment=True, attachment_filename=filename + '.xlsx')
    except Exception as e:
        print(e)
    return maps


@data_report.route('/admin/test_xlsx', methods=['post', 'get'])
def test_xlsx():
    # data = YourModel.query.all()
    sql = "select uid, username , money user from san_users limit 0, 10"
    mysql = Mysql()
    data = mysql.getAll(sql, None)
    mysql.dispose()
    # 创建 DataFrame 对象
    df = pd.DataFrame(data)

    # 创建 BytesIO 对象
    excel_data = BytesIO()

    # 将数据写入 BytesIO 中
    df.to_excel(excel_data, index=False, header=['uid', '用户名', '余额'])

    # 设置 BytesIO 指针到开头
    excel_data.seek(0)

    # 返回 Excel 数据至前端
    return send_file(excel_data, as_attachment=True, attachment_filename='output.xlsx')


def get_home_data(cid, is_show, stime, etime, limit, c_num):
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total'] = dict()
    group_str = ""
    if is_show == 'true':
        group_str = ", a.cid "
    sql = "select a.day,b.username %s,ifnull(sum(phone_num + face_num + email_num),0) as user_num, ifnull(sum(old_user_life),0) old_user_life," \
          "ifnull(sum(a.old_user_life)+sum(a.user_num),0) totals_num, ifnull(sum(a.game_num),0) game_num," \
          "ifnull(sum(a.new_game_num),0) as new_game_num,ifnull(sum(a.old_game_num),0) as old_game_num," \
          "ifnull(sum(a.recharge_money),0) as recharge_money,ifnull(sum(a.recharge_fee),0) as recharge_fee," \
          "ifnull(sum(a.new_user_num),0) as new_user_num,ifnull(sum(a.old_user_num),0) as old_user_num," \
          "ifnull(sum(a.new_user_recharge),0) new_user_recharge,ifnull(sum(a.old_user_recharge),0) as old_user_recharge," \
          "ifnull(sum(a.new_user_withdraw_num),0) as new_user_withdraw_num,ifnull(sum(a.old_user_withdraw_num),0) " \
          "as old_user_withdraw_num,ifnull(sum(a.new_user_withdraw),0) as new_user_withdraw,ifnull(sum(a.old_user_withdraw),0)" \
          " as old_user_withdraw,ifnull(sum(a.withdraw_money),0) as withdraw_money,ifnull(sum(a.withdraw_fee),0) as withdraw_fee," \
          "ifnull(sum(a.total_give_money),0) as total_give_money,ifnull(sum(a.vip_up),0) as vip_up," \
          "ifnull(sum(a.vip_week),0) vip_week,ifnull(sum(a.vip_month),0) vip_month,ifnull(sum(a.user_rebate),0) as user_rebate," \
          "ifnull(sum(a.user_first_recharge),0) as user_first_recharge,ifnull(sum(a.user_day_first_recharge),0) as" \
          " user_day_first_recharge,ifnull(sum(a.system_give),0) as system_give,ifnull(sum(invite_task_brokerage),0) as " \
          "invite_task_brokerage,ifnull(sum(a.one_bet_brokerage),0) as one_bet_brokerage,ifnull(sum(a.two_bet_brokerage),0) as" \
          " two_bet_brokerage,ifnull(sum(a.three_bet_brokerage),0) as three_bet_brokerage," \
          "ifnull(sum(a.first_recharge_brokerage),0) first_recharge_brokerage,ifnull(sum(a.total_bet),0) as total_bet," \
          "ifnull(sum(a.total_shu_ying),0) as total_shu_ying,ifnull(sum(a.total_cover_charge),0) as total_cover_charge," \
          "ifnull(sum(a.total_real_shu_ying),0) as total_real_shu_ying,ifnull(sum(a.new_user_xd_num),0) new_user_xd_num," \
          "ifnull(sum(a.old_user_xd_num),0) old_user_xd_num,ifnull(sum(a.vip_now),0) vip_now,ifnull(sum(a.vip_split),0) vip_split," \
          "ifnull(sum(a.vip_day),0) vip_day,ifnull(sum(a.sign_bonus),0) sign_bonus,ifnull(sum(a.loss_bonus),0) loss_bonus" \
          ",ifnull(sum(a.give_code_money),0) give_code_money,ifnull(sum(a.roller_money),0) roller_money,sum(ifnull(a.download_bonus,0)) download_bonus," \
          "sum(ifnull(a.recharge_achieve,0)) recharge_achieve,sum(ifnull(a.user_total_money,0)) user_total_money" \
          "	from san_day_money_total as a  left join san_agent b on a.cid=b.cid " % group_str
    sql2 = "select count(*) con from (select day, sum(recharge_money) recharge_money from san_day_money_total as a "
    sql3 = "select ifnull(sum(phone_num + face_num + email_num),0) as user_num, ifnull(sum(old_user_life),0) old_user_life," \
           "ifnull(sum(a.old_user_life)+sum(a.user_num),0) totals_num, ifnull(sum(a.game_num),0) game_num," \
           "ifnull(sum(a.new_game_num),0) as new_game_num,ifnull(sum(a.old_game_num),0) as old_game_num," \
           "ifnull(sum(a.recharge_money),0) as recharge_money,ifnull(sum(a.recharge_fee),0) as recharge_fee," \
           "ifnull(sum(a.new_user_num),0) as new_user_num,ifnull(sum(a.old_user_num),0) as old_user_num," \
           "ifnull(sum(a.new_user_recharge),0) new_user_recharge,ifnull(sum(a.old_user_recharge),0) as old_user_recharge," \
           "ifnull(sum(a.new_user_withdraw_num),0) as new_user_withdraw_num,ifnull(sum(a.old_user_withdraw_num),0) " \
           "as old_user_withdraw_num,ifnull(sum(a.new_user_withdraw),0) as new_user_withdraw,ifnull(sum(a.old_user_withdraw),0)" \
           " as old_user_withdraw,ifnull(sum(a.withdraw_money),0) as withdraw_money,ifnull(sum(a.withdraw_fee),0) as withdraw_fee," \
           "ifnull(sum(a.total_give_money),0) as total_give_money,ifnull(sum(a.vip_up),0) as vip_up," \
           "ifnull(sum(a.vip_week),0) vip_week,ifnull(sum(a.vip_month),0) vip_month,ifnull(sum(a.user_rebate),0) as user_rebate," \
           "ifnull(sum(a.user_first_recharge),0) as user_first_recharge,ifnull(sum(a.user_day_first_recharge),0) as" \
           " user_day_first_recharge,ifnull(sum(a.system_give),0) as system_give,ifnull(sum(invite_task_brokerage),0) as " \
           "invite_task_brokerage,ifnull(sum(a.one_bet_brokerage),0) as one_bet_brokerage,ifnull(sum(a.two_bet_brokerage),0) as" \
           " two_bet_brokerage,ifnull(sum(a.three_bet_brokerage),0) as three_bet_brokerage," \
           "ifnull(sum(a.first_recharge_brokerage),0) first_recharge_brokerage,ifnull(sum(a.total_bet),0) as total_bet," \
           "ifnull(sum(a.total_shu_ying),0) as total_shu_ying,ifnull(sum(a.total_cover_charge),0) as total_cover_charge," \
           "ifnull(sum(a.total_real_shu_ying),0) as total_real_shu_ying,ifnull(sum(a.new_user_xd_num),0) new_user_xd_num," \
           "ifnull(sum(a.old_user_xd_num),0) old_user_xd_num,ifnull(sum(a.vip_now),0) vip_now,ifnull(sum(a.vip_split),0) vip_split," \
           "ifnull(sum(a.vip_day),0) vip_day,ifnull(sum(a.sign_bonus),0) sign_bonus,ifnull(sum(a.loss_bonus),0) loss_bonus" \
           ",ifnull(sum(a.give_code_money),0) give_code_money,ifnull(sum(a.roller_money),0) roller_money,sum(ifnull(a.download_bonus,0)) download_bonus," \
           "sum(ifnull(a.recharge_achieve,0)) recharge_achieve,sum(ifnull(a.user_total_money,0)) user_total_money" \
           "	from san_day_money_total as a "
    sql_list = []
    if cid:
        sql_list.append(" a.cid = '%s'" % cid)
    if stime:
        sql_list.append("  a.day >= '%s'" % stime)
    if etime:
        sql_list.append("  a.day <= '%s'" % etime)
    sql_str = public_util.data_list_to_str(sql_list)
    sql += sql_str
    sql3 += sql_str
    sql += " group by day desc %s order by day desc limit %d, %d" % (group_str,c_num, limit)
    sql2 += " group by day %s order by day desc limit 100000) aa " % group_str
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    cont = mysql.getOne(sql2, None)
    total = mysql.getOne(sql3, None)
    mysql.dispose()
    # user_avg_money
    if res:
        for d in res:
            d['day'] = str(d['day'])
            d['user_num'] = str(d['user_num'])
            d['old_user_life'] = str(d['old_user_life'])
            d['totals_num'] = str(int(d['user_num']) + int(d['old_user_life']))
            d['game_num'] = str(d['game_num'])
            d['new_game_num'] = str(d['new_game_num'])
            d['old_game_num'] = str(d['old_game_num'])
            d['new_user_num'] = str(d['new_user_num'])
            d['old_user_num'] = str(d['old_user_num'])
            d['new_user_withdraw_num'] = str(d['new_user_withdraw_num'])
            d['old_user_withdraw_num'] = str(d['old_user_withdraw_num'])
            d['old_user_xd_num'] = str(d['old_user_xd_num'])
            d['new_user_xd_num'] = str(d['new_user_xd_num'])
            d['recharge_achieve'] = str(d['recharge_achieve'])
            d['user_total_money'] = str(d['user_total_money'])
            d['r_num'] = str(float(d['new_user_num']) + float(d['old_user_num']))  # 总充值人数
            d['total_user_life'] = float(d['user_num']) + float(d['old_user_life'])  # 用户总日活
            d['total_game_life'] = float(d['new_game_num']) + float(d['old_game_num'])  # 总玩家日活
            d['total_user_num'] = float(d['new_user_num']) + float(d['old_user_num'])  # 当日付费总人数
            # lv = round((float(d['new_user_xd_num']) + float(d['old_user_xd_num'])) / 100, 2) if float(
            #     d['new_user_xd_num']) > 0 and float(d['old_user_xd_num']) > 0 else 0
            # d['recharge_ratio'] = round(float(d['total_user_num']) / lv, 2) if float(
            #     d['total_user_life']) > 0 and lv>0 else 0

            d['recharge_ratio'] = round(float(d['r_num']) / float(d['total_user_life']) * 100, 2) if float(
                d['total_user_life']) > 0 else 0  # 充值率
            d['recharge_ratio'] = str(d['recharge_ratio']) + '%'  # 当日整体付费率

            if int(d['user_num']) > 0:
                d['new_user_ratio'] = round(float(d['new_user_num']) / float(d['user_num']) * 100, 2)
                d['new_user_ratio'] = str(d['new_user_ratio']) + '%'
            else:
                d['new_user_ratio'] = 0  # 新用户付费率
            d['old_user_ratio'] = round(float(d['old_user_num']) / float(d['old_user_life']) * 100,
                                        2) if float(d['old_user_life']) > 0 else 0
            d['old_user_ratio'] = str(d['old_user_ratio']) + '%' if d['old_user_ratio'] != 0 else 0  # 老用户付费率
            print(d['recharge_money'],d['total_user_num'],d['new_user_recharge'],d['new_user_num'],d['old_user_recharge'],d['old_user_num'])
            d['user_avg_money'] = round(float(d['recharge_money']) /float(d['total_user_num'])) if float(d['recharge_money']) > 0 else 0   # 用户人均付费金额
            d['new_user_avg_money'] = round(float(d['new_user_recharge']) /float(d['new_user_num'])) if float(d['new_user_recharge']) > 0 else 0   # 新增人均付费金额
            d['old_user_avg_money'] = round(float(d['old_user_recharge']) /float(d['old_user_num'])) if float(d['old_user_recharge']) > 0 else 0   # 老用户人均付费金额

            # d['new_user_ratio'] = round(float(d['new_user_num']) / lv, 2) if float(d['new_user_num']) > 0 and lv>0 else 0
            # d['new_user_ratio'] = str(d['new_user_ratio']) + '%'  # 新用户付费率
            # d['old_user_ratio'] = round(float(d['old_user_num']) / lv, 2) if float(d['old_user_num']) > 0 and lv>0 else 0
            # d['old_user_ratio'] = str(d['old_user_ratio']) + '%'  # 老用户付费率

            d['total_withdraw_num'] = float(d['new_user_withdraw_num']) + float(d['old_user_withdraw_num'])  # 总提现数量
            # d['total_user_withdraw'] = float(d['new_user_withdraw']) + float(d['old_user_withdraw'])# 总提现金额
            d['new_r_w'] = float(d['new_user_recharge']) - float(d['new_user_withdraw'])  # 新用户充提差
            d['old_r_w'] = float(d['old_user_recharge']) - float(d['old_user_withdraw'])  # 老用户充提差
            d['total_r_w'] = d['new_r_w'] + d['old_r_w']  # 总提差
            d['new_w_ratio'] = round(float(d['new_user_withdraw']) / float(d['new_user_recharge']) * 100,
                                     2) if float(d['new_user_recharge']) > 0 else 0  # 新用户提现率
            d['old_w_ratio'] = round(float(d['old_user_withdraw']) / float(d['old_user_recharge']) * 100,
                                     2) if float(d['old_user_recharge']) > 0 else 0  # 老用户提现率
            d['total_w_ratio'] = round(float(d['withdraw_money']) / float(d['recharge_money']) * 100,
                                       2) if float(d['recharge_money']) > 0 else 0  # 总提现率
            d['total_brokerage_money'] = float(d['first_recharge_brokerage']) + float(d['one_bet_brokerage']) + \
                                         float(d['two_bet_brokerage']) + float(d['three_bet_brokerage']) + \
                                         float(d['invite_task_brokerage'])  # 总佣金

        total['user_num'] = str(total['user_num'])
        total['old_user_life'] = str(total['old_user_life'])
        total['totals_num'] = str(total['totals_num'])
        total['game_num'] = str(total['game_num'])
        total['new_game_num'] = str(total['new_game_num'])
        total['old_game_num'] = str(total['old_game_num'])
        total['new_user_num'] = str(total['new_user_num'])
        total['old_user_num'] = str(total['old_user_num'])
        total['new_user_withdraw_num'] = str(total['new_user_withdraw_num'])
        total['old_user_withdraw_num'] = str(total['old_user_withdraw_num'])
        total['old_user_xd_num'] = str(total['old_user_xd_num'])
        total['new_user_xd_num'] = str(total['new_user_xd_num'])
        total['recharge_achieve'] = str(total['recharge_achieve'])
        total['user_total_money'] = str(total['user_total_money'])
        data['total'] = total
        data['total']['r_num'] = float(data['total']['new_user_num']) + float(data['total']['old_user_num'])  # 总充值人数
        data['total']['total_user_life'] = float(data['total']['user_num']) + float(
            data['total']['old_user_life'])  # 用户总日活
        data['total']['total_game_life'] = float(data['total']['new_game_num']) + float(
            data['total']['old_game_num'])  # 总玩家日活
        data['total']['total_user_num'] = float(data['total']['new_user_num']) + float(
            data['total']['old_user_num'])  # 当日付费总人数
        lv = round((float(data['total']['new_user_xd_num']) + float(data['total']['old_user_xd_num'])) / 100,
                   2) if float(data['total']['new_user_xd_num']) > 0 and float(
            data['total']['old_user_xd_num']) > 0 else 0
        data['total']['recharge_ratio'] = round(
            float(data['total']['total_user_num']) / lv, 2) if float(
            data['total']['total_user_life']) > 0 and lv > 0 else 0
        data['total']['recharge_ratio'] = str(data['total']['recharge_ratio']) + '%'  # 当日整体付费率

        if int(data['total']['user_num']) > 0:
            data['total']['new_user_ratio'] = round(
                float(data['total']['new_user_num']) / float(data['total']['user_num']) * 100, 2)
            data['total']['new_user_ratio'] = str(data['total']['new_user_ratio']) + '%'
        else:
            data['total']['new_user_ratio'] = 0  # 新用户付费率
        data['total']['old_user_ratio'] = round(
            float(data['total']['old_user_num']) / float(data['total']['old_user_life']) * 100,
            2) if float(data['total']['old_user_life']) > 0 else 0
        data['total']['old_user_ratio'] = str(data['total']['old_user_ratio']) + '%' if data['total'][
                                                                                            'old_user_ratio'] != 0 else 0  # 老用户付费率
        # data['total']['new_user_ratio'] = round(float(data['total']['new_user_num']) / lv, 2) if float(
        #     data['total']['new_user_num']) > 0 and lv>0 else 0
        # data['total']['new_user_ratio'] = str(data['total']['new_user_ratio']) + '%'  # 新用户付费率
        # data['total']['old_user_ratio'] = round(float(data['total']['old_user_num']) / lv, 2) if float(
        #     data['total']['old_user_num']) > 0 and lv>0 else 0
        data['total']['old_user_ratio'] = str(data['total']['old_user_ratio']) + '%'  # 老用户付费率
        data['total']['total_withdraw_num'] = float(data['total']['new_user_withdraw_num']) + float(
            data['total']['old_user_withdraw_num'])  # 总提现数量
        data['total']['total_user_withdraw'] = float(data['total']['new_user_withdraw']) + float(
            data['total']['old_user_withdraw'])  # 总提现金额
        data['total']['new_r_w'] = float(data['total']['new_user_recharge']) - float(
            data['total']['new_user_withdraw'])  # 新用户充提差
        data['total']['old_r_w'] = float(data['total']['old_user_recharge']) - float(
            data['total']['old_user_withdraw'])  # 老用户充提差
        data['total']['total_r_w'] = data['total']['new_r_w'] + data['total']['old_r_w']  # 总提差
        data['total']['new_w_ratio'] = round(
            float(data['total']['new_user_withdraw']) / float(data['total']['new_user_recharge']) * 100,
            2) if float(data['total']['new_user_recharge']) > 0 else 0  # 新用户提现率
        data['total']['old_w_ratio'] = round(
            float(data['total']['old_user_withdraw']) / float(data['total']['old_user_recharge']) * 100,
            2) if float(data['total']['old_user_recharge']) > 0 else 0  # 老用户提现率
        data['total']['total_w_ratio'] = round(
            float(data['total']['withdraw_money']) / float(data['total']['recharge_money']) * 100,
            2) if float(data['total']['recharge_money']) > 0 else 0  # 总提现率
        data['total']['total_brokerage_money'] = float(data['total']['first_recharge_brokerage']) + float(
            data['total']['one_bet_brokerage']) + \
                                                 float(data['total']['two_bet_brokerage']) + float(
            data['total']['three_bet_brokerage']) + \
                                                 float(data['total']['invite_task_brokerage'])  # 总佣金

        data['total']['user_avg_money'] = round(float(total['recharge_money']) / float(total['total_user_num'])) if float(
            total['recharge_money']) > 0 else 0  # 用户人均付费金额
        data['total']['new_user_avg_money'] = round(float(total['new_user_recharge']) / float(total['new_user_num'])) if float(
            d['new_user_recharge']) > 0 else 0  # 新增人均付费金额
        data['total']['old_user_avg_money'] = round(float(total['old_user_recharge']) / float(total['old_user_num'])) if float(
            d['old_user_recharge']) > 0 else 0  # 老用户人均付费金额

        data['data'] = res
        data['count'] = cont['con']
    return data


# 获取毛利数据
def get_profit_list(data):
    maps = dict()
    maps['table'] = []
    maps['rw_data'] = []
    maps1 = dict()
    maps1['title'] = "赠送成本与手续费"
    # maps1['tips'] = "赠送"
    maps1['arr'] = []
    maps2 = dict()
    maps2['title'] = "游戏输赢"
    maps2['arr'] = []
    maps3 = dict()
    maps3['title'] = "毛利"
    maps3['arr'] = []
    for d in data:
        maps['table'].append(str(d['day'].strftime('%m-%d')))
        total_give = d['give_code_money'] + d['user_day_first_recharge'] + d['user_first_recharge'] + d['user_rebate'] \
                     + d['loss_bonus'] + d['vip_day'] + d['recharge_fee'] - d['withdraw_fee']
        maps1['arr'].append(round(total_give, 2))

        maps2['arr'].append(round(d['total_bet'] - d['total_shu_ying'], 2))
        maps3['arr'].append(round(d['total_bet'] - d['total_shu_ying'] - total_give, 2))
    maps['rw_data'].append(maps1)
    maps['rw_data'].append(maps2)
    maps['rw_data'].append(maps3)
    data = maps
    return data


# 获取今日打码数据
def get_bet_data(data):
    maps = dict()
    maps['total_bet'] = str(data['total_bet'])
    maps['total_shu_ying'] = str(data['total_shu_ying'])
    maps['total_real_shu_yin'] = str(round(data['total_bet'] - data['total_shu_ying'], 2))
    return maps


# 赠送数据
def get_give_data(data):
    # 赠送数据
    maps = dict()
    maps['data'] = []
    maps['title'] = '赠送数据'
    maps['data'].append(
        add_data('签到赠送', str(round(data.get('sign_bonus', 0), 2)),
                 "R$"))
    maps['data'].append(add_data('打码反水', str(round(data.get('user_rebate', 0), 2)), "R$"))
    maps['data'].append(add_data('补给箱', str(round(data.get('loss_bonus', 0), 2)), "R$"))
    maps['data'].append(add_data('兑换码赠送', str(round(data.get('give_code_money', 0), 2)), "R$"))
    maps['data'].append(add_data('vip晋级奖励', str(round(data.get('vip_up', 0), 2)), "R$"))
    maps['data'].append(add_data('vip立即反水', str(round(data.get('vip_now', 0), 2)), "R$"))
    maps['data'].append(add_data('vip拆分反水', str(round(data.get('vip_split', 0), 2)), "R$"))
    maps['data'].append(add_data('vip日奖励', str(round(data.get('vip_day', 0), 2)), "R$"))
    maps['data'].append(add_data('vip每周奖励', str(round(data.get('vip_week', 0), 2)), "R$"))
    maps['data'].append(add_data('vip每月奖励', str(round(data.get('vip_month', 0), 2)), "R$"))
    maps['data'].append(add_data('首充赠送', str(round(data.get('user_first_recharge', 0), 2)), "R$"))
    maps['data'].append(add_data('日复充赠送', str(round(data.get('user_day_first_recharge', 0), 2)), "R$"))
    maps['data'].append(add_data('系统赠送', str(round(data.get('system_give', 0), 2)), "R$"))
    maps['data'].append(add_data('转轮赠送', str(round(data.get('roller_money', 0), 2)), "R$"))
    maps['data'].append(add_data('下载奖励', str(round(data.get('download_bonus', 0), 2)), "R$"))
    maps['data'].append(add_data('充值成就', str(round(data.get('recharge_achieve', 0), 2)), "R$"))
    maps['data'].append(add_data('用户总余额', str(round(data.get('user_total_money', 0), 2)), "R$"))
    maps['data'].append(
        add_data('总金额', str(round(data.get('vip_day', 0) + data.get('system_give', 0) + data.get('user_rebate', 0) +
                                  data.get('loss_bonus', 0) + data.get('give_code_money', 0)
                                  + data.get('user_first_recharge', 0) + data.get('user_day_first_recharge', 0)
                                  + data.get('vip_up', 0) + data.get('vip_now', 0) + data.get('vip_split',
                                                                                              0) + data.get('vip_week',
                                                                                                            0)
                                  + data.get('vip_month', 0) + data.get('roller_money', 0) + data.get('download_bonus',
                                                                                                      0)
                                  + data.get('sign_bonus', 0) + data.get('recharge_achieve', 0)
                                  , 2)), "R$"))
    return maps


# 首页月充值提现数据
def get_recharge_list(data):
    maps = dict()
    maps['table'] = []
    maps['rw_data'] = []
    maps1 = dict()
    maps1['title'] = "充值金额"
    maps1['arr'] = []
    maps2 = dict()
    maps2['title'] = "提现金额"
    maps2['arr'] = []
    maps3 = dict()
    maps3['title'] = "充提差"
    maps3['arr'] = []
    for d in data:
        maps['table'].append(str(d['day'].strftime('%m-%d')))
        maps1['arr'].append(round(d['recharge_money'], 2))
        maps2['arr'].append(round(d['withdraw_money'], 2))
        maps3['arr'].append(round(d['recharge_money'] - d['withdraw_money'], 2))
    maps['rw_data'].append(maps1)
    maps['rw_data'].append(maps2)
    maps['rw_data'].append(maps3)
    data = maps
    return data


# 首页卡片数据
def get_card_data(data):
    arr = []
    # 注册数据
    maps = dict()
    maps['data'] = []
    maps['title'] = '注册数据'
    maps['data'].append(add_data('总注册', str(data['phone_num'] + data['face_num']), "人"))
    maps['data'].append(add_data('手机注册', str(data['phone_num']), "人"))
    maps['data'].append(add_data('邮箱注册', str(data['face_num']), "人"))
    arr.append(maps)
    # 游戏玩家数据
    maps = dict()
    maps['data'] = []
    maps['title'] = '玩家游玩数据'
    maps['data'].append(add_data('总人数', str(data['new_game_num'] + data['old_game_num']), "人"))
    maps['data'].append(add_data('新玩家Play', str(data['new_game_num']), "人"))
    maps['data'].append(add_data('老玩家Play', str(data['old_game_num']), "人"))
    cur_num = get_cur_user_num()
    maps['data'].append(add_data('在线人数', str(cur_num.get('count', 0)), "人"))
    arr.append(maps)
    # 佣金数据
    maps = dict()
    maps['data'] = []
    maps['title'] = '佣金数据'
    maps['data'].append(
        add_data('总金额', str(round(data.get('first_recharge_brokerage', 0) + data.get('invite_task_brokerage', 0), 2)),
                 "R$"))
    maps['data'].append(add_data('邀请任务', str(round(data.get('invite_task_brokerage', 0), 2)), "R$"))
    maps['data'].append(add_data('330人', str(round(data.get('first_recharge_brokerage', 0), 2)), "R$"))
    maps['data'].append(add_data('打码返佣', str(round(
        data.get('one_bet_brokerage', 0) + data.get('two_bet_brokerage') + data.get('three_bet_brokerage', 0), 2)),
                                 "R$"))
    arr.append(maps)
    return arr


# 获取充值数据
def get_recharge_Data(cid, day):
    maps = dict()
    try:
        sql_list = []
        sql_list.append(" day = '%s'" % day)
        if cid:
            sql_list.append(" cid = '%s'" % cid)
        sql_str = public_util.data_list_to_str(sql_list)

        recharge_sql = "select " \
                       "'新用户' row_name, " \
                       "ifnull(sum(new_user_recharge),0) pay_money, " \
                       "ifnull(sum(new_user_num),0) pay_user_sum, " \
                       "ifnull(round((sum(new_user_num)/sum(user_num))* 100,2),0) pay_lv, " \
                       "ifnull(round(sum(new_user_recharge)/sum(new_user_num),2),0) pay_arppu, " \
                       "ifnull(round(sum(new_user_recharge)/sum(user_num),2),0) pay_arpu " \
                       "from san_day_money_total %s " \
                       " UNION " \
                       "select " \
                       "'老用户' row_name, " \
                       "ifnull(sum(old_user_recharge),0) pay_money, " \
                       "ifnull(sum(old_user_num),0) pay_user_sum, " \
                       "ifnull(round((sum(old_user_num)/sum(old_user_life))* 100,2),0) pay_lv, " \
                       "ifnull(round(sum(old_user_recharge)/sum(old_user_num),2),0) pay_arppu, " \
                       "ifnull(round(sum(old_user_recharge)/sum(old_user_life),2),0) pay_arpu " \
                       "from san_day_money_total %s " \
                       " UNION " \
                       "select " \
                       "'总用户' row_name, " \
                       "ifnull(sum(recharge_money),0) pay_money, " \
                       "ifnull(sum(old_user_num+new_user_num),0) pay_user_sum, " \
                       "ifnull(round((sum(old_user_num+new_user_num))/(sum(phone_num + face_num + email_num + old_user_life))* 100,2),0) pay_lv, " \
                       "ifnull(round(sum(recharge_money)/(sum(old_user_num+new_user_num)),2),0) pay_arppu, " \
                       "ifnull(round(sum(recharge_money)/(sum(phone_num + face_num + email_num + old_user_life)),2),0) pay_arpu " \
                       "from san_day_money_total %s " % (sql_str, sql_str, sql_str)
        mysql = Mysql()
        recharge_res = mysql.getAll(recharge_sql, None)
        mysql.dispose()
        if recharge_res:
            for item in recharge_res:
                item['pay_user_sum'] = str(item['pay_user_sum'])
                item['pay_lv'] = str(item['pay_lv'])
            maps = recharge_res
    except Exception as e:
        print(e)
    return maps


def get_withdraw_Data(cid, day):
    maps = dict()
    try:
        sql_list = []
        sql_list.append(" day = '%s'" % day)
        if cid:
            sql_list.append(" cid = '%s'" % cid)
        sql_str = public_util.data_list_to_str(sql_list)
        withdraw_sql = "select " \
                       "'新用户' row_name, " \
                       "ifnull(sum(new_user_withdraw),0) withdraw_money, " \
                       "ifnull(sum(new_user_recharge-new_user_withdraw),0) w_r_gap, " \
                       "ifnull(round(sum(new_user_withdraw)/sum(new_user_recharge)* 100,2),0) withdraw_lv, " \
                       "ifnull(sum(old_user_withdraw_num),0) withdraw_user_sum " \
                       "from san_day_money_total %s " \
                       " UNION " \
                       "select " \
                       "'老用户' row_name, " \
                       "ifnull(sum(old_user_withdraw),0) withdraw_money, " \
                       "ifnull(sum(old_user_recharge-old_user_withdraw),0) w_r_gap, " \
                       "ifnull(round(sum(old_user_withdraw)/sum(old_user_recharge)* 100,2),0) withdraw_lv, " \
                       "ifnull(sum(new_user_withdraw_num),0) withdraw_user_sum " \
                       "from san_day_money_total  %s " \
                       " UNION " \
                       "select " \
                       "'总用户' row_name, " \
                       "ifnull(sum(withdraw_money),0) withdraw_money, " \
                       "ifnull(sum(recharge_money-withdraw_money),0) w_r_gap, " \
                       "ifnull(round(sum(withdraw_money)/sum(recharge_money)* 100,2),0) withdraw_lv, " \
                       "ifnull(sum(new_user_withdraw_num+old_user_withdraw_num),0) withdraw_user_sum " \
                       "from san_day_money_total %s " % (sql_str, sql_str, sql_str)
        mysql = Mysql()
        withdraw_res = mysql.getAll(withdraw_sql, None)
        mysql.dispose()
        if withdraw_res:
            for item in withdraw_res:
                item['withdraw_user_sum'] = str(item['withdraw_user_sum'])
            maps = withdraw_res
    except Exception as e:
        print(e)
    return maps


def add_data(title, num, unit):
    new_data = dict()
    new_data['title'] = title
    new_data['num'] = num
    new_data['unit'] = unit
    return new_data


def get_total_data(day, cid):
    sql = "select ifnull(sum(phone_num), 0) phone_num, ifnull(sum(face_num),0) face_num," \
          " ifnull(sum(new_game_num),0) new_game_num, ifnull(sum(old_game_num),0) old_game_num,  " \
          " ifnull(sum(first_recharge_brokerage),0) first_recharge_brokerage, ifnull(sum(invite_task_brokerage),0) invite_task_brokerage, " \
          " ifnull(sum(one_bet_brokerage),0) one_bet_brokerage, ifnull(sum(two_bet_brokerage),0) two_bet_brokerage, " \
          " ifnull(sum(total_bet),0) total_bet  ," \
          " ifnull(sum(total_shu_ying),0) total_shu_ying  ," \
          " ifnull(sum(three_bet_brokerage),0) three_bet_brokerage  ," \
          " ifnull(sum(vip_day), 0) vip_day ," \
          " ifnull(sum(sign_bonus), 0) sign_bonus," \
          " ifnull(sum(vip_up), 0) vip_up," \
          " ifnull(sum(vip_now), 0) vip_now," \
          " ifnull(sum(vip_split), 0) vip_split," \
          " ifnull(sum(vip_day), 0) vip_day," \
          " ifnull(sum(vip_week), 0) vip_week," \
          " ifnull(sum(vip_month), 0) vip_month," \
          " ifnull(sum(loss_bonus), 0) loss_bonus ," \
          " ifnull(sum(user_rebate), 0) user_rebate ," \
          " ifnull(sum(user_first_recharge), 0) user_first_recharge ," \
          " ifnull(sum(user_day_first_recharge), 0) user_day_first_recharge ," \
          " ifnull(sum(give_code_money), 0) give_code_money ," \
          " ifnull(sum(system_give), 0) system_give," \
          " ifnull(sum(roller_money), 0) roller_money," \
          " ifnull(sum(download_bonus), 0) download_bonus," \
          " ifnull(sum(recharge_achieve),0) recharge_achieve," \
          " ifnull(sum(user_total_money),0) user_total_money" \
          " from san_day_money_total where day = '%s' " % day
    if cid:
        sql += " and cid = '%s'" % cid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res if res is not None else {}


def get_month_data(cid):
    day = public_util.get_last_three_day()
    sql = "select day,ifnull(SUM(recharge_money),0) recharge_money,ifnull(SUM(recharge_fee),0) recharge_fee, SUM(withdraw_money)" \
          " withdraw_money,SUM(withdraw_fee) withdraw_fee, SUM(vip_day) vip_day," \
          " SUM(loss_bonus) loss_bonus, SUM(user_rebate) user_rebate" \
          ",SUM(user_first_recharge) user_first_recharge, SUM(user_day_first_recharge)" \
          " user_day_first_recharge,SUM(give_code_money) give_code_money," \
          "SUM(system_give) system_give , SUM(total_bet) total_bet ," \
          " SUM(total_shu_ying) total_shu_ying from san_day_money_total where day >= '%s'" % str(day)
    if cid:
        sql += " and cid = '%s'" % cid
    sql += " GROUP BY `day` ORDER BY `day`"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


def get_cur_user_num():
    sql = "select count(*) count from san_users where cur_gameid > 0"
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res if res is not None else {}
