// userDataUtil.js
const Mysql = require('../Mysql/mysql')
const Time = require('./Date');
const Common = require('./common');
const Utils = require('./utils');
const redis = require('../Redis/index')
const game_util = require('./game_util');
class UserDataUtil {
	constructor() {

	}

	/**
	 * 根据用户ID获取用户信息
	 * @param {number} uid - 用户ID
	 * @returns {Promise<object|null>} 用户信息或null
	 */
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

	/**
* 根据用户phone获取用户信息
* @param {number} phone - 用户手机号
* @returns {Promise<object|null>} 用户信息或null
*/
	static async get_user_by_phone(phone) {
		try {
			const mysql = new Mysql()
			const res = await mysql.getOne("select * from  san_users where phone = ?", [phone]);
			return res;
		} catch (error) {
			console.error('查询执行错误:', error);
			throw error;
		}
	}
	
	/**
* 根据用户aaid获取用户信息
* @param {string} aaid - 用户手机号
* @returns {Promise<object|null>} 用户信息或null
*/
static async get_user_by_aaid(aaid) {
	try {
		const mysql = new Mysql()
		const res = await mysql.getOne("select * from  san_users where aaid = ?", [aaid]);
		return res;
	} catch (error) {
		console.error('查询执行错误:', error);
		throw error;
	}
}
	/**
* 根据用户cpf获取用户信息
* @param {number} cpf - 用户cpf
* @returns {Promise<object|null>} 用户信息或null
*/
	static async get_user_by_cpf(cpf, uid) {
		try {
			const mysql = new Mysql()
			const res = await mysql.getOne("select * from  san_users where CPF = ? and uid != ?", [cpf, uid]);
			return res;
		} catch (error) {
			console.error('查询执行错误:', error);
			throw error;
		}
	}

	/**
* 根据用户email获取用户信息
* @param {string} email - 用户邮箱
* @returns {Promise<object|null>} 用户信息或null
*/
	static async get_user_by_email(email) {
		try {
			const mysql = new Mysql()
			const res = await mysql.getOne("select * from  san_users where email = ?", [email]);
			return res;
		} catch (error) {
			console.error('查询执行错误:', error);
			throw error;
		}
	}
	/**
* 根据用户face_id获取用户信息
* @param {string} face_id - 用户face_id
* @returns {Promise<object|null>} 用户信息或null
*/
	static async get_user_by_facebook(face_id) {
		try {
			const mysql = new Mysql()
			const res = await mysql.getOne("select * from  san_users where face_id = ?", [face_id]);
			return res;
		} catch (error) {
			console.error('查询执行错误:', error);
			throw error;
		}
	}

	/**
* 用户活跃留存统计
* @param {Object} user - 用户对象
*/
	static async user_keep_func(user) {
		// if (user['user_type'] === 0) {
		// 	return;
		// }
		this.login_user_first_pay(user);  // 首次充值用户活跃验证
		let user_day = Time.formatDateHms(user['add_time']).slice(0, 10);
		const now_day = Time.formatDate(new Date());
		const user_day_key = 'user_keep_log_' + now_day;
		if (user_day != now_day) {
			Common.update_old_user_life(user, now_day);  // 老客日活统计
		}
		const dateObject = new Date(user_day);
		const re_int = Time.day_int(user_day);
		const login_int = Time.day_int(now_day);
		const space_time = login_int - re_int;
		if (space_time > 86400 * 29) {
			return;
		}
		if (await redis.hget(user_day_key, String(user['uid']))) {
			return;
		}
		const day_num = parseInt(space_time / 86400);
		const maps = {};
		maps['uid'] = user['uid'];
		maps['cid'] = user['cid'];
		maps['time'] = Time.formatDateHms((user['add_time']));
		maps['day'] = now_day;
		maps['user_flag'] = day_num === 0 ? 1 : 0;  // 新用户标识
		maps['day_num'] = day_num + 1;  // 用户留存天数
		redis.rpush('user_login_data_list', JSON.stringify(maps), (err, result) => {
			if (err) {
				console.error('推入元素失败', err);
				return;
			}
			console.log('推入元素成功', result);
		});
		redis.hset(user_day_key, String(user['uid']), '1');
		redis.expire(user_day_key, 86400 * 2);
	}

