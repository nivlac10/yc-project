<template>
  <div class="addToHomeScreen">
    <div class="btn" @click="btnClick" v-show="btnShow">
      {{ t('btnName.AdicionaràTelaInicial') }}
    </div>
    <div class="img_box" @click="btnClick" v-show="imgShow">
      <img src="@assets/images/public/iosdw.png" alt="">
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { isSafari } from "@/utils/baseFun";
export default defineComponent({
  name: "addToHomeScreen",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      btnShow: false,
      imgShow: false
    });

    if (isSafari()) {
      if ("standalone" in window.navigator && window.navigator.standalone) {
        state.btnShow = false
      }
      else {
        state.btnShow = true
      }
    }
    else state.btnShow = false;

    const btnClick = () => {
      state.imgShow = !state.imgShow
    }
    return { ...toRefs(state), store, t, btnClick };
  },
});
</script>
<style  lang="scss" scoped>
.addToHomeScreen {
  display: none;

  .btn {
    position: fixed;
    bottom: 90px;
    left: 50%;
    z-index: 40;
    transform: translateX(-50%);
    padding: 12px 47px;
    text-align: center;
    font-size: 13px;
    font-weight: bold;
    border-radius: 20px;
    white-space: nowrap;
    color: var(--theme-font-color-fff);
    // background: linear-gradient(to bottom, #000, var(--auxiliary-background-18));

    background: linear-gradient(180deg, rgba(0, 42, 81, 0.9) 0%, #3C88FB 100%);
  }

  .img_box {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 1000;
    background: rgba($color: #000000, $alpha: 0.5);

    img {
      position: absolute;
      bottom: 0;
      width: 100%;
    }
  }
}

@media (max-width: 768px) {
  .addToHomeScreen {
    display: block;
  }
}
</style>
