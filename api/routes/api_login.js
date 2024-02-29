var express = require('express');
var router = express.Router();
const userDataUtil = require('../utils/userDataUtil');
const Utils = require('../utils/utils')
const Mysql = require('../Mysql/mysql')
const Time = require('../utils/Date')
const Common = require('../utils/common')
const { nanoid } = require('nanoid');
const OTP_CODE = '66001234'
const redis = require('../Redis/index');
// 手机登录
router.all('/api/user_phone_login', async (req, res) => {
    let data = {
        "code": 0,
        "data": {
        }
    }
    try {
        let resData = req.body
        let phone = resData.phone.replace(/\s/g, '')
        let password = resData.password.replace(/\s/g, '')
        let user = await userDataUtil.get_user_by_phone(phone)
        if (user == null) {
            data['code'] = 3
            res.send(data)
            return
        }
        let pass_str = userDataUtil.add_storage_pass(phone, password)
        if (user['password'] != pass_str) {
            data['code'] = 9
            res.send(data)
            return
        }
        userHourLogin(user)
        user['user_token'] = await userDataUtil.return_user_login_token(user['uid'], req.realIp)
        data['data'] = await userDataUtil.return_user_data(user)
        data['code'] = 1
    } catch (error) {
        console.log(error);
    }
    res.send(data)
    return
})

// 邮箱登录
router.all('/api/user_email_login', async (req, res) => {
    let data = {
        "code": 0,
        "data": {
        }
    }
    try {
        let resData = req.body
        let email = resData.email.replace(/\s/g, '')
        let password = resData.password.replace(/\s/g, '')
        let user = await userDataUtil.get_user_by_email(email)
        if (user == null) {
            data['code'] = 3
            res.send(data)
            return
        }
        let pass_str = userDataUtil.add_storage_pass(email, password)
        if (user['password'] != pass_str) {
            data['code'] = 9
            res.send(data)
            return
        }
        userHourLogin(user)
        user['user_token'] = await userDataUtil.return_user_login_token(user['uid'], req.realIp)
        data['data'] = await userDataUtil.return_user_data(user)
        data['code'] = 1
    } catch (error) {
        console.log(error);
    }
    res.send(data)
    return
})

// 手机注册
router.all('/api/user_phone_register', async (req, res) => {
    let data = {
        "code": 0,
        "data": {
        }
    }
    try {
        let resData = req.body;
        console.log('手机注册', resData);
        let phone = resData.phone.replace(/\s/g, '')
        let password = resData.password.replace(/\s/g, '')
        let otp = resData.otp.replace(/\s/g, '')
        let cid = resData.cid ? resData.cid : '1'
        let parent_id = resData.code ? resData.code : '0';
        let aaid = resData.aaid || '';

        if (password.length < 6) {
            data['code'] = 6
            res.send(data)
            return
        }
        // 如果该用户已注册
        let user = await userDataUtil.get_user_by_phone(phone)
        if (user) {
            if (otp != OTP_CODE) {
                let con = await redis.get(phone)
                if (con == null) {
                    data['code'] = 12
                    res.send(data)
                    return
                }
                if (con != String(otp)) {
                    data['code'] = 13
                    res.send(data)
                    return
                }
            }
            user['user_token'] = await userDataUtil.return_user_login_token(user['uid'], req.realIp)
            data['code'] = 1
            data['data'] = await userDataUtil.return_user_data(user)
            res.send(data)
            return
        }
        let ip = req.realIp
        let user_ip = await userDataUtil.get_user_ip_num(ip)
        let limit_ip = await redis.hget("san_game_all_conf", "user_ip_max_num") || 999
        if (parseInt(user_ip) > parseInt(limit_ip)) {
            data['code'] = 101
            res.send(data)
            return
        }
        if (otp != OTP_CODE) {
            let con = await redis.get(phone)
            if (con == null) {
                data['code'] = 12
                res.send(data)
                return
            }
            if (con != String(otp)) {
                data['code'] = 13
                res.send(data)
                return
            }
        }
        const utils = new Utils()
        // 用户名称
        let nickname = utils.random_str(5)
        // 用户id
        let uid = nanoid(10).replace(/-/g, '_');
        let sqlDat = await add_phone_new_user(uid, phone, password, nickname, cid, parent_id, ip, aaid)
        if (sqlDat['res'] != 0) {
            let maps = {
            }
            await singReturnUserData(maps, uid, nickname, sqlDat['give_money'], sqlDat['remain_code_amount'], cid, 1, req.realIp)
            data['data'] = maps
            data['code'] = 1
        }
    } catch (error) {
        console.log(error);
    }
    res.send(data)
    return
})

