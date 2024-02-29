# coding=utf-8
import json

from app.game import game
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import util_update_redis, redis, public_util, RKEY
import sys

import importlib
from SqlConntion.RedisDB import Redis

importlib.reload(sys)
PATH = 'cover/'

# 平台列表
@game.route('/admin/game_conf_post', methods=['post'])
@login_required
def game_conf_post():
    data=dict()
    data['code']=1
    mysql = Mysql()
    sql = "select * from san_factory_list where status=1"
    data['data'] = mysql.getAll(sql, None)
    mysql.dispose()
    return jsonify(data)

# 获取列表
@game.route('/admin/game_list_post', methods=['post'])
@login_required
def game_list_post():
    data = dict()
    data['data'] = []
    data['count'] = 0
    data['code'] = 0
    try:
        page = request.values.get('page', '1')
        limit = int(request.values.get('limit', '20'))
        gid = request.values.get('gid', '')
        game_type = request.values.get('game_type', '')
        status = request.values.get('status', '')
        factory_id = request.values.get('factory_id')
        offset = (int(page) - 1) * limit
        sql_list = []
        if gid:
            sql_list.append(" (locate('%s', a.game_id) or locate('%s', a.game_name)) " % (gid, gid))
        if game_type:
            sql_list.append(" a.game_type = %s " % game_type)
        if factory_id:
            sql_list.append(" a.factory_id= '%s' " % factory_id)
        if status:
            sql_list.append(" a.status = %s " % status)
        sql_str = public_util.data_list_to_str(sql_list)
        sql = "select a.*,b.factory_name from san_game_list " \
              "as a  left join san_factory_list as b on a.factory_id=b.factory_id %s  " \
              "order by a.status desc ,a.sort_index desc, a.game_id  asc limit %s, %s" % (sql_str,offset, limit)
        sql2 = "select count(*) count from san_game_list  as a %s "%sql_str
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            redis_R = Redis()
            url_host = redis_R.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
            redis_R.close()
            for item in res:
                if item['cover']:
                    item['cover'] = url_host + item['cover']
                game_type_list = json.loads(redis.get("task_game_type_list")) if redis.get("task_game_type_list") else []
                item['add_time'] = str(item['add_time'])
            data['data'] = res
            data['count'] = int(cont['count'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 添加厂商
@game.route('/admin/add_game_post', methods=['post'])
@login_required
def add_game_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '添加失败！'
    try:
        file = request.files.get('file')
        game_name = request.values.get('game_name')
        sort_index = request.values.get('sort_index')
        game_type = request.values.get('game_type')
        factory_id = request.values.get('factory_id')
        cover = public_util.Get_image_url(file,PATH)
        sql = "insert into san_game_list(game_name,sort_index,game_type,cover,factory_id,add_time) values(%s,%s,%s,%s,%s,Now())"
        mysql = Mysql()
        res = mysql.insertOne(sql, [game_name, sort_index, game_type, cover, factory_id])
        mysql.dispose()
        if res:
            # 更新版本号
            util_update_redis.game_data_version_rise()
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '添加成功！'
    except Exception as e:
        print(e)
    return jsonify(data)



# 修改厂商
@game.route('/admin/game_detail_post', methods=['post'])
@login_required
def game_detail_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '修改失败！'
    try:
        game_id = request.values.get('game_id')
        file = request.files.get('file')
        game_name = request.values.get('game_name')
        sort_index = request.values.get('sort_index')
        game_type = request.values.get('game_type')
        factory_id = request.values.get('factory_id')
        status = request.values.get('status')
        sql = "update san_game_list set game_name = %s, sort_index = %s,factory_id=%s" \
              ",  game_type = %s, status = %s"
        parame=[game_name, sort_index, factory_id, game_type, status]
        if file:
            cover = public_util.Get_image_url(file,PATH)
            sql += ", cover = %s"
            parame.append(cover)
        sql += " where game_id = %s"
        parame.append(game_id)
        mysql = Mysql()
        res = mysql.update(sql, parame)
        mysql.dispose()
        if res:
            # 更新版本号
            util_update_redis.game_data_version_rise()
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '修改成功！'
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除厂商
@game.route('/admin/delete_game_post', methods=['post'])
@login_required
def delete_game_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        game_id = request.values.get('game_id')
        sql = "delete from san_game_list where game_id = '%s'" % game_id
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.game_data_version_rise()
            data['code'] = 1
            data['status'] = 1
            data['msg'] = "成功！"
    except Exception as e:
        print(e)
    return jsonify(data)


# 禁用厂商
@game.route('/admin/update_game_status_post', methods=['post'])
@login_required
def update_game_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        status = request.values.get('status')
        game_id = request.values.get('game_id')
        sql = "update san_game_list set status = '%s' where game_id = '%s'" % (status, game_id)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.game_data_version_rise()
            data['msg'] = "成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
