#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/06/20 17:33
# @Author : 78957
from flask import Blueprint

user = Blueprint('user', __name__)

from . import user_info                  # 用户
from . import user_brokerage_log    # 用户打码返佣记录
from . import user_day_report       # 用户日报表
from . import user_game_log         # 用户游戏记录
from . import user_logs             # 用户登录记录
from . import user_loss_bonus       # 用户破产补贴
from . import user_money_logs       # 用户金额变动记录
from . import user_recharge_data    # 付费
from . import user_operate          # 用户操作
from . import email                 # 用户消息
from . import user_sbo_bet_log_heshi # 核实用户SBO注单记录