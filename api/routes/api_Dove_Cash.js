/*
 * @Author: wawodel 69891926+wawodel@users.noreply.github.com
 * @Date: 2024-01-26 14:23:37
 * @LastEditors: wawodel 69891926+wawodel@users.noreply.github.com
 * @LastEditTime: 2024-01-26 16:34:51
 * @FilePath: \express-admin\routes\api_Dove_ Cash.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */

const RKEY = require('../RKEY')
var express = require('express');
var router = express.Router();
const Time = require('../utils/Date');
const userDataUtil = require('../utils/userDataUtil');
//签名密钥
const serverkey = 'lLmDU32YaE';
const crypto = require('crypto');
//通过设备信息获取游戏信息
router.get('/channel/v1/device1', async (req, res) => {
    let resData = req.query;
    let successData = {
        code: '',//0是请求成功
        msg: '',
        data: {
            gmuser_id: '',//游戏用户ID 
            gmuser_name: '',//游戏用户名称
            gmuser_type: '',//游戏用户类型（0是新用户，1是老用户）
            gmrole_value: '',//游戏角色充值（单位：卢比）
            gmrole_time: '',//游戏角色创建时间
        },
    }

    let errData = {
        status: 'error',
        errmsg: '',//失败原因
    }
    if (!resData.gpcadid) {
        return res.send(errData)
    }
    let Sign = getSign(resData.appid, resData.campaign, resData.channelid, resData.gpcadid, resData.adid);
    if (Sign !== resData.sign) {
        errData.errmsg = 'sign 不正确';
        return res.send(errData)
    }
    let user = await userDataUtil.get_user_by_aaid(resData.gpcadid);
    if (user) {
        successData.code = 0
        successData.msg = "success"
        successData.data = returnUserData(user)
        return res.send(successData)
    } else {
        errData.errmsg = '未找到关联用户';
        return res.send(errData)
    }
})

//通过游戏用户ID获取游戏信息
router.get('/channel/v1/user1', async (req, res) => {
    req.body.appid = 1;
    let resData = req.query;
    let successData = {
        code: '1',//0是请求成功
        msg: '',
        data: {
        },
    }

    let errData = {
        status: 'error',
        errmsg: '',//失败原因
    }
    let user = await userDataUtil.get_user_by_uid(resData.gmuserid);
    if (user) {
        let Sign = getUserSign(resData.appid, resData.campaign, resData.channelid, user['uid'])
        if (Sign !== resData.sign) {
            errData.errmsg = 'sign 不正确';
            return res.send(errData)
        }
        successData.code = 0
        successData.msg = "success"
        successData.data = returnUserData(user)
        return res.send(successData)
    } else {
        errData.errmsg = '未找到关联用户';
        return res.send(errData)
    }


})
function returnUserData(user) {
    let day = Time.get_today_ymd()
    let user_day = Time.formatDateHms(user['add_time']).slice(0, 10);
    let new_user_flag = (day === user_day) ? 0 : 1;
    let data = {
        gmuser_id: user.uid,
        gmuser_name: user.nickname,
        gmuser_type: new_user_flag,
        gmuser_value: user.total_money,
        gmrole_time: Time.days_int(user.add_time) * 1000
    }
    return data
}

//Dove Cash签名

function getSign(appid, campaign, channelid, gpcadid, adid) {
    const data = appid + campaign + channelid + gpcadid + adid + serverkey;
    const md5Hash = crypto.createHash('md5');
    md5Hash.update(data);
    return md5Hash.digest('hex');
}
function getUserSign(appid, campaign, channelid, uid) {
    const data = appid + campaign + channelid + uid + serverkey;
    const md5Hash = crypto.createHash('md5');
    md5Hash.update(data);
    return md5Hash.digest('hex');
}
module.exports = router;

