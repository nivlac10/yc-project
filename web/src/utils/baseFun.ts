// import { showToast } from 'vant';
import { UserService } from "@/api/user";
import { store } from "@/store/index"
import useClipboard from "vue-clipboard3";
import { ElMessage } from 'element-plus'
import router from '../router'
import i18n from '@/lang/index.js'
import { ElLoading } from 'element-plus'
const { toClipboard } = useClipboard();
import { ElNotification } from 'element-plus';
import { computed } from "vue";
// 消息提示
// export function ElMessagePopup(str: string, type: string = 'info') {
//     console.log(getImageUrl('public/home_button_icon.png'));
//     let msg = computed(() => str)
//     let img = type == 'info' ? getImageUrl('public/home_button_icon.png') : type == 'error' ? '' : '';
//     ElMessage({
//         //@ts-ignore
//         dangerouslyUseHTMLString: true,
//         // icon: `${type == 'info' ? '123' : type == 'error' ? '' : ''}`,
//         message: `<img src='${img}' /> <div><p class="ElMessagePopup_title">${type == 'info' ? 'SUCCESS' : type == 'error' ? 'ERROR' : 'WARRING'}</p> <p>${msg.value}</p></div>`,
//         customClass: "ElMessagePopup ElMessageGreen",
//         type: type,
//         duration: 1000,
//     })

// }
export function SuccessNotiFun(text) {
	ElNotification({
		// title: computed(() => i18n.global.t("Success")).value,
		message: computed(() => i18n.global.t(text)).value,
		type: 'success',
		duration: 3000
	})
}
export function WarningNotiFun(text) {
	ElNotification({
		// title: computed(() => i18n.global.t("Warning")).value,
		message: computed(() => i18n.global.t(text)).value,
		type: 'warning',
		duration: 3000
	})
}
export function ErrorNotiFun(text) {

}

// 引入本地图片
export function getImageUrl(name: string) {
	return new URL(`/src/assets/images/${name}`, import.meta.url).href;
}

// 切割成多个数组 arr：切割的数组 counts：每个数组的个数
export function sliceArr(arr, counts) {
	const cloneArr: Array<any> = [...arr];
	const result = [];
	while (cloneArr.length) {
		result.push(cloneArr.splice(0, counts) as never);
	}
	return result;
}

/**
 * copy
 */
export function copy(txt: string = 'null') {
	toClipboard(txt);
	ElNotification({
		// title: computed(() => i18n.global.t("Success")).value,
		message: computed(() => i18n.global.t("CopySuccessful")).value,
		type: 'success',
		duration: 1000
	})
}

/**
 * 更新用户信息
 */
export async function getUserInfo() {
	store.dispatch('status/setLoadingShow', true)
	// let loading = ElLoading.service({
	//     lock: true,
	//     text: 'Loading',
	//     background: 'rgba(0, 0, 0, 0.7)',
	// })
	store.commit("status/getUserInfoLoad", true)
	let a = await UserService.get_user_info({});
	store.dispatch('user/setData', a.data.data)
	store.commit("status/getUserInfoLoad", false)
	// loading.close()
	store.dispatch('status/setLoadingShow', false)
	// 
}
export async function getUserInfoNoLoad() {
	store.commit("status/getUserInfoLoad", true)
	let a = await UserService.get_user_info({});
	store.dispatch('user/setData', a.data.data)
	store.commit("status/getUserInfoLoad", false)
	// 
}
// 退出登录
export async function logoutFun() {
	const state = {
		commission: 0, //佣金
		first_pay_type: 0, //是否是首充
		header_img: 0,  //头像下标
		money: 0, //余额
		new: 0,
		nickname: '', //用户名
		phone: '', //手机号
		remain_code_amount: 0, //剩余打码量
		sh: '', //审核模式
		token: '',
		total_bet: 0, //总打码
		total_money: 0, //总充值
		total_withdraw: 0, //总提现
		uid: 0,
		vip_lv: 0,
		vip_low_lv: 1,
		with_money: 0, //可提现金额
		need_code_amount: 0,
		share_lv: 1,
		share_valid_number: 0,
		vip_day: 0,
		vip_earnings: 0,
		sign_bonus: 0,
		team_one_user_num: 0,
		total_commission: 0,
		CPF: "",
		username: "",
		give_money: 0,
		download_bonus: 0,
	}

	store.dispatch('user/setData', state)
	router.push("/")
	// store.state.user = state as any
}

/**
 *提示 
 */
export function toast(txt: string, data = "") {
	// showToast({ message: i18n.global.t(txt)+data, position: 'top', className: 'toast', teleport: 'body' });
}

