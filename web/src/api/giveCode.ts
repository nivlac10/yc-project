import { get, post } from "@/utils/http";

export class giveCode {
	static user_receive_code = (params?: object) => post('/user_receive_code', params);
	static get_give_code_list = (params?: object) => post('/get_give_code_list', params);
}
