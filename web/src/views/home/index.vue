<template>
  <div class="home_index">
    <router-view />
  </div>
</template> 
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";
export default defineComponent({
  name: "home_index",
  setup() {
    const store = useStore();
    const state = reactive({});
    return { ...toRefs(state), store };
  },
});
</script>
<style  lang="scss" scoped>
.home_index {
  padding: 0 10px;
}
</style>
