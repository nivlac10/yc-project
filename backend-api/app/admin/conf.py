#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-04-05
import datetime
import importlib
import json
import time,random,requests

from SqlConntion.RedisDB import Redis
from . import admin
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import util_update_redis, public_util, constant, redis, RKEY
import sys

importlib.reload(sys)

PATH = 'conf/'

# 系统配置
@admin.route('/admin/system_conf',methods=['post'])
@login_required
def system_conf():
    data = dict()
    data['code'] = 1
    data['conf'] = get_conf()
    data['sms_conf'] = SMS_CONF
    return jsonify(data)


# 查询系统配置
@admin.route('/admin/system_conf_list_post', methods=['post'])
@login_required
def system_conf_list_post():
    data =dict()
    data['code'] = 0
    sql = "select * from san_conf"
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    redis_R = Redis()
    if res:
        url_host = redis_R.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
        redis_R.close()
        res['platform_min_icon_url'] = url_host + res['platform_min_icon_url']
        res['platform_title_icon_url'] = url_host + res['platform_title_icon_url']
        res['code_template'] = json.loads(res['code_template']) if res['code_template'] else ''
        data['data'] = res
    data['code'] = 1
    return jsonify(data)



# 更新系统配置
@admin.route('/admin/system_conf_post', methods=['post'])
@login_required
def system_conf_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        key_list = ['tmp_user_money', 'bind_phone_money', 'facebook_user_money', 'user_ip_max_num', 'gift_code_rate',
                    'min_recharge_money', 'max_recharge_money','min_withdraw_commission', 'min_withdraw_money',
                    'max_withdraw_money', 'default_money', 'pay_money_list', 'account_max_num', 'withdraw_poundage',
                    'auto_withdraw_flag', 'resource_host', 'code_template', 'sms_conf', 'copy_link', 'share_title',
                    'share_detail', 'success_email','share_contact_email', 'auto_min_withdraw_money',
                    'auto_min_withdraw_ip_num', 'auto_min_withdraw_sb_num', 'first_charge_give_rate',
                    'day_charge_give_rate', 'currency', 'is_maintain', 'maintain_title', 'maintain_remarks', 'ios_url',
                    'android_url', 'qrcode_url', 'service_terms_url', 'tg_channel_url', 'platform_title', 'platform_livechat_id',
                    'platform_path', 'platform_url', 'platform_telegram_chat_id', 'platform_telegram_bot_token']

        platform_min_icon = request.files.get('platform_min_icon_url')
        platform_title_icon = request.files.get('platform_title_icon_url')
        platform_min_icon = public_util.Get_image_url(platform_min_icon, PATH)
        platform_title_icon = public_util.Get_image_url(platform_title_icon, PATH)
        maps = dict()
        for d in key_list:
            if d == 'platform_title_icon_url' or d == 'platform_min_icon_url':
                maps[d] = request.files.get(d)
                maps[d] = public_util.Get_image_url(maps[d], PATH)
            else:
                maps[d] = request.values.get(d)
        sql = "update san_conf set "
        params = []
        for k in key_list:
            sql += k + " = %s,"
            params.append(maps[k])

        if platform_min_icon:
            sql += " platform_min_icon_url = %s,"
            params.append(platform_min_icon)
        if platform_title_icon:
            sql += " platform_title_icon_url = %s,"
            params.append(platform_title_icon)
        sql = sql[:-1]
        mysql = Mysql()
        res = mysql.update(sql, params)
        mysql.dispose()
        if res >= 0:
            util_update_redis.get_conf_all()
            data['msg'] = '操作成功'
            data['status'] = 1
            data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 更新Redis
@admin.route('/admin/update_redis_conf_post', methods=['post'])
@login_required
def update_redis_conf_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        util_update_redis.get_conf_all()
        util_update_redis.add_game_withdraw_conf()
        util_update_redis.add_activity_data()
        util_update_redis.add_channel_conf()
        util_update_redis.add_notice_data()
        util_update_redis.set_reds_san_service_list()
        util_update_redis.set_reds_san_commission_desc_list()
        util_update_redis.set_reds_san_banner_list()
        util_update_redis.set_redis_san_external_game_list()
        util_update_redis.set_redis_san_game_list()
        util_update_redis.set_redis_san_hot_game_list()
        util_update_redis.save_vip_lv_to_redis()
        util_update_redis.san_recharge_activity_slogan()
        util_update_redis.game_data_version_rise()
        util_update_redis.game_task_list_conf()
        util_update_redis.update_game_time_conf()
        util_update_redis.set_recharge_ladder_activity_list()
        util_update_redis.get_pay_ladder_action_list()
        util_update_redis.set_recharge_activity_conf()
        util_update_redis.san_user_invite_task()
        data['code'] = 1
        data['status'] = 1
        data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 搜索按钮
