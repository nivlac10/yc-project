# -*- coding: utf-8 - *-
# @Time: 2023/2/13
# @Author:Jack c
import json
import operator
import random
import time

from SqlConntion.MySqlConn import Mysql
from SqlConntion.RedisDB import Redis
from app import  RKEY, util


# 获取所有配置
from app.admin.agent import raddomPhone
from app.public_util import getRandomString


def get_conf_all():
    sql = "select * from san_conf"
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    redis = Redis()
    if res:
        key_list = res.keys()
        if len(key_list) > 0:
            for d in key_list:
                redis.hset(RKEY.SAN_GAME_ALL_CONF, str(d), str(res[d]))
    redis.close()
    return res


# 获取后台配置
def get_single_conf(key_name, value=''):
    redis = Redis()
    if isinstance(value, int):
        return int(redis.hget(RKEY.SAN_GAME_ALL_CONF, key_name) or value)
    elif isinstance(value, str):
        return redis.hget(RKEY.SAN_GAME_ALL_CONF, key_name) or value
    elif isinstance(value, float):
        return float(redis.hget(RKEY.SAN_GAME_ALL_CONF, key_name) or value)
    elif isinstance(value, list):
        d = redis.hget(RKEY.SAN_GAME_ALL_CONF, key_name)
        if d is None:
            return value
        return json.loads(d)
    elif isinstance(value, dict):
        d = redis.hget(RKEY.SAN_GAME_ALL_CONF, key_name)
        if d is None:
            return value
        return json.loads(d)
    data = redis.hget(RKEY.SAN_GAME_ALL_CONF, key_name) or ""
    redis.close()
    return data


# 生成提现配置
def add_game_withdraw_conf():
    sql = "select * from san_pay_list where with_flag = 1 order by sort_index desc"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    print(res)
    mysql.dispose()
    redis = Redis()
    if res:
        resource_host = redis.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
        for d in res:
            d['cover'] = resource_host + d['cover'] if d['cover'] else ''
    res = list(res) if res else []
    redis.set(RKEY.SAN_GAME_NEW_WITHDRAW_CONF, json.dumps(res))
    redis.close()


# 邀请任务
def san_user_invite_task():
    sql = "select * from san_user_invite_task  order by task_id"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    if res:
        redis = Redis()
        redis.set(RKEY.SAN_USER_INVITE_TASK, json.dumps(res))
        redis.close()

# 生成渠道配置
def add_channel_conf():
    sql = "select * from san_agent"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    if res:
        redis = Redis()
        for d in res:
            del d['add_time']
            redis.hset(RKEY.SAN_GAME_NEW_CHANNEL_CONF, str(d['cid']), json.dumps(d))
        redis.set("san_agent", json.dumps(res))
        redis.close()

# 更新活动列表
def add_activity_data():
    try:
        sql = "select aid,title,info,icon_url,img_url,type,url,button_name from " \
              "san_activity_list where status = 1 order by sort_index desc,aid asc"
        mysql = Mysql()
        res = mysql.getAll(sql, None) or []
        mysql.dispose()
        redis = Redis()
        if res:
            resource_host = redis.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
            for item in res:
                item['icon_url'] = resource_host + item['icon_url']
                item['img_url'] = resource_host + item['img_url']
        redis.set(RKEY.SAN_GAME_NEW_ACTIVITY_CONF, json.dumps(res))
        redis.close()
    except Exception as e:
        print(e)


# 更新redis游戏类型
def add_game_type_data():
    try:
        sql = "select id,type_name,type,icon,sort_index,jump_route,rakeback_open from " \
              "san_game_type_list where status = 1 order by sort_index desc"
        sql2 = "select * from san_game_type_list "
        mysql = Mysql()
        res = mysql.getAll(sql, None) or []
        res2 = mysql.getAll(sql2, None) or []
        mysql.dispose()
        redis = Redis()
        if res:
            resource_host = redis.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
            for item in res:
                item['icon'] = resource_host + item['icon']
        redis.set(RKEY.SAN_GAME_TYPE_CONF, json.dumps(res))
        redis.set("task_game_type_list", json.dumps(res2))
        redis.close()
    except Exception as e:
        print(e)


# 获取公告数据
def add_notice_data():
    try:
        sql = "select id, title, info, url,type,button_name,add_time from" \
              " san_notice_list where status = 1 order by sort_index desc, id asc"
        mysql = Mysql()
        res = mysql.getAll(sql, None) or []
        mysql.dispose()
        redis = Redis()
        if res:
            for item in res:
                item['add_time']=str(item['add_time'])
            redis.set(RKEY.SAN_GAME_NEW_NOTICE_CONF, json.dumps(res))
        redis.close()
    except Exception as e:
        print(e)


