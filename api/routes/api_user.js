var express = require('express');
var router = express.Router();
const Mysql = require('../Mysql/mysql')
const redis = require('../Redis/index')
const auth = require('../middleware/auth')
const Time = require('../utils/Date')
const RKEY = require('../RKEY')
const userDataUtil = require('../utils/userDataUtil')

const OTP_CODE = '08181234'

// 用户刷新token
router.post('/api/get_user_token', auth, async (req, res, next) => {
	let data = {
		code: 0,
		data: {},
	}
	try {
		if (req.uid == 0) {
			data['code'] = 2
			return res.send(data)
		}
		let user = await userDataUtil.get_user_by_uid(req.uid)
		if (!user) {
			data['code'] = 3
			return res.send(data)
		}

		let token = await userDataUtil.return_user_login_token(req.uid, req.realIp)
		user['user_token'] = token
		data['data'] = await userDataUtil.return_user_data(user)
		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 获取用户信息
router.post('/api/get_user_info', auth, async (req, res, next) => {
	let data = {
		code: 0,
		data: {},
	}
	try {
		if (req.uid == 0) {
			data['code'] = 2
			return res.send(data)
		}
		let user = await userDataUtil.get_user_by_uid(req.uid)
		if (!user) {
			data['code'] = 3
			return res.send(data)
		}

		data['data'] = await userDataUtil.return_user_data(user)
		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 用户佣金转余额
router.post('/api/user_transfer_commission', auth, async (req, res, next) => {
	let data = {
		code: 0,
		state: 0,
	}
	try {
		let money = req.body.money
		if (money) {
			data['code'] = 100;
			return res.send(data)
		}
		if (req.uid === 0) {
			data['code'] = 1;
			return res.send(data)
		}
		if (money === null) {
			data['code'] = 0;
			return res.send(data)
		}
		let user = await userDataUtil.get_user_by_uid(req.uid);
		if (!user) {
			data['code'] = 3;
			return res.send(data)
		}
		if (parseFloat(user['commission']) < parseFloat(money)) {
			data['code'] = 35;  // 佣金不足
			return res.send(data)
		}
		let commission = money

		const resSql = new Mysql("update san_users set commission = commission - ?, money = money + ? where uid = ?",
			[commission, commission, req.uid])

		if (resSql > 0) {
			var after_money = parseFloat(user['money']) + parseFloat(commission);
			var after_commission = parseFloat(user['commission']) - parseFloat(commission);

			common.user_money_log_func(uid, commission, user['money'], after_money, 9);
			common.user_commission_log_func(uid, commission, user['commission'], after_commission, 102);
			common.user_brokerage_log_func(user['uid'], 0, 0, commission, 4);

			data['money'] = after_money;
			data['state'] = 1;
		}

		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 修改用户头像名称
router.post('/api/change_user_info', auth, async (req, res, next) => {
	let data = {
		code: 0,
		state: 0,
	}
	try {
		let header_img = req.body.header_img ? req.body.header_img : (req.body.header_img === 0 ? 0 : 1);
		let nickname = req.body.nickname.replace("'", '').replace('"', '');

		if (req.uid == 0) {
			data['code'] = 2;  // 登陆认证失败重新登陆
			return res.send(data)
		}

		let sql = "update san_users set nickname = ?, header_img = ? where uid = ?";
		const mysql = new Mysql();
		const resSql = await mysql.awaitSql(sql, [nickname, header_img, req.uid]);
		if (resSql) {
			data['state'] = 1;
		}

		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 用户打码量清零操作
router.post('/api/user_code_empty', auth, async (req, res, next) => {
	let data = {
		code: 0,
		state: 0,
	}
	try {
		if (req.uid == 0) {
			data['code'] = 2;  // 登陆认证失败重新登陆
			return res.send(data)
		}
		let user = await userDataUtil.get_user_by_uid(req.uid)
		if (!user) {
			data['code'] = 3;
			return res.send(data)
		}
		if (user['money'] > 5 ) {
			data['code'] = 46  // 不满足操作条件
			return res.send(data)
		}

		let sql = "update san_users set remain_code_amount = 0, need_code_amount = 0 where uid = ?"
		let sql2 = "insert into san_user_code_log (uid, cid, before_code, after_money, code_type, add_time) values " +
			"(?,?,?,?,?,NOW())"

		const mysql = new Mysql()
		const resSql = await mysql.awaitSql(sql, [req.uid])
		mysql.sql(sql2, [req.uid, user['cid'], user['remain_code_amount'], 0, 1])
		if (resSql) {
			data['state'] = 1
		}

		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 绑定用户手机号
router.post('/api/bind_user_phone', auth, async (req, res, next) => {
	let data = {
		code: 0,
		state: 0,
	}
	try {
		let phone = req.body.phone.replace("'", '').replace('"', '').replace(' ', '')
		let otp = req.body.otp
		if (req.uid == 0) {
			data['code'] = 2;  // 登陆认证失败重新登陆
			return res.send(data)
		}
		if (otp != OTP_CODE) {
			var con = await redis.get(String(phone));
			if (con == null) {
				data['code'] = 12;  // 手机验证码失效，重新获取验证码
				return res.send(data)
			}
			if (con !== String(otp)) {
				data['code'] = 13;  // 验证码错误
				return res.send(data)
			}
		}
		let phone_user = await userDataUtil.get_user_by_phone(phone)
		if (phone_user) {
			data['code'] = 17;  // 手机号已注册
			return res.send(data)
		}

		const mysql = new Mysql()
		const resSql = await mysql.awaitSql("update san_users set phone = ? where uid = ?", [phone, req.uid])
		if (resSql) {
			data['state'] = 1
		}

		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 绑定用户提现数据
router.post('/api/bind_user_withdrawal_info', auth, async (req, res, next) => {
	let data = {
		code: 0,
		state: 0,
	}
	try {
		let CPF = req.body.cpf.replace("'", '').replace('"', '').replace(' ', '')
		let pay_type = req.body.pay_type.replace("'", '').replace('"', '').replace(' ', '')
		let username = req.body.username.replace("'", '').replace('"', '')
		if (CPF == '') {
			data['code'] = 1
			return res.send(data)
		}
		if (username == '') {
			data['code'] = 1
			return res.send(data)
		}
		if (req.uid == 0) {
			data['code'] = 2;  // 登陆认证失败重新登陆
			return res.send(data)
		}
		let phone_user = await userDataUtil.get_user_by_cpf(CPF, req.uid)
		if (phone_user) {
			data['code'] = 88  // CPF已被使用
			return res.send(data)
		}

		const mysql = new Mysql()
		const resSql = await mysql.awaitSql("update san_users set username = ?, CPF = ? , pay_type = ? where uid = ?", [username, CPF, pay_type, req.uid])
		if (resSql) {
			data['state'] = 1
		}

		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 绑定用户邮箱
router.post('/api/bind_user_email', auth, async (req, res, next) => {
	let data = {
		code: 0,
		state: 0,
	}
	try {
		let email = req.body.email.replace("'", '').replace('"', '')
		let otp = req.body.otp
		if (req.uid == 0) {
			data['code'] = 2;  // 登陆认证失败重新登陆
			return res.send(data)
		}
		if (String(otp) !== OTP_CODE) {
			var con = await redis.get(String(email));
			if (con === null) {
				data['code'] = 12;  // 手机验证码失效，重新获取验证码
				return res.send(data)
			}
			if (con !== String(otp)) {
				data['code'] = 13;  // 验证码错误
				return res.send(data)
			}
		}
		let email_user = await userDataUtil.get_user_by_email(email)
		if (email_user) {
			data['code'] = 41 // 邮箱已注册
			return res.send(data)
		}
		const mysql = new Mysql()
		const resSql = await mysql.awaitSql("update san_users set email = ? where uid = ?", [email, req.uid])
		if (resSql) {
			data['state'] = 1
		}

		data['code'] = 1
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 修改用户密码
router.post('/api/change_user_pwd', auth, async (req, res, next) => {
	let data = {
		code: 0,
		state: 0,
	}
	try {
		let old_pwd = req.body.old_pwd
		let new_pwd = req.body.new_pwd
		if (req.uid == 0) {
			data['code'] = 2;  // 登陆认证失败重新登陆
			return res.send(data)
		}
		let user = await userDataUtil.get_user_by_uid(req.uid)
		if (!user) {
			data['code'] = 3
			return res.send(data)
		}
		let register_type = parseInt(user['register_type'])
		let register = ['phone', 'email']
		let user_login_type = user[register[register_type]]
		old_pwd = await userDataUtil.add_storage_pass(user_login_type, old_pwd)
		if (old_pwd != user['password']) {
			data['code'] = 5;  // 2次密码不一致
			return res.send(data)
		}
		new_pwd = await userDataUtil.add_storage_pass(user_login_type, new_pwd)

		const mysql = new Mysql()
		const resSql = await mysql.awaitSql("update san_users set password = ? where uid = ?", [new_pwd, req.uid])
		if (resSql) {
			data['state'] = 1
		}

		data['code'] = 2
		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 用户忘记密码
router.post('/api/user_forget_password', async (req, res, next) => {
	let data = {
		code: 0,
	}

	try {
		let password = req.body.password.trim()
		let phone = req.body.phone.replace(/\s/g, '')
		let otp = req.body.otp || ''
		if (password.length < 6) {
			data['code'] = 6
			return res.send(data)
		}
		let user = await userDataUtil.get_user_by_phone(phone)
		if (!user) {
			data['code'] = 3
			return res.send(data)
		}
		if (otp != OTP_CODE) {
			let con = await redis.get(phone)
			if (!con) {
				data['code'] = 12
				return res.send(data)
			}
			if (con != otp) {
				data['code'] = 13
				return res.send(data)
			}
		}
		let pass_str = userDataUtil.add_storage_pass(phone, password)
		const mysql = new Mysql()
		const resSql = await mysql.awaitSql("update san_users set password = ? where uid = ?", [pass_str, user['uid']])
		if (resSql >= 0) {
			data['code'] = 1
			redis.del(phone.toString())
		}

		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

// 用户忘记密码
router.post('/api/user_forget_email_password', async (req, res, next) => {
	let data = {
		code: 0,
	}

	try {
		let password = req.body.password.trim()
		let email = req.body.email.replace(/\s/g, '')
		let otp = req.body.otp || '' // 邮箱验证码
		if (password.length < 6) {
			data['code'] = 6
			return res.send(data)
		}
		let user = await userDataUtil.get_user_by_email(email)
		if (!user) {
			data['code'] = 3
			return res.send(data)
		}
		if (otp != OTP_CODE) {
			let con = await redis.get(email)
			if (!con) {
				data['code'] = 12
				return res.send(data)
			}
			if (con != otp) {
				data['code'] = 13
				return res.send(data)
			}
		}
		let pass_str = await userDataUtil.add_storage_pass(email, password)
		const mysql = new Mysql()
		const resSql = await mysql.awaitSql("update san_users set password = ? where uid = ?", [pass_str, user['uid']])
		if (resSql >= 0) {
			data['code'] = 1
			redis.del(email.toString())
		}

		res.send(data)
	} catch (error) {
		console.log(error);
	}
})

module.exports = router;