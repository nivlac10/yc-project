from SqlConntion import ConnConfig
from . import admin
from flask import render_template, request, jsonify, make_response, abort, json
from SqlConntion.MySqlConn import Mysql
from app import public_util, util, constant
from app.util import login_required
from app.my_session import MySession
from ..constant import HOST_ARR
from app import redis
import sys, requests, string, random
import time, pyotp


# 获取数据库数据
@admin.route('/admin/get_p_conf', methods=['post'])
def get_p_conf():
    data = dict()
    data['code'] = 0
    data['data'] = []
    try:
        db_conf = constant.DBCONFIG
        for d in db_conf:
            maps = dict()
            maps['index'] = d
            maps['p_name'] = db_conf[d]['p_name']
            data['data'].append(maps)
        data['code'] = 1
    except Exception as e:
        print(e)
        data['status'] = 500
    return jsonify(data)


# 管理员登陆处理
@admin.route('/admin/login', methods=['post'])
def login():
    data = dict()
    data['code'] = 0
    data['msg'] = '登陆失败'
    data['data'] = dict()
    data['data']['token'] = ''
    data['data']['roles'] = []
    data['data']['username'] = ''
    # if True:
    try:
        username = request.values.get('username')
        password = request.values.get('password')
        code = request.values.get('code')
        # if request.host not in HOST_ARR:
        #     return abort(404)
        code = str(code).lower()
        user_key = 'user_login_error' + username
        user_flag = int(redis.get(user_key)) if redis.get(user_key) else 0
        constant.DBINDEX = 0
        res = get_user_info(username)
        if res is None:
            data['msg'] = '账号不存在'
            data['ip'] = add_login_code(public_util.get_current_ip())
            admin_login(username, u"账号不存在")
            return jsonify(data)
        if res['status'] != 1 and str(username) != "admin":
            data['msg'] = "账号已禁用"
            data['ip'] = add_login_code(public_util.get_current_ip())
            admin_login(username, u"账号已禁用")
            return jsonify(data)
        p_str = verify_pass(res['password'], code)
        if password != p_str:
            err_num = user_flag + 1
            redis.set(user_key, err_num, ex=600)
            data['code'] = 2
            data['ip'] = add_login_code(public_util.get_current_ip())
            data['msg'] = '密码错误'
            admin_login(username, u"密码错误")
            return jsonify(data)
        # if verify_otp_code(res['user_key'], code) is False:
        #     data['msg'] = '动态口令错误'
        #     return jsonify(data)
        user = MySession.create_session(str(res['id']))
        # user_info['uid']=user
        # user_info['admin_user']=username
        # user_info['admintype']=res['admintype']
        data['code'] = 1
        data['msg'] = '登录成功！'
        data['data']['token'] = user
        # data['data']['roles'].append(str(res['admintype']))
        # data['data']['username'] = res['username']
        # data['data']=user_info
        admin_login(username, u"登陆成功")
        update_login_time(username)
    except Exception as e:
        print(e)
        data['status'] = 500
    return jsonify(data)


# 获取管理员信息
@admin.route('/admin/get_info', methods=['post'])
@login_required
def get_info():
    data = dict()
    data['code'] = 0
    data['data'] = dict()
    data['data']['username'] = ''
    data['data']['roles'] = []
    token = request.headers.get('Authorization')
    admin_uid = redis.hget(token, 'n')
    # try:
    if True:
        sql = "select * from san_administrator where id = %s"
        constant.DBINDEX = 0
        print(constant.DBINDEX)
        mysql = Mysql()
        res = mysql.getOne(sql, [admin_uid])
        print(constant.DBINDEX)
        mysql.dispose()
        print("#################")
        print(res)
        if res:
            data['code'] = 1
            data['data']['username'] = res['username']
            data['data']['roles'].append(str(res['admintype']))
            print()
    # except Exception as e:
    #     print(e)
    return jsonify(data)


# 退出登录
@admin.route('/admin/login_out',methods=['post'])
@login_required
def out():
    data = dict()
    data['code'] = 3
    uid = request.headers.get('uid')
    MySession.clear_session(uid)
    # login_str = "<script>location.href = '/admin/login.html';</script>"
    return jsonify(data)


