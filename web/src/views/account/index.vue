<template>
  <div class="account">
    <back :back-name-show="false" :title="t('account.CentrodeContas')" />

    <div class="tabs">
      <div class="tab_item" :class="{ tab_item: true, active: tabIdx == index }" v-for="(item, index) in tab"
        :key="item.title + index" @click="tabIdx = index">
        <svg-icon :name="item.img" :color="tabIdx == index ? '#fff' : '#B2B6C5'" />
        <div>{{ item.title }}</div>
      </div>
    </div>

    <my-account v-if="tabIdx == 0" />
    <Transactions v-else-if="tabIdx == 1" />
    <settings v-else />
  </div>
</template>
<script lang="ts">
import { getImageUrl } from "@/utils/baseFun";
import {
  reactive,
  toRefs,
  getCurrentInstance,
  defineComponent,
  watch,
  computed
} from "vue";
import { useRouter, useRoute } from "vue-router";
import myAccount from "./components/myAccount.vue";
import Transactions from "./components/Transactions.vue";
import { useI18n } from "vue-i18n";
import back from "@com/back/index.vue"
import settings from "./components/settings.vue"
export default defineComponent({
  name: "account",
  components: { myAccount, Transactions, back, settings },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const { t } = useI18n();
    const state = reactive({
      tabIdx: 0,
      tab: [
        {
          img: 'Subtract',
          title: computed(() => t('account.Conta')),
        },
        {
          img: 'Transactions_icon',
          title: computed(() => t('account.Transações')),
        },
        {
          img: 'Settings',
          title: computed(() => t('account.Configurações')),
        },
      ],
    });
    watch(
      () => router,
      (to) => {
        if (route.query.tabIdx) state.tabIdx = route.query.tabIdx as any;
        else state.tabIdx = 0;
      },
      { deep: true, immediate: true }
    );

    const tabChange = (index: number) => {
      state.tabIdx = index;
    };

    return { ...toRefs(state), t, tabChange };
  },
});
</script>
<style  lang="scss" scoped>
.account {
  .tabs {
    display: flex;
    gap: 12px;
    padding: 12px 16px;
    margin-bottom: 25px;
    background: var(--theme-box-background);
    border-radius: 12px;

    .tab_item {
      cursor: pointer;
      padding: 4px 0 12px 0;
      width: 125px;
      text-align: center;
      border-radius: 8px;
      background: #2F3445;

      &:hover {
        background: #4181EE;

        .svg-icon {
          color: #fff !important;
        }

        div {
          color: #fff;
        }
      }

      &.active {
        background: #4181EE;

        div {
          color: var(--theme-font-color-fff);
        }
      }

      .svg-icon {
        margin-bottom: 4px;
        width: 40px;
        height: 40px;
        color: #B2B6C5;
      }

      div {
        font-size: 14px;
        color: #98ABD0;
      }
    }
  }
}

@media (max-width: 768px) {
  .account {
    margin: 0 12px;

    .tabs {
      gap: 8px;
      padding: 8px;
      margin-bottom: 12px;
      border-radius: 8px;

      .tab_item {
        cursor: pointer;
        padding: 4px 0 12px 0;
        width: 99px;
        border-radius: 8px;

        .svg-icon {
          margin-bottom: 2px;
          width: 35px;
          height: 35px;
        }

        div {
          font-size: 12px;
        }
      }
    }
  }
}
</style>
