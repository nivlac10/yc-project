<template>
  <div class="loading_index">
    <img src="@assets/images/public/loading.gif" alt="">
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
export default defineComponent({
  name: "loading_index",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const state = reactive({});
    return { ...toRefs(state), store };
  },
});
</script>
<style  lang="scss" scoped>
.loading_index {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 999999;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba($color: #000000, $alpha: 0.5);

  img {
    width: 400px;
  }
}

@media (max-width: 768px) {
  .loading_index {
    img {
      width: 50%;
    }
  }
}
</style>
