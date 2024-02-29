<template>
  <div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";
export default defineComponent({
  name: "",
  components: {

  },
  setup() {
    const store = useStore();
    const state = reactive({
    });
    return { ...toRefs(state), store };
  },
});
</script>
<style  lang="scss" scoped></style>
