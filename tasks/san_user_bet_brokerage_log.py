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
            time.sleep(600)
        except Exception as e:
            print(e)


def task_start():
    hour = time.strftime("%H")
    if int(hour) < 3:
        return
    yesterday = get_yes_today()
    task_key = 'san_user_bet_brokerage_log_flag_' + str(yesterday)
    if redis.get(task_key):
        return True
    page = 1
    while True:
        res = get_game_data(yesterday, page)
        if res is None:
            break
        for d in res:
            user = get_user_info(d['uid'])
            if user is None:
                continue
            if user['parent_id'] == 0:
                continue
            user_bet_brokerage_func(d, user)
        page += 1
    redis.set(task_key, '1', ex=86400 * 7)


# 用户打码返佣数据处理
def user_bet_brokerage_func(data, user):
    if str(user['parent_id']) != '0':
        one_ratio = redis.hget('san_game_all_conf', 'one_bet_rebate') or 0.5
        add_bet_brokerage(one_ratio, 1, user['parent_id'], data['uid'], data['day'], data['bet'])
    if str(user['super_id']) != '0':
        two_ratio = redis.hget('san_game_all_conf', 'two_bet_rebate') or 0.5*0.3
        add_bet_brokerage(two_ratio, 2, user['super_id'], data['uid'], data['day'], data['bet'])
    if str(user['super_parent_id']) != '0':
        three_ratio = redis.hget('san_game_all_conf', 'three_bet_rebate') or 0.5*0.3*0.3
        add_bet_brokerage(three_ratio, 3, user['super_parent_id'], data['uid'], data['day'], data['bet'])


# 添加打码佣金记录
def add_bet_brokerage(ratio, lv_num, uid, game_uid, day, bet):
    money = round(float(bet)*float(ratio)/100, 2)
    mysql = Mysql()
    try:
        sql = "insert into san_user_day_brokerage(uid, day, lv_num, game_uid, game_bet, money, add_time) values " \
              "('%s', '%s', '%s', '%s', '%s', '%s', now())" % (uid, day, lv_num, game_uid, bet, money)
        mysql.insertOne(sql, None)
    except Exception as e:
        print(e)
    mysql.dispose()


# 获取用户信息
def get_user_info(uid):
    sql = "select * from san_users where uid = '%s'" % uid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


def get_game_data(day, page):
    limit = 5000
    c_num = (page - 1) * limit
    sql = "select sum(total_bet) bet, uid, day from san_game_wj_user_day_total where day = '%s' " \
          "group by uid order by uid desc limit %d, %d" % (day, c_num, limit)
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


# 获取昨天的日期
def get_yes_today():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')



if __name__ == "__main__":
    daemonize('/dev/null', '/tmp/san_user_bet_brokerage_log.txt', '/tmp/san_user_bet_brokerage_log_error.txt')
    main()
