/**
 * API Code 说明
 * 0   请求失败
 * 1   请求成功
 * 2   登陆认证不通过
 * 3   账号不存在
 * 4   此账号手机已绑定
 * 5   2次密码不一致
 * 6   密码为6到12位字母数字组合验证失败
 * 7   密码不能为纯数字
 * 8   手机号码不能为空
 * 9   登陆密码错误
 * 10  当前为临时用户，请先绑定手机或facebook
 * 11  当前账户必须为临时账号(临时账号获取token)
 * 12  手机验证码失效，重新获取验证码
 * 13  手机验证码错误
 * 14  任务不存在
 * 15  任务已领取
 * 16  任务邀请好友数量不足
 * 17  手机号已注册
 * 18  账号已绑定facebook
 * 19  参数不能为空
 * 20  当前facebook账号已被绑定
 * 21  金额不能小于0
 * 22  下单失败
 * 23  余额不足
 * 24  参数错误
 * 25  打码量不足
 * 26  用户未充值
 * 27  充值金额少于0
 * 28  参数错误
 * 29  当前支付通已关闭
 * 30  存在未过期的月卡
 * 31  没有月卡记录
 * 32  签到已领取或已过期
 * 33  今日已领取月卡
 * 34  当前账号已绑定上级
 * 35  佣金不足
 * 36  用户需要充值
 * 37  游戏中不能获取外接游戏链接
 * 38  奖励已领取
 * 39  领取条件未达标
 * 40  请稍等几秒钟再发送！
 * 41  此邮箱已被绑定
 * 42  code码不存在
 * 43  code已过期
 * 44  code码已被抢完请下次再试
 * 45  该用户已领取过code
 * 46  您不满足当前操作条件
 * 47  领取还在冷却中
 * 100  支付下单失败
 * 101  您的设备注册数已达到限制
 */

const { upperCase, digits } = require('lodash');
const crypto = require('crypto');
const redis = require('../Redis/index')

class utils {
	/**
	 * 将响应数据转化为 JSON 格式，并设置响应头信息。
	 * @param {Object} res - Express 响应对象
	 * @param {Object} response - 响应数据对象
	 * @param {number} counts - 计数值
	 */
	to_counts_json(res, response, counts) {
		/*
		使用 res.json() 方法将响应数据转换为 JSON 格式，并发送给客户端。
		同时设置 Access-Control-Allow-Origin 和 counts 的响应头信息。
		*/
		res.json(response);
		res.set('Access-Control-Allow-Origin', '*');
		res.set('counts', counts);
	}
	// toCountsJson 用法示例
	// const express = require('express');
	// const app = express();
	// const port = 3000;

	// app.get('/', (req, res) => {
	//     const responseData = { key: 'value' }; // 替换为你的实际响应数据
	//     const countsValue = 10; // 替换为你的实际计数值

	//     toCountsJson(res, responseData, countsValue);
	// });

	// app.listen(port, () => {
	//     console.log(`Server is running at http://localhost:${port}`);
	// });

	/**
	 * 将响应数据转化为 JSON 格式，并设置响应头信息。
	 * @param {Object} response - 响应数据对象
	 * @returns {Object} - JSON 格式的响应对象
	 */
	toJson(response) {
		/*
		使用 JSON.stringify() 方法将响应数据转换为 JSON 格式，
		并设置 Access-Control-Allow-Origin 的响应头信息。
		*/
		const jsonResponse = {
			data: JSON.stringify(response),
			headers: {
				'Access-Control-Allow-Origin': '*'
			}
		};

		return jsonResponse;
	}

	/**
	 * 使用 MD5 算法对字符串进行加密。
	 * @param {string} inputString - 要加密的字符串
	 * @returns {string} - 加密后的字符串
	 */
	md5(inputString) {
		if (typeof inputString === 'string') {
			// 创建 MD5 加密对象
			const md5 = require('md5');

			// 使用 MD5 算法对字符串进行加密
			const encryptedString = md5(inputString);

			return encryptedString;
		} else {
			return '';
		}
	}

