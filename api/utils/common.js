/*
 * @Author: wawodel 69891926+wawodel@users.noreply.github.com
 * @Date: 2023-12-01 15:13:21
 * @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 * @LastEditTime: 2023-12-20 17:56:12
 * @FilePath: \Node-admin\app\utils\common.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */

const Mysql = require('../Mysql/mysql');
const redis = require('../Redis/index');
const RKEY = require('../RKEY');
const axios = require('axios');
const Time = require('./Date');
// # 金额变动类型
MONEY_TYPE_CONF = {
	'0': {
		'code': '0',
		'name': '充值',
		'type': 0
	},
	'1': {
		'code': '1',
		'name': '提现',
		'type': 0
	},
	'2': {
		'code': '2',
		'name': '周VIP',
		'type': 0
	},
	'3': {
		'code': '3',
		'name': '月VIP',
		'type': 0
	},
	'4': {
		'code': '4',
		'name': 'VIP晋级',
		'type': 0
	},
	'5': {
		'code': '5',
		'name': '充值活动赠送',
		'type': 0
	},
	'6': {
		'code': '6',
		'name': '新用户日首充',
		'type': 0
	},
	'7': {
		'code': '7',
		'name': 'slot返水',
		'type': 0
	},
	'8': {
		'code': '8',
		'name': 'live返水',
		'type': 0
	},
	'9': {
		'code': '9',
		'name': '佣金转入',
		'type': 0
	},
	'10': {
		'code': '10',
		'name': 'table返水',
		'type': 0
	},
	'11': {
		'code': '11',
		'name': 'fish返水',
		'type': 0
	},
	'12': {
		'code': '12',
		'name': '系统赠送',
		'type': 0
	},
	'13': {
		'code': '13',
		'name': '平台转出',
		'type': 0
	},
	'14': {
		'code': '14',
		'name': '平台转入',
		'type': 0
	},
	'17': {
		'code': '17',
		'name': '提现返还',
		'type': 0
	},
	'18': {
		'code': '18',
		'name': '充值活动',
		'type': 0
	},
	'19': {
		'code': '19',
		'name': 'fast返水',
		'type': 0
	},
	'20': {
		'code': '20',
		'name': '日签到',
		'type': 0
	},
	'21': {
		'code': '21',
		'name': '用户日打码任务',
		'type': 0
	},
	'22': {
		'code': '22',
		'name': '用户破产补助',
		'type': 0
	},
	'23': {
		'code': '23',
		'name': '用户领取code码',
		'type': 0
	},
	'24': {
		'code': '24',
		'name': 'vip立反奖励',
		'type': 0
	},
	'25': {
		'code': '25',
		'name': 'vip日反水',
		'type': 0
	},
	'26': {
		'code': '26',
		'name': 'vip每周反水',
		'type': 0
	},
	'27': {
		'code': '27',
		'name': 'vip每月反水',
		'type': 0
	},
	'28': {
		'code': '28',
		'name': 'vip拆分反水',
		'type': 0
	},
	'29': {
		'code': '29',
		'name': '每日免费转轮赠送',
		'type': 0
	},
	'30': {
		'code': '30',
		'name': '下载APK',
		'type': 0
	},
	'31': {
		'code': '31',
		'name': '仲夏节每日大放送(德州)',
		'type': 0
	},
	'32': {
		'code': '32',
		'name': '总胜多少局和连胜奖励(德州)',
		'type': 0
	},
	'33': {
		'code': '33',
		'name': '皇家礼包(德州)',
		'type': 0
	},
	'34': {
		'code': '34',
		'name': '皇家同花顺奖励',
		'type': 0
	},
	'35': {
		'code': '35',
		'name': '抽到888和8888，666和6666，777和7777(德州)',
		'type': 0
	},
	'36': {
		'code': '36',
		'name': '竞标赛获胜(德州)',
		'type': 0
	},
	'37': {
		'code': '37',
		'name': '竞标赛入场费(德州)',
		'type': 0
	},
	'38': {
		'code': '38',
		'name': '俱乐部门票(德州)',
		'type': 0
	},
	'39': {
		'code': '39',
		'name': '邮箱发放(德州)',
		'type': 0
	},
	'40': {
		'code': '40',
		'name': '救济金(德州)',
		'type': 0
	},
	'41': {
		'code': '41',
		'name': '俱乐部转账(德州)',
		'type': 0
	},
	'42': {
		'code': '42',
		'name': '发送大喇叭(德州)',
		'type': 0
	},
	'43': {
		'code': '43',
		'name': '充值成就奖励',
		'type': 0
	},
	'44': {
		'code': '44',
		'name': '任务刷新(德州)',
		'type': 0
	},
	// # 佣金变动
	'100': {
		'code': '100',
		'name': '佣金提现',
		'type': 1
	},
	'101': {
		'code': '101',
		'name': '佣金提现返还',
		'type': 1
	},
	'102': {
		'code': '102',
		'name': '佣金转出',
		'type': 1
	},
	'103': {
		'code': '103',
		'name': '一级打码返佣',
		'type': 1
	},
	'104': {
		'code': '104',
		'name': '二级打码返佣',
		'type': 1
	},
	'105': {
		'code': '105',
		'name': '三级打码返佣',
		'type': 1
	},
	'106': {
		'code': '106',
		'name': '直属首充佣金',
		'type': 1
	},
	'107': {
		'code': '107',
		'name': '邀请任务佣金',
		'type': 1
	},
}