# 修改管理密码处理
@admin.route('/admin/update_pass_post', methods=['post'])
@login_required
def update_pass_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    try:
        san_pass = request.values.get('new_pass')
        old_pass = request.values.get('old_pass')
        username = request.values.get('admin_user')
        if str(san_pass) == str(old_pass):
            data['status'] = 2
            data['msg'] = '新密码不能跟老密码一至'
            return jsonify(data)
        user = get_user_info(username)
        if user is None:
            data['status'] = 2
            data['msg'] = '用户不存在'
            return jsonify(data)
        # p_str = util.md5(str(old_pass)+login_key)
        # p_str = get_encryption(str(username), str(old_pass), user['user_key'])
        p_str = add_storage_pass(username, str(old_pass))
        if p_str != user['password']:
            data['status'] = 2
            data['msg'] = '旧密码不对'
            return jsonify(data)
        # san_str = util.md5(str(san_pass)+login_key)
        # san_str = get_encryption(str(username), str(san_pass), user['user_key'])

        san_str = add_storage_pass(username, str(san_pass))
        res = update_user_pass(san_str, user['id'])
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '修改成功'
            uid = request.headers.get('uid')
            MySession.clear_session(uid)

            return jsonify(data)
    except Exception as e:
        print (e)
    return util.to_json(data)


# 验证code
def verify_otp_code(sec, code):
    return pyotp.totp.TOTP(sec).verify(code)


# 生成储存的用户密码
def add_storage_pass(username, password):
    md_str = public_util.md5(str(username)) + public_util.md5(password)
    s_str = ''.join(sorted(public_util.md5(''.join(sorted(md_str)))))
    return s_str


# 验证登陆密码
def verify_pass(user_pass, code):
    u_str = public_util.md5(str(user_pass)) + public_util.md5(str(code))
    u_sort = sorted(u_str)
    m_str = sorted(public_util.md5(''.join(u_sort)))
    return ''.join(m_str)


# 生成验证码
def add_login_code(ip):
    code_list = random_code()
    code_str = ''.join(code_list).lower()
    redis.set(code_str, '1', ex=60)
    redis.set(ip, '1', ex=1)
    return code_list


# 随机生成4位code
def random_code():
    chars = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz123456789"
    num = 4
    return [random.choice(chars) for x in range(num)]


# 计算密码
def get_encryption(username, password, user_key):
    p_key = public_util.md5(str(password) + str(user_key))
    u_key = public_util.md5(str(username) + str(user_key))
    content = u_key + p_key
    res_list = sorted(content)
    res_str = public_util.md5(''.join(res_list))
    con_list = sorted(res_str)
    return ''.join(con_list)


# 修改密码
def update_user_pass(san_str, uid):
    sql = "update san_administrator SET password = %s WHERE id = %s"
    mysql = Mysql()
    res = mysql.update(sql, [san_str, uid])
    mysql.dispose()
    return res


# 获取用户信息
def get_user_info(username):
    sql = "select * FROM san_administrator WHERE username = %s"
    mysql = Mysql()
    res = mysql.getOne(sql, [username])
    mysql.dispose()
    return res

# 获取用户信息
def get_user_id(uid):
    sql = "select * FROM san_administrator WHERE id = %s"
    mysql = Mysql()
    res = mysql.getOne(sql, [uid])
    mysql.dispose()
    return res


# 管理员登陆记录
def admin_login(username, content):
    ip = public_util.get_current_ip()
    country = ''
    province = ''
    city = ''
    url = 'http://ip-api.com/json/%s?lang=zh-CN' % str(ip)
    # url = 'https://freeapi.ipip.net/' + str(ip)
    r = requests.get(url)
    if r.status_code == 200:
        res = json.loads(r.text)
        print(res)
        if res['status'] == 'success':
            country = res['country']
            province = res['regionName']
            city = res['city']
    addtime = time.strftime('%Y-%m-%d %H:%M:%S')
    type = 0
    sql = "insert into san_log_login (username, time, ip, type, status, country, province, city) VALUES (%s, %s, " \
          "%s, %s, %s, %s, %s, %s)"
    mysql = Mysql()
    res = mysql.insertOne(sql, [username, addtime, ip, type, content, country, province, city])
    mysql.dispose()
    return res


# 更新用户最后登陆时间
def update_login_time(username):
    sql = "update san_administrator SET loginnum = loginnum + 1, logintime = now() WHERE username = %s"
    mysql = Mysql()
    mysql.update(sql, [username])
    mysql.dispose()