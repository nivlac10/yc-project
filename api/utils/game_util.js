const Mysql = require('../Mysql/mysql');
const constant = require("../constant");
const { nanoid } = require('nanoid');
const axios = require('axios');
const querystring = require('querystring');

class game_util {
    // PG 登录游戏
    static async pg_get_game_url(user, game, ip, token) {
        let data = {}
        data['code'] = 0
        data['url'] = ""
        try {

            let game_url = constant.PG_conf['url'] + "/external-game-launcher/api/v1/GetLaunchURLHTML?trace_id=" + nanoid(20);
            let maps = {
                operator_token: constant.PG_conf['operator_token'],
                path: `/${game['provider_game_id']}/index.html`,
                extra_args: { btt: 1, ops: token, l:"en" },
                url_type: 'game-entry',
                client_ip: ip,
            }
            maps.extra_args = querystring.stringify(maps.extra_args);
            const formData = querystring.stringify(maps);
            let res = await axios.post(game_url, formData, {
                headers: {
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                timeout: 10000,
            })
            data['code'] = 1
            data['url'] = res.data
            return data
        } catch (error) {
            console.log(error);
        }
        return data
    }





    static async seamless_out_login_user_game(uid) {
        let sql = `update san_users set cur_gameid = 0 where uid = "${uid}"`
        const mysql = new Mysql()
        let res = await mysql.sql(sql, null)
        // mysql.dispose()
        return res ? true : false
    }
    static async seamless_login_user_game(uid, game) {
        let game_time = parseInt(new Date().getTime() / 1000);
        let sql = "update san_users set cur_gameid = ?, game_time = ? where uid = ?"
        const mysql = new Mysql()
        mysql.sql(sql, [game['gid'], game_time, uid])
    }

}

module.exports = game_util