class common {
	constructor() {
	}
	static USER_FIRST_RECHARGE_RATE = 0.2  // 用户首充赠送倍率
	static USER_DAY_FIRST_RECHARGE_RATE = 0.1  // 用户每日首充赠送倍率
	static loss_money_list = [
		{
			"loss_money": -100,
			"bonus": 2,
		},
		{
			"loss_money": -200,
			"bonus": 4,
		}, {
			"loss_money": -500,
			"bonus": 10,
		}, {
			"loss_money": -1000,
			"bonus": 20
		}, {
			"loss_money": -2000,
			"bonus": 40,
		}, {
			"loss_money": -3000,
			"bonus": 60,
		}, {
			"loss_money": -5000,
			"bonus": 100,
		}, {
			"loss_money": -10000,
			"bonus": 200,
		}, {
			"loss_money": -20000,
			"bonus": 400,
		}, {
			"loss_money": -50000,
			"bonus": 1000,
		}, {
			"loss_money": -100000,
			"bonus": 2000,
		},
	]
	// # 获取用户当前vip等级
	static async get_recharge_money_vip(total_bet) {
		const nowVipConf = {
			vip_lv: 0,
			vip_low_lv: 0
		};

		const vipConfStr = JSON.parse(await redis.get("san_vip_low_vip_list")) || "";
		const vipConf = vipConfStr ? vipConfStr : [];

		try {
			for (let d = 0; d < vipConf.length; d++) {
				if (parseFloat(total_bet) >= parseFloat(vipConf[d].need_code_amount)) {
					nowVipConf.vip_lv = vipConf[d].vip_lv;
					nowVipConf.vip_low_lv = vipConf[d].lv;
					continue;
				}
				// break;  // 如果取消注释这一行，则第一次满足条件后就会跳出循环
			}
		} catch (e) {
			console.error(e);
		}
		return nowVipConf

	}
	// 验证用户 VIP
	static async verify_user_vip_lv(user) {
		const totalBet = user.total_bet;
		const vipLv = user.vip_lv;
		const vipLowLv = user.vip_low_lv;
		const nowVipLv = await this.get_recharge_money_vip(totalBet);
		if (parseFloat(nowVipLv.vip_lv) > parseFloat(vipLv) || parseFloat(nowVipLv.vip_low_lv) > parseFloat(vipLowLv)) {
			// 调用更新用户 VIP 等级的方法
			this.update_user_vip_lv(user.uid, nowVipLv);
			user.vip_lv = nowVipLv.vip_lv;
			user.vip_low_lv = nowVipLv.vip_low_lv;
		}
	}
	// # 更新用户vip
	static async update_user_vip_lv(uid, vip_lv) {
		try {
			let mysql = new Mysql(this.app);
			const res = await mysql.awaitSql("update san_users set vip_lv = ? , vip_low_lv = ? where uid = ?", [vip_lv['vip_lv'], vip_lv['vip_low_lv'], uid]);
			return res;
		} catch (error) {
			console.error('查询执行错误:', error);
			throw error;
		}
	}

