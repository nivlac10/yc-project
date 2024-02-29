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
            time.sleep(300)
        except Exception as e:
            print(e)


# 用户充值提现汇总
def task_start():
    recharge = get_recharge_success_data()
    if recharge:
        for d in recharge:
            mysql = Mysql()
            try:
                day = str(d['add_time'])[:10]
                re_day = str(d['user_time'])[:10]
                sql = "insert into san_day_money_total(day, cid, recharge_money, recharge_fee) values ('%s', " \
                      "'%s',  '%s', '%s') ON DUPLICATE KEY UPDATE recharge_money = recharge_money + '%s', " \
                      "recharge_fee = recharge_fee + '%s'" % \
                      (day, d['cid'], d['money'], d['pay_fee'], d['money'], d['pay_fee'])
                sql2 = "update san_order_list set audit_flag = 1 where id = '%s'" % d['id']
                day_key = get_update_num(int(d['day_num']))
                sql3 = "insert into san_user_day_recharge(day, cid, %s) values ('%s', '%s', '%s') ON " \
                       "DUPLICATE KEY UPDATE %s = %s + '%s'" % \
                       (day_key, re_day, d['cid'], d['money'], day_key, day_key, d['money'])
                mysql.insertOne(sql, None)
                mysql.update(sql2, None)
                mysql.insertOne(sql3, None)
            except Exception as e:
                print(e)
                mysql.dispose(2)
                continue
            mysql.dispose()
    withdraw = get_withdraw_success_data()
    if withdraw:
        for d in withdraw:
            mysql = Mysql()
            try:
                day = str(d['add_time'])[:10]
                sql = "insert into san_day_money_total(day, cid, withdraw_money, withdraw_fee) values ('%s', " \
                      "'%s', '%s', '%s') ON DUPLICATE KEY UPDATE withdraw_money = withdraw_money + '%s', " \
                      "withdraw_fee = withdraw_fee + '%s'" % \
                      (day, d['cid'], d['money'], d['pay_fee'], d['money'], d['pay_fee'])
                sql2 = "update san_withdraw_list set audit_flag = 1 where id = '%s'" % d['id']
                sql3 = "update san_users set total_withdraw = total_withdraw + '%s' where uid = '%s'" % \
                       (d['money'], d['uid'])
                sql4 = "insert into san_user_team_day_report(uid, day, total_withdraw, withdraw_num) values ('%s', " \
                       "'%s', '%s', 1) ON DUPLICATE KEY UPDATE total_withdraw = total_withdraw + '%s', " \
                       "withdraw_num = withdraw_num + 1" % (d['uid'], day, d['money'], d['money'])
                mysql.insertOne(sql, None)
                mysql.update(sql2, None)
                mysql.update(sql3, None)
                mysql.insertOne(sql4, None)
                if d['parent_id'] != '0':
                    team_key = '8888slot_team_one_withdraw_' + day
                    user_num = 0 if redis.hget(team_key, str(d['uid'])) else 1
                    sql_p = "insert into san_user_team_day_report(uid, day, team_one_withdraw, " \
                            "team_one_withdraw_user_num) values ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE " \
                            "team_one_withdraw = team_one_withdraw + '%s', " \
                            "team_one_withdraw_user_num = team_one_withdraw_user_num + '%s'" % \
                            (d['parent_id'], day, d['money'], user_num, d['money'], user_num)
                    mysql.insertOne(sql_p, None)
                    if user_num == 1:
                        redis.hset(team_key, str(d['uid']), '1')
                        redis.expire(team_key, 86400 * 3)
                if d['super_id'] != '0':
                    team_key = '8888slot_team_two_withdraw_' + day
                    user_num = 0 if redis.hget(team_key, str(d['uid'])) else 1
                    sql_s = "insert into san_user_team_day_report(uid, day, team_two_withdraw, " \
                            "team_two_withdraw_user_num) values ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE " \
                            "team_two_withdraw = team_two_withdraw + '%s', " \
                            "team_two_withdraw_user_num = team_two_withdraw_user_num + '%s'" % \
                            (d['super_id'], day, d['money'], user_num, d['money'], user_num)
                    mysql.insertOne(sql_s, None)
                    if user_num == 1:
                        redis.hset(team_key, str(d['uid']), '1')
                        redis.expire(team_key, 86400 * 3)
                if d['super_parent_id'] != '0':
                    team_key = '8888slot_team_three_withdraw_' + day
                    user_num = 0 if redis.hget(team_key, str(d['uid'])) else 1
                    sql_ps = "insert into san_user_team_day_report(uid, day, team_three_withdraw, " \
                             "team_three_withdraw_user_num) values ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE " \
                             "team_three_withdraw = team_three_withdraw + '%s', " \
                             "team_three_withdraw_user_num = team_three_withdraw_user_num + '%s'" % \
                             (d['super_parent_id'], day, d['money'], user_num, d['money'], user_num)
                    mysql.insertOne(sql_ps, None)
                    if user_num == 1:
                        redis.hset(team_key, str(d['uid']), '1')
                        redis.expire(team_key, 86400 * 3)
            except Exception as e:
                print(e)
                mysql.dispose(2)
                continue
            mysql.dispose()
    return False


# 获取更新字段
def get_update_num(day_num):
    try:
        if int(day_num) < 15:
            return 'd' + str(int(day_num) + 1)
        elif 15 <= int(day_num) < 20:
            return 'd20'
        elif 20 <= int(day_num) < 25:
            return 'd25'
        elif 25 <= int(day_num) < 30:
            return 'd30'
        else:
            return 'dother'
    except Exception as e:
        print(e)


# 获取用户提现成功数据
def get_withdraw_success_data():
    sql = "select a.id, a.success_time, a.money, a.cid, a.add_time, a.uid, a.pay_fee, b.add_time user_time, " \
          "b.parent_id, b.super_id, b.super_parent_id" \
          " from san_withdraw_list a left join san_users b on b.uid = a.uid where a.status = 1 and " \
          "a.audit_flag = 0 order by a.id asc"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


# 获取用户充值成功数据
def get_recharge_success_data():
    sql = "select a.id, a.success_time, a.money, a.cid, a.add_time, a.uid, a.pay_fee, " \
          "datediff(a.add_time, b.add_time) day_num, b.add_time user_time, b.parent_id, b.super_id, " \
          "b.super_parent_id from san_order_list a LEFT JOIN " \
          "san_users b on b.uid = a.uid where a.status = 1 and a.audit_flag = 0 order by id asc"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res

if __name__ == "__main__":
    daemonize('/dev/null', '/tmp/san_user_money_log.txt', '/tmp/san_user_money_log_error.txt')
    main()
