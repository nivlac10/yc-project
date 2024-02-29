<template>
  <div class="refer">
    <barckTitle :backNameShow="false" :title="t('refer.BÔNUSPORINDICAÇÃO')" />
    <div class="column_tab">
      <div :class="{ active: tabsIdx == i }" v-for="(v, i) in tabs" @click="tabsIdx = i">{{ v.value }}</div>
    </div>

    <referral-reward v-if="tabsIdx == 0" />
    <myInvitations v-if="tabsIdx == 1"></myInvitations>
    <DataStatistics v-if="tabsIdx == 2"></DataStatistics>
    <members v-if="tabsIdx == 3"></members>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent,computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import barckTitle from "@/components/back/index.vue";
import referralReward from "./components/referralReward.vue"
import DataStatistics from "./components/DataStatistics.vue";
import members from "./components/members.vue";
import myInvitations from "./components/myInvitations.vue";


export default defineComponent({
  name: "refer",
  components: { barckTitle, referralReward, DataStatistics, members, myInvitations },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      tabsIdx: 0,
      tabs: [computed(()=>t('refer.RecompensaporIndicação')), computed(()=>t('refer.MinhasIndicações')), computed(()=>t('refer.Membros')), computed(()=>t('refer.EstatísticasDados'))]
    });
    proxy.$mitt.on('changeTabsIdx', (val: number) => {
      state.tabsIdx = val
    })
    return { ...toRefs(state), store, t, };
  },
});
</script>
<style  lang="scss" scoped>
.refer {
  .column_tab {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;

    div {
      cursor: pointer;
      padding: 17px 16px;
      background: #202330;
      border-radius: 8px;
      font-size: 16px;
      font-weight: bold;
      color: #9195A3;
      box-sizing: border-box;
      border: 2px solid transparent;

      &.active {
        color: #FFFFFF;
        background: rgba(65, 129, 238, 0.5);
        border: 2px solid rgba(65, 129, 238, 0.8);
      }
    }
  }
}

@media (max-width: 768px) {
  .refer {
    padding: 0 12px;

    .column_tab {
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 12px;

      div {
        cursor: pointer;
        padding: 11px 8px;
        border-radius: 6px;
        font-size: 12px;
      }
    }
  }
}
</style>