// 邮箱注册
router.all('/api/user_email_register', async (req, res) => {
    let data = {
        "code": 0,
        "data": {
        }
    }
    try {
        let resData = req.body
        let email = resData.email.replace(/\s/g, '')
        let password = resData.password.replace(/\s/g, '')
        let cid = resData.cid ? resData.cid : '1'
        let parent_id = resData.code ? resData.code : '0';
        let aaid = resData.aaid || '';
        if (password.length < 6) {
            data['code'] = 6
            res.send(data)
            return
        }
        // 如果该用户已注册 直接return
        let user = await userDataUtil.get_user_by_email(email)
        if (user) {
            data['code'] = 41
            res.send(data)
            return
        }
        let ip = req.realIp
        let user_ip = await userDataUtil.get_user_ip_num(ip)
        let limit_ip = await redis.hget("san_game_all_conf", "user_ip_max_num") || 999
        if (parseInt(user_ip) > parseInt(limit_ip)) {
            data['code'] = 101
            res.send(data)
            return
        }
        const utils = new Utils()
        // 用户名称
        let nickname = utils.random_str(5)
        // 用户id
        const uid = nanoid(10).replace(/-/g, '_');
        let sqlDat = await add_email_new_user(uid, email, password, nickname, cid, parent_id, ip, aaid)
        if (sqlDat['res'] != 0) {
            let maps = {
            }
            await singReturnUserData(maps, uid, nickname, sqlDat['give_money'], sqlDat['remain_code_amount'], cid, 2, req.realIp)
            data['data'] = maps
            data['code'] = 1
        }
    } catch (error) {
        console.log(error);
    }

    res.send(data)
})


// 用户注册信息返回的内容
const singReturnUserData = async (maps, uid, nickname, give_money, remain_code_amount, cid, flag, ip) => {
    maps['uid'] = uid
    maps['token'] = await userDataUtil.return_user_login_token(uid, ip)
    maps['phone'] = ''
    maps['nickname'] = nickname
    maps['header_img'] = 0
    maps['money'] = give_money
    maps['commission'] = 0
    maps['total_money'] = 0
    maps['total_withdraw'] = 0
    maps['total_bet'] = 0
    maps['vip_lv'] = 0
    maps['is_first_pay'] = 1
    maps['cid'] = cid
    maps['sh'] = 0
    maps['new'] = 1
    maps['remain_code_amount'] = remain_code_amount
    maps['need_code_amount'] = remain_code_amount
    maps['with_money'] = 0
    maps['add_time'] = Time.formatDateHms(new Date())
    userDataUtil.update_user_day_num_data(cid, flag)
    userHourLogin(maps)
}


