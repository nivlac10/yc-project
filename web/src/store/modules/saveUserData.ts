/*
 * @Author: haosan 123@qq.com
 * @Date: 2023-06-21 15:05:27
 * @LastEditors: haosan 123@qq.com
 * @LastEditTime: 2023-08-28 15:53:29
 * @FilePath: \web1.1\src\store\modules\saveUserData.ts
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import { Module } from 'vuex';
import { saveUserDataState, RootStateTypes } from '@/store/interface/index';

const saveUserDataModule: Module<saveUserDataState, RootStateTypes> = {
	namespaced: true,
	state: {
		accountNumber: {
			phone: '',
			password: ''
		}, // 账号
		withdrawalSettings: {} // 提款设置
	},
	mutations: {
		getAccountNumber(state: any, data: boolean) {
			state.accountNumber = data;
		},
		getWithdrawalSettings(state: any, data: boolean) {
			state.withdrawalSettings = data;
		},
	},
	actions: {
		// 设置用户账号
		async setAccountNumber({ commit }, data: boolean) {
			commit('getAccountNumber', data);
		}, 
		// 提款设置 
		async setWithdrawalSettings({ commit }, data: boolean) {
			commit('getWithdrawalSettings', data);
		},
	},
};

export default saveUserDataModule;
