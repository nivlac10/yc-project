# -*- coding: UTF-8 -*-
import os


def startall():
    open = input('是否关闭全部任务？(1 yes/0 no)')
    if open == 1:
        os.system('killall -9 python3')
        os.system('ps -ef')
        print('已关闭')
    open = input('是否启动全部任务？(1 yes/0 no)')
    if open == 1:
        os.system('python3  /home/task/san_bet_data_lpop.py')
        os.system('python3  /home/task/san_user_money_log.py')
        os.system('python3	/home/task/san_user_bet_brokerage_log.py')
        os.system('python3	/home/task/san_user_bet_brokerage_result.py')
        os.system('python3  /home/task/san_game_give_total.py')
        os.system('python3  /home/task/san_game_user_team.py')
        os.system('python3  /home/task/san_login.py')
        os.system('python3  /home/task/san_user_active.py')
        os.system('python3  /home/task/san_first_recharge.py')
        os.system('python3  /home/task/san_user_recharge_log.py')
        os.system('python3  /home/task/san_user_day_hour_report.py')
        os.system('python3  /home/task/san_fb_using_event.py')
        os.system('python3  /home/task/san_update_game_time.py')
        os.system('ps -ef')
        print('已启动')


if __name__ == '__main__':
    startall()
