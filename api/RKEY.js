class RKEY {
	constructor() {

	}
	// redis常量

	// 域名key redis.hset 第二个key
	static CDN_HOST = 'resource_host'
	// 所有游戏配置  表 san_conf  redis.hset存储
	static SAN_GAME_ALL_CONF = "san_game_all_conf"
	// 游戏类型列表
	static SAN_GAME_TYPE_CONF = "san_game_type_conf"
	// 所有支付配置  表  san_pay_list  redis.set
	static SAN_GAME_NEW_PAY_CONF = "san_game_new_payment_conf"
	// 提现配置  表 san_pay_list redis.hset
	static SAN_GAME_NEW_WITHDRAW_CONF = 'san_game_new_transfer_conf'
	// 支付类型配置
	static SAN_GAME_PAY_TYPE_CONF = 'san_game_pay_type_conf'
	// 支付套餐配置  san_card_list  redis.set
	static SAN_GAME_NEW_RECHARGE_CARD_CONF = 'san_game_new_recharge_card_conf'
	// 支付套餐配置 根据card_id配置  redis.hset
	static SAN_GAME_NEW_RECHARGE_TOTAL_CONF = 'san_game_new_recharge_total_conf'
	// 渠道配置 san_agent  表san_agent redis.hset  cid
	static SAN_GAME_NEW_CHANNEL_CONF = 'san_game_new_channel_conf'
	// 活动配置 表san_activity_list 表san_activity_list redis.set存储
	static SAN_GAME_NEW_ACTIVITY_CONF = 'san_game_new_activity_conf'
	// 公告配置  san_notice_list redis.set
	static SAN_GAME_NEW_NOTICE_CONF = 'san_game_new_notice_conf'
	// 客服配置 san_service_list redis.set
	static SAN_GAME_SERVICE_LIST = "san_service_list"
	// 佣金配置 san_commission_desc_list  redis.set
	static SAN_COMMISSION_DESC_LIST = 'san_commission_desc_list'
	// 邀请任务配置
	static SAN_USER_INVITE_TASK = "san_user_invite_task"
	// 轮播图配置 表san_banner_list   redis.set
	static SAN_GAME_BANNER_LIST = "san_banner_list"
	// 游戏列表配置 san_external_game_list redis.set
	static SAN_EXTERNAL_GAME_LIST = 'san_external_game_list'
	// 热门游戏配置
	static SAN_GAME_HOT_GAME_LIST = "san_game_hot_game_list"
	// 厂家列表配置 san_game_list  redis.set
	static SAN_GAME_FACTORY_LIST = 'san_game_list'
	// 游戏版本配置
	static GAME_DATA_VERSION = 'game_data_version'
	// vip等级KEY
	static SAN_GAME_VIP_LV_LIST = "san_game_vip_lv_list"
	// 支付活动配置
	static SAN_GAME_PAY_ACTION_CONF = "san_game_pay_action_conf"
	// 支付活动list
	static SAN_GAME_PAY_ACTION_LIST_CONF = "san_action_pay_list_conf"
	// 支付活动阶梯
	static SAN_GAME_PAY_ACTION_LADDER_LIST_CONF = "san_action_pay_ladder_list_conf"
}

module.exports = RKEY;