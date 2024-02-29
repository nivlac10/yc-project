/*
 * @Author: wawodel 69891926+wawodel@users.noreply.github.com
 * @Date: 2023-06-08 16:39:47
 * @LastEditors: wawodel 69891926+wawodel@users.noreply.github.com
 * @LastEditTime: 2023-12-26 15:48:06
 * @FilePath: \web1.1\src\api\user.ts
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import { get, post } from "@/utils/http";

export class UserService {
	static get_user_info = (params?: object) => post('/get_user_info', params);
	static get_user_token = (params?: object) => post('/get_user_token', params);
	static user_transfer_commission = (params?: object) => post('/user_transfer_commission', params);
	static send_phone_code = (params?: object) => post('/send_phone_code', params);
	static bind_user_phone = (params?: object) => post('/bind_user_phone', params);
	static change_user_pwd = (params?: object) => post('/change_user_pwd', params);
	static change_user_info = (params?: object) => post('/change_user_info', params);
	static send_email_code = (params?: object) => post('/send_email_code', params); // 发送email验证码
	static bind_user_email = (params?: object) => post('/bind_user_email', params); // 绑定email

	static get_sign_list = (params?: object) => post('/get_sign_list', params); // 签到列表
	static receive_sign_bonus = (params?: object) => post('/receive_sign_bonus', params); // 领取签到奖励

	static get_bet_day_task_list = (params?: object) => post('/get_bet_day_task_list', params); // 打码任务状态
	static receive_bet_day_task_bonus = (params?: object) => post('/receive_bet_day_task_bonus', params); // 领取打码任务

	static get_loss_money_bouns_list = (params?: object) => post('/get_loss_money_bouns_list', params); // 获取补给箱列表状态
	static receive_loss_bonus = (params?: object) => post('/receive_loss_bonus', params); // /用户领取补给箱奖励
	static get_loss_receive_record = (params?: object) => post('/get_loss_receive_record', params); // 领取记录
	static user_code_empty = (params?: object) => post('/user_code_empty', params); // 打码量清零
	static bind_user_withdrawal_info = (params?: object) => post('/bind_user_withdrawal_info', params); // 保存用户提现信息

	static get_bonus_cabinet_state = (params?: object) => post('/get_bonus_cabinet_state', params); // 奖金柜状态
	static user_get_yesterday_recharge_bonus = (params?: object) => post('/user_get_yesterday_recharge_bonus', params); // 用户领取昨日充值奖励
	static de_zhou_get_bet_bonus_get = (params?: object) => post('/de_zhou_get_bet_bonus_get', params); // 用户领取德州每日下注奖励
	static apk_download_bonus = (params?: object) => post('/apk_download_bonus', params); // 下载apk奖励
}