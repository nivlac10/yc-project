var express = require('express');
var router = express.Router();
const Mysql = require('../Mysql/mysql')
const redis = require('../Redis/index')
const auth = require('../middleware/auth')
const Time = require('../utils/Date')
const RKEY = require('../RKEY')
const Common = require('../utils/common')


// 用户充值记录
router.post('/api/get_user_order_list', auth, async (req, res, next) => {
	let data = {
		code: 0,
		data: [],
		count: 0,
	}
	try {
		let start_date = req.body.start_date
		let end_date = req.body.end_date
		let page = req.body.page || 1
		let limit = req.body.limit || 20
		let offset = (parseInt(page) - 1) * parseInt(limit)
		if (req.uid == 0) {
			data['code'] = 1
			return res.send(data)
		}
		var sql = `select order_number, money, status, add_time, first_pay from san_order_list where uid = '${req.uid}'`;
		var sql2 = `select count(*) count from san_order_list where uid = '${req.uid}'`;
		if (start_date) {
			sql += ` and add_time >= '${start_date}'`;
			sql2 += ` and add_time >= '${start_date}'`;
		}
		if (end_date) {
			end_date = `${end_date} 24:00:00`;
			sql += ` and add_time <= '${end_date}'`;
			sql2 += ` and add_time <= '${end_date}'`;
		}
		sql += ` order by add_time desc limit ${offset}, ${limit}`;

		const mysql = new Mysql()
		const resSql = await mysql.getAll(sql, [])
		const cont = await mysql.getOne(sql2, [])
		if (resSql) {
			for (var i = 0; i < resSql.length; i++) {
				resSql[i]['add_time'] = Time.formatDate(resSql[i]['add_time'])
				resSql[i]['total_money'] = resSql[i]['money'].toString()
				if (parseInt(resSql[i]['first_pay']) === 1) {
					resSql[i]['total_money'] = parseFloat(resSql[i]['money']) + (parseFloat(resSql[i]['money']) * Common.USER_FIRST_RECHARGE_RATE);
				}
				if (parseInt(resSql[i]['first_pay']) === 2) {
					resSql[i]['total_money'] = parseFloat(resSql[i]['money']) + (parseFloat(resSql[i]['money']) * Common.USER_DAY_FIRST_RECHARGE_RATE);
				}
			}
			data['count'] = cont['count'];
			data['data'] = resSql;
		}
		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
});

// 用户提现记录
router.post('/api/get_user_order_withdraw_list', auth, async (req, res, next) => {
	let data = {
		code: 0,
		data: [],
		count: 0,
	}
	try {
		let start_date = req.body.start_date
		let end_date = req.body.end_date
		let page = req.body.page || 1
		let limit = req.body.limit || 20
		let offset = (parseInt(page) - 1) * parseInt(limit)
		if (req.uid == 0) {
			data['code'] = 1
			return res.send(data)
		}
		var sql = `select order_number, money, status, add_time, rate from san_withdraw_list where uid = '${req.uid}'`
		var sql2 = `select count(*) count from san_withdraw_list where uid = '${req.uid}'`
		if (start_date) {
			sql += ` and add_time >= '${start_date}'`
			sql2 += ` and add_time >= '${start_date}'`
		}
		if (end_date) {
			end_date = `${end_date} 24:00:00`
			sql += ` and add_time <= '${end_date}'`
			sql2 += ` and add_time <= '${end_date}'`
		}
		sql += ` order by add_time desc limit ${offset}, ${limit}`

		const mysql = new Mysql()
		const resSql = await mysql.getAll(sql, [])
		const cont = await mysql.getOne(sql2, [])
		if (resSql) {
			for (var i = 0; i < resSql.length; i++) {
				resSql[i]['add_time'] = Time.formatDate(resSql[i]['add_time'])
				if (resSql[i]['status'] === 5) {
					resSql[i]['status'] = 1;
				}
				if (resSql[i]['status'] === 3) {
					resSql[i]['status'] = 0;
				}
				if (![0, 1].includes(resSql[i]['status'])) {
					resSql[i]['status'] = 2;
				}
			}
			data['count'] = cont['count'];
			data['data'] = resSql;
		}
		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
});

module.exports = router;