/**
 * 字符串补零
 * @param str
 * @param length
 * @returns newStr
 */
export function setStringLength(str: string, length: number) {
	let newStr = '';
	if (str.split(".")[1] && str.split(".")[1].length > length) {
		newStr = `${str.split(".")[0]}.${str.split(".")[1].substring(0, 2)}`;
	} else if (str.split(".")[1] && str.split(".")[1].length < length) {
		newStr = str;
		for (let index = 0; index < length - str.split(".")[1].length; index++) {
			newStr += "0";
		}
	} else if (str.split(".")[1] && str.split(".")[1].length == 2) {
		newStr = str;
	} else if (!str.split(".")[1]) {
		newStr = str + ".00";
	} else {
	}

	return newStr;
}

// 防抖
let debounceTimer: any = null, throttleTimer: any = null
export const debounce = (fn: Function, delay: number = 600): void => {
	let fun = (...args: unknown[]) => {
		if (debounceTimer) {
			clearTimeout(debounceTimer);
		}
		debounceTimer = setTimeout(() => {
			fn.apply(this, args);
		}, delay);
	};
	fun();
};
// 节流
export const throttle = (fn: Function, delay: number = 1000): void => {

	let fun = (...args: unknown[]) => {
		if (throttleTimer) {
			return;
		}
		throttleTimer = setTimeout(() => {
			fn.apply(this, args);
			throttleTimer = null;
		}, delay);
	}
	fun();
}

/**
 * @description: 百分比
 * @param {*} num 
 * @param {*} total
 * @return {*}
 */
export function toPercent(num: number, total: number) {
	const val = (Math.round(num / total * 10000) / 100.00)
	if (val >= 100) return 100
	else return (Math.round(num / total * 10000) / 100.00);// 小数点后两位百分比
}

/**
 * @description: 等级百分比方法
 * @return {*}
 */
export function levelPercent() {
	const vip_conf = store.state.conf.all_conf.vip_conf;
	const vip_lv = store.state.user.vip_lv;
	let idx = 0;
	if (vip_lv >= vip_conf.length - 1) idx = vip_lv;
	else idx = vip_lv + 1;
	const rechargePercent = toPercent(
		store.state.user.total_money,
		vip_conf[idx].recharge
	);
	const rechargeNextLvVal = vip_conf[idx].recharge;

	const betPercent = toPercent(
		store.state.user.total_bet,
		vip_conf[idx].bet
	);
	const betNextLvVal = vip_conf[idx].bet;
	return {
		rechargePercent: rechargePercent,
		rechargeNextLvVal: rechargeNextLvVal,
		betPercent: betPercent,
		betNextLvVal: betNextLvVal
	}
}

// 等级名称
export function levelName(lv: number) {
	const arr: Array<string> = [
		computed(() => i18n.global.t('vipBonus.Novatos')).value,
		computed(() => i18n.global.t('vipBonus.Bronze')).value,
		computed(() => i18n.global.t('vipBonus.Prata')).value,
		computed(() => i18n.global.t('vipBonus.Ouro')).value,
		computed(() => i18n.global.t('vipBonus.Platina')).value,
		computed(() => i18n.global.t('vipBonus.Diamante')).value,
		computed(() => i18n.global.t('vipBonus.DiamantedeSangue')).value,
		computed(() => i18n.global.t('vipBonus.Vibranium')).value,
	]
	return arr[lv]
}

// liveChat弹出
export function clickLivechat() {

	if (store.state.user.token) {

		//@ts-ignore
		LiveChatWidget.call("set_customer_name", store.state.user.uid);
		//@ts-ignore
		LiveChatWidget.call("set_customer_email", store.state.user.phone);
		//@ts-ignore
		if (window.LiveChatWidget) window.LiveChatWidget.call("maximize");
	} else {
		store.dispatch('status/setLoginShow', true)
	}
}

//1、 得到今天、昨天、明天日期
// dates为数字类型，0代表今日,-1代表昨日，1代表明日，返回yyyy-mm-dd格式字符串，dates不传默认代表今日。
export function getDate(dates) {
	let dd = new Date();
	let n = dates || 0;
	dd.setDate(dd.getDate() + n);
	let y = dd.getFullYear();
	let m: any = dd.getMonth() + 1;
	let d: any = dd.getDate();
	m = m < 10 ? "0" + m : m;
	d = d < 10 ? "0" + d : d;
	let day = y + "-" + m + "-" + d;
	return day;
}

