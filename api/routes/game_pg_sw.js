var express = require('express');
var router_pg_sw = express.Router();
const Mysql = require('../Mysql/mysql')
const Time = require('../utils/Date')
const redis = require('../Redis/index');
const axios = require('axios');
const crypto = require('crypto');
const currency = ""  //货币符号
const USER_BET_LOG_KEY = ''  //用户注单队列key
const Token = ""
const Secret = ""
const rate = 1000
const URL = ""
// PG用户登录
async function login_pg_user(user) {
    const data = {
        user_token: "",
        user_id: 0,
        code: 0
    };

    try {
        const maps = {
            operator_token: Token,
            init_amount: rate,
            user_id: user.uid,
            user_name: user.nickname,
            currency: currency,
            ts: Math.floor(Date.now()),
        };
        maps.sign = signData(maps, Secret)
        const response = await axios.post(`${URL}/api/web/user_session/`, maps);
        const content = response.data;
        if (content.status === 0) {
            data.user_token = content.data.token;
            data.user_id = content.data.user_id;
            data.code = 1;
        }
    } catch (error) {
        console.error(error);
    }

    return data;
}



// 获取 PG 游戏 URL
async function get_pg_game_url(user_id, user_token, game) {
    let game_url = "";
    try {
        const maps = {
            operator_token: Token,
            user_id: user_id,
            user_token: user_token,
            game_code: game.provider_game_id,
            language: "en",
            ts: Math.floor(Date.now()),
        };
        maps.sign = signData(maps, Secret) // 生成签名
        const response = await axios.post(`${URL}/api/web/game_url/`, maps);
        const content = response.data;
        if (content.code === 0) {
            game_url = content.url; // 获取游戏 URL
        }
    } catch (error) {
        console.error(error);
    }

    return game_url;
}



function signData(data, secret) {
    const sortedKeys = Object.keys(data).sort();
    const dataStr = sortedKeys.map(key => `${key}=${data[key]}`).join('&');
    const signature = crypto.createHash('md5').update(dataStr + `&key=${secret}`).digest('hex');
    return signature;
}

// 获取余额
router_pg_sw.all("/api/sw_pg/getBalance", async (req, res) => {
    let data = {}
    data['data'] = {}
    data['error'] = null
    try {
        resData = req.body
        if (resData.OperatorToken != Token || resData.SecretStr != Secret) {
            data['data'] = null
            data['error'] = 3202
            console.log("签名不对", data);
            return res.json(data)
        }
        let uid = resData.UseID
        const user = await get_user_info(uid)
        data['data']['currency_code'] = "BRL"
        data['data']['balance_amount'] = parseInt(user['money'] * rate)
        data['data']['updated_time'] = Math.floor(Date.now())
        data['error'] = null
        return res.json(data)
    } catch (error) {
        console.log(error);
    }

})
// 下注处理
router_pg_sw.all("/api/sw_pg/TransInOut", async (req, res) => {
    let data = {}
    data['data'] = {}
    data['error'] = {}
    try {
        let reqData = req.body
        let pg_back_operator_token = reqData.OperatorToken
        let pg_back_secret_key = reqData.SecretStr
        let uid = reqData.UseID
        let bet_amount = reqData.Bet / rate  // 下注金额
        let win_amount = reqData.Award / rate  //  赢分
        let transfer_amount = reqData.UpdateCredit / rate  // 实际输赢
        let game_id = reqData.GameID  // 游戏id
        let transaction_id = reqData.Term  // 局号

        if (pg_back_operator_token != Token || pg_back_secret_key != Secret) {
            data['data'] = null
            data['error'] = 3202
            console.log("签名不对", data);
            return res.json(data)
        }
        const user = await get_user_info(uid)
        let user_money = user['money']
        if (parseFloat(user_money) < parseFloat(bet_amount)) {
            data['data'] = null
            data['error']['code'] = "3202"
            data['error']['message'] = "余额不足无法投注"

            console.log(req.url, "\n", reqData, "\n", data)
            return res.json(data)
        }

        if (await redis.get("san_game_pg_bet_transaction_id" + String(transaction_id))) {
            data['data']['currency_code'] = currency
            data['data']['balance_amount'] = parseInt(user_money * rate)
            data['data']['updated_time'] = Math.floor(Date.now())
            data['error'] = null
            // console.log(req.url, "\n", reqData, "\n", data)
            return res.json(data)

        }
        const game = await get_game_data(game_id)
        if (!game) {
            data['data'] = null
            data['error']['code'] = "1402"
            data['error']['message'] = "游戏不存在"

            console.log(req.url, "\n", reqData, "\n", data)
            return res.json(data)
        }
        let resData = {}
        resData['transaction_id'] = transaction_id
        resData['game_id'] = game_id
        resData['bet_amount'] = bet_amount
        resData['win_amount'] = win_amount
        resData['transfer_amount'] = transfer_amount
        let Over = await user_bet_func(user, game, resData, user_money, req.realIp)
        if (Over['state'] == 1) {
            data['data']['currency_code'] = currency
            data['data']['balance_amount'] = parseInt(Over['balance'] * rate)
            data['data']['updated_time'] = Math.floor(Date.now())
            data['error'] = null

            // console.log(req.url, "\n", reqData, "\n", data)
            return res.json(data)
        } else {
            data['data'] = null
            data['error']['code'] = "3033"
            data['error']['message'] = "投注失败"

            console.log(req.url, "\n", reqData, "\n", data)
            return res.json(data)
        }
    } catch (error) {
        data['data'] = null
        data['error']['code'] = "1200"
        data['error']['message'] = "内部服务器错误"
        console.log(error);
        return res.json(data)
    }
})


