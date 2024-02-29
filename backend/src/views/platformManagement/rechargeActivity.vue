<template>
  <div class="app-container app-container_re">
    <el-card class="box-card box-card_re">
      <recharge-activity-com1 />
    </el-card>
    <el-card class="box-card box-card_re uno-margin-top">
      <recharge-activity-com2 />
    </el-card>
  </div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import rechargeActivityCom1 from "./components/rechargeActivityCom1.vue"
import rechargeActivityCom2 from "./components/rechargeActivityCom2.vue"
const router = useRouter();
const state = reactive({
})


</script>

<style lang="scss" scoped>
.app-container_re {
  padding: 0;
}

.box-card_re {
  >:deep(.el-card__body) {
    padding: 0;
  }
}
</style>


