import { get, post } from "@/utils/http";

export class bettingBouns {
	static get_data = (params?: object) => post('/user_rebate_list', params);
	
}
