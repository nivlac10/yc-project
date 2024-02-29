import { Module } from 'vuex';
import { helpState, RootStateTypes } from '@/store/interface/index';

const helpModule: Module<helpState, RootStateTypes> = {
	namespaced: true,
	state: {
        index:[0,0],
	},
	mutations: {
        setIndex(state: any, data: any) {
			state.index = data;
		},
	},
	actions: {
	},
};

export default helpModule;
