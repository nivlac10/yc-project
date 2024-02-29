#!/usr/bin/env python
# coding: utf-8
import datetime
import importlib
import json
import os
import time

import redis
import sys
from MysqlConn import Mysql
import Config

importlib.reload(sys)
pool = redis.ConnectionPool(host=Config.R_host, port='6379', db=Config.R_db, password='', decode_responses=True)
redis = redis.Redis(connection_pool=pool)

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
            time.sleep(120)
        except Exception as e:
            print(e)


MONEY_TYPE = {
    'team_recharge_brokerage': 'first_recharge_brokerage',
    'team_invite_task_brokerage': 'invite_task_brokerage',
    'team_one_bet_brokerage': 'one_bet_brokerage',
    'team_two_bet_brokerage': 'two_bet_brokerage',
    'team_three_bet_brokerage': 'three_bet_brokerage',
    'vip_up': 'vip_up',
    'vip_week': 'vip_week',
    'vip_month': 'vip_month',
    'vip_earnings': 'user_rebate',
    'first_recharge_give': 'user_first_recharge',
    'day_first_recharge_give': 'user_day_first_recharge',
    'system_give': 'system_give',
    'give_money': 'total_give_money'
}


# 日汇总
def task_start():
    yes_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    now_day = str(time.strftime('%Y-%m-%d'))
    hour = time.strftime("%H")
    hour = int(hour)
    if int(hour) < 1:
        yes_data, user_money = get_give_data(yes_str)
        if yes_data or user_money:
            data_func(yes_data, user_money, yes_str)
    now_data, user_money = get_give_data(now_day)
    if now_data or user_money:
        data_func(now_data, user_money, now_day)


# 数据处理
def data_func(data, user_money, day):
    try:
        if data:
            for d in data:
                sql = "insert into san_day_money_total(day, cid, first_recharge_brokerage, invite_task_brokerage, " \
                      "one_bet_brokerage, two_bet_brokerage, three_bet_brokerage, vip_up, vip_week, vip_month, " \
                      "user_rebate, user_first_recharge, user_day_first_recharge, system_give, total_give_money" \
                      ",vip_day ,vip_now,vip_split, loss_bonus, sign_bonus) values " \
                      "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" \
                      ", '%s', '%s', '%s', '%s', '%s') ON " \
                      "DUPLICATE KEY UPDATE first_recharge_brokerage = '%s', invite_task_brokerage = '%s', " \
                      "one_bet_brokerage = '%s', two_bet_brokerage = '%s', three_bet_brokerage = '%s', " \
                      "vip_up = '%s', vip_week = '%s', vip_month = '%s', user_rebate = '%s', user_first_recharge = '%s', " \
                      "user_day_first_recharge = '%s', system_give = '%s', total_give_money = '%s'" \
                      ", vip_day='%s',vip_now='%s',vip_split='%s',loss_bonus='%s',sign_bonus='%s'" % \
                      (day, d['cid'], d['team_recharge_brokerage'], d['team_invite_task_brokerage'],
                       d['team_one_bet_brokerage'], d['team_two_bet_brokerage'], d['team_three_bet_brokerage'], d['vip_up'],
                       d['vip_week'], d['vip_month'], d['vip_earnings'], d['first_recharge_give'],
                       d['day_first_recharge_give'], d['system_give'],
                       d['vip_day'], d['vip_now'], d['vip_split'], d['loss_bonus'], d['sign_bonus'],
                       d['give_money'], d['team_recharge_brokerage'],
                       d['team_invite_task_brokerage'], d['team_one_bet_brokerage'], d['team_two_bet_brokerage'],
                       d['team_three_bet_brokerage'], d['vip_up'], d['vip_week'], d['vip_month'], d['vip_earnings'],
                       d['first_recharge_give'], d['day_first_recharge_give'], d['system_give'], d['give_money']
                       , d['vip_day'], d['vip_now'], d['vip_split'], d['loss_bonus'], d['sign_bonus'])
                mysql = Mysql()
                try:
                    result = mysql.insertOne(sql, None)
                except Exception as e:
                    print(e)
                mysql.dispose()
        if user_money:
            for d in user_money:
                sql = "insert into san_day_money_total(day, cid, user_total_money) values " \
                      "('%s', '%s', '%s') ON " \
                      "DUPLICATE KEY UPDATE user_total_money = '%s'" %(d['day'], d['cid'], d['money'], d['money'])
                mysql = Mysql()
                try:
                    result = mysql.insertOne(sql, None)
                except Exception as e:
                    print(e)
                mysql.dispose()
    except Exception as e:
        print(e)


# 获取赠送数据
def get_give_data(day):
    arr = ['team_recharge_brokerage', 'team_invite_task_brokerage', 'team_one_bet_brokerage', 'team_two_bet_brokerage',
           'team_three_bet_brokerage', 'vip_up', 'vip_day', 'vip_week', 'vip_month', 'vip_now', 'vip_split',
           'vip_earnings', 'sign_bonus', 'loss_bonus',
           'first_recharge_give',
           'day_first_recharge_give', 'system_give', 'give_money']
    sum_content = sum_key(arr)
    sql = "select %s, b.cid from san_user_team_day_report a left join san_users b on b.uid = a.uid where " \
          "a.day = '%s' group by b.cid" % (sum_content, day)
    sql2 = "select cid, sum(money) money from san_users group by cid"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    res2 = mysql.getAll(sql2, None)
    mysql.dispose()
    if res2:
        for d in res2:
            d['day'] = day
    return res, res2


def sum_key(arr):
    content = ''
    for d in arr:
        content += 'sum(a.' + d + ') ' + d + ','
    return content[:-1]


if __name__ == "__main__":
    daemonize('/dev/null', '/tmp/san_game_give_total.txt', '/tmp/san_game_give_total_error.txt')
    main()
    # task_start()