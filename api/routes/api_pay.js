var express = require('express');
var router = express.Router();
const Mysql = require('../Mysql/mysql')
const redis = require('../Redis/index')
const auth = require('../middleware/auth')
const Time = require('../utils/Date')
const RKEY = require('../RKEY')
const Utils = require('../utils/utils')
const icepay = require('./send_order_icepay')

const orders_callback = require("./orders_callback")
const Common = require('../utils/common')

const PAY_CONF = {
	1: icepay,
}

// 用户充值
router.all('/api/test_user_pay', auth, async (req, res, next) => {
	console.log('test_user_paytest_user_paytest_user_pay');
	// 提现配置
	var sql = "select * from san_pay_list where with_flag = 1 order by sort_index desc";
	var mysql = new Mysql();
	var resSql = await mysql.getAll(sql, []);
	if (resSql) {
		var resource_host = (await redis.hget(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST)) || '';
		for (var i = 0; i < resSql.length; i++) {
			resSql[i]['cover'] = resource_host + (resSql[i]['cover'] || '');
		}
	}
	resSql = resSql || [];
	redis.set(RKEY.SAN_GAME_NEW_WITHDRAW_CONF, JSON.stringify(resSql));
})

// 用户充值
router.post('/api/user_pay', auth, async (req, res, next) => {
	let data = {
		code: 0,
		url: '',
		pay_type: 0
	}
	console.log(req.uid)
	try {
		let money = req.body.money
		let bonus_type = req.body.bonus_type || 0
		let pay_type = req.body.pay_type
		if (req.uid == 0) {
			data['code'] = 2  // 登陆认证失败重新登陆
			return res.send(data)
		}
		if (parseFloat(money) <= 0) {
			data['code'] = 27  // 支付金额不能小于或等于0
			return res.send(data)
		}
		let min_recharge_money = (await redis.hget('san_game_all_conf', 'min_recharge_money')) || '0'
		if (parseFloat(money) < parseFloat(min_recharge_money)) {
			data['code'] = 100  // 充值金额低于最低充值
			return res.send(data)
		}
		let pay_info = await get_pay_info(parseFloat(money))
		if (!pay_info) {
			data['code'] = 29  // 查无此通道
			return res.send(data)
		}
		data['pay_type'] = pay_info['pay_type']
		if (parseFloat(money) < parseFloat(pay_info['min_payment_money']) || parseFloat(money) > parseFloat(pay_info['max_payment_money'])) {
			data['code'] = 28;  // 参数错误
			return res.send(data)
		}
		let user = await get_user_info(req.uid)
		pay_info['phone'] = user['phone']
		pay_info['name'] = user['nickname']
		if (!user) {
			data['code'] = 3
			return res.send(data)
		}
		const util = new Utils()
		let order_number = util.add_order_number()
		let result = await call_pay_func(order_number, money, pay_info)
		var status = (result['code'] === 1) ? 0 : 3;
		let day = Time.get_today_ymd()
		let user_day = Time.formatDateHms(user['add_time']).slice(0, 10);
		let new_user_flag = (day === user_day) ? 0 : 1;
		if (result['code'] != 0) {
			let res = await add_order_log(user, money, order_number, order_number, new_user_flag, result, status, pay_info, bonus_type, req.realIp)
			if (res <= 0) return res.send(data)
			data['url'] = result['url']
			data['order_number'] = order_number
			data['code'] = 1
		} else {
			add_order_log(user, money, order_number, order_number, new_user_flag, result, status, pay_info, bonus_type, req.realIp)
			data['code'] = 100
		}
		console.log('data', data);
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 用户查询充值状态
router.post('/api/get_order_state', auth, async (req, res, next) => {
	let data = {
		code: 0,
		msg: 'Transaction Not Yet Completed！！！',
		first_pay: 0,
		state: 0,
		money: 0
	}
	try {
		let order_number = req.body.order_number
		if (req.uid == 0) {
			data['code'] = 2  // 登陆认证失败重新登陆
			return res.send(data)
		}
		let con = await get_order_info(order_number, req.uid)
		if (!con) {
			data['code'] = 36
			return res.send(data)
		}
		data['state'] = con['status']
		data['money'] = con['money']
		if (con['status'] == 0) {
			data['code'] = 1
		} else if (con['status'] == 1) {
			data['code'] = 1
			data['msg'] = "Successful Transaction！"
			data['first_pay'] = con['first_pay']
		} else if (con['status'] == 2) {
			data['code'] = 1
			data['msg'] = "Transaction Failed！"
		}

		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 获取充值活动
router.post('/api/get_recharge_activity', auth, async (req, res, next) => {
	let data = {
		data: [],
		code: 0,
		first_charge_give_rate: (await redis.hget(RKEY.SAN_GAME_ALL_CONF, 'first_charge_give_rate')) || 0,
		day_charge_give_rate: (await redis.hget(RKEY.SAN_GAME_ALL_CONF, 'day_charge_give_rate')) || 0,
	}
	try {
		let recharge_list = await redis.get(RKEY.SAN_GAME_PAY_ACTION_CONF)
		recharge_list = recharge_list ? (JSON.parse(recharge_list)) : []
		if (recharge_list.length === 0) {
			data['code'] = 1;
			return res.send(data)
		} else {
			var new_arr = [];
			for (var i = 0; i < recharge_list.length; i++) {
				var item = recharge_list[i];
				if (parseInt(Date.now() / 1000) < parseInt(item['over_time'])) {
					new_arr.push(item);
				}
			}
			data['data'] = new_arr;
			data['code'] = 1;
		}
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 获取用户信息
const get_user_info = async (uid) => {
	let sql = `select * from san_users where uid = ?`
	const mysql = new Mysql()
	const res = await mysql.getOne(sql, [uid])
	return res
}

// 获取支付渠道信息 
const get_pay_info = async (money) => {
	let pay = await redis.get(RKEY.SAN_GAME_NEW_WITHDRAW_CONF)
	if (pay === null) {
		return null;
	}
	pay = JSON.parse(pay)
	if (pay.length === 0) {
		return null;
	}
	let arr = []
	let total_v = 0
	let vs = []
	for (var i = 0; i < pay.length; i++) {
		var p = pay[i];
		if (p['min_payment_money'] <= money && p['max_payment_money'] >= money) {
			arr.push(p);
			total_v += p['sort_index'];
			vs.push(total_v);
		}
	}
	if (arr.length === 0) {
		return null;
	}
	if (total_v === 0) {
		return arr[0];
	}
	var r = Math.floor(Math.random() * total_v);
	for (var i = 0; i < vs.length; i++) {
		if (r < vs[i]) {
			return arr[i];
		}
	}
	return arr[0];
}


const call_pay_func = async (order_number, money, pay_data) => {
	let maps = {
		code: 0,
		url: '',
		oid: '',
		money: 0,
		msg: ''
	}
	if (!PAY_CONF.hasOwnProperty(String(pay_data['pay_id']))) {
		maps.oid = order_number
		maps.msg = 'pay id error'
		return maps;
	}
	maps = await PAY_CONF[pay_data['pay_id']].http_post_pay_data(order_number, money, pay_data);
	return maps
}

// 添加下单记录
const add_order_log = async (user, money, order_number, pay_order_number, new_user_flag, content, status, pay, bonus_type, ip) => {
	let pay_fee = Math.round(parseFloat(money) * parseFloat(pay['pay_ratio']) / 100, 2);
	const sql = "insert into san_order_list(uid,  cid, order_number, pay_order_number, money, user_ip,  new_user_flag," +
		" pay_id, status, err_msg, pay_fee, add_time, bonus_type) values (?, ?, ?, " +
		"?, ?, ?, ?, ?, ?, ?, ?,  now(), ?)"
	const mysql = new Mysql()
	const resSql = await mysql.awaitSql(sql, [user['uid'], user['cid'], order_number, pay_order_number, money, ip, new_user_flag,
	pay['pay_id'], status, JSON.stringify(content), pay_fee, bonus_type])
	return resSql
}

// 获取用户订单详情
const get_order_info = async (order_number, uid) => {
	const mysql = new Mysql()
	const resSql = await mysql.getOne('select * from san_order_list where order_number = ? and uid = ?', [order_number, uid])
	return resSql
}

module.exports = router;