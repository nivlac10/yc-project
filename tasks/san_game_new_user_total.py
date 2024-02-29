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
            if con is False:
                time.sleep(5)
            else:
                time.sleep(0.5)
        except Exception as e:
            print(e)
            time.sleep(0.1)


# 游戏数据日汇总 用户游戏记录日汇总
def task_start():
    arr = []
    for d in range(5000):
        res = redis.lpop('san_game_new_total_data_list')
        if res is None:
            break
        arr.append(json.loads(res))
    if len(arr) == 0:
        return True
    try:
        total = dict()
        for d in arr:
            for key in d:
                if key not in total:
                    total[key] = dict()
                    total[key]['uid'] = d[key]['uid']
                    total[key]['day'] = d[key]['day']
                    total[key]['cid'] = d[key]['cid']
                    total[key]['game_id'] = d[key]['game_id']
                    total[key]['gid'] = d[key]['gid']
                    total[key]['my_game'] = d[key]['my_game']
                    total[key]['game_type'] = d[key]['game_type']
                    total[key]['bet_num'] = d[key]['bet_num']
                    total[key]['bet'] = d[key]['bet']
                    total[key]['shu_ying'] = d[key]['shu_ying']
                    total[key]['real_shu_ying'] = d[key]['real_shu_ying']
                else:
                    total[key]['bet_num'] += d[key]['bet_num']
                    total[key]['bet'] += d[key]['bet']
                    total[key]['shu_ying'] += d[key]['shu_ying']
                    total[key]['real_shu_ying'] += d[key]['real_shu_ying']
        if total:
            data_func(total)
    except Exception as e:
        print(e)
    return False


def data_func(total):
    for x in total:
        mysql = Mysql()
        try:
            sql = "insert into san_game_wj_user_day_total (day, cid, game_id, gid, my_game, uid, game_type," \
                   " total_bet, total_shu_ying, total_real_shu_ying, total_num) values ('%s', '%s', " \
                   "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE " \
                   "total_bet = total_bet + '%s', total_shu_ying = total_shu_ying + '%s', " \
                   "total_real_shu_ying = total_real_shu_ying + '%s', total_num = total_num + '%s'" % \
                   (total[x]['day'], total[x]['cid'], total[x]['game_id'], total[x]['gid'], total[x]['my_game'],
                    total[x]['uid'], total[x]['game_type'], total[x]['bet'], total[x]['shu_ying'],
                    total[x]['real_shu_ying'], total[x]['bet_num'], total[x]['bet'], total[x]['shu_ying'],
                    total[x]['real_shu_ying'], total[x]['bet_num'])
            sql2 = "insert into san_user_team_day_report(uid, day, total_bet, total_win, total_real_win, total_num) " \
                   "values ('%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE " \
                   "total_bet = total_bet + '%s', total_win = total_win + '%s', " \
                   "total_real_win = total_real_win + '%s', total_num = total_num + '%s'" % \
                   (total[x]['uid'], total[x]['day'], total[x]['bet'], total[x]['shu_ying'], total[x]['real_shu_ying'],
                    total[x]['bet_num'], total[x]['bet'], total[x]['shu_ying'], total[x]['real_shu_ying'],
                    total[x]['bet_num'])
            mysql.insertOne(sql, None)
            mysql.insertOne(sql2, None)
        except Exception as e:
            print(e)
            mysql.dispose(2)
            maps = dict()
            maps[x] = total[x]
            redis.rpush('san_game_new_total_data_list', json.dumps(maps))
            break
        mysql.dispose()




if __name__ == "__main__":
    daemonize('/dev/null', '/tmp/san_game_total_new_user_total_log.txt', '/tmp/san_game_total_new_user_total_error.txt')
    main()
