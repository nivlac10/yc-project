# coding=utf-8
import os
import time



from . import admin
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import util_update_redis
import sys

import importlib

importlib.reload(sys)



# 获取列表
@admin.route('/admin/notice_list_post', methods=['post'])
@login_required
def notice_list_post():
    data = dict()
    data['code'] = 0
    data['count'] = 0
    data['data'] = []
    try:
        page = request.values.get('page', '1')
        limit = request.values.get('limit', '20')
        offset = (int(page) - 1) * int(limit)
        sql = "select * from san_notice_list order by status desc," \
              "sort_index desc, id asc limit %s, %s" % (offset, limit)
        sql2 = "select count(*) count from san_notice_list"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for item in res:
                item['add_time'] = str(item['add_time'])
            data['count'] = int(cont['count'])
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 禁用公告
@admin.route('/admin/update_notice_status_post', methods=['post'])
@login_required
def update_notice_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        status = request.values.get('status')
        id = request.values.get('id')
        sql = "update san_notice_list set status = '%s' where id = '%s'" % (status, id)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            data['msg'] = "成功！！"
            data['status'] = 1
            data['code'] = 1
            util_update_redis.add_notice_data()
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加公告
@admin.route('/admin/add_notice_post', methods=['post'])
@login_required
def add_notice_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        info = request.values.get('info')
        title = request.values.get('title')
        button_name = request.values.get('button_name')
        sort_index = request.values.get('sort_index')
        url = request.values.get('url')
        type = request.values.get("type")
        add_time = request.values.get("add_time")
        sql = "insert into san_notice_list (info, add_time, title,button_name,sort_index,url,type)" \
              " values(%s, %s, %s,%s,%s,%s,%s)"
        mysql = Mysql()
        res = mysql.insertOne(sql, [info,add_time, title, button_name, sort_index, url, type])
        mysql.dispose()
        if res:
            util_update_redis.add_notice_data()
            data['msg'] = "成功！！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改公告
@admin.route('/admin/update_notice_post', methods=['post'])
@login_required
def update_notice_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        info = request.values.get('info')
        title = request.values.get('title')
        id = request.values.get('id')
        button_name = request.values.get('button_name')
        sort_index = request.values.get('sort_index')
        url = request.values.get('url')
        type = request.values.get("type")
        add_time = request.values.get("add_time")
        sql = "update san_notice_list set info = %s, title = %s,button_name=%s," \
              "sort_index=%s,url=%s,type=%s,add_time=%s where id = %s"
        mysql = Mysql()
        res = mysql.update(sql, [info, title, button_name, sort_index, url, type,add_time, id])
        mysql.dispose()
        if res:
            util_update_redis.add_notice_data()
            data['msg'] = "成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除公告
@admin.route('/admin/delete_notice_post', methods=['post'])
@login_required
def delete_notice_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "失败！"
    try:
        id = request.values.get('id')
        sql = "delete from san_notice_list where id = '%s'" % id
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.add_notice_data()
            data['status'] = 1
            data['code'] = 1
            data['msg'] = "成功！"
    except Exception as e:
        print(e)
    return jsonify(data)
