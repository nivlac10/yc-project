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


# 获取昨天的所有游戏数据
def task_start():
    hour = time.strftime("%H")
    if int(hour) < 3:
        return
    yes_str = yes_day_str()
    task_key = "user_active_flag" + str(yes_str)
    if redis.get(task_key):
        return
    try:
        s_day, e_day, user_day = get_yes_day()
        sql = "select count(uid) num, day, cid, day_num from (select distinct a.uid, a.cid, b.add_time, " \
              "DATE_FORMAT(b.add_time,'%%Y-%%m-%%d') day, datediff(CURDATE(), b.add_time) day_num from " \
              "san_game_bet_log a left join san_users b on b.uid = a.uid where a.add_time >= '%s' and " \
              "a.add_time < '%s' and b.add_time >= '%s') a GROUP BY a.day, a.cid" % (s_day, e_day, user_day)
        # print sql
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        mysql.dispose()
        if res:
            mysql = Mysql()
            for d in res:
                try:
                    key_day = 'd' + str(int(d['day_num']))
                    sql = "insert into san_user_active_data(day, cid, %s) values ('%s', '%s', '%s') ON " \
                          "DUPLICATE KEY UPDATE %s ='%s'" % \
                          (key_day, d['day'], d['cid'], d['num'], key_day, d['num'])
                    mysql.insertOne(sql, None)
                except Exception as e:
                    print(e)
                    continue
            mysql.dispose()
        redis.set(task_key, '1', ex=86400*10)
    except Exception as e:
        print(e)


# 获取昨天的日期
def yes_day_str():
    day = time.strftime("%Y-%m-%d")
    end_int = int(time.mktime(time.strptime(day, '%Y-%m-%d')))
    return time.strftime('%Y-%m-%d', time.localtime(end_int - 86400))


# 获取昨天的时间
def get_yes_day():
    day = time.strftime("%Y-%m-%d")
    end_int = int(time.mktime(time.strptime(day, '%Y-%m-%d')))
    start_int = end_int - 86400
    user_int = end_int - 7*86400
    s_day = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_int))
    e_day = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_int))
    user_day = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user_int))
    return s_day, e_day, user_day


if __name__ == "__main__":
    daemonize('/dev/null', '/tmp/san_user_active_log.txt', '/tmp/san_user_active_log_error.txt')
    main()
