from . import activity
from flask import request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app.util import user_power
from app import util_update_redis, redis, RKEY
from SqlConntion.RedisDB import Redis
from app import public_util

PATH = 'activity/'


# 查询活动配置列表
@activity.route('/admin/activity_list_post', methods=['post'])
@login_required
def activity_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        limit = request.values.get('limit', '20')
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql = "select * from san_activity_list order by sort_index asc limit %d,%d" % (int(offset), int(limit))
        sql_count = "select count(*) cou from san_activity_list"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        res_count = mysql.getOne(sql_count, None)
        mysql.dispose()
        if res:
            redis_R = Redis()
            url_host = redis_R.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
            redis_R.close()
            for item in res:
                item['add_time'] = str(item['add_time'])
                item['img_url'] = url_host + item['img_url']
                item['icon_url'] = url_host + item['icon_url']
            data['count'] = int(res_count['cou'])
            data["data"] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 新增活动配置
@activity.route('/admin/activity_add_post', methods=['post'])
@login_required
def activity_add_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        title = request.values.get('title')
        button_name = request.values.get('button_name')
        icon_url = request.files.get('icon_url')
        img_url = request.files.get('img_url')
        info = request.values.get('info')
        type = request.values.get('type')
        url = request.values.get('url')
        sort_index = request.values.get('sort_index')
        img_url = public_util.Get_image_url(img_url, PATH)
        icon_url = public_util.Get_image_url(icon_url, PATH)
        sql = "insert into san_activity_list (info, add_time, title, img_url, icon_url, type,url ,sort_index,button_name) " \
              "values(%s, Now(), %s, %s, %s,%s,%s,%s,%s)"
        mysql = Mysql()
        res = mysql.insertOne(sql, [info, title, img_url, icon_url, type, url, sort_index, button_name])
        mysql.dispose()
        if res:
            util_update_redis.add_activity_data()
            data['msg'] = "操作成功！！"
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改活动配置状态
@activity.route('/admin/activity_Disable_post', methods=['post'])
@login_required
def activity_Disable_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        status = request.values.get('status')
        aid = request.values.get('aid')
        sql = "update san_activity_list set status = '%s' where aid = '%s'" % (status, aid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.add_activity_data()
            data['code'] = 1
            data['msg'] = "操作成功！！"
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改活动配置
@activity.route('/admin/activity_update_post', methods=['post'])
@login_required
def activity_update_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        aid = request.values.get('aid')
        title = request.values.get('title')
        img_url = request.files.get('img_url')
        icon_url = request.files.get('icon_url')
        info = request.values.get('info')
        type = request.values.get('type')
        url = request.values.get('url')
        button_name = request.values.get("button_name")
        sort_index = request.values.get('sort_index')
        params = [info, title, type, url, sort_index, button_name]
        sql = "update san_activity_list set info=%s, title=%s, type=%s, url=%s, sort_index=%s,button_name=%s"
        img_str = public_util.Get_image_url(img_url, PATH)
        if img_url:
            sql += ", img_url = %s"
            params.append(img_str)
        icon_str = public_util.Get_image_url(icon_url, PATH)
        if icon_url:
            sql += ", icon_url = %s"
            params.append(icon_str)
        sql += " where aid=%s"
        params.append(aid)
        mysql = Mysql()
        res = mysql.update(sql, params)
        mysql.dispose()
        if res:
            util_update_redis.add_activity_data()
            data['code'] = 1
            data['msg'] = "操作成功！！"
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除活动
@activity.route('/admin/activity_delete_post', methods=['post'])
@login_required
def activity_delete_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        aid = request.values.get('aid')
        sql = "delete from san_activity_list where aid = '%s'" % aid
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.add_activity_data()
            data['code'] = 1
            data['msg'] = "操作成功！"
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
