#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-03-04
import json

from flask import request
# from telegram import Bot

from app import redis, util, constant, RKEY
from app.user import user_info
from SqlConntion.MySqlConn import Mysql
from SqlConntion.RedisDB import Redis

GIVE_BET_RATE = 20  # 赠送金额打码倍率
USER_FIRST_RECHARGE_RATE = 0.2  # 用户首充赠送倍率
USER_DAY_FIRST_RECHARGE_RATE = 0.1  # 用户每日首充赠送倍率

# 金额变动类型


MONEY_TYPE_CONF = {
    '0': {
        'code': '0',
        'name': '充值',
        'type': 0
    },
    '1': {
        'code': '1',
        'name': '提现',
        'type': 0
    },
    '2': {
        'code': '2',
        'name': '周VIP',
        'type': 0
    },
    '3': {
        'code': '3',
        'name': '月VIP',
        'type': 0
    },
    '4': {
        'code': '4',
        'name': 'VIP晋级',
        'type': 0
    },
    '5': {
        'code': '5',
        'name': '充值活动赠送',
        'type': 0
    },
    '6': {
        'code': '6',
        'name': '新用户日首充',
        'type': 0
    },
    '7': {
        'code': '7',
        'name': 'slot返水',
        'type': 0
    },
    '8': {
        'code': '8',
        'name': 'live返水',
        'type': 0
    },
    '10': {
        'code': '10',
        'name': 'table返水',
        'type': 0
    },
    '11': {
        'code': '11',
        'name': 'fish返水',
        'type': 0
    },
    '9': {
        'code': '9',
        'name': '佣金转入',
        'type': 0
    },
    '12': {
        'code': '12',
        'name': '系统赠送',
        'type': 0
    },
    '13': {
        'code': '13',
        'name': '平台转出',
        'type': 0
    },
    '14': {
        'code': '14',
        'name': '平台转入',
        'type': 0
    },
    '17': {
        'code': '17',
        'name': '提现返还',
        'type': 0
    },
    '18': {
        'code': '18',
        'name': '充值活动',
        'type': 0
    },
    '19': {
        'code': '19',
        'name': 'fast返水',
        'type': 0
    },
    '20': {
        'code': '20',
        'name': '日签到',
        'type': 0
    },
    '21': {
        'code': '21',
        'name': '用户日打码任务',
        'type': 0
    },
    '22': {
        'code': '22',
        'name': '用户破产补助',
        'type': 0
    },
    '23': {
        'code': '23',
        'name': '用户领取code码',
        'type': 0
    },
    '24': {
        'code': '24',
        'name': 'vip立反奖励',
        'type': 0
    },
    '25': {
        'code': '25',
        'name': 'vip日反水',
        'type': 0
    },
    '26': {
        'code': '26',
        'name': 'vip每周反水',
        'type': 0
    },
    '27': {
        'code': '27',
        'name': 'vip每月反水',
        'type': 0
    },
    '28': {
        'code': '28',
        'name': 'vip拆分反水',
        'type': 0
    }, '29': {
        'code': '29',
        'name': '每日免费转轮赠送',
        'type': 0
    }, '30': {
        'code': '30',
        'name': '下载APK',
        'type': 0
    }, '31': {
        'code': '31',
        'name': '仲夏节每日大放送(德州)',
        'type': 0
    }, '32': {
        'code': '32',
        'name': '总胜多少局和连胜奖励(德州)',
        'type': 0
    }, '33': {
        'code': '33',
        'name': '皇家礼包(德州)',
        'type': 0
    }, '34': {
        'code': '34',
        'name': '皇家同花顺奖励',
        'type': 0
    }, '35': {
        'code': '35',
        'name': '抽到888和8888，666和6666，777和7777(德州)',
        'type': 0
    }, '36': {
        'code': '36',
        'name': '竞标赛获胜(德州)',
        'type': 0
    },
    '37': {
        'code': '37',
        'name': '竞标赛入场费(德州)',
        'type': 0
    },
    '38': {
        'code': '38',
        'name': '俱乐部门票(德州)',
        'type': 0
    },
    '39': {
        'code': '39',
        'name': '邮箱发放(德州)',
        'type': 0
    },'40': {
        'code': '40',
        'name': '救济金(德州)',
        'type': 0
    },
    '41': {
        'code': '41',
        'name': '俱乐部转账(德州)',
        'type': 0
    },
    '42': {
        'code': '42',
        'name': '发送大喇叭(德州)',
        'type': 0
    },
    '43': {
        'code': '43',
        'name': '充值成就奖励',
        'type': 0
    },
    # 佣金变动
    '100': {
        'code': '100',
        'name': '佣金提现',
        'type': 1
    },
    '101': {
        'code': '101',
        'name': '佣金提现返还',
        'type': 1
    },
    '102': {
        'code': '102',
        'name': '佣金转出',
        'type': 1
    },
    '103': {
        'code': '103',
        'name': '一级打码返佣',
        'type': 1
    },
    '104': {
        'code': '104',
        'name': '二级打码返佣',
        'type': 1
    },
    '105': {
        'code': '105',
        'name': '三级打码返佣',
        'type': 1
    },
    '106': {
        'code': '106',
        'name': '直属首充佣金',
        'type': 1
    },
    '107': {
        'code': '107',
        'name': '邀请任务佣金',
        'type': 1
    },
}
# 充值活动配置
RECHARGE_ACTIVITY_CONF = [
    {
        "type": 0,
        'type_name': '单次充值赠送(范围阶梯)',
    }, {
        "type": 1,
        'type_name': '单次充值赠送(指定额度阶梯)',
    },
    {
        "type": 2,
        'type_name': '首次充值赠送(范围阶梯)',
    }, {
        "type": 3,
        'type_name': '首次充值赠送(指定额度阶梯)',
    },

]
# 佣金变动名称
COMMISSION_TYPE_CONF = [
    # 佣金提现
    {
        "name": "Commission Withdrawal",
        "type": 5,
        "mode": "-",
    },
    # 佣金转出
    {
        "name": "Commission Transfer",
        "type": 4,
        "mode": "-",
    },
    # 代理打码返佣
     {
        "name": "Betting Commission",
        "type": 1,
        "mode": "+",
    },
    # 直属首充佣金
    {
        "name": "Invitation Conquest",
        "type": 3,
        "mode": "+",
    },
    # 邀请任务佣金
    {
        "name": "Invitation Bonus",
        "type": 2,
        "mode": "+",
    },
    # 佣金提现返还
    # {
    #     "name": "Withdraw Fail",
    #     "type": 6,
    #     "mode": "+",
    # },
]

