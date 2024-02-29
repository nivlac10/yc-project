<template>
  <div>
    <div class="depositCom">
      <div class="list">
        <ul>
          <li :class="{ active: activeIdx == index }" v-for="(item, index) in money_list as any" :key="index"
            @click="(activeIdx = index), Selected(item)">
            <span>{{ t('base.currencySymbol') }} {{ item.money }}</span>
            <div class="gift" v-show="item.giveMoney > 0">
              +{{ item.giveMoney }}%
              <!-- <div class="gift" v-show="store.state.user['recharge_today_num'] < 2"> -->
              <!-- +10% -->
            </div>
            <img v-show="activeIdx == index" class="img_f" src="@assets/images/public/Shut_down_f.png" alt="">
          </li>
        </ul>
      </div>
      <!-- <div class="activity " v-if="store.state.user.first_pay_type == 1">
        <div :class="`top ${bonus_type ? '' : 'Participatedinevent'}`"
          :style="`background:url(${store.state.user.first_pay_type == 1 ? imgList[2] : store.state.user.first_pay_type == 0 ? imgList[0] : imgList[1]}) no-repeat`">
          <div class="topFont">
            <p>
              {{ store.state.user.first_pay_type == 1 ? t('deposit.SuperWelcomeBonus') : store.state.user.first_pay_type
                == 0 ? t('deposit.Youcanjoin') : t('deposit.DailyFirstDeposit') }}
            </p>

            <p>
              {{ store.state.user.first_pay_type == 1 ? t('deposit.SuperDeposit') : store.state.user.first_pay_type == 0 ?
                t('deposit.DailyFirstDeposit') : t('deposit.Deposittoget') }}
              <span v-show="store.state.user.first_pay_type == 0" style="color: #FFF500;">{{ t('deposit.YoucaBonus')
              }}</span>
            </p>
          </div>
          <p class="topP">
            {{ store.state.user.first_pay_type == 1 ? '+20%' : store.state.user.first_pay_type == 0 ? t('') : '+10%' }}
          </p>
        </div>
        <div class="bottom" v-show="store.state.user.first_pay_type !== 0">
          <el-checkbox v-model="bonus_type" :label="t('login.Nottoparticipate')" size="large" fill="#75ED3D" />
        </div>
      </div>
      <div class="amount_box">
        <div class="country">
          <img src="@assets/images/language/brazil.png" alt="" />
          <span>{{ t('base.currency') }}</span>
        </div>
        <span class="input_box_style">{{ moneyNum }}</span>
        <div class="gift_fontBox">
          <span class="gift_font" v-if="giveMoney > 0"> {{ t('deposit.Extra') }}+{{ t('base.currency') }} {{ giveMoney
          }}</span>
        </div>
      </div> -->
      <!-- <div :class="{ firstBonus: true, check_bonus: bonus_type }"
        v-if="store.state.user.first_pay_type == 1 || store.state.user.first_pay_type == 2">
        <p>
          {{ t('deposit.first_bouns') }}
        </p>
        <van-switch v-model="bonus_type" size="22px" active-color="#009C3B" inactive-color="#dcdee0" />
      </div> -->

      <van-checkbox v-model="bonus_type" checked-color="#50B06E" size="small"
        :disabled="store.state.user.first_pay_type == 0">
        <div>
          <span>{{ t('deposit.ReceberBônusdedepósito') }} (
            {{ store.state.user.first_pay_type == 0 ? 1 : 0 }}/1)
          </span>
          <!-- <el-popover placement="top" trigger="hover" popper-class="el_popover_style" :teleported="false" width='334px'>
            <template #reference>
              <img src="@assets/images/public/query.png" alt="" @click.stop="">
            </template>
            <div class="popover_content">
              <div class="popover_content_title">Primeiro depósito diário + 10% de bônus</div>
              <div class="popover_content_txt">
                ．Bônus de Depósito = Valor do Depósito x 10%<br />
                ．Os jogadores recebem um bônus de 10% em seu primeiro depósito todos os dias!
              </div>
            </div>
          </el-popover> -->
        </div>
      </van-checkbox>

      <div class="pix_title">{{ t('deposit.MétododeDepósito') }}</div>
      <div class="pix_input_box">
        <div>PIX</div>
        <img src="@assets/images/deposit/pix.png" alt="">
      </div>

      <div class="submit_btn" @click="toPay()">{{ t('account.Depósito') }}</div>

      <div class="see_d" @click="jumpDepositInstructions">{{ t('btnName.Instruções') }} ></div>
      <!-- <p style="text-align: right;cursor: pointer;color: #C3CFD9;" @click="jump">Regras de Depósito ></p> -->
      <!-- <div class="rules">
        <div class="title">{{ t('deposit.DepositNotes') }}</div>
        <p>{{ t('deposit.p1') }}</p>
        <p>{{ t('deposit.p2') }}</p>
        <p>{{ t('deposit.p_3') }}</p>
      </div> -->
    </div>
    <el-dialog v-model="showPayPop" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
      :width="store.state.status.isPc ? '512px' : '100%'">
      <payPop v-if="showPayPop" :Pay="payData" :money="moneyNum" :pay_type="pay_type" :pay_url="pay_url"></payPop>
    </el-dialog>

  </div>
