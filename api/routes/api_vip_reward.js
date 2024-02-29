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


// bonus_type
// 1 立即反水
// 2 拆分反水
// """

// """
// get_type
// 0 拆分反水
// 1 打码反水
// 2 每日反水
// 3 每周反水
// 4 每月反水
// 5 vip晋级

// # 拆分时段
let hour_list = [0, 8, 20];
// # 用户获取可领取vip奖励列表
router.all('/api/get_user_vip_bonus_state', auth, async (req, res) => {
    let uid = req.uid;
    let data = {
        code: 0,
        data: {
            split_bonus: {
                money: 0,
                time: 0,
                state: 0,
                wait_money: 0,
                total_money: 0
            },
            now_bonus: {
                money: 0,
                time: 0,
                state: 0
            },
            day_bonus: {
                money: 0,
                state: 0
            },
            week_bonus: {
                money: 0,
                state: 0
            },
            month_bonus: {
                money: 0,
                state: 0
            },
            lv_up_bonus: {
                state: 0
            }
        },
        bonus_num: 0
    };

    if (true) {
        if (uid == '0') {
            data.code = 2;
            res.send(data);
            return;
        }
        user = await userDataUtil.get_user_by_uid(uid);
        if (!user) {
            data.code = 3;
            res.send(data);
            return
        }
        let VIP_CONF = await get_vip_lv_list_data();

        if (VIP_CONF) {
            let vip_conf = VIP_CONF[parseInt(user['vip_lv'])];
            // # 获取立即反水当前打码量
            code_amount = await get_now_code_amount(uid, vip_conf);
            // # 立即反水数据
            data.data.now_bonus.money = get_total_bonus(code_amount, vip_conf, "bet");
            let user_key = "vip_now_bonus_bonus_" + user['uid'].toString();
            let expire_time = await redis.ttl(user_key);
            data.data.now_bonus.time = expire_time > 0 ? expire_time : 0;

            if (expire_time <= 0 && data.data.now_bonus.money > 0) {
                data.data.now_bonus.state = 1;
                data.bonus_num += 1;
            }
            // 每日领取
            let day = Time.get_today_ymd();
            let user_day_key = "user_day_bet_bonus_" + uid.toString();
            let day_expire_time = redis.ttl(user_day_key);

            data.data.day_bonus.time = day_expire_time > 0 ? day_expire_time : 0;
            let user_vip_day_code_amount_key = `vip_day_code_amount_${day}`;
             //测试 
            //   await  redis.hset(user_vip_day_code_amount_key, String(uid),'1000');
            let today_day_code_amount = await redis.hget(user_vip_day_code_amount_key, String(uid));
            // 写入测试
            today_day_code_amount = today_day_code_amount ? parseFloat(today_day_code_amount) : 0;
            if (!(await redis.get(user_day_key)) && today_day_code_amount >= 10) {
                let day_code_amount = await get_day_code_amount(uid, vip_conf);
                data.data.day_bonus.money = get_total_bonus(day_code_amount, vip_conf, 'day_bet');

                if (data.data.day_bonus.money > 0) {
                    data.data.day_bonus.state = 1;
                    data.bonus_num += 1;
                }
            }

            // # 每周领取
            let week_day = Time.get_weekday();
            week_day = (week_day === 0) ? 7 : week_day;
            let expire_week_day = vip_conf.week_bet_bonus_save_time;
            if (week_day <= expire_week_day) {
                const week_u = Time.get_how_year_week();
                const user_week_key = `user_week_bet_bonus_${week_u}`;
                if (!(await redis.hget(user_week_key, uid))) {
                    const week_code_amount = (await get_last_week_code_amount(uid)) || 0;
                    data.data.week_bonus.money = get_total_bonus(week_code_amount, vip_conf, 'week_bet');
                    if (data.data.week_bonus.money > 0) {
                        data.data.week_bonus.state = 1;
                        data.bonus_num += 1;
                    }
                }
            }

            // #  每月领取
            let expire_month_day = vip_conf['month_bet_bonus_save_time'];
            const today = new Date();
            const toDay = String(day).slice(8);
            if (Number(toDay) <= Number(expire_month_day)) {
                const month = today.getMonth() + 1;
                const user_month_key = `user_month_bet_bonus_${month}`;
                 //测试 
            //   await redis.hset(user_month_key, String(uid), '1000');
                // console.log(await redis.hget(user_month_key, String(uid)));
                if (!(await redis.hget(user_month_key, String(uid)))) {
                    const month_code_amount = await get_last_month_code_amount(uid);
                    const code_amount = month_code_amount || 0;

                    data.data.month_bonus.money = get_total_bonus(code_amount, vip_conf, "month_bet");
                    if (data.data.month_bonus.money > 0) {
                        data.data.month_bonus.state = 1;
                        data.bonus_num += 1;
                    }
                }
            }

            // #  日历领取
            let front_day = Time.get_front_day_h_s(1);
            let lasst_day = Time.get_back_day(1);
            const sql = `SELECT * FROM san_user_vip_bonus_log WHERE uid = "${uid}" AND unlock_time >= '${front_day}' AND unlock_time <= '${lasst_day} 23:59:59' AND bonus_type = 2 AND status = 0 ORDER BY unlock_time`;
            const sql2 = `SELECT SUM(bonus) AS bonus FROM san_user_vip_bonus_log WHERE uid = "${uid}" AND status = 0 AND unlock_time >= '${front_day}'`;
            const mysql = new Mysql();
            const sqlRes = await mysql.getAll(sql, null);
            const res2 = await mysql.getOne(sql2, null);
            if (sqlRes) {
                const current_time = Math.floor(Date.now() / 1000); // Current time in seconds
                for (const bonusLog of sqlRes) {
                    if (current_time >= Time.days_int(String(bonusLog.unlock_time))) {
                        data['data']['split_bonus']['money'] += bonusLog.bonus;
                    } else {
                        if (data['data']['split_bonus']['money'] <= 0) {
                            data['data']['split_bonus']['wait_money'] += bonusLog.bonus;
                            data['data']['split_bonus']['time'] = Math.floor(
                                Time.days_int(String(bonusLog.unlock_time)) - current_time
                            );
                            break;
                        }
                    }
                }
            }

            if (res2 && res2.bonus) {
                data['data']['split_bonus']['total_money'] = Math.round(res2.bonus * 100) / 100;
            }

            if (data['data']['split_bonus']['money'] > 0) {
                data['data']['split_bonus']['state'] = 1;
                data['data']['split_bonus']['money'] = Math.round((data['data']['split_bonus']['money']) * 1000) / 1000;
                data['bonus_num'] += 1;
            }

            //   # vip升级奖励
            let arr = [];
            let sql_vip = `select * from san_user_vip_up_reward_log where  uid = "${uid}"`;
            let res_vip = await mysql.getAll(sql_vip, null);
            let vip_low_list = JSON.parse((await redis.get("san_vip_low_vip_list"))) || [];
            if (vip_low_list) {
                let arr = [];

                for (let d of vip_low_list) {
                    let vip_data = {
                        id: d.id,
                        vip_lv: d.vip_lv,
                        lv: d.lv,
                        state: 0
                    };

                    if (user.vip_lv > parseInt(d.vip_lv)) {
                        vip_data.state = 1;
                    }

                    if (user.vip_lv === parseInt(d.vip_lv)) {
                        if (user.vip_low_lv >= parseInt(d.lv)) {
                            vip_data.state = 1;
                        }
                    }

                    if (res_vip) {
                        for (let i of res_vip) {
                            if (String(i.vip_lv) === String(vip_data.vip_lv) && String(i.lv) === String(d.lv)) {
                                vip_data.state = 2;
                            }
                        }
                    }

                    arr.push(vip_data);
                }
                for (let d of arr) {
                    if (d.state === 1) {
                        data.data.lv_up_bonus.state = 1;
                        break;
                    }
                }
            }
            data.code = 1;
        }
    }
    return res.send(data);

});
// # 用户获取可领取vip升级奖励列表
router.all('/api/get_user_vip_up_bonus_state', auth, async (req, res) => {
    let data = {
        code: 0,
        data: []
    };
    let uid = req.uid;
    if (true) {
        try {
            if (uid === 0) {
                data.code = 2;
                return res.send(data);
            }

            let user = await userDataUtil.get_user_by_uid(uid);

            if (user === null) {
                data.code = 3;
                return res.send(data);
            }

            let arr = [];
            let sql = "SELECT * FROM san_user_vip_up_reward_log WHERE uid = ?";
            let mysql = new Mysql();
            let sqlRes = await mysql.getAll(sql, [uid]);

            let vip_low_list = (await redis.get("san_vip_low_vip_list")) ? JSON.parse(await redis.get("san_vip_low_vip_list")) : [];
            if (vip_low_list && vip_low_list.length > 0) {
                for (let d of vip_low_list) {
                    let vip_data = {
                        id: d.id,
                        vip_lv: d.vip_lv,
                        lv: d.lv,
                        state: 0
                    };

                    if (user.vip_lv > parseInt(d.vip_lv)) {
                        vip_data.state = 1;
                    }

                    if (user.vip_lv === parseInt(d.vip_lv)) {
                        if (user.vip_low_lv >= parseInt(d.lv)) {
                            vip_data.state = 1;
                        }
                    }

                    if (sqlRes) {
                        for (let i of sqlRes) {
                            if (String(i.vip_lv) === String(vip_data.vip_lv) && String(i.lv) === String(d.lv)) {
                                vip_data.state = 2;
                            }
                        }
                    }

                    arr.push(vip_data);
                }
            }

            data.data = arr;
            data.code = 1;
        } catch (error) {
            console.error(error);
        }
    }
    return res.send(data);
})

