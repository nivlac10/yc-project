<template>
  <!-- <HelloWorld msg="Hello Vue 3 + TypeScript + Vite" /> -->
  <!-- <router-view /> -->
  <router-view v-slot="{ Component }" v-if="pageShow">
    <keep-alive :include="keepAlivePage">
      <component :is="Component" />
    </keep-alive>
  </router-view>
  <login v-show="store.state.status.loginShow" /> <!-- 登陆 -->

  <div v-if="loadingDataState && !pageShow" class="logdin_max_box">
    <div class="loading_box">
      <div class="container">
        <picture>
          <div>
            <img class="logo1" src="@/assets/images/public/newLogo.gif" alt="" />
          </div>
          <!-- <div>
            <img class="logo2" src="@/assets/images/public/logo.png" alt="" />
          </div> -->
        </picture>
        <!-- <span class="loading"></span> -->
        <div class="caption">Loading...</div>
      </div>
    </div>
  </div>

  <img height="1" width="1" style="display:none" :src="pixurl" id="urlpixel" />
  <noscript v-if="liveChatId !== 0"><a :href="`https://www.livechat.com/chat-with/${liveChatId}/`" rel="nofollow">Chat
      with
      us</a>, powered by <a href="https://www.livechat.com/?welcome" rel="noopener nofollow"
      target="_blank">LiveChat</a></noscript>
</template>
<script lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
// import HelloWorld from "./components/HelloWorld.vue";

import {
  computed,
  defineComponent,
  getCurrentInstance,
  reactive,
  toRefs,
  ref,
  watch
} from "vue";
import { useStore } from "@/store/index";
import { ConfService } from "@/api/conf";
import { UserService } from "@/api/user";
import login from "@/views/login/index.vue";
import { useRouter, useRoute } from "vue-router";
import { bonusCabinetFun } from "@/utils/startInterface"
import { liveChatLode } from '@/utils/baseFun'

export default defineComponent({
  name: "app",
  components: { login },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const store = useStore();
    const state = reactive({
      isShieldShow: false,
      loadingDataState: true,
      pageShow: false,
      liveChatId: 0,
    });

    // FB 投放pix img 网页请求
    let pixurl = ref("https://www.facebook.com/tr?id=" + localStorage.getItem('pixel') + "&ev=PageView&noscript=1")
    const keepAlivePage = computed(() => {
      return store.state.keepAlive.keepAliveNames;
    });
    const setKeepAlivePage = () => {
      var arr: Array<string> = [""];
      store.dispatch("keepAlive/setCacheKeepAlive", arr);
    };
    setKeepAlivePage();

    // 判断是否为apk内打开
    // @ts-ignore
    let isApk = window.AndroidEM ? true : false
    // @ts-ignore
    try {
      //@ts-ignore
      isApk = window.Native.getMyDeviceId ? true : false
    } catch (error) {
      // alert(JSON.stringify(error))
      console.log(error);
    }

    store.dispatch("status/setisApk", isApk)

    // 获取所有配置
    const conf = async () => {
      // 获取配置
      let conf = await ConfService.get_conf({});
      if (conf.data.code) {
        store.state.conf.all_conf = conf.data as any;
        state.liveChatId = conf.data.platform.platform_livechat_id;
        liveChatLode(state.liveChatId);
      }
      // 如果客户不属于目标国家 则拦截
      if (conf.data.is_shield == 0) {
        state.isShieldShow = true;
      }
      if (store.state.user.token) {
        let user = await UserService.get_user_token({});
        store.dispatch("status/setUserInfoLoad", false)
        store.dispatch("status/setPlayIngState", false)
        store.dispatch("user/setData", user.data.data);
      }
      //  获取游戏列表
      let game_version = store.state.conf.game_data_version || "0";
      if (game_version != conf.data.game_data_version) {
        let game = await ConfService.get_game_list({
          game_data_version: game_version,
        }); //  游戏列表 游戏版本写入缓存
        if (store.state.conf.game_data_version != game.data.game_data_version) {
          store.state.conf.game_list = game.data as any;
          store.state.conf.game_data_version = game.data.game_data_version;
        }
      }
      state.pageShow = true;
      // 切换loading 状态
      // state.loadingDataState = false;
    };
    try {
      conf();
    } catch (error) {
      console.log(error);

    }


    // 通过屏幕宽度判断是否为移动端
    const screenWidthChange = () => {
      var screenWidth =
        document.body.clientWidth ||
        document.body.scrollWidth ||
        window.screen.availWidth ||
        document.body.offsetWidth;
      if (screenWidth < 768) {
        store.state.status.isPc = false
        // store.commit("status/getIsPc", false);
      } else {
        store.state.status.isPc = true
        // store.commit("status/getIsPc", true);
      }

    };
    screenWidthChange();
    // 监听屏幕宽度判断PC 移动
    window.addEventListener("resize", screenWidthChange);

    const router = useRouter()
    // 获取cid
    let cid = getQueryString("c");
    // 跳转转轮
    if (cid != null) {
      localStorage.setItem("c", cid);
      // if (!isApk) {
      //   router.push("/spin")

      // }
    }
    // 获取邀请人code
    let code = getQueryString("code");
    if (code != null) localStorage.setItem("code", code);

    // 获取链接上的参数
    function getQueryString(name) {
      var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
      var r = window.location.search.substr(1).match(reg);
      if (r != null) return unescape(r[2]);
      return null;
    }

    //是否为安卓端 apk
    //@ts-ignore
    localStorage.setItem('isApp', window?.jsbridge?.appsFlyerEvent ? 'true' : 'false');

    watch(() => store.state.user.token, (val) => {
      if (val) bonusCabinetFun()
    }, { deep: true, immediate: true })
    return { ...toRefs(state), keepAlivePage, pixurl, store };
  },
});

