#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-03-02
import datetime
import json
import sys
from datetime import datetime, timedelta
import redis
import requests
from flask import request

from SqlConntion.MySqlConn import Mysql
from app import constant, util
import importlib

from app.user import user
from app.util import login_required

importlib.reload(sys)
ServerId = '8888SLOT_BET_01'
# 正式环境
SBO_URL = "https://ex-api-yy5.tw946.com/"
CompanyKey = 'D75FE9768CA240E2888F0247B8364E28'
USER_BET_LOG_KEY = '8888slot_user_bet_log_redis_data'  # 用户注单队列key

from SqlConntion.RedisDB import Redis

# 获取用户列表数据
@user.route('/admin/user_sbo_bet_log_heshi', methods=['post'])
@login_required
def user_sbo_bet_log_heshi():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败！'
    if True:
    # try:
        uid = request.values.get('uid')
        user = get_user_info(uid)
        game_data = get_sbo_data(str(user['add_time']), uid)
        user_bet_arr = get_user_bet_log(str(user['add_time']), user['uid'])
        if game_data.get('result'):
            for i in game_data['result']:
                if i['refNo'] not in user_bet_arr:
                    bet_handle_func(i)
        data['code'] = 1
        data['status'] = 1
        data['msg'] = '成功！'
    # except Exception as e:
    #     print(e)
    return util.to_json(data)


def bet_handle_func(d):
    redis = Redis()
    if d['status'] in ['draw', 'lose', 'won', 'Bonus']:
        day = d['modifyDate'][:10]
        gameId = d['gameId']
        gpId = str(d['gpId'])
        game_time_hour = d['modifyDate'][:13]
        platform_bet_key = 'sbo_bet_log_' + game_time_hour
        if redis.hget(platform_bet_key, d['refNo']):
            return
        user = get_user_info(d['username'].replace('_' + constant.DBCONFIG[constant.DBINDEX]['sbo_agent'], ''))
        game = get_game_info(gameId, gpId)
        if game is None:  # 游戏或用户不存在
            print("查无此游戏", gameId, gpId, user['uid'])
            redis.hset(platform_bet_key, d['refNo'], '1')
            return
        if user is None:
            print("查无此用户", d['username'].replace('_' + constant.DBCONFIG[constant.DBINDEX]['sbo_agent'], ''))
            redis.hset(platform_bet_key, d['refNo'], '1')
            return
        user_day = str(user['add_time'])[:10] if user.get('add_time') else day
        user_flag = 0 if user_day == day else 1
        if user_flag == 0:
            user_hy_key_new = str(day) + 'user_day_game_number_new'
        else:
            user_hy_key_new = str(day) + 'user_day_game_number_old'
        user_game_key = 'san_game_user_day_flag_' + day
        redis_key_new = str(day) + 'user_day_game_number_total'
        if redis.hget(user_game_key, str(user['uid'])) is None:
            redis.hset(user_game_key, str(user['uid']), '1')
            redis.hincrby(user_hy_key_new, str(user['cid']), 1)
            redis.hincrby(redis_key_new, str(user['cid']), 1)
            redis.expire(user_hy_key_new, 86400 * 6)
            redis.expire(redis_key_new, 86400 * 6)
            redis.expire(user_game_key, 86400 * 2)
        maps = dict()
        maps['day'] = day
        maps['uid'] = user['uid']
        maps['nickname'] = user['nickname']
        maps['cid'] = user['cid']
        maps['aid'] = user['aid']
        maps['parent_id'] = user['parent_id']
        maps['super_id'] = user['super_id']
        maps['super_parent_id'] = user['super_parent_id']
        maps['gid'] = game['gid']
        maps['game_id'] = game['game_id']
        maps['my_game'] = game['my_game']
        maps['game_name'] = game['game_name']
        maps['game_type'] = game['game_type']
        maps['bet'] = d['stake']
        maps['real_shu_ying'] = d['winLost']
        maps['shu_ying'] = round(float(maps['bet']) + float(maps['real_shu_ying']), 2)
        maps['bet_num'] = 1
        maps['bet_time'] = d['modifyDate'][:19].replace('T', ' ')
        maps['game_number'] = d['refNo']
        maps['round_id'] = d['gameRoundId'] if type == 0 else d['refNo']
        maps['before_money'] = user.get('money', 0)
        maps['after_money'] = round(float(user.get('money', 0)) + float(maps['real_shu_ying']), 2)
        user['money'] = maps['after_money']
        # user_key = 'san_game_wj_game_user_conf_' + str(user['uid'])
        # redis.set(user_key, json.dumps(user))
        # redis.expire(user_key, 86400)
        redis.rpush(USER_BET_LOG_KEY, json.dumps(maps))  # 用户注单数据
        update_money_sql(maps)
        redis.hset(platform_bet_key, d['refNo'], '1')  # 设置处理标识
        print("处理成功  状态：", d['status'], "uid:", user['uid'], "输赢:", d['winLost'])


