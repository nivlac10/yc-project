# 后台访问域名
from app import withdraw_ice_pay

HOST_ARR = []

# 不屏蔽地址
allow_ip = ["巴西", "香港"]

my_pay_private_key = """
"""

"""
    创蓝云智 => 短信平台
"""
# 账号
CHUANG_LANG_YUN_ZHI_ACCOUNT = ""
# 密码
CHUANG_LANG_YUN_ZHI_PASSWORD = ""

"""
    gogopay 支付
"""
# appid
GO_GO_PAY_URL = ""
TEST_GO_GO_PAY_APPID = ""
TEST_GO_GO_PAY_SING_KEY = ""

"""
    Adco 支付
"""
ADOC_Url = ""
ADOC_merchant_id = ""
ADOC_api_key = ""
ADOC_api_secret = ""
ADOC_public_key = ""
ACOD_private_key = ''

"""
NTPAY
"""
NTPAY = {
    "url": "",
    "merchant_id": "",
    "merchant_pwd": "",
    "secret": ""
}

"""
ONEPAY
"""
ONEPAY = {
    "url": "",
    "mchId": "",
    "txChannel": "",
    "appId": "",
    "public_key": """"""
}

DBINDEX = 0

DBCONFIG = {
    0: {
        'p_name': '1',
        'db_name': "",
        'redis_db': "127.0.0.1",
        "sbo_agent": "",
        "MongoURL": "mongodb://127.0.0.1:27017",
        "MongodbName": "1winpg",
        "withdraw_conf": {
            '1': withdraw_ice_pay,
        }
    }
}