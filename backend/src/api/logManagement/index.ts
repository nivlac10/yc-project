import { request } from "@/utils/service"

// 后台用户登陆数据列表
export function login_log_post(data: any) {
  return request<any>({
    url: "/login_log_post",
    method: "post",
    data
  })
}

// 黑名单用户列表
export function black_list_post(data: any) {
  return request<any>({
    url: "/black_list_post",
    method: "post",
    data
  })
}

// 添加黑名单处理
export function add_black_post(data: any) {
  return request<any>({
    url: "/add_black_post",
    method: "post",
    data
  })
}

// 异常列表
export function unusual_user_log_post(data: any) {
  return request<any>({
    url: "/unusual_user_log_post",
    method: "post",
    data
  })
}

// 黑名单ip列表
export function black_ip_list_post(data: any) {
  return request<any>({
    url: "/black_ip_list_post",
    method: "post",
    data
  })
}

// 黑名单ip列表
export function black_account_list_post(data: any) {
  return request<any>({
    url: "/black_account_list_post",
    method: "post",
    data
  })
}

// 删除黑名单
export function delete_unusual_user_post(data: any) {
  return request<any>({
    url: "/delete_unusual_user_post",
    method: "post",
    data
  })
}

// 获取事件上报记录
export function event_report_list_post(data: any) {
  return request<any>({
    url: "/event_report_list_post",
    method: "post",
    data
  })
}