import { Module } from 'vuex';
import { startDataState, RootStateTypes } from '@/store/interface/index';

const helpModule: Module<startDataState, RootStateTypes> = {
	namespaced: true,
	state: {
		bonusCabinet: {
			loss_bonus_state: 0,
			refer_bonus_state: 0,
			roller_bonus_state: 0,
			sign_bonus_state: 0
		}
	},
	mutations: {
		getBonusCabinetData(state: any, data: object) {
			state.bonusCabinet = data
		},
	},
	actions: {
		async setBonusCabinetData({ commit, state }, data: object) {
			commit('getBonusCabinetData', data);
		},
	},
};

export default helpModule;
