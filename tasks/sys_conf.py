#!/usr/bin/env python
# coding: utf-8
import os

from MysqlConn import Mysql
import sys, redis, json, telegram, time, psutil, importlib

import Config

importlib.reload(sys)
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
            time.sleep(5*60)
        except Exception as e:
            print(e)


at_pay_check = ''


def task_start():
    num = 0
    for d in range(0, 5):
        num += float(psutil.cpu_percent())
        time.sleep(1)
    cpu_rate = num / 5
    memory_rate = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    if cpu_rate >= 50 or memory_rate >= 50 or disk_usage >= 80:
    # if True:
        cpu_rate = str(cpu_rate) + '%'
        memory_rate = str(memory_rate) + '%'
        disk_usage = str(disk_usage) + '%'
        lj_num, sy_num, dl_num = get_mysql_data()
        content = u"%s🔍🔍🔍\n服务器运行监测异常\nCPU使用率：%s\n内存占用率：%s\n磁盘占用率：%s\nMySQL\n连接数：%s\n正在使用：%s\n插入语句等待队列：%s" % \
                  (at_pay_check, str(cpu_rate), str(memory_rate), str(disk_usage), str(lj_num), str(sy_num), str(dl_num))
        send_telegram(content)


def get_mysql():
    s_time = time.time()
    mysql = Mysql()
    try:
        mysql.getOne('select count(*) from san_administrator', None)
    except Exception as e:
        print(e)
    mysql.dispose()
    return time.time() - s_time


def get_mysql_data():
    lj_num, sy_num, dl_num = '0', '0', '0'
    mysql = Mysql()
    sql = "SHOW GLOBAL STATUS LIKE '%threads%';"
    res = mysql.getAll(sql, None)
    mysql.dispose()
    if res:
        for d in res:
            if d['Variable_name'] == 'Threads_connected':
                lj_num = d['Value']
            if d['Variable_name'] == 'Threads_running':
                sy_num = d['Value']
            if d['Variable_name'] == 'Delayed_insert_threads':
                dl_num = d['Value']
    return lj_num, sy_num, dl_num


# 发送通知
def send_telegram(content):
    bot_token = Config.BOT_TOKEN
    chat_id = Config.CHAT_ID
    bot = telegram.Bot(token=bot_token)
    # 修改群ID和机器人
    data = bot.send_message(chat_id=chat_id, text=content, parse_mode='html')


if __name__ == "__main__":
    daemonize('/dev/null', '/tmp/san_sys_conf_log.txt', '/tmp/san_sys_conf_error.txt')
    main()