	/**
	 * 首次充值用户活跃标识
	 * @param {Object} user - 用户对象
	 */
	static async login_user_first_pay(user) {
		try {
			if (user['is_first_pay'] === 0) {  // 非首日充值用户
				return;
			}
			const userDay = String(user['add_time']).slice(0, 10);
			const nowDay = String(new Date().toISOString().slice(0, 10));
			const userFlag = 'user_first_recharge_flag_' + nowDay;  // 今日首次充值用户活跃标识
			const res = await redis.hget(userFlag, String(user['uid']));
			if (res) {  // 用户活跃已标识
				return;
			}
			const userTimestamp = new Date(userDay).getTime() / 1000;
			const loginTimestamp = new Date(nowDay).getTime() / 1000;
			const spaceTime = loginTimestamp - userTimestamp;
			const dayNum = Math.floor(spaceTime / 86400);
			const maps = {
				cid: user['cid'],
				day: userDay,
				day_num: dayNum + 1
			};
			redis.rpush('user_first_recharge_data_list', JSON.stringify(maps));
			redis.hset(userFlag, String(user['uid']), '1');
			redis.expire(userFlag, 86400 * 2);
		} catch (error) {
			console.error(error);
		}
	}
	/**
	* 根据IP获取用户数
	* @param {string} ip - 用户注册IP
	* @returns {number} - 用户数
	*/
	static async get_user_ip_num(ip) {
		let num = 0;
		try {
			const mysql = new Mysql()
			const res = await mysql.getAll("select count(*) count from san_users where register_ip = ?", [ip]);
			if (res) {
				num = res[0]['count']
			}
			return num;
		} catch (error) {
			console.error('查询执行错误:', error);
			throw error;
		}
	}

	/**
	 * 查询外接游戏信息
	 * @param {number} gid - 游戏ID
	 * @returns {object} - 游戏信息
	 */
	static async get_wj_game(gid) {
		try {
			const mysql = new Mysql();
			const res = await mysql.getOne("select * from san_external_game_list where gid = ?", [gid]);
			return res;
		} catch (error) {
			console.error('查询执行错误:', error);
			throw error;
		}
	}

	/**
			* 生成储存的用户密码
			* @param {string} phone - 用户手机号
			* @param {string} password - 用户密码
			* @returns {string} - 生成的储存密码
			*/
	static add_storage_pass(phone, password) {
		const utils = new Utils()
		let md_str = utils.md5(String(phone)) + utils.md5(String(password));
		let s_str = utils.md5(md_str.split('').sort().join('')).split('').sort().join('');
		return s_str;
	}

	/**
* 生成储存的用户密码
* @param {string} phone - 用户手机号
* @param {string} password - 用户密码
* @returns {string} - 储存的用户密码
*/
	static addStoragePass(phone, password) {
		const utils = new Utils()
		const mdStr = utils.md5(String(phone)) + utils.md5(password);
		const sStr = utils.md5(mdStr.split('').sort().join('')).split('').sort().join('');
		return sStr;
	}


	/**
	 * 返回用户新token
	 * @param {number} uid - 用户ID
	 * @param {number} ip - 用户Ip
	 * @returns {string} - 生成的用户新token
	 */
	static async return_user_login_token(uid, ip) {
		try {
			const utils = new Utils()
			const msStr = utils.random_str(8);
			const token = utils.md5(this.addStoragePass(msStr, Time.formatDate(new Date())));

			const tokenKey = `user_login_token_${token}`;
			const onlyKey = `only_user_${uid}`;

			const lastToken = await redis.get(onlyKey);

			if (lastToken) {
				redis.del(`user_login_token_${lastToken}`);
			}

			redis.setex(tokenKey, 86400 * 3, String(uid));
			redis.setex(onlyKey, 86400 * 3, token);

			this.update_user_new_token(uid, token, ip);

			return token;
		} catch (error) {
			console.error('生成用户新token出错:', error);
			throw error;
		}
	}
	/**
	 * 更新用户的登录token
	 * @param {number} uid - 用户ID
	 * @param {string} token - 新生成的用户登录token
	 *  @param {number} ip - 用户Ip
	 * @returns {Object} - 数据库更新结果
	 */
	static async update_user_new_token(uid, token, ip) {
		try {
			const mysql = new Mysql()
			mysql.sql(`update san_users set user_token = "${token}", login_time = now(), login_ip ="${ip}"  where uid = "${uid}"`, null)
		}
		catch (error) {
			console.error('查询执行错误:', error);
			throw error;
		}
	}

