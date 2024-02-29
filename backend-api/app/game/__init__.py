#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/06/20 17:33
# @Author : 78957
from flask import Blueprint

game = Blueprint('game', __name__)


from . import factory               # 集成商

from . import game_list             # 游戏厂商详情
from . import game_data             # 游戏平台数据
from . import game_data_external    # 游戏数据
from . import game_data_factory     # 用户游戏平台数据
from . import game_type             # 游戏类型
from . import game_user             # 用户游戏信息
from . import external_game         # 游戏
from . import game_bet_log         # 游戏打码日志