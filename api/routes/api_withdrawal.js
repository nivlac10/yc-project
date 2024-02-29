var express = require('express');
var router = express.Router();
const Mysql = require('../Mysql/mysql')
const redis = require('../Redis/index')
const auth = require('../middleware/auth')
const Time = require('../utils/Date')
const RKEY = require('../RKEY')
const Utils = require('../utils/utils')
const icepay = require('./send_order_icepay')
const user_withdraw_verify = require('./user_withdraw_verify')
const user_withdraw_rule = require('./user_withdraw_rule')
const common = require('../utils/common')

// 提现状态
// 0  提现下单成功
// 1  提现成功
// 2 提现失败
// 3 人工审核
// 4 成功后失败
// 5 拒绝提现
// 6 下单失败

const withdraw_conf = {
	1: icepay,
}

// 用户余额提现下单接口
router.post('/api/user_money_withdraw_func', auth, async (req, res, next) => {
	let data = {
		code: 0,
		msg: ''
	}
	try {
		let money = req.body.money.replace(/\s+/g, '') || '0'  // 金额
		let name = req.body.name || ''  // 用户姓名
		let cpf = req.body.imps_account.replace(/\s+/g, '') || ''  // 用户CPF 税号
		let pix = req.body.ifsc || 0 // 用户提现类型 0 Gcash  1 paymaya
		let pix_num = cpf
		let phone = req.body.phone || '0'  // 用户手机
		let email = req.body.email || '' // 用户邮箱
		let money_type = req.body.money_type || '0'  // 提现类型 0余额 1佣金
		money_type = String(money_type)
		money = parseFloat(req.body.money);  // 转换成浮点数
		let pay_data = await get_conf_pay(money)
		if (!pay_data) {
			data['code'] = 28  // 支付不存在或禁用
			return res.send(data)
		}
		let pay_id = pay_data['pay_id']
		let user = await user_withdraw_verify.user_info_verify(req.uid, money, money_type, req.realIp, cpf)  // 验证用户身份及金额
		if (user['code'] !== 1) {
			data['code'] = user['code'];
			data['msg'] = user['msg'];
			if (user['code'] === 100) {
				data['msg'] = user['msg'];
			}
			return res.send(data)
		}

		let game_rule = await user_withdraw_rule.user_withdraw_rule_verify(user, String(cpf), parseFloat(money), req.realIp, money_type)
		if (game_rule.code == 101) {
			data.code = 1;
			return res.send(data)
		}
		if (game_rule.code == 88) {
			data.code = 88;
			return res.send(data)
		}
		if (game_rule.code !== 1) {
			if (game_rule.code == 88) {
				data.code = 0;
				data.msg = game_rule.msg;
				return res.send(data)
			}
			data.code = game_rule.code;
			return res.send(data)
		}
		const util = new Utils()
		const order_number = util.add_order_number();
		let day = Time.get_today_ymd()
		let user_day = Time.formatDateHms(user['add_time']).slice(0, 10);
		let new_user_flag = (day === user_day) ? 0 : 1;
		const flag = (await redis.hget('san_game_all_conf', 'auto_withdraw_flag')) || 1;  // 自动提现开关
		const auto_withdraw_min = (await redis.hget('san_game_all_conf', 'auto_min_withdraw_money')) || 100;  // 自动提现金额

		let status = null // --------

		// if (parseInt(flag) === 1 && parseFloat(auto_withdraw_min) >= parseFloat(money) && money_type === "0" ||
		// 	(money_type === "1" && parseFloat(money) <= 100 && parseInt(user.with_num) < 3)) {
		const user_pay_data = {
			money: money,
			name: name,
			account: cpf,
			ifsc: pix,
			money_type: money_type
		};
		if (parseInt(flag) === 1 && parseFloat(auto_withdraw_min) >= parseFloat(money) && money_type === "0") {
			console.log("自动审核");
			if (money_type === "0") {
				update_user_info(user, parseFloat(money));
			}
			if (money_type === "1") {
				update_user_commission(user, parseFloat(money));
			}
			const w_data = await withdraw_conf[pay_id].http_post_withdraw_data(user_pay_data, order_number, money, pay_data, user.vip_lv);
			if (w_data.code === 1) {
				// common.auto_withdraw_notice(user.uid, money);
				status = 0;
				data.msg = "Submetido com sucesso!";
				data.code = 1;
			} else {
				if (money_type === "0") {
					add_withdraw_user_info(user, parseFloat(money));  // 下单失败退回余额
				}
				if (money_type === "1") {
					add_withdraw_user_commission(user, parseFloat(money));
				}
				// send_user_email(user.uid, w_data.msg);
				status = 6;
				data.msg = w_data.msg;
			}
			add_user_withdraw_log(req.realIp, user, parseFloat(money), order_number, order_number, name,
				pix_num, pix, cpf, new_user_flag,
				status, pay_id, w_data, pay_data, user.audit_remark, money_type);
		} else {
			console.log("人工审核");
			status = 3;
			if (money_type === "0") {
				update_user_info(user, parseFloat(money));
			}
			if (money_type === "1") {
				update_user_commission(user, parseFloat(money));
			}
			let maps = '';
			const res = await add_user_withdraw_log(req.realIp, user, parseFloat(money), order_number, order_number, name,
				pix_num, pix, cpf, new_user_flag,
				status, pay_id, maps, pay_data, user.audit_remark, money_type);
			if (res > 0) {
				if (money_type === "0") {
					common.withdraw_notice(user, parseFloat(money), user_pay_data);
				}
				if (money_type === "1") {
					common.commission_withdraw_notice(user, parseFloat(money), user_pay_data);
				}
			}
			data.code = 1;
			data.msg = "Submetido com sucesso!";
			data.order_num = order_number;
		}

		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 根据支付权重返回下单支付
const get_conf_pay = async (money) => {
	let pay = await redis.get(RKEY.SAN_GAME_NEW_WITHDRAW_CONF)  // set_redis文件
	if (!pay) {
		return null;
	}
	pay = JSON.parse(pay);
	if (pay.length === 0) {
		return null;
	}
	let arr = [];
	let total_v = 0;
	let vs = [];
	for (let i = 0; i < pay.length; i++) {
		let p = pay[i];
		if (p.min_transfer_money <= money && p.max_transfer_money >= money) {
			arr.push(p);
			total_v += p.withdraw_index;
			vs.push(total_v);
		}
	}
	if (arr.length === 0) {
		return null;
	}
	if (total_v === 0) {
		return arr[0];
	}
	let r = Math.floor(Math.random() * total_v);
	for (let i = 0; i < vs.length; i++) {
		if (r < vs[i]) {
			return arr[i];
		}
	}
	return arr[0];
}


// 更新用户信息
const update_user_info = (user, money) => {
	user_withdraw_verify.update_user_money(user.uid, money, 0);  // 更新余额
	const after_money = parseFloat(user.money) - money;
	common.user_money_log_func(user.uid, money, user.money, after_money, 1);  // 余额变动记录
}

// 更新用户佣金信息
const update_user_commission = (user, money) => {
	user_withdraw_verify.update_user_commission(user.uid, money, 0);  // 更新佣金
	const after_money = parseFloat(user.commission) - money;
	common.user_commission_log_func(user.uid, money, user.commission, after_money, 100);  // 佣金变动记录
	common.user_brokerage_log_func(user.uid, 0, 0, money, 5);  // 佣金经纪记录
}

// 更新用户信息（提现）
const add_withdraw_user_info = (user, money) => {
	user_withdraw_verify.update_user_money(user.uid, money, 1);  // 更新余额
	const beforeMoney = parseFloat(user.money) - money;
	common.user_money_log_func(user.uid, money, beforeMoney, user.money, 17);  // 余额变动记录
}

// 返回佣金
const add_withdraw_user_commission = (user, money) => {
	user_withdraw_verify.update_user_commission(user.uid, money, 1);  // 更新佣金
	let before_money = parseFloat(user.commission) - money;
	common.user_commission_log_func(user.uid, money, before_money, user.commission, 101);  // 佣金变动记录
	common.user_brokerage_log_func(user.uid, 0, 0, money, 6);
}

// 提现失败，发送通知
const send_user_email = async (uid, content) => {
	const info = "Withdraw fail : " + content;
	const title = 'Withdraw fail';
	const sql = "insert into san_user_message(uid, title, content, add_time) values (?, ?, ?, now())";
	const mysql = new Mysql();
	const res = await mysql.awaitSql(sql, [uid, title, info]);
	return res
}

// 添加用户提现记录
const add_user_withdraw_log = async (ip, user, money, order_number, pay_order_number, collection_name,
	pix_num, pix, cpf, new_user_flag, status, pay_id,
	return_data, pay, audit_remark, money_type, is_int = 0) => {
	const fee = user.vip_lv.pay_fee;
	let fee_ratio = (100 - parseFloat(fee)) / 100;
	if (fee_ratio < 0) {
		fee_ratio = 0;
	}
	const send_money = is_int === 0 ? parseFloat(money) * fee_ratio : Math.round(parseFloat(money) * fee_ratio);
	const rate = parseFloat(money) - send_money;
	const pay_fee = parseFloat(money) * parseFloat(pay.withdraw_ratio) / 100;

	const sql = "insert into san_withdraw_list(uid, cid, order_number, pay_order_number, money, user_ip, collection_name, " +
		"pix_num, pix, cpf, rate, send_money, " +
		"new_user_flag, status, pay_id, err_msg, send_data, pay_fee, audit_remark, money_type, add_time) " +
		"values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, now())";

	const params = [user.uid, user.cid, order_number, pay_order_number, money, ip, collection_name,
		pix_num, pix, cpf, rate, send_money, new_user_flag, status,
		pay_id, JSON.stringify(return_data), JSON.stringify(return_data), pay_fee, audit_remark, money_type];
	const mysql = new Mysql();
	const res = await mysql.awaitSql(sql, params);
	return res
}

module.exports = router;