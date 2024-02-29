import { request } from "@/utils/service"



//查询打码日志列表
export function bet_code_log_list_post(data: any) {
    return request<any>({
        url: "/bet_code_log_list_post",
        method: "post",
        data
    })
}


//获取用户反水记录日志
export function bet_task_log_list_post(data: any) {
    return request<any>({
        url: "/bet_task_log_list_post",
        method: "post",
        data
    })
}


// 日签到---------------------------------------------------------start

//日签到列表
export function user_sign_list_post(data: any) {
    return request<any>({
        url: "/user_sign_list_post",
        method: "post",
        data
    })
}

// 日签到---------------------------------------------------------end


// 破产补助---------------------------------------------------------start

//破产补助列表
export function user_loss_bonus_log_post(data: any) {
    return request<any>({
        url: "/user_loss_bonus_log_post",
        method: "post",
        data
    })
}
// 破产补助---------------------------------------------------------end



// 充值奖励奖励

//查询打码日志列表
export function recharge_bonus_log_post(data: any) {
    return request<any>({
        url: "/recharge_bonus_log_post",
        method: "post",
        data
    })
}



//转轮赠送金额日志列表
export function roller_money_log_post(data: any) {
    return request<any>({
        url: "/roller_money_log_post",
        method: "post",
        data
    })
}


//转轮赠送金额日志列表
export function dezhou_bonus_log_post(data: any) {
    return request<any>({
        url: "/dezhou_bonus_log_post",
        method: "post",
        data
    })
}


//充值成就领取日志列表
export function recharge_achieve_log_post(data: any) {
    return request<any>({
        url: "/recharge_achieve_log_post",
        method: "post",
        data
    })
}


//佣金邀请任务日志列表
export function invite_task_log_post(data: any) {
    return request<any>({
        url: "/invite_task_log_post",
        method: "post",
        data
    })
}

//每日活跃记录
export function user_keep_log_post(data: any) {
    return request<any>({
        url: "/user_keep_log_post",
        method: "post",
        data
    })
}


//每日活跃记录
export function give_code_log_list_post(data: any) {
    return request<any>({
        url: "/give_code_log_list_post",
        method: "post",
        data
    })
}
