#!/usr/bin/env python
# coding: utf-8
import datetime
import importlib
import json
import os
import redis
import sys
from MysqlConn import Mysql
import Config
from MongoDBConn import MongoDB

importlib.reload(sys)
pool = redis.ConnectionPool(host=Config.R_host, port='6379', db=Config.R_db, password='', decode_responses=True)
redis = redis.Redis(connection_pool=pool)
USER_BET_LOG_KEY = '8888slot_user_bet_log_redis_data'  # 用户注单队列key

"""
将当前进程fork为一个守护进程
注意：如果你的守护进程是由inetd启动的，不要这样做！inetd完成了
所有需要做的事情，包括重定向标准文件描述符，需要做的事情只有chdir()和umask()了
"""

# 运行时的log输出的文件路径
run_log = ''
# 发生错误时的log输出的文件路径
err_log = ''


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # 重定向标准文件描述符（默认情况下定向到/dev/null）
    try:
        pid = os.fork()
        # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            sys.exit(0)  # 父进程退出
    except OSError as e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 从母体环境脱离
    os.chdir("/")  # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.umask(0)  # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()  # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # 第二个父进程退出
    except OSError as e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 进程已经是守护进程了，重定向标准文件描述符

    for f in sys.stdout, sys.stderr:
        f.flush()
    si = open(stdin, 'rb', 0)
    so = open(stdout, 'a+')
    se = open(stderr, 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())  # dup2函数原子化关闭和复制文件描述符
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


# 示例函数：每秒打印一个数字和时间戳
def main():
    import time
    while True:
        try:
            con = task_start()
            if con is False:
                time.sleep(5)
        except Exception as e:
            print(e)


# 注单数据处理
def task_start():
    arr = []
    for d in range(5000):
        res = redis.lpop(USER_BET_LOG_KEY)
        if res is None:
            break
        arr.append(json.loads(res))
    if len(arr) == 0:
        return False
    bet_data_func(arr)
    bet_log_func(arr)


# 数据处理
def bet_data_func(arr):
    maps = dict()
    for d in arr:
        user_key = str(d['day']) + '_' + str(d['uid']) + '_' + str(d['gid'])
        if user_key not in maps:
            user = dict()
            user['uid'] = d['uid']
            user['cid'] = d['cid']
            user['day'] = d['day']
            user['my_game'] = d['my_game']
            user['game_id'] = d['game_id']
            user['gid'] = d['gid']
            user['game_type'] = d['game_type']
            user['bet_num'] = 1
            user['bet'] = float(d['bet'])
            user['shu_ying'] = float(d['shu_ying'])
            user['real_shu_ying'] = float(d['real_shu_ying'])
            user['parent_id'] = d['parent_id']
            user['super_id'] = d['super_id']
            user['super_parent_id'] = d['super_parent_id']
            user['add_time'] = d['add_time']
            maps[user_key] = user
        else:
            maps[user_key]['bet_num'] += 1
            maps[user_key]['bet'] += float(d['bet'])
            maps[user_key]['shu_ying'] += float(d['shu_ying'])
            maps[user_key]['real_shu_ying'] += float(d['real_shu_ying'])
    if maps:
        bet_data_sql_func(maps)


