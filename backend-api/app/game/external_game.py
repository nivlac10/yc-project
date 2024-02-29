# coding=utf-8
import json
import os

from app.game import game
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import RKEY, common, util_update_redis, redis, public_util
from SqlConntion.RedisDB import Redis
import sys

import importlib

importlib.reload(sys)
PATH = "game_icon/"




# 查询游戏厂商
@game.route('/admin/factory_game_list', methods=['post'])
@login_required
def admin_factory_game_list():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['data'] = []
    try:
        my_game = request.values.get('my_game')
        mysql = Mysql()
        sql = "select * from san_game_list "
        if my_game:
            sql += " where my_game='%s'" % my_game
        res = mysql.getAll(sql, None)
        mysql.dispose()
        if res:
            data['data'] = res
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)

# 游戏列表
@game.route('/admin/external_game_conf_post', methods=['post'])
@login_required
def external_game_conf_post():
    data =dict()
    sql = "select game_id, game_name,factory_id from san_game_list "
    sql1 = "select factory_id,factory_name from san_factory_list "
    mysql = Mysql()
    game_type_list = json.loads(redis.get("task_game_type_list")) if redis.get(
        "task_game_type_list") else []
    data['code']=1
    data['game_list'] = mysql.getAll(sql, None)
    data['factory_list'] = mysql.getAll(sql1, None)
    data['game_type_list'] = game_type_list
    mysql.dispose()
    return jsonify(data)


