#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-03-03
import importlib, random
import json

from app.admin import admin
from flask import request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import RKEY, redis, public_util, util_update_redis
import pyotp
import qrcode, base64
from io import BytesIO
import sys, os, time



importlib.reload(sys)



# 获取渠道列表数据
@admin.route('/admin/agent_list_post', methods=['post'])
@login_required
def agent_list_post():
    data = dict()
    data['data'] = []
    data['code'] = 0
    data['count'] = 0
    try:
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql = "select a.*, b.username pro_name, c.username service_name from san_agent a left join san_proxy_list b " \
              "on b.aid = a.aid left join san_service c on c.service_id = a.sid limit %d, %d" % (offset, limit)
        sql2 = "select count(*) con from san_agent "
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['pro_name'] = d['pro_name'] if d['pro_name'] else '未分配'
                d['service_name'] = d['service_name'] if d['service_name'] else '未分配'
                d['add_time'] = str(d['add_time'])
                d['verify_str'] = '是' if d['verify_flag'] == 1 else '否'
                d['is_apk_str'] = '是' if d['is_apk'] == 1 else '否'
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)

# 获取渠道列表数据
@admin.route('/admin/simple_agent_list_post', methods=['post'])
@login_required
def simple_agent_list_post():
    data = dict()
    data['data'] = []
    data['code'] = 0
    data['count'] = 0
    try:
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)
        sql = "select cid,username from san_agent limit %d, %d" % (offset, limit)
        sql2 = "select count(*) con from san_agent "
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            data['data'] = res
            data['count'] = cont['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)




# 新增渠道处理
@admin.route('/admin/add_agent_post', methods=['post'])
@login_required
def add_agent_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        username = request.values.get('username', '').strip()
        verify_flag = request.values.get('verify_flag')
        aid = request.values.get('aid')
        is_apk = request.values.get('is_apk')
        fb_access_token = request.values.get('fb_access_token')
        fb_pixel_id = request.values.get('fb_pixel_id')
        re_ratio = request.values.get('re_ratio')
        # install_event = request.values.get('install_event', '')
        # register_event = request.values.get('register_event', '')
        # recharge_event = request.values.get('recharge_event', '')
        # pay_event = request.values.get('pay_event', '')
        if username == '':
            data['msg'] = '渠道名称不能为空'
            return jsonify(data)
        con = get_agent_name(username)
        if con:
            data['msg'] = '渠道名称已存在'
            return jsonify(data)
        proxy = get_proxy_detail(aid)
        if proxy is None:
            data['msg'] = '代理不存在'
            return jsonify(data)
        if proxy['status'] != 1:
            data['msg'] = '代理已禁用'
            return jsonify(data)
        user_key = pyotp.random_base32(32)
        p_str = add_storage_pass(str(username), '123456')
        sql = "insert into san_agent(username, verify_flag, user_key, password, aid,is_apk,fb_access_token,fb_pixel_id," \
              "re_ratio, add_time) values ('%s', '%s','%s', '%s', '%s','%s','%s','%s','%s', now())" \
              % (username, verify_flag, user_key, p_str, aid, is_apk, fb_access_token, fb_pixel_id, re_ratio)
        mysql = Mysql()
        res = mysql.insertOne(sql, None)
        mysql.dispose()
        if res > 0:
            util_update_redis.add_channel_conf()
            data['code'] = 1
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)