	/**
* 更新老客登陆大厅数据
* @param {Object} user - 用户对象
* @param {string} now_day - 当前日期
*/
	static async update_old_user_life(user, now_day) {
		try {
			const old_user_life_key = 'old_user_life_day_flag_' + now_day;
			if (await redis.hget(old_user_life_key, String(user['uid']))) {
				return;
			}
			const old_user_life_login_key = 'old_user_life_login_key_' + now_day;
			redis.hincrby(old_user_life_login_key, String(user['cid']), 1);
			redis.expire(old_user_life_login_key, 86400 * 3);
			redis.hset(old_user_life_key, String(user['uid']), '1');
			redis.expire(old_user_life_key, 86400 * 7);
		} catch (e) {
			console.error(e);
		}
	}

	/**
	 * 用户余额变动记录
	 * @param {number} uid - 用户ID
	 * @param {number} money - 变动的金额
	 * @param {number} before_money - 变动前的金额
	 * @param {number} after_money - 变动后的金额
	 * @param {number} money_type - 金额类型
	 * @returns {Object} - 数据库插入结果
	 */
	static async user_money_log_func(uid, money, before_money, after_money, money_type) {
		try {
			const mysql = new Mysql();
			const res = await mysql.awaitSql(
				"insert into san_user_money_log(uid, money, before_money, after_money, money_type, add_time) values (?, ?, ?, ?, ?, now())",
				[uid, money, before_money, after_money, money_type]
			);
			// console.log('res', res);
			return res;
		} catch (error) {
			console.error('用户余额变动记录出错:', error);
			throw error;
		}
	}

	/**
* 用户每日数据汇总
* @param {number} uid - 用户ID
* @param {string} day - 日期
* @param {Object} kwargs - 其他汇总数据，以属性名和值的形式传递
*/
	static user_day_data_total(uid, day, data) {
		if (!data || Object.keys(data).length === 0) {
			return;
		}
		const mysql = new Mysql();
		let sql = "INSERT INTO san_user_team_day_report(uid, day, ";
		const columns = [];
		const values = [];

		for (const key in data) {
			sql += key + ",";
			columns.push(key);
			values.push(data[key]);
		}

		sql = sql.slice(0, -1) + ") VALUES (" + '"' + uid + '"' + ',"' + day + '",';
		sql += values.map(value => '"' + value + '"').join(',') + ") ON DUPLICATE KEY UPDATE ";

		for (let i = 0; i < columns.length; i++) {
			sql += columns[i] + '=' + columns[i] + '+' + values[i] + ',';
		}

		sql = sql.slice(0, -1);
		// console.log(sql);
		try {
			mysql.sql(sql, null);
		} catch (error) {
			console.log(error);
		}
	}

	/**
	 * 用户每日数据汇总
	 * @param {number} cid - 公司ID
	 * @param {string} day - 日期
	 * @param {Object} data - 其他汇总数据，以属性名和值的形式传递
	 */
	static day_money_total(cid, day, data) {
		if (!data || Object.keys(data).length === 0) {
			return;
		}
		const mysql = new Mysql();
		let sql = "INSERT INTO san_day_money_total(cid, day, ";
		const columns = [];
		const values = [];

		for (const key in data) {
			sql += key + ",";
			columns.push(key);
			values.push(data[key]);
		}

		sql = sql.slice(0, -1) + ") VALUES (" + '"' + cid + '"' + ',"' + day + '",';
		sql += values.map(value => '"' + value + '"').join(',') + ") ON DUPLICATE KEY UPDATE ";

		for (let i = 0; i < columns.length; i++) {
			sql += columns[i] + '=' + columns[i] + '+' + values[i] + ',';
		}

		sql = sql.slice(0, -1);
		// console.log(sql);
		try {
			mysql.sql(sql, null);
		} catch (error) {
			console.log(error);
		}
	}


