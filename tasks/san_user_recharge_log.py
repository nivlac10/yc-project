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
from datetime import timedelta

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


# 任务开始
def task_start():
    yes_str = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    now_day = str(time.strftime('%Y-%m-%d'))
    hour = time.strftime("%H")
    hour = int(hour)
    if int(hour) < 5:
        try:
            update_day_game_user_data(yes_str)
            res = get_day_recharge_data(yes_str)
            if res:
                data_content(res, yes_str)
            with_res = get_day_withdraw_data(yes_str)
            if with_res:
                withdraw_data_content(with_res, yes_str)
            xd_data = get_day_recharge_xd_data(yes_str)
            if xd_data:
                data_recharge_xd_content(xd_data, yes_str)
        except Exception as e:
            print(e)
    try:
        update_day_game_user_data(now_day)
        now_data = get_day_recharge_data(now_day)
        if now_data:
            data_content(now_data, now_day)
        now_with = get_day_withdraw_data(now_day)
        if now_with:
            withdraw_data_content(now_with, now_day)
        xd_data = get_day_recharge_xd_data(now_day)
        if xd_data:
            data_recharge_xd_content(xd_data, now_day)
    except Exception as e:
        print(e)
    return True


# 提现数据处理
def withdraw_data_content(data, day):
    if data is None:
        return
    mysql = Mysql()
    for d in data:
        try:
            old_withdraw_result_num = int(d['old_withdraw_result_num']) if d['old_withdraw_result_num'] else 0
            new_withdraw_result_num = int(d['new_withdraw_result_num']) if d['new_withdraw_result_num'] else 0
            old_user_withdraw_num = int(d['old_user_withdraw_num']) if d['old_user_withdraw_num'] else 0
            new_user_withdraw_num = int(d['new_user_withdraw_num']) if d['new_user_withdraw_num'] else 0
            new_user_withdraw = float(d['new_user_withdraw']) if d['new_user_withdraw'] else 0
            old_user_withdraw = float(d['old_user_withdraw']) if d['old_user_withdraw'] else 0
            withdraw_money = float(d['withdraw_money']) if d['withdraw_money'] else 0
            withdraw_fee = float(d['withdraw_fee']) if d['withdraw_fee'] else 0
            sql = "insert into san_day_money_total(day, cid, old_withdraw_result_num, new_withdraw_result_num, " \
                  "old_user_withdraw_num, new_user_withdraw_num, new_user_withdraw, old_user_withdraw, " \
                  "withdraw_money, withdraw_fee) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') " \
                  "ON DUPLICATE KEY UPDATE old_withdraw_result_num = '%s', new_withdraw_result_num = '%s', " \
                  "old_user_withdraw_num = '%s', new_user_withdraw_num = '%s', new_user_withdraw = '%s', " \
                  "old_user_withdraw = '%s', withdraw_money = '%s', withdraw_fee = '%s'" % \
                  (day, d['cid'], old_withdraw_result_num, new_withdraw_result_num,
                   old_user_withdraw_num, new_user_withdraw_num, new_user_withdraw, old_user_withdraw, withdraw_money,
                   withdraw_fee, old_withdraw_result_num, new_withdraw_result_num, old_user_withdraw_num,
                   new_user_withdraw_num, new_user_withdraw, old_user_withdraw, withdraw_money, withdraw_fee)
            mysql.insertOne(sql, None)
        except Exception as e:
            print(e)
            print(sql)
            mysql.dispose(2)
            return
    mysql.dispose()


# 充值下单数据处理
def data_recharge_xd_content(data, day):
    if data is None:
        return
    mysql = Mysql()
    for d in data:
        try:
            new_num = int(d['new_num']) if d['new_num'] else 0
            old_num = int(d['old_num']) if d['old_num'] else 0
            new_user_xd_num = int(d['new_user_xd_num']) if d['new_user_xd_num'] else 0
            old_user_xd_num = int(d['old_user_xd_num']) if d['old_user_xd_num'] else 0
            new_order_num = int(d['new_order_num']) if d['new_order_num'] else 0
            old_order_num = int(d['old_order_num']) if d['old_order_num'] else 0
            new_user_order_num = int(d['new_user_order_num']) if d['new_user_order_num'] else 0
            old_user_order_num = int(d['old_user_order_num']) if d['old_user_order_num'] else 0
            sql = "insert into san_day_money_total(day, cid, new_num, old_num, new_user_xd_num, old_user_xd_num, " \
                  "new_order_num, old_order_num, new_user_order_num, old_user_order_num) values ('%s', '%s', '%s', " \
                  "'%s', '%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE new_num = '%s', " \
                  "old_num = '%s', new_user_xd_num = '%s', old_user_xd_num = '%s', new_order_num = '%s', " \
                  "old_order_num = '%s', new_user_order_num = '%s', old_user_order_num = '%s'" % \
                  (day, d['cid'], new_num, old_num, new_user_xd_num, old_user_xd_num, new_order_num,
                   old_order_num, new_user_order_num, old_user_order_num, new_num, old_num, new_user_xd_num,
                   old_user_xd_num, new_order_num, old_order_num, new_user_order_num, old_user_order_num)
            mysql.insertOne(sql, None)
        except Exception as e:
            print(e, "func data_recharge_xd_content", time.strftime("%Y-%m-%d %H:%M:%S"))
            print(sql)
    mysql.dispose()


