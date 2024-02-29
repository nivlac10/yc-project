
import time
from flask import jsonify, request, abort
import requests, json, re, random, string
import hashlib
import codecs
import datetime, os
from SqlConntion.MySqlConn import Mysql
from app import redis,RKEY
from datetime import timedelta

PATH_FILE = '/home/file/'



# 获取今天日期
def get_today():
    now = datetime.datetime.now()
    return now

# 获取今天日期
def get_today_y_m_d():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d')

# 获取今天周几
def get_weekday():
    weekday = datetime.datetime.now().weekday()
    return int(weekday) + 1


# 获取昨天日期
def get_yesterday():
    yesterday = get_today() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def get_sevenday():
    sevenday = get_today() - timedelta(days=6)
    return sevenday.strftime('%Y-%m-%d')


# 获取本周第一天日期
def get_this_week_start():
    this_week_start = get_today() - timedelta(days=get_today().weekday())
    return this_week_start.strftime('%Y-%m-%d')


# 获取上周第一天日期
def get_last_week_start():
    last_week_start = get_today() - timedelta(days=get_today().weekday() + 7)
    return last_week_start.strftime('%Y-%m-%d')


# 获取上周最后一天日期
def get_last_week_end():
    last_week_end = get_today() - timedelta(days=get_today().weekday() + 1)
    return last_week_end.strftime('%Y-%m-%d')


# 获取下周一不转换时间
def get_next_week_monday():
    today = get_today()
    start_time = today + datetime.timedelta(days=7 - today.weekday())
    return start_time


# 获取下个月一号 不转换时间
def get_next_month_one():
    _time = datetime.date.today()
    first_day = datetime.date(_time.year, _time.month, 1)
    year = first_day.year
    month = first_day.month
    next_month_first_day = datetime.datetime(year + (month == 12), month == 12 or month + 1, 1, 0, 0, 0)
    return next_month_first_day


# 根据日期获取当天凌晨时间
def get_day_zero_time(date):
    if not date:
        return 0
    date_zero = datetime.datetime.now().replace(year=date.year, month=date.month,
                                                day=date.day, hour=0, minute=0, second=0)
    date_zero_time = int(time.mktime(date_zero.timetuple()))
    return date_zero_time


# 获取这月开始第一天
def get_this_month_start():
    this_month_start = datetime.datetime(get_today().year, get_today().month, 1)
    return this_month_start


# 获取上月最后一天
def get_last_month_end():
    last_month_end = get_this_month_start() - timedelta(days=1)
    return last_month_end


# 获取上月开始第一天
def get_last_month_start():
    last_month_start = datetime.datetime(get_last_month_end().year, get_last_month_end().month, 1)
    return last_month_start.strftime('%Y-%m-%d')


# 获取前30天
def get_last_three_day():
    last_three_day = get_today() - timedelta(days=30)
    return last_three_day.strftime('%Y-%m-%d')


def get_last_six_day():
    last_three_day = get_today() - timedelta(days=60)
    return last_three_day.strftime('%Y-%m-%d')


# 转化成json格式
def to_counts_json(response, counts):
    response_json = jsonify(response)
    response_json.headers['Access-Control-Allow-Origin'] = '*'
    response_json.headers['counts'] = counts
    return response_json


# 转化成json格式
def to_json(response):
    response_json = jsonify(response)
    response_json.headers['Access-Control-Allow-Origin'] = '*'
    return response_json


# md5加密
def md5(string):
    string = str(string)
    if isinstance(string, str):
        m = hashlib.md5()
        string = codecs.encode(string)
        m.update(string)
        return m.hexdigest()
    else:
        return ''

# md5加密
def md5_string(in_str):
    md5 = hashlib.md5()
    md5.update(in_str.encode("utf8"))
    result = md5.hexdigest()
    return result


# 时间戳转换为日期（年月日时分秒）
def int_day(timestamp):
    dd = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    return dd


#  时间戳转换为日期（年月日）
def int_ymd(timestamp):
    day = time.strftime('%Y-%m-%d', time.localtime(timestamp))
    return day


def int_ymds(timestamp):
    day = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    return day


# 日期转换为时间戳
def day_int(day):
    dt = int(time.mktime(time.strptime(day, '%Y-%m-%d')))
    return dt




# 操作记录公共方法
def user_update_log(action, pyname, content, sql_str, username=''):
    """
    :param username: 操作人
    :param action: 路由名称
    :param pyname: PY文件名称
    :param content: 操作内容
    :param sql_str: sql语句
    :return:
    """
    try:
        if username == '':
            username = request.cookies.get('admin_user', '')
        operate_ip = get_current_ip()  # 操作人IP
        country = ''
        province = ''
        city = ''
        place = country + '-' + province + '-' + city
        sql_str, num = re.subn('\"', '\'', str(sql_str), flags=re.I)
        mysql = Mysql()
        sql = "insert into new_syslog (username,ip,controller,time,action,content,sql_str,place) " \
              "VALUES ('%s','%s','%s',now(),'%s','%s',\"%s\",'%s')" \
              % (str(username), str(operate_ip), str(pyname), str(action), str(content), str(sql_str), str(place))
        mysql.insertOne(sql, None)
        mysql.dispose()
    except Exception as e:
        print(e)


