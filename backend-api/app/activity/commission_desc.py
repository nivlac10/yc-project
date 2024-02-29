# coding=utf-8


from . import activity
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import util_update_redis
import sys

import importlib

importlib.reload(sys)



# 获取佣金活动列表
@activity.route('/admin/commission_desc_list_post', methods=['post'])
@login_required
def commission_desc_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] =0
    try:
        page = request.values.get('page', '1')
        limit = request.values.get('limit', '20')
        offset = (int(page) - 1) * int(limit)
        sql = "select a.* ,b.title as aTitle from san_commission_desc_list as a " \
              "left join san_activity_list as b on a.aid=b.aid" \
              " order by a.status desc,a.sort_index desc , a.id asc limit %s, %s" % (offset, limit)
        sql2 = "select count(*) count from san_commission_desc_list"
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


# 禁用佣金活动简介
@activity.route('/admin/update_commission_desc_status_post', methods=['post'])
@login_required
def update_commission_desc_status_post():
    data = dict()
    data['status'] = 0
    data['code'] = 0
    data['msg'] = "操作失败！"
    try:
        status = request.values.get('status')
        id = request.values.get('id')
        sql = "update san_commission_desc_list set status = '%s' where id = '%s'" % (status, id)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.set_reds_san_commission_desc_list()
            data['msg'] = "操作成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加佣金活动简介
@activity.route('/admin/add_commission_desc_post', methods=['post'])
@login_required
def add_commission_desc_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        info = request.values.get('info')
        title = request.values.get('title')
        aid = request.values.get('aid')
        sort_index = request.values.get("sort_index")
        sql = "insert into san_commission_desc_list (info, title,aid,sort_index) values(%s, %s, %s,%s)"
        mysql = Mysql()
        res = mysql.insertOne(sql, [info, title, aid, sort_index])
        mysql.dispose()
        if res:
            data['code'] = 1
            data['msg'] = "操作成功！！"
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改佣金活动简介
@activity.route('/admin/update_commission_desc_post', methods=['post'])
@login_required
def update_commission_desc_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        info = request.values.get('info')
        title = request.values.get('title')
        id = request.values.get('id')
        aid = request.values.get('aid')
        sort_index = request.values.get("sort_index")
        sql = "update  san_commission_desc_list set info = %s, title = %s, aid = %s,sort_index=%s where id = %s"
        mysql = Mysql()
        res = mysql.update(sql, [info, title, aid, sort_index, id])
        mysql.dispose()
        if res:
            util_update_redis.set_reds_san_commission_desc_list()
            data['msg'] = "操作成功！！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除佣金活动简介
@activity.route('/admin/delete_commission_desc_post', methods=['post'])
@login_required
def delete_commission_desc_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        id = request.values.get('id')
        sql = "delete from san_commission_desc_list where id = '%s'" % id
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.set_reds_san_commission_desc_list()
            data['msg'] = "操作成功！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
