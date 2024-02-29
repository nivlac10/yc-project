<template>
  <div class="headerUser">
    <div class="headerUser_mask" v-if="userInfoFlag" @click.stop="closeUserInfo">
      <div></div>
    </div>

    <div class="box">
      <div class="user_info">
        <img :src="getImageUrl(
          `avatar/headsculpture_img_${store.state.user.header_img}.png`
        )
          " alt="" />
        <div class="user_m">
          <div class="t_box">{{ store.state.user.nickname }}</div>
          <div class="b_box">
            <div>ID：{{ store.state.user.uid }}</div>
            <img src="@assets/images/public/copy.png" alt="" @click="copy(store.state.user.uid.toString())" />
          </div>
        </div>
      </div>
      <withdraw-column-amount-info v-if="userInfoFlag" />
      <!-- <div class="user_level">
        <div class="level_column">
          <img :src="getImageUrl(`vipBonus/level_${store.state.user.vip_lv}.png`)" alt="" />
          <span>{{ levelName(store.state.user.vip_lv) }}</span>
        </div>
        <div class="progress">
          <div class="txt">
            <div>{{ t('vipBonus.Recharge') }}</div>
          </div>
          <el-progress class="el-progress_box" :stroke-width="10" :percentage="levelPercent().rechargePercent"
            status="exception">
            <span>
              {{ store.state.user.total_money }}/{{
                levelPercent().rechargeNextLvVal
              }}
            </span>
          </el-progress>
          <div class="txt">
            <div>{{ t('vipBonus.BetAmount') }}</div>
          </div>
          <el-progress class="el-progress_box" :stroke-width="10" :percentage="levelPercent().betPercent"
            status="exception">
            <span>
              {{ store.state.user.total_bet }}/{{ levelPercent().betNextLvVal }}
            </span>
          </el-progress>
        </div>
      </div> -->
      <div class="list">
        <ul>
          <li v-for="(item, index) in list" :key="item.title + index" @click="closeUserInfo, urlJump(item)">
            <div>
              <img :src="item.img" alt="" />
              <span>{{ item.title }}</span>
            </div>
            <img class="arrow_img" src="@assets/images/public/h_user_arrow.png" alt="">
          </li>
        </ul>
      </div>
      <div class="logout">
        <div @click="logout">
          <img src="@assets/images/header/Logout_icon.png" alt="" />
          <span>{{ t('headerUser.Logout') }}</span>
        </div>
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
  watch,
  onMounted,
  computed,
  nextTick
} from "vue";
import { useStore } from "@/store/index";
import { useRouter } from "vue-router";
import {
  clickLivechat,
  copy,
  getImageUrl,
  levelName,
  levelPercent,
  logoutFun,
  toPercent,
} from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
import withdrawColumnAmountInfo from "@views/deposit/components/withdrawColumnAmountInfo.vue"

