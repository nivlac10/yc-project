<template>
  <div class="withdrawColumn">
    <refer-withdrawal-information class="referWithdrawalInformation" />
    <div class="withdraw_info">
      <withdraw-column-amount-info />
      <!-- <div class="setting_btn_box">
        <div class="setting_btn"><span @click="jump">{{ t('deposit.READMORE') }}</span></div>
      </div> -->
    </div>
    <!-- <withdrawal-information /> -->
    <div class="withdraw_mode">
      <div class="amount_box">
        <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="inputFoucs"
          :inputRed="inputTxtRed" :data="validateForm.money" :isHead="false"
          :popTxt="`${t('deposit.Retiradadigitada')} ≥ ${store.state.conf.all_conf.pay_conf['min_withdraw_money']}${t('base.currency')}`"
          inputType="Number" class="RinputHeat">
          <template #head>
            <div class="country">
              <img src="@assets/images/language/brazil.png" alt="" />
              <span>{{ t('base.currency') }}</span>
            </div>
          </template>
        </Rinput>
      </div>
    </div>
    <div class="rate txt_box">
      <img :class="{ img_rotate: showMoreFlag }" src="@assets/images/public/down_arrow.png" alt=""
        @click="showMoreFlag = !showMoreFlag">
      <div>
        <div>
          <span>{{ t('deposit.Taxa') }}:&nbsp;</span>
          <span>{{ setRate }}</span>
        </div>
        <div>
          <span>{{ t('deposit.ValoraReceber') }}:&nbsp;</span>
          <span>{{ moneyFormat(setYouwillWin) }}</span>
        </div>
      </div>
      <div v-if="showMoreFlag">
        <span>{{ t('deposit.Limitederetiradadiária') }}:&nbsp;</span>
        <span>{{ vip_conf.day_max_withdraw }}</span>
      </div>
      <div v-if="showMoreFlag">
        <span>{{ t('deposit.Vezesderetiradadiária') }}:&nbsp;</span>
        <span>{{ vip_conf.withdraw_num }}</span>
      </div>
    </div>
    <div class="submit_btn" @click="submit">{{ t('deposit.RetirarDinheiro') }}</div>
    <div class="see_d" @click="jumpDepositInstructions">{{ t('btnName.Instruções') }} ></div>

    <!-- 设置手机号 -->
    <set-phone-number v-if="setPhoneNumberShow" />
  </div>
</template>
<script lang="ts">
import {
  reactive,
  toRefs,
  getCurrentInstance,
  defineComponent,
  computed,
} from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { DepositAndWithdraw } from "@/api/DepositAndWithdraw";
import { debounce, SuccessNotiFun, getUserInfo, getUserInfoNoLoad, moneyFormat } from "@/utils/baseFun";
import withdrawalInformation from "./withdrawalInformation.vue";
import { ElLoading } from 'element-plus'
import { useI18n } from "vue-i18n";
import withdrawColumnAmountInfo from "@views/deposit/components/withdrawColumnAmountInfo.vue"
import setPhoneNumber from "@views/account/components/setPhoneNumber.vue";
import { UserService } from "@/api/user"
import referWithdrawalInformation from "@views/Refer/components/withdrawalInformation.vue"
import promptPopup from "@/components/promptPopup";
import Rinput from "@views/Refer/components/input.vue";