# 获取列表
@game.route('/admin/external_game_list_post', methods=['post'])
@login_required
def external_game_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        page = request.values.get('page', '1')
        limit = request.values.get('limit', '20')
        gid = request.values.get('gid', '')
        game_type = request.values.get('game_type', '')
        game_id = request.values.get('game_id', '')
        status = request.values.get('status', '')
        my_game = request.values.get('my_game')
        is_hot = request.values.get('is_hot')
        is_top = request.values.get('is_top')
        is_demo = request.values.get('is_demo')
        offset = (int(page) - 1) * int(limit)
        sql = "select a.*,b.game_name platform_name,b.factory_id,c.factory_name " \
              "from san_external_game_list a left join san_game_list b on " \
              "a.game_id = b.game_id left join san_factory_list as c on b.factory_id=c.factory_id  "
        sql2 = "select count(*) count from san_external_game_list as a "
        sql_list = []
        if gid:
            sql_list.append(" (locate('%s', a.gid) or locate('%s', a.game_name))" % (gid, gid))
        if game_type:
            sql_list.append("  a.game_type = '%s'" % game_type)
        if game_id:
            sql_list.append("  a.game_id = '%s'" % game_id)
        if status:
            sql_list.append(" a.status = '%s'" % status)
        if my_game:
            sql_list.append(" a.my_game = '%s'" % my_game)
        if is_hot:
            sql_list.append("  a.is_hot = '%s'" % is_hot)
        if is_top:
            sql_list.append("  a.is_top = '%s'" % is_top)
        if is_demo:
            sql_list.append("  a.is_demo = '%s'" % is_demo)
        sql_str = public_util.data_list_to_str(sql_list)
        sql += sql_str
        sql2 += sql_str
        sql += " order by a.status desc ,a.sort_index,a.gid  asc limit %s, %s" % (offset, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            arr = ['自动', '横屏', '竖屏']
            redis_R = Redis()
            url_host = redis_R.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
            redis_R.close()
            for item in res:
                # item['screen'] = arr[item['screen']]

                if item['icon']:
                    item['icon'] = url_host + item['icon']
                # game_type_list = json.loads(redis.get("task_game_type_list")) if redis.get(
                #     "task_game_type_list") else []
                # for type in game_type_list:
                #     if item['game_type'] == type['type']:
                #         item['game_type'] = type['type_name']
            data['count'] = int(cont['count'])
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 添加游戏
@game.route('/admin/add_external_game_post', methods=['post'])
@login_required
def external_add_game_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '添加失败！'
    try:
        game_name = request.values.get('game_name')
        sort_index = request.values.get('sort_index')
        game_type = request.values.get('game_type')
        game_id = request.values.get('game_id')
        my_game = request.values.get('my_game')
        screen = request.values.get('screen')
        is_hot = request.values.get('is_hot')
        is_top = request.values.get('is_top')
        is_demo = request.values.get('is_demo')
        sql = "insert into san_external_game_list(game_name,sort_index,game_type, game_id, screen,my_game,is_hot,is_top,is_demo) values(" \
              "%s,%s,%s,%s,%s, %s,%s,%s, %s)"
        mysql = Mysql()
        res = mysql.insertOne(sql, [game_name, sort_index, game_type, game_id, screen, my_game, is_hot, is_top, is_demo])
        mysql.dispose()
        if res:
            # 更新版本号
            util_update_redis.game_data_version_rise()
            data['status'] = 1
            data['msg'] = '添加成功！'
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改游戏
@game.route('/admin/external_game_detail_post', methods=['post'])
@login_required
def external_game_detail_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '修改失败！'
    try:
        game_id = request.values.get('game_id')
        my_game=request.values.get('my_game')
        game_name = request.values.get('game_name')
        sort_index = request.values.get('sort_index')
        game_type = request.values.get('game_type')
        gid = request.values.get('gid')
        screen = request.values.get('screen')
        min_enter_money = request.values.get('min_enter_money')
        min_recharge_money = request.values.get('min_recharge_money')
        is_hot = request.values.get('is_hot')
        is_top = request.values.get('is_top')
        is_demo = request.values.get('is_demo')
        sql = "update san_external_game_list set game_name = '%s', sort_index = '%s', screen = '%s'" \
              ", game_type = '%s', game_id = '%s',min_enter_money='%s'," \
              "min_recharge_money='%s',is_hot='%s',is_top = '%s',is_demo = '%s', my_game='%s'  where gid = '%s'"\
              %(game_name, sort_index, screen, game_type, game_id, min_enter_money, min_recharge_money,
                 is_hot, is_top,is_demo, my_game,gid)
        # params = [game_name, sort_index, screen, game_type, platform_id, min_enter_money, min_recharge_money,
        #          is_hot, is_top, game_id]
        # if file:
        #     icon = public_util.save_game_img_file(public_util.PATH_FILE + PATH, file, gid)
        #     image_url = PATH + icon
        #     sql += ", icon = %s"
        #     params.append(image_url)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            # 更新版本号
            util_update_redis.game_data_version_rise()
            data['status'] = 1
            data['msg'] = '修改成功！'
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除游戏
@game.route('/admin/delete_external_game_post', methods=['post'])
@login_required
def delete_external_game_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        gid = request.values.get('gid')
        sql = "delete from san_external_game_list where gid = %s"
        mysql = Mysql()
        res = mysql.delete(sql, [gid])
        mysql.dispose()
        if res:
            util_update_redis.game_data_version_rise()
            data['msg'] = "操作成功！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 禁用游戏
@game.route('/admin/update_external_game_status_post', methods=['post'])
@login_required
def update_external_game_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        status = request.values.get('status')
        gid = request.values.get('gid')
        sql = "update san_external_game_list set status = %s where gid = %s"
        mysql = Mysql()
        res = mysql.update(sql, [status, gid])
        mysql.dispose()
        if res:
            util_update_redis.game_data_version_rise()
            data['msg'] = "操作成功！！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 保存图片到本地
def save_img_file(path, file_img, gid):
    img_name = ''
    try:
        if file_img:
            file_name = file_img.filename
            if os.path.exists(path) is False:
                os.makedirs(path)
            names = file_name.split('.')
            img_name = str(gid) + '.' + names[len(names) - 1]
            img_local_path = os.path.join(path, img_name)
            file_img.save(img_local_path)
    except Exception as e:
        print(e)
    return img_name