@admin.route('/admin/search_btn', methods=['post'])
@login_required
def search_btn():
    data = dict()
    data['start_day'] = ''
    data['end_day'] = ''
    data['code'] = 0
    start_time = request.values.get('start_time')
    end_time = request.values.get('end_time')
    datetype = request.values.get('datetype')
    dateset = request.values.get('dateset')
    stime, etime = return_time(start_time, end_time, datetype, dateset)
    data['start_day'] = stime
    data['end_day'] = etime
    data['code'] = 1
    return jsonify(data)




# 获取所有配置
def get_conf():
    sql = "select * from san_conf"
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    if res:
        res['code_template'] = json.loads(res['code_template']) if res['code_template'] else ''
        res['recharge_conf_arr'] = json.loads(res['recharge_conf_arr']) if res['recharge_conf_arr'] else ''
        res['withdraw_conf_arr'] = json.loads(res['withdraw_conf_arr']) if res['withdraw_conf_arr'] else ''
    return res



# 创蓝云智
def chuan_lang_yun_zhi(mobile):
    num = random.randint(1000, 9999)
    redis_R = Redis()
    code_template = redis_R.hget(RKEY.SAN_GAME_ALL_CONF, 'code_template') or ''
    redis_R.close()
    if code_template:
        code_template = json.loads(code_template)
    else:
        return False, num
    sms_code_template = code_template['lcyz']
    data = dict()
    data['account'] = constant.CHUANG_LANG_YUN_ZHI_ACCOUNT
    data['password'] = constant.CHUANG_LANG_YUN_ZHI_PASSWORD
    data['msg'] = sms_code_template.replace('<code>', str(num))
    data['mobile'] = str(mobile)
    url = 'http://intapi.253.com/send/json'
    res = requests.post(url, data=json.dumps(data), verify=False, timeout=10)
    content = json.loads(res.text)
    flag = True if str(content['code']) == "0" else False
    return flag, num


# 短信通道配置
SMS_CONF = {
    'lcyz': {
        'name': u'创蓝云智',
        'func': str(chuan_lang_yun_zhi)
    },
}




# 返回查询时间
def return_time(start_time, end_time, datetype, dateset):
    day = time.strftime("%Y-%m-%d")
    if str(dateset) == '0' and str(datetype) == '0':
        return start_time, end_time
    if str(dateset) != '0':
        if dateset == '1':
            return day, day
        if dateset == '2':
            return public_util.get_yesterday(), public_util.get_yesterday()
        if dateset == '3':
            return public_util.get_this_week_start(), day
        if dateset == '4':
            return public_util.get_last_week_start(), public_util.get_last_week_end()
        if dateset == '5':
            return public_util.get_this_month_start().strftime("%Y-%m-%d"), day
        if dateset == '6':
            return public_util.get_last_month_start(), public_util.get_last_month_end().strftime("%Y-%m-%d")
        if dateset == '7':
            this_year_start = datetime.datetime(datetime.datetime.now().year, 1, 1)
            this_year_end = datetime.datetime(datetime.datetime.now().year + 1, 1, 1) - datetime.timedelta(days=1)
            return this_year_start.strftime("%Y-%m-%d"), this_year_end.strftime("%Y-%m-%d")
        if dateset == '8':
            return '', ''
        if dateset == '9':
            last_year_end = datetime.datetime(datetime.datetime.now().year, 1, 1) - datetime.timedelta(days=1)
            last_year_start = datetime.datetime(last_year_end.year, 1, 1)
            return last_year_start.strftime("%Y-%m-%d"), last_year_end.strftime("%Y-%m-%d")
        if dateset == '10':
            end_day = datetime.datetime.now() - datetime.timedelta(days=1)
            start_day = datetime.datetime.now() - datetime.timedelta(days=7)
            return start_day.strftime("%Y-%m-%d"), end_day.strftime("%Y-%m-%d")
        if dateset == '11':
            end_day = datetime.datetime.now() - datetime.timedelta(days=1)
            start_day = datetime.datetime.now() - datetime.timedelta(days=30)
            return start_day.strftime("%Y-%m-%d"), end_day.strftime("%Y-%m-%d")
    if str(datetype) != '0':
        if start_time == '' or end_time == '':
            return day, day
        if str(datetype) == '+1':
            start_time_t = datetime.datetime.strptime(start_time, "%Y-%m-%d")
            end_time_t = datetime.datetime.strptime(end_time, "%Y-%m-%d")
            start_time_r = start_time_t + datetime.timedelta(days=1)
            end_time_r = end_time_t + datetime.timedelta(days=1)
            return start_time_r.strftime("%Y-%m-%d"), end_time_r.strftime("%Y-%m-%d")
        if str(datetype) == '-1':
            start_time_t = datetime.datetime.strptime(start_time, "%Y-%m-%d")
            end_time_t = datetime.datetime.strptime(end_time, "%Y-%m-%d")
            start_time_r = start_time_t - datetime.timedelta(days=1)
            end_time_r = end_time_t - datetime.timedelta(days=1)
            return start_time_r.strftime("%Y-%m-%d"), end_time_r.strftime("%Y-%m-%d")
    return day, day