import { request } from "@/utils/service"

// 代理列表------------------------------------------
// 代理列表
export function proxy_list_post(data: any) {
  return request({
    url: "/proxy_list_post",
    method: "post",
    data
  })
}
// 添加代理
export function add_proxy_post(data: any) {
  return request({
    url: "/add_proxy_post",
    method: "post",
    data
  })
}
// 修改代理状态
export function update_proxy_list_post(data: any) {
  return request({
    url: "/update_proxy_list_post",
    method: "post",
    data
  })
}
// 修改代理
export function proxy_detail_post(data: any) {
  return request({
    url: "/proxy_detail_post",
    method: "post",
    data
  })
}
// 删除代理
export function delete_proxy_post(data: any) {
  return request({
    url: "/delete_proxy_post",
    method: "post",
    data
  })
}

// 渠道列表------------------------------------------
// 获取渠道列表
export function agent_list_post(data: any) {
  return request({
    url: "/agent_list_post",
    method: "post",
    data
  })
}
// 新增渠道处理
export function add_agent_post(data: any) {
  return request({
    url: "/add_agent_post",
    method: "post",
    data
  })
}
// 更新渠道信息
export function update_agent_post(data: any) {
  return request({
    url: "/update_agent_post",
    method: "post",
    data
  })
}
// 更新状态
export function update_agent_statue_post(data: any) {
  return request({
    url: "/update_agent_statue_post",
    method: "post",
    data
  })
}
// 删除渠道
export function delete_agent_post(data: any) {
  return request({
    url: "/delete_agent_post",
    method: "post",
    data
  })
}

// 测试回传
export function test_backhaul_post(data: any) {
  return request({
    url: "/test_backhaul_post",
    method: "post",
    data
  })
}