</template>
<script lang="ts">
import {
  reactive,
  toRefs,
  getCurrentInstance,
  defineComponent,
  computed,
  watch
} from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { DepositAndWithdraw } from "@/api/DepositAndWithdraw";
import payPop from "./payPop.vue";
import { debounce } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
import { add_shopping_cart } from "@/utils/Adjust"
import { getImageUrl } from "@/utils/baseFun";
export default defineComponent({
  name: "depositCom",
  components: { payPop },
  setup() {
    const store = useStore();
    const router = useRouter();
    const { proxy } = getCurrentInstance() as any;
    const { t } = useI18n();
    const state = reactive({
      list: [],
      activeIdx: 0,
      amount: 0,
      isPayPop: false,
      showPayPop: computed(() => store.state.status.showPayPop),
      payData: {},
      recharge_activity_res: [],
      money_list: [],
      moneyNum: 0,
      giveMoney: 0,
      first_pay_rate: 0,
      day_first_pay_rate: 0,
      bonus_type: true,
      pay_type: null,
      pay_url: null,
      imgList: [getImageUrl('deposit/backdrop.png'), getImageUrl('deposit/backdrop2.png'), getImageUrl('deposit/backdrop3.png'),],
      checked1: true,
    });

    async function toPay() {
      const fun = () => {
        let bonus_type = state.bonus_type ? 1 : 0
        add_shopping_cart();
        DepositAndWithdraw.pay({ money: state.moneyNum, bonus_type: bonus_type }).then((res) => {
          if (res.data.code == 1) {
            state.payData = res.data;
            store.state.status.showPayPop = true;
            state.pay_type = res.data.pay_type
            state.pay_url = res.data.url
          }
        });
      };
      debounce(fun);
    }
    const Selected = (item: any) => {
      state.moneyNum = item.money;
      state.giveMoney = item.giveMoney;
      state.amount = item.money;
    };
    // 初始化充值数据
    const getRechargeActivity = async () => {
      // 初始化充值列表

      const pay_money_list =
        store.state.conf.all_conf.pay_conf["pay_money_list"];
      for (let i = 0; i < pay_money_list.length; i++) {
        let moenyData = {
          money: pay_money_list[i],
          // giveMoney: 0
        };
        state.money_list.push(moenyData as never);
      }

      await DepositAndWithdraw.get_recharge_activity({}).then((res) => {
        if (res.data.code) {
          state.recharge_activity_res = res.data as any;
          state.first_pay_rate = state.recharge_activity_res["first_charge_give_rate"];
          state.day_first_pay_rate = state.recharge_activity_res["day_charge_give_rate"];
        }
        for (let i = 0; i < state.money_list.length; i++) {
          state.money_list[i]["giveMoney"] = giveMoneyFunc(
            state.money_list[i]["money"]
          ) as never;
        }
      });

      Selected(state.money_list[0]);
    };
    watch(() => state.bonus_type, () => {
      if (state.bonus_type) {
        for (let i = 0; i < state.money_list.length; i++) {
          state.money_list[i]["giveMoney"] = giveMoneyFunc(
            state.money_list[i]["money"]
          ) as never;
        }
      } else {
        for (let i = 0; i < state.money_list.length; i++) {
          state.money_list[i]["giveMoney"] = 0 as never
        }
      }
      state.giveMoney = state.money_list[state.activeIdx]["giveMoney"]
    })
    getRechargeActivity();
    // 判断当前金额是否满足 赠送条件 满足则返回赠送金额
    const giveMoneyFunc = (money: any) => {
      // 判断是否是第一次充值
      let active_money = 0;
      let recharge_activity = state.recharge_activity_res["data"];
      if (recharge_activity.length > 0) {
        //@ts-ignore
        let nowTime: any = parseInt(Date.now() / 1000);
        for (let i = 0; i < recharge_activity.length; i++) {

          // 判断当前时间戳是否满足活动要求
          if (
            nowTime > recharge_activity[i].start_time &&
            nowTime < recharge_activity[i].over_time
          ) {
            // 新用户
            if (store.state.user.first_pay_type == 1) {
              if (recharge_activity[i].recharge_activity_type == 2 || recharge_activity[i].recharge_activity_type == 3) {
                //  判断是否为充值范围活动
                if (recharge_activity[i].scope.length > 0) {
                  for (let d = 0; d < recharge_activity[i].scope.length; d++) {
                    // 范围赋值
                    let scope = recharge_activity[i].scope[d];
                    if (
                      money >= scope.min_recharge &&
                      money <= scope.max_recharge
                    ) {
                      // active_money += (money * scope.send_rate) / 100;
                      active_money = scope.send_rate
                    }
                  }
                }
                //  判断是否为充值阶梯活动
                if (recharge_activity[i].step.length > 0) {
                  for (let d = 0; d < recharge_activity[i].step.length; d++) {
                    // 阶梯赋值
                    let step = recharge_activity[i].step[d];
                    if (money == step.recharge_amount) {
                      // active_money += (money * step.send_rate) / 100;
                      active_money = step.send_rate
                    }
                  }
                }
              }
            }
            // 老用户日冲
            if (store.state.user.first_pay_type == 2) {
              if (recharge_activity[i].recharge_activity_type == 0 || recharge_activity[i].recharge_activity_type == 1) {
                //  判断是否为充值范围活动
                if (recharge_activity[i].scope.length > 0) {
                  for (let d = 0; d < recharge_activity[i].scope.length; d++) {
                    // 范围赋值
                    let scope = recharge_activity[i].scope[d];
                    if (
                      money >= scope.min_recharge &&
                      money <= scope.max_recharge
                    ) {
                      // active_money += (money * scope.send_rate) / 100;
                      active_money = scope.send_rate
                    }
                  }
                }
                //  判断是否为充值阶梯活动
                if (recharge_activity[i].step.length > 0) {
                  for (let d = 0; d < recharge_activity[i].step.length; d++) {
                    // 阶梯赋值
                    let step = recharge_activity[i].step[d];
                    if (money == step.recharge_amount) {
                      // active_money += (money * step.send_rate) / 100;
                      active_money = step.send_rate
                    }
                  }
                }
              }
            }
          }
        }
      }
      return active_money;
    };

    const moneyChange = () => {
      state.giveMoney = giveMoneyFunc(state.moneyNum);
    };

    const jump = () => {
      proxy.$mitt.emit("depositComShow", 3);
    }

    const jumpDepositInstructions = () => {
      proxy.$mitt.emit("depositComShow", 4);
    }
    return { ...toRefs(state), t, toPay, store, Selected, moneyChange, jump, jumpDepositInstructions };
  },
});
</script>
<style  lang="scss" scoped>
:deep(.el-checkbox) {
  height: auto !important;
}