# bonus配置
BONUS_TYPE_CONF = [
    {
        'type': '0',
        'type_name': 'Recharge'  # 充值
    },
    {
        'type': '1',
        'type_name': 'Vip Upgrade'  # Vip升级
    },
    {
        'type': '2',
        'type_name': 'Vip Week'  # 每周领取
    },
    {
        'type': '3',
        'type_name': 'Vip Month'  # 每月领取
    },
    {
        'type': '4',
        'type_name': 'Slot'  # slot反水
    },
    {
        'type': '5',
        'type_name': 'Live'  # live反水
    }
]

# vip_lv 配置
VIP_CONF = [
    {'vip_lv': 0, 'recharge': 0, 'bet': 0, 'withdraw_num': 20, 'max_withdraw': 50000, 'pay_fee': 2,
     'day_max_withdraw': 1000000, 'lv_reward': 0, 'slot': 0.4, 'table': 0.4, 'live': 0.4, 'week_bonus': 2,
     'month_bonus': 5, },
    {'vip_lv': 1, 'recharge': 1000, 'bet': 6000, 'withdraw_num': 20, 'max_withdraw': 50000, 'pay_fee': 2,
     'day_max_withdraw': 1000000, 'lv_reward': 20, 'slot': 0.45, 'table': 0.45, 'live': 0.4, 'week_bonus': 20,
     'month_bonus': 30},
    {'vip_lv': 2, 'recharge': 10000, 'bet': 60000, 'withdraw_num': 20, 'max_withdraw': 50000, 'pay_fee': 2,
     'day_max_withdraw': 1000000, 'lv_reward': 60, 'slot': 0.5, 'table': 0.5, 'live': 0.4, 'week_bonus': 40,
     'month_bonus': 80},
    {'vip_lv': 3, 'recharge': 50000, 'bet': 300000, 'withdraw_num': 20, 'max_withdraw': 50000, 'pay_fee': 2,
     'day_max_withdraw': 1000000, 'lv_reward': 200, 'slot': 0.55, 'table': 0.55, 'live': 0.4, 'week_bonus': 80,
     'month_bonus': 160},
    {'vip_lv': 4, 'recharge': 100000, 'bet': 600000, 'withdraw_num': 20, 'max_withdraw': 50000, 'pay_fee': 2,
     'day_max_withdraw': 1000000, 'lv_reward': 600, 'slot': 0.6, 'table': 0.6, 'live': 0.4, 'week_bonus': 160,
     'month_bonus': 320},
    {'vip_lv': 5, 'recharge': 500000, 'bet': 3000000, 'withdraw_num': 30, 'max_withdraw': 50000, 'pay_fee': 1,
     'day_max_withdraw': 1500000, 'lv_reward': 1500, 'slot': 0.65, 'table': 0.65, 'live': 0.4, 'week_bonus': 320,
     'month_bonus': 640},
    {'vip_lv': 6, 'recharge': 1000000, 'bet': 6000000, 'withdraw_num': 30, 'max_withdraw': 50000, 'pay_fee': 1,
     'day_max_withdraw': 1500000, 'lv_reward': 5000, 'slot': 0.7, 'table': 0.7, 'live': 0.4, 'week_bonus': 640,
     'month_bonus': 1280},
    {'vip_lv': 7, 'recharge': 5000000, 'bet': 30000000, 'withdraw_num': 30, 'max_withdraw': 50000, 'pay_fee': 1,
     'day_max_withdraw': 1500000, 'lv_reward': 15000, 'slot': 0.8, 'table': 0.8, 'live': 0.4, 'week_bonus': 1280,
     'month_bonus': 2560},
    {'vip_lv': 8, 'recharge': 10000000, 'bet': 60000000, 'withdraw_num': 40, 'max_withdraw': 50000, 'pay_fee': 1,
     'day_max_withdraw': 2000000, 'lv_reward': 50000, 'slot': 0.9, 'table': 0.9, 'live': 0.4, 'week_bonus': 2560,
     'month_bonus': 5120},
    {'vip_lv': 9, 'recharge': 50000000, 'bet': 300000000, 'withdraw_num': 40, 'max_withdraw': 50000, 'pay_fee': 1,
     'day_max_withdraw': 2000000, 'lv_reward': 150000, 'slot': 1, 'table': 1, 'live': 0.4, 'week_bonus': 5120,
     'month_bonus': 10240},
]

