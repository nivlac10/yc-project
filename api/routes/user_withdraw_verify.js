const Time = require('../utils/Date')
const redis = require('../Redis/index')
const Mysql = require('../Mysql/mysql')
const RKEY = require('../RKEY')
const common = require('../utils/common')
const userDataUtil = require('../utils/userDataUtil')
class user_withdraw_verify {
    /**
     * @description: 用户身份验证
     * @param {*} uid 用户uid
     * @param {*} money 用户提现申请金额
     * @param {*} money_type
     * @return {*}
     */
    static async user_info_verify(uid, money, money_type, ip, cpf) {
        var data = {};
        data['code'] = 0;
        data['uid'] = 0;
        data['add_time'] = '';
        data['money'] = 0;
        data['cid'] = 0;
        data['aid'] = 0;
        data['is_auto'] = 1;
        data['with_num'] = 0;
        data['audit_remark'] = '';
        data['commission'] = 0;
        data['vip_lv'] = {};
        data['msg'] = '';

        if (['0', '1'].indexOf(String(money_type)) === -1) {
            return data;
        }

        var user_withdraw_life = 'san_game_user_withdraw_life_time_' + uid;

        if (await redis.get(user_withdraw_life)) {
            data['code'] = 40;
            data['msg'] = 'Aguarde alguns segundos antes de enviar!';
            return data;
        }

        redis.setex(user_withdraw_life, 12, '1')

        var user = await userDataUtil.get_user_by_uid(uid);

        if (!user) {
            data['code'] = 3;
            return data;
        }

        if (user['vip_lv'] < 0 || user['vip_lv'] > 9) {
            data['code'] = 3;
            return data;
        }
        // 获取vip信息
        let vipData = await this.get_vip_lv_list_data();
        data['vip_lv'] = vipData[user['vip_lv']]
        if (money_type == 0) {
            let with_num = await this.get_user_day_order_num(user['uid']);
            data['with_num'] = with_num['num'];
            console.log("用户提现 用户id：" + uid + "今日成功提现金额与次数", with_num['num'], with_num['money']);

            if (data['vip_lv']['day_max_withdraw'] < parseFloat(money) && String(money_type) === '0') {
                data['msg'] = 'please increase your vip_lv level';
                data['code'] = 201;
                return data;
            }

            if (with_num['num'] >= data['vip_lv']['withdraw_num'] && String(money_type) === '0') {
                data['msg'] = "Today's submission limit has been reached";
                data['code'] = 202;
                return data;
            }
        }
        if (money_type == 1) {
            let commission_with_num = await this.get_user_day_commission_order_num(user['uid']);
            if (commission_with_num['num'] > 0) {
                data['msg'] = "Today's submission limit has been reached";
                data['code'] = 203;
                return data;
            }
        }

        if (user['total_money'] === 0 && String(money_type) === '0') {
            data['code'] = 26;
            var info = '用户没有充值记录';
            common.add_user_withdraw_log(user['uid'], info, ip);
            var user_info = 'Withdrawal requires a successful recharge record';
            this.send_user_email(user['uid'], user_info);
            return data;
        }

        if (String(money_type) === '1' && parseFloat(money) > user['commission']) {
            data['code'] = 23;
            return data;
        }

        if (String(money_type) !== '1') {
            var remain_code_amount = parseFloat(user['remain_code_amount']);

            if (remain_code_amount > 0) {
                data['code'] = 25;
                return data;
            }

            if (parseFloat(user['money']) < parseFloat(money)) {
                data['code'] = 23;
                var info = '可提现金额' + user['money'] + ' 小于申请提现金额' + money;
                common.add_user_withdraw_log(uid, info, ip);
                return data;
            }
        }

        data['code'] = 1;
        data['uid'] = user['uid'];
        data['add_time'] = String(user['add_time']);
        data['money'] = user['money'];
        data['cid'] = user['cid'];
        data['aid'] = user['aid'];
        data['commission'] = user['commission'];
        data['phone'] = user['phone'];
        data['email'] = user['email'];
        data['username'] = user['username'];
        data['CPF'] = cpf;
        data['total_money'] = user['total_money'];
        data['total_withdraw'] = user['total_withdraw'];
        data['pay_type'] = user['pay_type']
        data['parent_id'] = user['parent_id']
        data['super_id'] = user['super_id']
        data['super_parent_id'] = user['super_parent_id']
        data['total_commission'] = user['total_commission']
        return data;
    }

