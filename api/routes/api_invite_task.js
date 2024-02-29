var express = require('express');
var router = express.Router();
const userDataUtil = require('../utils/userDataUtil');
const Utils = require('../utils/utils')
const Mysql = require('../Mysql/mysql')
const Time = require('../utils/Date')
const common = require('../utils/common')
const redis = require('../Redis/index');
const auth = require('../middleware/auth')
const RKEY = require('../RKEY');
const { functions } = require('lodash');
// 用户查询邀请任务状态
router.all('/api/get_user_invite_state', auth, async (req, res) => {
    let data = {
    }
    data['code'] = 0
    data['data'] = []
    data['num'] = 0
    try {
        data['num'] = req.uid ? await common.get_invite_number(req.uid) : 0
        data['data'] = await get_invite_data(req.uid, data['num'])
        data['code'] = 1
    } catch (error) {
        console.log(error);
    }
    res.send(data)
})

// 用户领取邀请任务奖励
router.all('/api/user_receive_invite_task', auth, async (req, res) => {
    let data = {
    }
    data['code'] = 0
    data['money'] = 0
    data['status'] = 0
    try {
        let uid = req.uid
        if (uid == 0) {
            data['code'] = 2
            res.send(data)
            return
        }
        let task_id = req.body.task_id
        let INVITE_TASK_CONF = await getInviteTaskConf()
        let task_conf = null
        if (INVITE_TASK_CONF.length > 0) {
            for (let i = 0; i < INVITE_TASK_CONF.length; i++) {
                const element = INVITE_TASK_CONF[i];
                if (task_id == element['task_id']) {
                    task_conf = element
                }
            }
        }
        if (task_conf == null) {
            // task_id错误
            data['code'] = 14
            res.send(data)
            return
        }
        let task_state = await get_task_state(uid, task_id)
        if (task_state) {
            // 已经领取过了
            data['code'] = 15
            res.send(data)
            return
        }
        let user = await userDataUtil.get_user_by_uid(uid)
        let num = await common.get_invite_number(req.uid)
        if (num < task_conf['num']) {
            data['code'] = 16
            res.send(data)
            return
        }
        data['status'] = user_receive_invite_task_reward(user, task_conf)
        data['money'] = task_conf['money']
        data['code'] = 1
    } catch (error) {
        console.log(error);
    }
    res.send(data)
})


const user_receive_invite_task_reward = (user, task_conf) => {
    let status = 0
    let day = Time.get_today_ymd()
    let after_money = parseFloat(task_conf['money']) + parseFloat(user['commission'])
    let give_money = parseFloat(task_conf['money'])
    common.user_commission_log_func(user['uid'], give_money, user['commission'], after_money, 107)  // 佣金日志
    let sql1 = `update san_users set commission = commission + ?, total_commission = total_commission + ? , share_task_brokerage = share_task_brokerage + ? where uid = ?`
    let sql2 = "insert into san_user_invite_task_log (uid, task_id, money, add_time) values (?, ?, ?, Now())"
    let sql3 = "insert into san_user_team_day_report (day, uid, team_invite_task_brokerage) values (?,?,?) ON DUPLICATE KEY UPDATE team_invite_task_brokerage = team_invite_task_brokerage + ?"
    const mysql = new Mysql()
    try {
        mysql.sql(sql1, [give_money, give_money, give_money, user['uid']])
        mysql.sql(sql2, [user['uid'], task_conf['task_id'], give_money])
        mysql.sql(sql3, [day, user['uid'], give_money, give_money])
        status = 1
        common.user_brokerage_log_func(user['uid'], 0, 0, task_conf['money'], 2)
    } catch (error) {
        console.log(error);
    }
    return status
}

// 查询用户是否有领取记录
const get_task_state = async (uid, task_id) => {
    sql = "select * from san_user_invite_task_log where uid = ? and task_id = ?"
    const mysql = new Mysql()
    let res = await mysql.getOne(sql, [uid, task_id])
    return res
}


const get_invite_data = async (uid, num) => {
    let INVITE_TASK_CONF = await getInviteTaskConf()
    let task_state_list = await get_all_task_state(uid)
    let over_task_list = []
    //循环出用户领取过的列表id
    task_state_list.map((i) => {
        over_task_list.push(i['task_id'])
    })
    let arr = []
    for (let i = 0; i < INVITE_TASK_CONF.length; i++) {
        const element = INVITE_TASK_CONF[i];
        let data = {}
        data['state'] = 0
        data['num'] = element['num']
        data['money'] = element['money']
        data['task_id'] = element['task_id']
        data['invite_num'] = num
        if (parseInt(num) >= data['num']) {
            data['state'] = 1
            data['invite_num'] = element['num']
            if (over_task_list.includes(element['task_id'])) {
                data['state'] = 2
            }
        }
        arr.push(data)
    }
    return arr

}

async function getInviteTaskConf() {
    let INVITE_TASK_CONF = await redis.get(RKEY.SAN_USER_INVITE_TASK)
    INVITE_TASK_CONF = INVITE_TASK_CONF ? JSON.parse(INVITE_TASK_CONF) : []
    return INVITE_TASK_CONF
}

// 查询用户邀请任务
async function get_all_task_state(uid) {
    arr = []
    sql = "select task_id from san_user_invite_task_log where uid = ?"
    const mysql = new Mysql()
    res = await mysql.getAll(sql, [uid])
    if (res) {
        arr = res
    }
    return arr
}

module.exports = router