# 更新渠道信息
@admin.route('/admin/update_agent_post', methods=['post'])
@login_required
def update_agent_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        cid = request.values.get('cid')
        username = request.values.get('username')
        verify_flag = request.values.get('verify_flag')
        report_conf = request.values.get('report_conf')
        host = request.values.get('host')
        rate = request.values.get('rate')
        aid = request.values.get('aid')
        is_apk = request.values.get('is_apk')
        install_event = request.values.get('install_event', '')
        open_event = request.values.get('open_event', '')
        register_event = request.values.get('register_event', '')
        recharge_event = request.values.get('recharge_event', '')
        first_recharge_event = request.values.get('first_recharge_event', '')
        fb_access_token = request.values.get('fb_access_token')
        fb_pixel_id = request.values.get('fb_pixel_id')
        re_ratio = request.values.get('re_ratio')
        con = get_agent_info(cid)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        sql = "update san_agent set username = %s, verify_flag = %s, report_conf = %s, host = %s, " \
              "rate = %s, aid = %s, install_event = %s, open_event = %s, register_event = %s, " \
              "recharge_event = %s, first_recharge_event = %s,is_apk=%s,fb_access_token=%s,fb_pixel_id=%s,re_ratio=%s" \
              " where cid = %s"
        mysql = Mysql()
        res = mysql.update(sql, [username, verify_flag, report_conf, host, rate, aid, install_event, open_event,
                                 register_event,
                                 recharge_event, first_recharge_event, is_apk, fb_access_token, fb_pixel_id, re_ratio,
                                 cid])
        mysql.dispose()
        if res >= 0:
            util_update_redis.add_channel_conf()
            data['msg'] = '操作成功'
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 更新渠道信息状态
@admin.route('/admin/update_agent_statue_post', methods=['post'])
@login_required
def update_agent_statue_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        cid = request.values.get('cid')
        status = request.values.get('status')
        if status not in ['0', '1']:
            data['msg'] = '参数错误'
            return jsonify(data)
        con = get_agent_info(cid)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        sql = "update san_agent set status = '%s' where cid = '%s'" % (status, cid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res > 0:
            util_update_redis.add_channel_conf()
            data['status'] = 1
            data['code'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除渠道
@admin.route('/admin/delete_agent_post', methods=['post'])
@login_required
def delete_agent_post():
    data = dict()
    data['code'] = 0
    data['msg'] = '操作失败'
    data['status'] = 0
    try:
        cid = request.values.get('cid')
        con = get_agent_info(cid)
        if con is None:
            data['msg'] = '参数错误'
            return jsonify(data)
        sql = "delete from san_agent where cid = '%s'" % cid
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res > 0:
            redis.hdel(RKEY.SAN_GAME_NEW_CHANNEL_CONF, cid)
            data['code'] = 1
            data['msg'] = '操作成功'
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 获取渠道二维码
@admin.route('/admin/agent_code_img', methods=['post'])
@login_required
def agent_code_img():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '获取失败'
    data['data'] = ''
    try:
        cid = request.values.get('cid')
        user = get_agent_info(cid)
        if user is None:
            data['msg'] = '渠道不存在'
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


# 测试回传
@admin.route('/admin/test_backhaul_post', methods=['post'])
@login_required
def test_backhaul_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        cid = request.values.get('cid')
        util_update_redis.fb_usgin_event_func(cid)
        data['code'] = 1
        data['status'] = 1
        data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)




def raddomPhone(num):
    number = ''
    for d in range(num):
        random.randint(0, 9)
        number += str(random.randint(0, 9))
    return number


def getRandomString(randomlength=4):
    digits = "0123456789"
    ascii_letters = "abcdefghijklmnopqrstuvwxyz"
    str_list = [random.choice(digits + ascii_letters) for i in range(randomlength)]
    random_str = "".join(str_list)
    return random_str


# 获取代理详情
def get_proxy_detail(aid):
    sql = "select * from san_proxy_list where aid = '%s'" % aid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 获取所有代理
def get_proxy_all():
    sql = "select aid, username from san_proxy_list where status = 1 order by aid desc"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


# 获取所有客服
def get_service_all():
    sql = "select service_id, username from san_service order by service_id desc"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


# 生成储存的用户密码
def add_storage_pass(username, password):
    md_str = public_util.md5(str(username)) + public_util.md5(password)
    s_str = ''.join(sorted(public_util.md5(''.join(sorted(md_str)))))
    return s_str


# 获取支付详情
def get_pay_info(pay_id):
    sql = "select * from san_pay_list where pay_id = '%s' and status = 1" % pay_id
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 获取所有支付
def get_pay_list():
    sql = "select pay_id, pay_name from san_pay_list where status = 1"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


# 保存游戏图片到本地
def game_img_file(game_img):
    img_str = ''
    try:
        if game_img:
            file_name = game_img.filename
            new_path = '/home/file/icon/'
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            apk_list = file_name.split('.')
            img_name = str(int(time.time() * 1000)) + '.' + apk_list[len(apk_list) - 1]
            img_local_path = os.path.join(new_path, img_name)
            game_img.save(img_local_path)
            img_str = img_name
    except Exception as e:
        print(e)
    return img_str


# 查询游戏是否存在
def get_game_info(game_id):
    sql = "select * from san_game_list where game_id = '%s'" % game_id
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 获取所有游戏
def get_game_all():
    sql = "select game_id, game_name from san_game_list"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res


# 获取渠道详情
def get_agent_info(cid):
    sql = "select * from san_agent where cid = '%s'" % cid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res


# 查询渠道名称是否已存在
def get_agent_name(username):
    sql = "select * from san_agent where username = '%s'" % username
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res
