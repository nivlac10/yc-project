import { request } from "@/utils/service"

// 会员列表------------------------------------------------------start
// 查询会员列表
export function user_list_post(data: any) {
  return request<any>({
    url: "/user_list_post",
    method: "post",
    data
  })
}
// 删除
export function delete_user_post(data: any) {
  return request<any>({
    url: "/delete_user_post",
    method: "post",
    data
  })
}

// 修改用户状态
export function update_user_status_post(data: any) {
  return request<any>({
    url: "/update_user_status_post",
    method: "post",
    data
  })
}
// 获取用户详情
export function recharge_user_detail_post(data: any) {
  return request<any>({
    url: "/recharge_user_detail_post",
    method: "post",
    data
  })
}

// 用户充值
export function user_recharge_post(data: any) {
  return request<any>({
    url: "/user_recharge_post",
    method: "post",
    data
  })
}

//获取vip等级列表
export function vip_lv_list(data: any) {
  return request<any>({
    url: "/vip_lv_list",
    method: "post",
    data
  })
}

//支付分析
export function pay_day_data_post(data: any) {
  return request<any>({
    url: "/pay_day_data_post",
    method: "post",
    data
  })
}


// 会员列表------------------------------------------------------end


//余额日志------------------------------------------------------start


// 查询余额日志金额类型列表
export function money_type_list_post(data: any) {
  return request<any>({
    url: "/money_type_list_post",
    method: "post",
    data
  })
}



// 查询余额日志列表
export function money_log_list_post(data: any) {
  return request<any>({
    url: "/money_log_list_post",
    method: "post",
    data
  })
}
export function play_promotion_list(data: any) {
  return request<any>({
    url: "/play_promotion_list",
    method: "post",
    data
  })
}


//余额日志------------------------------------------------------end



//邮件管理------------------------------------------------------start

// 查询用户消息列表
export function email_list_post(data: any) {
  return request<any>({
    url: "/email_list_post",
    method: "post",
    data
  })
}


//邮件管理------------------------------------------------------end

// 核实SBO用户注单记录
export function withdraw_type_post(data: any) {
  return request<any>({
    url: "/withdraw_type_post",
    method: "post",
    data
  })
}

// 核实SBO用户注单记录
export function user_sbo_bet_log_heshi(data: any) {
  return request<any>({
    url: "/user_sbo_bet_log_heshi",
    method: "post",
    data
  })
}
