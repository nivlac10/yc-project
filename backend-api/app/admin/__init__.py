#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/06/20 17:33
# @Author : 78957
from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import login         # 登录
from . import index         # 首页菜单权限
from . import power         # 路由菜单
from . import admins        # 管理员信息
from . import conf

from . import agent         # 渠道信息
from . import black         # 黑名单
from . import event_report  # 事件上报
# 列表as

from . import notice        # 公告
from . import pay_conf      # 支付配置
from . import pay_data      # 支付数据
from . import proxy         # 代理
from . import recharge      # 充值
from . import send_phone    # 用户短信
from . import withdraw      # 提现
from . import active        # 留存数据
from . import withdraw_data # 提现分析
from . import plate_alert   # 平台功能弹窗