<template>
  <div class="signIn">
    <el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
      :width="store.state.status.isPc ? '908px' : '100%'">
      <div class="signIn_content">
        <img class="close_img" src="@assets/images/public/Shut_down.png" alt="" @click="closeBtn" />
        <div class="figure_img"></div>
        <div class="title_img">
          <img src="@assets/images/signIn/title.png" alt="" />
        </div>
        <div class="list">
          <ul>
            <li v-for="(item, index) in signList as any" :key="index">
              <div class="box">
                <div class="day_title" v-if="item.weekday < 8">
                  {{ t("signIn.Day") }} {{ item.weekday }}
                </div>
                <div class="day_title" v-else>
                  {{ t("signIn.PerfectReward") }}
                </div>
                <div class="img">
                  <img :src="imgList[index]" alt="" />
                </div>
                <div class="money">
                  {{ t("base.currencySymbol") }} {{ item.money }}
                </div>
                <img class="flag_img" src="@assets/images/signIn/Sign_in_successfully.png" alt=""
                  v-show="item.state == 2" />
                <img class="flag_img" src="@assets/images/signIn/for_sign_in.png" alt="" v-show="item.state == 3" />
                <div class="none_mask" v-show="item.state == 2 || item.state == 3"></div>
              </div>
              <img v-show="item.state == 1" class="light_img" src="@assets/images/signIn/light.png" alt="" />
            </li>
          </ul>
        </div>
        <div class="b_box">
          <div>
            <ul>
              <li @click="jump">Ver apresentações de evento</li>
              <!-- <li>{{ t("signIn.p1") }}</li> -->
              <!-- <li>{{ t("signIn.p2") }}</li>
              <li>{{ t("signIn.p3") }}</li>
              <li>{{ t("signIn.p4") }}</li> -->
            </ul>
          </div>
          <div>
            <div
              :class="{ btn: true, sl_box_shadow: claimStatus == 0, sl_box_shadow_red: claimStatus == 1, sl_box_shadow_green: claimStatus == 2 || claimStatus == 3 }"
              @click="checkIn">
              <span v-show="claimStatus == 0">{{ t("login.LOGIN") }}</span>
              <span v-show="claimStatus == 1">{{ t("deposit.DEPOSIT") }}</span>
              <span v-show="claimStatus == 2 || claimStatus == 3">{{ t("signIn.CHECKIN") }}</span>
              <div class="none_mask" v-show="claimStatus == 3"></div>
            </div>
            <div class="num" v-show="claimStatus != 0">{{ t('signIn.Frequency') }} {{ signInNum }} / 7</div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { UserService } from "@/api/user";
