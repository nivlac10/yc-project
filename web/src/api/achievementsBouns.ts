import { get, post } from "@/utils/http";

export class achievementsBouns {
	static get_recharge_achieve_state = (params?: object) => post('/get_recharge_achieve_state', params);
    static receive_recharge_achieve_bonus = (params?: object) => post('/receive_recharge_achieve_bonus', params);
	
}
