import { request } from "@/utils/service"




//游戏类型------------------------------------------------------start


// 获取游戏类型数据
export function game_type_list_post(data) {
  return request({
    url: "/game_type_list_post",
    method: "post",
    data
  })
}

// 添加游戏类型
export function add_game_type_post(data) {
  return request({
    url: "/add_game_type_post",
    method: "post",
    data
  })
}

// 添加游戏类型
export function update_game_type_post(data) {
  return request({
    url: "/update_game_type_post",
    method: "post",
    data
  })
}

// 添加游戏类型
export function update_game_type_status_post(data) {
  return request({
    url: "/update_game_type_status_post",
    method: "post",
    data
  })
}
// 添加游戏类型
export function delete_game_type_post(data) {
  return request({
    url: "/delete_game_type_post",
    method: "post",
    data
  })
}

//游戏类型------------------------------------------------------end

//游戏平台------------------------------------------------------start

// 游戏平台列表配置
export function game_conf_post(data) {
  return request({
    url: "/game_conf_post",
    method: "post",
    data
  })
}


// 游戏平台列表
export function game_list_post(data) {
  return request({
    url: "/game_list_post",
    method: "post",
    data
  })
}

// 添加游戏平台
export function add_game_post(data) {
  return request({
    url: "/add_game_post",
    method: "post",
    data
  })
}

// 修改游戏平台
export function game_detail_post(data) {
  return request({
    url: "/game_detail_post",
    method: "post",
    data
  })
}
// 禁用游戏平台
export function update_game_status_post(data) {
  return request({
    url: "/update_game_status_post",
    method: "post",
    data
  })
}
// 删除游戏平台
export function delete_game_post(data) {
  return request({
    url: "/delete_game_post",
    method: "post",
    data
  })
}

//游戏平台------------------------------------------------------end



//游戏列表------------------------------------------------------start

// 获取游戏列表查询
export function external_game_conf_post(data) {
  return request({
    url: "/external_game_conf_post",
    method: "post",
    data
  })
}



// 获取游戏列表
export function external_game_list_post(data) {
  return request({
    url: "/external_game_list_post",
    method: "post",
    data
  })
}

// 添加游戏
export function add_external_game_post(data) {
  return request({
    url: "/add_external_game_post",
    method: "post",
    data
  })
}

// 修改游戏
export function external_game_detail_post(data) {
  return request({
    url: "/external_game_detail_post",
    method: "post",
    data
  })
}

// 禁用游戏
export function update_external_game_status_post(data) {
  return request({
    url: "/update_external_game_status_post",
    method: "post",
    data
  })
}

// 删除游戏
export function delete_external_game_post(data) {
  return request({
    url: "/delete_external_game_post",
    method: "post",
    data
  })
}

//游戏列表------------------------------------------------------end

// 获取游戏汇总数据
export function external_game_total_post(data) {
  return request({
    url: "/external_game_total_post",
    method: "post",
    data
  })
}

// 获取用户游戏数据
export function external_game_user_detail_post(data) {
  return request({
    url: "/external_game_user_detail_post",
    method: "post",
    data
  })
}

// 获取游戏记录查询条件信息
export function game_log_conf_post(data) {
  return request({
    url: "/game_log_conf_post",
    method: "post",
    data
  })
}


// 获取用户游戏记录数据
export function user_game_log_list_post(data) {
  return request({
    url: "/user_game_log_list_post",
    method: "post",
    data
  })
}

// 获取游戏平台数据
export function game_day_data_post(data) {
  return request({
    url: "/game_day_data_post",
    method: "post",
    data
  })
}


// 获取集成商汇总数据
export function factory_game_total_post(data) {
  return request({
    url: "/factory_game_total_post",
    method: "post",
    data
  })
}


export function game_bet_log_post(data) {
  return request({
    url: "/game_bet_log_post",
    method: "post",
    data
  })
}




