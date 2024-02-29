
from . import admin
from flask import render_template, request, jsonify
from SqlConntion.MySqlConn import Mysql
from app.util import login_required
from app.util import user_power
from app import public_util
import sys, time

import importlib
importlib.reload(sys)



# 获取模块列表
@admin.route('/admin/power_class_post',methods=['post'])
@login_required
def power_class_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    try:
        sql = "select * from san_power_class order by c_index desc,cid asc"
        mysql = Mysql()
        powers = mysql.getAll(sql,None)
        mysql.dispose()
        if powers:
            for power in powers:
                power['add_time']=str(power['add_time'])
                # 转换时间戳
                # power['time_int']=public_util.days_int(power['add_time']) * 1000
            data['data']=powers
        data['code'] = 1
    except Exception as ex:
        print (ex)
    return jsonify(data)


# 添加模块
@admin.route('/admin/add_power_class_post',methods=['post'])
@login_required
def add_power_class_post():
    data= dict()
    data['code']=0;
    data['status']=0;
    data['msg']='操作失败';
    try:
      name =  request.values.get('class_name')
      icon =  request.values.get('class_icon')
      index =  request.values.get('c_index')
      res=get_power_iscontain(name)
      if res:
          data['status']=2
          data['msg'] ='模板已存在'
      res=add_power(name,icon,index)
      if res:
          data['code'] = 1;
          data['status'] = 1
          data['msg'] = '添加成功'
    except Exception as ex:
        print (ex)
    return data




# 编辑模块处理
@admin.route('/admin/power_class_detail_post',methods=['post'])
@login_required
def power_class_detail_post():
    data = dict()
    data['code']=0;
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        class_name = request.values.get('class_name')
        c_index = request.values.get('c_index')
        cid = request.values.get('cid')
        icon = request.values.get('icon')
        res = update_power_class(class_name, c_index, cid,icon)
        if res > 0:
            data['code']=1;
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print (e)
    return jsonify(data)


# 删除模块
@admin.route('/admin/delete_power_class', methods=['post'])
@login_required
def delete_power_class():
    data = dict()
    data['code']=0;
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        cid = request.values.get('cid')
        res = get_power_below(cid)
        if res:
            data['status'] = 2
            data['msg'] = '存在下级路由，请先删除下级路由'
            return jsonify(data)
        con = _delete_class(cid)
        if con > 0:
            data['code']=1;
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print (e)
    return jsonify(data)


# 获取路由数据
@admin.route('/admin/router_list_post', methods=['post'])
@login_required
def router_list_post():
    data = dict()
    data['code'] = 0
    data['data'] = []
    data['count'] = 0
    try:
        cid = request.values.get('cid')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql = "select r.*, c.class_name FROM san_power_router r LEFT JOIN san_power_class c ON c.cid = r.cid" \
              " WHERE 1=1"
        sql2 = "select count(*) con FROM san_power_router r LEFT JOIN san_power_class c ON c.cid = r.cid WHERE 1=1"
        if cid:
            sql += " and r.cid = '%s'" % cid
            sql2 += " and r.cid = '%s'" % cid
        sql += " order by  c.c_index desc,c.cid asc,r.r_index desc,r.rid asc limit %d, %d" % (c_num, limit)
        mysql = Mysql()
        res = mysql.getAll(sql, None)
        cont = mysql.getOne(sql2, None)
        mysql.dispose()
        if res:
            for d in res:
                d['add_time'] = str(d['add_time'])
                # d['time_int'] = public_util.days_int(d['add_time']) * 1000
            data['data'] = res
            data['code'] = 1
            data['count'] = int(cont['con'])
    except Exception as e:
        print (e)
    return jsonify(data)




