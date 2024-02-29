import { request } from "@/utils/service"

// 支付通道------------------------------------------------------start
// 查询活动配置列表
export function pay_list_post(data: any) {
  return request<any>({
    url: "/pay_list_post",
    method: "post",
    data
  })
}

// 支付通道列表
export function pay_day_data_post(data: any) {
  return request<any>({
    url: "/pay_day_data_post",
    method: "post",
    data
  })
}

// 添加
export function add_pay_post(data: any) {
  return request<any>({
    url: "/add_pay_post",
    method: "post",
    data
  })
}

// 修改
export function pay_detail_post(data: any) {
  return request<any>({
    url: "/pay_detail_post",
    method: "post",
    data
  })
}


// 启用支付
export function update_pay_statue_post(data: any) {
  return request<any>({
    url: "/update_pay_statue_post",
    method: "post",
    data
  })
}


// 启用提现
export function open_withdraw_channel_post(data: any) {
  return request<any>({
    url: "/open_withdraw_channel_post",
    method: "post",
    data
  })
}

// 删除支付处理
export function delete_pay_channel_post(data: any) {
  return request<any>({
    url: "/delete_pay_channel_post",
    method: "post",
    data
  })
}
// 支付通道------------------------------------------------------end

// 提现分析------------------------------------------------------start

export function withdraw_day_data_post(data: any) {
  return request<any>({
    url: "/withdraw_day_data_post",
    method: "post",
    data
  })
}

// 提现分析------------------------------------------------------end

// 充值列表------------------------------------------------------start

// 充值列表
export function recharge_conf_list_post(data: any) {
  return request<any>({
    url: "/recharge_conf_list_post",
    method: "post",
    data
  })
}

// 充值列表
export function recharge_list_post(data: any) {
  return request<any>({
    url: "/recharge_list_post",
    method: "post",
    data
  })
}

// 充值列表订单详情
export function user_order_detail_post(data: any) {
  return request<any>({
    url: "/user_order_detail_post",
    method: "post",
    data
  })
}

// 充值列表------------------------------------------------------end

//提现列表
export function withdraw_list_post(data: any) {
  return request<any>({
    url: "/withdraw_list_post",
    method: "post",
    data
  })
}


//用户游戏记录汇总
export function user_game_total_data_post(data: any) {
  return request<any>({
    url: "/user_game_total_data_post",
    method: "post",
    data
  })
}

//用户订单详情
export function withdraw_order_detail_post(data: any) {
  return request<any>({
    url: "/withdraw_order_detail_post",
    method: "post",
    data
  })
}

//所有支付
export function withdraw_pay_list(data: any) {
  return request<any>({
    url: "/withdraw_pay_list",
    method: "post",
    data
  })
}

//通过用户提现
export function adopt_user_withdraw_post(data: any) {
  return request<any>({
    url: "/adopt_user_withdraw_post",
    method: "post",
    data
  })
}

//驳回用户提现
export function refuse_user_withdraw_post(data: any) {
  return request<any>({
    url: "/refuse_user_withdraw_post",
    method: "post",
    data
  })
}

// 没收用户提现
export function cancel_user_withdraw_post(data: any) {
  return request<any>({
    url: "/cancel_user_withdraw_post",
    method: "post",
    data
  })
}


