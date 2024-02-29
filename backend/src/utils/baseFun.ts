

import router from "@/router"
import { ElNotification } from 'element-plus';
import useClipboard from "vue-clipboard3";

const { toClipboard } = useClipboard();
export function goToUserInfo(uid) {
  router.push({
    name: "userInfo",
    params: {
      uid: uid
    },
  })
}
// 成功弹窗
export function SuccessNotiFun(text) {
  ElNotification({
    title: "成功",
    message: text,
    type: 'success',
    duration: 3000
  })
}
// 成功弹窗
export function WarningNotiFun(text) {
  ElNotification({
    title: "警告",
    message: text,
    type: 'warning',
    duration: 3000
  })
}
// 拷贝
export function copy(txt: string = 'null') {
	toClipboard(txt);
	ElNotification({
		title: "成功",
		message: "复制成功！",
		type: 'success',
		duration: 1000
	})
}