# 游戏厂商配置
GAME_MAKER = [
    {
        'game_maker_name': 'In-house',
        'my_game': 0
    },
    {
        'game_maker_name': 'SBO',
        'my_game': 2
    },
    {
        'game_maker_name': 'AWC',
        'my_game': 3
    },
]

GS_GAME_TYPE = {
    '1': 'Slot',
    '2': 'Live Casino',
    '3': 'Sport Book',
    '4': 'Virtual Sport',
    '5': 'Lottery',
    '6': 'Qipai',
    '7': 'P2P',
    '8': 'Fishing',
    '9': 'Others'
}
HOME_GAME_TYPE = [
    {'game_type_name': 'Slot', 'game_type_id': 0, 'game_play_type': 0, 'rakeback_open': 1},
    {'game_type_name': 'Table', 'game_type_id': 1, 'game_play_type': 1, 'rakeback_open': 1},
    {'game_type_name': 'Live', 'game_type_id': 2, 'game_play_type': 1, 'rakeback_open': 1},
    {'game_type_name': 'Fish', 'game_type_id': 3, 'game_play_type': 0, 'rakeback_open': 1},
]

HOME_GAME_TYPE_API = []
for d in HOME_GAME_TYPE:
    data = dict()
    data['game_type_name'] = d['game_type_name']
    data['game_type_id'] = d['game_type_id']
    data['game_play_type'] = d['game_play_type']
    HOME_GAME_TYPE_API.append(data)