	// 获取邀请人数
	static async get_invite_number(uid) {
		const mysql = new Mysql()
		const res = await mysql.getOne('select count(*) count from san_user_activity_total_data where parent_id = ? and bet_num >= 5 and total_money >= 100', [uid])
		return res.count ? res.count : 0
	}

	// 获取可领取任务奖励列表
	static async get_invite_data(uid, num) {
		let INVITE_TASK_CONF = JSON.parse(await redis.get(RKEY.SAN_USER_INVITE_TASK)) ? JSON.parse(await redis.get(RKEY.SAN_USER_INVITE_TASK)) : []
		let res = []
		let task_state_list = await common.get_all_task_state(uid)
		let over_task_list = []
		for (let i = 0; i < task_state_list.length; i++) {
			const element = task_state_list[i];
			over_task_list.push(element.task_id)
		}
		for (let item = 0; item < INVITE_TASK_CONF.length; item++) {
			const data = {
				state: 0,
				num: INVITE_TASK_CONF[item]['num'],
				money: INVITE_TASK_CONF[item]['money'],
				task_id: INVITE_TASK_CONF[item]['task_id'],
				invite_num: num,
			}
			if (num >= data['num']) {
				data['state'] = 1
				data['invite_num'] = INVITE_TASK_CONF[item]['num']
				if (over_task_list.includes(INVITE_TASK_CONF[item]['task_id'])) data['state'] = 2
			}
			res.push(data)
		}
		return res
	}

	static async get_all_task_state(uid) {
		let arr = []
		const mysql = new Mysql()
		const res = mysql.getAll("select task_id from san_user_invite_task_log where uid = ?", [uid])
		if (res) arr = res
		return arr
	}
	// 用户佣金变动记录
	static async user_commission_log_func(uid, commission, before_commission, after_commission, commission_type) {
		let sql = "insert into san_user_money_log(uid, money, before_money, after_money, money_type, log_type, add_time) values (?, ?, ?, ?, ?, 1, Now())"
		const mysql = new Mysql()
		let res = await mysql.awaitSql(sql, [uid, commission, before_commission, after_commission, commission_type])
		return res
	}

	// # 佣金记录
	static async user_brokerage_log_func(uid, game_id, lv_num, money, money_type) {
		let sql = "insert into san_user_day_brokerage (uid, day, lv_num, game_uid, game_bet, money, status, add_time,update_time, money_type) values (?, NOW(), ?, ?, ?,?,?, NOW(), NOW(),?)"
		const mysql = new Mysql()
		let res = await mysql.awaitSql(sql, [uid, lv_num, game_id, 0, money, 1, money_type])
		return res
	}

	// 添加用户提现异常
	static add_user_withdraw_log(uid, info, ip) {
		const mysql = new Mysql()
		const sql = "insert into san_user_unusual_log(uid, ip, info, add_time) values (?, ?, ?, now())"
		mysql.sql(sql, [uid, ip, info])
	}


	// 提现审核播报
	static async withdraw_notice(user, money, user_pay_data) {
		try {
			let txt = '🔔🔔🔔\n提现审核提醒\n平台:' + await redis.hget(RKEY.SAN_GAME_ALL_CONF, 'platform_title') +
				'\n提现类型:余额' +
				'\n提现姓名:' + String(user_pay_data['name']) +
				'\n卡号:' + String(user_pay_data['account']) +
				'\nifsc:' + String(user_pay_data['ifsc']) +
				'\n用户UID:' + String(user['uid']) +
				'\n今日提现成功次数:' + String(user['with_num']) +
				'\n提现金额' + String(money) +
				'\n用户充提差' + String(parseFloat(user['total_money'] - user['total_withdraw'], 2))
			this.send_telegram(txt)
		} catch (error) {
			console.log(error);
		}
	}
	// 佣金提现审核播报
	static async commission_withdraw_notice(user, money, user_pay_data) {
		try {

			let txt = '🔔🔔🔔\n提现审核提醒\n平台:' + await redis.hget(RKEY.SAN_GAME_ALL_CONF, 'platform_title') +
				'\n提现类型:佣金' +
				'\n提现姓名:' + String(user_pay_data['name']) +
				'\n卡号:' + String(user_pay_data['account']) +
				'\nifsc:' + String(user_pay_data['ifsc']) +
				'\n用户UID:' + String(user['uid']) +
				'\n今日提现成功次数:' + String(user['with_num']) +
				'\n提现金额' + String(money) +
				'\n用户充提差' + String(parseFloat(user['total_money'] - user['total_withdraw']))
			this.send_telegram(txt)
		} catch (error) {
			console.log(error);
		}
	}

