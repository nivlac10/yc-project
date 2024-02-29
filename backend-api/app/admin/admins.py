from . import admin
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app.util import user_power
from app import public_util
import string, random, pyotp
import sys, qrcode, base64
from io import BytesIO
from app import redis


# 获取管理员数据
@admin.route('/admin/admin_list_post', methods=['post'])
@login_required
def admin_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    try:
        sql = "select * FROM san_administrator"
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        mysql.dispose()
        if res:
            for d in res:
                d['logintime'] = str(d['logintime']) if d['logintime'] else ''
                # d['time_int'] = public_util.days_int(d['logintime']) * 1000 if d['logintime'] else 0
            data['data'] = res
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 新增管理员处理
@admin.route('/admin/add_admin_post', methods=['post'])
@login_required
def add_admin_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        username = request.values.get('username')
        password = request.values.get('password')
        admintype = request.values.get('admintype')
        userinfo = request.values.get('userinfo')
        user = get_user(username)
        p_str = add_storage_pass(str(username), str(password))
        if user:
            data['status'] = 2
            data['msg'] = '账号已存在'
            return jsonify(data)
        user_key = pyotp.random_base32(32)
        sql = "insert INTO san_administrator(username, password, admintype, userinfo, user_key, addtime, " \
              "logintime) VALUES " \
              "('%s', '%s', '%s', '%s', '%s', now(), now())" % (username, p_str, admintype, userinfo, user_key)
        mysql = Mysql()
        res = mysql.insertOne(sql, None)
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
            # content = u'管理员' + request.cookies.get('admin_user', '') + '新增' + username + '的账号'
            # util.user_update_log('/admin/add_admin_post', 'admins', content, sql)
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改资料
@admin.route('/admin/admin_detail_post', methods=['post'])
@login_required
def admin_detail_post():
    data = dict()
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        uid = request.values.get('uid')
        userinfo = request.values.get('userinfo')
        sql = "update san_administrator SET userinfo = '%s' WHERE id = '%s'" % (userinfo, uid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res > 0:
            data['status'] = 1
            data['msg'] = '操作成功'
            content = u'管理员' + request.cookies.get('admin_user', '') + '修改了' + uid + '的账号'
            # util.user_update_log('/admin/admin_detail_post', 'admins', content, sql)
    except Exception as e:
        print(e)
    return jsonify(data)


# 更新管理员状态
@admin.route('/admin/update_admin_statue_post', methods=['post'])
@login_required
def update_admin_statue_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        uid = request.values.get('uid')
        token = request.headers.get('Authorization')
        admin_uid = redis.hget(token, 'n')
        status = request.values.get('status')
        sql = "update san_administrator SET status = '%s' WHERE id = '%s'" % (status, uid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
            status_str = u'激活' if status == '1' else u'禁用'
            content = u'管理员' + admin_uid + status_str + uid + '的账号'
            public_util.user_update_log('/admin/update_admin_statue_post', 'admins', content, sql)
    except Exception as e:
        print(e)
    return jsonify(data)


# 重置密钥
@admin.route('/admin/reset_admin_secret', methods=['post'])
@login_required
def reset_admin_secret():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '重置失败'
    try:
        uid = request.values.get('uid')
        user = get_uid(uid)
        if user is None:
            data['status'] = 2
            data['msg'] = '用户不存在'
            return jsonify(data)
        user_key = pyotp.random_base32(32)
        sql = "update san_administrator set user_key = '%s' where id = '%s'" % (user_key, uid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '重置成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改资料
@admin.route('/admin/update_admin_post', methods=['post'])
@login_required
def update_admin_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        uid = request.values.get('uid')
        token = request.headers.get('Authorization')
        admin_uid = redis.hget(token, 'n')
        user_name = request.values.get('user_name')
        userinfo = request.values.get('userinfo')
        sql = "update san_administrator SET userinfo = '%s',username='%s' WHERE id = '%s'" % (userinfo, user_name, uid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
            content = u'管理员' + admin_uid + '修改了' + uid + '的账号'
            public_util.user_update_log('/admin/update_admin_post', 'admins', content, sql)
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除管理员
@admin.route('/admin/delete_admin_one', methods=['post'])
@login_required
def delete_admin_one():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        uid = request.values.get('uid')
        token = request.headers.get('Authorization')
        admin_uid = redis.hget(token, 'n')
        user = get_uid(uid)
        if user is None:
            data['status'] = 2
            data['msg'] = '账号不存在'
            return jsonify(data)
        sql = "delete FROM san_administrator WHERE id = '%s'" % uid
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
            content = u'管理员' + str(admin_uid) + '删除' + user['username'] + '的账号'
            public_util.user_update_log('/admin/delete_admin_one', 'admins', content, sql)
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改用户权限
@admin.route('/admin/admin_power_post', methods=['post'])
@login_required
def admin_power_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        class_str = request.values.get('class_str')
        router_str = request.values.get('router_str')
        interface_str = request.values.get('interface_str')
        token = request.headers.get('uid')
        uid = redis.hget(token, 'n')
        sql = "update san_administrator SET class_str = '%s', router_str = '%s',interface_str='%s' WHERE id = '%s'" % \
              (class_str, router_str, interface_str, uid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 获取二维码
@admin.route('/admin/user_code_img', methods=['post'])
@login_required
def user_code_img():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '获取失败'
    data['data'] = ''
    try:
        uid = request.values.get('uid')
        user = get_uid(uid)
        if user is None:
            data['msg'] = '用户不存在'
            return jsonify(data)
        url = 'otpauth://totp/%s?secret=%s' % (user['username'], user['user_key'])
        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=15, border=1, )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        f = BytesIO()
        img.save(f, "png")
        data['code'] = 1
        data['data'] = u"data:image/png;base64," + base64.b64encode(f.getvalue()).decode('ascii')
        data['status'] = 1
        data['msg'] = '获取成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 查询账号是否存在
def get_user(username):
    sql = "select * FROM san_administrator WHERE username = '%s'" % username
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 生成储存的用户密码
def add_storage_pass(username, password):
    md_str = public_util.md5(str(username)) + public_util.md5(password)
    s_str = ''.join(sorted(public_util.md5(''.join(sorted(md_str)))))
    return s_str


# 获取删除信息
def get_uid(uid):
    sql = "select * FROM san_administrator WHERE id = '%s'" % uid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res
