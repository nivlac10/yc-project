<template>
  <div class="layout">
    <audio @timeupdate="updateProgress" controls ref="audioRef" :src="store.state.music.audioUrl" style="display: none">
      <!-- <source :src="audioUrl" type="audio/mpeg" /> -->
      <!-- Seu navegador não suporta reprodução de áudio -->
    </audio>
    <loading-index v-if="store.state.status.loadingShow" />
        <!-- 签到页vip详情弹窗 -->
    <vipCheckInPop></vipCheckInPop> 
    <!-- loading..... -->
    <!-- <sign-in v-if="store.state.status.signInShow" /> 签到 -->
    <!-- <daily-betting-bonus v-if="store.state.status.dailyBettingBonusShow" /> 每日投注奖金 -->
    <!-- <supply-crate v-if="store.state.status.supplyCrateShow" /> 补给箱 -->
    <!-- <super-invitation-popup /> 超级邀请宝箱 -->
    <deposit-com v-if="store.state.status.depositShow" />
    <!-- 充值提现 -->
    <announcement v-if="store.state.status.announcementShow" />
    <activityPopup />
    <!-- <login v-show="store.state.status.loginShow" /> 登陆 -->
    <Cumulativerechargebonus v-if="store.state.status.isBônusdepósito"></Cumulativerechargebonus>
    <gamePop v-if="store.state.status.allGameShow"></gamePop>
    <roller v-if="store.state.status.rollerShow"></roller>
    <audio-index v-if="store.state.music.musicShow" />
    <!-- 滚轮 -->
    <header-com class="headerCom" />
    <div class="layout_content">
      <sidebar-com :class="{
        sidebarCom: true,
        sidebarCom_transition: !store.state.status.sidebarIsShow,
        showSidebarCom: true,
        'hidden-xs-only': true,
      }" />
      <div class="sidebar_phone">
        <el-drawer v-model="store.state.status.sidebarIsShow" direction="ltr" :with-header="false" z-index="10000">
          <sidebar-com :class="{
            sidebarCom: true,
            sidebarCom_transition: !store.state.status.sidebarIsShow,
            showSidebarCom: true,
          }" />
        </el-drawer>
      </div>
      <div class="content_box" id="content_box">
        <div class="container">
          <content-com class="contentCom" />

          <!-- <div class="customer_box">
            <img
              class="customer"
              src="@assets/images/layout/customer_icon.png"
              alt=""
            />
          </div> -->
          <deposito v-if="!store.state.status.isPc"></deposito>
        </div>
        <footer-com />
      </div>
      <deposito v-if="store.state.status.isPc"></deposito>
    </div>
    <tabbar-com />
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, onMounted, ref } from "vue";
import { useStore } from "@/store/index";
import headerCom from "./components/header.vue";
import sidebarCom from "./components/sidebar.vue";
import contentCom from "./components/content.vue";
import footerCom from "./components/footer.vue";
import tabbarCom from "./components/tabbar.vue";
import login from "@/views/login/index.vue";
import depositCom from "@/views/deposit/index.vue";
import deposito from "../deposito/index.vue";
import signIn from "@/views/signIn/index.vue";
import dailyBettingBonus from "@views/dailyBettingBonus/index.vue";
import supplyCrate from "@views/supplyCrate/index.vue";
import { getCookie, setcookie } from "@/utils/baseFun";
import loadingIndex from "@com/loading/index.vue";
// import superInvitationPopup from "@views/superInvitationPopup/index.vue"
import announcement from "../announcement/index.vue";
import gamePop from "@/views/gamePop/index.vue";
import activityPopup from "@views/activityPopup/index.vue";
import roller from "@/components/Roller/index.vue";
import audioIndex from "@com/aPlayer/index.vue"
import Cumulativerechargebonus from "@/components/Cumulativerechargebonus/Cumulativerechargebonus.vue"
import vipCheckInPop from '../vipBonus/childrens/vipCheckIn.vue';

