const Mysql = require('../Mysql/mysql')
const redis = require('../Redis/index')
const auth = require('../middleware/auth')
const Time = require('../utils/Date')
const userDataUtil = require('../utils/userDataUtil');
const Common = require('../utils/common')
const moment = require('moment');

class orders_callback {

    static async pay_callback_func(order, user, status, pay_order_id, pay_money) {
        try {
            let money = parseFloat(pay_money)
            let give_money = 0  //赠送金额
            let ratio = 1  // 赠送打码倍率
            let first_pay = 0 //# 订单类型  0普通订单  1 首充订单  2 每日首充订单
            let activity_send_money = 0
            if (status == 1) {
                let day = Time.formatDateHms(new Date())
                this.add_user_sign_state(user['uid'], day)
                this.user_hour_report(user['cid'], user['uid'], day, money)
                if (user['parent_id'] != '0' && user['total_money'] <= 0) {
                    Common.recharge_give_parent_money(user['parent_id'], user['uid'])
                }
                if (order['bonus_type'] == 1) {
                    let activityRes = await this.recharge_activity_award(order, user)
                    first_pay = activityRes.first_pay
                    activity_send_money = activityRes.give_money
                    if (activityRes.bet_rate > 0) {
                        ratio = activityRes.bet_rate
                    }
                    give_money = activity_send_money
                }
                // # 用户是否参数充值活动
                this.update_payment_status(order, status, pay_order_id, pay_money, first_pay, activity_send_money)
                this.update_money_func(order, give_money, ratio, user, first_pay)
            } else {
                this.update_payment_status(order, status, pay_order_id, pay_money, first_pay, activity_send_money)
            }
        } catch (error) {
            console.log(error);
        }
    }

    static async add_user_sign_state(uid, today) {
        let receive_state_key = "sign_receive_state_key_" + String(today)
        let sign_state_day = await redis.hget(receive_state_key, String(uid))
        if (sign_state_day) {
            redis.hset(receive_state_key, String(uid), "1")
            redis.expire(receive_state_key, 86400)
        }
    }

    static async user_hour_report(cid, uid, day, money) {
        // 创建一个新的 Date 对象，表示当前时间
        const currentDate = new Date();
        // 获取当前小时
        const hour = currentDate.getHours();
        let pay_hour_key = 'pay_hour_key_' + String(day) + '_' + String(hour)
        if (!(await redis.hget(pay_hour_key, String(uid)))) {
            userDataUtil.user_add_hour_func(cid, 3, uid)
        }
        userDataUtil.user_add_hour_func(cid, 2, uid)
        userDataUtil.user_add_hour_func(cid, 4, uid, parseFloat(money))
    }




    static async recharge_activity_award(order, user) {
        // 获取redis中存在的活动
        const recharge_list = JSON.parse(await redis.get('san_game_pay_action_conf')) || [];
        const money = order.money;
        let give_money = 0;
        let now_code = 0;
        let bet_rate = 0;
        const day = moment(order.add_time).format('YYYY-MM-DD');
        const fist_give_key = 'first_recharge_give_money_flag_' + day;
        let first_pay = 0;

        if (recharge_list.length !== 0) {
            const now_time = Math.floor(Date.now() / 1000);

            for (const item of recharge_list) {
                // 校验当前时间是否满足活动条件
                if (now_time < item.over_time && now_time > item.start_time) {
                    let send_money = 0;  // 赠送金额
                    let ladder_id = 0;  // 阶梯id

                    if (user.first_recharge == 0) {
                        // 判断活动类型  0范围 1 阶梯
                        if (item.scope.length > 0 && item.recharge_activity_type === 2) {
                            for (const d of item.scope) {
                                if (parseFloat(d.min_recharge) <= parseFloat(money) && parseFloat(d.max_recharge) >= money) {
                                    const rate = parseFloat(d.send_rate) / 100;
                                    send_money = parseFloat(money) * rate;
                                    ladder_id = d.id;
                                }
                            }
                        }

                        if (item.step.length > 0 && item.recharge_activity_type === 3) {
                            for (const d of item.step) {
                                if (parseFloat(d.recharge_amount) === money) {
                                    const rate = parseFloat(d.send_rate) / 100;
                                    send_money = parseFloat(money) * rate;
                                    ladder_id = d.id;
                                }
                            }
                        }

                        first_pay = 1;
                        redis.hset(fist_give_key, String(user.uid), '1');
                        redis.expire(fist_give_key, 86400);
                    } else {
                        let is_fist_key = await redis.hget(fist_give_key, String(user.uid))
                        console.log(fist_give_key, String(user.uid), await redis.ttl(fist_give_key));
                        if (!is_fist_key) {
                            // 判断活动类型  0范围 1 阶梯
                            if (item.scope.length > 0 && item.recharge_activity_type === 0) {
                                for (const d of item.scope) {
                                    if (parseFloat(d.min_recharge) <= parseFloat(money) && parseFloat(d.max_recharge) >= money) {
                                        const rate = parseFloat(d.send_rate) / 100;
                                        send_money = parseFloat(money) * rate;
                                        ladder_id = d.id;
                                    }
                                }
                            }

                            if (item.step.length > 0 && item.recharge_activity_type === 1) {
                                for (const d of item.step) {
                                    if (parseFloat(d.recharge_amount) === money) {
                                        const rate = parseFloat(d.send_rate) / 100;
                                        send_money = parseFloat(money) * rate;
                                        ladder_id = d.id;
                                    }
                                }
                            }

                            first_pay = 2;
                            redis.hset(fist_give_key, String(user.uid), '1');
                            redis.expire(fist_give_key, 86400 * 2);
                        }
                    }

                    // 赠送金额大于0执行以下操作
                    if (send_money > 0) {
                        give_money += send_money;
                        now_code += parseFloat(send_money) * parseInt(item.bet_rate);
                        bet_rate = item.bet_rate;
                        this.insert_recharge_activity_log(user.uid, send_money, item.recharge_activity_id,
                            item.recharge_activity_type, ladder_id, order);
                        // 上述 insert_recharge_activity_log 方法需要根据实际情况进行定义
                    }
                }
            }
        }
        // console.log(give_money, now_code, bet_rate, first_pay, user.first_recharge);
        return { give_money, now_code, bet_rate, first_pay };
    }


