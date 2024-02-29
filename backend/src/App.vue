<script lang="ts" setup>
import { h } from "vue"
import { useTheme } from "@/hooks/useTheme"
import { ElNotification } from "element-plus"
// 将 Element Plus 的语言设置为中文
import zhCn from "element-plus/lib/locale/lang/zh-cn"
import { storeToRefs } from "pinia";
import confStore from "@/store/modules/conf";
import { agent_list_post } from "@/api/channelManagement";
import { game_list_post, factory_list_post } from "@/api/IntegratorManagement";
import { external_game_list_post, game_type_list_post } from "./api/gameManagement";
import { vip_lv_list } from "./api/userManagenment";
import { getToken } from "@/utils/cache/cookies"
import { reactive } from "vue";
import { provide, nextTick } from "vue";

const state = reactive({
  isReload: true
})

const store = confStore();

const { initTheme } = useTheme()

let { agent_list, factory_list, factory_details_list, external_game_list, gameType, isPc, vipLvList } = storeToRefs(store);

if (getToken()) {
  // 渠道
  agent_list_post({ limit: 999, page: 1 }).then((res: any) => {
    agent_list.value = res.data;
  })
  // 集成商
  factory_list_post({ limit: 999, page: 1 }).then((res: any) => {
    factory_list.value = res.data;
  })
  // 游戏平台 集成商详情接口
  // game_list_post({ limit: 999, page: 1 }).then((res: any) => {
  //   factory_details_list.value = res.data;
  // })
  // 所有游戏
  external_game_list_post({ limit: 999, page: 1 }).then((res: any) => {
    external_game_list.value = res.data;
  })

  // 游戏类型
  game_type_list_post({ limit: 999, page: 1 }).then((res: any) => {
    gameType.value = res.data;
  })


  //get vip_Lv list
  vip_lv_list({ limit: 999, page: 1 }).then((res: any) => {
    vipLvList.value = res.data;
  })
}

/** 初始化主题 */
initTheme()

const reload = () => {
  state.isReload = false
  nextTick(() => {
    state.isReload = true
  })
}
provide('reload', reload)
function felxible() {
  // 获取当前屏幕宽度xp值
  const doc = document.documentElement;
  // 屏幕宽度赋值
  const win_w = doc.clientWidth;
  // 判断屏幕宽度
  if (win_w > 750) {

    isPc.value = true

  } else {
    isPc.value = false
  }
}
// 当屏幕宽度发生变化时给fontsize赋值
window.addEventListener("resize", function () {
  felxible();
});
felxible();
</script>

<template>
  <ElConfigProvider :locale="zhCn">
    <router-view v-if="state.isReload" />
  </ElConfigProvider>
</template>
