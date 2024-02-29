<template>
  <div class="deposit">
    <div class="colse_btn" @click="closeBtn">
      <img src="@assets/images/public/Shutdownx.png" alt="" />
    </div>
    <div class="tab">
      <div :class="{ active: tabIdx == index }" v-for="(item, index) in tab" :key="item.title + index"
        @click="tabIdx = index">
        {{ item.title }}
      </div>
    </div>
    <div class="column_title">
      <span v-show="tabIdx == 0">{{ t('deposit.OpçõesdeDepósito') }}</span>
      <!-- <span v-show="tabIdx == 1">RETIRADA</span> -->
    </div>
    <div>
      <deposit-column v-show="tabIdx == 0" />
      <withdraw-column v-show="tabIdx == 1" />
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import depositColumn from "./components/depositColumn.vue";
import withdrawColumn from "./components/withdrawColumn.vue";
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "deposit",
  components: { depositColumn, withdrawColumn },
  setup() {
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      tabIdx: 0,
      tab: [{ title: computed(() => t('account.Depósito')) }, { title: computed(() => t('account.Retirada')) }],
    });

    const closeBtn = () => {
      store.dispatch('status/setDepositShow', false)
    }
    return { ...toRefs(state), t, store, closeBtn };
  },
});
</script>
<style  lang="scss" scoped>
.deposit {
  position: relative;
  padding: 36px 19px 34px 19px;
  width: 100%;
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

  .tab {
    margin: 0 auto;
    padding: 2px;
    box-sizing: border-box;
    display: flex;
    width: 258px;
    margin-bottom: 39px;
    background: #2F3445;
    border-radius: 8px;

    div {
      width: 50%;
      text-align: center;
      cursor: pointer;
      // padding: 13px 31px;
      border-radius: 8px;
      line-height: 32px;
      font-size: 16px;
      font-weight: 600;
      color: #98ABD0;
    }

    .active {
      color: #fff;
      background: rgba(65, 129, 238, 0.5);
    }
  }

  .column_title {
    margin-bottom: 17px;
    font-size: 14px;
    color: #B2B6C5;

    span {
      font-weight: 600;
    }
  }
}

@media (max-width: 768px) {
  .deposit {
    margin: 0 11px;
    width: 100%;

    .colse_btn {
      img {
        width: 18px;
      }
    }

    .tab {
      div {
        font-size: 14px;
      }
    }

    .column_title {
      font-size: 20px;
    }
  }
}
</style>