	/**
* 用户日活数据
* @param {number} cid - 公司ID
* @param {number} flag - 标识
* @param {number} uid - 用户ID
* @param {number} num - 数量，默认为1.0
*/
	static user_add_hour_func(cid, flag, uid, num = 1.0) {
		const flagList = ['t', 'v', 'b', 'r', 'm', 'a', 'o'];
		const day = new Date().toISOString().slice(0, 10);
		const hour = new Date().getHours();
		const data = {
			cid: cid,
			uid: uid,
			day: day,
			hour: hour,
			key_str: flagList[flag] + hour,
			num: num
		};
		const redisKey = "user_hour_data";
		redis.rpush(redisKey, JSON.stringify(data));
	}

	// 更新用户日数据统计
	/**
	 * @param {string} cid - 公司 ID
	 * @param {number} flag - 标志位，用于选择统计类型
	 * Flag Values:
	 *   0: Temporary user count
	 *   1: Phone number count
	 *   2: Face recognition count
	 */
	static async update_user_day_num_data(cid, flag) {
		const flagList = ["tem_num", "phone_num", "face_num"];
		const keyStr = flagList[flag];
		const day = new Date().toISOString().split('T')[0];
		const redisTotalKey = `${day}_san_game_register_${keyStr}`;
		redis.hincrby(redisTotalKey, String(cid), 1);
		redis.expire(redisTotalKey, 86400 * 3);
	}

	/**
* 更新用户团队信息
* @param {Object} share_data 分享数据
*/
	static update_user_team_data(share_data) {
		// console.log('更新用户团队信息',share_data);
		if (!share_data) {
			return;
		}
		this.update_user_team_level_data(share_data.uid, 0);
		this.update_user_agent_data(share_data.uid, 0);

		if (share_data.parent_id != '0') {
			this.update_user_team_level_data(share_data.parent_id, 1);
			this.update_user_agent_data(share_data.parent_id, 1);
		}

		if (share_data.super_id != '0') {
			this.update_user_team_level_data(share_data.super_id, 2);
			this.update_user_agent_data(share_data.super_id, 2);
		}
	}

	/**
	 * 更新代理数据
	 * @param {Number} uid 用户ID
	 * @param {Number} lv 级别
	 */
	static update_user_agent_data(uid, lv) {
		try {
			let day = Time.formatDate(new Date());
			let arr = ['team_one_user_num', 'team_two_user_num', 'team_three_user_num'];
			const mysql = new Mysql()
			mysql.sql(`INSERT INTO san_user_team_day_report(day, uid, ${arr[lv]}) VALUES ("${day}", "${uid}", 1) ON DUPLICATE KEY UPDATE ${arr[lv]} = ${arr[lv]} + 1`);
			// console.log('更新代理数据',`INSERT INTO san_user_team_day_report(day, uid, ${arr[lv]}) VALUES ("${day}", "${uid}", 1) ON DUPLICATE KEY UPDATE ${arr[lv]} = ${arr[lv]} + 1`);
			console.log('更新代理数据', `用户id:${uid} 等级 ${arr[lv]}`);
		} catch (error) {
			console.error('更新执行错误:', error);
			throw error;
		}
	}

	/**
	 * 更新团队不同级数的人数
	 * @param {Number} uid 用户ID
	 * @param {Number} lv 级别          
	 */
	static async update_user_team_level_data(uid, lv) {
		let arr = ['team_one_user_num', 'team_two_user_num', 'team_three_user_num'];
		const mysql = new Mysql()
		try {
			let sql = '';
			if (lv <= 2) {
				sql = `UPDATE san_users SET team_user_num = team_user_num + 1, ${arr[lv]} = ${arr[lv]} + 1 WHERE uid = "${uid}"`;
			} else {
				sql = `UPDATE san_users SET team_user_num = team_user_num + 1 WHERE uid = "${uid}"`;
			}
			mysql.sql(sql);
		} catch (error) {
			console.error('更新执行错误:', error);
			throw error;
		}
	}