BIND_BONUS = 1  # 绑定朋友赠送的bonus

INVITE_TASK_CONF = {
    '1': {
        'num': 5,
        'money': 25
    },
    '2': {
        'num': 15,
        'money': 150
    },
    '3': {
        'num': 30,
        'money': 450
    },
    '4': {
        'num': 80,
        'money': 1600
    }, '5': {
        'num': 200,
        'money': 6000
    },
}


# 游戏记录详情
GAME_LOG_CONF = {
    '871': 'bcbm.html',
    '872': 'brzjh.html',
    '873': 'brab.html',
    '874': 'brpair.html',
    '875': 'fruit.html',
    '876': 'fish.html',
    '877': 'bjl.html',
    '878': 'roulette.html',
    '879': 'crash.html',
    '880': 'wingo.html',
    '881': 'hilo.html',
    '882': 'dice.html',
    '884': 'mines.html',
    '885': 'fruitbomb.html',
    '886': 'roller.html',
    '887': 'wheeloftime.html',
    '888': 'magicwheel.html',
    '889': 'jokersjewels.html',
    '890': 'fruit_slot.html',
    '891': 'juicy.html',
    '892': 'burningaces.html',
    '893': 'jollytreasures.html',
    '894': 'bonanzagold.html',
    '895': 'starlightprincess.html',
    '896': 'greatrhinomegaways.html'
}


# 游戏详情表
GAME_DETAIL_TABLE = {
    '871': 'san_bcbm_detail_log',
    '872': 'san_brzjh_detail_log',
    '873': 'san_brab_detail_log',
    '874': 'san_brpair_detail_log',
    '875': 'san_fruit_detail_log',
    '876': 'san_fish_detail_log',
    '877': 'san_bjl_detail_log',
    '878': 'san_roulette_detail_log',
    '879': 'san_crash_detail_log',
    '880': 'san_wingo_detail_log',
    '881': 'san_hilo_detail_log',
    '882': 'san_dice_detail_log',
    '883': 'san_luckynumber_detail_log',
    '884': 'san_mines_detail_log',
    '885': 'san_fruitbomb_detail_log',
    '886': 'san_roller_detail_log',
    '887': 'san_slot_wheeloftime_detail_log',
    '888': 'san_slot_magicwheel_detail_log',
    '889': 'san_slot_jokersjewels_detail_log',
    '890': 'san_slot_fruitslot_detail_log',
    '891': 'san_slot_juicy_detail_log',
    '892': 'san_slot_burningaces_detail_log',
    '893': 'san_slot_jollytreasures_detail_log',
    '894': 'san_slot_bonanzagold_detail_log',
    '895': 'san_slot_starlightprincess_detail_log',
    '896': 'san_slot_greatrhinomegaways_detail_log'
}


