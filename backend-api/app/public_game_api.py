from random import random

from SqlConntion.MySqlConn import Mysql
from app import constant,public_util
import requests
import sys, time, json,importlib

importlib.reload(sys)
pwd = "66001234"


# 外接游戏退出
def wj_game_login_out(user, gid):
    game = get_wj_game(gid)
    if game is None:
        update_user_game(user['uid'])
        print("############无此游戏############")
        return True
    # SBO
    if game['my_game'] == 1:
        res = sbo_user_login_out(user, game)
        return True if res else False
    # PG
    if game['my_game'] == 2:
        res = seamless_out_login_user_game(user['uid'])
        return True if res else False
    # TaDa
    if game['my_game'] == 3:
        res = TaDa_login_out(user, game)
        return True if res else False
    # GS
    if game['my_game'] == 4:
        res = GS_user_withdraw(user, game)
        return True if res else False
    else:
        update_user_game(user['uid'])
        return True



# SBO 退出登录
def sbo_user_login_out(user, game):
    try:
        url = constant.SBO_URL + '/web-root/restricted/player/logout.aspx'
        maps = dict()
        maps['CompanyKey'] = constant.SBO_Company_Key
        maps['ServerId'] = constant.SBO_ServerId
        maps['Username'] = str(user['uid']) + '_' + constant.SBO_agent
        headers = dict()
        headers['Content-Type'] = 'application/json'
        res = requests.post(url, data=json.dumps(maps), headers=headers, verify=False, timeout=5)
        content = res.text
        content = json.loads(content)
        if content['error']['id'] == 0:
            user_sbo_withdraw(user, game)
            return True
    except Exception as e:
        print(e)
    return False




# 将用户余额转出sbo
def user_sbo_withdraw(user, game):
    transfer_id = 'SboWith' + public_util.add_order_number()
    flag = False
    try:
        url = constant.SBO_URL + '/web-root/restricted/player/withdraw.aspx'
        maps = dict()
        maps['CompanyKey'] = constant.SBO_Company_Key
        maps['ServerId'] = constant.SBO_ServerId
        maps['Username'] = str(user['uid']) + '_' + constant.SBO_agent
        maps['Amount'] = 0
        maps['txnId'] = transfer_id
        maps['IsFullAmount'] = True
        headers = dict()
        headers['Content-Type'] = 'application/json'
        res = requests.post(url, data=json.dumps(maps), headers=headers, verify=False, timeout=5)
        content = res.text
        result = json.loads(content)
        print("SBO余额转出 =>", result['amount'], "UID:", user['uid'], public_util.get_today())
        if result['error']['id'] == 0:
            money = float(result['amount'])
            flag = True
            if money > 0:
                refno = result['refno'] if 'refno' in result else transfer_id
                update_user_money_withdraw(user, money, transfer_id, refno, game)
                user['money'] = round(money + user['money'], 2)
    except Exception as e:
        print(e)
    return flag


# TaDa余额转出到我方
def TaDa_user_withdraw(user, game):
    flag = False
    transfer_id = 'TaDaDeposit' + add_order_number()
    try:
        url = constant.TaDa_API_URL + "ExchangeTransferByAgentId"
        maps = dict()
        maps['Account'] = user['uid']
        maps['TransactionId'] = transfer_id
        maps['Amount'] = round(float(user['money']), 2)
        maps['TransferType'] = 1
        maps['AgentId'] = constant.TaDa_AgentId
        maps['Key'] = tada_Key(maps)
        maps['Time'] = str(public_util.get_today())
        headers = dict()
        res = requests.post(url, data=maps, headers=headers, verify=False)
        content = res.text
        content = json.loads(content)
        if content['ErrorCode'] == 0:
            money = float(content['Data']['CoinBefore'])
            print("TADA 退出:", money, user['uid'])
            flag = True
            if money > 0:
                refno = content['Data']['TransactionId'] if content['Data'].get('TransactionId') else transfer_id
                update_user_money_withdraw(user, money, transfer_id, refno, game)
                user['money'] = round(money + user['money'], 2)
            else:
                update_user_game(user['uid'])
    except Exception as e:
        print(e)
    return flag



# 无缝钱包退出游戏
def seamless_out_login_user_game(uid):
    sql = "update san_users set cur_gameid = 0 where uid = '%s'" % uid
    mysql = Mysql()
    res = mysql.update(sql, None)
    mysql.dispose()
    return True if res else False

# 查询会员状态
def TaDa_get_user_money(uid):
    money = 0
    try:
        url = constant.TaDa_API_URL + 'GetMemberInfo'
        maps = dict()
        maps['Accounts'] = uid
        maps['AgentId'] = constant.TaDa_AgentId
        maps['Key'] = tada_Key(maps)
        headers = dict()
        res = requests.post(url, data=maps, headers=headers, verify=False)
        content = res.text
        content = json.loads(content)
        if content['ErrorCode'] == 0:
            money = content['Data'][0]['Balance']
    except Exception as e:
        print(e)
    return money



# 查询SBO中用户余额
def get_sbo_user_money(uid):
    money = 0
    try:
        url = constant.SBO_URL + '/web-root/restricted/player/get-player-balance.aspx'
        maps = dict()
        maps['CompanyKey'] = constant.SBO_Company_Key
        maps['ServerId'] = constant.SBO_ServerId
        maps['Username'] = str(uid) + '_' + constant.SBO_agent
        headers = dict()
        headers['Content-Type'] = 'application/json'
        res = requests.post(url, data=json.dumps(maps), headers=headers, verify=False, timeout=5)
        content = res.text
        result = json.loads(content)
        if result.get("balance"):
            money = float(result.get("balance"))
    except Exception as e:
        print(e)
    return money



