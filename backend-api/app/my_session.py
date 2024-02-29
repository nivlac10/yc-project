# -*- coding: UTF-8 -*-
"""
Created on 2016年7月2日

@author: steve bi
自定义的Session类:
uid是服务器通过对于正常登录的登录用户的用户名和服务器端的KEY混合后的散列字符串
st为Session存活的起始时间
n为Session对应的用户名
LIFE_TIME为Session的有效存活时间,当用户发起request到服务器之后服务器端需要重新设置存活起始时间
COMMON_KEY为计算用户的uid的key
"""
import codecs

from app import redis
import time
import hashlib

# Session的生命周期
LIFE_TIME = 24 * 60 * 60
# 用于产生uid和数据库中的密码的公用KEY
COMMON_KEY = 'iwqhioj1oi398r32u98twefjh9834ugjanfo'


class MySession:
    """
    自定义的Session类
    类中的方法使用静态方法
    用户的Session保存在Redis中,需要添加对redis的依赖
    """

    def __init__(self):
        pass

    @staticmethod
    def exists(uid):
        """
        判断某个uid是否存在
        :param uid: 用来标示session的编码
        :return: 如果存在返回Ture, 不存在返回False
        """
        if redis.exists(uid):
            return True
        return False

    @staticmethod
    def add_param(uid, data):
        """
        根据uid添加参数
        :param uid: 用来标示session的编码
        :param data: 需要添加的数据
        :return: 添加结果
        """
        if MySession.exists(uid):
            for p in data:
                redis.hset(uid, p['key'], p['value'])
            return True
        return False

    @staticmethod
    def get_param(uid, key):
        """
        根据uid获取参数
        :param uid: 用来标示session的编码
        :param key: 需要获取的参数key
        :return: 参数
        """
        if MySession.exists(uid):
            return redis.hget(uid, key)
        return None

    @staticmethod
    def reactive(uid):
        """
        当用户处于活动状态的时候,更新session的存活起始时间
        :param uid: 用来标示session的用户编码
        :return: None
        """
        if MySession.exists(uid):
            redis.expire(uid, LIFE_TIME)
            return True
        return False

    @staticmethod
    def create_session(name):
        """
        在用户成功登录之后保存用户的session
        :param name: 用户名
        :return: 用来标示session的用户编码
        """
        key = name + COMMON_KEY + str(time.time())
        m1 = hashlib.md5()
        key = codecs.encode(key)
        m1.update(key)
        uid = m1.hexdigest().upper()
        redis.hset(uid, 'n', name)
        redis.expire(uid, LIFE_TIME)
        return uid

    @staticmethod
    def clear_session(uid):
        """
        清除某个session
        :param uid: 用来标示session的用户编码
        :return: None
        """
        if MySession.exists(uid):
            redis.delete(uid)
        return

    @staticmethod
    def get_name(uid):
        """
        获取某个Session的用户名
        :param uid: 用来标示session的用户编码
        :return: 如果存在则返回用户名,如果不存在则返回None
        """
        if MySession.exists(uid):
            return redis.hget(uid, 'n')
        else:
            return None

