/*
 * @Author: wawodel 69891926+wawodel@users.noreply.github.com
 * @Date: 2023-12-05 17:23:37
 * @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 * @LastEditTime: 2024-01-22 15:46:15
 * @FilePath: \express-admin\routes\api_roller_money.js
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

const max_roller_money = 1
const min_roller_money = 3
const need_bet_amount = 100

router.all('/api/receive_roller_money', auth, async (req, res) => {
    let uid = req.uid || 0;
    const data = {
        code: 0,
        money: 0
    };
    // console.log('uid',uid);
    try {
        if (uid === 0) {
            data.code = 3;
            res.send(data);
            return;
        }

        const user = await userDataUtil.get_user_by_uid(uid);

        if (!user) {
            data.code = 3;
            res.send(data);
            return;
        }

        const day = Time.get_today_ymd();
        // await redis.hset("user_bet_roller_amount", String(uid), '100');
        let userBetRollerAmount = await redis.hget("user_bet_roller_amount", String(uid));
        let rollerNum = 0;
        if (userBetRollerAmount) {
            userBetRollerAmount = parseInt(userBetRollerAmount);
            rollerNum = parseInt(userBetRollerAmount / need_bet_amount);
        }
        if (rollerNum < 1) {
            data.code = 39;
            res.send(data)
            return;
        }

        const money = parseFloat(Utils.getRandomArbitrary(min_roller_money, max_roller_money).toFixed(2));
        const apiRes = await add_roller_money_log(user, money, userBetRollerAmount);

        if (apiRes) {
            await update_user_money(user, money, day);
            data.money = money;
            data.code = 1;
        }
    } catch (error) {
        console.error(error);
    }
    res.send(data);
    return
});

//  查询状态
router.all('/api/roller_money_state', auth, async (req, res) => {
    const data = {
        code: 0,
        num: 0,
        bet_amount: 0,
        need_amount: need_bet_amount
    };
    let uid = req.uid || '0';

    try {
        if (uid === '0') {
            data.code = 1;
            res.send(data);
            return;
        }

        let rollerNum = 0;

        // await redis.hset("user_bet_roller_amount", String(uid),'1000');
        let userBetRollerAmount = await redis.hget("user_bet_roller_amount", String(uid));
        // console.log('userBetRollerAmount',userBetRollerAmount);

        if (userBetRollerAmount) {
            userBetRollerAmount = parseFloat(userBetRollerAmount);
            rollerNum = Math.floor(userBetRollerAmount / need_bet_amount);
        } else {
            userBetRollerAmount = 0;
        }
        // console.log(rollerNum);

        if (userBetRollerAmount > need_bet_amount) {
            userBetRollerAmount = userBetRollerAmount - (need_bet_amount * rollerNum);
        }

        data.num = rollerNum;
        data.bet_amount = parseFloat(userBetRollerAmount.toFixed(2));
        data.code = 1;
        res.send(data);
        return;
    } catch (error) {
        console.error(error);
    }

})

/**
 * 添加领取日志
 * @param {Object} user - 用户信息对象
 * @param {number} money - 领取金额
 * @param {number} userBetRollerAmount - 用户押注金额
 * @returns {Promise<number>} - 返回插入结果，1 表示成功，0 表示失败
 */
async function add_roller_money_log(user, money, userBetRollerAmount) {
    try {
        const sql = "INSERT INTO san_roller_money_log (cid, uid, add_time, money) VALUES (?, ?, NOW(), ?)";
        const mysql = new Mysql();
        const res = await mysql.awaitSql(sql, [user.cid, user.uid, money]);

        if (res) {
            userBetRollerAmount -= need_bet_amount;
            redis.hset("user_bet_roller_amount", user.uid.toString(), userBetRollerAmount);
        }

        return res;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

/**
 * 修改用户数据与汇总
 * @param {Object} user - 用户信息对象
 * @param {number} money - 变动金额
 * @param {string} day - 当前日期字符串
 * @returns {Promise<number>} - 返回更新结果，1 表示成功，0 表示失败
 */
async function update_user_money(user, money, day) {
    try {
        const rate = (await redis.hget(RKEY.SAN_GAME_ALL_CONF, "gift_code_rate")) || 10;
        const codeAmount = parseFloat(money) * parseFloat(rate);
        const nowCode = parseFloat(user.remain_code_amount) <= 0
            ? parseFloat(user.remain_code_amount) + codeAmount
            : parseFloat(user.remain_code_amount);

        const nowNeedCode = parseFloat(user.remain_code_amount) <= 0
            ? parseFloat(user.need_code_amount) + codeAmount
            : parseFloat(user.need_code_amount) + codeAmount;
        const afterMoney = parseFloat(user.money) + parseFloat(money);

        const sql = "UPDATE san_users SET money = money + ?, roller_money = roller_money + ?, give_money = give_money + ?" +
            ", remain_code_amount = ?, need_code_amount = ? WHERE uid = ?";
        const mysql = new Mysql(); // 请确保 Mysql 类的实现已经定义
        const res = await mysql.awaitSql(sql, [money, money, money, nowCode, nowNeedCode, user.uid]);

        if (res) {
            // 余额日志
            Common.user_money_log_func(user.uid, money, parseFloat(user.money), afterMoney, 29);
            // 用户日汇总
            Common.user_day_data_total(user.uid, day, { give_money: money, roller_money: money });
            // 日总汇总
            Common.day_money_total(user.cid, day, { roller_money: money });
        }

        return res;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

/**
 * 查询当日是否有充值
 * @param {number} uid - 用户ID
 * @returns {Promise<Object|null>} - 返回查询结果，包含充值信息或 null
 */
async function get_today_order(uid) {
    try {
        const sql = "SELECT id FROM san_order_list WHERE uid = ? AND DATE(notify_time) = CURDATE() AND status = 1";
        const mysql = new Mysql();
        const res = await mysql.getOne(sql, [uid]);

        return res;
    } catch (error) {
        console.error(error);
        throw error;
    }
}


module.exports = router;

