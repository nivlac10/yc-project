<template>
  <div class="app-container">
    <el-collapse v-model="state.activeNames">
      <el-collapse-item name="1">
        <template #title>
          <div style="font-size: 24px; font-weight: 600; margin-left: 20px;">返佣配置</div>
        </template>
        <commission-configuration-com1 />
      </el-collapse-item>
      <el-collapse-item name="2">
        <template #title>
          <div style="font-size: 24px; font-weight: 600; margin-left: 20px;">邀请任务</div>
        </template>
        <commission-configuration-com2 />
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import commissionConfigurationCom1 from "./components/commissionConfigurationCom1.vue"
import commissionConfigurationCom2 from "./components/commissionConfigurationCom2.vue"
const router = useRouter();
const state = reactive({
  activeNames: ['1'],
})
</script>

<style lang="scss" scoped></style>