# 更新平台功能弹窗列表
def add_plate_alert_data():
    try:
        sql = "select id,img_url,type,url,close_type,user_type from " \
              "san_plate_alert_list where status = 1 order by sort_index desc,id asc"
        mysql = Mysql()
        res = mysql.getAll(sql, None) or []
        mysql.dispose()
        redis = Redis()
        if res:
            resource_host = redis.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
            for item in res:
                item['img_url'] = resource_host + item['img_url']
        redis.set(RKEY.san_plate_alert_list, json.dumps(res))
        redis.close()
    except Exception as e:
        print(e)

# 更新客服
def set_reds_san_service_list():
    try:
        sql = "select service_name,service_ab,service_header_img,url,service_icon" \
              " from san_service_list where status= 1 order by sort_index desc,id asc "
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        mysql.dispose()
        redis = Redis()
        if res:
            resource_host = redis.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
            for item in res:
                item['service_icon'] = resource_host + item['service_icon']
                item['service_header_img'] = resource_host + item['service_header_img']
            redis.set(RKEY.SAN_GAME_SERVICE_LIST, json.dumps(res))
        redis.close()
    except Exception as e:
        print(e)


# 更新佣金简介列表
def set_reds_san_commission_desc_list():
    try:
        sql = "select id,aid,title,info from san_commission_desc_list where status = 1 " \
              "order by sort_index desc, id asc"
        mysql = Mysql()
        res = mysql.getAll(sql, None) or []
        mysql.dispose()
        redis = Redis()
        redis.set(RKEY.SAN_COMMISSION_DESC_LIST, json.dumps(res))
        redis.close()
    except Exception as e:
        print(e)


# 更新redis轮播图列表
def set_reds_san_banner_list():
    try:
        sql = "select bid,img_url,type,url from san_banner_list " \
              "where status = 1 order by sort_index desc,bid asc"
        mysql = Mysql()
        res = mysql.getAll(sql, None) or []
        mysql.dispose()
        redis = Redis()
        if res:
            resource_host = redis.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
            for item in res:
                item['img_url'] = resource_host + item['img_url']
        redis.set(RKEY.SAN_GAME_BANNER_LIST, json.dumps(res))
        redis.close()
    except Exception as e:
        print(e)


#
# 获取游戏列表
def set_redis_san_external_game_list():
    sql = "select a.gid,a.game_id,a.game_name,a.icon,a.game_type,a.screen,a.is_hot,a.is_top, b.game_name f_name" \
          ", b.status, a.sort_index,a.rtp,a.is_demo  from " \
          "san_external_game_list a left join san_game_list b on a.game_id = b.game_id" \
          "  where b.status != 0 and a.status = 1  order by  a.is_top desc,  a.is_hot desc, a.sort_index desc "
    mysql = Mysql()
    res = mysql.getAll(sql, None) or []
    mysql.dispose()
    redis = Redis()
    if res:
        resource_host = redis.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
        for item in res:
            if operator.contains(item['icon'], "game_icon"):
                item['icon'] = resource_host + item['icon']
    redis.set(RKEY.SAN_EXTERNAL_GAME_LIST, json.dumps(res))
    redis.close()


# 获取热门列表
def set_redis_san_hot_game_list():
    sql = "select gid,game_id,game_name,icon,game_type,screen from " \
          "san_external_game_list where status = 1 and is_hot=1 " \
          " order by sort_index,gid asc limit 0,12 "
    mysql = Mysql()
    res = mysql.getAll(sql, None) or []
    mysql.dispose()
    redis = Redis()
    if res:
        resource_host = redis.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
        for item in res:
            item['icon'] = resource_host + item['icon']
    redis.set(RKEY.SAN_GAME_HOT_GAME_LIST, json.dumps(res))
    redis.close()


# 更新redi中san_game_list数据
def set_redis_san_game_list():
    sql = "select game_id,game_name,cover,game_type, status from san_game_list where status != 0 " \
          "order by sort_index desc,game_id asc "
    mysql = Mysql()
    res = mysql.getAll(sql, None) or []
    mysql.dispose()
    redis = Redis()
    if res:
        resource_host = redis.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST) or ''
        for item in res:
            item['cover'] = item['cover'] if item['cover'] != "" else "1672905693683.png"
            item['cover'] = resource_host + item['cover']
    redis.set(RKEY.SAN_GAME_FACTORY_LIST, json.dumps(res))
    redis.close()

# 游戏版本升级
def game_data_version_rise():
    print("游戏列表版本升级")
    try:
        redis = Redis()
        if redis.get(RKEY.GAME_DATA_VERSION) is None:
            redis.set(RKEY.GAME_DATA_VERSION, '1')
            return '1'
        game_data_version = int(redis.get(RKEY.GAME_DATA_VERSION))
        res = redis.set(RKEY.GAME_DATA_VERSION, str(game_data_version + 1))
        redis.close()
        set_redis_san_game_list()
        set_redis_san_external_game_list()
        set_redis_san_hot_game_list()
        add_game_type_data()
        update_game_time_conf()
        game_task_list_conf()
        return res
    except Exception as e:
        print(e)


