<template>
  <div class="header">
    <div class="box">
      <div class="head_l">
        <!-- <svg-icon class="hidden-xs-only" @click="menuClick()" style="width: 50px; height: 40px; cursor: pointer"
          name="nav" color="#000" /> -->

        <!-- <img src="@assets/images/public/menu_icon.png"  class="menu_icon" alt=""> -->
        <div :class="{ menu_btn_box: true, chake_icon: !store.state.status.sidebarIsShow }" @click="menuClick()">
          <svg-icon name="menu_btn" class="menu_icon"></svg-icon>

        </div>

        <!--  <span style="cursor: pointer" @click="$router.push('/')" >
          BIGWIN<span class="sl_font logo">777</span>
        </span> -->
        <img v-if="store.state.status.isPc" name="logo" class="logo" @click="$router.push('/')"
          :src="store.state.conf.all_conf.platform['platform_title_icon_url']" />
        <img class="logo" v-else :src="store.state.conf.all_conf.platform['platform_min_icon_url']" alt=""
          @click="$router.push('/')">
        <vipPop v-if="store.state.user.token != ''"></vipPop>
        <!-- <footballBtn></footballBtn> -->
      </div>
      <div class="head_r" v-if="!store.state.user.token">
        <div class=" entrar_btn" @click="showLoginBox(0)">{{ t('account.LOGIN') }}</div>
        <div class="Registrar_btn" @click="showLoginBox(1)">{{ t('account.REGISTER') }}</div>
      </div>
      <div class="isSign_box" v-else>
        <div class="pc">
          <div class="pc_none">
            <div class="wallet">
              <div class="country">
                <img src="@assets/images/public/brazil.png" alt="" />
              </div>
              <div class="money">
                <!-- <div class="money_state" v-if="!store.state.status.userInfoLoad"> -->
                <div class="money_state">
                  <span v-if="!store.state.status.playIngState">{{
                    moneyFormat(store.state.user.money, false)
                  }}</span>
                  <span v-else>{{ t('base.Playing') }}...</span>
                </div>
                <!-- <div class="load_money" v-else>
                  <span>....</span>
                </div> -->
              </div>
            </div>
            <div class="deposit  hidden-xs-only" @click="store.state.status.depositShow = true"
              v-if="!store.state.status.playIngState">

              <img src="@assets/images/layout/Depósito_icon.png" alt="" />
              <span v-if="store.state.status.isPc">{{ t('account.Depósito') }}</span>
              <img src="@/assets/images/public/Label.png" alt="" class="moneyLable">
            </div>
          </div>
          <div class="user" @click="showInfo(0)" v-if="store.state.status.isPc">
            <div class="user_box">
              <img class="avatar" :src="getImageUrl(
                `avatar/headsculpture_img_${store.state.user.header_img}.png`
              )
                " alt="" />
              <img class="arrow" src="@assets/images/header/arrow.png" alt="" v-if="store.state.status.isPc" />
            </div>
          </div>

          <div class="notice" @click="showDeposito" v-if="store.state.status.isPc">
            <img src="@assets/images/header/nav_horn.png" alt="" />
          </div>
        </div>
      </div>

      <header-user :class="{ headerUserCom: true, headerUserCom_show: userInfoFlag }" :data="userInfoFlag" />
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";
import headerUser from "./headerUser.vue";
import { getImageUrl, getUserInfo, moneyFormat, getUserInfoNoLoad } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
import selectImg from "./selectImg.vue";
import vipPop from "./vipPop.vue";
import footballBtn from "./footballBtn.vue";