// # 用户领取vip升级奖励
router.all('/api/user_get_vip_up_bonus', auth, async (req, res) => {
    let data = {
        code: 0,
        status: 0
    };
    let uid = req.uid;
    if (true) {
        try {
            let id = req.body.id;
            if (uid === 0) {
                data.code = 2;
                res.send(data);
                return;
            }

            let user = await userDataUtil.get_user_by_uid(uid);

            if (!user) {
                data.code = 3;
                res.send(data);
                return;
            }

            let vip_low_list = (await redis.get("san_vip_low_vip_list")) ? JSON.parse((await redis.get("san_vip_low_vip_list"))) : [];
            let vip_conf = null;

            if (vip_low_list && vip_low_list.length > 0) {
                for (let d of vip_low_list) {
                    if (String(d.id) === String(id)) {
                        vip_conf = d;
                    }
                }
            }

            if (vip_conf === null) {
                data.code = 28; // 参数错误
                res.send(data);
                return;
            }

            if (parseFloat(vip_conf.need_code_amount) > parseFloat(user.total_bet)) {
                data.code = 39; // 领取条件未达标
                res.send(data);
                return;
            }

            let sql = `SELECT * FROM san_user_vip_up_reward_log WHERE uid = "${uid}" AND vip_lv = '${vip_conf.vip_lv}' AND lv = '${vip_conf.lv}'`;
            let mysql = new Mysql();
            let res1 = await mysql.getOne(sql, null);

            if (res1) {
                data.code = 38; // 奖励已领取
                res.send(data);
                return;
            }

            let VIP_CONF = await get_vip_lv_list_data();

            if (VIP_CONF) {
                // 获取用户当前vip等级配置
                let vipLvConf = VIP_CONF[parseInt(user.vip_lv)];
                let total_bonus = vip_conf.bonus;
                let now_bonus = parseFloat(total_bonus) * (parseFloat(vipLvConf.lv_reward_now_rate) / 100);
                let split_bonus = [];

                for (let d = 0; d < parseInt(vipLvConf.lv_reward_split_day); d++) {
                    let spBonus = parseFloat(total_bonus) * (parseFloat(vipLvConf.lv_reward_split_rate) / 100) / parseInt(vipLvConf.lv_reward_split_day);
                    split_bonus.push(spBonus);
                }
                // 用户领取奖励 用户 立即领取奖励 拆分后奖励 余额变动日志 获取类型
                user_vip_receive_bonus(user, now_bonus, split_bonus, 4, 5);
                let sql2 = `INSERT INTO san_user_vip_up_reward_log (uid, vip_lv, lv, money, add_time) VALUES ("${uid}", '${vip_conf.vip_lv}', '${vip_conf.lv}', '${vip_conf.bonus}', NOW())`;
                let res2 = await mysql.awaitSql(sql2, null);

                if (res2) {
                    data.total_bonus = total_bonus;
                    data.bonus = now_bonus;
                    data.split_bonus = parseFloat(total_bonus) - parseFloat(now_bonus);
                    data.status = 1;
                }
            }

            data.code = 1;
        } catch (error) {
            console.error(error);
        }
    }

    return res.send(data)

})

