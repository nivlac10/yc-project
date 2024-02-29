import { request } from "@/utils/service"


//查
export function get_interface_list_post(data) {
  return request<any>({
    url: "/interface_list_post",
    method: "post",
    data
  })
}

// 管理员列表
export function admin_list_post(data) {
  return request<any>({
    url: "/admin_list_post",
    method: "post",
    data
  })
}

// 新增管理员
export function add_admin_post(data) {
  return request<any>({
    url: "/add_admin_post",
    method: "post",
    data
  })
}

// 更新管理员状态
export function update_admin_post(data) {
  return request<any>({
    url: "/update_admin_post",
    method: "post",
    data
  })
}

// 删除管理员
export function delete_admin_one(data) {
  return request<any>({
    url: "/delete_admin_one",
    method: "post",
    data
  })
}

// 修改管理员权限
export function update_admin_statue_post(data) {
  return request<any>({
    url: "/update_admin_statue_post",
    method: "post",
    data
  })
}


// 重置密钥
export function reset_admin_secret(data) {
  return request<any>({
    url: "/reset_admin_secret",
    method: "post",
    data
  })
}