export function getLastWeekData() {//获得上周周一~周日的年月日  
	let lastweek = { start_day: '', end_day: '' };
	let date = new Date();
	// 上周一的日期
	date.setDate(date.getDate() - 7 - date.getDay() + 1);
	let m: any = date.getMonth() + 1;
	let d: any = date.getDate();
	m = m < 10 ? "0" + m : m;
	d = d < 10 ? "0" + d : d;
	lastweek.start_day = date.getFullYear() + "-" + m + "-" + d;

	// 上周日的日期
	date.setDate(date.getDate() + 6);
	m = date.getMonth() + 1;
	d = date.getDate();
	m = m < 10 ? "0" + m : m;
	d = d < 10 ? "0" + d : d;
	lastweek.end_day = date.getFullYear() + "-" + m + "-" + d;
	return lastweek
}


//获取cookie
export function getCookie(name) {
	let arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
	if (arr = document.cookie.match(reg))
		return decodeURI(arr[2]);
	else
		return "";
}

//设置cookie
//@param min 分钟数
export function setcookie(name, value, min) {
	let expires;
	if (min) {
		let date = new Date();
		date.setTime(date.getTime() + (min * 60 * 1000));
		expires = "; expires=" + date.toUTCString();
	}
	else {
		expires = "";
	}
	document.cookie = name + "=" + encodeURI(value) + expires + "; path=/";
}

//清除cookie
export function DeleteCookie(name) {
	let cval = getCookie(name);
	if (cval != null) {
		document.cookie = name + "=" + encodeURI(cval) + "; expires=Fri, 31 Dec 1999 23:59:59 GMT" + ";path=/";
	}
}

// 判断是否Safari苹果浏览器
export function isSafari() {
	let ua = navigator.userAgent.toLowerCase();
	if (ua.indexOf('applewebkit') > -1 && ua.indexOf('mobile') > -1 && ua.indexOf('safari') > -1 &&
		ua.indexOf('linux') === -1 && ua.indexOf('android') === -1 && ua.indexOf('chrome') === -1 &&
		ua.indexOf('ios') === -1 && ua.indexOf('browser') === -1) {
		return true;
	} else {
		return false;
	}
}

// 判断设备
export function judgmentEquipment() {
	let client = '';
	if (/(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)) { //判断iPhone|iPad|iPod|iOS
		client = 'iOS';
	} else if (/(Android)/i.test(navigator.userAgent)) { //判断Android
		client = 'Android';
	} else {
		client = 'PC';
	}
	return client;
}

// 下载图片
export const downloadIamge = (imgsrc, name) => {
	// let fileName = new Date().getTime() + ".png";
	// downloadIamge(document.querySelector('.QR_code img').src, fileName);
	//下载图片地址和图片名
	let image = new Image();
	// 解决跨域 Canvas 污染问题
	image.setAttribute("crossOrigin", "anonymous");
	image.onload = function () {
		let canvas = document.createElement("canvas");
		canvas.width = image.width;
		canvas.height = image.height;
		let context: any = canvas.getContext("2d");
		context.drawImage(image, 0, 0, image.width, image.height);
		let url = canvas.toDataURL("image/png"); //得到图片的base64编码数据'
		let a = document.createElement("a"); // 生成一个a元素
		let event = new MouseEvent("click", {
			bubbles: true,
			cancelable: true,
			view: window
		}); // 创建一个单击事件
		a.download = name || "photo"; // 设置图片名称
		a.href = url; // 将生成的URL设置为a.href属性
		a.dispatchEvent(event); // 触发a的单击事件
	};
	image.src = imgsrc;
}

//将毫秒的时间转换成美式英语的时间格式,eg:3rd May 2018
export function englishFormatDate(millinSeconds) {
	var date = new Date(millinSeconds);
	var monthArr = new Array(
		computed(() => i18n.global.t('monthName.jan')).value,
		computed(() => i18n.global.t('monthName.fev')).value,
		computed(() => i18n.global.t('monthName.mar')).value,
		computed(() => i18n.global.t('monthName.abr')).value,
		computed(() => i18n.global.t('monthName.maio')).value,
		computed(() => i18n.global.t('monthName.jun')).value,
		computed(() => i18n.global.t('monthName.jul')).value,
		computed(() => i18n.global.t('monthName.ago')).value,
		computed(() => i18n.global.t('monthName.set')).value,
		computed(() => i18n.global.t('monthName.out')).value,
		computed(() => i18n.global.t('monthName.nov')).value,
		computed(() => i18n.global.t('monthName.dez')).value,
	);
	var suffix = new Array("st", "nd", "rd", "th");

	var year = date.getFullYear(); //年
	var month = monthArr[date.getMonth()]; //月
	var ddate = date.getDate(); //日

	return ddate + " " + month
}


/**
 * 将日期字符串转时间戳
 * @param dateStr 日期字符串
 * @param Joiner 日期字符串的连接符
 */