	/**
	 * 获取客户端IP地址
	 * @param {Object} req - 请求对象
	 * @returns {string} - 客户端IP地址
	 */
	getCurrentIP(req) {
		// 从请求头中获取X-Forwarded-For字段
		const forwardedFor = req.headers['x-forwarded-for'];

		// 如果X-Forwarded-For存在，则使用逗号分隔的第一个IP地址
		if (forwardedFor) {
			const ipList = forwardedFor.split(',');
			return ipList[0];
		}

		// 否则，使用远程地址
		return req.connection.remoteAddress;
	}

	/**
	 * 生成指定长度的随机字符串
	 * @param {number} num - 字符串长度
	 * @returns {string} - 随机字符串
	 */
	random_str(num) {
		const chars = 'abcdefghijklmnopqrstuvwxyz';
		let result = '';
		for (let i = 0; i < num; i++) {
			result += chars.charAt(Math.floor(Math.random() * chars.length));
		}
		return result;
	}

	/**
	 * 将数据列表转换为字符串拼接的 SQL 条件
	 * @param {Array} sqlList - SQL 条件列表
	 * @returns {string} - SQL 条件字符串
	 */
	data_list_to_str(sqlList) {
		let sqlStr = "";
		if (sqlList.length > 0) {
			if (sqlList.length > 1) {
				sqlStr += " WHERE " + sqlList.join(' AND ');
			} else {
				sqlStr += " WHERE " + sqlList[0];
			}
		}
		return sqlStr;
	}


	/**
	 * 生成指定范围的随机小数（保留两位小数）
	 * @param {number} min - 最小值（包含）
	 * @param {number} max - 最大值（不包含）
	 * @returns {number} - 生成的随机小数
	 */
	getRandomArbitrary(min, max) {
		return parseFloat((Math.random() * (max - min) + min).toFixed(2));
	}


	/**
	 * 生成订单号
	 * @returns {string} - 生成的订单号
	 */
	add_order_number() {
		const timeStr = new Date().toISOString().replace(/\D/g, '').slice(0, -3);
		const randomNum = Math.floor(Math.random() * 900000 + 100000);
		return `${timeStr}${randomNum}`;
	}

	/**
	 * 用户登录验证中间件
	 * @param {function} func - 处理函数
	 * @returns {function} - 中间件函数
	 */
	api_login_required = (func) => {
		return async (req, res, next) => {
			try {
				let uid = 0;
				let userToken = req.query.token || req.headers.token || '';
				if (userToken === '') {
					return func(uid, req, res, next);
				}

				const tokenKey = `user_login_token_${userToken}`;
				const getAsync = promisify(redisClient.get).bind(redisClient);
				const con = await getAsync(tokenKey);

				if (!con) {
					return func(uid, req, res, next);
				}

				const onlyKey = `only_user_${con}`;
				const resFromRedis = await getAsync(onlyKey);

				if (!resFromRedis || resFromRedis !== userToken) {
					return func(uid, req, res, next);
				}

				return func(con, req, res, next);
			} catch (error) {
				console.error('用户登陆验证出错:', error);
			}
		}
	}

	// 
	/**
* 随机生成渠道 key
* @returns {string} - 渠道 key
*/
	random_channel_key = () => {
		const num = random(2, 5);
		const chars = upperCase + digits;
		return Array.from({ length: num }, () => random(0, chars.length - 1)).map(i => chars[i]).join('');
	};


	//  获取渠道信息
	async get_channel_info(cid) {
		const res = await redis.hget(RKEY.SAN_GAME_NEW_CHANNEL_CONF, String(cid));
		return res ? JSON.parse(res) : null;
	}



	// 生成订单号
	add_order_number() {
		const now = new Date();
		const year = now.getFullYear();
		const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are zero-based
		const day = String(now.getDate()).padStart(2, '0');
		const hours = String(now.getHours()).padStart(2, '0');
		const minutes = String(now.getMinutes()).padStart(2, '0');
		const seconds = String(now.getSeconds()).padStart(2, '0');
		const milliseconds = String(now.getMilliseconds()).padStart(3, '0');

		// 生成随机数，确保足够的随机性
		const randomPart = String(Math.floor(Math.random() * 1000)).padStart(3, '0');

		// 组合订单号
		const orderNumber = `${year}${month}${day}${hours}${minutes}${seconds}${milliseconds}${randomPart}`;

		return orderNumber;
	}

}


// const data = random_str(12);
// console.log(data);

module.exports = utils;

