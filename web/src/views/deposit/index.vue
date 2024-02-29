<template>
  <div class="deposit">
    <el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
      :width="store.state.status.isPc ? '424px' : '100%'">
      <deposit-column v-show="depositComShow == 0" />
      <withdraw-settings v-if="depositComShow == 1" />
      <bets-amount-rules v-if="depositComShow == 2" />
      <deposit-rules v-if="depositComShow == 3" />
      <deposit-instructions v-if="depositComShow == 4" />
    </el-dialog>


  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import depositColumn from "./deposit.vue";
import withdrawSettings from "./components/withdrawSettings.vue";
import betsAmountRules from "./components/betsAmountRules.vue";
import payPop from "./components/payPop.vue";
import depositRules from "./components/depositRules.vue";
import depositInstructions from "./components/depositInstructions.vue";
export default defineComponent({
  name: "deposit",
  components: { depositColumn, withdrawSettings, betsAmountRules, payPop, depositRules, depositInstructions },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const store = useStore();
    const router = useRouter();
    const state = reactive({
      dialogVisible: true,
      depositComShow: 0,
      showPayPop: computed(() => store.state.status.showPayPop),
    });

    proxy.$mitt.on("depositComShow", (val: number) => {
      state.depositComShow = val;
    });
    return { ...toRefs(state), store };
  },
});
</script>
<style  lang="scss" scoped>
.deposit {
  >.box {
    >span {
      color: pink;
    }
  }
}

@media (max-width: 768px) {}
</style>
