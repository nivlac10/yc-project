<template>
  <div class="downloadApp" v-if="show && !store.state.status.isApk && isApp == 'false'">
    <!-- <div class="l_box">
      <div>
        <img src="@assets/72.png" alt="">
      </div>
      <div>
        <div class="logo_t">
          <img src="@assets/images/download/Group.png" alt="">
        </div>
        <div class="star">
          <img v-for="(index) in 5" :key="index" src="@assets/images/download/Star.png" alt="">
        </div>
      </div>
    </div>
    <div class="r_box">
      <a class="btn" :href="store.state.conf.all_conf.android_url + 'bigwin777-c13.apk'">Baixar <span>+R$ 2</span></a>
      <img src="@assets/images/public/Off.png" alt="" @click="show = false">
    </div> -->
    <img
      src="@/assets/images/download/Capsulediagram.png"
      alt=""
      class="downloadImg"
      @click="download()"
    />
    <img
      src="@/assets/images/download/Off.png"
      alt=""
      class="close"
      @click="show = false"
    />
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { downloadAPK } from "@/utils/baseFun";
export default defineComponent({
  name: "downloadApp",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      show: true,
      isApp: null,
    });
    function download() {
      downloadAPK();
    }
    state.isApp = localStorage.getItem("isApp") as any;
    return { ...toRefs(state), store, t, download };
  },
});
</script>
<style lang="scss" scoped>
.downloadApp {
  position: fixed;
  z-index: 5;
  left: 0;
  bottom: 65px;
  display: flex;
  justify-content: space-between;
  padding: 0px 10px;
  width: 100%;
  box-sizing: border-box;
  // background: url(@/assets/images/download/backdrop.png) no-repeat;
  // background: url(@/assets/images/download/Capsulediagram.png) no-repeat;
  background-size: 100% 100%;
  .close {
    position: absolute;
    top: -20px;
    left: 23px;
    width: 20px;
  }
  .downloadImg {
    width: 100%;
    // height: ;
  }

  .l_box {
    display: flex;

    div:nth-child(1) {
      margin-right: 4px;

      img {
        width: 40px;
        border-radius: 8px;
      }
    }

    div:nth-child(2) {
      .logo_t {
        img {
          width: 86px;
        }
      }

      .star {
        img {
          margin-right: 5px;
          width: 10px;
        }
      }
    }
  }

  .r_box {
    display: flex;
    align-items: center;

    .btn {
      margin-right: 10px;
      padding: 10px 24px;
      font-size: 16px;
      font-weight: 500;
      color: var(--theme-font-color-fff);
      background: #d9384e;
      border-radius: 20px;
      span {
        color: #fff500;
        font-weight: 600;
      }
    }

    img {
      width: 18px;
      height: 18px;
    }
  }
}

@media (max-width: 768px) {
}
</style>