    // # 充值成功更新用户余额
    static async update_money_func(order, give_money, ratio, user, first_pay) {
        try {
            const mysql = new Mysql()
            let give_key = 'day_first_recharge_give'
            let sql_arr = []
            let update_money = parseFloat(give_money) + parseFloat(order['money'])
            let code_num = parseFloat(((give_money * parseInt(ratio) + parseFloat(order['money']))).toFixed(2))
            const now_code = (user.remain_code_amount <= 0) ? code_num : parseFloat(user.remain_code_amount) + code_num;
            const now_need_code = (user.remain_code_amount <= 0) ? code_num : parseFloat(user.need_code_amount) + code_num;
            let day = Time.formatDate(order['add_time'])
            console.log(`充值金额：${order['money']} 赠送金额：${give_money} 打码倍率：${ratio} 当前打码量:${now_code} , 需求打码量： ${now_need_code}, 用户余额：${user['money']}, 充值用户id:${user['uid']}, 日期：${day}`);
            let sql1 = `update san_users set money = money + ${update_money}, total_money = total_money + ${order['money']}, 
            remain_code_amount = ${now_code},need_code_amount = ${now_need_code}, give_money = give_money + ${give_money} `
            if (first_pay == 1) {
                sql1 += ", first_recharge = 1, first_recharge_give = " + String(give_money)
                give_key = "first_recharge_give"
            }
            if (give_money > 0 && first_pay == 2) {
                sql1 += ", day_first_recharge_give = day_first_recharge_give + " + String(give_money)
            }
            sql1 += ` where uid = "${user['uid']}"`
            let sql2 = `insert into san_user_team_day_report(uid, day, total_recharge, recharge_num, ${give_key}, give_money) values
            ('${user['uid']}', '${day}', '${order['money']}', 1, '${give_money}', '${give_money}') ON DUPLICATE KEY UPDATE total_recharge = total_recharge + '${order['money']}',
            recharge_num = recharge_num + 1, ${give_key} = ${give_key} + '${give_money}', give_money = give_money + '${give_money}'`
            // # 累计充值奖励  汇总
            let sql3 = ` insert into san_user_activity_total_data(uid, total_money, parent_id)  
            values ('${user['uid']}', '${order['money']}', '${user['parent_id']}') ON DUPLICATE KEY UPDATE  
            total_money = total_money + '${order['money']}'`
            sql_arr.push(sql1)
            sql_arr.push(sql2)
            sql_arr.push(sql3)
            mysql.affairs(sql_arr)
            let before_money = user['money']
            let after_money = before_money + order['money']
            let money_type = 0   //# 充值
            Common.user_money_log_func(user['uid'], order['money'], before_money, after_money, money_type)
            if (first_pay != 0) {
                let g_before_money = after_money
                let g_after_money = g_before_money + give_money
                let g_money_type = first_pay == 1 ? 6 : 5
                Common.user_money_log_func(user['uid'], give_money, g_before_money, g_after_money, g_money_type)
            }
            this.update_user_team_func(order, user, day)
        } catch (error) {
            console.log(error);
        }
    }
    // # 团队数据处理
    static async update_user_team_func(order, user, day) {
        let sql_arr = []
        const mysql = new Mysql()
        if (user['parent_id'] != '0') {
            try {
                let team_key = 'slot_pub_team_one_recharge_' + day
                let user_num = await redis.hget(team_key, String(user['uid']))
                user_num = user_num ? 0 : 1
                let sql_p = `
                insert into san_user_team_day_report(uid, day, team_one_recharge, team_one_recharge_user_num) 
                    values ("${user['parent_id']}", "${day}", "${order['money']}", "${user_num}") ON DUPLICATE KEY UPDATE 
                    team_one_recharge = team_one_recharge + "${order['money']}", 
                    team_one_recharge_user_num = team_one_recharge_user_num + "${user_num}"
                    `
                sql_arr.push(sql_p)
                let sql_pu = `update san_users set team_one_recharge = team_one_recharge + "${order['money']}" where uid = "${user['parent_id']}"`
                sql_arr.push(sql_pu)
                if (user_num == 1) {
                    redis.hset(team_key, String(user['uid']), '1')
                    redis.expire(team_key, 86400)
                }
            } catch (error) {
                console.log(error);
            }
        }
        if (user['super_id'] != '0') {
            try {
                let team_key = 'slot_pub_team_two_recharge_' + day
                let user_num = await redis.hget(team_key, String(user['uid']))
                user_num = user_num ? 0 : 1
                let sql_p = `
                insert into san_user_team_day_report(uid, day, team_two_recharge, team_two_recharge_user_num) 
                    values ("${user['super_id']}", "${day}", "${order['money']}", "${user_num}") ON DUPLICATE KEY UPDATE 
                    team_two_recharge = team_two_recharge + "${order['money']}", 
                    team_one_recharge_user_num = team_one_recharge_user_num + "${user_num}"
                    `
                sql_arr.push(sql_p)
                let sql_pu = `update san_users set team_two_recharge = team_two_recharge + "${order['money']}" where uid = "${user['super_id']}"`
                sql_arr.push(sql_pu)
                if (user_num == 1) {
                    redis.hset(team_key, String(user['uid']), '1')
                    redis.expire(team_key, 86400)
                }
            } catch (error) {
                console.log(error);
            }
        }
        if (user['super_parent_id'] != '0') {
            try {
                let team_key = 'slot_pub_team_three_recharge_' + day
                let user_num = await redis.hget(team_key, String(user['uid']))
                user_num = user_num ? 0 : 1
                let sql_p = `insert into san_user_team_day_report(uid, day, team_three_recharge, team_three_recharge_user_num) 
                    values ("${user['super_parent_id']}", "${day}", "${order['money']}", "${user_num}") ON DUPLICATE KEY UPDATE 
                    team_three_recharge = team_three_recharge + "${order['money']}", 
                    team_one_recharge_user_num = team_one_recharge_user_num + "${user_num}"
                    `
                sql_arr.push(sql_p)
                let sql_pu = `update san_users set team_three_recharge = team_three_recharge + "${order['money']}" where uid = "${user['super_parent_id']}"`
                sql_arr.push(sql_pu)
                if (user_num == 1) {
                    redis.hset(team_key, String(user['uid']), '1')
                    redis.expire(team_key, 86400)
                }
            } catch (error) {
                console.log(error);
            }
        }
        try {
            // console.log(sql_arr);
            mysql.affairs(sql_arr)
        } catch (error) {
            console.log(error);
        }
    }

    // # 添加充值活动日志
    static async insert_recharge_activity_log(uid, send_money, recharge_activity_id, recharge_activity_type, ladder_id, order) {
        let sql = "insert into san_recharge_activity_log(uid, recharge_activity_id, ladder_id, recharge_money, send_amount," +
            "  order_id, recharge_activity_type, add_time) values(?, ?, ?, ?, ?, ?, ? ,Now())"
        const mysql = new Mysql()
        mysql.sql(sql, [uid, recharge_activity_id, ladder_id, order['money'], send_money, order['order_number'],
            recharge_activity_type])
    }

    // # 更新订单状态
    static async update_payment_status(order, status, pay_order_id, pay_money, first_pay, activity_send_money) {
        let success_time = Time.formatDateHms(new Date)
        const sql = "update san_order_list set status = ?, amount = ?, success_time = ?, pay_order_number = ?, " +
            " notify_time = now(), first_pay = ?, activity_send_money = ? where id = ? "
        const mysql = new Mysql()
        try {
            mysql.sql(sql, [status, pay_money, success_time, pay_order_id, first_pay, activity_send_money, order['id']])
        } catch (error) {
            console.log(error);
        }
    }
}

module.exports = orders_callback