// # 用户领取立即反水奖励
router.all('/api/user_get_now_vip_bonus', auth, async (req, res) => {
    let uid = req.uid;
    let data = {
        code: 0,
        total_bonus: 0,
        split_bonus: 0,
        bonus: 0,
        status: 0
    };

    if (true) {
        // try {
        if (uid === 0) {
            data.code = 2;
            return res.send(data);
        }

        let user = await userDataUtil.get_user_by_uid(uid);

        if (user === null) {
            data.code = 3;
            return res.send(data);
        }

        let user_key = "vip_now_bonus_bonus_" + user.uid;

        if ((await redis.get(user_key))) {
            data.code = 47; // 冷却中
            return res.send(data);
        }

        let day = Time.get_today_ymd();
        let user_get_num = await redis.hget("user_vip_get_num_" + day, user.uid);
        user_get_num = parseInt(user_get_num) || 0;

        if (user_get_num >= 11) {
            data.code = 48; // 今日已达到领取上限
            return res.send(data);
        }

        let VIP_CONF = await get_vip_lv_list_data();

        if (VIP_CONF) {
            // 获取用户当前vip等级配置
            let vip_conf = VIP_CONF[user.vip_lv];
            let code_amount = await get_now_code_amount(uid, vip_conf);

            // 获取用户可立即领取金额
            let now_bonus = get_now_bonus(vip_conf, code_amount, "bet");

            // 获取用户拆分金额
            let split_bonus = get_now_split_bonus(vip_conf, code_amount, "bet");

            if (now_bonus <= 0) {
                data.code = 39;
                return res.send(data);
            }

            // 用户领取奖励
            // 用户  立即领取奖励   拆分后奖励   余额变动日志    获取类型
            let receiveRes = await user_vip_receive_bonus(user, now_bonus, split_bonus, 24, 1);

            if (receiveRes) {
                // 用户累计的打码量清零
                for (let d = 0; d <= parseInt(vip_conf.bet_bonus_save_time); d++) {
                    let set_day = Time.get_front_day(d);
                    let user_vip_code_amount_key = "vip_code_amount" + set_day;
                    redis.hset(user_vip_code_amount_key, user.uid, '0');
                    redis.expire(user_vip_code_amount_key, 86400 * 3);
                }

                // 添加用户领取冷却时间
                redis.setex(user_key, 1800, '1');

                // 用户领取次数增加
                user_get_num += 1;
                redis.hset("user_vip_get_num_" + day, user.uid, user_get_num.toString());
                redis.expire("user_vip_get_num_" + day, 86400 * 2);

                data.total_bonus = get_total_bonus(code_amount, vip_conf, "bet");
                data.bonus = now_bonus;
                data.split_bonus = parseFloat(data.total_bonus) - parseFloat(now_bonus);
                data.status = 1;
            }
        }

        data.code = 1;
    }

    return res.send(data);

})

