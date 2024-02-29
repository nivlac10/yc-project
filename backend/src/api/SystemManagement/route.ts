
import { request } from "@/utils/service"
//查
export function get_router_list_post(data) {
  return request<any>({
    url: "/router_list_post",
    method: "post",
    data
  })
}
