var express = require('express');
var router = express.Router();
const Mysql = require('../Mysql/mysql')
const redis = require('../Redis/index')
const auth = require('../middleware/auth')
const Time = require('../utils/Date')
const RKEY = require('../RKEY')
const { loss_money_list, get_invite_number, get_invite_data, user_day_data_total, day_money_total, user_money_log_func } = require('../utils/common');
const UserDataUtil = require('../utils/userDataUtil');

// 获取大厅列表
router.post('/api/get_game_list', async (req, res, next) => {
	let game_version = req.body.game_data_version || 0
	let data = {
		code: 0,
		game_type: [],
		factory_list: [],
		game_list: [],
		hot_list: [],
		game_data_version: 0,
	}
	try {
		let game_redis_version = await redis.get(RKEY.GAME_DATA_VERSION)
		if (!game_version) {
			game_redis_version = '1'
			redis.set(RKEY.GAME_DATA_VERSION, game_redis_version.toString())
		}
		if (game_version.toString() != game_redis_version.toString()) {
			if (await redis.get(RKEY.SAN_EXTERNAL_GAME_LIST))
				//  游戏列表
				data.game_list = JSON.parse(await redis.get(RKEY.SAN_EXTERNAL_GAME_LIST))
			if (await redis.get(RKEY.SAN_GAME_FACTORY_LIST))
				//  厂商列表
				data.factory_list = JSON.parse(await redis.get(RKEY.SAN_GAME_FACTORY_LIST))
			// 热门游戏列表
			// data['hot_list'] = json.loads(redis.get(RKEY.SAN_GAME_HOT_GAME_LIST))
		}
		data.game_data_version = game_redis_version
		data.code = 1
		res.send(data);
	} catch (error) {
		console.log(error);
	}
});

// 奖金柜获取状态
router.post('/api/get_bonus_cabinet_state', auth, async (req, res, next) => {
	const mysql = new Mysql()
	const data = {
		code: 0,
		data: {
			sign_bonus_state: 0, // 充值
			loss_bonus_state: 0, // 不可领取
			refer_bonus_state: 0,
			roller_bonus_state: 1,
			de_zhou_bonus_state: 0
		}
	}
	try {
		// 今日签到状态
		let day = Time.get_today_ymd()
		const sql = await mysql.getOne("select id,money from san_user_sign_log where uid = ? and day = ?", [req.uid, day])
		let receive_state_key = "sign_receive_state_key_" + day
		let sign_state_day = await redis.hget(receive_state_key, req.uid)

		if (sign_state_day) data.data.sign_bonus_state = 1  // 可领取
		if (sql) data.data.sign_bonus_state = 2  // 已领取

		// 补给箱状态
		let loss_bonus = await get_user_yesterday_loss_money(req.uid)
		if (loss_bonus > 0) {
			let user_key = "loss_bonus_log_" + day
			data.data.loss_bonus_state = 1  // 可领取
			if (await redis.hget(user_key, req.uid.toString())) {
				data.data.loss_bonus_state = 2  // 已领取
			}
		}

		// 邀请任务佣金
		num = req.uid != 0 ? await get_invite_number(req.uid) : 0
		let arr = get_invite_data(req.uid, num)
		for (let i = 0; i < arr.length; i++) {
			const element = arr[i];
			if (element.state == 1) {
				return data.data.refer_bonus_state = 1
			}
		}

		// 转盘状态
		let roller_user_key = "user_receive_roller_money_" + day
		if (await redis.hget(roller_user_key, req.uid)) data.data.roller_bonus_state = 0

		data.code = 1
		res.send(data);
	} catch (error) {
		console.log(error);
	}
});
// 下载奖励
router.post('/api/apk_download_bonus', auth, async (req, res, next) => {
	const mysql = new Mysql()
	const data = {
		code: 0,
		data: {
			code: 0, // 充值
			money: 0, // 不可领取
			state: 0,
		}
	}
	const money = 5
	try {
		const uid = req.uid
		if (uid == 0) {
			data.code = 2
			return res.send(data)
		}
		let loading = await redis.get("api_loading_" + String(uid))
		if (loading) {
			data.code = 40
			return res.send(data)
		}
		redis.setex("api_loading_" + String(uid), 30, "1")
		const user = await UserDataUtil.get_user_by_uid(uid)
		if (user['download_bonus'] > 0) {
			data['code'] = 38
			return res.send(data)
		}
		// 今日签到状态
		let day = Time.get_today_ymd()
		const sql = await mysql.awaitSql("insert into san_user_download_bonus_log (uid, cid, money, add_time) values (?, ?,?,NOW())", [uid, user['cid'], money])
		if (sql) {
			const rate = 10
			let after_money = parseFloat(user['money']) + parseFloat(money);
			// 计算所需打码量
			let code_amount = parseFloat(money) * parseFloat(rate);
			let remain_code_amount = (parseFloat(user['remain_code_amount']) <= 0) ?
				code_amount :
				(parseFloat(user['remain_code_amount']) + parseFloat(code_amount));
			let need_code_amount = (parseFloat(user['remain_code_amount']) <= 0) ?
				code_amount :
				parseFloat(user['need_code_amount']) + parseFloat(code_amount);
			let sql2 = "update san_users set money = money + ?, download_bonus = download_bonus + ?, give_money = give_money + ?, remain_code_amount =  ?, need_code_amount =  ? where uid = ?"
			mysql.sql(sql2, [money, money, money, remain_code_amount, need_code_amount, user['uid']])
			user_day_data_total(user['uid'], day, { give_money: money, download_bonus: money })
			day_money_total(user['cid'], day, { download_bonus: money })
			user_money_log_func(user['uid'], money, user['money'], after_money, 30)
			data['money'] = money
		} else {
			return res.send(data);
		}
		data.code = 1
	} catch (error) {
		console.log(error);
	}
	res.send(data);
});
// 补给箱获取可领取状态
const get_user_yesterday_loss_money = async (uid) => {
	const mysql = new Mysql()
	try {
		let bonus = 0
		let yesterday = Time.get_yesterday()
		const res = await mysql.getOne("select uid,total_real_win from san_user_team_day_report where day = ? and  uid = ?", [yesterday, uid])
		if (res) {
			let loss_money = res.total_real_win
			if (loss_money < 0) {
				for (let i = 0; i < loss_money_list.length; i++) {
					const element = loss_money_list[i];
					if (loss_money <= i['loss_money']) bonus = element['bonus']
				}
			}
		}
		return bonus

	} catch (error) {

	}
}


module.exports = router;