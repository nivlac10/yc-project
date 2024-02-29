from . import admin
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app.util import user_power
from app.my_session import MySession
from app import redis


# 用户权限
@admin.route('/admin/user_power', methods=['post', 'get'])
@login_required
def user_power():
    token = request.headers.get('Authorization')
    admin_uid = redis.hget(token, 'n')
    data = {}
    data['contentManagement'] = []
    try:
        con = get_user_status(admin_uid)
        if con is None:
            return jsonify(data)
        if con['admintype'] == 1:
            data['contentManagement'] = admin_power()
        else:
            if get_power(con['router_str']) is None:
                return jsonify(data)
            data['contentManagement'] = admin_power(con['router_str'],con['interface_str'])
    except Exception as e:
        print (e)
    return jsonify(data)


# 查询状态正常用户
def get_user_status(username):
    sql = "select * FROM san_administrator WHERE id = '%s' and status = 1" % username
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 超级管理员权限
def admin_power( router_str='',interface_str=''):
    sql = "select * FROM san_power_class WHERE 1=1"
    sql2 = "select * FROM san_power_router WHERE 1=1"
    sql3 = "select * FROM san_power_interface WHERE 1=1"
    if router_str:
        sql2 += " and rid in(%s)" % router_str
        sql += " and cid in(select cid from san_power_router where rid in(%s))" % router_str
        sql3 += " and jid in(select cid from san_power_router where rid in(%s))" % router_str
    sql += " ORDER BY c_index desc, cid ASC"
    sql2 += " order by r_index desc, rid asc"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    con = mysql.getAll(sql2, None)
    mysql.dispose()
    arr = []
    if res:
        for d in res:
            p = {}
            p['title'] = d['class_name']
            p['icon'] = d['icon']
            p['href'] = ''
            p['spread'] = False
            p['children'] = []
            if con:
                m = []
                for k in con:
                    if d['cid'] == k['cid']:
                        maps = {}
                        maps['title'] = k['router_name']
                        maps['href'] = k['router_url']
                        maps['spread'] = False
                        m.append(maps)
                p['children'] = m
            arr.append(p)
    return arr


# 获取用户权限模块
def get_power(router_str):
    router_str = router_str.strip()
    if router_str == '':
        return None
    sql = "select * FROM san_power_class WHERE cid in(select cid from san_power_router where rid in(%s))" % router_str
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res