# 获取IP
def get_current_ip():
    ip = request.headers.get('X-Real-Ip', request.remote_addr)
    return ip


# 返回当月的第一天跟最后一天
def getMonthFirstDayAndLastDay(year=None, month=None):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: firstDay: 当月的第一天，datetime.date类型
              lastDay: 当月的最后一天，datetime.date类型
    """
    import datetime, calendar
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year
    if month:
        month = int(month)
    else:
        month = datetime.date.today().month
    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)
    # 获取当月的第一天
    firstDay = datetime.date(year=year, month=month, day=1)
    lastDay = datetime.date(year=year, month=month, day=monthRange)
    return firstDay, lastDay





def some_time(create_time):
    create_time = int(time.mktime(create_time.timetuple()))
    cur_time = time.time()
    c_time = cur_time - create_time
    if c_time / 60 < 1:
        last_time = u'刚刚'
    elif c_time / 60 < 60:
        last_time = str(int(c_time / 60)) + u'分钟前'
    elif c_time / 60 / 60 < 24:
        last_time = str(int(c_time / 60 / 60)) + u'小时前'
    elif c_time / 86400 < 30:
        last_time = str(int(c_time / 86400)) + u'天前'
    elif c_time / 86400 / 30 < 12:
        last_time = str(int(c_time / 86400 / 30)) + u'月前'
    else:
        last_time = u'1年前'
    return last_time


#  随机生成指定长度的字符串
def random_str(num):
    chars = string.ascii_lowercase
    return ''.join(random.choice(chars) for x in range(num))


# 随机生成渠道key
def random_channel_key():
    num = random.randint(2, 5)
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(num))


# 签名验证
def sign_verify(p_list, maps, sign, s_key):
    sign_str = ''
    for d in p_list:
        if maps[d] or maps[d] == '':
            sign_str += '%s=%s&' % (d, maps[d])
    if sign_str == '':
        return False
    sign_str = sign_str[:-1] + s_key
    v_sign = md5(str(sign_str))
    return sign == v_sign


# 获取渠道信息
def get_channel_info(cid):
    res = redis.hget(RKEY.SAN_GAME_NEW_CHANNEL_CONF, str(cid))
    return json.loads(res) if res else None


# 保存图片到本地
def save_img_file(path, file_img):
    img_name = ''
    try:
        if file_img:
            file_name = file_img.filename
            if os.path.exists(path) is False:
                os.makedirs(path)
            names = file_name.split('.')
            str_name = getRandomString(5)
            img_name = str(int(time.time() * 1000)) + str_name + '.' + names[len(names) - 1]
            img_local_path = os.path.join(path, img_name)
            file_img.save(img_local_path)
    except Exception as e:
        print(e)
    return img_name

# 保存图片到本地
def save_game_img_file(path, file_img, gid):
    img_name = ''
    try:
        if file_img:
            file_name = file_img.filename
            if os.path.exists(path) is False:
                os.makedirs(path)
            names = file_name.split('.')
            img_name = str(gid) + '.' + names[len(names) - 1]
            img_local_path = os.path.join(path, img_name)
            file_img.save(img_local_path)
    except Exception as e:
        print(e)
    return img_name

def data_list_to_str(sql_list):
    sql_str = ""
    if len(sql_list) > 0:
        if len(sql_list) > 1:
            sql_str += " where " + ' and '.join(sql_list)
        else:
            sql_str += " where " + sql_list[0]
    return sql_str

def dataMongo_list_to_str(mg_list):
    sql_str = {}
    if len(mg_list) > 0:
        sql_str = {'$and': mg_list}
    return sql_str


# 判断两个日期是否相同
def judge_date_same(date_1, date_2):
    flag = 0
    if date_1.strftime("%Y-%m-%d") == date_2.strftime("%Y-%m-%d"):
        flag = 1
    return flag


def getRandomString(randomlength=4):
    digits = "0123456789"
    ascii_letters = "abcdefghijklmnopqrstuvwxyz"
    str_list = [random.choice(digits + ascii_letters) for i in range(randomlength)]
    random_str = "".join(str_list)
    return random_str

# 订单号
def add_order_number():
    time_str = time.strftime("%Y%m%d%H%M%S")
    return str(time_str) + str(random.randint(100000, 999999))

    # 图片处理

def Get_image_url(image,PATH):
    img_url = ''
    if image:
        img_name = save_img_file(PATH_FILE + PATH, image)
        img_url = PATH + img_name
    return img_url


# 查询集成商
def get_table_info(tablename,where_str,where_val):
    mysql = Mysql()
    query_sql = "select * from "+tablename+" where "+ where_str
    query_res = mysql.getOne(query_sql, [where_val])
    mysql.dispose()
    return query_res