//用户领取每日反水奖励
router.all('/api/user_get_day_vip_bonus', auth, async (req, res) => {
    let data = {
        code: 0,
        total_bonus: 0,
        split_bonus: 0,
        bonus: 0,
        status: 0
    };
    let uid = req.uid;

    if (true) {
        // try {
        if (uid === 0) {
            data.code = 2;
            res.send(data);
            return;
        }

        let user = await userDataUtil.get_user_by_uid(uid);

        if (!user) {
            data.code = 3;
            res.send(data);
            return;
        }

        let user_day_key = `user_day_bet_bonus_${uid}`;

        if ((await redis.get(user_day_key))) {
            data.code = 38; // 奖励已领取过
            res.send(data);
            return;
        }

        let day = Time.get_today_ymd();
        let user_vip_day_code_amount_key = `vip_day_code_amount_${day}`;
        let today_day_code_amount = await redis.hget(user_vip_day_code_amount_key, String(uid));
        today_day_code_amount = parseFloat(today_day_code_amount) || 0;

        if (today_day_code_amount < 10) {
            data.code = 39;
            res.send(data);
            return;
        }

        let VIP_CONF = await get_vip_lv_list_data();

        if (VIP_CONF) {
            // 获取用户当前vip等级配置
            let vip_conf = VIP_CONF[parseInt(user.vip_lv)];
            let code_amount = await get_day_code_amount(uid, vip_conf);

            // 获取用户可立即领取金额
            let now_bonus = get_now_bonus(vip_conf, code_amount, "day_bet");

            // 获取用户拆分金额
            let split_bonus = get_now_split_bonus(vip_conf, code_amount, "day_bet");

            if (now_bonus <= 0) {
                data.code = 39;
                res.send(data);
                return;
            }

            // 用户领取奖励 用户 立即领取奖励 拆分后奖励 余额变动日志 获取类型
            let receiveRes = await user_vip_receive_bonus(user, now_bonus, split_bonus, 25, 2);

            if (receiveRes) {
                // 用户累计的打码量清零
                for (let d = 0; d < parseInt(vip_conf.day_bet_bonus_save_time) + 1; d++) {
                    let setDay = Time.get_front_day(d);
                    let user_vip_day_code_amount_key = `vip_day_code_amount_${setDay}`;
                    redis.hset(user_vip_day_code_amount_key, String(user.uid), '0');
                    redis.expire(user_vip_day_code_amount_key, 86400 * 2);
                }

                // 添加领取标识
                redis.setex(user_day_key, 86400, '1');

                data.total_bonus = get_total_bonus(code_amount, vip_conf, "day_bet");
                data.bonus = now_bonus;
                data.split_bonus = parseFloat(data.total_bonus) - parseFloat(now_bonus);
                data.status = 1;
            }
        }

        data.code = 1;
        // } catch (error) {
        //     console.error(error);
        // }
    }

    return res.send(data)
})

//# 用户领取每周反水奖励
router.all('/api/user_get_week_vip_bonus', auth, async (req, res) => {
    let data = {
        code: 0,
        total_bonus: 0,
        split_bonus: 0,
        bonus: 0,
        status: 0
    };
    let uid = req.uid;
    if (true) {
        // try {
        if (uid === 0) {
            data.code = 2;

            return res.send(data);
        }

        let user = await userDataUtil.get_user_by_uid(uid);

        if (user === null) {
            data.code = 3;

            return res.send(data);
        }

        let week_u = Time.get_how_year_week();
        let user_week_key = "user_week_bet_bonus_" + week_u;

        if ((await redis.hget(user_week_key, user.uid))) {
            data.code = 38;  // 奖励已领取过
            return res.send(data);
        }

        let VIP_CONF = await get_vip_lv_list_data();

        if (VIP_CONF) {
            // 获取用户当前vip等级配置
            let vip_conf = VIP_CONF[user.vip_lv];
            let weekDay = Time.get_weekday();
            let week_day = (weekDay !== 0) ? weekDay : 7;

            if (parseInt(week_day) !== 0 && parseInt(week_day) > parseInt(vip_conf.week_bet_bonus_save_time)) {
                data.code = 47;
                return res.send(data);
            }

            let code_amount = await get_last_week_code_amount(uid);

            // 获取用户可立即领取金额
            let now_bonus = get_now_bonus(vip_conf, code_amount, "week_bet");

            // 获取用户拆分金额
            let split_bonus = get_now_split_bonus(vip_conf, code_amount, "week_bet");

            if (now_bonus <= 0) {
                data.code = 39;
                return res.send(data);
            }

            // 用户领取奖励
            // 用户  立即领取奖励   拆分后奖励   余额变动日志    获取类型
            let receiveRes = await user_vip_receive_bonus(user, now_bonus, split_bonus, 26, 3);

            if (receiveRes) {
                // 添加领取标识
                redis.hset(user_week_key, user.uid, 1);
                redis.expire(user_week_key, 86400 * 7);

                data.total_bonus = get_total_bonus(code_amount, vip_conf, "week_bet");
                data.bonus = now_bonus;
                data.split_bonus = parseFloat(data.total_bonus) - parseFloat(now_bonus);
                data.status = 1;
            }
        }

        data.code = 1;
    }
    return res.send(data);
})

