import { get, post } from "@/utils/http";

export class RollerService {
	static receive_roller_money = (params?: object) => post('/receive_roller_money', params);
    static roller_money_state = (params?: object) => post('/roller_money_state', params);
}
