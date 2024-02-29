import { Module } from 'vuex';
import { userState, RootStateTypes } from '@/store/interface/index';

const userModule: Module<userState, RootStateTypes> = {
	namespaced: true,
	state: {
		commission: 0, //佣金
		first_pay_type: 0, //是否是首充
		header_img: 0,  //头像下标
		money: 0, //余额
		new: 0,
		nickname: '', //用户名
		phone: '', //手机号
		remain_code_amount: 0, //剩余打码量
		sh: '', //审核模式
		token: '',
		total_bet: 0, //总打码
		total_money: 0, //总充值
		total_withdraw: 0, //总提现
		uid: 0,
		vip_lv: 0,
		vip_low_lv: 1,
		with_money: 0, //可提现金额
		need_code_amount: 0,
		share_lv: 1,
		share_valid_number: 0,
		vip_day: 0,
		vip_earnings: 0,
		sign_bonus: 0,
		team_one_user_num: 0,
		total_commission: 0,
		CPF: "",
		username: "",
		give_money: 0,
		download_bonus: 0,
	},
	mutations: {
		getData(state: any, data: Array<object>) {
			state = data
		},
	},
	actions: {
		async setData({ commit, state }, data: any) {
			for (const key in data) {
				state[key] = data[key];
			}
			commit('getData', { ...state });
		},
	},
};

export default userModule;