# 添加路由处理
@admin.route('/admin/add_router_post', methods=['post'])
@login_required
def add_router_post():
    data = dict()
    data['code']=0;
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        cid = request.values.get('cid')
        router_name = request.values.get('router_name')
        router_url = request.values.get('router_url')
        r_index = request.values.get('r_index')
        iscontain = get_router_iscontain(router_name)
        if iscontain:
            data['status'] = 2
            data['msg'] = '路由名称已存在'
            return jsonify(data)
        sql = "insert INTO san_power_router(router_name, cid, router_url, r_index, add_time) VALUES ('%s', '%s'," \
              " '%s', '%s', now())" % (router_name, cid, router_url, r_index)
        mysql = Mysql()
        res = mysql.insertOne(sql, None)
        mysql.dispose()
        if res > 0:
            data['code']=1;
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print (e)
    return jsonify(data)



# 更新路由处理
@admin.route('/admin/router_detail_post', methods=['post'])
@login_required
def router_detail_post():
    data = dict()
    data['code']=0;
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        cid = request.values.get('cid')
        router_name = request.values.get('router_name')
        router_url = request.values.get('router_url')
        r_index = request.values.get('r_index')
        rid = request.values.get('rid')
        sql = "update san_power_router set cid = '%s', router_name = '%s', router_url = '%s', r_index = '%s'" \
              " WHERE rid = '%s'" % (cid, router_name, router_url, r_index, rid)
        mysql = Mysql()
        res = mysql.update(sql, None)
        mysql.dispose()
        if res > 0:
            data['code']=1;
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print (e)
    return jsonify(data)


# 删除路由
@admin.route('/admin/delete_router_url', methods=['post'])
@login_required
def delete_router_url():
    data = dict()
    data['code']=0;
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        rid = request.values.get('rid')
        below = get_router_below(rid)
        if below:
            data['status'] = 2
            data['msg'] = '存在下级接口，请先删除下级接口'
            return jsonify(data)
        sql = "delete FROM san_power_router WHERE rid = '%s'" % rid
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res > 0:
            data['code']=1;
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print (e)
    return jsonify(data)

# 接口列表
@admin.route('/admin/interface_list_post', methods=['post'])
@login_required
def interface_list_post():
    data=dict()
    data['code']=0
    data['data']=[]
    data['count']=0
    try:
        cid=request.values.get('cid')
        rid=request.values.get('rid')
        i_name=request.values.get('interface_name')
        limit = int(request.values.get('limit', '20'))
        page = request.values.get('page', '1')
        c_num = (int(page) - 1) * int(limit)
        sql="SELECT jk.*,mb.class_name,ly.router_name FROM san_power_interface jk,san_power_class mb,san_power_router ly " \
            "where jk.cid=mb.cid and jk.rid=ly.rid"
        sql1="SELECT count(*) con FROM san_power_interface jk,san_power_class mb,san_power_router ly " \
            "where jk.cid=mb.cid and jk.rid=ly.rid"
        if cid:
            sql+=" and jk.cid='%s'"%cid
            sql1+=" and jk.cid='%s'"%cid
        if rid:
            sql += " and jk.rid='%s'" % rid
            sql1 += " and jk.rid='%s'" % rid
        if i_name:
            sql += " and jk.interface_name like '%%%s%%'" % i_name
            sql1 += " and jk.interface_name like '%%%s%%'" % i_name
        sql+=" order by  jk.j_index desc,jk.jid asc,mb.c_index desc,mb.cid asc,ly.r_index desc,ly.rid asc limit %d, %d"%(c_num,limit)
        mysql=Mysql()
        res=mysql.getAll(sql,None)
        count=mysql.getOne(sql1,None)
        mysql.dispose()
        if res:
            for interface in res:
                interface['add_time']=str(interface['add_time'])
            data['data']=res
            data['count'] = int(count['con'])
            data['code']=1
    except Exception as e:
        print(e)
    return jsonify(data);