	/**
* 获取邀请人数据
* @param {Number} uid 用户ID
* @param {Number} lv 级别
*/
	static async get_user_parent_id(uid) {
		if (!uid && Number(uid) == 0) {
			return null;
		}
		// 根据用户ID获取用户信息
		let user = await this.get_user_by_uid(uid);

		// 如果用户信息为空，则返回
		if (user === null) {
			return null;
		}

		return user
	}

	/**
* 用户日活数据
* @param {number} cid - 公司ID
* @param {number} flag - 标志位
* @param {number} uid - 用户ID
* @param {number} [num=1.0] - 数量，默认为1.0
*/
	static async user_add_hour_func(cid, flag, uid, num = 1.0) {
		const flag_list = ['t', 'v', 'b', 'r', 'm', 'a', 'o'];
		const day = new Date().toISOString().split('T')[0];
		const hour = new Date().getHours();
		const data = {
			cid,
			uid,
			day,
			hour,
			key_str: flag_list[flag] + hour.toString(),
			num,
		};

		const redis_key = "user_hour_data";
		redis.rpush(redis_key, JSON.stringify(data));
	}

	/**
	 * FB事件上报
	 * @param {object} user - 用户信息对象
	 * @param {number} money - 金额
	 * @param {string} type - 事件类型
	 */
	static fb_usgin_event_func(user, money, type) {
		const r_key = "fb_api_using_event_list";
		const data = {
			username: user.username,
			phone: user.phone,
			email: user.email,
			cid: user.cid,
			type,
			money,
			time: Math.floor(Date.now() / 1000),
		};

		redis.rpush(r_key, JSON.stringify(data));
	}

	/**
* 返回用户数据
* @param {Object} user - 用户对象
* @returns {Object} - 用户数据
*/
	static return_user_data(user) {
		const data = {};
		if (user) {
			if (user.cur_gameid > 0) {
				const game = this.get_wj_game(user.cur_gameid);
				game_util.seamless_out_login_user_game(user, game);
			}

			data.uid = user.uid;
			data.token = user.user_token;
			data.phone = user.phone;
			data.email = user.email;
			data.nickname = user.nickname;
			data.header_img = user.header_img;
			data.money = user.money;
			data.commission = user.commission;
			data.total_money = user.total_money;
			data.total_withdraw = user.total_withdraw;
			data.total_bet = user.total_bet;
			data.share_number = user.share_valid_number;
			data.register_type = user.register_type;

			// 更新首次充值标识 0无 1首充送20%  2日首冲送10%
			let first_pay_type = 0;

			if (user.first_recharge === 0) {
				first_pay_type = 1;
			} else {
				const fist_give_key = 'first_recharge_give_money_flag_' + Time.formatDate(new Date());
				redis.hget(fist_give_key, String(user.uid)).then((res) => {
					if (res === null) {
						first_pay_type = 2;
					}
				})
			}



			data.first_pay_type = first_pay_type;

			let remain_code_amount = user.remain_code_amount;

			if (remain_code_amount < 0) {
				remain_code_amount = 0;
			}

			data.remain_code_amount = remain_code_amount;
			data.need_code_amount = user.need_code_amount;
			data.share_valid_number = user.share_valid_number;
			data.team_one_user_num = user.team_one_user_num;
			data.total_commission = user.total_commission;
			data.share_lv = user.share_lv;
			data.add_time = Time.formatDateHms(user.add_time);
			data.sign_bonus = String(user.sign_bonus);
			data.vip_earnings = String(user.vip_earnings);
			data.username = user.username;
			data.CPF = user.CPF || "";
			data.give_money = user.give_money;
			data.total_commission = user.total_commission;
			data.download_bonus = user.download_bonus;
			data.pay_type = user.pay_type
			// 计算提现余额
			let with_money = 0;

			if (remain_code_amount <= 0) {
				with_money = data.money;
			}

			if (with_money < 0) {
				with_money = 0;
			}

			data.with_money = with_money;

			Common.verify_user_vip_lv(user);

			data.vip_lv = user.vip_lv;
			data.vip_low_lv = user.vip_low_lv;
			return data;
		}
	}


}


module.exports = UserDataUtil;
