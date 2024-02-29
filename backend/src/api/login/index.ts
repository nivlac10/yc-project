import { request } from "@/utils/service"
import type * as Login from "./types/login"

/** 获取登录验证码 */
export function getLoginCodeApi() {
  return request<any>({
    url: "login/code",
    method: "get"
  })
}

/** 登录并返回 Token */
export function loginApi(data: any) {
  return request<any>({
    url: "/login",
    method: "post",
    data
  })
}

/** 获取用户详情 */
export function getUserInfoApi() {
  return request<any>({
    url: "/get_info",
    method: "post"
  })
}

/** 获取平台信息 */
export function get_p_conf() {
  return request<any>({
    url: "/get_p_conf",
    method: "post"
  })
}
