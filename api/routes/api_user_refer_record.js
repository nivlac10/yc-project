var express = require('express');
var router = express.Router();
const Mysql = require('../Mysql/mysql')
const redis = require('../Redis/index')
const auth = require('../middleware/auth')
const Time = require('../utils/Date')
const RKEY = require('../RKEY')

// 用户查询团队列表
router.post('/api/get_member_list', auth, async (req, res, next) => {
	let data = {
		code: 0,
		data: [],
		count: 0
	}
	try {
		let page = req.body.page || 1
		let limit = req.body.limit || 10
		let offset = (parseInt(page) - 1) * parseInt(limit)
		let level = parseInt(req.body.level) || 0
		let nickname = req.body.nickname || ''
		if (req.uid == 0) {
			data['code'] = 1
			return res.send(data)
		}
		if (level > 3 || level < 0) {
			data['code'] = 28
			return res.send(data)
		}

		let sql = "select nickname,uid,parent_id,super_id,super_parent_id,add_time,team_one_user_num," +
			"bet_parent_brokerage,bet_super_brokerage,bet_parent_super_brokerage,recharge_parent_brokerage from " +
			"san_users where 1 = 1"
		let sql2 = "select count(*) count from san_users where 1 = 1"
		if (level == 1) {
			sql += ` and parent_id = '${req.uid}'`;
			sql2 += ` and parent_id = '${req.uid}'`;
		} else if (level == 2) {
			sql += ` and super_id = '${req.uid}'`;
			sql2 += ` and super_id = '${req.uid}'`;
		} else if (level == 3) {
			sql += ` and super_parent_id = '${req.uid}'`;
			sql2 += ` and super_parent_id = '${req.uid}'`;
		} else {
			sql += ` and (parent_id = '${req.uid}' or super_id = '${req.uid}' or super_parent_id = '${req.uid}')`;
			sql2 += ` and (parent_id = '${req.uid}' or super_id = '${req.uid}' or super_parent_id = '${req.uid}')`;
		}
		if (nickname.length > 0) {
			sql += ` and uid = '${nickname}'`;
			sql2 += ` and uid = '${nickname}'`;
		}
		sql += ` order by add_time desc limit ${offset}, ${limit}`;
		const mysql = new Mysql()
		resSql = await mysql.getAll(sql, [])
		cont = await mysql.getOne(sql2, [])
		if (resSql) {
			for (var i = 0; i < resSql.length; i++) {
				if (String(resSql[i]['parent_id']) === String(req.uid)) {
					resSql[i]['level'] = 1;
					resSql[i]['commission'] = Math.round(parseFloat(resSql[i]['recharge_parent_brokerage']) + parseFloat(resSql[i]['bet_parent_brokerage']) * 100) / 100;
				}

				if (String(resSql[i]['super_id']) === String(req.uid)) {
					resSql[i]['level'] = 2;
					resSql[i]['commission'] = Math.round(parseFloat(resSql[i]['bet_super_brokerage']) * 100) / 100;
				}

				if (String(resSql[i]['super_parent_id']) === String(req.uid)) {
					resSql[i]['level'] = 3;
					resSql[i]['commission'] = Math.round(parseFloat(resSql[i]['bet_parent_super_brokerage']) * 100) / 100;
				}

				resSql[i]['add_time'] = resSql[i]['add_time'].toString();
				delete resSql[i]['parent_id'];
				delete resSql[i]['super_id'];
				delete resSql[i]['super_parent_id'];
				delete resSql[i]['bet_parent_brokerage'];
				delete resSql[i]['recharge_parent_brokerage'];
				delete resSql[i]['bet_super_brokerage'];
				delete resSql[i]['bet_parent_super_brokerage'];
			}
			// console.log(resSql);
			data['count'] = cont['count'];
			data['data'] = resSql;
		}
		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
});

// 获取团队列表数据
router.post('/api/get_user_team_list', auth, async (req, res, next) => {
	const data = {
		code: 0,
		data: [],
		invite_task_brokerage: 0,
		recharge_brokerage: 0,
		total_person_num: 0,
		total_recharge_money: 0,
		total_first_recharge_num: 0,
		total_bet: 0,
		total_brokerage: 0,
	}
	try {
		let start_date = req.body.start_date
		let end_date = req.body.end_date
		if (req.uid == 0) {
			data['code'] = 1;
			for (var d = 0; d < 3; d++) {
				var _data = {};
				_data['person_num'] = 0;
				_data['recharge_money'] = 0;
				_data['first_recharge_num'] = 0;
				_data['bet'] = 0;
				_data['brokerage'] = 0;
				data['data'].push(_data);
			}
			return res.send(data)
		}
		let sql = "select SUM(team_one_user_num) one_num,SUM(team_two_user_num) two_num, " +
			"SUM(team_three_user_num) three_num,sum(team_one_recharge) one_recharge," +
			"sum(team_two_recharge) two_recharge,sum(team_three_recharge) three_recharge," +
			"sum(team_one_bet) one_bet,sum(team_two_bet) two_bet, sum(team_three_bet) three_bet," +
			"sum(team_one_bet_brokerage) one_bet_brokerage,sum(team_two_bet_brokerage) two_bet_brokerage," +
			"sum(team_three_bet_brokerage) three_bet_brokerage,sum(team_recharge_brokerage) team_recharge_brokerage," +
			"sum(team_invite_task_brokerage)  team_invite_task_brokerage " +
			"from san_user_team_day_report where uid=? "

		var param = [req.uid];
		if (start_date) {
			param.push(start_date);
			sql += " and day >= ?";
		}
		if (end_date) {
			end_date = end_date + ' 24:00:00';
			param.push(end_date);
			sql += " and day < ?";
		}

		const mysql = new Mysql()
		const resSql = await mysql.getOne(sql, param)
		data['code'] = 1
		if (resSql) {
			var level_one_data = {};
			level_one_data['person_num'] = parseInt(resSql['one_num']) || 0;
			level_one_data['recharge_money'] = Math.round(parseFloat(resSql['one_recharge']) * 100) / 100 || 0.00;
			level_one_data['bet'] = Math.round(parseFloat(resSql['one_bet']) * 100) / 100 || 0.00;
			level_one_data['brokerage'] = Math.round(parseFloat(resSql['one_bet_brokerage']) * 100) / 100 || 0.00;
			data['data'].push(level_one_data);

			var level_two_data = {};
			level_two_data['person_num'] = parseInt(resSql['two_num']) || 0;
			level_two_data['recharge_money'] = Math.round(parseFloat(resSql['two_recharge']) * 100) / 100 || 0.00;
			level_two_data['bet'] = Math.round(parseFloat(resSql['two_bet']) * 100) / 100 || 0.00;
			level_two_data['brokerage'] = Math.round(parseFloat(resSql['two_bet_brokerage']) * 100) / 100 || 0.00;
			data['data'].push(level_two_data);

			var level_three_data = {};
			level_three_data['person_num'] = parseInt(resSql['three_num']) || 0;
			level_three_data['recharge_money'] = Math.round(parseFloat(resSql['three_recharge']) * 100) / 100 || 0;
			level_three_data['bet'] = Math.round(parseFloat(resSql['three_bet']) * 100) / 100 || 0.00;
			level_three_data['brokerage'] = Math.round(parseFloat(resSql['three_bet_brokerage']) * 100) / 100 || 0.00;
			data['data'].push(level_three_data);

			data['invite_task_brokerage'] = Math.round(parseFloat(resSql['team_invite_task_brokerage']) * 100) / 100 || 0.00;
			data['recharge_brokerage'] = Math.round(parseFloat(resSql['team_recharge_brokerage']) * 100) / 100 || 0.00;

			for (var i = 0; i < data['data'].length; i++) {
				data['total_person_num'] += data['data'][i]['person_num'];
				data['total_recharge_money'] += data['data'][i]['recharge_money'];
				data['total_bet'] += data['data'][i]['bet'];
				data['total_brokerage'] += data['data'][i]['brokerage'];
			}
		}

		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 获取下级数据状态
router.post('/api/get_user_lower_data', auth, async (req, res, next) => {
	const data = {
		code: 0,
		data: [],
		count: 0,
	}
	try {
		let page = req.body.page || 1
		let limit = req.body.limit || 10
		let offset = (parseInt(page) - 1) * parseInt(limit)
		if (req.uid == 0) {
			data['code'] = 1
			return res.send(data)
		}
		let sql = "select uid, add_time, total_money, header_img from san_users where" +
			" parent_id = ? order by add_time DESC limit ?, ?"
		let sql2 = "select count(*) count from san_users where parent_id = ? "
		const mysql = new Mysql()
		const resSql = await mysql.getAll(sql, [req.uid, offset, limit])
		const count = await mysql.getOne(sql2, [req.uid])
		if (resSql) {
			data['count'] = count['count'];
			for (var i = 0; i < resSql.length; i++) {
				resSql[i]['add_time'] = Time.formatDate(resSql[i]['add_time'])
				resSql[i]['is_recharge'] = resSql[i]['total_money'] > 0 ? 1 : 0;
				delete resSql[i]['total_money'];
			}
		}
		data['data'] = resSql
		data['code'] = 1

		res.send(data)
	} catch (error) {
		console.log(error);
	}
});

// 获取邀请总值
router.post('/api/get_invite_total_data', auth, async (req, res, next) => {
	const data = {
		code: 0,
		data: 0,
	}
	try {
		let get_invite_total_data = await redis.get("get_invite_total_data")
		if (get_invite_total_data) {
			data['code'] = 1
			data['data'] = JSON.parse(get_invite_total_data)
			return res.send(data)
		}
		let sql = "select sum(invite_task_brokerage) task_bonus, sum(one_bet_brokerage + two_bet_brokerage" +
			" + three_bet_brokerage)  bet_bonus, sum(phone_num + email_num + face_num) user_num" +
			"  from san_day_money_total";
		const mysql = new Mysql()
		const resSql = await mysql.getOne(sql, [])
		if (resSql) {
			resSql['task_bonus'] = parseFloat(resSql['task_bonus']);
			resSql['bet_bonus'] = parseFloat(resSql['bet_bonus']);
			resSql['user_num'] = parseFloat(resSql['user_num']);
			data['data'] = resSql;
			redis.set("get_invite_total_data", JSON.stringify(resSql), "ex", 60 * 10);
		}
		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
});

module.exports = router;