from . import activity
from app.util import login_required
from app.util import user_power
from flask import request, jsonify
from SqlConntion.MySqlConn import Mysql
from app import RKEY,redis,util_update_redis,public_util
from SqlConntion.RedisDB import Redis

PATH = 'banner/'

# 获取列表
@activity.route('/admin/banner_list_post', methods=['post'])
@login_required
def banner_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        page = request.values.get('page', '1')
        limit = request.values.get('limit', '20')
        offset = (int(page) - 1) * int(limit)
        sql = "select * from san_banner_list order by status desc, sort_index desc,bid asc limit %s, %s" % (offset, limit)
        sql2 = "select count(*) count from san_banner_list"
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



# 禁用轮播图
@activity.route('/admin/update_banner_status_post', methods=['post'])
@login_required
def update_banner_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        status = request.values.get('status')
        bid = request.values.get('bid')
        sql = "update san_banner_list set status = '%s' where bid = '%s'" % (status, bid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            data['msg'] = "操作成功！！"
            util_update_redis.set_reds_san_banner_list()
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加轮播图
@activity.route('/admin/add_banner_post', methods=['post'])
@login_required
def add_banner_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        img_file = request.files.get('img_url')
        type = request.values.get('type')
        url = request.values.get('url')
        sort_index = request.values.get('sort_index')
        img_url = public_util.Get_image_url(img_file,PATH)
        sql = "insert into san_banner_list (add_time,img_url,type,url ,sort_index) values(Now(), %s,%s,%s,%s)"
        mysql = Mysql()
        res = mysql.insertOne(sql, [img_url, type, url, sort_index])
        mysql.dispose()
        if res:
            data['msg'] = "操作成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改轮播图
@activity.route('/admin/detail_banner_post', methods=['post'])
@login_required
def detail_banner_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        bid = request.values.get('bid')
        type = request.values.get('type')
        url = request.values.get('url')
        sort_index = request.values.get('sort_index')
        img_file = request.files.get('img_url')
        sql = "update  san_banner_list set  type = %s , url = %s, sort_index = %s "
        params = [type, url, sort_index]
        if img_file:
            img_url = public_util.Get_image_url(img_file,PATH)
            sql += ", img_url =%s"
            params.append(img_url)
        sql += " where bid = %s "
        params.append(bid)
        mysql = Mysql()
        res = mysql.update(sql,params)
        mysql.dispose()
        if res:
            util_update_redis.set_reds_san_banner_list()
            data['msg'] = "操作成功！！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除轮播图
@activity.route('/admin/delete_banner_post', methods=['post'])
@login_required
def delete_banner_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = "操作失败！"
    try:
        bid = request.values.get('bid')
        sql = "delete from san_banner_list where bid = '%s'" % bid
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res:
            util_update_redis.set_reds_san_banner_list()
            data['msg'] = "操作成功！"
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
