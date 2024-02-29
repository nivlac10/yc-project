import { get, post } from "@/utils/http";

export class VipService {
	static user_get_now_vip_bonus = (params?: object) => post('/user_get_now_vip_bonus', params); // 获取vip领取状态
	static get_user_vip_bonus_state = (params?: object) => post('/get_user_vip_bonus_state', params); // 获取vip领取状态
	static get_user_split_bonus_list = (params?: object) => post('/get_user_split_bonus_list', params); // 查询用户拆分奖金列表
	static user_get_split_bonus = (params?: object) => post('/user_get_split_bonus', params); // 用户领取拆分奖金
	static user_get_day_vip_bonus = (params?: object) => post('/user_get_day_vip_bonus', params); // 用户领取vip每日反水奖励
	static user_get_week_vip_bonus = (params?: object) => post('/user_get_week_vip_bonus', params); // 用户领取vip每周反水奖励
	static user_get_month_vip_bonus = (params?: object) => post('/user_get_month_vip_bonus', params); // 用户领取vip每周反水奖励
	static get_user_vip_up_bonus_state = (params?: object) => post('/get_user_vip_up_bonus_state', params); // 用户获取可领取vip升级奖励列表
	static user_get_vip_up_bonus = (params?: object) => post('/user_get_vip_up_bonus', params); // 用户领取vip升级奖励
	static get_user_vip_reward_state = (params?: object) => post('/get_user_vip_reward_state', params); // 获取vip领取状态
	
}