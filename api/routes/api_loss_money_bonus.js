var express = require('express');
var router = express.Router();
const Mysql = require('../Mysql/mysql')
const redis = require('../Redis/index')
const auth = require('../middleware/auth')
const Time = require('../utils/Date')
const RKEY = require('../RKEY')
const { loss_money_list, user_day_data_total, user_money_log_func } = require('../utils/common')
const UserDataUtil = require('../utils/userDataUtil')

router.post('/api/get_loss_money_bouns_list', auth, async (req, res, next) => {
	const data = {
		code: 0,
		data: [],
		loss_money: 0,
		bonus: 0,
		state: 0
	}
	try {
		if (req.uid != 0) await get_user_yesterday_loss_money(req.uid, data)
		if (data.bonus > 0) {
			let day = Time.get_today_ymd()
			let user_key = "loss_bonus_log_" + day
			data.state = 1
			if (await redis.hget(user_key, req.uid.toString())) data.state = 2
		}
		data.data = loss_money_list
		data.code = 1
		res.send(data);
	} catch (error) {
		console.log(error);
	}
});

router.post('/api/receive_loss_bonus', auth, async (req, res, next) => {
	const data = {
		code: 0,
		state: 0,
		money: 0,
	}
	try {
		if (req.uid == 0) {
			data.code = 3  // 用户未登录 或者用户token失效
			return res.send(data)
		}
		let day = Time.get_today_ymd()
		let user_key = "loss_bonus_log_" + day
		if (await redis.hget(user_key, req.uid.toString())) {
			data.code = 38  // 已领取过奖励
			return res.send(data)
		}

		let user_receive_state = await get_user_receive_log(req.uid, day)
		if (user_receive_state) {
			data.code = 38  // 已领取过奖励
			return res.send(data)
		}

		let yesterday_data = {}
		await get_user_yesterday_loss_money(req.uid, yesterday_data)
		if (yesterday_data.bonus == 0) {
			data.code = 39  // 领取条件未达标
			return res.send(data)
		}

		let user = await UserDataUtil.get_user_by_uid(req.uid)
		await user_receive_loss_bonus(user, day, yesterday_data)
		data.money = yesterday_data['bonus']
		data.code = 1
		data.state = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
});

router.post('/api/get_loss_receive_record', auth, async (req, res, next) => {
	const data = {
		code: 0,
		data: [],
		bonus: 0,
		count: 0,
	}
	try {
		let page = req.body.page || 1;
		let limit = req.body.limit || 10;
		let offset = (parseInt(page, 10) - 1) * parseInt(limit, 10);
		const mysql = new Mysql()
		if (req.uid == 0) {
			data['code'] = 3  // 用户未登录 或者用户token失效
			return res.send(data)
		}
		const resSql = await mysql.getAll("select uid,add_time,give_money from san_user_loss_money_bonus_log where uid = ? order by add_time desc limit  ?, ?",
			[req.uid, parseInt(offset), parseInt(limit)])

		const count = await mysql.getOne("select count(*) count, sum(give_money) bonus from san_user_loss_money_bonus_log where uid = ?", [req.uid])
		if (resSql) {
			data['bonus'] = count['bonus']
			data['count'] = count['count']
			for (let i = 0; i < resSql.length; i++) {
				const element = resSql[i];
				element['add_time'] = Time.formatDate(element['add_time'])
			}
			data['data'] = resSql
		}
		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
});

// 用户领取奖励
const user_receive_loss_bonus = async (user, day, yesterday_data) => {
	try {
		let money = yesterday_data['bonus']
		// 计算所需打码量
		let rate = await redis.hget(RKEY.SAN_GAME_ALL_CONF, "gift_code_rate") || 10
		let code_amount = parseFloat(money) * parseFloat(rate)
		var remain_code_amount;
		if (parseFloat(user['remain_code_amount']) <= 0) {
			remain_code_amount = code_amount;
		} else {
			remain_code_amount = parseFloat(user['remain_code_amount']) + code_amount;
			remain_code_amount = Math.round(remain_code_amount * 100) / 100; // 保留两位小数
		}
		var need_code_amount;
		if (parseFloat(user['remain_code_amount']) <= 0) {
			need_code_amount = code_amount;
		} else {
			need_code_amount = parseFloat(user['need_code_amount']) + parseFloat(code_amount);
		}
		var after_money = (parseFloat(user['money']) + parseFloat(money)).toFixed(2);

		const mysql = new Mysql()
		mysql.sql("update san_users set money = money + ?, loss_bonus = loss_bonus + ?, give_money = give_money + ?" +
			", remain_code_amount =  ?, need_code_amount =  ? where uid = ?",
			[money, money, money, remain_code_amount, need_code_amount, user['uid']])

		let user_key = "loss_bonus_log_" + day
		redis.hset(user_key, user['uid'], '1')
		redis.expire(user_key, 86400)

		// 用户日汇总
		user_day_data_total(user.uid, day, { give_money: money, loss_bonus: money });
		// 日总汇总
		// common.day_money_total(user.cid, day, { loss_bonus: money });
		// 余额日志
		user_money_log_func(user.uid, money, parseFloat(user.money), after_money, 22);
		add_loss_bonus_log(user.uid, day, yesterday_data);
	} catch (error) {
		console.log(error);
	}
}

// 添加日志
const add_loss_bonus_log = async (uid, day, yesterday_data) => {
	try {
		const mysql = new Mysql()
		await mysql.sql("insert into san_user_loss_money_bonus_log  (uid, day, loss_money,give_money, add_time)values (?,?,?, ?, NOW())",
			[uid, day, yesterday_data['loss_money'], yesterday_data['bonus']]
		)
	} catch (error) {
		console.log(error);
	}
}

// 获取可领取状态
const get_user_yesterday_loss_money = async (uid, data) => {
	data.bonus = 0
	data.loss_money = 0
	let yesterday = Time.get_yesterday()
	try {
		const mysql = new Mysql()
		const resSql = await mysql.getOne("select uid,total_real_win from san_user_team_day_report where day = ? and  uid = ?", [yesterday, uid])
		if (resSql) {
			data.loss_money = resSql.total_real_win
			if (data.loss_money < 0) {
				for (let i = 0; i < loss_money_list.length; i++) {
					const element = loss_money_list[i];
					if (data.loss_money <= element.loss_money) {
						data.bonus = element.bonus
					}
				}
			}
		}
	} catch (error) {
		console.log(error);
	}
}

// 查询用户是否有记录
const get_user_receive_log = async (uid, day) => {
	try {
		const mysql = new Mysql()
		const resSql = await mysql.getOne("select * from san_user_loss_money_bonus_log where day = ? and uid = ?", [day, uid])
		let user_key = "loss_bonus_log_" + day
		if (resSql) {
			await redis.hset(user_key, uid.toString(), '1')
			await redis.expire(user_key, 86400)
		}
		return resSql
	} catch (error) {
		console.log(error);
	}
}

module.exports = router;