# 添加接口
@admin.route('/admin/add_interface_post', methods=['post'])
@login_required
def add_interface_post():
    data = dict()
    data['code']=0;
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        cid=request.values.get('cid')
        rid=request.values.get('rid')
        url=request.values.get('interface_url')
        index=request.values.get('j_index')
        j_iscontain=get_interface_iscontain(url)
        if j_iscontain:
            data['status'] = 2
            data['msg'] = '接口已存在'
            return jsonify(data)
        res=add_interface(url,index,cid,rid)
        if res:
            data['code']=1;
            data['status'] = 1
            data['msg'] = '添加成功'
    except Exception as e:
        print(e)
    return jsonify(data)

# 更新接口
@admin.route('/admin/interface_detail_post', methods=['post'])
@login_required
def interface_detail_post():
    data = dict()
    data['code']=0;
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        jid=request.values.get('jid')
        cid=request.values.get('cid')
        rid=request.values.get('rid')
        url=request.values.get('interface_url')
        index=request.values.get('j_index')
        sql="update san_power_interface set cid='%s',rid='%s',interface_url='%s',j_index='%s' where jid='%s'"\
            %(cid,rid,url,index,jid)
        mysql=Mysql()
        res=mysql.update(sql,None)
        mysql.dispose()
        if res:
            data['code']=1;
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 删除接口
@admin.route('/admin/delete_interface_post', methods=['post'])
@login_required
def delete_interface_post():
    data = dict()
    data['code']=0;
    data['status'] = 0
    data['msg'] = '操作失败'
    try:
        jid=request.values.get('jid')
        sql = "delete FROM san_power_interface WHERE jid = '%s'" % jid
        mysql = Mysql()
        res = mysql.delete(sql, None)
        mysql.dispose()
        if res > 0:
            data['code']=1;
            data['status'] = 1
            data['msg'] = '操作成功'
    except Exception as e:
        print(e)
    return jsonify(data)


# 判断模块是否已存在
def get_power_iscontain(power_name):
    sql = "select * from san_power_class where class_name = '%s'" % power_name
    mysql=Mysql()
    res=mysql.getOne(sql,None)
    mysql.dispose()
    return res

# 添加模块
def add_power(power_name,icon,index):
    sql="insert into san_power_class(class_name,c_index,add_time,icon) values('%s','%s',now(),'%s')"%(power_name,index,icon)
    mysql=Mysql()
    res=mysql.insertOne(sql,None)
    mysql.dispose()
    return res

# 修改模块
def update_power_class(class_name, c_index, cid,icon):
    sql = "update san_power_class SET class_name = '%s', c_index = '%s',icon='%s' WHERE cid = '%s'" % (class_name, c_index,icon, cid)
    mysql = Mysql()
    res = mysql.update(sql, None)
    mysql.dispose()
    return res


# 查询是否存在下级路由
def get_power_below(cid):
    sql = "select * FROM san_power_router WHERE cid = '%s'" % cid
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res

# 删除模块操作
def _delete_class(cid):
    sql = "delete FROM san_power_class WHERE cid = '%s'" % cid
    mysql = Mysql()
    res = mysql.delete(sql, None)
    mysql.dispose()
    return res


# 查询路由名称是否存在
def get_router_iscontain(router_name):
    sql ="select * FROM san_power_router WHERE router_name = '%s'" % router_name
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res

# 查询是否存在下级接口
def get_router_below(rid):
    sql = "select * FROM san_power_interface WHERE rid = '%s'" % rid
    mysql = Mysql()
    res = mysql.getAll(sql, None)
    mysql.dispose()
    return res

# 查询接口是否存在
def get_interface_iscontain(interface_url):
    sql ="select * FROM san_power_interface WHERE interface_url = '%s'" % interface_url
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res

# 添加接口
def add_interface(interface_url,index,cid,rid):
    sql="insert into san_power_interface(rid,cid,interface_url,add_time,j_index) values('%s','%s','%s',now(),'%s')"\
        %(rid,cid,interface_url,index)
    mysql=Mysql()
    res=mysql.insertOne(sql,None)
    mysql.dispose()
    return res