//# 用户领取每月反水奖励
router.all('/api/user_get_month_vip_bonus', auth, async (req, res) => {
    let uid = req.uid;
    let data = {};
    data.code = 0;
    data.total_bonus = 0;
    data.split_bonus = 0;
    data.bonus = 0;
    data.status = 0;

    if (true) {
        // try {
        if (uid === 0) {
            data.code = 2;
            return res.send(data);
        }

        let user = await userDataUtil.get_user_by_uid(uid);
        if (!user) {
            data.code = 3;
            return res.send(data);
        }

        let month = new Date().getMonth() + 1;
        let user_month_key = "user_month_bet_bonus_" + month;

        if ((await redis.hget(user_month_key, uid))) {
            data.code = 38;  // 奖励已领取过
            return res.send(data);
        }

        let VIP_CONF = await get_vip_lv_list_data();

        if (VIP_CONF) {
            // 获取用户当前vip等级配置
            let vip_conf = VIP_CONF[user.vip_lv];

            let day = Time.get_today_ymd();
            let expire_week_day = vip_conf.month_bet_bonus_save_time;
            let to_day = day.slice(8);

            if (parseInt(to_day) > parseInt(expire_week_day)) {
                data.code = 47;
                return res.send(data);
            }

            let code_amount = await get_last_month_code_amount(uid);

            // 获取用户可立即领取金额
            let now_bonus = get_now_bonus(vip_conf, code_amount, "month_bet");

            // 获取用户拆分金额
            let split_bonus = get_now_split_bonus(vip_conf, code_amount, "month_bet");

            if (now_bonus <= 0) {
                data.code = 39;
                return res.send(data);
            }

            // 用户领取奖励
            // 用户  立即领取奖励   拆分后奖励   余额变动日志    获取类型
            let receiveRes = await user_vip_receive_bonus(user, now_bonus, split_bonus, 27, 4);

            if (receiveRes) {
                // 添加领取标识
                redis.hset(user_month_key, uid, 1);
                redis.expire(user_month_key, 86400 * 7);

                data.total_bonus = get_total_bonus(code_amount, vip_conf, "month_bet");
                data.bonus = now_bonus;
                data.split_bonus = parseFloat(data.total_bonus) - parseFloat(now_bonus);
                data.status = 1;
            }
        }

        data.code = 1;
    }
    return res.send(data);
})

// 获取用户拆分奖励接口
router.all('/api/get_user_split_bonus_list', auth, async (req, res) => {
    let uid = req.uid;
    let data = {
        code: 0,
        data: []
    };

    try {
        if (uid === 0) {
            data.code = 2;
            return res.send(data);
        }

        const user = await userDataUtil.get_user_by_uid(uid);

        if (!user) {
            data.code = 3;
            return res.send(data);
        }

        let last_week = Time.get_front_day(10);
        let sql = `select * from san_user_vip_bonus_log where uid = ? and day >= ? order by day, unlock_time`;
        let front_day = Time.get_front_day_h_s(1);
        let sql2 = `select sum(bonus) as bonus from san_user_vip_bonus_log where uid = ? and status = 0 and unlock_time >= ?`;

        const mysql = new Mysql();
        let sqlRes = await mysql.getAll(sql, [uid, last_week]);
        let res2 = await mysql.getOne(sql2, [uid, front_day]);

        if (res2) {
            data.total_money = res2.bonus ? parseFloat(res2.bonus.toFixed(2)) : 0.00;
        }
        if (sqlRes) {
            let back_day = Time.get_back_day(1);
            let today = Time.get_today_ymd();
            let current_time = Date.now() / 1000;
            let arr = [];
            let seen_days = new Set();
            let today_unlock_time = 0;

            // for (const d of sqlRes) {
            for (let index = 0; index < sqlRes.length; index++) {
                const d = sqlRes[index];
                let day = Time.formatDate(d.day);
                if (!seen_days.has(day)) {
                    seen_days.add(day)
                    let maps = {
                        day: day,
                        data: [],
                        total_bonus: 0,
                        state: 0
                    };
                    if (current_time >= Time.days_int(day + " 23:59:59")) {
                        maps.state = 1;
                    } else if (today == day) {
                        maps.state = 0;
                        maps.time = 0;
                        let hour = new Date().getHours();
                        for (const j of hour_list) {
                            if (hour < j) {
                                let unlockTime = day + " " + `${j}:00:00`;
                                maps.time = Time.days_int(unlockTime) - current_time;
                                today_unlock_time = maps.time;
                                break;
                            }
                        }
                    } else if (back_day == day && today_unlock_time == 0) {
                        maps.state = 2;
                        maps.time = Time.get_yesterday_zero_time();
                    } else {
                        maps.state = 3;
                    }

                    arr.push(maps);
                }
            }

            let back_day_bonus_flag = true;
            let today_bonus_flag = true;

            for (let index = 0; index < sqlRes.length; index++) {
                const i = sqlRes[index];
                let day = Time.formatDate(i.day);
                for (const item of arr) {
                    if (day === Time.formatDate(item.day)) {
                        if (current_time >= Time.days_int(day + " 23:59:59") || today == day || back_day == day) {
                            let newMaps = {
                                bonus: i.bonus,
                                unlock_time: Time.formatDateHms(i.unlock_time),
                                status: i.status
                            };
                            if (i.status !== 1 && day !== Time.formatDate(today)) {
                                let unlock_time = Time.days_int(Time.formatDateHms(i.unlock_time));
                                let endTime = unlock_time + 86400;

                                if (endTime < current_time) {
                                    newMaps.status = 2;
                                } else if (back_day === Time.formatDate(item.day)) {
                                    if (back_day_bonus_flag) {
                                        item.wait_bonus = i.bonus;
                                        back_day_bonus_flag = false;
                                    }
                                }
                            } else if (day === Time.formatDate(today) && i.status !== 1) {
                                const unlock_time = Time.days_int(Time.formatDateHms(i.unlock_time));

                                if (today_bonus_flag) {
                                    item.wait_bonus = i.bonus;
                                    today_bonus_flag = false;
                                }

                                if (unlock_time > current_time) {
                                    newMaps.status = 3;
                                }
                            }

                            item.data.push(newMaps);
                        }

                        item.total_bonus += i.bonus;
                        item.total_bonus = parseFloat(item.total_bonus.toFixed(3));

                    }
                }
            }

            data.data = arr;
        }

        data.code = 1;
    } catch (error) {
        console.error(error);
    }

    return res.send(data);
})
// # 用户领取拆分奖金
router.all('/api/user_get_split_bonus', auth, async (req, res) => {
    let uid = req.uid;
    let data = {};
    data.code = 0;
    data.state = 0;
    data.money = 0;

    if (true) {
        // try {
        let day = req.body.day;

        if (uid === 0) {
            data.code = 2;
            return res.send(data);
        }

        let user = await userDataUtil.get_user_by_uid(uid);

        if (user === null) {
            data.code = 3;
            return res.send(data);
        }

        let sql = `select * from san_user_vip_bonus_log where uid = '${uid}' and day = '${day}' AND status = 0`;
        let mysql = new Mysql();
        let res1 = await mysql.getAll(sql, null);

        if (res1 === null) {
            data.code = 38;
            return res.send(data);
        }

        let total_bonus = 0;
        let current_time = Date.now() / 1000;

        for (let d of res1) {
            let unlock_time = Time.days_int(Time.formatDateHms(d.unlock_time));
            let end_time = unlock_time + 86400;

            if (unlock_time < current_time && current_time < end_time) {
                total_bonus += d.bonus;

                sql = `update san_user_vip_bonus_log set status = 1, get_time = NOW() where uid = '${uid}' and day = '${Time.formatDate(d.day)}' and unlock_time = '${Time.formatDateHms(d.unlock_time)}' and bonus_type = 2 and get_type = 0`;
                mysql = new Mysql();
                mysql.sql(sql, null);
            }
        }
        user_receive_bonus(user, total_bonus, day, 28);

        data.state = 1;
        data.money = total_bonus;
        data.code = 1;
    }

    return res.send(data);

})

