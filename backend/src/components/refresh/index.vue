<script lang="ts" setup>
import { inject, ref, watchEffect } from "vue"
import { ElMessage } from "element-plus"

// 刷新
const refresh: any = inject('reload')
</script>

<template>
  <div @click="refresh()">
    <el-tooltip effect="dark" content="刷新页面" placement="bottom">
      <el-icon style="font-size: 20px;">
        <Refresh />
      </el-icon>
    </el-tooltip>
  </div>
</template>

<style lang="scss" scoped>
.svg-icon {
  font-size: 20px;

  &:focus {
    outline: none;
  }
}
</style>
