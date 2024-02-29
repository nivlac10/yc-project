import { request } from "@/utils/service"
// 系统配置------------------------------------------------------start

// 查询系统配置初始内容
export function system_conf(data: any) {
  return request<any>({
    url: "/system_conf",
    method: "post",
    data
  })
}

// 查询系统配置
export function system_conf_list_post(data: any) {
  return request<any>({
    url: "/system_conf_list_post",
    method: "post",
    data
  })
}

// 修改系统配置
export function system_conf_post(data: any) {
  return request<any>({
    url: "/system_conf_post",
    method: "post",
    data
  })
}

// 更新redis
export function update_redis_conf_post(data: any) {
  return request<any>({
    url: "/update_redis_conf_post",
    method: "post",
    data
  })
}

// 系统配置------------------------------------------------------end

// 活动配置------------------------------------------------------start
// 查询活动配置列表
export function activity_list_post(data: any) {
  return request<any>({
    url: "/activity_list_post",
    method: "post",
    data
  })
}

// 新增活动配置
export function activity_add_post(data: any) {
  return request<any>({
    url: "/activity_add_post",
    method: "post",
    data
  })
}

// 修改活动配置信息
export function activity_update_post(data: any) {
  return request<any>({
    url: "/activity_update_post",
    method: "post",
    data
  })
}

// 删除活动配置
export function activity_delete_post(data: any) {
  return request<any>({
    url: "/activity_delete_post",
    method: "post",
    data
  })
}

// 修改活动配置状态
export function activity_Disable_post(data: any) {
  return request<any>({
    url: "/activity_Disable_post",
    method: "post",
    data
  })
}
// 活动配置------------------------------------------------------end


// 公告---------------------------------------------------------start
// 公告列表
export function notice_list_post(data: any) {
  return request<any>({
    url: "/notice_list_post",
    method: "post",
    data
  })
}
// 添加公告
export function add_notice_post(data: any) {
  return request<any>({
    url: "/add_notice_post",
    method: "post",
    data
  })
}
// 禁用公告
export function update_notice_status_post(data: any) {
  return request<any>({
    url: "/update_notice_status_post",
    method: "post",
    data
  })
}
// 修改公告
export function update_notice_post(data: any) {
  return request<any>({
    url: "/update_notice_post",
    method: "post",
    data
  })
}
// 删除公告
export function delete_notice_post(data: any) {
  return request<any>({
    url: "/delete_notice_post",
    method: "post",
    data
  })
}
// 公告---------------------------------------------------------end

// 充值活动---------------------------------------------------------start
// 充值活动简介列表
export function recharge_activity_slogan_post(data: any) {
  return request<any>({
    url: "/recharge_activity_slogan_post",
    method: "post",
    data
  })
}
// 添加充值活动简介
export function add_slogan_post(data: any) {
  return request<any>({
    url: "/add_slogan_post",
    method: "post",
    data
  })
}
// 修改充值活动简介
export function update_slogan_post(data: any) {
  return request<any>({
    url: "/update_slogan_post",
    method: "post",
    data
  })
}
// 禁用充值活动简介
export function update_slogan_status_post(data: any) {
  return request<any>({
    url: "/update_slogan_status_post",
    method: "post",
    data
  })
}
// 删除充值活动简介
export function delete_slogan_post(data: any) {
  return request<any>({
    url: "/delete_slogan_post",
    method: "post",
    data
  })
}
// 充值活动列表
export function recharge_activity_list_post(data: any) {
  return request<any>({
    url: "/recharge_activity_list_post",
    method: "post",
    data
  })
}
// 添加充值活动
export function add_recharge_activity_post(data: any) {
  return request<any>({
    url: "/add_recharge_activity_post",
    method: "post",
    data
  })
}
// 修改充值活动
export function update_recharge_activity_post(data: any) {
  return request<any>({
    url: "/update_recharge_activity_post",
    method: "post",
    data
  })
}
// 删除充值活动
export function delete_recharge_activity_post(data: any) {
  return request<any>({
    url: "/delete_recharge_activity_post",
    method: "post",
    data
  })
}
// 列表邀请任务记录列表
export function recharge_activity_log_list_post(data: any) {
  return request<any>({
    url: "/recharge_activity_log_list_post",
    method: "post",
    data
  })
}
// 获取充值活动类型
export function recharge_activity_type_list_post(data: any) {
  return request<any>({
    url: "/recharge_activity_type_list_post",
    method: "post",
    data
  })
}
// 充值活动---------------------------------------------------------end


// 轮播图配置---------------------------------------------------------start

