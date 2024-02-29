<template>
  <div class="vipBonus_index">
    <router-view />

  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
export default defineComponent({
  name: "vipBonus_index",
  components: {},
  setup() {
    const state = reactive({});
    return { ...toRefs(state) };
  },
});
</script> 
<style  lang="scss" scoped>
.vipBonus_index {}
</style>