# TaDa 退出登录
def TaDa_login_out(user, game):
    try:
        url = constant.TaDa_API_URL + 'KickMember'
        maps = dict()
        maps['Account'] = user['uid']
        maps['AgentId'] = constant.TaDa_AgentId
        maps['Key'] = tada_Key(maps)
        headers = dict()
        res = requests.post(url, data=maps, headers=headers, verify=False)
        content = res.text
        content = json.loads(content)
        if content['ErrorCode'] == 0:
            return TaDa_user_withdraw(user, game)
    except Exception as e:
        print(e)
    return False



# GS余额转出游戏
def GS_user_withdraw(user, game):
    flag = False
    url = constant.GS_api_url + "/makeTransfer.aspx?"
    transfer_id = public_util.add_order_number()
    maps = dict()
    maps['operatorcode'] = constant.GS_operator_code
    maps['providercode'] = "EP"
    maps['username'] = str(user['uid'])
    maps['password'] = pwd
    maps['referenceid'] = transfer_id
    maps['type'] = "1"
    maps['amount'] = round(float(GS_get_user_money(user['uid'], game)), 2)
    maps['signature'] = public_util.md5(str(maps['amount']) + maps['operatorcode'] + pwd + str(maps['providercode']) +
                                 str(transfer_id) + maps['type'] + str(maps['username']) +
                                 constant.GS_secret_key).upper()
    url = url + dict_switch(maps)
    res = requests.get(url, verify=False)
    content = json.loads(res.text)
    if str(content['errCode']) == "0":
        money = maps['amount']
        print("余额转出 -- GS", user['uid'], "==>", money)
        flag = True
        if money > 0:
            refno =  transfer_id
            update_user_money_withdraw(user, money, transfer_id, refno, game)
            user['money'] = round(money + user['money'], 2)
        else:
            update_user_game(user['uid'])
    return flag



# 获取GS余额
def GS_get_user_money(uid, game):
    money = 0
    url = constant.GS_api_url + "/getBalance.aspx?"
    maps = dict()
    maps['operatorcode'] = constant.GS_operator_code
    maps['providercode'] = "EP"
    maps['username'] = str(uid)
    maps['password'] = pwd
    maps['signature'] = public_util.md5(constant.GS_operator_code + maps['password'] + maps['providercode'] + str(uid) + constant.GS_secret_key).upper()
    url = url + dict_switch(maps)
    res = requests.get(url, verify=False)
    content = json.loads(res.text)
    print(content)
    if str(content['errCode']) == '0':
        money = float(content['balance'])
    return money




# 用户转账钱包提出
def update_user_money_withdraw(user, money, odd_number, tx_code, game):
    gid = game['gid'] if game else 0
    game_id = game['game_id'] if game else 0
    my_game = game['my_game'] if game else 0
    uid = user['uid']
    before_money = user['money']
    after_money = round(before_money + float(money), 2)
    money_type = 14  # 平台转出
    transfer_type = 1  # 0 存款 1 取款
    game_time = int(time.time())
    sql = "update san_users set money = money + '%s', cur_gameid = 0, game_time = '%s' where uid = '%s'" % \
          (money, game_time, uid)
    sql2 = "insert into san_user_money_log(uid, money, before_money, after_money, money_type, add_time) values " \
           "('%s', '%s', '%s', '%s', '%s', now())" % (uid, money, before_money, after_money, money_type)
    sql3 = "insert into san_game_transfer_log(uid, transfer_type, gid, game_id, my_game, before_money, after_money, " \
           "money, transfer_id, tx_code, add_time) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
           "'%s', now())" % (uid, transfer_type, gid, game_id, my_game, before_money,
                             after_money, money, odd_number, tx_code)
    mysql = Mysql()
    try:
        mysql.update(sql, None)
        mysql.insertOne(sql2, None)
        mysql.insertOne(sql3, None)
    except Exception as e:
        print(e)
    mysql.dispose()



# 查询接游戏
def get_wj_game(gid):
    sql = "select * from san_external_game_list where gid = '%s'" % gid
    mysql = Mysql()
    res = mysql.getOne(sql, None)
    mysql.dispose()
    return res



# 用户游戏状态下线
def update_user_game(uid):
    sql = "update san_users set cur_gameid = 0 where uid = '%s'" % uid
    mysql = Mysql()
    mysql.update(sql, None)
    mysql.dispose()




def tada_Key(maps):
    keyG = tada_KeyG()
    query = dict_switch(maps)
    md5_str = public_util.md5_string(query + keyG)
    randomText2 = "aacsrt"
    randomText1 = "443215"
    key = randomText1 + md5_str + randomText2
    return key

# KeyG
def tada_KeyG():
    y = time.strftime("%Y%m%d", time.gmtime(int(time.time()) - 3600 * 4))
    y = y[2:4]
    m = time.strftime("%m", time.gmtime(int(time.time()) - 3600 * 4))
    d = time.strftime("%d", time.gmtime(int(time.time()) - 3600 * 4))
    if str(d[0:1]) == "0":
        d = d[1:2]
    day = y + m + d
    key = public_util.md5_string(day + constant.TaDa_AgentId + constant.TaDa_AgentKey)
    return key


# 将dict对象转换成键=值拼接时加上&
def dict_switch(data):
    new_str = ""
    for item in data.keys():
        new_str += str(item) + "=" + str(data[item]) + "&"
    new_str = new_str[:-1]
    return new_str



def add_order_number():
    time_str = time.strftime("%Y%m%d%H%M%S")
    return str(time_str) + str(random.randint(100000, 999999))