export default defineComponent({
  name: "header_com",
  components: { headerUser, selectImg, vipPop, footballBtn },
  setup() {
    const store = useStore();
    const { proxy } = getCurrentInstance() as any;
    const { t } = useI18n();
    const state = reactive({
      isGamePage: false,
      userInfoFlag: false, // 用户信息显示
      rewardValue: '',
      rewardList: [],

    });
    const menuClick = () => {
      // store.dispatch(
      //   "status/setSidebarIsShow",
      //   !store.state.status.sidebarIsShow
      // );
      store.state.status.sidebarIsShow = !store.state.status.sidebarIsShow
    };

    const showLoginBox = (val: number) => {
      store.dispatch('status/setLoginShow', true)
      proxy.$mitt.emit("showLoginBox", val);
    };
    // type 0|1 val: 显示隐|藏
    const showInfo = (type: number, val?: boolean | string) => {

      if (type == 0) {
        state.userInfoFlag = !state.userInfoFlag;
      } else {
        if (val) state.userInfoFlag = true;
        else state.userInfoFlag = false;
      }

      if (state.userInfoFlag) {
        getUserInfoNoLoad();
      }
    };
    proxy.$mitt.on("showInfo", (obj: object) => {
      showInfo(obj["type"], obj["val"]);
    });

    function showDeposito() {
      store.commit("status/setShowDeposito", !store.state.status.showDeposito);
    }
    const rLoad = () => {
      window.location.reload()
    }
    return {
      ...toRefs(state),
      t,
      store,
      getImageUrl,
      menuClick,
      showLoginBox,
      showInfo,
      showDeposito,
      selectImg,
      moneyFormat,
      rLoad
    };
  },
});
</script>
<style  lang="scss" scoped>
.header {
  user-select: none;

  .box {
    position: relative;
    height: 80px;
    background: var(--theme-navigationbar-background);
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 30px;

    .head_l {
      display: flex;
      align-items: center;
      gap: 16px;

      .logo {
        cursor: pointer;
        width: auto;
        // height: 55.4px;
      }

      .menu_btn_box {
        // transition: all 0.3s ease;
      }

      .menu_icon {
        width: 32px;
        height: 32px;
        // margin-left: 14px;
        color: #585E77;
        cursor: pointer;

      }

      .chake_icon {
        transform: rotate(-180deg);

      }

      .menu_icon:hover {
        color: #fff;
        // margin-left: 14px;
      }

      span {
        color: #fff;
        font-size: 30px;
        font-weight: 750;

        .logo {
          color: var(--auxiliary-font-color-6);
          font-size: 70px;
        }
      }
    }

    .head_r {
      display: flex;
      align-items: center;
      gap: 16px;

      .entrar_btn {
        border: 1px solid rgba(65, 129, 238, 1);
        color: rgba(65, 129, 238, 1);
      }

      .entrar_btn:active {
        background: rgba(65, 129, 238, 0.50);
      }

      .entrar_btn:hover {
        background: rgba(65, 129, 238, 0.50);
      }

      .Registrar_btn {
        background: rgba(65, 129, 238, 1);

      }

      .Registrar_btn:active {
        background: rgba(109, 163, 255, 1);
      }

      .Registrar_btn:hover {
        background: rgba(109, 163, 255, 1);
      }

      div {
        // padding: 8px 15px;
        width: 140px;
        display: flex;
        justify-content: center;
        align-items: center;
        // padding: 7px 0 9px 0;
        height: 40px;
        font-weight: 500;
        border-radius: 5px;
        font-size: 20px;
        border-radius: 8px;
        cursor: pointer;
        color: #fff;
      }

      .login {
        background-color: var(--theme-button-background);
        color: var(--theme-font-color-fff);
      }

      .register {
        background-color: var(--auxiliary-background-4);
        // box-shadow: 0px 0px 3px 3px #d9ca16;
      }
    }

    .logo {
      color: var(--auxiliary-font-color-6);
      height: auto;
      width: 265px;
      height: 50px;
      cursor: pointer;
    }

    .isSign_box {

      .pc {
        display: flex;
        gap: 14px;
      }

      .phone {
        display: flex;
        // display: 10px;
        gap: 10px;
        // align-items: center;
      }

      .pc_none {
        display: flex;
        gap: 14px;
      }

      .pc_gamePage {
        display: flex;

        .wallet {
          min-width: auto;
        }
      }

      .phone {
        display: none;
      }

      .wallet {
        display: flex;
        justify-content: space-between;
        border-radius: 10px;
        align-items: center;
        width: 200px;
        // margin-right: 10px;
        padding: 0 14px 0 18px;
        background-color: #2D3144;
        box-sizing: border-box;

        .money {
          span {
            font-size: 14px;
            font-weight: 600;
            color: var(--theme-font-color-fff);
          }
        }

        .country {
          display: flex;
          align-items: center;

          span {
            font-size: 20px;
            font-weight: 600;
            color: var(--theme-font-color-fff);
          }

          img {
            // margin-right: 10px;
            width: 28px;
          }
        }

        .money {
          display: flex;
          align-items: center;

          img {
            cursor: pointer;
            margin-left: 10px;
            width: 30px;
            height: 30px;
          }
        }
      }

      .deposit {
        cursor: pointer;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        // padding: 10px 20px;
        width: 154px;
        height: 40px;
        border-radius: 10px;
        background: #4181EE;

        img {
          width: 28px;
          height: 27px;
        }

        span {
          margin-left: 6px;
          font-size: 20px;
          font-weight: 500;
          color: #fff;
        }

        .moneyLable {
          width: 45px;
          height: 45px;
          position: absolute;
          top: -4px;
          right: -20px;
          animation: zy 3.5s .15s linear infinite;
          transform-origin:50% 0;
        }
      }

      .user {
        .user_box {
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          width: 74px;
          height: 40px;
          background: var(--theme-button-background);
          border-radius: 18px;

          .avatar {
            margin-right: 11px;
            width: 32px;
          }

          .arrow {
            width: 11px;
          }
        }
      }

      .notice {
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        background: var(--theme-button-background);
        border-radius: 50%;
        width: 40px;
        height: 40px;

        img {
          width: 18px;
          height: 23px;
        }
      }
    }
  }

  .headerUserCom {
    position: absolute;
    top: 80px;
    right: 30px;
    z-index: 8;
    transition: 0.2s all ease;
    // width: 0;
    width: 320px;
    height: 0;
    overflow: hidden;

    &.headerUserCom_show {
      // width: 330px;
      height: 744px;
    }
  }

  :deep(.el-input__wrapper) {
    box-shadow: none;
    background-color: rgba(45, 49, 68, 0.60);
    border-radius: 6px;
    padding: 1px 10px;

    .el-input__inner {
      font-size: 12px;
    }
  }
}