import { getImageUrl, getUserInfo, debounce } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
import { ElNotification } from 'element-plus'
export default defineComponent({
  name: "signIn",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      dialogVisible: true,
      imgList: [
        getImageUrl("signIn/home_species1_icon.png"),
        getImageUrl("signIn/home_species1_icon.png"),
        getImageUrl("signIn/home_species1_icon.png"),
        getImageUrl("signIn/pile_of_gold_coins.png"),
        getImageUrl("signIn/pile_of_gold_coins.png"),
        getImageUrl("signIn/purse.png"),
        getImageUrl("signIn/purse.png"),
        getImageUrl("signIn/big_purse.png"),
      ],
      signList: [
        { money: '-', state: 0, weekday: 1 },
        { money: '-', state: 0, weekday: 2 },
        { money: '-', state: 0, weekday: 3 },
        { money: '-', state: 0, weekday: 4 },
        { money: '-', state: 0, weekday: 5 },
        { money: '-', state: 0, weekday: 6 },
        { money: '-', state: 0, weekday: 7 },
        { money: '-', state: 0, weekday: 8 },
      ],
      claimStatus: 0, // 0 未登录, 1 充值, 2 未领取, 3 已领取
      signInNum: 0,
    });

    const closeBtn = () => {
      store.dispatch('status/setSignInShow', false)
    }

    const jump = () => {
      router.push('/ActivitySubpage?i=2')
      closeBtn()
    }

    // 设置领取状态
    const setClaimStatus = () => {
      state.signInNum = 0
      // 签到次数
      for (let i = 0; i < state.signList.length - 1; i++) {
        const element: any = state.signList[i];
        if (element.state == 0 || element.state == 1) {
          if (state.signInNum >= 7) state.signInNum = 7
          else state.signInNum += 1
        }
      }

      // 设置状态
      if (!store.state.user.token) return state.claimStatus = 0

      let flag = 0
      for (let i = 0; i < state.signList.length; i++) {
        const element: any = state.signList[i];
        if (element.state == 1) {
          state.claimStatus = 2
          break
        }
        else if (element.state == 2) {
          state.claimStatus = 3
        } else if (element.state == 0) {
          flag += 1
        }
      }
      if (flag == 8) {
        state.claimStatus = 1
      }
    }

    // 获取签到列表
    const getSignInList = () => {
      UserService.get_sign_list().then((res) => {
        state.signList = res.data.data;
        setClaimStatus() // 设置领取状态
      });
    };
    getSignInList(); // 获取签到列表

    watch(() => store.state.user.token, () => {
      getSignInList(); // 获取签到列表
    }, { deep: true })

    // 领取
    const checkIn = () => {
      if (state.claimStatus == 0) store.dispatch('status/setLoginShow', true)
      else if (state.claimStatus == 1) store.state.status.depositShow = true
      else if (state.claimStatus == 2) {
        const fun = () => {
          UserService.receive_sign_bonus().then((res) => {
            if (res.data.code == 1) {
              getSignInList(); // 获取签到列表
              getUserInfo() // 获取用户数据
              ElNotification({
                title: computed(() => t("Success")).value,
                message: computed(() => t("SuccessfullySignedIn")).value,
                type: 'success',
                duration: 3000,
                position: 'bottom-left',
              })
            }
          });
        }
        debounce(fun)
      }
    };
    return { ...toRefs(state), t, store, closeBtn, checkIn, jump };
  },
});
</script>
<style  lang="scss" scoped>
.signIn {
  .signIn_content {
    position: relative;
    padding: 0 25px 55px 25px;
    min-height: 650px;
    box-sizing: border-box;
    background: url("@assets/images/signIn/background.png") no-repeat;
    background-size: 100% 100%;

    .close_img {
      position: absolute;
      top: 15px;
      right: 12px;
      width: 28px;
    }

    .figure_img {
      position: absolute;
      bottom: -60px;
      left: -200px;
      z-index: 3;
      width: 274px;
      height: 460px;
      background: url("@assets/images/signIn/figure.png") no-repeat;
      background-size: 100% 100%;
    }

    .title_img {
      padding: 35px 0;
      text-align: center;

      img {
        width: 578px;
      }
    }

    .list {
      position: relative;
      z-index: 10;
      margin-bottom: 30px;

      ul {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 17px;

        li {
          cursor: pointer;
          position: relative;
          width: calc(25% - 17px);
          border-radius: 12px;
          background: rgba(0, 0, 0, 0.3);
          text-align: center;

          .box {
            position: relative;
            z-index: 1;
            height: 100%;

            .day_title {
              position: relative;
              z-index: 1;
              padding: 6px 0;
              font-size: 22px;
              font-weight: bold;
              color: var(--theme-font-color-fff);
              background: rgba(0, 0, 0, 0.2);
              border-radius: 12px 12px 0px 0px;
            }

            .img {
              img {
                width: 120px;
              }
            }

            .money {
              position: relative;
              z-index: 1;
              margin-bottom: 10px;
              font-size: 22px;
              font-weight: bold;
              color: var(--auxiliary-font-color-19);
            }

            .flag_img {
              position: absolute;
              right: -10px;
              bottom: -10px;
              z-index: 1;
              width: 69px;
            }

            .none_mask {
              position: absolute;
              top: 0;
              right: 0;
              bottom: 0;
              left: 0;
              background: rgba(0, 0, 0, 0.6);
              z-index: 0;
              border-radius: 12px;
            }
          }

          .light_img {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            width: 100%;
            height: 100%;
          }
        }
      }
    }

    .b_box {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 30px;

      div:nth-child(1) {
        padding-left: 40px;
        font-size: 18px;
        font-weight: 500;
        color: var(--auxiliary-font-color-19);

        ul {
          li {
            cursor: pointer;
            // list-style-type: initial;
            text-decoration: underline;
            line-height: 22px;
          }
        }
      }

      div:nth-child(2) {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        .btn {
          position: relative;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
          padding: 17px 0;
          min-width: 226px;
          font-size: 28px;
          font-weight: bold;
          color: var(--auxiliary-font-color-10);
          white-space: nowrap;

          .none_mask {
            position: absolute;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 7px;
          }
        }

        .num {
          padding-top: 10px;
          font-size: 22px;
          font-weight: bold;
          color: var(--auxiliary-font-color-19);
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .signIn {
    .signIn_content {
      margin: 0 20px;
      padding: 0 25px 25px 25px;
      min-height: 541px;
      background: url("@assets/images/signIn/background_p.png") no-repeat;
      background-size: 100% 100%;

      .figure_img {
        display: none;
        // top: 129px;
        // left: -27px;
        // transform: scale(0.8);
        // background: url(/src/assets/images/signIn/figure_p.png) no-repeat;
      }

      .title_img {
        padding: 13px 0;

        img {
          width: 213px;
        }
      }

      .list {
        margin-bottom: 25px;

        ul {
          gap: 8px;
          justify-content: center;

          li {
            margin-bottom: 0;
            width: calc(33.3333% - 8px);

            &:nth-last-child(1) {
              width: calc(38% - 8px);
            }

            .box {
              .day_title {
                font-size: 12px;
              }

              .img {
                img {
                  width: 60px;
                }
              }

              .money {
                font-size: 12px;
              }

              .flag_img {
                width: 36px;
              }
            }
          }
        }
      }

      .b_box {
        display: flex;
        align-items: center;
        flex-direction: column;
        gap: 13px;

        div:nth-child(1) {
          padding-left: 0;
          font-size: 12px;
          line-height: 14px;
        }

        div:nth-child(2) {
          width: 100%;
          padding: 8px 0;
          font-size: 16px;

          .num {
            font-size: 14px;
          }
        }
      }
    }
  }
}
</style>
