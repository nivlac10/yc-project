<template>
  <div class="vipBonus">

    <back :backNameShow="false" :img="getImageUrl('vipBonus/vip_head_img.png')" :title="t('vipBonus.VIPBÔNUS')" />
    <checkIn></checkIn>
    <LifetimeReferralBonus></LifetimeReferralBonus>

    <banner />
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { getImageUrl } from "@/utils/baseFun";
import banner from "../components/banner.vue";
import back from "@com/back/index.vue";
import checkIn from "../childrens/checkIn.vue";
import LifetimeReferralBonus from "../components/LifetimeReferralBonus.vue";
export default defineComponent({
  name: "vipBonus",
  components: { banner, back, LifetimeReferralBonus, checkIn},
  setup() {
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({});
    const jump = () => {
      router.push("/vipBonus/allRanks");
    };
    return { ...toRefs(state), t, store, jump, getImageUrl };
  },
});
</script>
<style  lang="scss" scoped>
.vipBonus {}

@media (max-width: 768px) {

  .vipBonus {
    padding: 0 12px;
  }
}
</style>