card_list_conf = [
    # 注册数据
    {
        'title': "注册数据",
        'hint': "注册人数",
        'data': [
            {
                'min_title': '安装数',
                'number': 0,
                'unit': "人",
                'key': 'install_num'
            },
            {
                'min_title': '注册数',
                'number': 0,
                'unit': "人",
                'key': 'register_num'
            }, {
                'min_title': '注册率',
                'number': 0,
                'unit': "%",
                'key': 'register_ratio'
            },
        ],
    },
    # 玩家日活数据
    {
        'title': "玩家日活",
        'hint': "玩家日活",
        'data': [
            {
                'min_title': '总玩家',
                'number': 0,
                'unit': "人",
                'key': 'game_num'
            },
            {
                'min_title': '老玩家',
                'number': 0,
                'unit': "人",
                'key': 'new_game_num'
            },
            {
                'min_title': '新玩家',
                'number': 0,
                'unit': "人",
                'key': 'old_game_num'
            },
            {
                'min_title': '在线人数',
                'number': 0,
                'unit': "人",
                'key': 'ol_num'
            },
        ],
    },
    # 游戏数据
    {
        'title': "游戏数据",
        'hint': "游戏数据",
        'data': [
            {
                'min_title': '总押',
                'number': 0,
                'unit': "分",
                'key': 'total_bet'
            },
            # {
            #     'min_title': '总赢',
            #     'number': 0,
            #     'unit': "分",
            #     'key': 'total_shu_ying'
            # },
            {
                'min_title': '概率',
                'number': 0,
                'unit': "%",
                'key': 'bet_pro'
            },
            {
                'min_title': '输赢',
                'number': 0,
                'unit': "分",
                'key': 'system_shu_ying'
            },
        ],
    },

]
table_list_conf = [
    # 充值数据
    {
        'max_title': "充值数据",
        'title': ['名称', '付费金额', '付费人数', '付费率', '付费ARPPU', '活跃ARPU'],
        'hint': "玩家日活",
        'data': [
            {
                'min_title': '新用户',
                'number': [
                    {
                        'value': 0,
                        'key': 'new_user_recharge'
                    }, {
                        'value': 0,
                        'key': 'new_user_num'
                    }, {
                        'value': 0,
                        'key': 'new_user_ratio'
                    }, {
                        'value': 0,
                        'key': 'new_pj_money'
                    }, {
                        'value': 0,
                        'key': 'new_up'
                    },
                ],
            },
            {
                'min_title': '老用户',
                'number': [{
                    'value': 0,
                    'key': 'old_user_recharge'
                }, {
                    'value': 0,
                    'key': 'old_user_num'
                }, {
                    'value': 0,
                    'key': 'old_user_ratio'
                }, {
                    'value': 0,
                    'key': 'old_pj_money'
                }, {
                    'value': 0,
                    'key': 'old_up'
                },
                ],
            },
            {
                'min_title': '总用户',
                'number': [
                    {
                        'value': 0,
                        'key': 'recharge_money'
                    }, {
                        'value': 0,
                        'key': 'r_num'
                    }, {
                        'value': 0,
                        'key': 'recharge_ratio'
                    }, {
                        'value': 0,
                        'key': 'pj_money'
                    }, {
                        'value': 0,
                        'key': 'total_up'
                    },
                ],
            },
        ],
    },
    # 充值提现数据
    {
        'max_title': "提现数据",
        # 'title': ['名称', '提现人数', '提现金额', '充提差', '提现率'],
        'title': ['名称', '提现总额', '充提差', '提现率', '提现人数'],
        'hint': "玩家日活",
        'data': [
            {
                'min_title': '新用户',
                'number': [
                    {
                        'value': 0,
                        'key': 'new_user_withdraw'
                    }, {
                        'value': 0,
                        'key': 'new_r_w'
                    }, {
                        'value': 0,
                        'key': 'new_w_ratio'
                    }, {
                        'value': 0,
                        'key': 'new_user_withdraw_num'
                    },
                ],
            },
            {
                'min_title': '老用户',
                'number': [
                    {
                        'value': 0,
                        'key': 'old_user_withdraw'
                    }, {
                        'value': 0,
                        'key': 'old_r_w'
                    }, {
                        'value': 0,
                        'key': 'old_w_ratio'
                    }, {
                        'value': 0,
                        'key': 'old_user_withdraw_num'
                    },
                ],
            },
            {
                'min_title': '总用户',
                'number': [
                    {
                        'value': 0,
                        'key': 'withdraw_money'
                    }, {
                        'value': 0,
                        'key': 'rw'
                    }, {
                        'value': 0,
                        'key': 'total_w_ratio'
                    }, {
                        'value': 0,
                        'key': 'total_user_withdraw_num'
                    },
                ],
            },
        ],
    },
    # 赠送数据
    {
        'max_title': "赠送数据",
        'title': ['名称', '总额', 'VIP晋级', 'VIP周卡', 'VIP月卡', 'VIP返水', '系统赠送'],
        'hint': "玩家日活",
        'data': [
            {
                'min_title': '数据',
                'number': [
                    {
                        'value': 0,
                        'key': 'total_give'
                    }, {
                        'value': 0,
                        'key': 'vip_up'
                    }, {
                        'value': 0,
                        'key': 'vip_week'
                    }, {
                        'value': 0,
                        'key': 'vip_month'
                    },
                    {
                        'value': 0,
                        'key': 'user_rebate'
                    },
                    {
                        'value': 0,
                        'key': 'system_give'
                    },
                ],
            },
        ],
    },
    # 佣金数据
    {
        'max_title': "佣金数据",
        'title': ['名称', '总额', '首充佣金', '任务佣金', '下注佣金'],
        'hint': "玩家日活",
        'data': [
            {
                'min_title': '数据',
                'number': [
                    {
                        'value': 0,
                        'key': 'total_brokerage'
                    }, {
                        'value': 0,
                        'key': 'first_recharge_brokerage'
                    }, {
                        'value': 0,
                        'key': 'invite_task_brokerage'
                    }, {
                        'value': 0,
                        'key': 'total_bet_brokerage'
                    },
                ],
            },
        ],
    },
]



