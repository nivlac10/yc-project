var express = require('express');
var router = express.Router();
const userDataUtil = require('../utils/userDataUtil');
const redis = require('../Redis/index');
const Time = require('../utils/Date');
const Utils = require('../utils/utils')
const Common = require('../utils/common')
const orders_callback = require("./orders_callback")
const user_withdraw_verify = require('./user_withdraw_verify')
const crypto = require('crypto');
const merchantID = 0
const secretKey = ""
// 充值回调
router.all('/api/ice_pay_notify_manage', async (req, res) => {
    try {
        let data = "error"
        let reqData = req.body
        let maps = {}
        console.log("ice_pay充值回调", req.body);
        maps['amount'] = reqData.amount
        maps['merchantId'] = reqData.merchantId
        maps['orderId'] = reqData.orderId
        maps['payOrderId'] = reqData.payOrderId
        maps['status'] = reqData.status
        maps['timestamp'] = reqData.timestamp
        maps['sign'] = reqData.sign
        let sign = paySignature(maps['amount'], reqData.merchantId, reqData.orderId, maps['timestamp'], secretKey)
        if (sign != reqData.sign) {
            data = "签名不正确！"
            console.log("签名不正确！");
            return res.send(data)
        }
        let money = reqData.amount / 100

        let con = await Common.get_order_info(maps['orderId'])
        if (!con) {
            data = "订单不存在！"
            console.log("订单不存在！"); return res.send(data)
        }
        const user = await userDataUtil.get_user_by_uid(con['uid'])
        if (!user) {
            data = "查无次订单用户"
            console.log("查无次订单用户:", maps['mchOrdernum']);
            return res.send(data)
        }
        const user_pay_key = 'san_game_pay_user_flag_' + String(user['uid']) + '_' + String(con['pay_id']) + '_' + String(con['card_id'])
        redis.del(user_pay_key)
        const order_status = maps['status'] == 1 ? 1 : 2

        orders_callback.pay_callback_func(con, user, order_status, String(reqData.ordernum), String(money))
        data = "OK"
        return res.send(data)
    } catch (error) {
        console.log(error);
    }
})


// 提现回调
router.all('/api/ice_pay_withdraw_notify', async (req, res) => {
    try {
        let data = "error"
        let reqData = req.body
        let maps = {}
        console.log("ice_pay充值回调", req.body);
        maps['amount'] = reqData.amount
        maps['merchantId'] = reqData.merchantId
        maps['orderId'] = reqData.orderId
        maps['payOrderId'] = reqData.payOrderId
        maps['status'] = reqData.status
        maps['timestamp'] = reqData.timestamp
        maps['sign'] = reqData.sign
        let sign = paySignature(maps['amount'], reqData.merchantId, reqData.orderId, maps['timestamp'], secretKey)
        if (sign != reqData.sign) {
            data = "签名不正确！"
            console.log("签名不正确！");
            return res.send(data)
        }
        let money = reqData.amount / 100

        let order_data = await user_withdraw_verify.get_user_withdraw_detail(maps['orderId'])

        if (!order_data) {
            data = "订单不存在！"
            console.log("订单不存在！"); return res.send(data)
        }
        const order_status = maps['status'] == 1 ? '1' : '2'
        const success_time = Time.formatDateHms(new Date)

        const return_msg = String(reqData.msg)
        const email_msg = 'check your bank info and re-withdraw sir'
        let orderRes = await user_withdraw_verify.update_order_info(order_data, String(money), order_status, success_time, return_msg, email_msg, String(maps['payOrderId']))
        if (orderRes) {
            data = "OK"
        }
        return res.send(data)
    } catch (error) {
        console.log(error);
    }
})
function paySignature(amount, merchantId, orderId, timestamp, secretKey) {
    const dataString = `${amount}${merchantId}${orderId}${timestamp}${secretKey}`;
    const md5Hash = crypto.createHash('md5').update(dataString).digest('hex');
    return md5Hash;
}
module.exports = router