export default defineComponent({
  name: "index",
  components: {
    headerCom,
    sidebarCom,
    contentCom,
    footerCom,
    tabbarCom,
    login,
    depositCom,
    deposito,
    signIn,
    dailyBettingBonus,
    supplyCrate,
    loadingIndex,
    // superInvitationPopup,
    announcement,
    gamePop,
    activityPopup,
    roller,
    audioIndex,
    Cumulativerechargebonus,
    vipCheckInPop
  },
  setup() {
    const store = useStore();
    const state = reactive({});

    store.state.status.announcementShow = false;
    
    // ------------------
    store.dispatch("status/setLoadingShow", false); // loading show


    const audioRef: any = ref(null)
    onMounted(async () => {
      audioInit(); // 音频初始化
      store.state.music.audioDom = audioRef.value // 获取音频dom
      if (!store.state.status.noBônusdepósito) {
        store.state.status.isBônusdepósito = true;
      }
    });
    // 音频初始化
    const audioInit = () => {
      store.state.music.audioUrlList = store.state.conf.all_conf['music_list'] // 获取音乐列表
      store.state.music.audioUrl = store.state.music.audioUrlList[store.state.music.currentAudioIdx].path
      var myVid = audioRef.value;
      myVid.loop = false;

      const initFun = () => {
        store.state.music.audioStatus = "pause"; // 显示播放icon
        store.state.music.audioDuration = 0 // 进度条初始化
        store.state.music.audioStart = '00:00'
        store.state.music.duration = '00:00'
      }
      // 监听音频播放完毕
      myVid.addEventListener(
        "ended",
        () => {
          initFun()
          store.dispatch('music/setPlayAudioMode') // // 设置播放音频模式
        },
        false
      );
      if (myVid != null) {
        initFun()
        myVid.oncanplay = function () {
          store.state.music.duration = transTime(myVid.duration); // 计算音频时长
        };
        myVid.volume = store.state.music.audioVolume / 100; // 设置音量
      }
    }
    /**
     * @description: 音频播放时间换算
     * @param {*} time 音频当前播放时间，单位秒
     * @return {*}
     */
    const transTime = (time: string) => {
      var duration = parseInt(time);
      var minute: any = parseInt((duration / 60).toString());
      var sec = (duration % 60) + "";
      var isM0 = ":";
      if (minute === 0) minute = "00";
      else if (minute < 10) minute = "0" + minute;

      if (sec.length === 1) sec = "0" + sec;

      return minute + isM0 + sec;
    }

    // 更新进度条与当前播放时间
    const updateProgress = (e) => {
      store.dispatch('music/setUpdateProgress', e)
    }

    // console.log(((new Date(new Date().setHours(23, 59, 59, 999)).getTime() - new Date().getTime()) / 1000 / 60).toFixed(0)); // 当天剩余分钟
    // console.log(new Date(new Date().setHours(0, 0, 0, 0)).getTime()); // 当天开始时间戳
    // console.log(new Date(new Date().setHours(23, 59, 59, 999)).getTime()); // 当天结束时间戳
    // 设置签到当天内自动弹一次
    // if (!getCookie('signInShowFlag')) {
    //   // 当天剩余时间 分钟
    //   const time = ((new Date(new Date().setHours(23, 59, 59, 999)).getTime() - new Date().getTime()) / 1000 / 60).toFixed(0)
    //   setcookie('signInShowFlag', true, time)
    //   store.state.status.signInShow = true
    // }

    return { ...toRefs(state), store, updateProgress, audioRef };
  },
});
</script>
<style lang="scss" scoped>
$navBarheight: 80px;

.layout {
  min-height: 100vh;
  background: var(--theme-background);

  .headerCom {
    position: fixed;
    top: 0;
    z-index: 99;
    width: 100%;
  }

  .layout_content {
    position: relative;
    padding-top: $navBarheight;
    display: flex;
    overflow: hidden;

    .sidebar_phone {
      display: none;

      :deep(.el-overlay) {
        top: 80px;
      }

      :deep(.el-drawer) {
        width: auto !important;
        background: var(--theme-menu-background);

        .el-drawer__body {
          padding: 0;
        }
      }
    }

    .sidebarCom {
      position: relative;
      z-index: 1001;
      // padding-left: 19px;
      width: 260px;
      min-height: 100%;
      flex-shrink: 0;
      transition: 0.2s all ease;
      overflow: hidden;
      overflow-y: scroll;
    }

    .showSidebarCom {
      display: block;
    }

    .sidebarCom_transition {
      padding-left: 0;
      width: 0 !important;
    }

    .content_box {
      position: relative;
      height: calc(100vh - $navBarheight);
      overflow-y: scroll;
      overflow-x: hidden;
      width: 100%;

      .container {
        position: relative;
      }

      .customer {
        position: absolute;
        right: -100px;
      }
    }

    .customer_box {
      display: block;
      position: fixed;
      top: 50%;
      right: 50%;
      z-index: 1;
      transform: translate(600px, -50%);
    }
  }
}

@media screen and (max-width: 768px) {
  $navBarheight: 44px;

  .layout {
    .layout_content {
      padding-top: $navBarheight;

      .sidebar_phone {
        :deep(.el-overlay) {
          top: 44px;
        }
      }
    }

    .customer_box {
      display: none;
    }

    .content_box {
      height: auto !important;
    }

    .sidebarCom {
      // padding-left: 20px !important;
      width: 232px !important;
      min-height: auto !important;
    }

    .sidebar_phone {
      display: block !important;
    }

    .showSidebarCom {
      // display: none !important;
    }
  }
}
</style>