# 获取用户当前vip等级
def get_recharge_money_vip(recharge_money, total_bet):
    num = 0
    vip_conf = json.loads(redis.get(RKEY.SAN_GAME_VIP_LV_LIST)) if redis.get(RKEY.SAN_GAME_VIP_LV_LIST) else VIP_CONF
    try:
        for d in range(0, len(vip_conf)):
            if float(recharge_money) >= float(vip_conf[d]['recharge']) and float(total_bet) >= float(
                    vip_conf[d]['bet']):
                num = vip_conf[d]['vip_lv']
                if d == 9:
                    num = 9
                continue
            break
    except Exception as e:
        print(e)
    return num


# 验证用户vip
def verify_user_vip_lv(user):
    recharge_money = user['total_money']
    total_bet = user['total_bet']
    vip_lv = user['vip_lv']
    now_vip_lv = get_recharge_money_vip(recharge_money, total_bet)
    if float(now_vip_lv) > float(vip_lv):
        update_user_vip_lv(user['uid'], now_vip_lv)
        user['vip_lv'] = now_vip_lv


# 更新用户vip
def update_user_vip_lv(uid, vip_lv):
    sql = "update san_users set vip_lv = '%s' where uid = '%s'" % (vip_lv, uid)
    mysql = Mysql()
    try:
        mysql.update(sql, None)
    except Exception as e:
        print(e)
    mysql.dispose()


# 更新用户余额信息
def update_user_data_info(uid, **kwargs):
    """
    只更新用户数字类型的字段，不能字符串类型数据
    """
    if kwargs:
        sql = "update san_users set "
        for d in kwargs:
            sql += d + "=" + d + "+" + str(kwargs[d]) + ","
        sql = sql[:-1]
        sql += " where uid = '" + str(uid)+"'"
        mysql = Mysql()
        try:
            res = mysql.update(sql, None)
        except Exception as e:
            print(e)
        mysql.dispose()
        return res


# 用户每日数据汇总
def user_day_data_total(uid, day, **kwargs):
    if kwargs:
        sql = "insert into san_user_team_day_report(uid, day, "
        arr = []
        for d in kwargs:
            sql += d + ','
            arr.append(d)
        if len(arr) == 0:
            return
        sql = sql[:-1] + ')' + ' values(' + str(uid) + ',"' + str(day) + '",'
        for k in range(len(arr)):
            sql += str(kwargs[arr[k]]) + ','
        sql = sql[:-1] + ')' + 'ON DUPLICATE KEY UPDATE '
        for j in range(len(arr)):
            sql += arr[j] + '=' + arr[j] + '+' + str(kwargs[arr[j]]) + ','
        sql = sql[:-1]
        mysql = Mysql()
        try:
            mysql.insertOne(sql, None)
        except Exception as e:
            print(e)
        mysql.dispose()


