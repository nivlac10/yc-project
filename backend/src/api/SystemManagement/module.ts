import { request } from "@/utils/service"


//增
export function add_power_class_post(data) {
  return request<any>({
    url: "/add_power_class_post",
    method: "post",
    data
  })
}

//删
export function delete_power_class(data) {
  return request<any>({
    url: "/delete_power_class",
    method: "post",
    data
  })
}

//改
export function power_class_detail_post(data) {
  return request<any>({
    url: "/power_class_detail_post",
    method: "post",
    data
  })
}

//查
export function get_power_class_post(data) {
  return request<any>({
    url: "/power_class_post",
    method: "post",
    data
  })
}
