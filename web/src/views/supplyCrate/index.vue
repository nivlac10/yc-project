<template>
  <div class="supplyCrate_index">
    <div class="head">
      <barckTitle></barckTitle>
      <img src="@/assets/images/supplyCrate/BÔNUS_PARA_PERDA.png" alt="" srcset="" class="titleImg">
    </div>
    <supply-crate v-if="comShow == 0" />

    <activities />
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import supplyCrate from "./components/supplyCrate.vue"
import activities from "./components/activities.vue"
import barckTitle from "@/components/back/index.vue";
export default defineComponent({
  name: "supplyCrate_index",
  components: { supplyCrate, activities, barckTitle },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      comShow: 0,
    });

    return { ...toRefs(state), store, t, };
  },
});
</script>
<style  lang="scss" scoped>
.supplyCrate_index {
  .titleImg {
    width: 100%;
    margin-bottom: 24px;
  }

}

@media (max-width: 768px) {
  .head{
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>
