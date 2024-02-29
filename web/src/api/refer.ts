/*
 * @Author: haosan 123@qq.com
 * @Date: 2023-08-22 11:18:20
 * @LastEditors: haosan 123@qq.com
 * @LastEditTime: 2023-08-23 11:54:00
 * @FilePath: \web1.1\src\api\refer.ts
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import { get, post } from "@/utils/http";

export class ReferService {
	static get_commission_list = (params?: object) => post('/get_commission_list', params);
	static get_member_list = (params?: object) => post('/get_member_list', params);
	static get_user_team_data = (params?: object) => post('/get_user_team_data', params);
	static get_user_invite_state = (params?: object) => post('/get_user_invite_state', params);
	static user_receive_invite_task = (params?: object) => post('/user_receive_invite_task', params);
	static get_commission_total_data = (params?: object) => post('/get_commission_total_data', params);
	static get_invite_task_top10 = (params?: object) => post('/get_invite_task_top10', params);
	static get_user_lower_data = (params?: object) => post('/get_user_lower_data', params);
	static get_user_team_list = (params?: object) => post('/get_user_team_list', params);
	static get_invite_total_data = (params?: object) => post('/get_invite_total_data', params);
}
