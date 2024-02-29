<template>
  <div class="content">
    <router-view />
  </div>
</template>

<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";
export default defineComponent({
  name: "content",
  setup() {
    const store = useStore();
    const state = reactive({});
    return { ...toRefs(state) };
  },
});
</script>
<style  lang="scss" scoped>
.content {
}
</style>
