import { get, post } from "@/utils/http";

export class ConfService {
	static get_conf = (params?: object) => post('/get_conf', params);
	static get_game_list = (params?: object) => post('/get_game_list', params);
	static get_top_10 = (params?: object) => post('/get_top_10', params);
}
