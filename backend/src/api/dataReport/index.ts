import { request } from "@/utils/service"

// 付费分析数据
export function user_payment_detail_post(data: any) {
	return request<any>({
		url: "/user_payment_detail_post",
		method: "post",
		data
	})
}
// 付费留存数据
export function user_keep_pay_post(data: any) {
	return request<any>({
		url: "/user_keep_pay_post",
		method: "post",
		data
	})
}

// 用户活跃数据
export function user_keep_post(data: any) {
	return request<any>({
		url: "/user_keep_post",
		method: "post",
		data
	})
}

// 获取事件统计数据
export function event_report_total_post(data: any) {
	return request<any>({
		url: "/event_report_total_post",
		method: "post",
		data
	})
}

// 玩家活跃数据
export function user_active_post(data: any) {
	return request<any>({
		url: "/user_active_post",
		method: "post",
		data
	})
}

// 获取用户每日报表数据
export function user_day_report_post(data: any) {
	return request<any>({
		url: "/user_day_report_post",
		method: "post",
		data
	})
}

// 用户日报表
export function user_day_report_list_post(data: any) {
	return request<any>({
		url: "/user_day_report_list_post",
		method: "post",
		data
	})
}

//获取每日数据---------------------------------------------------------start

export function day_data_list_post(data: any) {
	return request<any>({
		url: "/day_data_list_post",
		method: "post",
		data
	})
}
// 获取每日数据---------------------------------------------------------end
