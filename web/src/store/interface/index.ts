// 路由缓存列表
export interface KeepAliveNamesState {
	keepAliveNames: Array<string>
}

// 配置
export interface confState {
	all_conf: {
		activity: Array<any>
		banner: Array<any>
		commission_desc: Array<any>
		currency: Array<any>
		customer_service: Array<any>
		maintain_conf: Array<any>
		notice_list: Array<any>
		pay_conf: object
		service_terms_url: string
		share_conf: object
		vip_conf: Array<any>
		commission_type: Array<any>
		tg_channel_url: string
		invite_recharge_bonus_list: Array<any>
		android_url: string,
		san_plate_alert_list: Array<any>,
		platform: {
			platform_livechat_id: number | string,
			platform_min_icon_url: string,
			platform_path: string,
			platform_title: string,
			platform_title_icon_url: string,
			platform_url: string
		},
		invit_recharge_gift:string
	}
	game_list: {
		factory_list: Array<any>
		game_data_version: string
		game_list: Array<any>
		game_type: Array<any>
		hot_list: Array<any>
	}
	game_data_version: string
	neverNoPop: boolean
	top10: Array<any>
}

// 用户
export interface userState {
	commission: number //佣金
	first_pay_type: number //是否是首充
	header_img: number  //头像下标
	money: number //余额
	new: number
	nickname: string //用户名
	phone: string //手机号
	remain_code_amount: number //剩余打码量
	sh: string //审核模式
	token: string
	total_bet: number //总打码
	total_money: number //总充值
	total_withdraw: number //总提现
	uid: number
	vip_lv: number
	vip_low_lv: number
	with_money: number //可提现金额
	need_code_amount: number
	share_lv: number
	share_valid_number: number
	vip_day: number
	vip_earnings: number
	sign_bonus: number
	team_one_user_num: number
	total_commission: number
	CPF: string
	username: string
	give_money: number // 总赠送
	download_bonus: number
}

export interface statusState {
	loadingShow: boolean // loading.....
	isPc: boolean // 是否pc端
	sidebarIsShow: boolean // 侧边栏显示
	loginShow: boolean // 显示登录
	showDeposito: boolean //显示系统通知
	depositShow: boolean // 显示提现
	showBonusConversion: boolean, // 显示奖金转余额
	showPayPop: boolean, // 显示充值支付弹窗
	signInShow: boolean, // 显示签到
	dailyBettingBonusShow: boolean // 显示每日投注奖金
	supplyCrateShow: boolean // 显示补给箱
	announcementShow: boolean // 显示公告
	userInfoLoad: boolean,
	playIngState: boolean,
	isApk: boolean,
	ActivitySubpageDataIndex: number,
	allGameShow: boolean, //所有游戏弹窗
	game_id: number,
	rollerShow: boolean,//是否显示滚轮弹窗
	isBônusdepósito:boolean, //是否显示累计存款奖励
	noBônusdepósito:boolean, //是否不再显示累计存款奖励
	vipCheckIn:boolean, //是否显示签到页vip详情弹窗
}

export interface helpState {
	index: Array<number>
}

export interface saveUserDataState {
	accountNumber: object // 账号
	withdrawalSettings: object // 提款设置
}

export interface vipBonusState {
	split_time: string
	now_time: string
	day_time: string
	day_bonus: {
		money: number,
		state: number,
		time: number
	},
	month_bonus: {
		money: number,
		state: number
	},
	now_bonus: {
		money: number,
		state: number,
		time: number
	},
	week_bonus: {
		money: number,
		state: number
	},
	split_bonus: {
		money: number,
		state: number,
		time: number,
		wait_money: number,
		total_money: number,
	},
	lv_up_bonus: {
		state: number
	}
	bonus_num: number,
	badgeShow: boolean,
	sgin_data:object,
}

export interface startDataState {
	bonusCabinet: {
		loss_bonus_state: 0,
		refer_bonus_state: 0,
		roller_bonus_state: 0,
		sign_bonus_state: 0
	}
}

export interface musicState {
	musicShow: boolean // 显示音乐播放器
	audioDom: HTMLElement | string, // 音频dom
	audioUrl: string, // 音频地址
	currentAudioIdx: number, // 当前播放音频的索引
	audioUrlList: Array<any>,
	audioVolume: number, // 音量
	audioDuration: number, // 音频当前播放时间 百分比
	audioStart: string, // 音频当前播放时间 时间格式
	duration: string, // 音频总时间
	audioStatus: string, // 音频状态
	audioPlayStatus: number, // 音频播放状态
	audioPlayStatusList: Array<object>
}

// 主接口(顶级类型声明)
export interface RootStateTypes {
	keepAlive: KeepAliveNamesState
	conf: confState
	user: userState
	status: statusState
	help: helpState
	saveUserData: saveUserDataState
	vipBonusState: vipBonusState
	startData: startDataState
	music: musicState
}