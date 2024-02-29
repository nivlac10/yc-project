#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-03-02
import importlib
import json

from flask import request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.RKEY import SAN_EXTERNAL_GAME_LIST
from app.user import user
from app.util import login_required
from app import public_util, common, redis, public_game_api, util
import sys, time, random
from  app.admin import conf

importlib.reload(sys)


# 获取用户列表数据
@user.route('/admin/user_list_post', methods=['post'])
@login_required
def user_list_post():
    data = dict()
    data['data'] = []
    data['code'] = 0
    data['count'] = 0
    data['total'] = dict()
    # 添加显示字段：
        # 会员等级
        # 团队人数
        # 团队总充值
        # 总打码量
        # 注单数
        # 总实际输赢
    # 添加查询条件：
        # 最小打码量
        # 最大打码量
        # 排序【desc|asc】

    if True:
        nickname = request.values.get('nickname')
        username = request.values.get('username')
        CPF = request.values.get('CPF')
        cid = request.values.get('cid')
        user_type = request.values.get('user_type', '1')
        vip = request.values.get('vip_lv')
        sh = request.values.get('sh')
        sort = request.values.get('sort', '0')
        min_money = request.values.get('min_money')
        max_money = request.values.get('max_money')
        min_total_bet = request.values.get('min_total_bet')
        max_total_bet = request.values.get('max_total_bet')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        line = request.values.get('line')
        order = request.values.get('order','desc')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql = "select a.*, b.username bname from san_users a left join " \
              "san_agent b on b.cid = a.cid where a.user_gm = 0"
        sql2 = "select count(*) con,sum(total_bet) total_bet,sum(total_num) total_num,sum(total_real_shu_ying) total_real_shu_ying," \
               " sum(money) money, sum(commission) commission,sum(total_money) total_money,sum(total_withdraw) total_withdraw," \
               "sum(give_money) give_money, sum(total_commission) total_commission " \
               " from(select * from san_users where user_gm = 0"
        if nickname:
            sql += " and (locate('%s', a.uid)>0 or locate('%s', register_ip)>0 or locate('%s', aaid)>0 or locate('%s', a.nickname) > 0 or " \
                   "locate('%s', a.phone)>0)" % (nickname, nickname, nickname, nickname, nickname)
            sql2 += " and (locate('%s', uid)>0 or locate('%s', register_ip)>0 or locate('%s', aaid)>0 or locate('%s', nickname) > 0 or " \
                    "locate('%s', phone)>0)" % (nickname, nickname, nickname, nickname, nickname)
        if username:
            sql += " and locate('%s', a.username)>0" % (username)
            sql2 += " and locate('%s', username)>0" % (username)
        if CPF:
            sql += " and locate('%s', a.CPF)>0" % (CPF)
            sql2 += " and locate('%s', CPF)>0" % (CPF)
        if cid:
            sql += " and a.cid = '%s'" % cid
            sql2 += " and cid = '%s'" % cid
        if user_type:
            sql += " and a.user_type = '%s'" % user_type
            sql2 += " and user_type = '%s'" % user_type
        if sh:
            sql += " and a.sh = '%s'" % sh
            sql2 += " and sh = '%s'" % sh
        if min_money:
            sql += " and a.total_money >= '%s'" % min_money
            sql2 += " and total_money >= '%s'" % min_money
        if max_money:
            sql += " and a.total_money <= '%s'" % max_money
            sql2 += " and total_money <= '%s'" % max_money
        if min_total_bet:
            sql += " and a.total_bet >= '%s'" % min_total_bet
            sql2 += " and total_bet >= '%s'" % min_total_bet
        if max_total_bet:
            sql += " and a.total_bet <= '%s'" % max_total_bet
            sql2 += " and total_bet <= '%s'" % max_total_bet
        if line:
            sql += " and a.cur_gameid > 0"
            sql2 += " and cur_gameid > 0"
        if vip:
            sql += " and a.vip_lv = '%s'"%vip
            sql2 += " and vip_lv = '%s'"%vip
        if stime:
            sql += " and a.add_time >= '%s'"%stime
            sql2 += " and add_time >= '%s'"%stime
        if etime:
            etime += " 23:59:59"
            sql += " and a.add_time <= '%s'"%etime
            sql2 += " and add_time <= '%s'"%etime
        sort_list = ['a.uid', 'a.total_money', 'a.total_withdraw', 'a.money', 'a.team_one_user_num',
                     'a.total_commission','a.total_bet','a.team_recharge','a.add_time','total_num','a.total_real_shu_ying','a.commission']
        # a.uid 用户编码
        # total_money 总充值
        # total_withdraw 总提现
        # money 金额
        # team_one_user_num 团队一级人数
        # total_commission 总佣金
        # total_bet 总打码量
        # team_recharge 团段总充值
        # add_time  注册时间
        # total_num 注单数
        # total_real_shu_ying 总实际输赢
        sql += " order by %s %s limit %d, %d" % (sort_list[int(sort)],order, c_num, limit)
        sql2 += ") aa"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        vip_list = ['普通用户', '白银会员', '黄金会员', '砖石会员']
        game = get_game_conf()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time']) if d['add_time'] else ''
                d['login_time'] = str(d['login_time']) if d['login_time'] else ''
                d['user_type_str'] = '否' if d['user_type'] == 1 else '是'
                # d['time_int'] = public_util.days_int(d['add_time']) * 1000
                d['sh_str'] = '正常用户' if d['sh'] == 0 else '审核用户'
                d['cur_game'] = '离线'
                if d['cur_gameid'] > 0:
                    d['cur_game'] = game[str(d['cur_gameid'])] if str(d['cur_gameid']) in game else '未知游戏'
            data['data'] = res
            data['count'] = cont['con']
            data['total'] = cont
            data['total']['total_num'] = str(cont['total_num'])
        data['code'] = 1
    # except Exception as e:
    #     print(e)
    return jsonify(data)


