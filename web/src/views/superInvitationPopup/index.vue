<template>
  <div class="superInvitationPopup" v-show="flag">
    <div class="content_box">
      <img class="close_img" src="@assets/images/public/Shutdown.png" alt="" @click="closeBtn">
      <img class="header_img" src="@assets/images/public/loading.png" alt="" />
      <div class="box">
        <p>
          {{ t('superInvitationPopup.p1') }}<span>8225 {{ t('base.currency') }}</span>
        </p>
        <div class="btn" @click="urlJump">{{ t('account.GETBONUS') }}</div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "superInvitationPopup",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      flag: false
    });

    if (sessionStorage.getItem('superInvitationPopupFlag')) state.flag = false
    else state.flag = true

    const closeBtn = () => {
      state.flag = false
      sessionStorage.setItem('superInvitationPopupFlag', 'true',)
    }

    const urlJump = () => {
      closeBtn()
      router.push('/refer')
    }

    return { ...toRefs(state), store, t, closeBtn, urlJump };
  },
});
</script>
<style  lang="scss" scoped>
.superInvitationPopup {
  position: fixed;
  left: 50%;
  bottom: 40px;
  transform: translateX(-50%);
  z-index: 20;

  .content_box {
    position: relative;
    width: 551px;
    min-height: 128px;
    background: url(@assets/images/superInvitationPopup/backdrop.png) no-repeat;
    background-size: 100% 100%;

    .close_img {
      cursor: pointer;
      position: absolute;
      top: 13px;
      right: 15px;
      width: 13px;
    }

    .header_img {
      position: absolute;
      left: -65px;
      width: 143px;
      transform: rotate(-15deg);
    }

    .box {
      display: flex;
      align-items: center;
      min-height: 128px;

      p {
        padding-left: 80px;
        font-size: 20px;
        font-weight: bold;
        color: var(--theme-font-color-fff);
        line-height: 30px;

        span {
          font-weight: bold;
          color: var(--auxiliary-font-color-25);
        }
      }

      .btn {
        margin-right: 10px;
        cursor: pointer;
        padding: 14px 24px;
        font-size: 20px;
        font-weight: bold;
        color: var(--theme-font-color-fff);
        white-space: nowrap;
        border-radius: 8px;
        background: var(--auxiliary-background-22);
        box-sizing: border-box;
      }
    }
  }
}

@media (max-width: 768px) {
  .superInvitationPopup {
    padding: 0 14px;
    box-sizing: border-box;
    width: 100%;
    bottom: 105px;

    .content_box {
      width: 100%;

      .header_img {
        position: absolute;
        top: 0;
        left: 50%;
        width: 128px;
        transform: rotate(0deg) translate(-50%, -50%);
      }

      .box {
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 100%;
        width: 100%;
        padding: 0 29px;
        box-sizing: border-box;

        p {
          text-align: center;
          padding: 40px 0 0 0;
          font-size: 18px;
          font-weight: bold;
          color: var(--theme-font-color-fff);
          line-height: 20px;
          margin-bottom: 15px;

          span {
            font-weight: bold;
            color: var(--auxiliary-font-color-25);
          }
        }

        .btn {
          margin: 0 0 10px 0;
          width: 100%;
          text-align: center;
          padding: 8px 0;
          font-size: 14px;
          border-radius: 4px;
        }
      }
    }
  }
}
</style>