// # 循环出vip保留的天数剩余的打码量
async function get_now_code_amount(uid, vip_conf) {
    let code_amount = 0;
    for (let d = 0; d <= parseInt(vip_conf.bet_bonus_save_time); d++) {
        let get_day = Time.get_front_day(d);
        let user_vip_code_amount_key = "vip_code_amount" + get_day;
         //测试 
        // await redis.hset(user_vip_code_amount_key, uid.toString(), '1000');
        let code = await redis.hget(user_vip_code_amount_key, uid.toString());
        code_amount += parseFloat(code) || 0;
    }
    return code_amount;
}

/**
 * 获取立即领取vip奖励的值
 * @param {Object} vip_conf - VIP 等级配置对象
 * @param {number} code_amount - 用户的打码量
 * @param {string} str_key - 键名后缀
 * @returns {number} - 立即领取 VIP 奖励的值
 */
function get_now_bonus(vip_conf, code_amount, str_key) {
    let money = 0;
    code_amount = parseFloat(code_amount) || 0;

    if (code_amount > 0) {
        let totalMoney = get_total_bonus(code_amount, vip_conf, str_key);
        let nowRate = parseFloat(vip_conf[str_key + '_bonus_now_rate']) / 100;
        money = totalMoney * nowRate;

        if (money <= 0.004) {
            money = 0;
        }

        if (0.005 <= money && money < 0.01) {
            money = 0.01;
        }
    }

    return parseFloat(money.toFixed(2));
}


// # 获取vip等级数据
async function get_vip_lv_list_data() {
    let vip_lv_list = await redis.get(RKEY.SAN_GAME_VIP_LV_LIST)
    let vip_list_data = []
    if (vip_lv_list) {
        vip_list_data = JSON.parse(vip_lv_list);
    }
    return vip_list_data
}

// # 获取可领取的所有奖励
function get_total_bonus(code_amount, vip_conf, str_key) {
    let rate = parseFloat(vip_conf[str_key + '_bonus_rate']) / 100;
    let totalMoney = code_amount * rate;
    let roundedTotalMoney = Math.round(totalMoney * 100) / 100;

    return roundedTotalMoney;
}


// # 循环出vip保留的天数剩余的打码量
async function get_day_code_amount(uid, vip_conf) {
    let code_amount = 0;
    for (let d = 0; d <= parseInt(vip_conf['day_bet_bonus_save_time']); d++) {
        const get_day = Time.get_front_day(d);
        const user_vip_day_code_amount_key = "vip_day_code_amount_" + String(get_day);
        const code = (await redis.hget(user_vip_day_code_amount_key, String(uid))) || 0;
        code_amount += parseFloat(code) || 0;
    }

    return code_amount;
}
// # 获取上周用户slot总打码量
async function get_last_week_code_amount(uid) {
    const last_week_start = Time.get_last_week_start();
    const last_week_end = Time.get_last_week_end();
    const sql = `SELECT SUM(total_activity_bet) total_activity_bet FROM san_user_team_day_report WHERE uid = '${uid}' AND day >= '${last_week_start}' AND day <= '${last_week_end}'`;
    const mysql = new Mysql();
    const res = await mysql.getOne(sql, null);
    return res.total_activity_bet || 0;
}

