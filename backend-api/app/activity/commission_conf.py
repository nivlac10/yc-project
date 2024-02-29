# coding=utf-8


from . import activity
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
import sys

import importlib
from .. import util_update_redis

importlib.reload(sys)


# 获取邀请任务列表
@activity.route('/admin/invite_task_list_post', methods=['post'])
@login_required
def invite_task_list_post():
    data = dict()
    data['count']=0
    data['code'] = 0
    data['data']=[]
    try:
        page = request.values.get('page', '1')
        limit = request.values.get('limit', '20')
        offset = (int(page) - 1) * int(limit)
        sql = "select * from san_user_invite_task order by task_id limit %s, %s" % (offset, limit)
        sql2 = "select count(*) count from san_user_invite_task"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            data['count'] = int(cont['count'])
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 查询返佣配置
@activity.route('/admin/task_conf_list_post', methods=['post'])
@login_required
def task_conf_list_post():
    data = dict()
    data['code'] = 0
    data['data']=[]
    try:
        mysql = Mysql()
        sql="select invit_recharge_gift,one_bet_rebate,two_bet_rebate,three_bet_rebate from san_conf"
        res = mysql.getAll(sql, None)
        mysql.dispose()
        if res :
            data['code'] = 1
            data['data'] = res
    except Exception as e:
        print(e)
    return jsonify(data)




# 修改返佣配置
@activity.route('/admin/update_data_conf', methods=['post'])
@login_required
def update_data_conf():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        key_list = ['invit_recharge_gift', 'one_bet_rebate', 'two_bet_rebate', 'three_bet_rebate' ]
        maps = dict()
        for d in key_list:
            maps[d] = request.values.get(d)
        sql = "update san_conf set "
        params = []
        for k in key_list:
            sql += k + " = %s,"
            params.append(maps[k])
        sql = sql[:-1]
        mysql = Mysql()
        res = mysql.update(sql, params)
        mysql.dispose()
        if res >= 0:
            util_update_redis.get_conf_all()
            data['msg'] = '操作成功'
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)




# 添加邀请任务
@activity.route('/admin/add_invite_task_post', methods=['post'])
@login_required
def add_invite_task_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        task_name = request.values.get('task_name')
        num = request.values.get('num')
        money = request.values.get('money')
        sql = "insert into san_user_invite_task (task_name, num, money) values(%s, %s, %s)"
        mysql = Mysql()
        res = mysql.insertOne(sql, [task_name, num, money])
        mysql.dispose()
        if res:
            util_update_redis.san_user_invite_task()
            data['code'] = 1
            data['msg'] = "操作成功！！"
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改邀请任务
@activity.route('/admin/update_invite_task_post', methods=['post'])
@login_required
def update_invite_task_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        task_id = request.values.get('task_id')
        task_name = request.values.get('task_name')
        num = request.values.get('num')
        money = request.values.get('money')
        sql = "update  san_user_invite_task set  task_name = %s, num = %s, money = %s  where task_id = %s "
        mysql = Mysql()
        res = mysql.update(sql, [task_name, num, money,task_id])
        mysql.dispose()
        if res:
            util_update_redis.san_user_invite_task()
            data['msg'] = "操作成功！！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除邀请任务
@activity.route('/admin/delete_invite_task_post', methods=['post'])
@login_required
def delete_invite_task_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        task_id = request.values.get('task_id')
        sql = "delete from san_user_invite_task where task_id = %s"
        mysql = Mysql()
        res = mysql.delete(sql, [task_id])
        mysql.dispose()
        if res:
            util_update_redis.san_user_invite_task()
            data['msg'] = "操作成功！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
