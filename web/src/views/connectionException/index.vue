<template>
  <div class="connectionException">
    <div class="img">
      <img
        src="@assets/images/connectionException/Abnormal_connection.png"
        alt=""
      />
      <p>Uh oh ! Look like something broke.</p>
    </div>
    <div class="content">
      <div class="top_box">Possible Causes</div>
      <div class="txt_box">Your region is not supported</div>
    </div>
    <div class="btn">
      <div>
        <img src="@assets/images/public/logo.png" alt="" />
      </div>
      <div>
        <!-- <img src="@assets/images/public/customer_service.png" alt="" /> -->
        <!-- <span>LIVE SUPPORT</span> -->
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
export default defineComponent({
  name: "connectionException",
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
.connectionException {
  min-height: 100vh;
  background: var(--theme-box-background);
  .img {
    margin-bottom: 27px;
    text-align: center;
    img {
      width: 175px;
    }
    p {
      font-size: 32px;
      font-weight: bold;
      color: var(--theme-font-color-fff);
    }
  }
  .content {
    margin-bottom: 38px;
    font-size: 32px;
    font-weight: bold;
    .top_box {
      padding: 20px 0 20px 40px;
      color: var(--theme-font-color-fff);
      background: var(--auxiliary-background-19);
      border-radius: 16px 16px 0px 0px;
    }
    .txt_box {
      padding: 24px 0 190px 40px;
      color: var(--auxiliary-font-color-9);
      background: var(--auxiliary-background-17);
      border-radius: 0 0 16px 16px;
    }
  }
  .btn {
    display: flex;
    justify-content: space-between;
    div {
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100px;
    }
    // div:nth-child(1) {
    //   border-radius: 8px;
    //   background: var(--theme-button-background);
    //   img {
    //     width: 237px;
    //   }
    // }
    div:nth-child(2) {
      border-radius: 8px;

      width: 431px;
      height: 101px;
      background: #fbe852;
      box-shadow: inset 0px 12px 12px 0px rgba(245, 187, 86, 0.54),
        inset 14px -12px 12px 0px rgba(245, 187, 86, 0.58),
        inset -10px 0px 17px 0px rgba(245, 181, 86, 0.67),
        inset 0px -19px 24px 0px rgba(245, 181, 86, 0.25),
        inset 0px 5px 0px 0px #bf911b;
      img {
        // width: 237px;
      }
      span {
        font-size: 36px;
        font-weight: bold;
        color: #1b1d29;
      }
    }
  }
}

@media (max-width: 768px) {
}
</style>