.depositCom {
  .payPop {
    height: 100%;
  }

  .list {
    ul {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      column-gap: 10px;
      row-gap: 8px;

      li {
        cursor: pointer;
        position: relative;
        height: 64px;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #2F3445;
        border-radius: 8px;

        .img_f {
          position: absolute;
          right: 7px;
          bottom: 6px;
          display: none;
          width: 15px;
        }

        &.active {
          background: #4181EE;

          >span {
            color: var(--theme-font-color-fff);
          }

          .gift {
            background: #6FCD7E;
          }

          .img_f {
            display: block;
          }
        }

        >span {
          font-size: 20px;
          font-weight: 600;
          color: #B2B6C5;
        }

        .gift {
          position: absolute;
          top: 0;
          right: 0;
          width: 48px;
          text-align: center;
          line-height: 20px;
          font-size: 12px;
          border-radius: 0px 8px 0px 8px;
          color: #FFFFFF;
          background: #585E77;
        }
      }
    }
  }

  .amount_box {

    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 10px 0 20px 0;
    padding: 10px 10px;
    border: 2px solid #53535C;
    border-radius: 10px;

    .country {

      display: flex;
      align-items: center;

      img {
        margin-right: 10px;
        width: 37px;
      }

      span {
        font-size: 20px;
        font-weight: 500;
        color: var(--theme-font-color-fff);
      }
    }

    .input_box_style {
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 20px;
      color: #fff;

    }

    .gift_fontBox {
      min-width: 100px;
      min-height: 10px;
    }

    .gift_font {

      font-size: 15px;
      color: var(--auxiliary-font-color-7);
    }
  }

  :deep(.van-checkbox) {
    margin: 20px 0;

    .van-checkbox__icon {
      font-size: 15px;
      border: 1px solid #FFFFFF;
      border-radius: 50%;

      .van-icon {
        border: none;
      }
    }

    .van-checkbox__label {
      font-size: 14px;
      color: #FFFFFF;

      >div {
        display: flex;
        align-items: center;

        img {
          margin-left: 10px;
          width: 15px;
        }
      }
    }
  }

  .popover_content {
    .popover_content_title {
      margin-bottom: 8px;
      font-size: 14px;
      font-weight: bold;
      color: #F3B343;
    }

    .popover_content_txt {
      // margin-bottom: 14px;
      font-size: 12px;
      color: #B2B6C5;
      line-height: 16px;
      white-space: pre-wrap;
      // word-break: break-word;
      // word-wrap: break-word;
    }
  }

  .pix_title {
    font-size: 14px;
    font-weight: 600;
    color: #B2B6C5;
  }

  .pix_input_box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 16px 0 20px 0;
    padding: 0 10px 0 16px;
    height: 40px;
    border-radius: 6px;
    border: 1px solid #4C4F5D;

    div {
      font-size: 14px;
      color: #FFFFFF;
    }

    img {
      width: 58px;
    }
  }

  .submit_btn {
    cursor: pointer;
    margin-bottom: 20px;
    line-height: 40px;
    text-align: center;
    background: #4181EE;
    border-radius: 34px;
    font-size: 16px;
    font-weight: 600;
    color: #FFFFFF;
  }

  .see_d {
    cursor: pointer;
    font-size: 14px;
    color: #4181EE;
    text-align: right;
  }

  .rules {
    .title {
      margin-bottom: 10px;
      font-size: 20px;
      font-weight: bold;
      color: var(--auxiliary-font-color-9);
    }

    p {
      margin-bottom: 5px;
      line-height: 21px;
      font-weight: 500;
      font-size: 14px;
      color: var(--auxiliary-font-color-9);
    }
  }
}

