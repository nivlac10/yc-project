/*
 * @Author: wawodel 69891926+wawodel@users.noreply.github.com
 * @Date: 2023-08-29 12:38:30
 * @LastEditors: wawodel 69891926+wawodel@users.noreply.github.com
 * @LastEditTime: 2023-12-28 15:46:21
 * @FilePath: \web1.1\src\store\modules\vipBonusState.ts
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import { Module } from 'vuex';
import { vipBonusState, RootStateTypes } from '@/store/interface/index';
import { UserService } from '@/api/user';
import { VipService } from '@/api/vip';

const helpModule: Module<vipBonusState, RootStateTypes> = {
	namespaced: true,
	state: {
		split_time: '00:00',
		now_time: '00:00',
		day_time: '00:00',
		day_bonus: {
			money: 0,
			state: 0,
			time: 0
		},
		month_bonus: {
			money: 0,
			state: 0
		},
		now_bonus: {
			money: 0,
			state: 0,
			time: 0
		},
		week_bonus: {
			money: 0,
			state: 0
		},
		split_bonus: {
			money: 0,
			state: 0,
			time: 0,
			wait_money: 0,
			total_money: 0,
		},
		lv_up_bonus: {
			state: 0
		},
		bonus_num: 0,
		badgeShow: false,
		sgin_data: {},
	},
	mutations: {
		getData(state: any, data: Array<object>) {
			state = data
		},
		init_sgin_data(state: any,data: Array<object>) {
			state.sgin_data = data
		},
	},

	actions: {
		async setData({ commit, state }, data: any) {
			for (const key in data) {
				state[key] = data[key];
			}
			commit('getData', { ...state });
		},
		async init_sgin_data({ commit, state }, data: any) {
			const now = new Date();
			const midnight = new Date(
				now.getFullYear(),
				now.getMonth(),
				now.getDate() + 1, // 将日期设置为明天
				0, 0, 0, 0
			);
			let sginData  = await	UserService.get_sign_list();
			sginData.data['time'] = Math.floor((midnight.getTime() - now.getTime()) / 1000);
			commit('init_sgin_data', sginData.data);
		},
	},
};



export default helpModule;
