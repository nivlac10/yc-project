<template>
  <div class="betsAmountRules">
    <el-dialog class="loginDialog" v-model="dialogVisible" :show-close="false" :close-on-click-modal="false"
      :close-on-press-escape="false" :width="store.state.status.isPc ? '512px' : '100%'">
      <div class="content_box">
        <img class="close_btn" src="@assets/images/public/popover_error_icon.png" alt="" @click="closeCom">
        <div class="header">
          <img src="@assets/images/public/popover_return.png" alt="" @click="jump">
          <div class="title">
            {{ t('deposit.BetsAmountRules') }}
          </div>
        </div>
        <ul>
          <li>{{ t('deposit.betsAmountRules_1') }}</li>
          <li>{{ t('deposit.betsAmountRules_2') }}</li>
          <li>{{ t('deposit.betsAmountRules_3') }}</li>
          <li>{{ t('deposit.betsAmountRules_4') }}</li>
        </ul>
        <div class="txt">
          <p>{{ t('deposit.betsAmountRules_5') }}</p>
          <p>{{ t('deposit.betsAmountRules_6') }}</p>
          <p>{{ t('deposit.betsAmountRules_7') }}</p>
          <p>{{ t('deposit.betsAmountRules_8') }}</p>
        </div>
        <div class="txt">
          <p>{{ t('deposit.betsAmountRules_9') }}</p>
          <p>{{ t('deposit.betsAmountRules_6') }}</p>
          <p>{{ t('deposit.betsAmountRules_10') }}</p>
          <p>{{ t('deposit.betsAmountRules_11') }}</p>
        </div>
        <div class="txt">
          <p>{{ t('deposit.betsAmountRules_12') }}</p>
          <p>{{ t('deposit.betsAmountRules_13') }}</p>
          <p>{{ t('deposit.betsAmountRules_14') }}</p>
          <p>{{ t('deposit.betsAmountRules_15') }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "betsAmountRules",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      dialogVisible: true,
    });
    const closeCom = () => {
      store.dispatch('status/setDepositShow', false)
    }
    const jump = () => {
      proxy.$mitt.emit("depositComShow", 0);
    }
    return { ...toRefs(state), store, t, jump, closeCom };
  },
});
</script>
<style  lang="scss" scoped>
.betsAmountRules {
  .content_box {
    position: relative;
    padding: 56px 28px 40px 28px;
    width: 100%;
    border-radius: 16px;
    background: var(--theme-box-background);
    box-sizing: border-box;

    .close_btn {
      cursor: pointer;
      position: absolute;
      top: 23px;
      right: 28px;
      width: 25px;
    }

    .header {
      display: flex;
      align-items: center;
      margin-bottom: 25px;

      img {
        cursor: pointer;
        margin-right: 15px;
        width: 30px;
      }

      .title {
        font-size: 26px;
        font-weight: bold;
        color: var(--theme-font-color-fff);
      }
    }

    ul {
      padding-left: 20px;
      margin-bottom: 24px;

      li {
        font-size: 14px;
        font-weight: 500;
        color: var(--auxiliary-font-color-9);
        line-height: 16px;
        list-style: disc;
      }
    }

    .txt {
      margin-bottom: 24px;

      p {
        font-size: 14px;
        font-weight: 500;
        color: var(--auxiliary-font-color-9);
        line-height: 21px;
      }
    }
  }
}

@media (max-width: 768px) {
  .betsAmountRules {
    .content_box {
      padding: 36px 20px 40px 20px;
      border-radius: 0;

      .close_btn {
        top: 14px;
        right: 19px;
        width: 18px;
      }

      .header {
        img {
          cursor: pointer;
          margin-right: 8px;
          width: 30px;
        }

        .title {
          font-size: 17px;
        }
      }

      p {
        margin-bottom: 5px;
        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
        color: #7992A7;
      }
    }
  }
}
</style>
