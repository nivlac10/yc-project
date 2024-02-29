var express = require('express');
var router = express.Router();
const auth = require('../middleware/auth');
const Mysql = require('../Mysql/mysql')
const util = require('../utils/utils');
const userDataUtil = require('../utils/userDataUtil');

// # 获取用户不同游戏类型的返水列表
router.all('/api/user_rebate_list', auth, async (req, res) => {
    let uid = req.uid;
    const data = {
        code: 0,
        data: [],
        count: 0,
        vip_earnings: 0,
        title: ["Slot Bonus", "Table Bonus", "Live Bonus", "Fish Bonus", "Fast Bonus"]
    };

    try {
        const page = req.body.page || 1;
        const limit = parseInt(req.body.limit) || 10;
        const offset = (parseInt(page) - 1) * limit;

        if (uid === 0) {
            data.code = 1;
            return util.toJson(data);
        }

        const user = await userDataUtil.get_user_by_uid(uid);

        if (!user) {
            data.code = 3;
            return res.send(data);
        }

        const mysql = new Mysql();
        const rebateSql = "select `day`, vip_earnings, slot_earnings, table_earnings, live_earnings, fish_earnings, fast_earnings" +
            " from san_user_team_day_report where uid = ? order by day desc limit ?, ?";
        const countSql = "select count(*) as num from san_user_team_day_report where uid = ?";
        const res = await mysql.getAll(rebateSql, [uid, offset, limit]);
        const count = await mysql.getOne(countSql, [uid]);

        data.vip_earnings = parseFloat(user.vip_earnings);

        if (res) {
            for (const d of res) {
                d.day = String(d.day);
            }

            data.data = res;
            data.count = count.num;
        }

        data.code = 1;
    } catch (error) {
        console.error(error);
    }

    return res.send(data);
})

module.exports = router;