def bet_data_sql_func(total):
    for x in total:
        total[x]['bet'] = round(total[x]['bet'], 2)
        total[x]['shu_ying'] = round(total[x]['shu_ying'], 2)
        total[x]['real_shu_ying'] = round(total[x]['real_shu_ying'], 2)
        sql = "insert into san_game_wj_user_day_total (day, cid, game_id, gid, my_game, uid, game_type, " \
              "total_bet, total_shu_ying, total_real_shu_ying, total_num) values ('%s', '%s', '%s', '%s', '%s', " \
              "'%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE total_bet = total_bet + '%s', " \
              "total_shu_ying = total_shu_ying + '%s', total_real_shu_ying = total_real_shu_ying + '%s', " \
              "total_num = total_num + '%s'" % \
              (total[x]['day'], total[x]['cid'], total[x]['game_id'], total[x]['gid'], total[x]['my_game'],
               total[x]['uid'], total[x]['game_type'], total[x]['bet'], total[x]['shu_ying'],
               total[x]['real_shu_ying'], total[x]['bet_num'], total[x]['bet'], total[x]['shu_ying'],
               total[x]['real_shu_ying'], total[x]['bet_num'])
        sql4 = "insert into san_game_day_total(day, game_id, cid, total_bet, total_shu_ying, " \
               "total_real_shu_ying, total_cover_charge,total_num) values ('%s', '%s', '%s','%s', '%s', " \
               "'%s', '%s', 1) ON DUPLICATE KEY UPDATE total_bet = total_bet + '%s', " \
               "total_shu_ying = total_shu_ying + '%s', total_real_shu_ying = total_real_shu_ying + '%s', " \
               "total_cover_charge = total_cover_charge + '%s', total_num = total_num + 1" % \
               (total[x]['day'], total[x]['game_id'], total[x]['cid'], total[x]['bet'], total[x]['shu_ying'],
                total[x]['real_shu_ying'],
                0, total[x]['bet'], total[x]['shu_ying'], total[x]['real_shu_ying'], 0)
        sql5 = "insert into san_day_money_total(day, cid, total_bet, total_shu_ying, total_real_shu_ying, " \
               "total_cover_charge) values ('%s', '%s', '%s', '%s', '%s', '%s') ON " \
               "DUPLICATE KEY UPDATE total_bet = total_bet + '%s', total_shu_ying = total_shu_ying + '%s', " \
               "total_real_shu_ying = total_real_shu_ying + '%s',total_cover_charge = total_cover_charge + '%s'" % \
               (total[x]['day'], total[x]['cid'], total[x]['bet'], total[x]['shu_ying'], total[x]['real_shu_ying'], 0,
                total[x]['bet'], total[x]['shu_ying'], total[x]['real_shu_ying'], 0)
        sql6 = "insert into san_user_day_game_total(uid, day, game_id, cid, total_bet, total_shu_ying, " \
               "total_real_shu_ying, total_cover_charge, total_num) values ('%s', '%s', '%s', '%s', '%s', " \
               "'%s', '%s', '%s', 1) ON DUPLICATE KEY UPDATE total_bet = total_bet + '%s', " \
               "total_shu_ying = total_shu_ying + '%s', total_real_shu_ying = total_real_shu_ying + '%s', " \
               "total_cover_charge = total_cover_charge + '%s', total_num = total_num + 1" % \
               (total[x]['uid'], total[x]['day'], total[x]['game_id'], total[x]['cid'], total[x]['bet'],
                total[x]['shu_ying'], total[x]['real_shu_ying'],
                0, total[x]['bet'], total[x]['shu_ying'], total[x]['real_shu_ying'], 0)
        sql7 = "insert into san_game_wj_day_total (day, cid, game_id, gid, my_game, game_type, total_bet, " \
               "total_shu_ying, total_real_shu_ying, total_num) values ('%s', '%s', '%s', '%s', '%s', " \
               "'%s', '%s', '%s', '%s', 1) ON DUPLICATE KEY UPDATE total_bet = total_bet + '%s', " \
               "total_shu_ying = total_shu_ying + '%s', total_real_shu_ying = total_real_shu_ying + '%s', " \
               "total_num = total_num + 1" % \
               (total[x]['day'], total[x]['cid'], total[x]['game_id'], total[x]['gid'], total[x]['my_game'],
                total[x]['game_type'], total[x]['bet'], total[x]['shu_ying'],
                total[x]['real_shu_ying'], total[x]['bet'], total[x]['shu_ying'], total[x]['real_shu_ying'])
        mysql = Mysql()
        if total[x]['parent_id'] != '0':
            sql_parent = "update san_users set team_one_bet = team_one_bet + '%s' where uid = '%s'" % \
                         (total[x]['bet'], total[x]['parent_id'])
            sql_parent_total = "insert into san_user_team_day_report(day, uid, team_one_bet) values " \
                               "('%s', '%s', '%s') ON DUPLICATE KEY UPDATE team_one_bet = " \
                               "team_one_bet + '%s'" % (
                                   total[x]['day'], total[x]['parent_id'], total[x]['bet'], total[x]['bet'])
            mysql.update(sql_parent, None)
            mysql.insertOne(sql_parent_total, None)
        if total[x]['super_id'] != '0':
            sql_super = "update san_users set team_two_bet = team_two_bet + '%s' where uid = '%s'" % \
                        (total[x]['bet'], total[x]['super_id'])
            sql_super_total = "insert into san_user_team_day_report(day, uid, team_two_bet) values ('%s', '%s', " \
                              "'%s') ON DUPLICATE KEY UPDATE team_two_bet = team_two_bet + '%s'" % \
                              (total[x]['day'], total[x]['super_id'], total[x]['bet'], total[x]['bet'])
            mysql.update(sql_super, None)
            mysql.insertOne(sql_super_total, None)
        if total[x]['super_parent_id'] != '0':
            sql_super_parent = "update san_users set team_three_bet = team_three_bet + '%s' where uid = '%s'" % \
                               (total[x]['bet'], total[x]['super_parent_id'])
            super_parent_total = "insert into san_user_team_day_report(day, uid, team_three_bet) values ('%s', " \
                                 "'%s', '%s') ON DUPLICATE KEY UPDATE team_three_bet = team_three_bet + '%s'" % \
                                 (total[x]['day'], total[x]['super_parent_id'], total[x]['bet'], total[x]['bet'])
            mysql.update(sql_super_parent, None)
            mysql.insertOne(super_parent_total, None)
        try:
            user_day = str(total[x]['add_time'])[:10] if total[x]['add_time'] else total[x]['day']
            user_flag = 0 if user_day == total[x]['day'] else 1
            if user_flag == 0:
                user_hy_key_new = str(total[x]['day']) + 'user_day_game_number_new'
            else:
                user_hy_key_new = str(total[x]['day']) + 'user_day_game_number_old'
            redis_key_new = str(total[x]['day']) + 'user_day_game_number_total'
            user_game_key = 'san_game_user_day_flag_' + str(total[x]['day'])
            if redis.hget(user_game_key, str(total[x]['uid'])) is None:
                redis.hset(user_game_key, str(total[x]['uid']), '1')
                redis.hincrby(user_hy_key_new, str(total[x]['cid']), 1)
                redis.hincrby(redis_key_new, str(total[x]['cid']), 1)
                redis.expire(user_hy_key_new, 86400 * 6)
                redis.expire(redis_key_new, 86400 * 6)
                redis.expire(user_game_key, 86400 * 2)
            mysql.insertOne(sql, None)
            mysql.insertOne(sql4, None)
            mysql.insertOne(sql5, None)
            mysql.insertOne(sql6, None)
            mysql.insertOne(sql7, None)
            update_money_sql(total[x])
            if int(total[x]['game_type']) == 0:
                user_get_num = redis.hget("user_vip_get_num_" + str(total[x]['day']), str(total[x]['uid']))
                user_get_num = int(user_get_num) if user_get_num else 0
                user_vip_day_bonus_count(total[x])
                if user_get_num < 11:
                    user_vip_code_amount_key = "vip_code_amount" + str(total[x]['day'])
                    code = redis.hget(user_vip_code_amount_key, str(total[x]['uid']))
                    user_vip_code = float(code) + float(total[x]['bet']) if code else total[x]['bet']
                    redis.hset(user_vip_code_amount_key, str(total[x]['uid']), str(round(float(user_vip_code), 2)))
                    redis.expire(user_vip_code_amount_key, 86400 * 2)
        except Exception as e:
            print(e)
        mysql.dispose()


