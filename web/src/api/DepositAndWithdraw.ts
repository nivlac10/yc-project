import { get, post } from "@/utils/http";

export class DepositAndWithdraw {
	static pay = (params?: object) => post('/user_pay', params);
    static withdraw = (params?: object) => post('/user_money_withdraw_func', params);
    static get_user_order_list = (params?: object) => post('/get_user_order_list', params);
    static get_user_order_withdraw_list = (params?: object) => post('/get_user_order_withdraw_list', params);
    static get_recharge_activity = (params?: object) => post('/get_recharge_activity', params);
}