export default defineComponent({
  name: "withdrawColumn",
  components: { withdrawalInformation, withdrawColumnAmountInfo, setPhoneNumber, referWithdrawalInformation, Rinput },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      validateForm: {
        money: "",
        name: store.state.user.username,
        cpf: store.state.user.CPF,
        pix: "CPF",
        pix_num: store.state.user.CPF,
        money_type: 0,
      },
      showMoreFlag: false,
      setPhoneNumberShow: false,
      inputFoucs: false,
      inputTxtRed: 1,
      vip_conf: store.state.conf.all_conf.vip_conf[store.state.user.vip_lv]
    });
    const settings = () => {
      proxy.$mitt.emit("depositComShow", 1);
    };
    getUserInfoNoLoad()
    const setRate = computed(() => {
      const pay_fee =
        store.state.conf.all_conf.vip_conf[store.state.user.vip_lv].pay_fee;
      return pay_fee + "%";
    });

    const setYouwillWin = computed(() => {
      const pay_fee =
        store.state.conf.all_conf.vip_conf[store.state.user.vip_lv].pay_fee;
      let money: number | string = state.validateForm.money;
      money = (money as any) - (money as any) * (pay_fee / 100);
      return money;
    });

    const changeInputState = (val, data) => {
      if (state.inputTxtRed == 1 && val == 'blur') {
        state.inputTxtRed = 0;
      }
      if (!data) {
        state.inputFoucs = !state.inputFoucs;
      }
    }
    const inputFun = (val) => {
      if (!val) {
        state.inputTxtRed = 1;
      }
      if (Number(val) > store.state.user.with_money) {
        state.inputTxtRed = 0;
        promptPopup('notificationPopup', { disappear: true, text: t('promptPopup.Ovalordesaqueque'), type: 'error' })
      } else {
        state.validateForm.money = val;
        state.inputTxtRed = 2;
      }
    }

    const submit = () => {
      if (!store.state.user.CPF || !store.state.user.username)
        return promptPopup('notificationPopup', { disappear: true, text: t('promptPopup.Salveasinformações'), type: 'error' })
      if (state.validateForm.money == "") return;
      if (!store.state.user.phone) return state.setPhoneNumberShow = true
      const fun = () => {
        let loading = ElLoading.service({
          lock: true,
          text: 'Loading',
          background: 'rgba(0, 0, 0, 0.7)',
        })

        DepositAndWithdraw.withdraw({
          money: state.validateForm.money,
          name: store.state.user.username,
          cpf: store.state.user.CPF,
          pix: "CPF",
          pix_num: store.state.user.CPF,
          money_type: 0,
        }).then(
          (res) => {
            loading.close()
            if (res.data.code == 1) {
              SuccessNotiFun("SuccessfullySubmitted")
              store.state.status.depositShow = false
              getUserInfo()
            }

          }
        );
      };
      debounce(fun);
    };

    const jump = () => {
      proxy.$mitt.emit("depositComShow", 2);
    }


    proxy.$mitt.on("showCom", (val: number) => {
      state.setPhoneNumberShow = false;
    });
    function user_code_empty() {
      if (store.state.user.money <= 0.5 && store.state.user.remain_code_amount > 0) {
        UserService.user_code_empty().then((res) => {
          if (res.data.code == 1) {
            store.state.status.depositShow = false
            getUserInfo().then(() => {
              store.state.status.depositShow = true
            })
          }
        })
      }
    }

    const jumpDepositInstructions = () => {
      proxy.$mitt.emit("depositComShow", 4);
    }

    return {
      ...toRefs(state),
      store,
      t,
      settings,
      submit,
      setRate,
      jump,
      setYouwillWin,
      user_code_empty,
      changeInputState,
      inputFun,
      moneyFormat,
      jumpDepositInstructions
    };
  },
});
</script>
<style  lang="scss" scoped>
.withdrawColumn {
  :deep(.referWithdrawalInformation) {
    .l_box {
      // padding: 0 !important;
    }

    .boder {
      margin-bottom: 0 !important;
    }

    .r_box {
      display: none !important;
    }
  }

  .withdraw_info {
    // margin-bottom: 18px;
    // padding: 11px 15px;
    // border: 1px solid #4C4F5D;
    // border-radius: 6px;

    .setting_btn_box {
      display: grid;
      margin-bottom: 10px;
      align-items: center;
      cursor: pointer;

      .setting_btn {
        // padding-bottom: 12px;
        text-align: center;

        span {
          cursor: pointer;
          font-size: 14px;
          font-weight: 600;
          color: var(--auxiliary-font-color-27);
        }
      }
    }

    .limpar_btn {
      padding: 5px;
      display: flex;
      // justify-content: center;
      border-radius: 100px;
      // justify-content: space-evenly;
      justify-content: space-between;
      align-items: center;

      span {
        color: #fff;
        font-size: 14px;
        font-weight: 600;
      }
    }

    div {
      font-size: 20px;
      color: var(--auxiliary-font-color-9);
    }

    // :deep(.el_popover_style) {
    //   background: var(--auxiliary-background-14);
    //   border: none;
    //   border-radius: 12px;
    //   font-size: 20px;

    //   .popover_content {
    //     .popover_content_header {
    //       margin-bottom: 12px;
    //       font-size: 14px !important;
    //       font-weight: bold;
    //       color: var(--theme-font-color-fff);
    //     }

    //     .popover_content_txt {
    //       font-size: 14px;
    //       font-weight: 400;
    //       color: var(--auxiliary-font-color-9);
    //       // line-height: 16px;
    //       text-indent: 2rem;
    //     }

    //     .popover_content_btn {
    //       text-align: right;
    //       cursor: pointer;
    //       font-size: 14px;
    //       font-weight: 500;
    //       color: var(--auxiliary-font-color-27);
    //     }
    //   }

    //   .el-popper__arrow {
    //     &::before {
    //       background: var(--auxiliary-background-14);
    //       border: none;
    //     }
    //   }
    // }
  }

  .withdraw_mode {
    margin: 18px 0;
    border-radius: 6px;

    .red {
      color: #EB4859;
    }

    .amount_box {
      position: relative;
      // display: flex;
      align-items: center;
      margin-top: 10px;

      .country {
        // position: absolute;
        // left: 18px;
        // top: 8px;
        display: flex;
        align-items: center;

        img {
          margin-right: 10px;
          width: 37px;
        }

        span {
          font-size: 14px;
          font-weight: 500;
          color: var(--theme-font-color-fff);
        }
      }

      :deep(.el_input_box) {
        .el-input__inner {
          // text-align: center;
          padding-left: 14px;
        }
      }
    }
  }

  .txt_box {
    position: relative;
    display: flex;
    flex-wrap: wrap;

    img {
      position: absolute;
      right: 8px;
      width: 16px;
    }

    .img_rotate {
      transform: rotate(180deg);
    }

    >div {
      display: flex;
      width: 100%;
      margin-bottom: 12px;

      &:nth-child(2) {
        div {
          margin-right: 15px;
        }
      }

      span:nth-child(1) {
        font-size: 14px;
        color: #B2B6C5;
      }

      span:nth-child(2) {
        font-size: 14px;
        color: #75ED3D;
      }
    }
  }

  .rate {
    margin-bottom: 5px;
  }

  .submit_btn {
    cursor: pointer;
    margin-bottom: 20px;
    font-size: 16px;
    text-align: center;
    font-weight: 600;
    color: #FFFFFF;
    line-height: 40px;
    background: #4181EE;
    border-radius: 138px;
  }

  .see_d {
    cursor: pointer;
    font-size: 14px;
    color: #4181EE;
    text-align: right;
  }
}
</style>
