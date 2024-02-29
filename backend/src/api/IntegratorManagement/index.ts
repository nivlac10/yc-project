import { request } from "@/utils/service"

// 获取集成商列表
export function factory_list_post(data) {
  return request({
    url: "/factory_list_post",
    method: "post",
    data
  })
}

// 添加集成商
export function add_factory_post(data) {
  return request({
    url: "/add_factory_post",
    method: "post",
    data
  })
}

// 编辑集成商
export function update_factory_post(data) {
  return request({
    url: "/update_factory_post",
    method: "post",
    data
  })
}

// 删除集成商
export function delete_factory_post(data) {
  return request({
    url: "/delete_factory_post",
    method: "post",
    data
  })
}

// 禁用集成商
export function update_factory_status(data) {
  return request({
    url: "/update_factory_status",
    method: "post",
    data
  })
}



// 获取集成商详情列表
export function game_list_post(data) {
  return request({
    url: "/game_list_post",
    method: "post",
    data
  })
}

