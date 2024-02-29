# -*- coding: UTF-8 -*-
"""
Created on 2016年5月7日
@author: steve bi

"""
# 本地
DBHOST="127.0.0.1"
DBPORT = 3306
DBUSER="root"
DBNAME=""
DBPWD=""
DBCHAR = "utf8"


R_host = "127.0.0.1"
R_db = 0


# mongoDB
MongoDB_URL = "mongodb://127.0.0.1"
MongoDB_DBNAME = ""


# 飞机群机器人
BOT_TOKEN = ""
CHAT_ID = ""

# byte转str
def bytes_to_str(date_list):
    if date_list:
        if type(date_list) == list:
            for date in date_list:
                for key in date.keys():
                    if type(date[key]) == bytes:
                        date[key] = bytes.decode(date[key])
        else:
            for key in date_list.keys():
                if type(date_list[key]) == bytes:
                    date_list[key] = bytes.decode(date_list[key])
    return date_list