# vip存入redis
def save_vip_lv_to_redis():
    sql = "select * from san_vip_lv_list order by vip_id asc"
    sql2 = "select * from san_vip_low_vip_list order by vip_lv asc, id asc"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    res2 = mysql.getAll(sql2, None)
    mysql.dispose()
    redis = Redis()
    if res and res2:
        for d in res:
            d['vip_low_lv'] = []
            for i in res2:
                if str(d['vip_lv']) == str(i['vip_lv']):
                    d['vip_low_lv'].append(i)
        redis.set(RKEY.SAN_GAME_VIP_LV_LIST, json.dumps(res))
        redis.close()
        save_vip_low_lv_to_redis()


# vip升级条件与奖励存入redis
def save_vip_low_lv_to_redis():
    sql2 = "select * from san_vip_low_vip_list order by vip_lv asc, id asc"
    mysql = Mysql()
    res = mysql.getAll(sql2, None)
    mysql.dispose()
    if res:
        redis = Redis()
        redis.set("san_vip_low_vip_list", json.dumps(res))
        redis.close()


# 设置充值获得配置
def set_recharge_activity_conf():
    sql = "select * from san_recharge_activity_list where status = 1"
    mysql = Mysql()
    res = mysql.getAll(sql, None) or []
    mysql.dispose()
    conf = []
    if res:
        for d in res:
            d['s_time'] = str(d['start_time'])
            d['e_time'] = str(d['over_time'])
            d['start_time'] = util.days_int(str(d['start_time'])) if str(d['start_time']) else 0
            d['over_time'] = util.days_int(str(d['over_time'])) if str(d['over_time']) else 0
            d['add_time'] = str(d['add_time'])

            activity_type = d['recharge_activity_type']
            d['step'] = [] if activity_type in [0, 2] else set_recharge_scope(d['recharge_activity_id'])
            d['scope'] = set_recharge_scope(d['recharge_activity_id']) if activity_type in [0, 2] else []
            conf.append(d)
    redis = Redis()
    redis.set(RKEY.SAN_GAME_PAY_ACTION_CONF, json.dumps(conf))
    redis.set(RKEY.SAN_GAME_PAY_ACTION_LIST_CONF, json.dumps(res))
    redis.close()

#  充值活动阶梯更新
def set_recharge_ladder_activity_list():
    mysql = Mysql()
    sql = "select * from san_recharge_activity_ladder_list"
    res = mysql.getAll(sql, None) or []
    mysql.dispose()

    redis = Redis()
    redis.set(RKEY.SAN_GAME_PAY_ACTION_LADDER_LIST_CONF, json.dumps(res))
    redis.close()

def get_pay_ladder_action_list():
    redis = Redis()
    recharge_activity_list = []
    recharge_activity_data = redis.get(RKEY.SAN_GAME_PAY_ACTION_LADDER_LIST_CONF)
    if recharge_activity_data:
        recharge_activity_list = json.loads(recharge_activity_data)
    redis.close()
    return recharge_activity_list


def set_recharge_scope(activity_id):
    list_data = get_pay_ladder_action_list()
    list_action_list = []
    if len(list_data) > 0:
        for d in list_data:
            if d['recharge_activity_id'] == activity_id:
                list_action_list.append(d)
    return list_action_list


# 游戏配置
def update_game_time_conf():
    sql = "select gid, game_id,game_name, game_type, my_game from san_external_game_list "
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    if res:
        redis = Redis()
        for d in res:
            redis.hset('slot_pub_update_game_time_conf', str(d['gid']), json.dumps(d))
        redis.close()


# 任务专用游戏列表
def game_task_list_conf():
    sql = "select * from san_external_game_list"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    if res:

        redis = Redis()
        redis.set("game_task_list", json.dumps(res))
        redis.close()


# 充值活动简介
def san_recharge_activity_slogan():
    sql = "select id,info,sort_index from san_recharge_activity_slogan where status = 1 order by sort_index desc"
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    if res:
        redis = Redis()
        redis.set("san_recharge_activity_slogan", json.dumps(res))
        redis.close()


# 更新至redis
def set_gift_code():
    now_int = int(time.time())
    sql = "select * from san_give_code where status = 1 and end_time > %s " % now_int
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    if res:
        redis = Redis()
        redis.delete('san_give_code')
        for d in res:
            d['add_time'] = str(d['add_time'])
            redis.hset('san_give_code', str(d['code']), json.dumps(d))
        redis.close()
    # return res


# 更新至redis
def fb_usgin_event_func(cid):
    for d in range(2):
        type = d + 1
        money = 0
        if type == 2:
            money = random.randint(20, 1000)
        r_key = "fb_api_using_event_list"
        email_lang = random.randint(5, 20)
        maps = dict()
        maps['email'] = getRandomString(email_lang) + "@gmail.com"
        maps['phone'] = raddomPhone(11)  # 随机11位数字
        maps['cid'] = cid
        maps['type'] = str(type)
        maps['money'] = money
        maps['time'] = int(time.time())
        redis = Redis()
        redis.rpush(r_key, json.dumps(maps))
        redis.close()

    # return res

if __name__ == '__main__':
    update_game_time_conf()
    game_task_list_conf()