import { request } from "@/utils/service"

/** 获取登录验证码 */
export function admin_home(data: any) {
  return request<any>({
    url: "/admin_home",
    method: "post",
    data
  })
}

// 搜索时间按钮
export function search_btn(data: any) {
  return request<any>({
    url: "/search_btn",
    method: "post",
    data
  })
}

// 首页数据
export function home_data_post(data: any) {
  return request<any>({
    url: "/home_data_post",
    method: "post",
    data
  })
}


// 德州扑克
export function game_id_data_post(data: any) {
  return request<any>({
    url: "/game_id_data_post",
    method: "post",
    data
  })
}