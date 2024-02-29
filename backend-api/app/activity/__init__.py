#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/06/20 17:33
# @Author : 78957
from flask import Blueprint

activity = Blueprint('activity', __name__)


from . import give_code         # 礼包码
from . import commission_conf   # 返佣配置
from . import commission_desc   # 佣金活动
from . import commission_log    # 佣金日志
from . import banner        # 轮播图
from . import activitys      # 活动配置
from . import vip_lv        # 会员等级
from . import bet_task      # 打码任务
from . import recharge_activity     # 充值活动
from . import user_sign             # 用户签到\
from . import vip_bonus_log         # 会员奖励记录
from . import recharge_bonus_log    # 充值奖励领取记录
from . import roller_money_log      # 转轮赠送金额日志列表
from . import dezhou_bonus_log      # 德州下注奖励日志
from . import recharge_achieve_log  # 充值成就领取日志
from . import invite_task_log       # 佣金邀请任务日志
from . import keep_log              # 每日活跃记录