// # 获取上月用户slot总打码量
async function get_last_month_code_amount(uid) {
    const lastMonthStart = Time.get_last_month_start();
    const lastMonthEnd = Time.get_last_month_end();
    const sql = `SELECT SUM(total_activity_bet) AS total_activity_bet FROM san_user_team_day_report WHERE uid = "${uid}" AND day >= '${lastMonthStart}' AND day <= '${lastMonthEnd}'`;
    const mysql = new Mysql();
    try {
        const res = await mysql.getOne(sql, null);
        return res && res.total_activity_bet ? res.total_activity_bet : 0;
    } catch (error) {
        console.error(error);
        return 0;
    } finally {
    }
}

/**
 * 获取拆分后金额
 * @param {Object} vip_conf - VIP 等级配置对象
 * @param {number} code_amount - 用户的打码量
 * @param {string} str_key - 键名后缀
 * @returns {Array} - 拆分后的金额数组
 */
function get_now_split_bonus(vip_conf, code_amount, str_key) {
    const arr = [];

    if (code_amount > 0) {
        // 计算出拆分前金额
        const totalMoney = get_total_bonus(code_amount, vip_conf, str_key);
        const nowRate = parseFloat(vip_conf[str_key + '_bonus_split_rate']) / 100;
        const money = totalMoney * nowRate;

        for (let i = 0; i < parseInt(vip_conf[str_key + '_bonus_split_day']); i++) {
            const arrMoney = money / parseInt(vip_conf[str_key + '_bonus_split_day']);
            arr.push(arrMoney);
        }
    }

    return arr;
}

/**
 * 用户领取奖励
 * @param {Object} user - 用户对象
 * @param {number} now_bonus - 立即领取的奖励金额
 * @param {Array} split_bonus - 拆分后的奖励数组
 * @param {number} money_type - 奖励类型
 * @param {number} get_type - 获取类型
 * @returns {Object} - 领取结果
 */
async function user_vip_receive_bonus(user, now_bonus, split_bonus, money_type, get_type) {
    const day = Time.get_today_ymd();
    add_vip_now_bonus_log(user, day, now_bonus, get_type);
    const res = await user_receive_bonus(user, now_bonus, day, money_type);
    const todayBonus = await get_user_today_bonus_log(user.uid);
    const bonusArr = [];
    // 添加拆分日志
    for (let d = 0; d < split_bonus.length; d++) {
        const splitDay = Time.get_back_day(d + 1);
        for (let i = 0; i < hour_list.length; i++) {
            const hour = hour_list[i];
            const bonus = parseFloat((split_bonus[d] / 3).toFixed(3));
            const data = {
                uid: user.uid,
                cid: user.cid,
                day: splitDay,
                bonus: bonus,
                hour: hour,
                get_type: get_type,
            };
            bonusArr.push(data);
        }
    }
    if (todayBonus === null) {
        let date = new Date();
        const nowHour = parseInt(date.getHours());
        let splitIndex = 0;
        for (let index = 0; index < hour_list.length; index++) {
            const element = hour_list[index];
            if (nowHour < element) {
                splitIndex++;
            }
        }
        if (splitIndex !== 0 && bonusArr.length > 0) {
            for (let d = 0; d < splitIndex; d++) {
                bonusArr[bonusArr.length - (d + 1)].day = day;
            }
        }
    }
    for (let i = 0; i < bonusArr.length; i++) {
        const data = bonusArr[i];
        add_vip_spil_bonus_log(data.uid, data.cid, data.day, data.bonus, data.hour, data.get_type);
    }
    return res;
}



/**
 * 添加用户立即领取vip奖金日志
 * @param {Object} user - 用户对象
 * @param {string} day - 日期
 * @param {number} bonus - 奖金金额
 * @param {number} get_type - 获取类型
 * @returns {boolean} - 操作结果
 */
async function add_vip_now_bonus_log(user, day, bonus, get_type) {
    const sql = "insert into san_user_vip_bonus_log (uid,cid,bonus_type,get_type,bonus,day,unlock_time,get_time,status) values " +
        "(?, ?, 1, ?, ?, ?, NOW(), NOW(), 1) ON DUPLICATE KEY UPDATE bonus = bonus + ?";
    const mysql = new Mysql();
    const res = await mysql.awaitSql(sql, [user.uid, user.cid, get_type, bonus, day, bonus]);
    return res;
}

/**
 * 领取奖励修改打码量以及用户余额
 * @param {Object} user - 用户对象
 * @param {number} money - 奖金金额
 * @param {string} day - 日期
 * @param {number} money_type - 奖金类型
 * @returns {boolean} - 操作结果
 */
