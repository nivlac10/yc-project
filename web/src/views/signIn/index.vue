<template>
  <div class="signIn">
    <div class="signIn_content">
      <back :backNameShow="false" :title="t('signIn.BÔNUSCHECKIN')" />
      <div class="h_column">
        <div class="box">
          <div class="money">
            <p>{{ t('base.currencySymbol') }} {{ todayMoney }}</p>
            <p>{{ t('signIn.BônusDeHoje') }}</p>
          </div>
        </div>
        <div class="box">
          <div class="money">
            <p>{{ signDay }}</p>
            <p>{{ t('signIn.ContagemDeCheckinConsecutive') }}</p>
          </div>
        </div>
        <div class="box">
          <div class="money">
            <p>{{ t('base.currencySymbol') }} {{ store.state.user.sign_bonus }}</p>
            <p>{{ t('signIn.BônusAcumulado') }}</p>
          </div>
        </div>
      </div>
      <div class="list">
        <ul>
          <li :class="{ li_red: item.state == 1, li_grey: item.state == 2, li_yellow: index == 29 }"
            v-for="( item, index ) in  (signList as any) " :key="index">
            <div class="t_box">{{ item.day }} {{ t('signIn.Dias') }}</div>
            <div :class="{ b_box: true, b_box_p: (index + 1) % 7 == 0 && index > 1 && index < 22, b_box_y: index == 29 }">
              <div class="img_box">
                <img class="gold_img" src="@assets/images/signIn/gold.png" alt="">
                <img v-show="item.state == 2" class="successfully" src="@assets/images/signIn/Sign_in_successfully.png"
                  alt="">
              </div>
              <div>{{ t('base.currencySymbol') }} {{ item.money }}</div>
            </div>
          </li>
        </ul>
      </div>
      <div class="click_btn" @click="checkIn">
        <span :class="{ sl_box_shadow: true, mask: claimStatus == 2 }">{{ t('btnName.Checkin') }}</span>
      </div>
      <div class="rules">
        <div class="title">{{ t('signIn.Regras') }}</div>
        <p>{{ t('signIn.p1') }}</p>
        <p>{{ t('signIn.p2') }}</p>
        <p>{{ t('signIn.p3') }}</p>
        <p>{{ t('signIn.p4') }}</p>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { UserService } from "@/api/user";
import { getImageUrl, getUserInfo, debounce, moneyFormat } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
import back from "@com/back/index.vue"
import promptPopup from "@/components/promptPopup/index";