// # 用户下注处理
async function user_bet_func(user, game, data, user_money, ip) {
    let resData = {
        "balance": user_money,
        "state": 0
    }
    let balance = user_money
    let amount = data['bet_amount']
    let win_amount = data['win_amount']
    let transfer_amount = data['transfer_amount']
    try {
        let after_money = parseFloat(balance) + parseFloat(transfer_amount)
        balance = after_money
        nickname = user['nickname']
        let maps = {}
        maps['day'] = Time.get_today_ymd()
        maps['uid'] = user['uid']
        maps['nickname'] = user['nickname'].replace('"', '').replace('"', '')
        maps['cid'] = user['cid']
        maps['aid'] = user['aid']
        maps['parent_id'] = user['parent_id']
        maps['super_id'] = user['super_id']
        maps['super_parent_id'] = user['super_parent_id']
        maps['gid'] = game['gid']
        maps['game_id'] = game['game_id']
        maps['my_game'] = game['my_game']
        maps['game_name'] = game['game_name']
        maps['game_type'] = game['game_type']
        maps['bet'] = amount
        maps['real_shu_ying'] = transfer_amount
        maps['shu_ying'] = win_amount
        maps['bet_num'] = 1
        maps['add_time'] = Time.formatDateHms(user['add_time'])
        maps['bet_time'] = Time.formatDateHms(Time.get_today())
        maps['game_number'] = data['transaction_id']
        maps['round_id'] = data['transaction_id']
        maps['before_money'] = user_money
        maps['after_money'] = after_money
        redis.rpush(USER_BET_LOG_KEY, JSON.stringify(maps))  // 用户注单数据
        user['money'] = after_money
        await set_user_info_redis(user)
        await updateMoneySql(maps)
        redis.setex("san_game_pg_bet_transaction_id" + String(data['transaction_id']), 3600 * 2, '1')
    } catch (error) {
        console.log(error);
    }
    resData['balance'] = balance
    resData['state'] = 1
    return resData
}



async function updateMoneySql(maps) {
    const sql = `update san_users set money = money + ${maps['real_shu_ying']}
                 where uid = "${maps['uid']}"`;
    const mysql = new Mysql();

    try {
        const res1 = await mysql.awaitSql(sql, null);
    } catch (e) {
        console.error(e);
    }
}

// 累计充值奖励  汇总
async function userTotalRechargeActivityBetNum(user) {
    const mysql = new Mysql();

    try {
        const sql = `insert into san_user_activity_total_data(uid, bet_num, parent_id)
                     values ("'${user['uid']}'", 1, "'${user['parent_id']}'")
                     ON DUPLICATE KEY UPDATE bet_num = bet_num + 1`;

        const res = mysql.sql(sql, null);
    } catch (e) {
        console.error(e);
    }
}
// 用户打码转轮打码量
async function userRollerAmount(uid, totalActivityBet) {
    try {
        const userBetRollerAmount = await redis.hget("user_bet_roller_amount", uid);

        let newUserBetRollerAmount = userBetRollerAmount ? parseFloat(userBetRollerAmount) : 0;
        newUserBetRollerAmount += totalActivityBet;

        redis.hset("user_bet_roller_amount", uid, newUserBetRollerAmount);
    } catch (e) {
        console.error(e);
    }
}

// 获取用户信息
async function get_user_info(uid) {
    const user_key = 'san_game_wj_game_user_conf_' + String(uid);

    // Check if data is present in Redis
    const redisData = await redis.get(user_key);
    if (redisData) {
        const res = JSON.parse(redisData);
        return res;
    }

    // Default currency
    const sql = `select * from san_users where uid = ?`;
    const mysql = new Mysql();
    const res = await mysql.getOne(sql, [uid]);

    if (res) {
        delete res['login_time'], res['face_id'], res['face_img'], res['face_email'], res['android_id'], res['aaid']
        res['add_time'] = Time.get_front_day_h_s(res['add_time'])

        // Set data in Redis with a TTL of 86400 seconds (1 day)
        await set_user_info_redis(res);
    }

    return res;
}

// 用户信息写入redis
async function set_user_info_redis(user) {
    const user_key = 'san_game_wj_game_user_conf_' + String(user['uid']);
    await redis.setex(user_key, 86400, JSON.stringify(user));
}

// 认证PG游戏
async function get_game_data(gameId) {
    const gameKey = `web_game_pg_game_data_info_${gameId}`;

    // 检查 Redis 中是否有缓存数据
    const redisData = await redis.get(gameKey);
    if (redisData) {
        const res = JSON.parse(redisData);
        return res;
    }

    // 如果缓存中没有数据，则从 MySQL 数据库中获取
    const sql = `select * from san_external_game_list where provider_id = '${gameId}' and my_game = 2`;
    const mysql = new Mysql();
    const res = await mysql.getOne(sql, null);

    // 如果从数据库中获取到数据，则将数据存入 Redis 缓存，并设置过期时间为 86400 秒 (1 天)
    if (res) {
        await redis.setex(gameKey, 86400, JSON.stringify(res));
    }
    return res;
}


module.exports = { login_pg_user, get_pg_game_url, router_pg_sw }