# 获取用户信息
@user.route('/admin/recharge_user_detail_post', methods=['post'])
@login_required
def recharge_user_detail_post():
    data = dict()
    data['data'] = []
    data['conf'] = []
    data['game'] = []
    data['pay'] = []
    data['code'] = 0
    try:
        cid = request.values.get('uid')
        sql = "select a.*,b.username cname from san_users a left join san_agent b on b.cid = a.cid  where a.uid = '%s'" % cid
        mysql = Mysql()
        res = mysql.getOne(sql, None)
        mysql.dispose()
        if res:
            game = get_game_conf()
            # TaDa_money = public_game_api.TaDa_get_user_money(res['uid'])
            # SBO_money = public_game_api.get_sbo_user_money(res['uid'])
            # res['TaDa_money'] = TaDa_money
            # res['SBO_money'] = SBO_money
            res['SBO_money'] = 0
            res['status'] = "启用" if res['status'] == 1 else "禁用"
            if res['cur_gameid'] > 0:
                res['flag'] = game[str(res['cur_gameid'])] if str(res['cur_gameid']) in game else '未知游戏'
            else:
                res['flag'] = "离线"
            if res['total_bet'] != 0:
                res['bet_pro'] = str(round(float(res['total_shu_ying']) / float(res['total_bet']) * 100, 2)) + '%'
            else:
                res['bet_pro'] = str(0) + "%"
            if res['withdraw_type'] == 0:
                res['withdraw_str'] = "正常"
            elif res['withdraw_type'] == 1:
                res['withdraw_str'] = "审核"
            elif res['withdraw_type'] == 2:
                res['withdraw_str'] = "白名单"
            res['vip_count'] = round(float(res['vip_split'])+float(res['vip_now'])+float(res['vip_up'])+float(res['vip_day'])+float(res['vip_week'])+float(res['vip_month']), 2)
            res['give_money'] = round(float(res['first_recharge_give'])+float(res['day_first_recharge_give'])+float(res['sign_bonus'])+float(res['loss_bonus'])+float(res['roller_money'])
                                      +float(res['give_code_money'])+float(res['download_bonus'])+float(res['system_give'])+float(res['recharge_achieve'])+float(res['vip_count']), 2)
            res['add_time'] = str(res['add_time'])
            res['login_time'] = str(res['login_time'])

            user_data = get_user_black_log(res['uid'], type=0)
            res['is_black'] = True if user_data else False
            if res['is_black'] == False :
                if res['parent_id'] != 0 and res['is_black'] == False:
                    user_data = get_user_black_log(res['parent_id'], type=1)
                if res['super_id'] != 0 and res['is_black'] == False:
                    user_data = get_user_black_log(res['super_id'], type=1)
                if res['super_parent_id'] != 0 and res['is_black'] == False:
                    user_data = get_user_black_log(res['super_parent_id'], type=1)
                if user_data and user_data['type']==1:
                    res['is_black'] = True
                else: res['is_black'] = False
        conf = common.MONEY_TYPE_CONF
        game = redis.get(SAN_EXTERNAL_GAME_LIST)
        if game:
            game = json.loads(game)
        pay = get_all_pay()
        data['data'] = res
        data['conf'] = conf
        data['game'] = game
        data['pay'] = pay
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 更新用户状态
@user.route('/admin/update_user_status_post', methods=['post'])
@login_required
def update_user_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        uid = request.values.get('uid')
        status = request.values.get('status')
        if status not in ['0', '1']:
            data['msg'] = '参数错误'
            return jsonify(data)
        sql = "update san_users set status = '%s' where uid = '%s'" % (status, uid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除用户
@user.route('/admin/delete_user_post', methods=['post'])
@login_required
def delete_user_post():
    data = dict()
    data['msg'] = '操作失败'
    data['status'] = 0
    data['code'] = 0
    try:
        uid = request.values.get('uid')
        user = get_user_info(uid)
        if user is None:
            data['msg'] = '用户不存在'
            return jsonify(data)
        if user['status'] == 1:
            data['msg'] = '用户正在使用，请先禁用账号'
            return jsonify(data)
        sql = "delete from san_users where uid = '%s'" % uid
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res > 0:
            data['msg'] = '操作成功'
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 用户充值处理
@user.route('/admin/user_recharge_post', methods=['post'])
@login_required
def user_recharge_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        uid = request.values.get('uid')
        money = float(request.values.get('money'))
        remain_code_amount = request.values.get("remain_code_amount")
        # if float(money) <= 0:
        #     data['msg'] = '金额不能小于0'
        #     return jsonify(data)
        con = get_user_info(uid)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        user_code_money = con['remain_code_amount']
        if user_code_money < 0:
            remain_code_amount = float(remain_code_amount) + abs(user_code_money)
        day = public_util.get_today().strftime('%Y-%m-%d')
        res = common.update_user_data_info(uid, money=money, give_money=money, remain_code_amount=remain_code_amount,
                                           system_give=money)
        if res:
            common.user_day_data_total(uid, day, give_money=money, system_give=money)
            data['status'] = 1
            data['code'] = 1
            data['msg'] = '操作成功'
            common.user_money_log_func(con['uid'], money, con['money'], float(money) + float(con['money']), 12)  # 变动记录
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取用户充值列表数据
@user.route('/admin/user_recharge_data_post', methods=['post'])
@login_required
def user_recharge_data_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total_money'] = 0
    try:
        uid = request.values.get('uid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql = "select a.*, b.nickname, c.pay_name from san_order_list a left join san_users b on b.uid = a.uid left " \
              "join san_pay_list c on c.pay_id = a.pay_id where a.uid = '%s'" % uid
        sql2 = "select count(*) con from san_order_list a left join san_users b on b.uid = a.uid where a.uid = '%s'" % uid
        sql3 = "select sum(a.money) money from san_order_list a left join san_users b on b.uid = a.uid where " \
               "a.uid = '%s'" % uid
        sql += " order by a.id desc limit %d, %d" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        total = mysql.getOne(sql3, None)
        mysql.dispose()
        status_list = ['下单成功', '充值成功', '充值失败', '下单失败']
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                # d['time_int'] = public_util.days_int(d['add_time']) * 1000
                d['notify_time'] = str(d['notify_time'])
                d['status_str'] = status_list[d['status']]
                # d['success_int'] = public_util.days_int(d['success_time']) * 1000 if d['success_time'] else 0
                d['pay_name'] = d['pay_name'] if d['pay_name'] else ''
            data['data'] = res
            data['count'] = cont['con']
            data['total_money'] = str(total['money']) if total['money'] else 0
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 更新用户信息
@user.route('/admin/user_edit_data_post', methods=['post'])
@login_required
def update_user_sh_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        uid = request.values.get('uid')
        nickname = request.values.get('nickname')
        new_pass = request.values.get('new_pass', '').replace(' ', '')
        withdraw_type = request.values.get('withdraw_type')
        remain_code_amount = request.values.get("remain_code_amount")
        user = get_user_info(uid)
        if user is None:
            data['msg'] = '用户不存在'
            return jsonify(data)
        sql = "update san_users set nickname = '%s', withdraw_type = '%s',remain_code_amount='%s'" % (
            nickname, withdraw_type, remain_code_amount)
        if new_pass:
            if user['phone'] == '':
                data['msg'] = '用户手机号为空'
                return jsonify(data)
            password = add_storage_pass(user['username'], new_pass)
            sql += ", password = '%s'" % password
        sql += " where uid = '%s'" % uid
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res >= 0:
            data['status'] = 1
            data['code'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取用户提现列表数据
@user.route('/admin/user_withdraw_data_post', methods=['post'])
@login_required
def user_withdraw_data_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total_money'] = 0
    data['send_money'] = 0
    data['rate'] = 0
    try:
        uid = request.values.get('uid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql = "select a.*, b.nickname, c.pay_name from san_withdraw_list a left join san_users b on b.uid = a.uid " \
              "left join san_pay_list c on c.pay_id = a.pay_id where a.uid = '%s'" % uid
        sql2 = "select count(*) con from san_withdraw_list a left join san_users b on b.uid = a.uid where " \
               "a.uid = '%s'" % uid
        sql3 = "select sum(a.money) money, sum(send_money) send_money, sum(rate) rate from san_withdraw_list a " \
               "left join san_users b on b.uid = a.uid where a.uid = '%s'" % uid
        sql += " order by a.id desc limit %d, %d" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        total = mysql.getOne(sql3, None)
        mysql.dispose()
        status_list = ['下单成功', '提现成功', '提现失败', '人工审核', '成功后失败', '拒绝提现', '下单失败']
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                # d['time_int'] = public_util.days_int(d['add_time']) * 1000
                # d['success_int'] = public_util.days_int(d['success_time']) * 1000 if d['success_time'] else 0
                d['notify_time'] = str(d['notify_time'])
                d['status_str'] = status_list[d['status']]
                d['pay_name'] = d['pay_name'] if d['pay_name'] else ''
            data['data'] = res
            data['count'] = cont['con']
            data['total_money'] = str(total['money']) if total['money'] else 0
            data['send_money'] = str(total['send_money']) if total['send_money'] else 0
            data['rate'] = str(total['rate']) if total['rate'] else 0
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取用户余额日志数据
@user.route('/admin/user_money_log_data_post', methods=['post'])
@login_required
def user_money_log_data_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        uid = request.values.get('uid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql = "select a.*, b.nickname from san_user_money_log a left join san_users b on b.uid = a.uid where 1=1"
        sql2 = "select count(*) con from san_user_money_log a left join san_users b on b.uid = a.uid where 1=1"
        if uid:
            sql += " and a.uid = '%s'" % uid
            sql2 += " and a.uid = '%s' " % uid
        sql += " order by a.id desc limit %d, %d" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                # d['time_int'] = public_util.days_int(d['add_time']) * 1000
                d['money_type_str'] = common.MONEY_TYPE_CONF[str(d['money_type'])]['name'] if common.MONEY_TYPE_CONF[
                    str(d['money_type'])] else '未知'
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取用户游戏记录汇总
@user.route('/admin/user_game_total_data_post', methods=['post'])
@login_required
def user_game_total_data_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['total'] = dict()
    data['total']['cover_charge'] = 0
    data['total']['real_shu_ying'] = 0
    data['total']['code_size'] = 0
    data['total']['betting'] = 0
    data['total']['num'] = 0
    try:
        uid = request.values.get('uid')
        sql = "select sum(a.cover_charge) cover_charge, sum(a.real_shu_ying) real_shu_ying, a.uid, a.game_id, " \
              "sum(a.code_size) code_size, sum(a.betting) betting, count(a.odd_number) num, b.nickname, c.game_name " \
              "from san_game_bet_log a left join san_users b on b.uid = a.uid left join san_game_list c on " \
              "c.game_id = a.game_id where a.uid = '%s' group by game_id order by num desc" % uid
        sql2 = "select sum(cover_charge) cover_charge, sum(real_shu_ying) real_shu_ying, sum(code_size) code_size, " \
               "sum(betting) betting, count(odd_number) num from san_game_bet_log where uid = '%s'" % uid
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        total = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['cover_charge'] = str(d['cover_charge']) if d['cover_charge'] else 0
                d['real_shu_ying'] = str(d['real_shu_ying']) if d['real_shu_ying'] else 0
                d['code_size'] = str(d['code_size']) if d['code_size'] else 0
                d['betting'] = str(d['betting']) if d['betting'] else 0
                d['num'] = int(d['num']) if d['num'] else 0
            data['total']['cover_charge'] = str(total['cover_charge']) if total['cover_charge'] else 0
            data['total']['real_shu_ying'] = str(total['real_shu_ying']) if total['real_shu_ying'] else 0
            data['total']['code_size'] = str(total['code_size']) if total['code_size'] else 0
            data['total']['betting'] = str(total['betting']) if total['betting'] else 0
            data['total']['num'] = str(total['num']) if total['num'] else 0
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加审核账号处理
@user.route('/admin/add_verify_user_post', methods=['post'])
@login_required
def add_verify_user_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        cid = request.values.get('cid', '')
        nickname = request.values.get('nickname', '')
        phone = request.values.get('phone', '')
        if len(phone) != 10:
            data['msg'] = '手机号码错误'
            return jsonify(data)
        channel = get_channel(cid)
        if channel is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        phone_data = get_phone(phone)
        if phone_data:
            data['msg'] = '手机号已注册'
            return jsonify(data)
        res = add_account_func(cid, nickname, phone)
        if res >= 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加测试账号处理
@user.route('/admin/add_user_recharge_account_post', methods=['post'])
@login_required
def add_user_recharge_account_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        uid = request.values.get('uid', '0')
        money = request.values.get('money', '0')
        if float(money) <= 0:
            data['msg'] = '金额错误'
            return jsonify(data)
        user = get_user_info(str(uid))
        if user is None:
            data['msg'] = '用户不存在'
            return jsonify(data)
        if user['user_type'] != 1:
            data['msg'] = '用户类型为游客'
            return jsonify(data)
        if user['total_money'] > 0:
            data['msg'] = '当前用户已有充值'
            return jsonify(data)
        sql = "update san_users set total_money = '%s' where uid = '%s'" % (money, uid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 用户推广记录
@user.route("/admin/play_promotion_list", methods=['post'])
@login_required
def play_promotion_list():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['total'] = dict()
    data['start_day'] = ''
    data['end_day'] = ''
    try:
        uid = request.values.get('uid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        users_level = request.values.get('users_level')
        c_num = (int(page) - 1) * int(limit)
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        first_recharge = request.values.get("first_recharge")
        sql = "select add_time,uid,nickname,CPF,username,total_money,total_withdraw,total_bet,total_shu_ying," \
              "total_real_shu_ying,money,parent_id,super_id,super_parent_id" \
              ",bet_parent_brokerage,bet_super_brokerage,bet_parent_super_brokerage,recharge_parent_brokerage" \
              "  from san_users "
        sql2 = "select count(*) count, sum(total_money) total_money,sum(total_withdraw) total_withdraw ," \
               " sum(money) money from san_users "
        sql3 = "select  count(*) count from san_users "
        sql_list = []
        if users_level:
            if int(users_level) == 1:
                sql_list.append(" parent_id = '%s'" % uid)
            if int(users_level) == 2:
                sql_list.append(" super_id = '%s'" % uid)
            if int(users_level) == 3:
                sql_list.append(" super_parent_id = '%s'" % uid)
        else:
            sql_list.append(" (parent_id = '%s' or super_id = '%s' or super_parent_id = '%s')" % (uid, uid, uid))
        if first_recharge:
            if int(first_recharge) == 0:
                sql_list.append(" total_money=0 ")
            else:
                sql_list.append(" total_money>0 ")
        if stime:
            sql_list.append("  add_time >= '%s'" % stime)
        if etime:
            e_str = str(etime) + ' 23:59:59'
            sql_list.append("  add_time <= '%s'" % e_str)
        sql_str = public_util.data_list_to_str(sql_list)
        sql += sql_str
        sql2 += sql_str
        sql3 += sql_str
        sql3 += " and  total_money != 0"
        print(sql3)
        sql += " order by add_time desc limit %s,%s" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        total = mysql.getOne(sql2, None)
        res3 = mysql.getOne(sql3, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                if str(d['parent_id']) == str(uid):
                    d['level'] = 1
                    d['bet_brokerage'] = round(float(d['bet_parent_brokerage']), 2)
                if str(d['super_id']) == str(uid):
                    d['level'] = 2
                    d['bet_brokerage'] = round(float(d['bet_super_brokerage']), 2)
                if str(d['super_parent_id']) == str(uid):
                    d['level'] = 3
                    d['bet_brokerage'] = round(float(d['bet_parent_super_brokerage']), 2)
            total['total_money'] = str(total['total_money'])
            total['total_withdraw'] = str(total['total_withdraw'])
            total['money'] = str(total['money'])
            total['total_money_withdraw'] = round(float(total['total_money']) - float(total['total_withdraw']), 2)
            total['first_recharge'] = res3['count']
            data['data'] = res
            data['count'] = total['count']
            data['total'] = total
        data['start_day'] = stime
        data['end_day'] = etime
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改用户白名单
@user.route("/admin/withdraw_type_post", methods=['post'])
@login_required
def withdraw_type_post():
    data = dict()
    data['code'] = 0
    try:
        withdraw_type = request.values.get('withdraw_type')
        uid = request.values.get('uid')
        sql = "update san_users set withdraw_type = '%s' where uid = '%s' " %(withdraw_type, uid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)

# 获取异常用户
def get_user_black_log(uid,type=0):
    sql = "select * from san_user_black_log where uid = '%s' and type='%s'" % (uid,type)
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res

# 获取游戏配置
def get_game_conf():
    maps = dict()
    try:
        sql = "select gid, a.game_name,factory_name,c.game_name as gName from san_external_game_list as a left join " \
              "san_factory_list b on a.my_game=b.factory_id left join san_game_list as c on c.game_id=a.game_id"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        mysql.dispose()
        if res:
            for d in res:
                maps[str(d['gid'])] = d['factory_name'] + "/" + d['gName'] + "/" + d['game_name']
    except Exception as e:
        print(e)
    return maps


# 新增审核账号
def add_account_func(cid, nickname, phone):
    user = get_user_min_uid()
    uid = int(user['uid']) - 1 if user else 10668800
    password = add_storage_pass(phone, '123456')
    user_type = 1
    num = random.randint(0, 9)
    register_ip = public_util.get_current_ip()
    sh = 1  # 审核模式
    sql = "insert into san_users(uid, nickname, password, header_img, register_ip, phone, user_type, cid, sh, " \
          "money, add_time,device_info) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, 10, now(),'{}')"
    mysql = Mysql()
    res = mysql.insertOne(sql, [uid, nickname, password, num, register_ip, phone, user_type, cid, sh])
    mysql.dispose()
    return res


# 生成储存的用户密码
def add_storage_pass(username, password):
    md_str = public_util.md5(str(username)) + public_util.md5(password)
    s_str = ''.join(sorted(public_util.md5(''.join(sorted(md_str)))))
    return s_str


# 获取审核用户uid
def get_user_min_uid():
    sql = "select min(uid) uid from san_users;"
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 查询手机号码是否注册
def get_phone(phone):
    sql = "select * from san_users where phone = '%s'" % phone
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 查询渠道信息
def get_channel(cid):
    sql = "select * from san_agent where cid = '%s'" % cid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 查询用户信息详情
def get_user_info(uid):
    sql = "select * from san_users where uid = '%s'" % uid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 获取游戏配置
def get_game_conf():
    maps = dict()
    try:
        sql = "select gid,a.my_game, a.game_name,factory_name,c.game_name as gName from" \
              " san_external_game_list as a left join " \
              "san_factory_list b on a.my_game=b.factory_id left join san_game_list as c on c.game_id=a.game_id"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        mysql.dispose()
        if res:
            for d in res:
                maps[str(d['gid'])] = d['factory_name'] + "/" + d['gName'] + "/" + d['game_name']
    except Exception as e:
        print(e)
    return maps


# 获取所有支付
def get_all_pay():
    sql = "select pay_id, pay_name from san_pay_list where status = 1"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res
