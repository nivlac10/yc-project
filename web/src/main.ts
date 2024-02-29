import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { store, key } from './store'
import { service } from './utils/http'
import svgIcon from './icons/index.vue'
import vant from "./plugins/vant"
import "@/style/base.scss"
import "@/style/common.scss"
import 'element-plus/theme-chalk/display.css'
import mitt from 'mitt'
import i18n from '@/lang/index.js'
import "@/utils/rem"
import VueLuckyCanvas from '@lucky-canvas/vue'

const app = createApp(App)
// 挂载全局属性和方法
app.config.globalProperties.$http = service
app.config.globalProperties.$mitt = mitt();

app.use(i18n).use(router).use(store, key).use(vant).use(VueLuckyCanvas).component('svg-icon', svgIcon).mount('#app')