	// 发送TG机器人消息
	static async send_telegram(message) {
		const CHAT_ID = await redis.hget(RKEY.SAN_GAME_ALL_CONF, 'platform_telegram_chat_id')
		const BOT_TOKEN = await redis.hget(RKEY.SAN_GAME_ALL_CONF, 'platform_telegram_bot_token')
		const apiUrl = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
		let body = {
			chat_id: CHAT_ID,
			text: message,
		}
		try {
			const response = await axios.post(apiUrl, body);

			// const data = await response.json();
			// console.log('Telegram API response:', data);
		} catch (error) {
			// console.error('Error sending message to Telegram:', error.message);
		}
	}

	// 直属上级获取下级首充佣金奖励
	static async recharge_give_parent_money(parent_id, uid) {
		let user = await this.get_user_by_uid(parent_id);
		let USER_PARENT_COMMISSION = (await redis.hget(RKEY.SAN_GAME_ALL_CONF, 'invit_recharge_gift')) || 10;
		let give_money = USER_PARENT_COMMISSION;

		if (user === null) {
			console.log("parent is None");
			return;
		}

		let day = Time.get_today_ymd();

		// 添加团队日汇总
		let sql = `insert into san_user_team_day_report (day, uid, team_recharge_brokerage)
               values ('${day}', '${user.uid}', '${give_money}')
               ON DUPLICATE KEY UPDATE team_recharge_brokerage = team_recharge_brokerage + '${give_money}'`;

		// 更新用户佣金信息 （佣金余额， 总佣金， 邀请充值佣金）
		let sql2 = `update san_users set commission = commission + '${give_money}', total_commission = total_commission + '${give_money}', 
                share_recharge_brokerage = share_recharge_brokerage + '${give_money}', share_valid_number = share_valid_number + 1 
                where uid = '${user.uid}'`;

		let sql3 = `insert into san_user_day_brokerage (uid, day, lv_num, game_uid, game_bet, money, status, add_time,
                update_time, money_type) values ('${parent_id}', NOW(), '1', '${uid}', '0', '${give_money}', '1', NOW(), NOW(), '3')`;

		let mysql = new Mysql();
		// let res = mysql.insertOne(sql, null);  // 添加团队日汇总
		// let res2 = mysql.update(sql2, null);  // 更新用户佣金信息 （佣金余额， 总佣金， 邀请充值佣金）
		// let res3 = mysql.insertOne(sql3, [parent_id, '1', uid, '0', give_money, '1', '3']);
		let res2 = mysql.affairs([sql, sql2, sql3]);

		let after_commission = parseFloat(user.commission) + parseFloat(give_money);
		this.user_commission_log_func(user.uid, give_money, user.commission, after_commission, 106);  // 变动日志
	}


	// 用户佣金变动记录
	static async user_commission_log_func(uid, commission, before_commission, after_commission, commission_type) {
		let sql = `insert into san_user_money_log(uid, money, before_money, after_money, money_type, log_type, add_time) 
               values ('${uid}', '${commission}', '${before_commission}', '${after_commission}', '${commission_type}', 1, Now())`;

		let mysql = new Mysql();
		let res = await mysql.awaitSql(sql, null);

		return res;
	}
	// 查询
	static async get_order_info(order_number) {
		let sql = "select * from san_order_list where pay_order_number = ?"
		let mysql = new Mysql();
		let res = await mysql.getOne(sql, [order_number]);
		return res;
	}
	static async get_user_by_uid(uid) {
		try {
			const mysql = new Mysql()
			const res = await mysql.getOne("select * from  san_users where uid = ?", [uid]);
			return res;
		} catch (error) {
			console.error('查询执行错误:', error);
			throw error;
		}
	}
}


module.exports = common;