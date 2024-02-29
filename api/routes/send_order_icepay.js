
const Time = require('../utils/Date')
const redis = require('../Redis/index')
const crypto = require('crypto');

const Utils = require('../utils/utils')
const PayUrl = ""
const WithdrawUrl = ""
const merchantID = 0
const secretKey = ""
const axios = require('axios');

class HALOPAY {
	// 发起支付
	static async http_post_pay_data(order_number, money, pay_data) {
		let data = {}
		data['code'] = 0
		data['url'] = ''
		data['oid'] = ''
		data['money'] = 0
		data['msg'] = ''
		data['send_data'] = {}
		try {
			let maps = {}
			maps['amount'] = money * 100
			maps['merchantId'] = String(merchantID)
			maps['orderId'] = order_number
			maps['timestamp'] = Date.now()
			maps['notifyUrl'] = pay_data['recharge_url']
			maps['sign'] = this.paySignature(maps['amount'], merchantID, order_number, maps['timestamp'], secretKey)
			console.log(maps)
			const response = await axios.post(PayUrl, maps, {
				headers: {
					'Content-Type': 'application/json',
				},
				timeout: 10000,
			});
			let resData = response.data
			console.log('icepay_pay', resData);
			if (resData.msg == "Success") {
				data['code'] = 1
				data['oid'] = resData.payOrderId
				data['url'] = resData.paymentUrl
				return data
			}
		} catch (error) {
			console.log(error);
		}
		return data
	}

	// 发起提现
	static async http_post_withdraw_data(user_pay_data, order_number, money, pay_data, vip) {
		let data = {}
		data['code'] = 0
		data['is_int'] = 0  //# 提现金额是否是int
		data['data'] = {}
		data['msg'] = 'error'
		data['send_data'] = {}
		try {
			money = money * 100
			let fee = vip['pay_fee']
			let fee_ratio = (100 - parseFloat(fee)) / 100
			if (fee_ratio < 0) fee_ratio = 1
			let send_money = ((parseFloat(money) * fee_ratio).toFixed())  //提现最终金额
			console.log(send_money);
			let maps = {}
			maps['amount'] = send_money
			maps['merchantId'] = String(merchantID)
			maps['orderId'] = order_number
			maps['timestamp'] = Date.now()
			maps['notifyUrl'] = pay_data['withdraw_conf_url']
			maps['outType'] = 'IMPS'
			maps['accountNumber'] = user_pay_data['account']
			maps['ifsc'] = user_pay_data['ifsc']
			maps['accountHolder'] = user_pay_data['name']
			maps['sign'] = this.paySignature(maps['amount'], merchantID, order_number, maps['timestamp'], secretKey)
			console.log(maps);
			const response = await axios.post(WithdrawUrl, maps, {
				headers: {
					'Content-Type': 'application/json',
				},
				timeout: 10000,
			});
			let resData = response.data
			console.log('icepay_with', resData);
			if (resData.code == 100) {
				data['code'] = 1
				data['data'] = resData
				data['msg'] = resData.msg
				return data
			} else {
				data['code'] = 0
				data['data'] = resData
				data['msg'] = resData.msg
				return data
			}
		} catch (error) {
			console.log(error);
		}

	}
	// 代收签名
	static paySignature(amount, merchantId, orderId, timestamp, secretKey) {
		const dataString = `${amount}${merchantId}${orderId}${timestamp}${secretKey}`;
		const md5Hash = crypto.createHash('md5').update(dataString).digest('hex');
		return md5Hash;
	}
}

module.exports = HALOPAY