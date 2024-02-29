from flask import request, jsonify

from app.activity import activity
from app.util import login_required
from app import public_util
from SqlConntion.MySqlConn import Mysql


# 查询打码任务列表
@activity.route('/admin/bet_task_list_post', methods=['post'])
# @login_required
def bet_task_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        page = request.values.get('page')
        limit = request.values.get('limit')
        offset = (int(page) - 1) * int(limit);
        mysql = Mysql()
        sql = "select * from san_user_bet_day_task_list order by id asc limit %d,%d " % (int(offset), int(limit))
        sql_con = "select count(*) con from san_user_bet_day_task_list "
        res = mysql.getAll(sql, None)
        res_con = mysql.getOne(sql_con, None)
        mysql.dispose()
        if res:
            data['data'] = res
            data['count'] = res_con['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)


# 添加打码任务
@activity.route('/admin/add_bet_task_post', methods=['post'])
@login_required
def add_bet_task_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '添加失败'
    try:
        need_code_amount = request.values.get('need_code_amount')
        money = request.values.get('money')
        mysql = Mysql()
        sql = "insert into san_user_bet_day_task_list( need_code_amount, money, status) values (%s,%s,0) "
        res = mysql.insertOne(sql, [need_code_amount, money])
        mysql.dispose()
        if res:
            print(res)
            data['status'] = 1
            data['code'] = 1
            data['msg'] = '添加成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 修改打码任务
@activity.route('/admin/update_bet_task_post', methods=['post'])
@login_required
def update_bet_task_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '更新失败'
    try:
        id = request.values.get('id')
        need_code_amount = request.values.get('need_code_amount')
        money = request.values.get('money')
        status = request.values.get('status')
        mysql = Mysql()
        sql = "update  san_user_bet_day_task_list set need_code_amount=%s,money=%s,status=%s where id=%s "
        res = mysql.update(sql, [need_code_amount, money, status, id])
        mysql.dispose()
        if res:
            data['status'] = 1
            data['code'] = 1
            data['msg'] = '更新成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 禁用打码任务
@activity.route('/admin/update_bet_task_status_post', methods=['post'])
@login_required
def update_bet_task_status_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        id = request.values.get('id')
        status = request.values.get('status')
        mysql = Mysql()
        sql = "update  san_user_bet_day_task_list set status=%s where id=%s "
        res = mysql.update(sql, [status, id])
        mysql.dispose()
        if res:
            data['status'] = 1
            data['code'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除打码任务
@activity.route('/admin/delete_bet_task_post', methods=['post'])
@login_required
def delete_bet_task_post():
    data = dict()
    data['code'] = 0
    data['status'] = 0
    data['msg'] = '删除失败'
    try:
        id = request.values.get('id')
        mysql = Mysql()
        sql = "delete from san_user_bet_day_task_list where id=%s "
        res = mysql.delete(sql, [id])
        mysql.dispose()
        if res:
            data['status'] = 1
            data['code'] = 1
            data['msg'] = '删除成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 查询打码任务日志列表
@activity.route('/admin/bet_task_log_list_post', methods=['post'])
@login_required
def bet_task_log_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    data['count_money'] = 0
    try:
        uid = request.values.get('uid')
        task_id = request.values.get('task_id')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        page = request.values.get('page')
        limit = request.values.get('limit')
        offset = (int(page) - 1) * int(limit);
        sql_list = []
        sql_list.append(" task_log.uid=users.uid ")
        if uid:
            sql_list.append(" (task_log.uid like '%%%s%%' or users.nickname like '%%%s%%' )" % (uid, uid))
        if task_id:
            sql_list.append(" task_log.task_id='%s'" % task_id)
        if stime:
            sql_list.append(" task_log.add_time>='%s' " % (stime))
        if etime:
            etime = etime + " 23:59:59"
            sql_list.append(" task_log.add_time<='%s' " % (etime))
        sql_list = public_util.data_list_to_str(sql_list)
        mysql = Mysql()
        sql = "SELECT task_log.*,users.nickname FROM san_user_bet_day_task_log task_log,san_users users " \
              " %s order by id asc limit %d,%d " % (sql_list, int(offset), int(limit))
        sql_con = "SELECT count(*) con,sum(ifnull(task_log.money,0)) money FROM san_user_bet_day_task_log task_log,san_users users " \
                  " %s " % sql_list
        print(sql)
        res = mysql.getAll(sql, None)
        res_con = mysql.getOne(sql_con, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                d['day'] = str(d['day'])
            data['data'] = res
            data['count'] = res_con['con']
            data['count_money'] = res_con['money']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)



# 查询打码日志列表
@activity.route('/admin/bet_code_log_list_post', methods=['post'])
@login_required
def bet_code_log_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        uid = request.values.get('uid')
        cid = request.values.get('cid')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        page = request.values.get('page')
        limit = request.values.get('limit')
        offset = (int(page) - 1) * int(limit);
        sql_list = []
        if uid:
            sql_list.append(" (a.uid like '%%%s%%' or c.nickname like '%%%s%%' )" % (uid, uid))
        if cid:
            sql_list.append(" a.cid='%s'" % cid)
        if stime:
            sql_list.append(" a.add_time>='%s' " % (stime))
        if etime:
            etime = etime + " 23:59:59"
            sql_list.append(" a.add_time<='%s' " % (etime))
        sql_list = public_util.data_list_to_str(sql_list)
        mysql = Mysql()
        sql = "select a.*,b.username,c.nickname from san_user_code_log a inner join san_agent b on a.cid=b.cid " \
              " inner join san_users c on a.uid=c.uid " \
              " %s order by id asc limit %d,%d " % (sql_list, int(offset), int(limit))
        sql_con = "SELECT count(*) con from san_user_code_log a inner join san_users c on a.uid=c.uid %s " % sql_list
        res = mysql.getAll(sql, None)
        res_con = mysql.getOne(sql_con, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
            data['data'] = res
            data['count'] = res_con['con']
        data['code'] = 1
    except Exception as e:
        print(e)
    return jsonify(data)
