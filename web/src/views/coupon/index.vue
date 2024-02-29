<template>
  <div class="coupon">
    <div class="box">
      <receive-coupons />
      <receive-list />
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import receiveCoupons from "./components/receiveCoupons.vue"
import receiveList from "./components/receiveList.vue"
export default defineComponent({
  name: "coupon",
  components: { receiveCoupons, receiveList },
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
.coupon {
  padding-top: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  .box {
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    gap: 18px;
    max-width: 680px;
  }
}

@media (max-width: 768px) {
  .coupon {
    padding: 40px 20px 0 20px;

    .box {
      flex-direction: column;
    }
  }
}
</style>