// 手机注册
const add_phone_new_user = async (uid, phone, password, nickname, cid, parent_id, ip, aaid) => {
    let give_money = 0
    let remain_code_amount = 0
    let res = 0
    let sqlDat = {
        "give_money": 0,
        "remain_code_amount": 0,
        "res": 0,
    }
    try {
        // 登录密码加密
        let pass_str = userDataUtil.add_storage_pass(String(phone), String(password))
        // 赠送金额
        give_money = await redis.hget('san_game_all_conf', 'bind_phone_money') || 0
        remain_code_amount = parseFloat(give_money) * 10
        // 获取父级信息
        const user = await userDataUtil.get_user_parent_id(parent_id)
        const super_id = user ? user['parent_id'] : '0'
        const super_parent_id = user ? user['super_id'] : '0'
        const util = new Utils()
        const aid = 1
        let sql = "insert into san_users(uid ,phone, password,login_password, nickname, register_ip, aid, cid, add_time, money,  remain_code_amount,  parent_id, super_id, super_parent_id, give_money, system_give, need_code_amount, device_info, aaid) values  (?, ?, ?, ?,?, ?, ?, ?, now(),? , ?,?,?,?,?,?,?, ? , ?)"
        const mysql = new Mysql()
        let res = await mysql.awaitSql(sql, [uid, phone, pass_str, password,
            nickname, ip, aid, cid, give_money, remain_code_amount, parent_id
            , super_id, super_parent_id, give_money, give_money, remain_code_amount, '', aaid])
        if (await res > 0) {
            // 获取今日日期
            let day = Time.formatDate(new Date)
            //今日注册人数 使用reids哈希记数 
            let user_day_key = day + "_user_ip_num"
            redis.hincrby(user_day_key, String(ip), 1)
            redis.expire(user_day_key, 86400 * 2)
            // 修改用户父级团队信息
            userDataUtil.update_user_team_data(user)
            if (parseFloat(give_money) > 0) {
                // 修改后余额
                let after_money = parseFloat(give_money)
                // 添加用户余额日志
                Common.user_money_log_func(res, give_money, 0, after_money, 12)
                Common.user_day_data_total(res, day, { give_money: give_money, system_give: give_money })
            }
            // if (parent_id != '0') {
            //     common.invite_user_ok(parent_id, res)
            // }
            sqlDat['res'] = res
            sqlDat['give_money'] = give_money
            sqlDat['remain_code_amount']
            return sqlDat
        }
    } catch (error) {
        console.log(error);
        return sqlDat
    }
}
// 邮箱注册
const add_email_new_user = async (uid, email, password, nickname, cid, parent_id, ip, aaid) => {
    let give_money = 0
    let remain_code_amount = 0
    let res = 0
    let sqlDat = {
        "give_money": 0,
        "remain_code_amount": 0,
        "res": 0,
    }
    try {
        // 登录密码加密
        let pass_str = userDataUtil.add_storage_pass(String(email), String(password))
        // 赠送金额
        give_money = await redis.hget('san_game_all_conf', 'bind_phone_money') || 0
        remain_code_amount = parseFloat(give_money) * 10
        // 获取父级信息
        const user = await userDataUtil.get_user_parent_id(parent_id)
        const super_id = user ? user['parent_id'] : 0
        const super_parent_id = user ? user['super_id'] : 0
        const util = new Utils()
        const aid = 1
        let sql = "insert into san_users(uid ,email, password,login_password, nickname, register_ip, aid, cid, add_time, money,  remain_code_amount,  parent_id, super_id, super_parent_id, give_money, system_give, need_code_amount, device_info, aaid) values  (?, ?, ?, ?,?, ?, ?, ?, now(),? , ?,?,?,?,?,?,?, ?,? )"
        const mysql = new Mysql()
        let res = await mysql.awaitSql(sql, [uid, email, pass_str, password,
            nickname, ip, aid, cid, give_money, remain_code_amount, parent_id
            , super_id, super_parent_id, give_money, give_money, remain_code_amount, '', aaid])
        if (await res > 0) {
            // 获取今日日期
            let day = Time.formatDate(new Date)
            //今日注册人数 使用reids哈希记数 
            let user_day_key = day + "_user_ip_num"
            redis.hincrby(user_day_key, String(ip), 1)
            redis.expire(user_day_key, 86400 * 2)
            // 修改用户父级团队信息
            userDataUtil.update_user_team_data(user)
            if (parseFloat(give_money) > 0) {
                // 修改后余额
                let after_money = parseFloat(give_money)
                // 添加用户余额日志
                Common.user_money_log_func(res, give_money, 0, after_money, 12)
                Common.user_day_data_total(res, day, { give_money: give_money, system_give: give_money })
            }
            // if (parent_id != '0') {
            //     common.invite_user_ok(parent_id, res)
            // }
            sqlDat['res'] = res
            sqlDat['give_money'] = give_money
            sqlDat['remain_code_amount']
            return sqlDat
        }
    } catch (error) {
        console.log(error);
        return sqlDat
    }
}
// 用户日活处理
const userHourLogin = async (user) => {
    // 获取今日日期
    const day = new Date().toISOString().split('T')[0];
    // 获取当前小时
    const hour = new Date().getHours();
    // redisKye
    const rKey = "user_hour_login_key_" + String(day) + '_' + String(hour)
    redis.hget(rKey, String(user['uid'])).then((res) => {
        if (res == null) {
            userDataUtil.user_add_hour_func(user['cid'], 0, user['uid'])
            redis.hset(rKey, String(user['uid']), "1")
            redis.expire(rKey, 3600)
        }
    })
    userDataUtil.user_keep_func(user)
}


module.exports = router;