# 充值数据处理
def data_content(data, day):
    if data is None:
        return
    mysql = Mysql()
    for d in data:
        try:
            new_user_recharge = float(d['new_user_recharge']) if d['new_user_recharge'] else 0
            new_user_num = int(d['new_user_num']) if d['new_user_num'] else 0
            old_user_recharge = float(d['old_user_recharge']) if d['old_user_recharge'] else 0
            old_user_num = int(d['old_user_num']) if d['old_user_num'] else 0
            result_num = int(d['result_num']) if d['result_num'] else 0
            result_user_num = int(d['result_user_num']) if d['result_user_num'] else 0
            old_result_num = int(d['old_result_num']) if d['old_result_num'] else 0
            new_result_num = int(d['new_result_num']) if d['new_result_num'] else 0
            recharge_money = float(d['recharge_money']) if d['recharge_money'] else 0
            recharge_fee = float(d['recharge_fee']) if d['recharge_fee'] else 0
            sql = "insert into san_day_money_total(day, cid, new_user_recharge, new_user_num, " \
                  "old_user_recharge, old_user_num, result_num, result_user_num, old_result_num, new_result_num, " \
                  "recharge_money, recharge_fee) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                  "'%s', '%s') ON DUPLICATE KEY UPDATE new_user_recharge = '%s', new_user_num = '%s', " \
                  "old_user_recharge = '%s', old_user_num = '%s', result_num = '%s', result_user_num = '%s', " \
                  "old_result_num = '%s', new_result_num = '%s', recharge_money = '%s', recharge_fee = '%s'" % \
                  (day, d['cid'], new_user_recharge, new_user_num, old_user_recharge,
                   old_user_num, result_num, result_user_num, old_result_num, new_result_num, recharge_money,
                   recharge_fee,  new_user_recharge, new_user_num, old_user_recharge,old_user_num, result_num,
                   result_user_num, old_result_num, new_result_num, recharge_money, recharge_fee)
            mysql.insertOne(sql, None)
        except Exception as e:
            print(e, "func data_content", time.strftime("%Y-%m-%d %H:%M:%S"))
            print(sql)
            mysql.dispose(2)
            return
    mysql.dispose()


# 没有数据的时候更新游戏数据
def update_day_game_user_data(day):
    update_total_user_game_data(day)  # 总日活
    update_new_user_game_data(day)   # 新客游戏日活
    update_old_user_game_data(day)   # 老客游戏日活
    update_user_install_data(day)   # 安装上报
    update_register_data(day)       # 更新注册数
    update_old_user_login_data(day)   # 更新老客登陆数据


# 更新老客登陆大厅数据
def update_old_user_login_data(day):
    old_user_life_login_key = 'old_user_life_login_key_' + day
    res = redis.hgetall(old_user_life_login_key)
    if res:
        for d in res:
            sql = "insert into san_day_money_total(day, cid, old_user_life) values ('%s', '%s', '%s') ON " \
                  "DUPLICATE KEY UPDATE old_user_life = '%s'" % (day, d, res[d], res[d])
            mysql = Mysql()
            try:
                mysql.insertOne(sql, None)
            except Exception as e:
                print(e)
            mysql.dispose()


# 更新注册数
def update_register_data(day):
    flag_list = ["phone_num", "face_num"]
    for d in flag_list:
        redis_total_key = day + '_san_game_register_' + d
        res = redis.hgetall(redis_total_key)
        if res:
            for k in res:
                sql = "insert into san_day_money_total(day, cid, %s) values ('%s', '%s', '%s') ON DUPLICATE " \
                      "KEY UPDATE %s = '%s'" % (d, day, k, res[k], d, res[k])
                mysql = Mysql()
                try:
                    mysql.insertOne(sql, None)
                except Exception as e:
                    print(e)
                mysql.dispose()


# 更新老客日活数据
def update_old_user_game_data(day):
    redis_key_new = str(day) + 'user_day_game_number_old'
    data = redis.hgetall(redis_key_new)
    if data:
        mysql = Mysql()
        for d in data:
            sql = "insert into san_day_money_total(day, cid, old_game_num) values ('%s', '%s', " \
                  "'%s') ON DUPLICATE KEY UPDATE old_game_num = '%s'" % \
                  (day, d, data[d], data[d])
            mysql.insertOne(sql, None)
        mysql.dispose()


# 更新新客日活数据
def update_new_user_game_data(day):
    redis_key_new = str(day) + 'user_day_game_number_new'
    data = redis.hgetall(redis_key_new)
    if data:
        mysql = Mysql()
        for d in data:
            sql = "insert into san_day_money_total(day, cid, new_game_num) values ('%s', '%s', " \
                  "'%s') ON DUPLICATE KEY UPDATE new_game_num = '%s'" % \
                  (day, d, data[d], data[d])
            mysql.insertOne(sql, None)
        mysql.dispose()


