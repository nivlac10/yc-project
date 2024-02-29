import sys

import importlib
from app.user import user
from flask import request,jsonify
from app import public_util
from app.util import login_required
from SqlConntion.MySqlConn import Mysql

importlib.reload(sys)


# 破产补贴列表
@user.route('/admin/user_loss_bonus_list_post',methods=['post'])
@login_required
def user_loss_bonus_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    try:
        mysql = Mysql()
        sql="select * from san_user_loss_money_bonus_list "
        res = mysql.getAll(sql,None)
        mysql.dispose()
        if res:
            data['data'] = res
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)




# 添加破产补贴
@user.route('/admin/add_user_loss_bonus_post',methods=['post'])
@login_required
def add_user_loss_bonus_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '添加失败！'
    try:
        loss_money = request.values.get('loss_money')
        money = request.values.get('money')
        mysql = Mysql()
        sql="insert into san_user_loss_money_bonus_list( loss_money, money, status)  " \
            "values(%s,%s,0)"
        res = mysql.insertOne(sql,[loss_money,money])
        mysql.dispose()
        if res:
            data['msg'] = '添加成功！'
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 修改破产补贴
@user.route('/admin/update_user_loss_bonus_post',methods=['post'])
@login_required
def update_user_loss_bonus_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '修改失败！'
    try:
        id = request.values.get('id')
        loss_money = request.values.get('loss_money')
        money = request.values.get('money')
        status = request.values.get('status')
        mysql = Mysql()
        sql="update san_user_loss_money_bonus_list set loss_money=%s,money=%s,status=%s where id=%s "
        res = mysql.update(sql,[loss_money,money,status,id])
        mysql.dispose()
        if res:
            data['msg'] = '修改成功！'
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)

# 禁用破产补贴
@user.route('/admin/update_user_loss_bonus_status_post',methods=['post'])
@login_required
def update_user_loss_bonus_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败！'
    try:
        id = request.values.get('id')
        status = request.values.get('status')
        mysql = Mysql()
        sql="update san_user_loss_money_bonus_list set status=%s where id=%s "
        res = mysql.update(sql,[status,id])
        mysql.dispose()
        if res:
            data['msg'] = '操作成功！'
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)

# 删除破产补贴
@user.route('/admin/delete_user_loss_bonus_post',methods=['post'])
@login_required
def delete_user_loss_bonus_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '删除失败！'
    try:
        id = request.values.get('id')
        mysql = Mysql()
        sql="delete from san_user_loss_money_bonus_list  where id=%s "
        res = mysql.update(sql,[id])
        mysql.dispose()
        if res:
            data['msg'] = '删除成功！'
            data['code'] = 1
            data['status'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 破产补贴领取列表
@user.route('/admin/user_loss_bonus_log_post',methods=['post'])
@login_required
def user_loss_bonus_log_post():
    data = dict()
    data['code'] = 0
    data['count'] = 0
    data['count_money'] = 0
    data['data'] = []
    try:
        uid = request.values.get('uid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page) - 1) * int(limit)

        sql_list = []
        if uid:
            sql_list.append(" (bonus_log.uid  like '%%%s%%' or users.nickname like '%%%s%%') " % (uid, uid))
        if stime:
            sql_list.append(" bonus_log.day >= '%s' " % stime)
        if etime:
            etime = str(etime) +" 23:59:59"
            sql_list.append(" bonus_log.day <= '%s' " % etime)
        sql_str = public_util.data_list_to_str(sql_list)
        mysql = Mysql()
        sql="select bonus_log.*,users.nickname from san_user_loss_money_bonus_log bonus_log " \
            "left join san_users users on bonus_log.uid=users.uid  %s order by id desc limit %d,%d" %(sql_str,offset,limit)
        sql_con="select count(*) con,sum(bonus_log.give_money) give_money from san_user_loss_money_bonus_log bonus_log " \
            "left join san_users users on bonus_log.uid=users.uid  %s " %(sql_str)
        res = mysql.getAll(sql,None)
        sql_con = mysql.getOne(sql_con,None)
        mysql.dispose()
        if res:
            for log in res:
                log['add_time']=str(log['add_time'])
                log['day']=str(log['day'])
            data['data'] = res
            data['count'] = sql_con['con']
            data['count_money'] = sql_con['give_money']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)