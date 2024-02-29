import importlib
import json
import sys

from flask import  request, jsonify

from app import public_util,  redis,public_game_api
from app.util import login_required
from SqlConntion.MySqlConn import Mysql
from app.user import user

importlib.reload(sys)


# 用户代理等级升级
@user.route('/admin/up_user_lv', methods=['POST'])
@login_required
def up_user_lv():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '升级条件不达标！'
    try:
        uid = request.values.get('uid')
        user = get_user(uid)
        if user is None:
            data['msg'] = '用户不存在'
            return jsonify(data)
        up_lv_data = get_invite_bonus_data(int(user['share_lv']) + 1)
        if user['share_valid_number'] < up_lv_data['number']:
            return jsonify(data)
        sql = "update san_users set share_lv = share_lv + 1 where uid = '%s'"  % uid
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res:
            data['msg'] = '升级成功！！'
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 用户下线操作
@user.route('/admin/admin_user_exit_game', methods=['POST'])
@login_required
def admin_user_exit_game():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '下线失败'
    try:
        uid = request.values.get('uid')
        user = get_user(uid)
        if user is None:
            data['msg'] = '用户不存在'
            return jsonify(data)
        game = redis.hget('slot_pub_update_game_time_conf', str(user['cur_gameid']))
        if game is None:
            data['msg'] = '游戏不存在'
            return jsonify(data)
        game = json.loads(game)
        flag = public_game_api.wj_game_login_out(user, game['gid'], game)
        if flag:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '下线成功'
    except Exception as e:
        print(e)
    return jsonify(data)


#平台余额转出操作
@user.route('/admin/user_exit_money', methods=['POST'])
@login_required
def user_exit_money():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '转出失败！'
    try:
        uid = request.values.get('uid')
        user = get_user(uid)
        if user is None:
            data['msg'] = '用户不存在'
            return jsonify(data)
        flag = public_game_api.game_withdraw(user)
        if flag:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '转出成功！'
    except Exception as e:
        print(e)
    return jsonify(data)


# 发送邮件
@user.route('/admin/send_user_email_post', methods=['post'])
@login_required
def send_user_email_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        uid = request.values.get('uid')
        value = request.values.get('value')
        user = get_user(uid)
        if user is None:
            data['msg'] = '用户不存在'
            return jsonify(data)
        res = send_user_email(uid, value)
        if res > 0:
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '发送成功'
    except Exception as e:
        print(e)
    return jsonify(data)



# 获取用户信息
def get_user(uid):
    sql = "select * from san_users where uid = '%s'" % uid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 获取代理等级数据
def get_invite_bonus_data(lv):
    res = None
    sql = "select * from san_user_invite_recharge_bonus_list where lv = %s"
    mysql = Mysql()
    try:
        res = mysql.getOne(sql, [lv])
    except Exception as e:
        print(e)
    mysql.dispose()
    return res

# 提现失败，发送通知
def send_user_email(uid, content):
    title = 'System notification'
    sql = "insert into san_user_message(uid, title, content, add_time) values (%s, %s, %s, now())"
    mysql = Mysql()
    res = mysql.insertOne(sql, [uid, title, content])
    mysql.dispose()
    return res