</script>
<style lang="scss" scoped>
#app {
  .loading {
    width: 150px;
    display: block;
    height: 8px;
    margin: 18px auto;
    border-radius: 3px;

    border: 3px solid black;
    // background-color: #313343;
    border-image: linear-gradient(90deg, #323333 0%, #FDA900 51%, #343333 100%) 3;

    position: relative;
    overflow: hidden;
    z-index: 1;
  }

  .loading:before {
    content: "";
    height: 8px;
    width: 40%;
    position: absolute;
    top: 50%;
    -webkit-transform: translate(-34px, -50%);
    -ms-transform: translate(-34px, -50%);
    transform: translate(-34px, -50%);

    background: linear-gradient(270deg, #FB7E45 0%, #9B217D 100%);
    border-radius: 3px;
    -webkit-animation: initial-loading 1.4s infinite ease;
    animation: animation 1.4s infinite ease;
  }

  .caption {
    font-size: 18px;
    color: #98ABD0;
  }

  @-webkit-keyframes animation {
    0% {
      left: 0;
    }

    50% {
      left: 100%;
    }

    100% {
      left: 0;
    }
  }

  @keyframes animation {
    0% {
      left: 0;
    }

    50% {
      left: 100%;
    }

    100% {
      left: 0;
    }
  }

  .container img {
    max-width: 500px;
    width: 80%;
    animation: bounce 1.4s ease infinite;
    -webkit-animation: bounce 1.4s ease infinite;
    -moz-animation: bounce 1.4s ease infinite;
    -ms-animation: bounce 1.4s ease infinite;
    -o-animation: bounce 1.4s ease infinite;
  }

  @-webkit-keyframes bounce {
    0% {
      -webkit-transform: scale(1);
      transform: scale(1);
      -webkit-filter: blur(0);
      filter: blur(0);
    }

    50% {
      -webkit-transform: scale(0.9);
      transform: scale(0.9);
      -webkit-filter: blur(1.4);
      filter: blur(1.4);
    }

    100% {
      -webkit-transform: scale(1);
      transform: scale(1);
    }
  }

  @keyframes bounce {
    0% {
      -webkit-transform: scale(1);
      transform: scale(1);
      -webkit-filter: blur(0);
      filter: blur(0);
    }

    50% {
      -webkit-transform: scale(0.9);
      transform: scale(0.9);
      -webkit-filter: blur(1.4);
      filter: blur(1.4);
    }

    100% {
      -webkit-transform: scale(1);
      transform: scale(1);
    }
  }

  @media (min-width: 1024px) {
    .container img {
      max-width: 500px;
      width: 100%;
    }

    .loading {
      width: 350px;
      height: 16px;
      margin: 20px auto;
    }

    .loading:before {
      width: 40%;
      height: 11px;
    }
  }


  .logdin_max_box {
    width: 100vw;
    height: 100vh;
    background-color: #12151c;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .loading_box_img_box {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .loading_box {
      display: flex;
      flex-direction: column;
      justify-content: center;
      // align-items: center;
      gap: 20px;
      width: 80%;
      text-align: center;

      .logo1 {
        margin-bottom: 17px;
        width: 66px;
      }

      .logo2 {
        width: 100%;
      }

      span {
        text-align: center;
        font-size: 40px;
        font-weight: 600;
        color: #fff;
        margin-bottom: 50px;
      }
    }
  }
}

@media (max-width:768px) {

  .logo1 {
    width: 50px !important;
  }

  .caption {
    font-size: 16px !important;
  }
}
</style>
