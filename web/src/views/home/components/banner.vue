<template>
  <div class="banner">
    <el-carousel :interval="4000" type="card" class="hidden-xs-only el-carousel_style">
      <el-carousel-item v-for="item in bannerList" :key="item">
        <div class="banner_box" :style="{ background: `url(${item['img_url']})` }" @click="jumpRoute(item)">
        </div>
      </el-carousel-item>
    </el-carousel>

    <van-swipe class="my-swipe" :autoplay="3000" indicator-color="white">
      <van-swipe-item v-for="item in bannerList" :key="item">
        <div class="banner_box" @click="jumpRoute(item)">
          <img :src="item['img_url']" alt="" />
        </div>
      </van-swipe-item>
    </van-swipe>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";
import { jumpRoute } from "@/utils/pageUtile";
export default defineComponent({
  name: "banner",
  setup() {
    const store = useStore();
    const state = reactive({
      bannerList: []

    });
    state.bannerList = store.state.conf.all_conf.banner as any
    return { ...toRefs(state), jumpRoute };
  },
});
</script>
<style  lang="scss" scoped>
.banner {
  padding: 60px 0 50px 0;

  .banner_box {
    overflow: hidden;
    border-radius: 10px;
    height: 100%;
    background-size: 100% 100% !important;
  }

  :deep(.el-carousel) {
    height: 256px;

    .el-carousel__container {
      height: 100%;
    }

    .el-carousel__item {
      img {
        width: 100%;
        height: 100%;
      }
    }

    .el-carousel__indicators {
      position: absolute;
      transform: translate(-50%, 0%);
      bottom: 10px;

      .el-carousel__indicator {
        .el-carousel__button {
          width: 10px;
          height: 10px;
          border-radius: 50%;
          background: var(--theme-font-color-fff);
        }
      }
    }
  }

  .my-swipe {
    display: none;
    height: 150px;

    img {
      width: 100%;
      height: 100%;
    }
  }
}

:deep(.van-swipe-item) {
  border-radius: 8px;
}

@media screen and (max-width: 768px) {
  .banner {
    padding: 12px 0;

    .my-swipe {
      display: block;
    }
  }
}
</style>
