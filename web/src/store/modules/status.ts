import { Module } from 'vuex';
import { statusState, RootStateTypes } from '@/store/interface/index';

const statusModule: Module<statusState, RootStateTypes> = {
	namespaced: true,
	state: {
		loadingShow: false, // loading.....
		isPc: true, // 是否pc端
		sidebarIsShow: false, // 侧边栏显示
		loginShow: false, // 显示登录
		// userInfoShow: false, // 用户下拉信息显示
		showDeposito: false, //显示系统通知
		depositShow: false, // 显示提现
		showBonusConversion: false, // 显示奖金转余额
		showPayPop: false, //显示充值支付弹窗
		signInShow: true, // 显示签到 
		dailyBettingBonusShow: false, // 显示每日投注奖金
		supplyCrateShow: false, // 显示补给箱
		announcementShow: false,
		userInfoLoad: false,
		playIngState: false,
		isApk: false,
		ActivitySubpageDataIndex: 0,
		allGameShow: false,//所有游戏弹窗
		game_id: 1, //所有游戏弹窗游戏id
		rollerShow: false,//是否显示滚轮弹窗
		isBônusdepósito: false, //是否显示累计存款奖励
		noBônusdepósito: false,//是否不再显示累计存款奖励
		vipCheckIn: false,//是否显示签到页vip详情弹窗
	},
	mutations: {
		getLoadingShow(state: any, data: boolean) {
			state.loadingShow = data;
		},
		getrollerShow(state: any, data: boolean) {
			state.rollerShow = data;
		},
		getIsPc(state: any, data: boolean) {
			state.isPc = data;
		},
		getSidebarIsShow(state: any, data: boolean) {
			state.sidebarIsShow = data;
		},
		setShowDeposito(state: any, data: boolean) {
			state.showDeposito = data;
		},
		getDepositShow(state: any, data: boolean) {
			state.depositShow = data;
		},
		getUserInfoLoad(state: any, data: boolean) {
			state.userInfoLoad = data;
		},
		getPlayIngState(state: any, data: boolean) {
			state.playIngState = data;
		},
		getLoginShow(state: any, data: boolean) {
			state.loginShow = data;
		},
		getDailyBettingBonusShow(state: any, data: boolean) {
			state.dailyBettingBonusShow = data;
		},
		getSupplyCrateShow(state: any, data: boolean) {
			state.supplyCrateShow = data;
		},
		getSignInShow(state: any, data: boolean) {
			state.signInShow = data;
		},
		getisApk(state: any, data: boolean) {
			state.isApk = data;
		},

		getisBônusdepósito(state: any, data: boolean) {
			state.isBônusdepósito = data;
		},
		getnoBônusdepósito(state: any, data: boolean) {
			state.noBônusdepósito = data;
		},
		getvipCheckIn(state: any, data: boolean) {
			state.vipCheckIn = data;
		},

	},
	actions: {
		async setLoadingShow({ commit }, data: boolean) {
			commit('getLoadingShow', data);
		},
		async setRollerShow({ commit }, data: boolean) {
			commit('getrollerShow', data);
		},
		// 设置是否pc
		async setIsPc({ commit }, data: boolean) {
			commit('getIsPc', data);
		},
		// 设置侧边栏显示
		async setSidebarIsShow({ commit }, data: boolean) {
			commit('getSidebarIsShow', data);
		},
		async setUserInfoLoad({ commit }, data: boolean) {
			commit('getPlayIngState', data);
		},
		async setPlayIngState({ commit }, data: boolean) {
			commit('getPlayIngState', data);
		},
		async setLoginShow({ commit }, data: boolean) {
			commit('getLoginShow', data);
		},
		async setDepositShow({ commit }, data: boolean) {
			commit('getDepositShow', data);
		},
		async setDailyBettingBonusShow({ commit }, data: boolean) {
			commit('getDailyBettingBonusShow', data);
		},
		async setSupplyCrateShow({ commit }, data: boolean) {
			commit('getSupplyCrateShow', data);
		},
		async setSignInShow({ commit }, data: boolean) {
			commit('getSignInShow', data);
		}, async setisApk({ commit }, data: boolean) {
			commit('getisApk', data);
		},
		async setnoBônusdepósito({ commit }, data: boolean) {
			commit('getnoBônusdepósito', data);
		},
		async setisBônusdepósito({ commit }, data: boolean) {
			commit('getisBônusdepósito', data);
		},
		async setvipCheckIn({ commit }, data: boolean) {
			commit('getvipCheckIn', data);
		},
	},
};

export default statusModule;
