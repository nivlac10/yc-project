import { request } from "@/utils/service"

// vip管理------------------------------------------------------start

// 查询会员等级列表
export function vip_lv_list(data: any) {
    return request<any>({
        url: "/vip_lv_list",
        method: "post",
        data
    })
}
// 修改会员等级
export function edit_vip_lv(data: any) {
    return request<any>({
        url: "/edit_vip_lv",
        method: "post",
        data
    })
}

// 查询会员等级奖励等级列表
export function vip_lv_low_list(data: any) {
    return request<any>({
        url: "/vip_lv_low_list",
        method: "post",
        data
    })
}

// 查询会员等级奖励等级列表
export function edit_vip_lv_low(data: any) {
    return request<any>({
        url: "/edit_vip_lv_low",
        method: "post",
        data
    })
}

// vip管理------------------------------------------------------start



// Vip奖励记录------------------------------------------------------start


// VIP等级打码奖励领取记录列表
export function vip_bonus_log_list(data: any) {
    return request<any>({
        url: "/vip_bonus_log_list",
        method: "post",
        data
    })
}


// VIP等级打码奖励领取记录列表
export function vip_splic_bonus_log_list(data: any) {
    return request<any>({
        url: "/vip_splic_bonus_log_list",
        method: "post",
        data
    })
}

  // Vip奖励记录------------------------------------------------------end
