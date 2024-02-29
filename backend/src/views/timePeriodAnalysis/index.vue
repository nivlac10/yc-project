<template>
  <div class="app-container">
    <admin v-permission="['1', '2']"></admin>
    <editor v-permission="['4', '3']"></editor>
  </div>
</template>

<script lang="ts" setup >
import admin from './admin.vue';
import editor from './editor.vue';

</script>

<style lang="scss" scoped>
.box-card {
  overflow-x: scroll;

  .el-card__body {
    >div {
      // min-width: 800px;
    }
  }
}
</style>