.activity {
  width: 100%;
  height: 100%;
  position: relative;
  cursor: pointer;
  height: 130px;
  margin: 12px 0 18px;

  .top {
    position: absolute;
    top: 0;
    z-index: 2;
    width: 100%;
    height: 82px;
    border-radius: 8px;
    background-size: 100% 100% !important;
    display: flex;
    justify-content: center;
    align-items: center;

    .topFont {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      margin-right: 10px;
      padding-left: 25%;

      p {
        text-align: left;
        color: #fff;
      }
    }

    .topFont>p:nth-child(1) {
      font-size: 22px;
      font-weight: bold;
      margin-bottom: 6px;
    }

    .topFont>p:nth-child(2) {
      font-size: 15px;
      font-weight: bold;

      span {
        font-weight: bold;
      }
    }
  }

  .topP {
    font-size: 28px;
    color: #FFF500;
    font-weight: bold;
  }

  .bottom {
    position: absolute;
    bottom: 0;
    z-index: 1;
    width: calc(100% - 14px);
    height: 52px;
    border: 2px solid #53535C;
    border-radius: 8px;
    display: flex;
    align-items: center;
    padding-left: 10px;

    :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
      background-color: #75ED3D;
      border-color: #75ED3D;
    }

    :deep(.el-checkbox.el-checkbox--large .el-checkbox__inner) {
      width: 20px;
      height: 20px;
    }

    :deep(.el-checkbox__inner::after) {
      width: 6px;
      height: 12px;
      left: 5px;
      top: 1px;
    }

    :deep(.el-checkbox__input.is-checked+.el-checkbox__label) {
      color: #75ED3D;
      font-size: 14px;
      font-weight: bold;
    }

    :deep(.el-checkbox__label) {
      color: #C3CFD9;
      font-size: 14px;
      font-weight: bold;
    }

    :deep(.el-checkbox__inner) {
      background: transparent;
      border: #C3CFD9 2px solid;
      border-radius: 5px;
    }
  }

}