export default defineComponent({
  name: "signIn",
  components: { back },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      signList: [],
      claimStatus: 0, // 0 充值, 1 可领取, 2 已领取
      signInNum: 0,
      signDay: 0,
      todayMoney: 0,
      flag: false, // 领取签到状态
      amount: 0, // 领取金额
    });

    for (let i = 0; i < 30; i++) {
      state.signList.push({ day: i + 1, money: '-', state: 0 } as never)
    }

    // 获取签到列表
    const getSignInList = () => {
      UserService.get_sign_list().then((res) => {
        state.signList = res.data.data;
        state.signDay = res.data.sign_day
        state.todayMoney = res.data.today_money
        state.claimStatus = res.data.state
      });
    };
    getSignInList(); // 获取签到列表

    watch(() => store.state.user.token, () => {
      getSignInList(); // 获取签到列表
    }, { deep: true })

    // 领取
    const checkIn = () => {
      if (!store.state.user.token) {
        store.dispatch('status/setLoginShow', true)
      }
      if (state.claimStatus == 0) promptPopup('depositPopup', { tips: t('promptPopup.tips_Porfavor', { data1: moneyFormat(store.state.conf.all_conf.pay_conf['min_recharge_money']), data2: moneyFormat(store.state.conf.all_conf.pay_conf['min_recharge_money']) }), btnName: t('btnName.Depósito') })
      else if (state.claimStatus == 1) {
        const fun = () => {
          UserService.receive_sign_bonus().then((res) => {
            if (res.data.code == 1) {
              state.amount = res.data.money
              promptPopup('rewardPopup', { title: t('promptPopup.title_CheckinSucesso'), amount: res.data.money, tips: t('promptPopup.tips_Obônusjá'), btnName: t('btnName.Confirmar') })
              getSignInList() // 获取签到列表
            }
          });
        }
        debounce(fun)
      }
    };
    return { ...toRefs(state), t, store, checkIn };
  },
});
</script>
<style  lang="scss" scoped>
.signIn {
  .signIn_content {
    .h_column {
      display: flex;
      justify-content: space-around;
      padding: 35px 0;
      background: #202431;
      border-radius: 24px 24px 0px 0px;

      .box {
        text-align: center;

        p:nth-child(1) {
          color: var(--theme-font-color-fff);
          margin-bottom: 10px;
          font-size: 28px;
          font-weight: bold;
        }

        p:nth-child(2) {
          font-size: 18px;
          font-weight: 500;
          color: #B2B6C5;
        }
      }
    }

    .list {
      ul {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        column-gap: 17px;
        row-gap: 20px;
        padding: 32px;
        box-sizing: border-box;
        background: #2F3445;
        border-radius: 0px 0px 24px 24px;

        li {
          background: #E5A1B3;
          border-radius: 12px;

          &.li_grey {
            background: #61667D;
          }

          &.li_red {
            background: #BE1442;
          }

          &.li_yellow {
            background: #FFD600;
          }

          .t_box {
            position: relative;
            padding: 15px 0;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            color: var(--theme-font-color-fff);
            box-shadow: 0px 4px 6px 0px rgba(0, 0, 0, 0.25);
          }

          .b_box {
            padding-bottom: 10px;
            margin: 0 8px 8px 8px;
            text-align: center;
            background: #FFFFFF;
            border-radius: 0 0 12px 12px;

            &.b_box_p {
              background: #FFE7E7;
            }

            &.b_box_y {
              background: #FFF9C9;
            }

            .img_box {
              position: relative;

              .gold_img {
                padding: 13px 0;
                width: 56px;
              }

              .successfully {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 69px;
              }
            }

            div {
              font-size: 22px;
              font-weight: 500;
              color: #2D3144;
            }
          }
        }
      }
    }

    .click_btn {
      margin: 32px 0;
      text-align: center;
      font-size: 24px;
      color: #1B1D29;

      span {
        position: relative;
        display: inline-block;
        padding: 13px 80px;
        border-radius: 12px;
        font-weight: bold;

        &.mask::after {
          content: '';
          position: absolute;
          top: 0;
          right: 0;
          bottom: 0;
          left: 0;
          background: rgba(0, 0, 0, 0.5);
          border-radius: 12px;
        }
      }
    }

    .rules {
      .title {
        margin-bottom: 8px;
        font-size: 18px;
        font-weight: bold;
        color: #DEA541;
      }

      p {
        font-size: 16px;
        font-weight: 500;
        color: #B2B6C5;
        line-height: 30px;
      }
    }
  }

  .dialog_content {
    padding: 42px 20px 50px 20px;
    box-sizing: border-box;
    background: rgba(32, 35, 48, 0.94);
    border-radius: 12px;
    text-align: center;


    .true_box,
    .false_box {
      .btn {
        cursor: pointer;
        padding: 10px 0;
        font-size: 18px;
        font-weight: 600;
        color: #FFFFFF;
        background: #59C591;
        border-radius: 37px;
      }
    }

    .true_box {
      .tips {
        margin-bottom: 33px;
        font-size: 24px;
        font-weight: 600;
        color: #FFFFFF;
      }

      .content_box {
        margin-bottom: 33px;
        padding: 41px 13px;
        background: #2F3445;
        border-radius: 12px;

        img {
          display: block;
          margin: 0 auto;
          width: 68px;
        }

        div {
          padding: 30px 0 27px 0;
          font-size: 24px;
          font-weight: 600;
          color: #F8BF2E;
        }

        p {
          font-size: 16px;
          font-weight: 600;
          color: #B2B6C5;
          line-height: 19px;
        }
      }
    }

    .false_box {
      .title {
        font-size: 20px;
        font-weight: 600;
        color: #FFFFFF;
      }

      .tips {
        padding: 22px 20px;
        font-size: 16px;
        font-weight: 600;
        color: #B2B6C5;
        line-height: 19px;
      }

      .btn {
        margin: 0 40px;
        background: #CB394F;
      }
    }
  }
}

@media (max-width: 768px) {
  .signIn {
    padding: 0 14px;

    .signIn_content {
      .h_column {
        padding: 23px 10px 23px 5px;
        border-radius: 12px 12px 0px 0px;

        .box {
          width: 100%;

          p:nth-child(1) {
            margin-bottom: 14px;
            font-size: 18px;
          }

          p:nth-child(2) {
            font-size: 12px;
          }
        }
      }

      .list {
        ul {
          column-gap: 6px;
          row-gap: 8px;
          padding: 10px;
          border-radius: 0px 0px 12px 12px;

          li {
            background: #E5A1B3;
            border-radius: 4px;

            .t_box {
              padding: 7px 0;
              font-size: 12px;
            }

            .b_box {
              padding-bottom: 6px;
              margin: 0 4px 4px 4px;
              text-align: center;
              background: #FFFFFF;
              border-radius: 0 0 4px 4px;

              .img_box {
                position: relative;

                .gold_img {
                  padding: 4px 0;
                  width: 22px;
                }

                .successfully {
                  width: 22px;
                }
              }

              div {
                font-size: 12px;
              }
            }
          }
        }
      }

      .click_btn {
        margin: 16px 0;
        font-size: 16px;

        span {
          padding: 10px 40px;
          border-radius: 8px;

          &.mask::after {
            border-radius: 8px;
          }
        }
      }

      .rules {
        padding: 0 10px;

        .title {
          font-size: 12px;
        }

        p {
          font-size: 12px;
          line-height: 18px;
        }
      }
    }

    .dialog_content {
      margin: 0 10px;
      padding: 40px 20px 34px 20px;

      .true_box,
      .false_box {
        .btn {
          cursor: pointer;
          padding: 12px 0;
          font-size: 16px;
          border-radius: 30px;
        }
      }

      .true_box {
        .tips {
          font-size: 16px;
        }

        .content_box {
          margin-bottom: 27px;
          padding: 33px 11px;

          img {
            width: 56px;
          }

          div {
            padding: 24px 0 22px 0;
            font-size: 20px;
          }

          p {
            font-size: 14px;
            line-height: 16px;
          }
        }
      }

      .false_box {
        .title {
          font-size: 16px;
        }

        .tips {
          padding: 22px 20px;
          font-size: 12px;
          line-height: 14px;
        }

        .btn {
          margin: 0 40px;
          background: #CB394F;
        }
      }
    }
  }
}
</style>