export default defineComponent({
  name: "headerUser",
  props: {
    data: {
      type: Boolean,
    },
  },
  components: { withdrawColumnAmountInfo },
  setup(props) {
    const store = useStore();
    const router = useRouter();
    const { t } = useI18n();
    const { proxy } = getCurrentInstance() as any;
    const state = reactive({
      userInfoFlag: props.data,
      percentage: 0,
      remain_code_amount: 0,
      list: [
        {
          img: getImageUrl("header/deposit_icon.png"),
          title: computed(() => t('account.Depósito')),
          url: "deposit",
        },
        {
          img: getImageUrl("header/notify.png"),
          title: computed(() => t('headerUser.Notificar')),
          url: "notify",
        },
        {
          img: getImageUrl("header/MyAccount_icon.png"),
          title: computed(() => t('account.Conta')),
          url: "/account",
        },
        {
          img: getImageUrl("header/Transactions_icon.png"),
          title: computed(() => t('account.Transações')),
          url: "/account?tabIdx=1",
        },
        {
          img: getImageUrl("header/Settings.png"),
          title: computed(() => t('account.Configurações')),
          url: "/account?tabIdx=2",
        },
        {
          img: getImageUrl("header/VIPaward_icon.png"),
          title: computed(() => t('headerUser.BônusVIP')),
          url: "/vipBonus",
        },
        {
          img: getImageUrl("header/Refegaward_icon.png"),
          title: computed(() => t('headerUser.BônusdeConvite')),
          url: "/refer",
        },
        {
          img: getImageUrl("header/LiveSupport_icon.png"),
          title: computed(() => t('headerUser.Suporteaovivo')),
          url: "livechat",
        },
      ],
    });
    const closeUserInfo = () => {
      proxy.$mitt.emit("showInfo", { type: 0, val: "" });
    };

    onMounted(() => {

    });

    watch(
      () => props.data,
      (val) => {
        state.userInfoFlag = val;
        if (val) {
          nextTick(() => {
            (document.querySelector(".headerUser_mask") as any).addEventListener(
              "touchmove",
              function (event) {
                event.preventDefault();
              }
            );
          })
        }
      },
      { deep: true, immediate: true }
    );

    // 跳转路由
    const urlJump = (item: object) => {
      closeUserInfo();
      if (item['url'] == 'deposit') store.state.status.depositShow = true
      else if (item["url"] == "notify") store.commit("status/setShowDeposito", !store.state.status.showDeposito);
      else if (item["url"] == "livechat") clickLivechat()
      else router.push(item["url"]);
    };

    // 退出登录
    const logout = () => {
      closeUserInfo();
      logoutFun();
    };

    return {
      ...toRefs(state),
      store,
      t,
      getImageUrl,
      copy,
      levelName,
      closeUserInfo,
      levelPercent,
      urlJump,
      logout,
    };
  },
});
</script>
<style  lang="scss" scoped>
.headerUser {
  position: relative;
  white-space: nowrap;

  .headerUser_mask {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: rgba($color: #000000, $alpha: 0);

    >div {
      display: none;
      position: absolute;
      top: 80px;
      right: 0;
      bottom: 0;
      left: 0;
      background: rgba($color: #000000, $alpha: 0.5);
    }
  }

  .box {
    position: relative;
    z-index: 1;
    padding: 24px 12px 22px 12px;
    box-shadow: -7px 4px 8px 0px rgba(7, 11, 26, 0.25);
    background: var(--theme-box-background);
    border-radius: 12px;
    box-sizing: border-box;
    max-height: calc(100vh - 80px);
    overflow-y: scroll;

    .user_info {
      display: flex;
      align-items: center;
      padding-left: 12px;
      margin-bottom: 24px;

      >img {
        margin-right: 24px;
        width: 70px;
      }

      .user_m {

        .t_box {
          margin-bottom: 13px;
          font-size: 14px;
          color: #FFFFFF;
        }

        .b_box {
          display: flex;
          align-items: center;

          div {
            margin-right: 10px;
            font-size: 14px;
            color: #B2B6C5;
          }

          img {
            cursor: pointer;
            width: 13px;
          }
        }
      }
    }

    :deep(.withdrawColumnAmountInfo) {
      margin-bottom: 8px;

      .withdraw_amount {

        .l_box {
          background: #2F3445;
        }
      }
    }

    // .user_level {
    //   margin: 10px 0;
    //   padding: 10px 14px 20px 14px;
    //   background: var(--auxiliary-background-14);
    //   border-radius: 8px;
    //   position: relative;

    //   .level_column {
    //     display: flex;
    //     align-items: flex-end;
    //     margin-bottom: 5px;

    //     img {
    //       margin-right: 7px;
    //       width: 32px;
    //     }

    //     span {
    //       font-size: 18px;
    //       font-weight: bold;
    //       color: var(--auxiliary-font-color-9);
    //     }
    //   }

    //   .progress {
    //     .txt {
    //       margin-bottom: 8px;
    //       font-size: 10px;
    //       font-weight: 500;
    //       color: var(--auxiliary-font-color-9);
    //     }

    //     .el-progress_box {
    //       margin-bottom: 8px;
    //     }
    //   }
    // }

    .list {
      margin-bottom: 15px;
      // padding: 10px 0;
      border-radius: 8px;

      ul {
        li {
          cursor: pointer;
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 5px 7px 5px 10px;
          border-radius: 6px;
          background: #2F3445;

          &:nth-child(1),
          &:nth-child(2) {
            margin-bottom: 8px;

            .arrow_img {
              display: none;
            }
          }

          &:nth-child(3) {
            border-radius: 8px 8px 0 0;
          }

          &:nth-child(4),
          &:nth-child(5),
          &:nth-child(6) {
            border-radius: 0;
          }

          &:nth-last-child(1) {
            border-radius: 0 0 6px 6px;
          }

          &:hover {
            span {
              color: #FFFFFF;
            }
          }

          div {
            display: flex;
            align-items: center;

            img {
              margin-right: 11px;
              width: 26px;
            }

            span {
              font-size: 14px;
              color: #98ABD0;
            }
          }

          .arrow_img {
            width: 18px;
          }
        }
      }
    }

    .logout {
      display: flex;

      div {
        cursor: pointer;

        &:hover {
          span {
            color: #FFFFFF;
          }
        }

        img {
          margin-right: 6px;
          width: 26px;
          vertical-align: middle;
        }

        span {
          font-size: 14px;
          color: #98ABD0;
        }
      }
    }
  }
}

@media screen and (max-width: 768px) {
  .headerUser {
    .headerUser_mask {
      >div {
        display: block;
        top: 44px;
        max-height: calc(100vh - 44px);
      }
    }

    .box {
      padding: 24px 12px 19px 12px;
      padding-bottom: 110px;
      border-radius: 0;
      height: calc(100vh - 44px - 70px);
      overflow-y: scroll;

      .user_info {
        padding-left: 15px;

        >img {
          margin-right: 10px;
          width: 56px;
        }

        .user_m {

          .t_box {
            margin-bottom: 13px;
            font-size: 14px;
            color: #FFFFFF;
          }

          .b_box {
            display: flex;
            align-items: center;

            div {
              margin-right: 10px;
              font-size: 14px;
              color: #B2B6C5;
            }

            img {
              cursor: pointer;
              width: 13px;
            }
          }
        }
      }

      .list {
        ul {
          li {
            div {
              img {
                width: 23px;
                margin-right: 11px;
              }

              span {
                font-size: 13px;
              }
            }
          }
        }
      }

      .logout {
        div {
          img {
            margin-right: 4px;
            width: 23px;
          }

          span {
            font-size: 13px;
          }
        }
      }
    }
  }
}
</style>