// 获取轮播图列表
export function banner_list_post(data: any) {
  return request<any>({
    url: "/banner_list_post",
    method: "post",
    data
  })
}

// 禁用轮播图
export function update_banner_status_post(data: any) {
  return request<any>({
    url: "/update_banner_status_post",
    method: "post",
    data
  })
}

// 添加轮播图
export function add_banner_post(data: any) {
  return request<any>({
    url: "/add_banner_post",
    method: "post",
    data
  })
}

// 修改轮播图
export function detail_banner_post(data: any) {
  return request<any>({
    url: "/detail_banner_post",
    method: "post",
    data
  })
}

// 删除轮播图
export function delete_banner_post(data: any) {
  return request<any>({
    url: "/delete_banner_post",
    method: "post",
    data
  })
}

// 轮播图配置---------------------------------------------------------end

// 兑换码配置---------------------------------------------------------start

// 获取兑换码列表
export function give_code_post(data: any) {
  return request<any>({
    url: "/give_code_post",
    method: "post",
    data
  })
}

// 修改兑换码
export function detail_give_code_post(data: any) {
  return request<any>({
    url: "/detail_give_code_post",
    method: "post",
    data
  })
}

// 新增兑换码
export function add_gift_post(data: any) {
  return request<any>({
    url: "/add_gift_post",
    method: "post",
    data
  })
}


// 修改兑换码状态
export function update_give_code_status_post(data: any) {
  return request<any>({
    url: "/update_give_code_status_post",
    method: "post",
    data
  })
}

// 删除兑换码
export function delete_give_code_post(data: any) {
  return request<any>({
    url: "/delete_give_code_post",
    method: "post",
    data
  })
}
// 兑换码配置---------------------------------------------------------end

// 用户反水---------------------------------------------------------start

// 获取用户反水记录
export function bet_task_list_post(data: any) {
  return request<any>({
    url: "/bet_task_list_post",
    method: "post",
    data
  })
}

// 修改打码反水奖励
export function update_bet_task_post(data: any) {
  return request<any>({
    url: "/update_bet_task_post",
    method: "post",
    data
  })
}

// 添加打码反水奖励
export function add_bet_task_post(data: any) {
  return request<any>({
    url: "/add_bet_task_post",
    method: "post",
    data
  })
}

//修改打码反水奖励状态
export function update_bet_task_status_post(data: any) {
  return request<any>({
    url: "/update_bet_task_status_post",
    method: "post",
    data
  })
}
// 用户反水---------------------------------------------------------end

// 佣金配置---------------------------------------------------------start
// 查询返佣配置
export function task_conf_list_post(data: any) {
  return request<any>({
    url: "/task_conf_list_post",
    method: "post",
    data
  })
}


// 修改返佣配置
export function update_data_conf(data: any) {
  return request<any>({
    url: "/update_data_conf",
    method: "post",
    data
  })
}


// 获取邀请任务列表
export function invite_task_list_post(data: any) {
  return request<any>({
    url: "/invite_task_list_post",
    method: "post",
    data
  })
}
// 添加邀请任务
export function add_invite_task_post(data: any) {
  return request<any>({
    url: "/add_invite_task_post",
    method: "post",
    data
  })
}
// 修改邀请任务
export function update_invite_task_post(data: any) {
  return request<any>({
    url: "/update_invite_task_post",
    method: "post",
    data
  })
}
// 删除邀请任务
export function delete_invite_task_post(data: any) {
  return request<any>({
    url: "/delete_invite_task_post",
    method: "post",
    data
  })
}
// 佣金配置---------------------------------------------------------end

// 平台功能弹窗-----------------------------------------------------start

// 查询平台功能弹窗
export function plate_alert_list_post(data: any) {
  return request<any>({
    url: "/plate_alert_list_post",
    method: "post",
    data
  })
}


// 添加平台功能弹窗
export function add_plate_alert_post(data: any) {
  return request<any>({
    url: "/add_plate_alert_post",
    method: "post",
    data
  })
}


// 修改平台功能弹窗
export function detail_plate_alert_post(data: any) {
  return request<any>({
    url: "/detail_plate_alert_post",
    method: "post",
    data
  })
}


// 禁用平台功能弹窗
export function update_plate_alert_status_post(data: any) {
  return request<any>({
    url: "/update_plate_alert_status_post",
    method: "post",
    data
  })
}


// 删除平台功能弹窗
export function delete_plate_alert_post(data: any) {
  return request<any>({
    url: "/delete_plate_alert_post",
    method: "post",
    data
  })
}


// 平台功能弹窗-----------------------------------------------------end


