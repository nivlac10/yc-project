# coding=utf-8


from app.game import game
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import  util_update_redis, redis, public_util, RKEY
from SqlConntion.RedisDB import Redis
import sys

import importlib

importlib.reload(sys)
PATH = 'game_type/'



# 获取游戏类型列表
@game.route('/admin/game_type_list_post', methods=['post'])
@login_required
def game_type_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        page = request.values.get('page', '1')
        limit = request.values.get('limit', '20')
        offset = (int(page) - 1) * int(limit)
        sql = "select * from san_game_type_list order by status desc, sort_index desc limit %s, %s" % (offset, limit)
        sql2 = "select count(*) count from san_game_type_list"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            redis_R = Redis()
            url_host = redis_R.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
            redis_R.close()
            # for item in res:
            #     item['rakeback_open']='关闭' if item['rakeback_open']==0 else '开启'
            #     item['status']='关闭' if item['status']==0 else '开启'
                # item['icon'] = url_host + item['icon']
            data['data'] = res
            data['count'] = int(cont['count'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 禁用类型
@game.route('/admin/update_game_type_status_post', methods=['post'])
@login_required
def update_game_type_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        status = request.values.get('status')
        id = request.values.get('id')
        sql = "update san_game_type_list set status = '%s' where id = '%s'" % (status, id)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.game_data_version_rise()
            data['msg'] = "操作成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加类型
@game.route('/admin/add_game_type_post', methods=['post'])
@login_required
def add_game_type_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        type_name = request.values.get('type_name')
        type = request.values.get('type')
        # icon = request.files.get('icon')
        rakeback_open = request.values.get('rakeback_open')
        status = request.values.get('status')
        sort_index = request.values.get('sort_index')
        jump_route = request.values.get('jump_route')

        is_con, data['msg'] = get_type_list(id,type_name,type)
        if is_con:
            return jsonify(data)
        # icon_url = public_util.Get_image_url(icon,PATH)
        sql = "insert into san_game_type_list (type_name, type, rakeback_open, status, sort_index, jump_route) " \
              "values(%s, %s, %s, %s, %s, %s)"
        mysql = Mysql()
        res = mysql.insertOne(sql, [type_name, type, rakeback_open, status, sort_index, jump_route])
        mysql.dispose()
        if res:
            util_update_redis.game_data_version_rise()
            data['msg'] = "操作成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改公告
@game.route('/admin/update_game_type_post', methods=['post'])
@login_required
def update_game_type_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        id = request.values.get("id")
        type_name = request.values.get('type_name')
        type = request.values.get('type')
        icon = request.files.get('icon')
        rakeback_open = request.values.get('rakeback_open')
        status = request.values.get('status')
        sort_index = request.values.get('sort_index')
        jump_route = request.values.get('jump_route')
        is_con,data['msg'] = get_type_list(id,type_name,type)
        if is_con:
            return jsonify(data)
        sql = "update  san_game_type_list set  type_name = %s, type = %s, rakeback_open = %s, " \
              "status = %s,sort_index=%s, jump_route= %s "
        params = [type_name, type,  rakeback_open, status, sort_index, jump_route]
        if icon:
            icon_url = public_util.Get_image_url(icon,PATH)
            sql += ", icon = %s"
            params.append(icon_url)
        sql += " where id = %s "
        params.append(id)
        mysql = Mysql()
        res = mysql.update(sql, params)
        mysql.dispose()
        if res:
            util_update_redis.game_data_version_rise()
            data['msg'] = "操作成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除游戏类型
@game.route('/admin/delete_game_type_post', methods=['post'])
@login_required
def delete_game_type_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        id = request.values.get('id')
        sql = "delete from san_game_type_list where id = '%s'" % id
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.game_data_version_rise()
            data['msg'] = "操作成功！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)

# 查询是否存在该名称或类型
def get_type_list(id,type_name,type):
    data = ''
    code = False
    sql = "select * from san_game_type_list where id != '%s' and (type_name = '%s' or type= '%s')"%(id, type_name,type)
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    if res:
        for item in res:
                if str(type_name) == str(item['type_name']):
                    code = True
                    data = "该名称已存在！"
                if str(type) == str(item['type']):
                    code = True
                    data = "该类型已存！"
    return code,data
