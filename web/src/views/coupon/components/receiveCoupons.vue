<template>
  <div class="receiveCoupons">
    <div class="img">
      <img src="@assets/images/coupon/coupon_.png" alt="" />
      <p>{{ t('coupon.Resgateaquiseucódigodecupom') }}</p>
      <span>{{ t('coupon.Publicamossociais') }}</span>
      <div class="shaer_box">
        <img src="@assets/images/sidebar/Telegram_icon@2x.png" alt="" @click="jumpTo(0)" />
        <span>Telegram: <a style="color: #3EA0F1;" :href="store.state.conf.all_conf.tg_channel_url">{{
          store.state.conf.all_conf.tg_channel_url }}</a></span>
        <!-- <img src="@assets/images/sidebar/Twittr_icon@2x.png" alt="" @click="jumpTo(1)" />
        <img src="@assets/images/sidebar/Facebook_icon@2x.png" alt="" @click="jumpTo(2)" />
        <img src="@assets/images/sidebar/instagram_icon@2x.png" alt="" @click="jumpTo(3)" />
        <img src="@assets/images/sidebar/YouTube_icon@2x.png" alt="" @click="jumpTo(4)" /> -->
      </div>
    </div>
    <div class="input_box">
      <img src="@assets/images/coupon/coupon.png" alt="">
      <input type="text" v-model="code" :placeholder="t('coupon.digitarcódigodecupom')">
    </div>
    <!-- <div class="tips_box">
      <span>Montante de bonus: <span class="tips_span">0.1-100.00</span></span>
    </div> -->
    <div class="regulariy">
      <span>{{ t('coupon.ValordeBônus') }} :</span><span>{{t('base.currencySymbol')}} 0.1 ~ {{t('base.currencySymbol')}} 100</span>
    </div>

    <div class="btn">
      <span class="" @click="receiveClick">{{ t('dailyBettingBonus.CLAIM') }}</span>
    </div>

    <!-- <el-dialog v-model="needRecharg" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
      :width="store.state.status.isPc ? '760px' : '100%'">
      <div class="need_recharg_box">
        <div class="close_box">
          <img class="close_img" src="@assets/images/public/Shut_down.png" alt="" @click="btnClick(0)">
        </div>
        <div class="need_box">
          <img class="depos" src="@assets/images/coupon/Depósito.png" alt="">
          <span class="tips">Para receber o bônus do cupom, é necessário um depósito.</span>
          <div class="sl_box_shadow" @click="btnClick(2)"><span>Depósito</span></div>
        </div>
      </div>
    </el-dialog> -->
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { getUserInfo } from "@/utils/baseFun";
import { giveCode } from "@/api/giveCode"
import promptPopup from "@/components/promptPopup/index";
export default defineComponent({
  name: "receiveCoupons",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const route = useRoute()
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      code: '',
      dialogVisible: false,
      amount: 0,
      needRecharg: false
    });
    // if()
    if (route.query.r) {
      // console.log('route.query.r', route.query.r);
      state.code = route.query.r as any
    }
    let load = true
    // 领取
    const receiveClick = () => {
      if (load) {
        load = false
        giveCode.user_receive_code({ code: state.code }).then((res) => {
          if (res.data.code == 1) {
            promptPopup('rewardPopup', { title: t('promptPopup.title_VOCÊVENCEU'), amount: res.data.money, tips: t('promptPopup.tips_Obônusjá'), btnName: t('btnName.Confirmar') })
          } else if (res.data.code == 36) {
            // state.needRecharg = true
            promptPopup('depositPopup', { tips: t('promptPopup.tips_Parareceber'), btnName: t('btnName.Depósito') })

          }
        })
        load = true
      }
    }
    const goToTG = () => {
      window.open(store.state.conf.all_conf.tg_channel_url)
    }
    // 关闭
    const btnClick = (type: number) => {
      if (type == 1) {
        // getUserInfo()
        // state.dialogVisible = false
      } else if (type == 2) {
        store.state.status.depositShow = true
      } else if (type == 0) {

        // state.dialogVisible = false
        state.needRecharg = false
      }
    }
    // 跳转到社交软件
    const jumpTo = (index) => {

      let path = [
        { name: 'tg', url: store.state.conf.all_conf.tg_channel_url },
        { name: 'twitter', url: 'https://twitter.com/bigwin777io' },
        { name: 'Facebook', url: 'https://www.facebook.com/bigwin777.io' },
        { name: 'Instagram', url: 'https://www.instagram.com/bigwin777.io/' },
        { name: 'youtube', url: 'https://www.youtube.com/channel/UC5XmBVsYrdTsD98314GJqtg' },
      ]
      window.open(path[index].url);
    }
    return { ...toRefs(state), store, t, receiveClick, btnClick, goToTG, jumpTo };
  },
});
</script>
<style  lang="scss" scoped>
.receiveCoupons {
  // width: 100%;
  background-color: #1D1D29;
  padding: 20px 40px;
  border-radius: 23px 23px 23px 23px;
  display: flex;
  flex-direction: column;
  gap: 20px;

  .img {
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 20px;

    img {
      width: 240px;
    }

    p {
      // padding: 24px 0 24px 0;
      font-size: 30px;
      font-weight: bold;
      color: var(--theme-font-color-fff);
    }

    span {
      font-size: 16px;
      font-weight: 500;
      color: #B2B6C5;
      line-height: 19px;
    }

    .shaer_box {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 14px;

      img {
        width: 50px;
      }
    }
  }

  .input_box {
    height: auto;
    display: flex;
    background-color: #2D3144;
    border-radius: 12px 12px 12px 12px;
    padding: 0 10px;
    width: auto;

    img {
      width: 72px;
    }

    input {
      // padding-left: 56px;
      width: 100%;
      line-height: 80px;
      background: rgba($color: #000000, $alpha: 0);
      border-radius: 12px;
      border: 0;
      font-size: 24px;
      color: var(--theme-font-color-fff);
      box-sizing: border-box;

      &::placeholder {
        font-weight: 500;
        line-height: 80px;
        color: var(--auxiliary-font-color-2);
      }
    }
  }

  .regulariy {
    // padding: 50px 0;
    // text-align: center;
    font-size: 24px;
    font-weight: bold;

    span:nth-child(1) {
      margin-right: 5px;
      color: var(--auxiliary-font-color-9);
    }

    span:nth-child(2) {
      cursor: pointer;
      color: var(--auxiliary-font-color-23);
    }
  }

  .tips_box {

    // margin: 20;
    span {
      color: var(--auxiliary-font-color-9);
    }
  }

  .btn {
    cursor: pointer;
    display: flex;
    justify-content: center;
    background-color: #C01544;

    span {
      display: inline-block;
      padding: 25px 96px;
      font-size: 30px;
      font-weight: bold;
      color: #fff;
    }
  }

  .need_recharg_box {
    // width: 760px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #2D3144;
    padding: 10px 10px 40px 10px;
    gap: 20px;
    border-radius: 15.55px;

    .need_box {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 20px;
      // width: 496px;

    }

    .sl_box_shadow {
      padding: 15px 30px;
      color: #000;

      span {
        font-size: 28px;
        font-weight: 600;

      }
    }

    .depos {
      width: 154px;
    }

    .tips {
      color: #fff;
      font-size: 26px;
      line-height: 30px;
      text-align: center;
      // word-spacing: normal;
      word-wrap: break-word;
      width: 550px;
    }

    .close_box {
      width: 100%;
      display: flex;
      align-items: end;
      justify-content: right;
      // padding: 10px 0;

      img {
        width: 40px;
      }
    }

  }
}

@media (max-width: 768px) {
  .need_recharg_box {
    width: auto !important;
    margin: 0 20px !important;

    .tips {
      color: #fff;
      font-size: 18px !important;
      line-height: 30px;
      text-align: center;
      // word-spacing: normal;
      word-wrap: break-word;
      width: auto !important;
    }

    .sl_box_shadow {
      padding: 15px 25px !important;
      color: #000;

      span {
        font-size: 20px !important;
        font-weight: 600;

      }
    }
  }

  .receiveCoupons {

    // width: 100%;
    padding: 15px !important;

    .shaer_box {
      img {
        width: 30px !important;
      }
    }

    .img {
      text-align: center;

      img {
        width: 138px;
      }

      p {
        padding: 0px 0 0px 0;
        font-size: 18px;
      }

      span {
        font-size: 12px;
      }
    }

    .input_box {

      // margin: 0 20px;
      img {
        width: 36px !important;
      }

      input {
        padding-left: 21px;
        line-height: 46px;
        font-size: 16px;
      }
    }

    .regulariy {
      padding: 16px 0 30px 0;
      font-size: 14px;
    }

    .btn {
      border-radius: 6px;

      span {
        padding: 15px 26px;
        font-size: 20px;
      }
    }
  }
}
</style>
