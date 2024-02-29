<template>
  <div class="deposit">
    <div class="colse_btn" @click="payClose">
      <img src="@assets/images/public/Shutdownx.png" alt="" />
    </div>
    <div v-show="!callBackShow">
      <img loading="lazy" class="payImg" src="@/assets/images/deposit/pix.png" alt="" />
      <div class="payTop" v-show="pay_type == 0"><span>{{ t('account.Valor') }}</span><text>{{ moneyFormat(Props.money)
      }}</text></div>

      <!-- <div class="payTop"><span>Pagueate</span><text>{{time}}</text></div> -->

      <div class="payCenter" v-if="Props.pay_type == 0">
        <div>{{
          t('deposit.PorfavorabraseuaplicativodepagamentoeescaneieocódigoQRabaixoparapagar')
        }}
        </div>
        <vueQr :text="pay.url"></vueQr>
        <div>{{ t('deposit.CopieocódigoPixabaixoecoleemeuappdepagamentoparafinaliza') }}</div>
        <div class="payCenterButton" @click="copyToClip(pay.url)">{{ t('deposit.CopiarCódigoPIX') }}</div>
        <div style="text-align: left;width: 100%;">{{ t('deposit.Comopagar') }}</div>
        <div style="margin-top: -10px;">
          {{ t('deposit.ColeocódigoPixemseuappbancáriooucarteiradigitaldepreferênciaeconfirmeopagamento') }}</div>
      </div>
      <deposit-iframe v-else :url="Props.pay_url" />
    </div>
    <div class="callBack" v-show="callBackShow">
      <div class="head_t">{{ t('deposit.Resultadodopagamento') }}</div>
      <div class="head">
        <p>{{ t('deposit.ordernumber') }} : {{ pay.order_number }}</p>
        <img src="@/assets/images/public/copy.png" alt="" @click="copyToClip(pay.order_number)">
      </div>


      <div :class="{ loadImg2: loadState == true }" class="orderStateLoadBox"
        :style="{ backgroundColor: orderState == 2 ? '#FF0000' : '#6FCD7E' }">
        <img v-if="orderState == 0" src="@/assets/images/deposit/wallet-pending_return.png" alt="">
        <img v-if="orderState == 1" src="@/assets/images/deposit/OK.svg" alt="">
        <img v-if="orderState == 2" src="@/assets/images/deposit/err.svg" alt="">

      </div>
      <div class="orderState" v-if="orderState == 0">
        <span class="tips01">{{ t('deposit.orderTitle0') }}</span>
        <span class="tips02">{{ t('deposit.orderInfo0') }}</span>
      </div>
      <div class="orderState" v-if="orderState == 1">
        <span class="tips01">{{ t('deposit.orderTitle1') }}</span>
        <span class="tips02">{{ t('deposit.orderInfo1') }}</span>
      </div>
      <div class="orderState" v-if="orderState == 2">
        <span class="tips01">{{ t('deposit.orderTitle2') }}</span>
        <span class="tips02">{{ t('deposit.orderInfo2') }}</span>
      </div>
      <button class="load_btn" v-if="orderState == 0" @click="getOrderState">{{ t('btnName.Atualizar') }}</button>
      <!-- <div class="rechargeActivities_box">
        <img src="@assets/images/deposit/Deposit_bonus.png" alt="">
        <div class="rechargeActivities_box_title">Depósito + 10% de bônus</div>
        <div class="rechargeActivities_box_rules">
          ．Bônus de Depósito = Valor do Depósito x 10%<br />
          ．Os jogadores têm duas oportunidades de receber um bônus de depósito de 10% diariamente<br />
          ．Deposite hoje e receba seu bônus no『Gabinete Bônus』 amanhã!
        </div>
      </div> -->
    </div>
  </div>
</template>
<script setup>
import { ref, watch, onBeforeUnmount, getCurrentInstance } from "vue";
import { useI18n } from "vue-i18n";
import vueQr from 'vue-qr/src/packages/vue-qr.vue'
import { copy } from "@/utils/baseFun";
import { useStore } from "@/store/index";
import { deposito } from "@/api/deposito"
import { getUserInfo, moneyFormat } from "@/utils/baseFun"
import { rechage_adjust } from "@/utils/Adjust"
import depositIframe from "./depositIframe.vue";
let store = useStore();
const { t } = useI18n();
let callBackShow = ref(false);
let tdBarcodePaymentDialog = ref(true)
const { proxy } = getCurrentInstance();


const Props = defineProps({
  Pay: {},
  money: 0,
  pay_type: 0,
  pay_url: ''
});