    // 查询当日用户提现的订单数
    static async get_user_day_order_num(uid) {
        let day = Time.formatDate(new Date())
        let stime = day + ' 00:00:00';
        let etime = day + ' 23:59:59';
        let sql = "select count(id) num, sum(money) money from san_withdraw_list where uid = '" + uid +
            "' and add_time >= '" + stime + "' and add_time <= '" + etime + "' and status = 1"

        let mysql = new Mysql()
        let res = await mysql.getOne(sql, null)
        if (res) {
            res['money'] = res['money'] || 0;
        }
        return res
    }
    // 查询当日用户提现的订单数
    static async get_user_day_commission_order_num(uid) {
        let day = Time.formatDate(new Date())
        let stime = day + ' 00:00:00';
        let etime = day + ' 23:59:59';
        let sql = "select count(*) num from san_withdraw_list where uid = '" + uid +
            "' and add_time >= '" + stime + "' and add_time <= '" + etime + "' and (status = 1 or status = 3)"
        console.log(sql);
        let mysql = new Mysql()
        let res = await mysql.getOne(sql, null)
        return res
    }
    // 获取vip等级数据
    static async get_vip_lv_list_data() {
        var vip_lv_list = await redis.get(RKEY.SAN_GAME_VIP_LV_LIST)
        var vip_list_data = []
        if (vip_lv_list) {
            vip_list_data = JSON.parse(vip_lv_list)
        }
        return vip_list_data
    }

    // 提现失败，发送通知
    static async send_user_email(uid, content) {
        let info = "Withdraw fail : " + content
        let title = 'System notification'
        let sql = "insert into san_user_message(uid, title, content, add_time) values (?, ?, ?, now())"
        const mysql = new Mysql()
        mysql.sql(sql, [uid, title, info])
    }

    // 更新用户余额
    static async update_user_money(uid, money, flag) {
        let sql
        if (flag == 0) {
            sql = "update san_users set money = money - ? where uid = ?"
        } else {
            sql = "update san_users set money = money + ? where uid = ?"
        }
        const mysql = new Mysql()
        const res = await mysql.awaitSql(sql, [money, uid])
        return res
    }

    // 更新用户佣金
    static async update_user_commission(uid, money, flag) {
        let sql;
        if (flag === 0) {
            sql = `update san_users set commission = commission - ${money} where uid = '${uid}'`;
        } else {
            sql = `update san_users set commission = commission + ${money} where uid = '${uid}'`;
        }
        const mysql = new Mysql()
        const res = await mysql.awaitSql(sql, null);
        return res;
    }

    // 更新提现订单状态
    static async update_order_info(order, money, status, success_time, return_msg, file_msg, order_number = '') {
        let sql = `update san_withdraw_list set status = '${status}', amount = '${money}', success_time = '${success_time}', notify_time = now()`;
        if (order_number) {
            sql += `, pay_order_number = '${order_number}'`;
        }
        sql += ` where id = '${order.id}'`;
        const mysql = new Mysql();
        const res = await mysql.awaitSql(sql, null);
        if (status != '1') {
            this.update_order_error_msg(order.id, return_msg);
        }
        if (res > 0 && status == '2') {
            const user = await userDataUtil.get_user_by_uid(order.uid);
            if (order.money_type == 0) {
                const after_money = parseFloat(user.money) + parseFloat(order.money);
                this.update_user_money(user.uid, order.money, 1);
                common.user_money_log_func(user.uid, order.money, user.money, after_money, 17);
                this.send_user_email(order.uid, file_msg);
            } else if (order.money_type == 1) {
                this.update_user_commission(user.uid, order.money, 1);
                const after_money = parseFloat(user.commission) + parseFloat(order.money);
                common.user_commission_log_func(user.uid, order.money, user.commission, after_money, 101);
                common.user_brokerage_log_func(user.uid, 0, 0, money, 6);
                this.send_user_email(order.uid, file_msg);
            }
        }
        return res;
    }

    // 更新订单错误信息
    static async update_order_error_msg(oid, msg) {
        const sql = "update san_withdraw_list set err_msg = ? where id = ?";
        const mysql = new Mysql()
        try {
            mysql.sql(sql, [msg, oid])
        } catch (e) {
            console.error(e);
        }
    }

    // 获取用户提现订单
    static async get_user_withdraw_detail(order_number) {
        const sql = `select * from san_withdraw_list where order_number = '${order_number}'`;
        const mysql = new Mysql()
        const res = await mysql.getOne(sql, null);
        return res;
    }

    // 更新用户提现订单成功后失败状态
    static async update_withdraw_order_status(order_id) {
        const sql = `update san_withdraw_list set status = 4 where id = '${order_id}'`;
        const mysql = new Mysql();
        const res = await mysql.update(sql, null);
        return res;
    }
}


module.exports = user_withdraw_verify