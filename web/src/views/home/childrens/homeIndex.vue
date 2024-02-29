<template>
  <div class="homeIndex">
    <banner />
    <gameTypeColumn @def="changePage"></gameTypeColumn>
    <div v-if="pageData.isHome">
      <RouterView> </RouterView>
    </div>
    <div v-else class="no_data">
      <gameLiset :gameList="game_list" :count="count" @def="getGaemList"></gameLiset>
    </div>
    <add-to-home-screen v-if="currentDevice == 'iOS'" />
    <download-app v-else-if="currentDevice == 'Android'" />
    <div class="fixed_box">
      <div>
        <div class="fixed_min_box" style="margin-bottom: 17px;" @click="store.state.status.rollerShow = true">
          <img src="@assets/images/layout/slot.png" alt="">
          <div class="fixed_span_box">
            <span>{{ t('bonusCabinet.SlotGrátis') }}</span>
          </div>
        </div>
        <div class="fixed_min_box" @click="$router.push('/coupon')">
          <img src="@assets/images/layout/pack.png" alt="">
          <div class="fixed_span_box">
            <span>{{ t('sidebar.Cupom') }}</span>
          </div>
        </div>

        <!-- <img src="@assets/images/refer/newRefer/home_Telegram_icon@2x.png" alt="" @click="imgClick"> -->
        <!-- <a :href="store.state.conf.all_conf.android_url" v-if="!store.state.status.isApk && isApp == 'false'">
          <div class="download_btn">
            <img src="@assets/images/layout/Download.png" alt="">
            <span>+{{ t('base.currency') }}2</span>
          </div>
        </a> -->
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "@/store/index";
import banner from "../components/banner.vue";
import gameLiset from "@/components/gameList/index.vue";
import { get_game_data } from "@/utils/gameUtils";
import addToHomeScreen from "@views/addToHomeScreen/index.vue"
import { clickLivechat, judgmentEquipment } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
import downloadApp from "../components/downloadApp.vue";
import gameTypeColumn from "../components/gameTypeColumn.vue";
export default defineComponent({
  name: "homeIndex",
  components: { banner, gameLiset, addToHomeScreen, downloadApp, gameTypeColumn },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const route = useRoute();
    const { t } = useI18n();
    const state = reactive({
      game_type_list: store.state.conf.game_list.game_type,
      game_list: [],
      page: 1,
      limit: 28,
      pageData: {
        game_id: null,
        isHome: true,
        game_type: null,
        is_tag: 0,
        game_name: null,
        is_top: 0,
        is_hot: 0,
        gameListType: 0
      },
      typeIndex: 0,
      isApp: null,
      currentDevice: '',
      factory_list: [],
      count: 0
    });
    state.isApp = localStorage.getItem("isApp") as any;
    state.factory_list = store.state.conf.game_list.factory_list as any;
    state.currentDevice = judgmentEquipment()// 获取当前设备

    const changePage = (data: any) => {
      state.pageData.game_name = data
      if (data != null) {
        state.pageData.isHome = false
      } else {
        state.pageData.isHome = true
      }
      state.page = 1
      state.game_list = []
      getGaemList()
    }
    const getGaemList = () => {
      let gameList = get_game_data(state.pageData.game_id, state.pageData.game_type, state.pageData.game_name, state.pageData.is_top, state.pageData.is_hot, state.pageData.is_tag, state.page, state.limit)
      state.page++
      for (let i = 0; i < gameList.allGameList.length; i++) {
        // @ts-ignore
        state.game_list.push(gameList.allGameList[i])
      }
      state.count = gameList.count
    }
    const imgClick = () => {
      window.open(store.state.conf.all_conf.tg_channel_url)
    }

    return { ...toRefs(state), store, changePage, getGaemList, imgClick, t };
  },
});
</script>
<style  lang="scss" scoped>
.homeIndex {
  .fixed_box {

    position: fixed;
    right: 14px;
    bottom: 160px;
    z-index: 98;
    display: none;

    .fixed_min_box {
      // width: 100%;
      // margin-right: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;

      .fixed_span_box {
        background: linear-gradient(to top right, #F76336, #953BCF);
        border-radius: 50px;
        padding: 3px 15px;

        span {
          text-align: center;
          color: #fff;
          font-size: 13px;
        }
      }
    }

    div {
      display: flex;
      flex-direction: column;
      // gap: 10px;

      img {
        width: 50px;
      }

      .download_btn {
        position: relative;

        span {
          position: absolute;
          left: 50%;
          bottom: -12px;
          transform: translateX(-50%);
          display: inline-block;
          padding: 3px 5px;
          font-size: 12px;
          color: var(--theme-font-color-fff);
          background: linear-gradient(225deg, #4975FE 0%, #AF72FF 100%);
          border-radius: 8px;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .homeIndex {
    .fixed_box {
      display: block;
    }
  }
}
</style>
