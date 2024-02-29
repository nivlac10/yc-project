/*
 * @Author: wawodel 69891926+wawodel@users.noreply.github.com
 * @Date: 2023-12-05 16:42:22
 * @LastEditors: wawodel 69891926+wawodel@users.noreply.github.com
 * @LastEditTime: 2023-12-13 15:20:31
 * @FilePath: \express-admin\routes\api_give_code.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
/*
 * @Author: wawodel 69891926+wawodel@users.noreply.github.com
 * @Date: 2023-12-05 13:14:42
 * @LastEditors: wawodel 69891926+wawodel@users.noreply.github.com
 * @LastEditTime: 2023-12-06 17:22:13
 * @FilePath: \Node-admin\routes\api_give_code.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
const RKEY = require('../RKEY')
var express = require('express');
var router = express.Router();
const redis = require('../Redis/index')
const auth = require('../middleware/auth');
const Time = require('../utils/Date');
const Mysql = require('../Mysql/mysql')
const util = require('../utils/utils');
const Utils = new util();
const userDataUtil = require('../utils/userDataUtil');
const Common = require('../utils/common');


//用户领取
router.all('/api/user_receive_code', auth, async (req, res) => {
    const data = {
        code: 0,
        money: 0
    };
    try {
        const uid = req.uid;
        if (!uid) {
            data.code = 3;
            return res.send(data);
        }

        const code = req.body.code;
        console.log(code);
        const flag = await redis.get(`gift_flag_${uid}`);

        if (flag) {
            return res.send(data);
        }

        await redis.set(`gift_flag_${uid}`, '1', 'EX', 3);
        const give = await redis.hget('san_give_code', code);
        if (!give) {
            data.code = 42;
            return res.send(data);
        }

        const giveConf = JSON.parse(give);
        const nowInt = Math.floor(Date.now() / 1000);
        if (nowInt > giveConf.end_time) {
            data.code = 43;
            return res.send(data);
        }

        if (parseInt(giveConf.code_num) <= parseInt(giveConf.receive_num)) {
            data.code = 44;
            return res.send(data);
        }

        const log = await redis.hget(`san_give_code_log_${code}`, uid);

        if (log) {
            data.code = 45;
            return res.send(data);
        }

        const user = await userDataUtil.get_user_by_uid(uid);

        if (!user) {
            data.code = 2;
            return res.send(data);
        }

        if (giveConf.is_recharge == 1) {
            const isRecharge = await get_today_order(uid);

            if (!isRecharge) {
                data.code = 36;
                return res.send(data);
            }
        }

        let money = 0;
        if (giveConf.is_random == 0) {
            money = Utils.getRandomArbitrary(parseInt(giveConf.min_money),parseInt(giveConf.max_money) )
            
        } else {
            money = parseFloat(giveConf.fixed_money);
        }

        const afterMoney = parseFloat(user.money) + money;
        const updateResult = await update_user_money(user, money);

        if (updateResult) {
            await redis.hset(`san_give_code_log_${code}`, uid, '1');
            await redis.expire(`san_give_code_log_${code}`, 86400 * 30);
            await add_give_code_log(user, giveConf, money);

            const day = Time.get_today_ymd();

            // 余额日志
            Common.user_money_log_func(user.uid, money, parseFloat(user.money), afterMoney, 23);

            // 用户日汇总
            Common.user_day_data_total(user.uid, day, { give_money: money, give_code_money: money });

            // 日总汇总
            Common.day_money_total(user.cid, day, { give_code_money: money });

            data.code = 1;
            data.money = parseFloat(money.toFixed(2));
        }
    } catch (error) {
        console.error('Error in userReceiveCode:', error);
    }

    res.send(data);
    return;

})
//  用户领取记录
router.all('/api/get_give_code_list', (req, res) => {
    try {
        let data = {
            code: 0,
            data: []
        };
        let now = Date.now();
        for (let d = 0; d < 20; d++) {
            let maps = {
                add_time: Time.int_ymd(now / 1000),
                nickname: Utils.random_str(4) + '****@gmail.com',
                give_money: Math.round(Math.random() * (100 - 0.1) + 0.1)
            };
            now -= Math.random() * (10 - 5) + 5;
            data.data.push(maps);
        }

        data.code = 1;
        res.send(data);
        return;
    } catch (error) {
        console.error(error);
        throw error;
    }
})

/**
 * 添加领取日志
 * @param {Object} user - 用户信息对象
 * @param {Object} conf - 配置信息对象
 * @param {number} money - 领取金额
 */
async function add_give_code_log(user, conf, money) {
    try {
        const sql = "INSERT INTO san_give_code_log (cid, uid, add_time, give_money, code_id, code) VALUES (?, ?, NOW(), ?, ?, ?)";
        const sql2 = `UPDATE san_give_code SET receive_num = receive_num + 1 WHERE code_id = '${conf.code_id}'`;

        const mysql = new Mysql(); // 请确保 Mysql 类的实现已经定义
        
        const res = await mysql.awaitSql(sql, [user.cid, user.uid, money, conf.code_id, conf.code]);
        const res2 = await mysql.awaitSql(sql2, null);

        if (res2 > 0) {
            const sql3 = `SELECT * FROM san_give_code WHERE code_id = ${conf.code_id}`;
            const res3 = await mysql.getOne(sql3, null);

            if (res3) {
                res3.add_time = res3.add_time.toISOString(); // 转换为 ISO 格式的字符串
                redis.hset('san_give_code', conf.code, JSON.stringify(res3)); // 请确保 redis 对象的实现已经定义
            }
        }
    } catch (error) {
        console.error(error);
        throw error;
    }
}

/**
 * 修改用户数据与汇总
 * @param {Object} user - 用户信息对象
 * @param {number} money - 修改的金额
 * @returns {number} - 受影响的行数
 */
async function update_user_money(user, money) {
    try {
        const rate = (await redis.hget(RKEY.SAN_GAME_ALL_CONF, "gift_code_rate")) || 10;
        const codeAmount = parseFloat(money) * parseFloat(rate);
        const nowCode = (user.remain_code_amount <= 0) ? codeAmount : parseFloat(user.remain_code_amount) + codeAmount;
        const nowNeedCode = (user.remain_code_amount <= 0) ? codeAmount : parseFloat(user.need_code_amount) + codeAmount;

        const sql = "UPDATE san_users SET money = money + ?, give_code_money = give_code_money + ?, give_money = give_money + ?" +
            ", remain_code_amount = ?, need_code_amount = ? WHERE uid = ?";

        const mysql = new Mysql(); // 请确保 Mysql 类的实现已经定义
        const res = await mysql.awaitSql(sql, [money, money, money, nowCode, nowNeedCode, user.uid]);
        return res;
    } catch (error) {
        console.error('修改用户数据与汇总出错:', error);
        throw error;
    }
}

/**
 * 查询当日是否有充值
 * @param {number} uid - 用户ID
 * @returns {Object|null} - 查询结果对象或 null
 */
async function get_today_order(uid) {
    try {
        const sql = "SELECT id FROM san_order_list WHERE uid = ? AND DATE(notify_time) = CURDATE() AND status = 1";
        const mysql = new Mysql();
        const res = await mysql.getOne(sql, [uid]);
        return res;
    } catch (error) {
        console.error('查询当日是否有充值出错:', error);
        throw error;
    }
}




module.exports = router;