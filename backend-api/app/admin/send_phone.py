#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022/4/19 15:53
# @Author : 78957
import importlib

from . import admin
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util
import sys

importlib.reload(sys)



# 获取短信数据
@admin.route('/admin/send_phone_list_post', methods=['post'])
@login_required
def send_phone_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql = "select * from san_user_phone_data "
        sql2 = "select count(*) con from san_user_phone_data "
        sql_list = []
        if stime:
            sql_list.append("  day >= '%s'" % stime)
        if etime:
            sql_list.append(" day <= '%s'" % etime)
        sql_str = public_util.data_list_to_str(sql_list)
        sql += sql_str
        sql2 += sql_str
        sql += " order by day desc limit %d, %d" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['day'] = str(d['day'])
                d['install_num'] = float(d['install_num']) if d['install_num'] else 0  # 安装数
                d['send_num'] = float(d['send_num']) if d['send_num'] else 0  # 点击获取验证码按钮-次数
                d['send_aaid'] = float(d['send_aaid']) if d['send_aaid'] else 0  # 点击获取验证码按钮-设备
                d['send_phone'] = float(d['send_phone']) if d['send_phone'] else 0  # 点击获取验证码按钮-手机号码
                d['send_aaid_ratio'] = round(d['send_aaid'] / d['install_num'] * 100, 2) if d[
                                                                                                'install_num'] > 0 else 0  # 点击按钮率-设备
                d['send_aaid_ratio'] = str(d['send_aaid_ratio']) + '%' if d['send_aaid_ratio'] != 0 else 0
                d['zc_aaid_success'] = float(d['zc_aaid_success']) if d['zc_aaid_success'] else 0  # 回填成功-设备
                d['zc_aaid_success_ratio'] = round(d['zc_aaid_success'] / d['send_aaid'] * 100, 2) if d[
                                                                                                          'send_aaid'] > 0 else 0  # 回填成功率-设备
                d['zc_aaid_success_ratio'] = str(d['zc_aaid_success_ratio']) + '%' if d[
                                                                                          'zc_aaid_success_ratio'] != 0 else 0
                d['zc_aaid_fail'] = float(d['zc_aaid_fail']) if d['zc_aaid_fail'] else 0  # 回填失败-设备
                d['send_phone_ratio'] = round(d['send_phone'] / d['install_num'] * 100, 2) if d[
                                                                                                  'install_num'] > 0 else 0  # 点击按钮率-手机号码
                d['send_phone_ratio'] = str(d['send_phone_ratio']) + '%' if d['send_phone_ratio'] != 0 else 0
                d['zc_phone_success'] = float(d['zc_phone_success']) if d['zc_phone_success'] else 0  # 回填成功-手机号码
                d['zc_phone_success_ratio'] = round(d['zc_phone_success'] / d['send_phone'] * 100, 2) if d[
                                                                                                             'send_phone'] > 0 else 0  # 回填成功率-手机号码
                d['zc_phone_success_ratio'] = str(d['zc_phone_success_ratio']) + '%' if d[
                                                                                            'zc_phone_success_ratio'] != 0 else 0
                d['zc_phone_fail'] = float(d['zc_phone_fail']) if d['zc_phone_fail'] else 0  # 回填失败-手机号码
                d['send_num_ratio'] = round(d['send_num'] / d['install_num'] * 100, 2) if d[
                                                                                              'install_num'] > 0 else 0  # 点击按钮率-次数
                d['send_num_ratio'] = str(d['send_num_ratio']) + '%' if d['send_num_ratio'] != 0 else 0
                d['zc_success_num'] = float(d['zc_success_num']) if d['zc_success_num'] else 0  # 回填成功-次数
                d['zc_success_num_ratio'] = round(d['zc_success_num'] / d['send_num'] * 100, 2) if d[
                                                                                                       'send_num'] > 0 else 0  # 回填成功率-次数
                d['zc_success_num_ratio'] = str(d['zc_success_num_ratio']) + '%' if d[
                                                                                        'zc_success_num_ratio'] != 0 else 0
                d['zc_fail_num'] = float(d['zc_fail_num']) if d['zc_fail_num'] else 0
            data['data'] = res
            data['count'] = int(cont['con'])
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