def update_money_sql(maps):
    total_activity_bet = 0
    if int(maps['game_type']) == 0:
        total_activity_bet = maps['bet']
        # 用户打码转轮打码量
        user_roller_amount(maps['uid'], total_activity_bet)
    sql = "update san_users set remain_code_amount = remain_code_amount - '%s', " \
          "total_bet = total_bet + '%s', total_shu_ying = total_shu_ying + '%s', " \
          "total_real_shu_ying = total_real_shu_ying + '%s', total_num = total_num + '%s'" \
          "  where uid = '%s'" % (total_activity_bet,
                                maps['bet'],
                                maps['shu_ying'],
                                maps['real_shu_ying'], maps['bet_num'], maps['uid'])

    if maps['parent_id'] != 0:
        user_total_recharge_activity_bet_num(maps)
    sql2 = "insert into san_user_team_day_report(uid, day, total_bet,total_activity_bet, total_win, total_real_win, total_num) " \
           "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE total_bet = total_bet + '%s', " \
           "total_win = total_win + '%s', total_real_win = total_real_win + '%s', total_num = total_num + '%s', total_activity_bet = total_activity_bet + '%s'" % \
           (maps['uid'], maps['day'], total_activity_bet, maps['bet'], maps['shu_ying'],
            maps['real_shu_ying'],
            maps['bet_num'], maps['bet'], maps['shu_ying'], maps['real_shu_ying'],
            maps['bet_num'], total_activity_bet)
    mysql = Mysql()
    try:
        res1 = mysql.update(sql, None)
        res2 = mysql.insertOne(sql2, None)
    except Exception as e:
        print(e)
    mysql.dispose()


# 累计充值奖励  汇总
def user_total_recharge_activity_bet_num(user):
    mysql = Mysql()
    try:
        sql = "insert into san_user_activity_total_data(uid, bet_num, parent_id) " \
              "values ('%s', '%s', '%s') ON DUPLICATE KEY UPDATE " \
              "bet_num = bet_num + '%s'" % (user['uid'], 1, user['parent_id'], 1)
        res = mysql.insertOne(sql, None)
    except Exception as e:
        print(e)
    mysql.dispose()


# 用户打码转轮打码量
def user_roller_amount(uid, total_activity_bet):
    try:
        redis = Redis()
        user_bet_roller_amount = redis.hget("user_bet_roller_amount", str(uid))
        if user_bet_roller_amount:
            user_bet_roller_amount = float(user_bet_roller_amount)
        else:
            user_bet_roller_amount = 0
        user_bet_roller_amount += total_activity_bet
        redis.hset("user_bet_roller_amount", str(uid), user_bet_roller_amount)
    except Exception as e:
        print(e)


# 获取用户信息
def get_user_info(uid):
    sql = "select uid, nickname, aid, cid, parent_id, super_id, super_parent_id, add_time, money from san_users " \
          "where uid = '%s'" % uid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 获取游戏
def get_game_info(gameId, gpId):
    redis = Redis()
    game_list = json.loads(redis.get('game_task_list')) if redis.get('game_task_list') else []
    if len(game_list) == 0:
        sql = "select * from san_external_game_list"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        mysql.dispose()
        if res:
            redis.set("game_task_list", json.dumps(res))
            redis.expire("game_task_list", 300)
            game_list = res
    for game in game_list:
        if str(game['my_game']) == '1' and str(game['provider_game_id']) == str(gameId) and str(
                game['provider_id']) == str(gpId):
            # print("游戏正常")
            # print()
            # print(game)
            return game
    return None


def get_user_bet_log(yesterday, uid):
    arr = []
    sql = "select game_number from san_game_bet_log where uid = '%s' and update_time >= '%s' and update_time <= '%s'" \
          % (uid, yesterday, str(get_today()))
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    if res is None:
        return arr
    for d in res:
        arr.append(str(d['game_number']))
    return arr


def get_sbo_data(add_time, uid):
    url = SBO_URL + '/web-root/restricted/report/get-bet-list-by-modify-date.aspx'
    maps = dict()
    maps['companyKey'] = CompanyKey
    maps['serverId'] = ServerId
    maps['username'] = str(uid) + "_" + constant.DBCONFIG[constant.DBINDEX]['sbo_agent']
    maps['portfolio'] = "SeamlessGame"
    date_obj = datetime.strptime(str(add_time), "%Y-%m-%d")
    new_date_obj = date_obj - timedelta(days=1)
    maps['startDate'] = str(new_date_obj)
    maps['endDate'] = str(get_today())
    maps['language'] = "zh-cn"
    print(maps)
    headers = dict()
    headers['Content-Type'] = 'application/json'
    res = requests.post(url, data=json.dumps(maps), headers=headers, verify=False)
    content = res.text
    content = json.loads(content)
    return content


# 昨日有玩游戏的用户
def get_game_data(yesterday, page):
    limit = 5000
    c_num = (page - 1) * limit
    sql = "select uid from san_user_day_game_total where day = '%s' group by uid limit %d, %d" % (
        yesterday, c_num, limit)
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


# 获取昨天的日期
def get_yes_today():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    return yesterday


# 获取今天日期
def get_today():
    now = datetime.datetime.now()
    return now