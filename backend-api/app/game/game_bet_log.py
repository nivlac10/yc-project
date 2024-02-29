#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-04-26
import importlib
import sys
import time

from flask import render_template, request, jsonify
from app import public_util
from app.util import login_required
from SqlConntion.MongoDBConn import MongoDB
from app.game import game

importlib.reload(sys)



# 获取游戏打码记录数据
@game.route('/admin/game_bet_log_post', methods=['post'])
@login_required
def game_bet_log_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['total'] = []
    try:
        # san_game_bet_log
        day = time.strftime('%Y-%m-%d')

        gid = request.values.get('gid')
        uid = request.values.get('uid')
        cid = request.values.get('cid')
        game_id = request.values.get('game_id')
        my_game = request.values.get('my_game')
        stime = request.values.get('stime', day)
        etime = request.values.get('etime', day)
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        mg_list = []
        if cid:
            mg_list.append({'cid': int(cid)})
        if game_id:
            mg_list.append({'game_id': int(game_id)})
        if gid:
            mg_list.append({'gid': int(gid)})
        if my_game:
            mg_list.append({'my_game': int(my_game)})
        if uid:
            mg_list.append({'$or': [{'uid': {'$regex':uid }},{'nickname': {'$regex':uid }},{'game_number': {'$regex':uid }}]})
        if stime:
            mg_list.append({'add_time': {'$gte': stime}})
        if etime:
            etime = etime+" 23:59:59"
            mg_list.append({'add_time': {'$lte': etime}})

        mg_str = public_util.dataMongo_list_to_str(mg_list)
        mongoDB = MongoDB()
        list_res = mongoDB.find_limit("san_game_bet_log", offset, limit, "add_time", filter=mg_str,sort_index=-1 )
        count_res = mongoDB.count_documents("san_game_bet_log", filter=mg_str)
        mongoDB.close()
        if list_res:
            for d in list_res:
                d['add_time'] = str(d['add_time'])
                d['_id'] = str(d['add_time'])
                d['gl'] = round(float(d['bet'])/float(d['shu_ying']),4) if float(d['shu_ying'])>0 else 0
            data['data'] = list_res
            data['count'] = count_res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