let pay = ref(Props.Pay);
let loadState = ref(false);// 订单状态
let orderState = ref(0)

function copyToClip(v) {
  copy(v)
}

function payClose() {
  if (callBackShow.value) {
    store.state.status.showPayPop = false;
    callBackShow.value = false;
  } else {
    callBackShow.value = true;
  }
  getOrderState()
}

async function getOrderState() {
  loadState.value = true
  let orderData = await deposito.get_order_state({ order_number: Props.Pay.order_number })
  if (orderData.data.code == 1) {
    orderState.value = orderData.data.state
    if (orderState.value == 1) {
      store.state.status.depositShow = false
      getUserInfo()
      // 充值上报
      rechage_adjust(orderData.data.money)
      store.state.status.showPayPop = false
    }
  }
  loadState.value = false
}
// onBeforeUnmount(() => {
//   getOrderState()
// })
</script>
<style lang="scss" scoped>
.deposit {
  position: relative;
  padding: 35px 20px;
  width: 424px;
  background: #202330;
  border-radius: 16px;
  box-sizing: border-box;

  .colse_btn {
    cursor: pointer;
    position: absolute;
    top: 21px;
    right: 19px;

    img {
      width: 20px;
    }
  }
}

.payImg {
  width: 174px;
  margin-bottom: 24px;
}

.payTop {
  margin-bottom: 12px;
  display: flex;
  width: 100%;
  color: #B2B6C5;
  font-size: 16px;

  text {
    color: #fff;
    margin-left: 5px;
  }
}

.payCenter {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  font-size: 14px;
  font-weight: 400;
  color: #B2B6C5;
  line-height: 18px;

  .img {
    height: 150px !important;
    width: 150px !important;
    padding: 30px 0;
  }
}

.payCenterButton {
  cursor: pointer;
  width: 200px;
  line-height: 40px;
  background: #4181EE;
  border-radius: 6px;
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  color: #FFFFFF;
}

.callBack {
  display: flex;
  flex-direction: column;
  align-items: center;

  .head_t {
    margin-bottom: 16px;
    font-size: 16px;
    color: #B2B6C5;
  }

  .head {
    display: flex;
    justify-content: flex-end;
    align-items: center;

    p {
      font-size: 14px;
      color: #FFFFFF;
    }

    img {
      cursor: pointer;
      width: 18px;
      margin-left: 10px;
    }
  }

  .orderStateLoadBox {
    margin: 30px 0 32px 0;
    border-radius: 50%;
    position: relative;
    width: 70px;
    height: 70px;
    display: flex;
    justify-content: center;
    align-items: center;

    img {
      width: 48px;
    }
  }

  .orderState {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    padding: 0 10px;
    gap: 12px;
  }

  span {
    font-size: 14px;
    color: #fff;
    // line-height: 0.3rem;
    text-align: center;
  }

  .tips01 {
    font-weight: 600;
  }

  .tips02 {
    color: #B2B6C5;
    line-height: 18px;
  }


  .load_btn {
    cursor: pointer;
    border: none;
    background-color: #4181EE;
    color: #fff;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    line-height: 40px;
    width: 200px;
  }

  .rechargeActivities_box {
    margin-top: 24px;
    padding: 21px 11px;
    box-shadow: 0px 0px 15px 0px rgba(148, 239, 90, 0.05);
    border-radius: 8px;
    border: 1px solid #585E77;

    img {
      margin: 0 auto;
      display: block;
      width: 75px;
    }

    .rechargeActivities_box_title {
      padding: 12px 0 20px 0;
      text-align: center;
      font-size: 16px;
      font-weight: 600;
      color: #FFFFFF;
    }

    .rechargeActivities_box_rules {
      font-size: 14px;
      color: #B2B6C5;
      line-height: 16px;
    }
  }
}

.loadImg2 {
  -webkit-animation: rotate_360 1s infinite;
  animation: rotate_360 1s infinite;
}

@media (max-width: 768px) {
  .deposit {
    .rechargeActivities_box {
      margin-top: 20px;
      border-radius: 6px;

      img {
        width: 60px;
      }

      .rechargeActivities_box_title {
        padding: 12px 0 16px 0;
        font-size: 14px;
      }

      .rechargeActivities_box_rules {
        font-size: 12px;
        line-height: 13px;
      }
    }
  }
}

@media (max-width: 768px) {
  .deposit {
    width: 100%;

    .colse_btn {
      img {
        width: 18px;
      }
    }

  }
}
</style>