# 用户每日数据汇总
def day_money_total(cid, day, **kwargs):
    if kwargs:
        sql = "insert into san_day_money_total(cid, day,  "
        arr = []
        for d in kwargs:
            sql += d + ','
            arr.append(d)
        if len(arr) == 0:
            return
        sql = sql[:-1] + ')' + ' values(' + str(cid) + ',"' + str(day) + '",'
        for k in range(len(arr)):
            sql += str(kwargs[arr[k]]) + ','
        sql = sql[:-1] + ')' + 'ON DUPLICATE KEY UPDATE '
        for j in range(len(arr)):
            sql += arr[j] + '=' + arr[j] + '+' + str(kwargs[arr[j]]) + ','
        sql = sql[:-1]
        mysql = Mysql()
        try:
            mysql.insertOne(sql, None)
        except Exception as e:
            print(e)
        mysql.dispose()


# 用户余额变动记录
def user_money_log_func(uid, money, before_money, after_money, money_type):
    sql = "insert into san_user_money_log(uid, money, before_money, after_money, money_type, add_time) values ('%s', " \
          "'%s', '%s', '%s', '%s', now())" % (uid, money, before_money, after_money, money_type)
    mysql = Mysql()
    res = mysql.insertOne(sql, None)
    mysql.dispose()
    return res


# 邀请成功消息发送
def invite_user_ok(uid, invite_uid):
    title = 'System message'
    redis_R = Redis()
    share_template = redis_R.hget(RKEY.SAN_GAME_ALL_CONF, 'success_email') or ''  # 邀请成功邮件通知配置
    redis_R.close()
    content = share_template.replace('<uid>', str(invite_uid))
    sql = "insert into san_user_message(uid, title, content, add_time) values (%s, %s, %s, now())"
    mysql = Mysql()
    res = mysql.insertOne(sql, [uid, title, content])
    mysql.dispose()
    return res


# 添加用户提现异常
def add_user_withdraw_log(uid, info):
    ip = request.headers.get('X-Real-Ip', request.remote_addr)
    mysql = Mysql()
    try:
        sql = "insert into san_user_unusual_log(uid, ip, info, add_time) values ('%s', '%s', '%s', now())" % \
              (uid, ip, info)
        mysql.insertOne(sql, None)
    except Exception as e:
        print(e)
    mysql.dispose()


# 更新老客登陆大厅数据
def update_old_user_life(user, now_day):
    try:
        old_user_life_key = 'old_user_life_day_flag_' + now_day
        if redis.hget(old_user_life_key, str(user['uid'])):
            return
        # sql = "insert into san_day_money_total(day, cid, old_user_life) values ('%s', '%s', 1) ON " \
        #       "DUPLICATE KEY UPDATE old_user_life = old_user_life + 1" % (now_day, user['cid'])
        # mysql = Mysql()
        # mysql.insertOne(sql, None)
        # mysql.dispose()
        old_user_life_login_key = 'old_user_life_login_key_' + now_day
        redis.hincrby(old_user_life_login_key, str(user['cid']), 1)
        redis.expire(old_user_life_login_key, 86400 * 3)
        redis.hset(old_user_life_key, str(user['uid']), '1')
        redis.expire(old_user_life_key, 86400 * 7)
    except Exception as e:
        print(e)


# 用户大额充值提醒
# def user_recharge_tips(uid, money, flag):
#     if flag == 0:
#         txt = '🤑🤑🤑\n充值提醒\n\n用户:' + str(uid) + '\n\n充值' + str(money)
#     else:
#         txt = '🤑🤑🤑\n充值提醒\n\n大R用户:' + str(uid) + '\n\n充值' + str(money)
#     send_telegram(txt)
#
#
# # 大哥上线提醒
# def game_big_boy(user):
#     if redis.get('san_game_big_boy_' + str(user['uid'])) is None:
#         try:
#             txt = '🚀🚀🚀\n大R上线通知\nuid：%s\n总充值：%s\n总提现：%s\n余额：%s\n' % \
#                   (str(user['uid']), str(user['total_money']), str(user['total_withdraw']), str(user['money']))
#             send_telegram(txt)
#             redis.set('san_game_big_boy_' + str(user['uid']), '1', ex=1200)
#         except Exception as e:
#             print(e)