export function dateStrChangeTimeTamp(dateStr) {

	dateStr = dateStr.substring(0, 19);
	dateStr = dateStr.replace(/-/g, '/');
	let newDate = new Date(dateStr).getTime();
	return newDate;
}

/**
 * 转换时间格式
 * @param date 指定日期
 * @param format 格式 y m d 
 */

export function currentTimeChangeStr(format, date?, join?, join2?) {
	let time;


	let now = new Date();
	time = new Date(date) || now;
	let yy = time.getFullYear();
	let mm = time.getMonth() + 1;
	let dd = time.getDate();
	let hh = time.getHours();
	let ii = time.getMinutes();
	let ss = time.getSeconds();
	let rTime;
	let rTime2;
	let forData = format.split('');
	rTime = `${forData.indexOf('y') !== -1 ? join + yy : ''}${forData.indexOf('m') !== -1 ? mm < 10 ? forData.indexOf('y') !== -1 ? join : '' + '0' + mm : forData.indexOf('y') !== -1 ? join : '' + mm : ''}${forData.indexOf('d') !== -1 ? dd < 10 ? join + '0' + dd : join + dd : ''}`;
	rTime2 = `${forData.indexOf('h') !== -1 ? hh : ''}${forData.indexOf('i') !== -1 ? ii < 10 ? join2 + '0' + ii : join2 + ii : ''}${forData.indexOf('s') !== -1 ? ss < 10 ? join2 + '0' + ss : join2 + ss : ''}`
	return rTime + ' ' + rTime2;
}


/**
 * 
 */
export function stringFormat(txt) {
	// 将输入转换为字符串
	txt = txt.toString();

	// 切分整数部分和小数部分
	let integerPart, decimalPart;
	if (txt.indexOf('.') !== -1) {
		const parts = txt.split('.');
		integerPart = parts[0];

		decimalPart = parts[1].substring(0, 2);
		if (decimalPart.length == 1) {
			decimalPart = decimalPart + '0';
		}
	} else {
		integerPart = txt;
		decimalPart = '00';
	}

	// 处理整数部分的千位分隔符
	if (integerPart.length > 3) {
		const integerArray = integerPart.split('');
		for (let i = integerArray.length - 3; i > 0; i -= 3) {
			integerArray.splice(i, 0, '.');
		}
		integerPart = integerArray.join('');
	}

	// 拼接整数部分和小数部分
	const result = decimalPart ? (integerPart + ',' + decimalPart) : integerPart;

	return result;
}

/**
 * @description: 国家货币方法
 * @param {number} amount 金额
 * @param {boolean} currencySymbol 是否需要带货币符号 
 * @return {*}
 */
export const moneyFormat = (amount: number, currencySymbol: boolean = true) => {
	let a = Number(amount);
	let b
	if (currencySymbol) b = a.toLocaleString('PT', { style: 'currency', currency: 'BRL', currencyDisplay: 'symbol' })
	else b = a.toLocaleString('PT');
	return b
}

export const liveChatLode = (id) => {
	//@ts-ignore
	window.__lc = window.__lc || {};
	//@ts-ignore
	// window.__lc.license = 15427629;
	window.__lc.license = id;
	//@ts-ignore
	; (function (n, t, c) { function i(n) { return e._h ? e._h.apply(null, n) : e._q.push(n) } var e = { _q: [], _h: null, _v: "2.0", on: function () { i(["on", c.call(arguments)]) }, once: function () { i(["once", c.call(arguments)]) }, off: function () { i(["off", c.call(arguments)]) }, get: function () { if (!e._h) throw new Error("[LiveChatWidget] You can't use getters before load."); return i(["get", c.call(arguments)]) }, call: function () { i(["call", c.call(arguments)]) }, init: function () { var n = t.createElement("script"); n.async = !0, n.type = "text/javascript", n.src = "https://cdn.livechatinc.com/tracking.js", t.head.appendChild(n) } }; !n.__lc.asyncInit && e.init(), n.LiveChatWidget = n.LiveChatWidget || e }(window, document, [].slice))
}

export function downloadAPK() {
	let isApk = false
	try {
		//@ts-ignore
		isApk = window.Native.getMyDeviceId ? true : false
	} catch (error) {
		// alert(JSON.stringify(error))
		// console.log(error);
	}
	if (isApk) {
		try {
			//@ts-ignore
			window.Native.openURL(store.state.conf.all_conf.android_url + "c13.apk")
		} catch (error) {
			// alert(JSON.stringify(error))
			// console.log(error);
		}
	} else {
		window.open(store.state.conf.all_conf.android_url + "c13.apk")
	}

}