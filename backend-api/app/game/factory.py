# -*- coding: utf-8 - *-
# @Time: 2023/2/16
# @Author:Jack c

# ================================ 厂商列表========================
from app.game import game
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app import public_util
from app.util import login_required
import sys, os, time

import importlib

importlib.reload(sys)



# 获取集成商列表
@game.route('/admin/factory_list_post', methods=['POST'])
@login_required
def factory_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        page = request.values.get('page', '1')
        limit = int(request.values.get('limit', '20'))
        offset = (int(page) - 1) * limit
        sql = "select factory_id 'id',factory_name '名称',add_time '添加日期',status '状态' from san_factory_list order by factory_id limit %s, %s "
        sql2 = "select count(*) `count` from san_factory_list "
        mysql = Mysql()
        res = mysql.getAll(sql, [offset, limit])
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['添加日期'] = str(d['添加日期'])
            data['data'] = res
            data['count'] = int(cont['count'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加集成商
@game.route('/admin/add_factory_post', methods=['POST'])
@login_required
def add_factory_post():
        data = dict()
        data['code'] = 0
        data['status'] = 0
        data['msg'] = '添加失败！'
        try:
            factory_name = request.values.get('factory_name')
            if public_util.get_table_info('san_factory_list','factory_name=%s',factory_name):
                data['msg'] = '该集成商已存在'
            else:
                mysql = Mysql()
                sql = "insert into san_factory_list(factory_name,add_time) values (%s,now())"
                res = mysql.insertOne(sql, [factory_name])
                mysql.dispose()
                if res:
                    data['code'] = 1
                    data['status'] = 1
                    data['msg'] = '添加成功！'
        except Exception as e:
            print(e)
        return jsonify(data)





# 编辑集成商
@game.route('/admin/update_factory_post', methods=['POST'])
@login_required
def update_factory_post():
        data = dict()
        data['code'] = 0
        data['status'] = 0
        data['msg'] = '修改失败!'
        try:
            factory_id = request.values.get("factory_id")
            factory_name = request.values.get('factory_name')
            mysql = Mysql()
            update_sql = "update san_factory_list set factory_name=%s where factory_id=%s"
            res = mysql.update(update_sql, [factory_name, factory_id])
            mysql.dispose()
            if res:
                data['status'] = 1
                data['msg'] = '修改成功！'
                data['code'] = 1
        except Exception as e:
            print(e)
        return jsonify(data)


# 删除集成商
@game.route('/admin/delete_factory_post', methods=['post'])
@login_required
def delete_factory_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        factory_id = request.values.get('factory_id')
        if public_util.get_table_info('san_game_list','factory_id=%s',factory_id):
            data['msg'] = "该集成商下有平台"
        else:
            mysql = Mysql()
            sql = "delete from san_factory_list where factory_id = %s"
            res = mysql.delete(sql, [factory_id])
            mysql.dispose()
            if res:
                data['code'] = 1
                data['status'] = 1
                data['msg'] = "成功！"
    except Exception as e:
        print(e)
    return jsonify(data)


# 更新集成商状态
@game.route('/admin/update_factory_status', methods=['post'])
@login_required
def admin_update_factory_status():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        status = request.values.get('status')
        factory_id = request.values.get('factory_id')
        mysql = Mysql()
        sql = "update san_factory_list set status = %s where factory_id = %s"
        res = mysql.update(sql, [status, factory_id])
        mysql.dispose()
        if res:
            data['code'] = 1
            data['msg'] = "成功！！"
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