@media screen and (max-width: 768px) {
  .header {
    .box {
      padding: 0 12px;
      padding-left: 10px;
      height: 44px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;

      .menu_icon {
        width: 17.08px !important;
        height: 13px !important;
        // margin-right: 8px;
      }

      .head_l {
        gap: 9px !important;

        .logo {
          width: 28px;
          height: 35px;
          margin-right: 5px;
        }

        span {
          font-size: 18px;
        }
      }

      .head_r {
        gap: 8px;

        div {
          font-size: 12px;
          width: 82px;
          height: 26px;
          border-radius: 6px;
        }
      }

      .isSign_box {
        .pc {
          justify-content: flex-end;
        }

        .wallet {

          width: 120px !important;
          // width: 100% !important;
          // min-width: 100px !important;
          height: 30px;
          margin-right: 0px !important;
          padding: 0 12px 0 7px !important;
          background-color: #10121A;
          border-radius: 6px;


        }

        .country {
          display: flex;
          align-items: center;

          span {
            font-size: 12px !important;
            font-weight: 600;
            color: var(--theme-font-color-fff);
          }

          img {
            margin-right: 10px;
            width: 16px !important;
          }
        }

        .money_state {
          span {
            font-size: 10px !important;
          }
        }
      }

    }



    .deposit {
      cursor: pointer;
      display: flex;
      align-items: center;
      padding: 8px 10px !important;
      border-radius: 10px;
    }

    .headerUserCom {
      right: 0;
      height: auto !important;
      width: 0;
      top: 44px;

      &.headerUserCom_show {
        width: 268px;
      }
    }
  }

  .user_box {
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    width: auto !important;
    height: auto !important;
    background: rgba($color: #000000, $alpha: 0) !important;
    border-radius: 18px;
    padding: 4px;
    border: 3px solid #2C3545;
    border-radius: 100px !important;

    .avatar {
      margin-right: 0 !important;
      width: 28px !important;
    }
  }
}

@-webkit-keyframes zy {
  10% {
    transform: rotate(20deg);
  }

  20% {
    transform: rotate(-20deg);
  }

  30% {
    transform: rotate(20deg);
  }

  40% {
    transform: rotate(-20deg);
  }

  50%,
  100% {
    transform: rotate(0deg);
  }
}

</style>
