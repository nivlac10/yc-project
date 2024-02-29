

from . import activity
from flask import  request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app import public_util
import sys

import importlib
from .. import util_update_redis
importlib.reload(sys)

# 获取领取佣金日志列表
@activity.route('/admin/commission_log_list_post', methods=['post'])
@login_required
def commission_log_list_post():
    data = dict()
    data['code'] = 0
    data['count'] = 0
    data['data'] = []
    try:
        uid = request.values.get('uid')
        task_id = request.values.get('task_id')
        stime = request.values.get('stime')
        etime = request.values.get('etime')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        offset = (int(page)-1)*limit
        sql_list=[]
        sql_list.append(" task_log.task_id=task.task_id ")
        sql_list.append(" task_log.uid=users.uid ")
        if uid:
            sql_list.append(" (task_log.uid like '%%%s%%' or users.username like '%%%s%%' )"%(uid,uid))
        if task_id:
            sql_list.append(" (task_log.task_id like '%%%s%%' or task.task_name like '%%%s%%' )"%(task_id,task_id))
        if stime:
            sql_list.append(" task_log.add_time>='%s' "%(stime))
        if etime:
            etime=etime+" 23:59:59"
            sql_list.append(" task_log.add_time<='%s' "%(etime))
        sql_list = public_util.data_list_to_str(sql_list)
        mysql = Mysql()
        sql = "SELECT task_log.*,users.username,task.task_name FROM `san_user_invite_task_log` task_log," \
            "san_user_invite_task task,san_users users %s  order by task_log.id desc limit %d,%d" % (sql_list,offset,limit)
        sql_con = "SELECT count(*) con FROM `san_user_invite_task_log` task_log," \
            "san_user_invite_task task,san_users users %s " % (sql_list)
        res = mysql.getAll(sql,None)
        res_con = mysql.getOne(sql_con,None)
        if res:
            for task in res:
                task['add_time'] = str(task['add_time'])
            data['data'] = res
            data['count'] = res_con['con']
        data['code'] = 1
    except Exception as ex:
        print(ex)
    return jsonify(data)


