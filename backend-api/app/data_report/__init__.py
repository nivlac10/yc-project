#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/06/20 17:33
# @Author : 78957
from flask import Blueprint

data_report = Blueprint('data_report', __name__)

from . import hour_report             # 时段分析【充值|活跃注册|破产补贴|用户签到|打码量奖励】
from . import day_data              # 日数据
from . import pay_detail            # 支付通道分析数据
from . import home   # 首页