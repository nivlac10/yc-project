#!/usr/bin/env python
# coding: utf-8
import importlib
import json
import os
import time

import redis
import sys
from MysqlConn import Mysql
import Config

importlib.reload(sys)
pool = redis.ConnectionPool(host=Config.R_host, port='6379', db=0, password='', decode_responses=True)
redis = redis.Redis(connection_pool=pool)
USER_DAY_HOUR_KEY = 'user_hour_data'  # 用户注单队列key

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
                time.sleep(60)
        except Exception as e:
            print(e)


# 时段分析
def task_start():
    arr = []
    for d in range(5000):
        res = redis.lpop(USER_DAY_HOUR_KEY)
        if res is None:
            break
        arr.append(json.loads(res))
    if len(arr) == 0:
        return False
    data_func(arr)


def data_func(arr):
    maps = dict()
    for d in arr:
        hour_key = "hour_key_" + str(d['day']) + "_" + str(d['hour']) + "_" + str(d['cid']) + '_' + d['key_str']
        if hour_key not in maps:
            c_key = dict()
            c_key['cid'] = d['cid']
            c_key['num'] = d['num']
            c_key['day'] = d['day']
            c_key['key_str'] = d['key_str']
            maps[hour_key] = c_key
        else:
            maps[hour_key]['num'] += d['num']
    if maps:
        hour_day_data_func(maps)


# 数据处理
def hour_day_data_func(total):
    for x in total:
        sql = "insert into san_user_day_hour_report (day, cid, %s) values ('%s', '%s', %s) ON DUPLICATE KEY UPDATE" \
              " %s = %s + %s" % (total[x]['key_str'], total[x]['day'], total[x]['cid'], total[x]['num']
                                 , total[x]['key_str'], total[x]['key_str'], total[x]['num'])
        mysql = Mysql()
        res = mysql.insertOne(sql, None)
        mysql.dispose()
        # print(sql)


# 用户日活数据
def user_add_hour_func(cid, flag, uid, num=1):
    flag_list = ['t', 'v', 'b', 'r', 'm']
    day = str(time.strftime("%Y-%m-%d"))
    hour = int(str(time.strftime("%H")))
    data = dict()
    data['cid'] = cid
    data['uid'] = uid
    data['day'] = day
    data['hour'] = hour
    data['key_str'] = flag_list[flag] + str(hour)
    data['num'] = num
    redis_key = "user_hour_data"
    redis.rpush(redis_key, json.dumps(data))


if __name__ == "__main__":
    daemonize('/dev/null', '/tmp/san_user_day_hour_report.txt', '/tmp/san_user_day_hour_report.txt')
    main()
    # for i in range(500):
    #     user_add_hour_func(1, 0, 6, 1)
    #     user_add_hour_func(1, 1, 5, 1)
    #     user_add_hour_func(2, 2, 4, 1)
    #     user_add_hour_func(2, 3, 6, 1)
    #     user_add_hour_func(2, 4, 7, 10)
    # task_start()
