// http.ts
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios'
import qs from 'qs'
import { ElMessage } from 'element-plus'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { store } from "@/store/index"
import i18n from '@/lang/index.js'
import router from '../router'
import { computed } from "vue";
import { ElNotification } from 'element-plus'
import { logoutFun } from './baseFun'
const showStatus = (status: number) => {
	let message = ''
	switch (status) {
		case 0:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code0")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 2:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code2")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			logoutFun()
			router.push('/')
			store.dispatch('status/setLoginShow', true)
			break
		case 3:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code3")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			logoutFun()
			router.push('/')
			store.dispatch('status/setLoginShow', true)
			break
		case 4:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code4")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 5:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code5")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 6:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code6")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 7:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code7")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 8:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code8")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 9:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code9")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 10:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code10")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 11:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code11")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 12:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code12")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 13:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code13")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 14:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code14")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 15:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code15")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 16:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code16")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 17:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code17")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 18:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code18")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 19:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code19")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 20:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code20")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 21:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code21")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 22:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code22")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 23:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code23")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 24:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code24")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 25:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code25")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 26:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code26")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 27:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code27")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 28:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code28")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 29:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code29")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 30:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code30")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 31:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code31")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 32:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code32")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 33:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code33")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 34:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code34")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 35:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code35")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 36:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code36")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 37:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code37")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 38:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code38")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 39:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code39")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 40:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code40")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 41:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code41")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 42:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code42")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 43:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code43")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 44:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code44")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 45:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code45")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 46:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code46")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 88:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code88")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 100:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code100")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 101:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code101")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 201:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code201")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		case 202:
			ElNotification({
				message: computed(() => i18n.global.t("httpCode.code202")).value,
				type: 'warning',
				duration: 3000,
				offset: 65,
			})
			break
		default:
			message = `(${status})!`
	}
	return `${message}`
}

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
// axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8'
// axios.defaults.withCredentials = true; //设置CORS跨域 并设置访问权限 允许跨域携带cookie信息
// axios.defaults.headers.common['Authorization'] = ''; // 设置请求头为 Authorization
const service = axios.create({
	// 联调
	// baseURL: process.env.NODE_ENV === 'production' ? `/` : '/api',
	baseURL: `${import.meta.env.VITE_RES_URL}`,
	// baseURL: '/api',
	// headers: {
	// 	get: {
	// 		'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
	// 	},
	// 	post: {
	// 		'Content-Type': 'application/json;charset=utf-8'
	// 	}
	// },
	// 是否跨站点访问控制请求
	// withCredentials: true,
	timeout: 30000,
	// transformRequest: [
	// 	(data) => {
	// 		// json格式
	// 		// data = JSON.stringify(data)
	// 		// return data
	// 		if (!data) return data;
	// 		// formData格式
	// 		const formData = new FormData();
	// 		Object.keys(data).forEach((key) => {
	// 			if (data[key] instanceof Array) {
	// 				data[key].forEach((item) => {
	// 					formData.append(key, item);
	// 				});
	// 				return;
	// 			}
	// 			formData.append(key, data[key]);
	// 		});
	// 		return formData;
	// 	},
	// ],
	validateStatus() {
		// 使用async-await，处理reject情况较为繁琐，所以全部返回resolve，在业务代码中处理异常
		return true
	},
	transformResponse: [(data) => {
		if (typeof data === 'string' && data.startsWith('{')) {
			data = JSON.parse(data)
		}
		return data
	}]

})
// console.log(service.defaults.baseURL);

// 声明一个 Map 用于存储每个请求的标识 和 取消函数
const pending = new Map()
/**
 * 添加请求
 * @param {Object} config 
 */
const addPending = (config: AxiosRequestConfig) => {
	const url = [
		config.method,
		config.url,
		qs.stringify(config.params),
		qs.stringify(config.data)
	].join('&')
	// &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
	// config.cancelToken = config.cancelToken || new axios.CancelToken(cancel => {
	// 	if (!pending.has(url)) { // 如果 pending 中不存在当前请求，则添加进去
	// 		pending.set(url, cancel)
	// 	}
	// })
	// &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
}
/**
 * 移除请求
 * @param {Object} config 
 */
const removePending = (config: AxiosRequestConfig) => {
	const url = [
		config.method,
		config.url,
		qs.stringify(config.params),
		qs.stringify(config.data)
	].join('&')
	if (pending.has(url)) { // 如果在 pending 中存在当前请求标识，需要取消当前请求，并且移除
		const cancel = pending.get(url)
		cancel(url)
		pending.delete(url)
	}
}

/**
 * 清空 pending 中的请求（在路由跳转时调用）
 */
export const clearPending = () => {
	for (const [url, cancel] of pending) {
		cancel(url)
	}
	pending.clear()
	NProgress.done()
}

// 请求拦截器
service.interceptors.request.use((config: AxiosRequestConfig) => {
	NProgress.start()
	removePending(config) // 在请求开始前，对之前的请求做检查取消操作
	addPending(config) // 将当前请求添加到 pending 中

	const { url } = config;
	// if (url != '/login') {
	if (config.method == 'post') {
		config.data = {
			...config.data,
			token: store.state.user.token
		}
	}
	// }
	return config
}, (error) => {
	// 错误抛到业务代码
	error.data = {}
	// error.data.msg = '服务器异常，请联系管理员！'
	// return Promise.resolve(error)
})

// 响应拦截器
service.interceptors.response.use((response: AxiosResponse) => {
	NProgress.done()
	removePending(response) // 在请求结束后，移除本次请求
	const status = response.status
	let msg = ''
	showStatus(response.data.code)
	// if (status < 200 || status >= 300) {
	// 	// 处理http错误，抛到业务代码
	// 	msg = showStatus(status)
	// 	if (typeof response.data === 'string') {
	// 		response.data = { msg }
	// 	} else {
	// 		response.data.msg = msg
	// 	}
	// }

	return response
}, (error) => {
	if (axios.isCancel(error)) {
		console.log('repeated request: ' + error.message)
	} else {
		// handle error code
		// 错误抛到业务代码
		error.data = {}
		// error.data.msg = '请求超时或服务器异常，请检查网络或联系管理员！'
		// ElMessage.error(error.data.msg)
	}
	return Promise.reject(error)
})

import { HttpResponse } from '@/@types'
const post = (url, params) => {
	return new Promise<HttpResponse>((resolve, reject) => {
		service.post(url, params).then(res => {
			resolve(res);
		}).catch(error => {
			console.log('Request exception');
			reject(error);
		})
	})
}

const get = (url, params) => {
	params = params || {};
	return new Promise<HttpResponse>((resolve, reject) => {
		service.get(url, {
			params,
		}).then(res => {
			resolve(res);
		}).catch(error => {
			console.log('Request exception');
			reject(error);
		})
	})
}

export { post, get, service }