from . import admin
from app.util import login_required
from flask import request, jsonify
from SqlConntion.MySqlConn import Mysql
from app import RKEY,redis,util_update_redis,public_util
from SqlConntion.RedisDB import Redis

PATH = 'alert/'

# 获取平台功能弹窗列表
@admin.route('/admin/plate_alert_list_post', methods=['post'])
@login_required
def plate_alert_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        page = request.values.get('page', '1')
        limit = request.values.get('limit', '20')
        offset = (int(page) - 1) * int(limit)
        sql = "select * from san_plate_alert_list order by sort_index asc limit %s, %s" % (offset, limit)
        sql2 = "select count(*) count from san_plate_alert_list"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            data['count'] = int(cont['count'])
            redis_R = Redis()
            url_host = redis_R.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
            redis_R.close()
            for item in res:
                item['add_time'] = str(item['add_time'])
                item['img_url'] = url_host + item['img_url']
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加平台功能弹窗
@admin.route('/admin/add_plate_alert_post', methods=['post'])
@login_required
def add_plate_alert_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        img_file = request.files.get('img_url')
        type = request.values.get('type')
        url = request.values.get('url')
        sort_index = request.values.get('sort_index')
        close_type = request.values.get('close_type')
        user_type = request.values.get('user_type')
        img_url = public_util.Get_image_url(img_file,PATH)
        sql = "insert into san_plate_alert_list (add_time,img_url,type,url ,sort_index,close_type,user_type) values(Now(), %s,%s,%s,%s,%s,%s)"
        mysql = Mysql()
        res = mysql.insertOne(sql, [img_url, type, url, sort_index,close_type,user_type])
        mysql.dispose()
        if res:
            util_update_redis.add_plate_alert_data()
            data['msg'] = "操作成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改平台功能弹窗
@admin.route('/admin/detail_plate_alert_post', methods=['post'])
@login_required
def detail_plate_alert_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        id = request.values.get('id')
        img_file = request.files.get('img_url')
        url = request.values.get('url')
        type = request.values.get('type')
        sort_index = request.values.get('sort_index')
        close_type = request.values.get('close_type')
        user_type = request.values.get('user_type')
        sql = "update  san_plate_alert_list set  type = %s , url = %s, sort_index = %s,close_type=%s,user_type=%s "
        params = [type, url, sort_index,close_type,user_type]
        if img_file:
            img_url = public_util.Get_image_url(img_file,PATH)
            sql += ", img_url =%s"
            params.append(img_url)
        sql += " where id = %s "
        params.append(id)
        mysql = Mysql()
        res = mysql.update(sql,params)
        mysql.dispose()
        if res:
            util_update_redis.add_plate_alert_data()
            data['msg'] = "操作成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 禁用平台功能弹窗
@admin.route('/admin/update_plate_alert_status_post', methods=['post'])
@login_required
def update_plate_alert_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        status = request.values.get('status')
        id = request.values.get('id')
        sql = "update san_plate_alert_list set status = '%s' where id = '%s'" % (status, id)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.add_plate_alert_data()
            data['msg'] = "操作成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)




# 删除平台功能弹窗
@admin.route('/admin/delete_plate_alert_post', methods=['post'])
@login_required
def delete_plate_alert_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        id = request.values.get('id')
        sql = "delete from san_plate_alert_list where id = '%s'" % id
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.add_plate_alert_data()
            data['msg'] = "操作成功！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
