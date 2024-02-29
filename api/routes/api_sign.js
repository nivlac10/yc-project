var express = require('express');
var router = express.Router();
const Mysql = require('../Mysql/mysql')
const redis = require('../Redis/index')
const auth = require('../middleware/auth')
const Time = require('../utils/Date')
const RKEY = require('../RKEY')
const UserDataUtil = require('../utils/userDataUtil')
const common = require('../utils/common')

const vip_day_sing_key = "user_vip_day_sing_state_"

router.post('/api/get_sign_list', auth, async (req, res, next) => {
	let data = {}
	data['code'] = 0
	data['money'] = 0
	data['state'] = 1
	let vip_lv = 0
	try {
		// let arr = []
		// let sign_day = await redis.get("user_sign_day_" + req.uid.toString()) || 0
		// data.sign_day = sign_day
		const uid = req.uid
		const day = Time.get_today_ymd()
		const sing_state = await redis.hget(vip_day_sing_key + String(day), String(uid))
		if (sing_state) {
			data['state'] = 0
		}
		if (uid != 0) {
			const user = await UserDataUtil.get_user_by_uid(uid)

			vip_lv = user['vip_lv']
		}
		let vip_conf = await get_vip_lv_list_data()
		if (vip_conf) {
			data['money'] = vip_conf[vip_lv]['day_bonus']
		}
		data['code'] = 1
	} catch (error) {
		console.log(error);
	}
	return res.send(data);
});

// 用户领取签到奖励
router.post('/api/receive_sign_bonus', auth, async (req, res, next) => {
	const data = {
		code: 0,
		state: 0,
		money: 0,
	}
	let vip_lv = 0
	try {

		const uid = req.uid
		if (uid == 0) {
			data['code'] = 3  // 用户未登录 或者用户token失效
			return res.send(data)
		}
		const day = Time.get_today_ymd()
		const sing_state = await redis.hget(vip_day_sing_key + String(day), String(uid))
		if (sing_state) {
			data['code'] = 36
			return res.send(data)
		}
		const user = await UserDataUtil.get_user_by_uid(uid)
		if (user) {
			vip_lv = user['vip_lv']
		}
		let vip_conf = await get_vip_lv_list_data()
		if (vip_conf) {
			let money = vip_conf[vip_lv]['day_bonus']
			let sign_day = (await redis.get("user_sign_day_" + req.uid.toString()))
			sign_day = sign_day ? sign_day : 0
			sign_day = parseInt(sign_day) + 1
			data['money'] = money
			redis.hset(vip_day_sing_key + String(day), String(uid), '1')
			redis.expire(vip_day_sing_key + String(day), 86400 * 2)
			user_receive_bonus(uid, money, day, sign_day)
		}
		data['code'] = 1
		data['state'] = 1
		res.send(data);
	} catch (error) {
		console.log(error);
	}
});

const user_receive_bonus = async (uid, money, day, sign_day) => {
	try {
		let user = await UserDataUtil.get_user_by_uid(uid)
		let after_money = parseFloat(user['money']) + parseFloat(money);
		// 计算所需打码量
		let rate =  10
		let code_amount = parseFloat(money) * parseFloat(rate);
		let remain_code_amount = (parseFloat(user['remain_code_amount']) <= 0) ?
			code_amount :
			parseFloat(user['remain_code_amount']) + parseFloat(code_amount);
		let need_code_amount = (parseFloat(user['remain_code_amount']) <= 0) ?
			code_amount :
			parseFloat(user['need_code_amount']) + parseFloat(code_amount);
		// 修改用户信息
		const mysql = new Mysql()
		const resSql = await mysql.awaitSql("update san_users set money = money + ?, sign_bonus = sign_bonus + ?, give_money = give_money + ?" +
			", remain_code_amount = ?, need_code_amount = ? where uid = ?", [money, money, money, remain_code_amount, need_code_amount, user['uid']])
		if (resSql) {
			var out_time;
			if (sign_day !== 30) {
				out_time = Time.get_rest_time() + 86400;
			} else {
				out_time = Time.get_rest_time();
			}
			redis.setex("user_sign_day_" + uid.toString(), out_time, sign_day.toString());
		}
		await common.user_day_data_total(uid, day.toString(), { give_money: money, sign_bonus: money });
		await common.user_money_log_func(uid, money, parseFloat(user['money']), after_money, 20);
		add_sing_log(uid, money, day.toString(), sign_day);

	} catch (error) {
		console.log(error);
	}
}

const add_sing_log = (uid, money, day, sign_day) => {
	try {
		const mysql = new Mysql()
		const resSql = mysql.sql('insert into san_user_sign_log (uid,day, money,continue_day, add_time) values (?, ?, ?,?, NOW())', [uid, day, money, sign_day])
	} catch (error) {
		console.log(error);
	}
}
// # 获取vip等级数据
async function get_vip_lv_list_data() {
	let vip_lv_list = await redis.get(RKEY.SAN_GAME_VIP_LV_LIST)
	let vip_list_data = []
	if (vip_lv_list) {
		vip_list_data = JSON.parse(vip_lv_list);
	}
	return vip_list_data
}
module.exports = router;