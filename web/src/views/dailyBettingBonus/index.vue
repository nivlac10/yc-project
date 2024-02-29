<template>
  <div class="dailyBettingBonus_index">
    <back />
    <daily-betting-bonus />
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import dailyBettingBonus from "./components/dailyBettingBonus.vue"
import activities from "./components/activities.vue"
import back from "@/components/back/index.vue"
export default defineComponent({
  name: "dailyBettingBonus_index",
  components: { dailyBettingBonus, activities, back },
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
.dailyBettingBonus_index {}

@media (max-width: 768px) {
  .dailyBettingBonus_index {
    padding: 0 10px;
  }
}
</style>
