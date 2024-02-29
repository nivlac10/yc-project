import { get, post } from "@/utils/http";

export class deposito {
	static get_msg_list = (params?: object) => post('/get_msg_list', params);
    static delete_msg_listlist = (params?: object) => post('/delete_msg_list', params);
    static receive_msg_money = (params?: object) => post('/receive_msg_money', params);
    static get_order_state = (params?: object) => post('/get_order_state', params);
    
}
    