.Participatedinevent::after {
  content: '';
  position: absolute;
  top: 0;
  width: 100%;
  height: 82px;
  border-radius: 8px;
  background: rgba($color: #000000, $alpha: 0.4);
}

// @media (max-width: 768px) {
//   .depositCom {
//     .list {
//       ul {
//         li {
//           // padding: 20px 15px;
//           width: 106px;
//           height: 56px;

//           span {
//             font-size: 16px;
//           }
//         }
//       }
//     }

//     .amount_box {
//       padding: 5px 10px;

//       .country {
//         img {
//           margin-right: 7px;
//           width: 27px;
//         }

//         span {
//           font-size: 14px;
//         }
//       }

//       .input_box_style {
//         height: 37px;

//         :deep(.el-input__wrapper) {
//           input {
//             padding-left: 80px !important;

//             &::placeholder {
//               font-size: 12px;
//             }
//           }
//         }


//       }

//       .gift_fontBox {
//         min-width: 80px;
//       }

//       .gift_font {
//         font-size: 12px;
//       }
//     }

//     // .submit_btn {
//     //   padding: 8px 0;
//     //   border-radius: 8px;
//     // }

//     .rules {
//       .title {
//         font-size: 15px;
//       }

//       p {
//         font-size: 12px;
//         line-height: 15px;
//       }
//     }
//   }

//   .activity {
//     height: 94px;

//     .top {
//       height: 60px;


//       .topFont>p:nth-child(1) {
//         font-size: 15px;

//       }

//       .topFont>p:nth-child(2) {
//         font-size: 12px;
//       }
//     }

//     .topP {
//       font-size: 22PX;

//     }

//     .bottom {
//       height: 38px;
//     }
//   }

//   .Participatedinevent::after {
//     height: 60px;
//   }
// }

.check_bonus {

  background: linear-gradient(to right, #346F4D, #1A2A32) !important;
}

.firstBonus {
  // width: 100%;
  padding: 10px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(to right, #2D3144, #1D1D29);
  margin: 12px 0 18px;

  p {
    margin: 0;
    color: #DCE6E3;
    font-size: 14px;
    font-weight: 600;
    line-height: 14px;
    margin-left: 10px;
  }

  .num {
    font-size: 13px;
    color: #7AF806;
    font-weight: 700;
    margin-right: 10px;
  }
}
</style>
