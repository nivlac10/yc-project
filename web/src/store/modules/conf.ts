/*
 * @Author: wawodel 69891926+wawodel@users.noreply.github.com
 * @Date: 2023-06-08 16:39:47
 * @LastEditors: wawodel 69891926+wawodel@users.noreply.github.com
 * @LastEditTime: 2024-01-04 15:19:46
 * @FilePath: \web1.1\src\store\modules\conf.ts
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import { Module } from 'vuex';
import { confState, RootStateTypes } from '@/store/interface/index';

const confModule: Module<confState, RootStateTypes> = {
	namespaced: true,
	state: {
		all_conf: {
			activity: [],
			banner: [],
			commission_desc: [],
			currency: [],
			customer_service: [],
			maintain_conf: [],
			notice_list: [],
			pay_conf: {},
			service_terms_url: "",
			share_conf: {},
			vip_conf: [],
			commission_type: [],
			tg_channel_url: "",
			invite_recharge_bonus_list: [],
			android_url: '',
			san_plate_alert_list: [],
			platform: {
				platform_livechat_id: "",
				platform_min_icon_url: "",
				platform_path: "",
				platform_title: "",
				platform_title_icon_url: "",
				platform_url: ""
			},
			invit_recharge_gift:'0',
		},
		game_list: {
			factory_list: [],
			game_data_version: "",
			game_list: [],
			game_type: [],
			hot_list: []
		},
		game_data_version: "",
		neverNoPop: false,
		top10: [],
	},
	mutations: {
	},
	actions: {
	},
};

export default confModule;