#  用户每日打码累计
def user_vip_day_bonus_count(data):
    user_vip_day_code_amount_key = "vip_day_code_amount_" + str(data['day'])
    day_code = redis.hget(user_vip_day_code_amount_key, str(data['uid']))
    user_vip_code = float(day_code) + float(data['bet']) if day_code else data['bet']
    redis.hset(user_vip_day_code_amount_key, str(data['uid']), str(round(float(user_vip_code), 2)))
    redis.expire(user_vip_day_code_amount_key, 86400 * 2)

# 累计充值奖励  汇总
def user_total_recharge_activity_bet_num(user):
    mysql = Mysql()
    try:
        sql = "insert into san_user_activity_total_data(uid, bet_num, parent_id) " \
                        "values ('%s', '%s', '%s') ON DUPLICATE KEY UPDATE " \
                        "bet_num = bet_num + '%s'" % (user['uid'], 1, user['parent_id'], user['bet_num'])
        res = mysql.insertOne(sql, None)
    except Exception as e:
        print(e)
    mysql.dispose()


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


# 用户打码转轮打码量
def user_roller_amount(uid, total_activity_bet):
    try:
        user_bet_roller_amount = redis.hget("user_bet_roller_amount", str(uid))
        if user_bet_roller_amount:
            user_bet_roller_amount = float(user_bet_roller_amount)
        else:
            user_bet_roller_amount = 0
        user_bet_roller_amount += total_activity_bet
        redis.hset("user_bet_roller_amount", str(uid), user_bet_roller_amount)
    except Exception as e:
        print(e)


# 注单处理
def bet_log_func(arr):
    try:
        new_arr = arr
        for d in new_arr:
            d['add_time'] = str(get_today())
        mongodb = MongoDB()
        res = mongodb.insert_many("san_game_bet_log", arr)
        mongodb.close()
    except Exception as e:
        for d in arr:
            redis.rpush(USER_BET_LOG_KEY, json.dumps(d))



# 获取今天日期
def get_today():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now

if __name__ == "__main__":
    daemonize('/dev/null', '/tmp/san_awc_bet_date.txt', '/tmp/san_awc_bet_date_error.txt')
    main()
    # task_start()
