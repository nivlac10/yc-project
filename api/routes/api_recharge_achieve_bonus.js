var express = require('express');
var router = express.Router();
const Mysql = require('../Mysql/mysql')
const redis = require('../Redis/index')
const auth = require('../middleware/auth')
const Time = require('../utils/Date')
const RKEY = require('../RKEY')
const UserDataUtil = require('../utils/userDataUtil')
const Common = require('../utils/common');

const activity_conf = [
    {
        "id": 1,
        "recharge_money": 100,
        "bonus": 10,
    }, {
        "id": 2,
        "recharge_money": 300,
        "bonus": 30,
    }, {
        "id": 3,
        "recharge_money": 500,
        "bonus": 50,
    }, {
        "id": 4,
        "recharge_money": 1000,
        "bonus": 100,
    }, {
        "id": 5,
        "recharge_money": 5000,
        "bonus": 150,
    }, {
        "id": 6,
        "recharge_money": 10000,
        "bonus": 1000,
    }, {
        "id": 7,
        "recharge_money": 100000,
        "bonus": 5000,
    }, {
        "id": 8,
        "recharge_money": 500000,
        "bonus": 10000,
    }
];

router.all('/api/get_recharge_achieve_state', auth, async (req, res) => {
    let uid = req.uid;
    const data = {
        code: 0,
        bonus_list: activity_conf,
        money: 0
    };

    const mysql = new Mysql();

    try {
        for (const bonus of data.bonus_list) {
            bonus.state = 0;
        }

        if (uid === 0) {
            data.code = 1;
            return res.send(data);
        }

        const sql = "select * from san_user_activity_total_data where uid = ?";
        const sql2 = "select * from san_user_recharge_achieve_bonus_log where uid = ?";
        const res1 = await mysql.getOne(sql, [uid]);
        const res2 = await mysql.getAll(sql2, [uid]);
        if (res1) {
            data.money = res1.total_money;

            for (const bonus of data.bonus_list) {
                bonus.state = 0;
                if (bonus.recharge_money <= res1.total_money) {
                    bonus.state = 1;
                }

                if (res2) {
                    for (const log of res2) {
                        if (log.bonus_id === bonus.id) {
                            bonus.state = 2;
                        }
                    }
                }
            }
        }

        data.code = 1;
    } catch (e) {
        console.error(e);
    } finally {
    }

    return res.send(data);

})

router.all('/api/receive_recharge_achieve_bonus', auth, async (req, res) => {
    let uid = req.uid;
    const data = {
        code: 0,
        money: 0
    };
    const mysql = new Mysql();
    const bonusId = req.body.id;

    try {
        if (uid === 0) {
            data.code = 1;
            return res.send(data);
        }

        let activity = null;

        for (const bonus of activity_conf) {
            if (bonus.id === parseInt(bonusId)) {
                activity = bonus;
                break;
            }
        }

        if (!activity) {
            data.code = 28;
            return res.send(data);
        }

        const user = await UserDataUtil.get_user_by_uid(uid);
        const sql = `select total_money from san_user_activity_total_data where uid = '${uid}'`;
        const sql2 = 'select * from san_user_recharge_achieve_bonus_log where uid = ? and bonus_id = ?';

        const res1 = await mysql.getOne(sql, null);
        const res2 = await mysql.getOne(sql2, [uid, bonusId]);
        if (res2) {
            data.code = 38;
            return res.send(data);
        }

        if (res1.total_money < activity.recharge_money) {
            data.code = 46;
            return res.send(data);
        }

        const status = await update_user_money(user, activity.bonus, bonusId);

        if (status) {
            data.code = 1;
            data.money = activity.bonus;
        }
    } catch (e) {
        console.error(e);
    }

    return res.send(data);
})

//# 修改用户数据与汇总
async function update_user_money(user, money, bonusId) {
    let res = null;

    try {
        const day = Time.get_today_ymd();
        const rate = 10;
        const code_amount = parseFloat(money) * parseFloat(rate);
        const now_code = (user.remain_code_amount <= 0) ? code_amount : (user.remain_code_amount + code_amount).toFixed(2);
        const now_need_code = (user.remain_code_amount <= 0) ? (user.need_code_amount + code_amount) : (user.need_code_amount + code_amount);
        const after_money = user.money + money;

        const sql = `
            UPDATE san_users
            SET money = money + "${money}", recharge_achieve = recharge_achieve + "${money}", give_money = give_money + "${money}",
                remain_code_amount = "${now_code}", need_code_amount = "${now_need_code}"
            WHERE uid = "${user.uid}"
        `;
        const sql2 = `
            INSERT INTO san_user_recharge_achieve_bonus_log (uid, money, add_time, bonus_id)
            VALUES ("${user.uid}", "${money}", NOW(), "${bonusId}")
        `;

        const mysql = new Mysql();
        let sqlList = [sql, sql2];
        res = await mysql.affairs(sqlList, null);
        // res = await mysql.update(sql, [money, money, money, now_code, now_need_code, user.uid]);
        // const res2 = await mysql.insertOne(sql2, [user.uid, money, bonusId]);

        if (res) {
            // 余额日志
            Common.user_money_log_func(user.uid, money, parseFloat(user.money), after_money, 43);
            // 用户日汇总
            Common.user_day_data_total(user.uid, day, { give_money: money, recharge_achieve: money });
            // 日总汇总
            Common.day_money_total(user.cid, day, { recharge_achieve: money });
        }
    } catch (e) {
        console.error(e);
    }
    // console.log('修改用户数据与汇总',res);
    return res;
}

module.exports = router;