# 更新总活跃人数
def update_total_user_game_data(day):
    redis_key_new = str(day) + 'user_day_game_number_total'
    data = redis.hgetall(redis_key_new)
    if data:
        mysql = Mysql()
        for d in data:
            sql = "insert into san_day_money_total(day, cid, game_num) values ('%s', '%s', " \
                  "'%s') ON DUPLICATE KEY UPDATE game_num = '%s'" % \
                  (day, d, data[d], data[d])
            mysql.insertOne(sql, None)
        mysql.dispose()


# 更新安装上报数据
def update_user_install_data(day):
    redis_key = "day_user_install_report_" + str(day)
    data = redis.hgetall(redis_key)
    if data:
        mysql = Mysql()
        for d in data:
            try:
                sql = "insert into san_day_money_total(day, cid, install_num) values ('%s', '%s', " \
                      "'%s') ON DUPLICATE KEY UPDATE install_num = '%s'" % \
                      (day, d, data[d], data[d])
                mysql.insertOne(sql, None)
            except Exception as e:
                print(e, "func update_user_install_data", time.strftime("%Y-%m-%d %H:%M:%S"))
                print(sql)
        mysql.dispose()


# 获取每日充值下单数据
def get_day_recharge_xd_data(day):
    end_day = day + " 23:59:59"
    res = None
    sql = "select count(distinct id, if(new_user_flag = 0, true, null)) new_num, " \
          "count(distinct id, if(new_user_flag = 1, true, null)) old_num," \
          "count(distinct uid, if(new_user_flag = 0, true, null)) new_user_xd_num, " \
          "count(distinct uid, if(new_user_flag = 1, true, null)) old_user_xd_num," \
          "count(distinct id, if(new_user_flag = 0 and status != 3, true, null)) new_order_num," \
          "count(distinct id, if(new_user_flag = 1 and status != 3, true, null)) old_order_num," \
          "count(distinct uid, if(new_user_flag = 0 and status != 3, true, null)) new_user_order_num, " \
          "count(distinct uid, if(new_user_flag = 1 and status != 3, true, null)) old_user_order_num, cid from " \
          "san_order_list where add_time >= '%s' and add_time <= '%s' group by cid" % (day, end_day)
    mysql = Mysql()
    try:
        res = mysql.getAll(sql, None)
    except Exception as e:
        print(e, "func get_day_recharge_xd_data", time.strftime("%Y-%m-%d %H:%M:%S"))
        print(sql)
    mysql.dispose()
    return res


# 获取每日充值数据
def get_day_recharge_data(day):
    end_day = day + " 23:59:59"
    res = None
    sql = "select count(*) result_num, count(distinct uid, if(new_user_flag = 1, true, null)) old_user_num, cid, " \
          "count(distinct uid, if(new_user_flag = 0, true, null)) new_user_num, count(distinct uid) result_user_num," \
          "sum(if(new_user_flag = 0, money, 0)) new_user_recharge, " \
          "sum(if(new_user_flag = 1, money, 0)) old_user_recharge, " \
          "count(distinct id, if(new_user_flag = 1, true, null)) old_result_num," \
          "count(distinct id, if(new_user_flag = 0, true, null)) new_result_num, sum(money) recharge_money, " \
          "sum(pay_fee) recharge_fee " \
          "from san_order_list where add_time >= '%s' and add_time <= '%s' and status = 1 group by cid" % (day, end_day)
    mysql = Mysql()
    try:
        res = mysql.getAll(sql, None)
    except Exception as e:
        print(e, "func get_day_recharge_data", time.strftime("%Y-%m-%d %H:%M:%S"))
        print(sql)
    mysql.dispose()
    return res


# 获取每日提现数据
def get_day_withdraw_data(day):
    end_day = day + " 23:59:59"
    res = None
    sql = "select count(distinct id, if(new_user_flag = 1, true, null)) old_withdraw_result_num, " \
          "count(distinct id, if(new_user_flag = 0, true, null)) new_withdraw_result_num, " \
          "count(distinct uid, if(new_user_flag = 1, true, null)) old_user_withdraw_num, cid, " \
          "count(distinct uid, if(new_user_flag = 0, true, null)) new_user_withdraw_num, " \
          "sum(if(new_user_flag = 0, money, 0)) new_user_withdraw, " \
          "sum(if(new_user_flag = 1, money, 0)) old_user_withdraw, sum(money) withdraw_money, " \
          "sum(pay_fee) withdraw_fee from san_withdraw_list where add_time >= '%s' and " \
          "add_time <= '%s' and status = 1 group by cid" % (day, end_day)
    mysql = Mysql()
    try:
        res = mysql.getAll(sql, None)
    except Exception as e:
        print(e, "func get_day_withdraw_data", time.strftime("%Y-%m-%d %H:%M:%S"))
        print(sql)
    mysql.dispose()
    return res


if __name__ == "__main__":
    daemonize('/dev/null', '/tmp/san_user_recharge_log.txt', '/tmp/san_user_recharge_log_error.txt')
    main()
