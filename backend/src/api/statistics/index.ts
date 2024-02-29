import { request } from "@/utils/service"

// 充值时段分析
export function hour_report(data: any) {
  return request<any>({
    url: "/hour_report",
    method: "post",
    data
  })
}