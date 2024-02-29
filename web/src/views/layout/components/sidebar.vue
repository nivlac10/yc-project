<template>
  <div class="sidebar">
    <div class="sidebar_box">
      <div class="paddingBox">
        <div class="imgBox">
          <!-- <img :src="v" alt="" srcset="" v-for="v in imgList"> -->

          <div :style="{ background: `url(${v.url})` }" v-for="(v, i) in  (imgList as any) "
            :class="`${imgListIdx == v.path ? `sl_txt_shadow` : ''} imgBoxdiv`" @click="imgClickJump(v.path)">
            {{ v.txt }}
            <div class="visible" v-if="isVisible && v.path == '/bonusCabinet'">
              {{ t('sidebar.JogueGanhe') }}
            </div>
          </div>

          <!-- <div v-for="(v, i) in  (imgList as any) " :style="{ background: `url(${v.url})` }"
            :class="imgListIdx == v.path ? `sl_txt_shadow` : ''" @click="imgClickJump(v.path)"
            v-show="v.path !== '/bonusCabinet'">
            {{ v.txt }}
          </div> -->
        </div>
        <div class="promoções">{{ t('sidebar.promoções') }}</div>
        <div class="imgGridBox">
          <div v-for="(v, i) in  (imgGridList as any) " :style="{ background: `url(${v.url})` }"
            :class="imgListIdx == v.path ? `sl_txt_shadow` : ''" @click="imgClickJump(v.path)">
            {{ v.txt }}
          </div>
        </div>

        <music-small />
        
        <div :class="`${imgListIdx == '/TodosOsBouns' ? `sl_txt_shadow` : ''} allBounsBtn`"
          @click="imgClickJump('/TodosOsBouns')">
          <img src="@/assets/images/layout/Sidebar/image463.png" alt="" srcset="" />
          <p>{{ t('sidebar.TodososBônus') }}</p>
        </div>
        <div class="Jogar promoções">{{ t('sidebar.JogarBIGWIN') }}</div>
        <div :class="{ demoCollapseCoumn: true, active: activeName == '1' }">
          <el-collapse v-model="activeName" accordion>
            <el-collapse-item name="1">
              <template #title>
                <div class="select_box">
                  <div class="selected_column">
                    <div class="l_box">
                      <img src="@/assets/images/layout/Sidebar/Casino.png" alt="" />
                      <span>{{ t('sidebar.Cassino') }}</span>
                    </div>
                  </div>
                </div>
              </template>
              <div class="list">
                <div class="tab_list">
                  <ul class="tab_list_ul">
                    <li v-for="(item, index) in fontList[0]" :key="index" @click="imgClickJump(item.path)">
                      <img :src="item.icon" alt="" />
                      <span>
                        {{ item.txt }}
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>

        <div :class="{ demoCollapseCoumn: true, active: CasionName == '1' }">
          <el-collapse v-model="CasionName" accordion>
            <el-collapse-item name="1">
              <template #title>
                <div class="select_box">
                  <div class="selected_column">
                    <div class="l_box">
                      <img src="../../../assets/images/layout/Sidebar/fornecedor_icon.png" alt="" />
                      <span>{{ t('sidebar.Fornecedor') }}</span>
                    </div>
                  </div>
                </div>
              </template>
              <div class="list">
                <div class="tab_list">
                  <ul class="tab_list_ul2">
                    <li v-for="(item, index) in fontList[1]" :key="item.game_id" @click="openAllGameBox(item.game_id)">
                      <span>
                        {{ item.game_name }}
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>

        <div class="promoções Outra">{{ t('sidebar.Outra') }}</div>

        <div class="sidebar_box_top">
          <div v-for="(item, index) in tabList" :key="item['title']">
            <div class="list">
              <ul>
                <li v-for="(item2, index2) in item" :key="index2" @click="tabClick(item2)" @mouseenter="hover(index2)"
                  @mouseleave="tabIdx2 = null" :style="`display:${item2['path'] == 'download' && isApp == 'true' ? 'none' : 'flex'
                    } ;`">
                  <img :src="item2.value == tabIdx2 ? item2.img2 : item2.img" alt="" />
                  <span :class="{ sl_font: item2.value == tabIdx }">{{
                    item2.title
                  }}</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="download" @click="tabClick({ path: 'download' })">
            <img src="@/assets/images/layout/Sidebar/downloadAPP.png" alt="" />
            <p>{{ t('btnName.BaixaroAPP') }}</p>
          </div>
        </div>
      </div>

      <div class="img_list_1">
        <img src="@assets/images/sidebar/Telegram_icon@2x.png" alt="" @click="jumpTo(0)" />
        <img src="@assets/images/sidebar/Twittr_icon@2x.png" alt="" />
        <img src="@assets/images/sidebar/Facebook_icon@2x.png" alt="" />
        <img src="@assets/images/sidebar/instagram_icon@2x.png" alt="" />
        <img src="@assets/images/sidebar/YouTube_icon@2x.png" alt="" />
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import {
  reactive,
  toRefs,
  getCurrentInstance,
  defineComponent,
  computed,
  ref,
  watch,
} from "vue";
import { useStore } from "@/store/index";
import { getImageUrl, clickLivechat, WarningNotiFun, downloadAPK } from "@/utils/baseFun";
import { useRouter, useRoute } from "vue-router";
import router from "@/router";
import { useI18n } from "vue-i18n";
import { backgroundSize } from "html2canvas/dist/types/css/property-descriptors/background-size";
// import musicSmall from "./musicSmall.vue";

export default defineComponent({
  name: "sidebar",
  // components: { musicSmall },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();
    const { t, locale } = useI18n();
    let { proxy } = getCurrentInstance() as any;
    let isVisible = ref(false);

    let imgListIdx = ref("");
    const state = reactive({
      imgList: [
        {
          url: getImageUrl("layout/Sidebar/Garmário_de_bônus.png"),
          path: "/bonusCabinet",
          txt: computed(() => t('sidebar.GabineteBônus')),
        },
        {
          url: getImageUrl("layout/Sidebar/recompensas_VIP.png"),
          path: "/vipBonus",
          txt: computed(() => t('sidebar.BônusVIP')),
        },
        {
          url: getImageUrl("layout/Sidebar/bônus_de_convite.png"),
          path: "/refer",
          txt: computed(() => t('sidebar.BônusdeConvite')),
        },
        // {
        //   url: getImageUrl('layout/Sidebar/concorrência.png'),
        //   path: "",
        //   txt: 'Concorrência',
        // },
      ],
      imgGridList: [
        {
          url: getImageUrl("layout/Sidebar/bônus_de_perda.png"),
          path: "/supplyCrate",
          txt: computed(() => t('sidebar.BônusPerdido')),
        },
        // {
        //   url: getImageUrl("layout/Sidebar/bônus_de_login.png"),
        //   path: "/signIn",
        //   txt: computed(() => t('sidebar.BônusEntrada')),
        // },
        {
          url: getImageUrl("layout/Sidebar/Bônus_depósito.png"),
          path: "isBônusdepósito",
          txt: computed(() => t('sidebar.BônusDepósito')),
        },
        {
          url: getImageUrl("layout/Sidebar/cupom.png"),
          path: "/coupon",
          txt: computed(() => t('sidebar.Cupom')),
        },
        {
          url: getImageUrl("layout/Sidebar/rodadas_grátis.png"),
          path: "/roller",
          txt: computed(() => t('sidebar.SlotGrátis')),
        },
      ],
      fontList: [
        [
          {
            txt: computed(() => t('gameType.Salão')),
            icon: getImageUrl("layout/frontPage/Salão.png"),
            path: "/clHome",
          },
          {
            txt: computed(() => t('gameType.Coletar')),
            icon: getImageUrl("layout/frontPage/Coletar_icon.png"),
            path: "/flag",
          },
          {
            txt: computed(() => t('gameType.Popular')),
            icon: getImageUrl("layout/frontPage/hot.png"),
            path: "/hot",
          },
          {
            txt: computed(() => t('gameType.InHouse')),
            icon: getImageUrl("layout/frontPage/in-house.png"),
            path: "/in-house",
          },
          {
            txt: computed(() => t('gameType.Slot')),
            icon: getImageUrl("layout/frontPage/Slot_icon.png"),
            path: "/gameType/0",
          },
          // {
          //   txt: computed(() => t('gameType.Pescaria')),
          //   icon: getImageUrl("layout/frontPage/Pescaria_icon.png"),
          //   path: "/gameType/3",
          // },
          // {
          //   txt: computed(() => t('gameType.JogosMesa')),
          //   icon: getImageUrl("layout/frontPage/Mesa_Jogos_icon.png"),
          //   path: "/gameType/1",
          // },
          // {
          //   txt: computed(() => t('gameType.AoVivo')),
          //   icon: getImageUrl("layout/frontPage/Ao_Vivo_icon.png"),
          //   path: "/gameType/2",
          // },
        ],
        [...store.state.conf.game_list.factory_list],
      ],
      tabList: [
        [
          {
            img: getImageUrl("layout/Sidebar/anúncio_icon.png"),
            img2: getImageUrl("layout/Sidebar/anúncio_icon2.png"),
            title: computed(() => t('sidebar.Anuncio')),
            value: 7,
            path: "announcement",
          },
          {
            img: getImageUrl("layout/Sidebar/HelpCenter.png"),
            img2: getImageUrl("layout/Sidebar/HelpCenter2.png"),
            title: computed(() => t('sidebar.Ajuda')),
            value: 8,
            path: "/help",
          },
          {
            img: getImageUrl("layout/Sidebar/LiveSupport.png"),
            img2: getImageUrl("layout/Sidebar/LiveSupport2.png"),
            title: computed(() => t('headerUser.Suporteaovivo')),
            value: 9,
            path: "live",
          },
        ],
      ],
      tabIdx: 0,
      tabIdx2: null,
      value: {},
      options: [
        {
          value: "EN",
          label: "English",
          img: getImageUrl("language/english_flag.png"),
        },
        {
          value: "PT",
          label: "Portugues",
          img: getImageUrl("language/Flag_of_Brazil.png"),
        },
      ],
      isApp: null,
      activeName: "",
      CasionName: "",
    });

    state.isApp = localStorage.getItem("isApp") as any;

    const showisVisible = () => {
      for (const key in store.state.startData.bonusCabinet) {
        const e = store.state.startData.bonusCabinet[key];
        if (e == 1) {
          isVisible.value = true;
        }
      }
      if (store.state.vipBonusState.bonus_num == 1) {
        isVisible.value = true;
      }
    };
    showisVisible();

    const setSelector = () => {
      if (localStorage.getItem("lang")) {
        state.options.map((e) => {
          if (e.value == localStorage.getItem("lang")) {
            state.value = e;
          }
        });
      }
    };
    setSelector();
    // state.value = state.options[0];

    const changeSelect = (val: string) => {
      locale.value = val;

      // proxy.$i18n.locale = val;
      localStorage.setItem("lang", val);
      for (let i = 0; i < state.options.length; i++) {
        const e = state.options[i];
        if (e.value == val) {
          state.value = e;
          break;
        }
      }
    };

    // tab点击
    const tabClick = (item) => {
      // if (item.path != 'live' || item.path != 'tgOpen') state.tabIdx = item.value;
      // if (item.path == "signIn") store.state.status.signInShow = true;
      // else
      if (item.path == "live") clickLivechat();
      // else if (item.path == 'sssssssssss') store.dispatch('status/setDailyBettingBonusShow', true)
      // else if (item.path == 'aaaaaaaaaaa') store.dispatch('status/setSupplyCrateShow', true)
      else if (item.path == "download") {
        // WarningNotiFun("TheDownload")
        // router.push(item.path);
        // window.open(store.state.conf.all_conf.android_url + "bigwin777-c13.apk")
        downloadAPK();
      } else if (item.path == "announcement") {
        store.state.status.announcementShow = true;
      } else if (item.path == "tgOpen") {
        window.open(store.state.conf.all_conf.tg_channel_url);
      } else if (item.path) {
        router.push(item.path);
      }
      if (!store.state.status.isPc) store.state.status.sidebarIsShow = false;
    };

    // tab选中
    const tabActive = (path) => {
      // for (let i = 0; i < tabList.length; i++) {
      //   const elementI = tabList[i];
      //   for (let j = 0; j < elementI.length; j++) {
      //     const elementJ = elementI[j];
      //     if (path == elementJ.path) state.tabIdx = elementJ.value
      //   }
      // }
      // if (store.state.status.signInShow) state.tabIdx = 2
      // if (store.state.status.dailyBettingBonusShow) state.tabIdx = 9
      // if (store.state.status.supplyCrateShow) state.tabIdx = 10
    };
    watch(
      () => route,
      (to, from) => {
        tabActive(to.path);
      },
      { deep: true, immediate: true }
    );
    watch(
      () => [
        store.state.status.signInShow,
        store.state.status.dailyBettingBonusShow,
        store.state.status.supplyCrateShow,
      ],
      (val) => {
        val.forEach((item: boolean, index: number) => {
          tabActive(route.path);
          if (item) {
            if (index == 0) state.tabIdx = 2;
            // else if (index == 1) state.tabIdx = 9
            // else if (index == 2) state.tabIdx = 10
          }
        });
      },
      { deep: true, immediate: true }
    );

    const imgClickJump = (path: string) => {
      imgListIdx.value = path;
      if (path !== "" && path) {
        if (path == "/roller") {
          if (store.state.user.token && store.state.user.token !== "") {
            store.dispatch("status/setRollerShow", true);
          } else {
            store.dispatch("status/setLoginShow", true);
          }
        } else if (path == 'isBônusdepósito') {
          store.state.status.isBônusdepósito = true
        } else {
          router.push(path);
        }

        if (!store.state.status.isPc) {
          store.state.status.sidebarIsShow = false;
        }
      }
    };

    const jumpTo = (index) => {
      let path = [
        { name: "tg", url: store.state.conf.all_conf.tg_channel_url },
        { name: "twitter", url: "https://twitter.com/bigwin777io" },
        { name: "Facebook", url: "https://www.facebook.com/bigwin777.io" },
        { name: "Instagram", url: "https://www.instagram.com/bigwin777.io/" },
        {
          name: "youtube",
          url: "https://www.youtube.com/channel/UC5XmBVsYrdTsD98314GJqtg",
        },
      ];
      window.open(path[index].url);
    };
    const openAllGameBox = (game_id) => {
      store.state.status.allGameShow = true;
      store.state.status.game_id = game_id;
    };

    const hover = (idx) => {
      state.tabIdx2 = idx + 7;
    };

    return {
      ...toRefs(state),
      t,
      tabClick,
      changeSelect,
      jumpTo,
      imgClickJump,
      imgListIdx,
      openAllGameBox,
      hover,
      isVisible,
      store,
    };
  },
});
</script>
<style lang="scss" scoped>
.sidebar {
  user-select: none;
  width: 100%;
  height: calc(100vh - 80px);
  background: var(--theme-menu-background);
  // padding: 20px 35px;
  white-space: nowrap;
  box-sizing: border-box;

  .visible {
    background: url("@/assets/images/layout/Sidebar/wireframe.png") no-repeat;
    background-size: 100% 100%;
    border: none;
    width: 145px !important;
    height: 28px !important;
    min-width: 145px !important;
    font-size: 12px !important;
    color: #fff;
    padding: 0;
    box-sizing: unset;
    display: flex;
    justify-content: center;
    padding-top: 5px;
    position: absolute;
    top: -22px;
    right: 0;
  }

  .sidebar_box {
    width: 100%;
    height: 100%;
    display: flex !important;
    flex-direction: column;
    justify-content: space-between;
    background: #202330;

    .paddingBox {
      padding: 24px 24px 0px 24px;

      .imgBox {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 12px;

        .imgBoxdiv {
          width: 212px;
          height: 56px;
          background-size: 100% 100% !important;
          color: #fff;
          cursor: pointer;
          white-space: pre-wrap;
          box-sizing: border-box;
          padding: 10px 0px 10px 14px;
          font-size: 18px;
          font-weight: 800;
          display: flex;
          align-items: center;
          position: relative;
        }
      }

      .imgGridBox {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        row-gap: 12px;
        column-gap: 12px;

        div {
          background-size: 100% 100% !important;
          height: 56px;
          color: #fff;
          cursor: pointer;
          white-space: pre-wrap;
          font-size: 13px;
          font-weight: bold;
          padding-top: 8px;
          padding-left: 6px;
          box-sizing: border-box;

          &:nth-child(3) {
            padding-top: 12px;
          }
        }
      }

      .promoções {
        color: #585e77;
        font-size: 18px;
        margin: 20px 0 16px 0;
        font-weight: 800;
      }

      .Jogar {
        margin: 20px 0 16px 0;
      }

      .Outra {
        margin: 20px 0 16px 0;
      }

      .allBounsBtn {
        width: 100%;
        height: 51.52px;
        background: url("@/assets/images/layout/Sidebar/Todososbônus.png") no-repeat;
        background-size: 100% 100%;
        margin: 16px 0 28px 0;
        cursor: pointer;
        display: flex;
        align-items: center;
        padding-left: 22px;
        box-sizing: border-box;

        img {
          width: 38px;
          height: 32px;
        }

        p {
          color: #fff;
          font-size: 16px;
          font-weight: bold;
        }
      }

      .fontListBox {
        div {
          // display: flex;
          // justify-content: center;
          // align-items: center;

          img {
            width: 28px;
          }

          p {
            font-size: 14px;
            color: #98abd0;
          }
        }
      }

      .sidebar_box_top {
        width: 100%;

        .list {
          ul {
            padding-left: 14px;
          }
        }
      }
    }
  }

  .title {
    margin-bottom: 10px;
    font-size: 16px;
    font-weight: bold;
    color: var(--auxiliary-font-color-1);
  }

  .list {
    // margin-bottom: 20px;
    margin-top: 2px;

    ul {
      li {
        cursor: pointer;
        display: flex;
        align-items: center;
        margin-bottom: 4px;
        width: 220px;
        height: 36px;

        border-radius: 8px;

        &:hover {
          background: #2f3445;
        }

        img {
          width: 28px;
          margin-right: 9px;
        }

        span {
          font-size: 16px;
          color: #98abd0;
          vertical-align: middle;
        }
      }
    }
  }

  :deep(.el-select) {
    width: 214px;

    .el-input__wrapper {
      background: transparent;
      box-shadow: none;
      border: 2px solid var(--auxiliary-font-color-9);
      border-radius: 8px;

      input {
        color: var(--auxiliary-font-color-9);
        font-size: 18px;
      }
    }

    .is-focus {
      box-shadow: none;
    }
  }

  .img_list_1 {
    width: calc(100% - 38px);
    background: #2d3144;
    margin-top: 24px;
    padding: 27px 19px;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    justify-items: center;
    align-items: flex-start;
    padding-bottom: 75px;

    img {
      // margin-right: 8px;
      width: 30px;
    }
  }

  .download {
    margin-top: 28px;
    width: 100%;
    // margin-right: 19px;
    height: 44px;
    background: #4181ee;
    border-radius: 8px;
    display: flex;
    align-items: center;
    cursor: pointer;
    justify-content: center;

    img {
      width: 28px;
      // margin-left: 34px;
      // margin-right: 10px;
    }

    p {
      font-size: 16px;
      font-weight: 400;
      color: #fff;
    }
  }

  .demoCollapseCoumn {
    margin-bottom: 10px;

    :deep(.el-collapse) {
      border: none;
      // background: var(--theme-button-background);
      border-radius: 8px;

      &:hover {
        background: var(--theme-button-background);
      }

      .el-collapse-item__header {
        height: 40px;
        background: transparent;
        border: none;
        // font-size: 18px;
        color: #98abd0;
        align-items: center;

        .el-collapse-item__arrow {
          font-size: 20px;
          font-weight: bold;
          color: var(--auxiliary-font-color-1);
        }
      }

      .el-collapse-item__wrap {
        background: transparent;
        border: none;
      }

      .el-collapse-item__content {
        padding-bottom: 0;
      }

      .el-collapse-item__arrow {
        background: url(@assets/images/public/Frame_r.png) no-repeat;
        background-size: 100% 100%;
        font-size: 14px !important;

        svg {
          display: none;
        }
      }
    }

    .tab_list {
      .tab_list_ul {
        padding-left: 14px;
      }

      .tab_list_ul2 {
        padding-left: 18px;
      }

      ul {
        padding: 10px;
        padding-top: 0;
        display: flex;
        flex-direction: column;
        // gap: 4px;

        li {
          display: flex;
          align-items: center;
          // width: 100%;
          border-radius: 8px;
          // padding: 5px;
          gap: 4px;

          &.active_tab {
            background-color: var(--theme-box-background);
          }

          img {
            // margin-right: 9px;
            // width: 40px;
            width: 28px;
          }

          span {
            color: var(--auxiliary-font-color-9);
            font-size: 14px;
          }
        }
      }
    }
  }

  .active {
    :deep(.el-collapse) {
      background: var(--theme-button-background);
    }

    .el-collapse-item__header {
      color: var(--theme-font-color-fff);
    }

    .select_box {
      .selected_column {
        .l_box {
          span {
            color: #fff;
          }
        }
      }
    }
  }

  .select_box {
    width: 100%;
    border-radius: 8px;

    .selected_column {
      display: flex;
      justify-content: space-between;
      align-items: center;
      // padding: 0 14px;
      // background: var(--auxiliary-background-6);
      border-radius: 8px;
      height: 100%;
      width: 100%;

      .l_box {
        display: flex;
        align-items: center;
        height: 40px;
        gap: 10px;

        img {
          width: 28px;
          margin-left: 14px;
        }

        span {
          font-size: 16px;
          font-weight: 400;
          color: #98abd0;
          height: 28px;
          display: flex;
          align-items: center;
          // margin-bottom: -3px;
        }
      }

      .r_box {}
    }
  }
}

@media screen and (max-width: 768px) {
  .sidebar {
    width: 232px;
    height: calc(100vh - 44px);

    .sidebar_box {
      height: auto;

      .paddingBox {
        padding: 24px 16px;

        .imgBox {
          gap: 12px;

          div {
            width: 200px;
            height: 52.83px;
            font-size: 16px;
          }
        }

        .imgGridBox {
          row-gap: 12px;
          column-gap: 12px;

          div {
            font-size: 12px;
            font-weight: bold;
          }
        }

        .promoções {
          font-size: 14px;
          font-weight: 600;
        }

        .allBounsBtn {
          height: 44px;
          margin: 12px 0 25px 0;

          p {
            font-size: 14px;
          }
        }

        .sidebar_box_top {
          width: 100%;
        }

        .download {
          margin-top: 12px;
        }
      }
    }

    .tab_list {
      .tab_list_ul2 {
        padding-left: 18px !important;
      }
    }

    .list {
      ul {
        padding-left: 14px;

        li {
          span {
            font-size: 15px;
            // color: var(--theme-font-color-fff);
            vertical-align: middle;
          }
        }
      }
    }
  }
}
</style>
