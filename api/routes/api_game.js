var express = require('express');
var router = express.Router();
const userDataUtil = require('../utils/userDataUtil');
const redis = require('../Redis/index');
const Mysql = require('../Mysql/mysql')
const auth = require('../middleware/auth')
const game_util = require('../utils/game_util')
const constant = require("../constant");
const Time = require('../utils/Date');
const utils = require('../utils/utils');
const { login_pg_user, get_pg_game_url } = require("./game_pg_sw")


router.all('/api/get_game_play_url', auth, async (req, res) => {
    const data = {}
    data['code'] = 0
    data['url'] = ''
    try {
        let uid = req.uid
        let gid = req.body.gid
        let token = req.body.token
        if (!uid) {
            data['code'] = 3
            return res.send(data)
        }
        const game = await get_wj_game(gid)
        // console.log(game);
        if (game == null) {
            data['code'] = 24
            return res.send(data)
        }
        const user = await userDataUtil.get_user_by_uid(uid)
        let user_key = 'san_game_wj_game_user_conf_' + String(user['uid'])
        delete user['login_time'], user['face_id'], user['face_img'], user['face_email'], user['android_id'], user['aaid']
        user['add_time'] = Time.get_front_day_h_s(user['add_time'])
        redis.setex(user_key, 86400, JSON.stringify(user))
        if (user['cur_gameid'] > 0) {
            let cgame = await get_wj_game(user['cur_gameid'])
            if (cgame['my_game'] != game['my_game']) {
                let is_out = await wj_game_login_out(user, game)
                if (!is_out) {
                    data['code'] = 37  //游戏中
                    return res.send(data)
                }
            }
        } else {
            redis.setex(user_key, 86400, JSON.stringify(user))
        }
        if (game['my_game'] == 2) {
            let pg_user = await login_pg_user(user)
            // data['url'] = constant.PG_conf['Game_Url'] + `/${game['provider_game_id']}/index.html?ot=${constant.PG_conf['operator_token']}&ops=${token}&btt=1&l=zh`
            if (pg_user['code'] == 1) {

                data['code'] = 1
                data['url'] = await get_pg_game_url(pg_user['user_id'], pg_user['user_token'], game)
                game_util.seamless_login_user_game(user['uid'], game)
            }
            return res.send(data)
        }
    } catch (error) {
        console.log(error);
    }

    return res.send(data)



})



// # 获取游戏
async function get_wj_game(gid) {
    let game_list = JSON.parse(await redis.get('game_task_list')) || []
    if (game_list.length == 0) {
        let sql = "select * from san_external_game_list"
        let mysql = new Mysql()
        res = mysql.getAll(sql, null)
        if (res) {
            redis.setex("game_task_list", 1800, JSON.stringify(res))
            game_list = res
        }
    }
    if (game_list) {
        for (let i = 0; i < game_list.length; i++) {
            const element = game_list[i];
            if (element['gid'] == gid) {
                return element
            }
        }
    }
    return null
}

// 外接游戏退出
async function wj_game_login_out(user, game) {
    // if (game == null || game['my_game'] != 2) {
    game_util.seamless_out_login_user_game(user['uid'])
    return true
    // }
    // if (game['my_game'] == 2) {
    //     let url = constant.PG_conf['Game_Url'] + `/${game['']}`
    // }
}
module.exports = router