# # 提现审核
# def withdraw_notice(uid, money):
#     try:
#         txt = '🔔🔔🔔\n提现审核提醒\n\n用户:' + str(uid) + '\n\n金额' + str(money)
#         send_telegram(txt)
#     except Exception as e:
#         print(e)
#
#
# # 佣金提现审核
# def auto_withdraw_notice(uid, money):
#     try:
#         txt = '🔔🔔🔔\n自动审核提醒\n\n用户:' + str(uid) + '\n\n金额' + str(money)
#         print(txt)
#         send_telegram(txt)
#     except Exception as e:
#         print(e)


# 发送通知
# def send_telegram(content):
#     bot = Bot(token=constant.BOT_TOKEN)
#     # 不加ensure_ascii=False 结果会是ASCII编码，我们需要用中文正常显示
#     # textMsg = json.dumps(datas, ensure_ascii=False)
#
#     # 修改群ID和机器人
#     data = bot.send_message(chat_id=constant.CHAT_ID, text=content, parse_mode='html')
#     print(data)


# 直属上级获取下级首充佣金奖励
def recharge_give_parent_money(parent_id, uid, money):
    user = user_info.get_user_by_uid(parent_id)
    redis_R = Redis()
    USER_PARENT_COMMISSION = redis_R.hget(RKEY.SAN_GAME_ALL_CONF, 'invit_recharge_gift') or 10
    redis_R.close()
    give_money = round(float(money) * (float(USER_PARENT_COMMISSION) / 100), 2)
    if user is None:
        print("parent is None")
        return
    day = util.get_today().strftime('%Y-%m-%d')
    # 添加团队日汇总
    sql = "insert into san_user_team_day_report (day, uid, team_recharge_brokerage)" \
          " values ('%s','%s','%s') " % (day, user['uid'], give_money)
    sql += " ON DUPLICATE KEY UPDATE team_recharge_brokerage = team_recharge_brokerage + '%s'" % give_money
    # 更新用户佣金信息 （佣金余额， 总佣金， 邀请充值佣金）
    sql2 = "update san_users set commission = commission + '%s', total_commission = total_commission + '%s' " \
           " , share_recharge_brokerage = share_recharge_brokerage + '%s' where uid = '%s'" \
           % (give_money, give_money, give_money, user['uid'])
    sql3 = "insert into san_user_day_brokerage (uid, day, lv_num, game_uid, game_bet, money, status, add_time," \
           " update_time, money_type) values (%s, NOW(), %s, %s, %s,%s,%s, NOW(), NOW(),%s)"
    mysql = Mysql()
    res = mysql.insertOne(sql, None)  # 添加团队日汇总
    res2 = mysql.update(sql2, None)  # 更新用户佣金信息 （佣金余额， 总佣金， 邀请充值佣金）
    res3 = mysql.insertOne(sql3, [parent_id, 1, uid, 0, give_money, 1, 3])
    mysql.dispose()
    after_commission = round(float(user['commission']) + float(give_money), 2)
    user_commission_log_func(user['uid'], give_money, user['commission'], after_commission, 106)  # 变动日志


# 用户佣金变动记录
def user_commission_log_func(uid, commission, before_commission, after_commission, commission_type):
    sql = "insert into san_user_money_log(uid, money, before_money, after_money, money_type, log_type, add_time) " \
          "values ('%s', " \
          "'%s', '%s', '%s', '%s', 1, Now())" % (uid, commission, before_commission, after_commission, commission_type)
    mysql = Mysql()
    res = mysql.insertOne(sql, None)
    mysql.dispose()
    return res


# 佣金记录
def user_brokerage_log_func(uid, game_id, lv_num, money, money_type):
    sql = "insert into san_user_day_brokerage (uid, day, lv_num, game_uid, game_bet, money, status, add_time," \
           " update_time, money_type) values (%s, NOW(), %s, %s, %s,%s,%s, NOW(), NOW(),%s)"
    mysql = Mysql()
    res = mysql.insertOne(sql, [uid, lv_num, game_id, 0, money, 1, money_type])
    mysql.dispose()
    return res