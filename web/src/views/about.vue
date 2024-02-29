<template>
  <div class="about">
    <h1>1232132131</h1>
    <div class="box">
      <span>232322</span>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "about",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({});
    return { ...toRefs(state), store, t, };
  },
});
</script>
<style  lang="scss" scoped>
.about {
  >.box {
    >span {
      color: pink;
    }
  }
}

@media (max-width: 768px) {}
</style>
