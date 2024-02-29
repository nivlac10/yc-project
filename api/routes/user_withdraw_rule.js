const Time = require('../utils/Date')
const redis = require('../Redis/index')
const Mysql = require('../Mysql/mysql')
const RKEY = require('../RKEY')
const common = require('../utils/common')

class user_withdraw_rule {
	static async user_withdraw_rule_verify(user, account, money, ip, money_type) {
		var data = {};
		data['code'] = 0; // 0 未通过 1 通过用户验证
		data['msg'] = 'error';
		var min_withdraw_money = (await redis.hget('san_game_all_conf', 'min_withdraw_money')) || '0';
		let info = "";

		if (parseFloat(money) < parseFloat(min_withdraw_money)) {
			data['code'] = 21;
			info = '用户提现申请金额' + money + '小于设置最小提现金额' + min_withdraw_money;
			common.add_user_withdraw_log(user['uid'], info, ip);
			return data;
		}
		var user_data = await this.get_user_black_log(user['uid'], 0);
		let black_flag = false
		if (user_data) {
			black_flag = true
			info = "当前用户为黑名单";
		}
		user_data = await this.get_user_black_log(user['uid'], 1);
		if (user_data) {
			black_flag = true
			info = "当前用户为黑名单";
		}
		if (user['parent_id'] != '0') {
			user_data = await this.get_user_black_log(user['parent_id'], 1)
			if (user_data) {
				black_flag = true
				info = "当前用户团队中黑名单黑名单id:" + user['parent_id'];
			}
		}
		if (user['super_id'] != '0') {
			user_data = await this.get_user_black_log(user['super_id'], 1)
			if (user_data) {
				black_flag = true
				info = "当前用户团队中黑名单黑名单id:" + user['super_id'];
			}
		}
		if (user['super_parent_id'] != '0') {
			user_data = await this.get_user_black_log(user['super_parent_id'], 1)
			if (user_data) {
				black_flag = true
				info = "当前用户团队中黑名单黑名单id:" + user['super_parent_id'];
			}
		}
		if (black_flag) {
			data['code'] = 101;
			common.add_user_withdraw_log(user['uid'], info, ip);
			this.black_user_func(user['uid'], money, ip, money_type);
			return data;
		}
		var use_account = await this.get_now_account_user(account)

		if (use_account) {
			if (parseInt(use_account['uid']) !== parseInt(user['uid'])) {
				data['code'] = 88;
				data['msg'] = 'The current withdrawal account has been used by others';
				info = "提现账户税号已被使用";
				common.add_user_withdraw_log(user['uid'], info, ip);
				return data;
			}
		}

		data['code'] = 1;
		return data;
	}

	// 黑名单用户提现直接扣除余额
	static async black_user_func(uid, money, ip, money_type) {
		let money_key = ["money", "commission"]
		if (parseFloat(money) > 0) {
			var sql = `update san_users set ${money_key[money_type]} =  ${money_key[money_type]} -  ${money} where uid = "${uid}" `;
			var mysql = new Mysql();
			console.log(`黑名单用户直接扣除${money_key[money_type]}:  `, sql);
			var res = await mysql.awaitSql(sql, null);
			if (res > 0) {
				var info = `黑名单用户直接扣除${money_key[money_type]}:  ` + money;
				common.add_user_withdraw_log(uid, info, ip);
			}
		}
	}

	// 查询当前账号
	static async get_now_account_user(account) {
		var sql = "select * from san_withdraw_list where status = 1 and cpf = '" + account + "' limit 1";
		var mysql = new Mysql()
		var res = await mysql.getOne(sql, null)
		return res;
	}

	// 获取异常用户
	static async get_user_black_log(uid, type) {
		var sql = "select * from san_user_black_log where uid = ?";
		var mysql = new Mysql()
		var res = await mysql.getOne(sql, [uid, type])
		return res;
	}
}


module.exports = user_withdraw_rule