async function user_receive_bonus(user, money, day, money_type) {
    const after_money = (parseFloat(user.money) + parseFloat(money)).toFixed(2);
    const rate = (await redis.hget(RKEY.SAN_GAME_ALL_CONF, "gift_code_rate")) || 10;
    const code_amount = parseFloat(money) * parseFloat(rate);
    const remain_code_amount = (parseFloat(user.remain_code_amount) <= 0) ?
        code_amount : (parseFloat(user.remain_code_amount) + code_amount).toFixed(2);
    const need_code_amount = (parseFloat(user.remain_code_amount) <= 0) ?
        (parseFloat(user.need_code_amount) + code_amount) : parseFloat(user.need_code_amount) + parseFloat(code_amount);

    // 计算所需打码量
    let res = null;

    // 立返
    if (money_type === 24) {
        // 修改用户信息
        const sql = "update san_users set money = money + ?, vip_now = vip_now + ?, give_money = give_money + ?" +
            ",vip_earnings = vip_earnings + ?, remain_code_amount = ?, need_code_amount = ?  where uid = ?";
        const mysql = new Mysql();
        res = await mysql.awaitSql(sql, [money, money, money, money, remain_code_amount, need_code_amount, user.uid]);
        Common.user_day_data_total(user.uid, String(day), { give_money: money, vip_earnings: money, vip_now: money });
        Common.user_money_log_func(user.uid, money, parseFloat(user.money), parseFloat(after_money), money_type);
    }

    // 每日
    if (money_type === 25) {
        // 修改用户信息
        const sql = "update san_users set money = money + ?, vip_day = vip_day + ?, give_money = give_money + ?" +
            ",vip_earnings = vip_earnings + ?, remain_code_amount = ?, need_code_amount = ?   where uid = ?";
        const mysql = new Mysql();
        res = await mysql.awaitSql(sql, [money, money, money, money, remain_code_amount, need_code_amount, user.uid]);

        Common.user_day_data_total(user.uid, String(day), { give_money: money, vip_earnings: money, vip_day: money });
        Common.user_money_log_func(user.uid, money, parseFloat(user.money), parseFloat(after_money), money_type);
    }

    // 每周
    if (money_type === 26) {
        // 修改用户信息
        const sql = "update san_users set money = money + ?, vip_week = vip_week + ?, give_money = give_money + ?" +
            ",vip_earnings = vip_earnings + ? , remain_code_amount = ?, need_code_amount = ?  where uid = ?";
        const mysql = new Mysql();
        res = await mysql.awaitSql(sql, [money, money, money, money, remain_code_amount, need_code_amount, user.uid]);

        Common.user_day_data_total(user.uid, String(day), { give_money: money, vip_earnings: money, vip_week: money });
        Common.user_money_log_func(user.uid, money, parseFloat(user.money), parseFloat(after_money), money_type);
    }

    // 每月
    if (money_type === 27) {
        // 修改用户信息
        const sql = "update san_users set money = money + ?, vip_month = vip_month + ?, give_money = give_money + ?" +
            ",vip_earnings = vip_earnings + ?, remain_code_amount = ?, need_code_amount = ?  where uid = ?";
        const mysql = new Mysql();
        res = await mysql.awaitSql(sql, [money, money, money, money, remain_code_amount, need_code_amount, user.uid]);

        Common.user_day_data_total(user.uid, String(day), { give_money: money, vip_earnings: money, vip_month: money });
        Common.user_money_log_func(user.uid, money, parseFloat(user.money), parseFloat(after_money), money_type);
    }

    // 拆分领取
    if (money_type === 28) {
        // 修改用户信息
        const sql = "update san_users set money = money + ?, vip_split = vip_split + ?, give_money = give_money + ?" +
            ",vip_earnings = vip_earnings + ?, remain_code_amount = ?, need_code_amount = ?  where uid = ?";
        const mysql = new Mysql();
        res = await mysql.awaitSql(sql, [money, money, money, money, remain_code_amount, need_code_amount, user.uid]);
        Common.user_day_data_total(user.uid, String(day), { give_money: money, vip_earnings: money, vip_split: money });
        Common.user_money_log_func(user.uid, money, parseFloat(user.money), parseFloat(after_money), money_type);
    }

    // vip升级领取
    if (money_type === 4) {
        // 修改用户信息
        const sql = "update san_users set money = money + ?, vip_up = vip_up + ?, give_money = give_money + ?" +
            ",vip_earnings = vip_earnings + ?, remain_code_amount = ?, need_code_amount = ?   where uid = ?";
        const mysql = new Mysql();
        res = await mysql.awaitSql(sql, [money, money, money, money, remain_code_amount, need_code_amount, user.uid]);
        Common.user_day_data_total(user.uid, String(day), { give_money: money, vip_earnings: money, vip_up: money });
        Common.user_money_log_func(user.uid, money, parseFloat(user.money), parseFloat(after_money), money_type);
    }

    return res;
}

/**
 * 获取今天vip反水日志
 * @param {string} uid - 用户ID
 * @returns {Object} - 查询结果
 */
async function get_user_today_bonus_log(uid) {
    const day = Time.get_today_ymd();
    const sql = `select uid from san_user_vip_bonus_log where uid = '${uid}' and bonus_type = 2 and day = '${day}'`;
    const mysql = new Mysql();
    const res = await mysql.getOne(sql, null);
    return res;
}

/**
 * 添加用户拆分vip奖金日志
 * @param {string} uid - 用户ID
 * @param {string} cid - 客户ID
 * @param {string} day - 日期
 * @param {number} bonus - 奖金金额
 * @param {number} hour - 小时
 * @param {string} get_type - 获取类型
 */
function add_vip_spil_bonus_log(uid, cid, day, bonus, hour, get_type) {
    bonus = Math.round(bonus * 1000) / 1000;
    const unlock_time = `${day} ${hour.toString().padStart(2, '0')}:00`;
    const sql = `insert into san_user_vip_bonus_log (uid,cid,bonus_type,bonus,day,unlock_time,status) values ` +
        `('${uid}', '${cid}', 2, '${bonus}', '${day}', '${unlock_time}', 0) ON DUPLICATE KEY UPDATE bonus = bonus + ${bonus}`;
    const sql2 = `insert into san_user_vip_split_bonus_log (uid,cid,unlock_time,bonus,get_type, day, add_time) values ` +
        `('${uid}', '${cid}', '${unlock_time}', '${bonus}','${get_type}','${day}', NOW())`;
    const mysql = new Mysql();
    mysql.sql(sql)
    mysql.sql(sql2)
}


module.exports = router;

