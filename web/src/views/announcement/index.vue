<template>
  <div class="announcement">
    <el-dialog v-model="dialogVisible" :show-close="false" :close-on-press-escape="false"
      :width="store.state.status.isPc ? '757px' : '100%'" @close="store.state.status.announcementShow = false">
      <div class="dialog_content">
        <div class="close_box" @click="store.state.status.announcementShow = false">
          <img class="close_img" src="@assets/images/public/Shutdownx.png" alt="">
        </div>
        <div class="column_title">{{ t('bonusCabinet.ATIVIDADESDIÁRIAS') }}</div>
        <el-carousel class="el-carousel_style" arrow="always" :autoplay="false"
          :height="store.state.status.isPc ? '157px' : '130px'">
          <el-carousel-item v-for="(item) in (activity as any)" :key="item">
            <div class="img_box">
              <img v-for="(item2) in item" :key="item2" :src="item2.img_url" alt=""
                @click="jumpRoute(item2), dialogVisible = false">
            </div>
          </el-carousel-item>
        </el-carousel>
        <div class="column_title">{{ t('announcement.AVISOSDOSISTEMA') }}</div>
        <div class="txt_content_box">
          <div class="txt_content">
            <div v-for="(item, index) in (notice_list as any)" :key="item">
              <div class="txt_content_title">{{ item.title }}</div>
              <!-- <div class="txt_content_title2">【{{ item.title }}】</div> -->
              <div class="txt_content_h">
                <!-- {{ item.info }} -->
                <div v-html="item.info"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="all_btn">
          <span @click="jump">{{ t('sidebar.TodososBônus') }}</span>
          <img src="@assets/images/public/arrow_blue.png" alt="">
        </div>
      </div>
    </el-dialog>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { sliceArr } from "@/utils/baseFun";
import { jumpRoute } from "@/utils/pageUtile";

export default defineComponent({
  name: "announcement",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      dialogVisible: store.state.status.announcementShow,
      activity: [],
      notice_list: [],
    });

    //  活动
    state.activity = sliceArr(store.state.conf.all_conf.banner, store.state.status.isPc ? 2 : 1)
    // 公告
    state.notice_list = store.state.conf.all_conf.notice_list as never

    const jump = () => {
      router.push('/TodosOsBouns')
      store.state.status.announcementShow = false
    }

    return { ...toRefs(state), store, t, jumpRoute, jump };
  },
});
</script>
<style  lang="scss" scoped>
.announcement {
  .dialog_content {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 100%;
    padding: 26px 16px 15px 16px;
    background: #202431;
    border-radius: 12px;
    box-sizing: border-box;

    .close_box {
      position: absolute;
      top: 15px;
      right: 17px;
      width: 30px;
      height: 30px;
      display: flex;
      align-items: center;
      justify-content: center;

      .close_img {
        cursor: pointer;
        width: 20px;
      }
    }

    .column_title {
      padding-left: 10px;
      font-size: 18px;
      font-weight: 600;
      color: #B2B6C5;
    }

    .img_box {
      display: flex;
      gap: 17px;
      height: 100%;

      img {
        display: block;
        width: 50%;
        border-radius: 12px;
      }
    }

    .txt_content_box {
      padding: 24px 6px 24px 26px;
      background: #2F3445;
      border-radius: 12px;
      box-sizing: border-box;
    }

    .txt_content {
      display: flex;
      flex-direction: column;
      gap: 20px;
      height: 254px;
      overflow-y: scroll;

      &::-webkit-scrollbar {
        display: block;
      }

      .txt_content_title {
        margin-bottom: 12px;
        font-size: 16px;
        font-weight: 600;
        color: #F3B343;
      }

      .txt_content_title2 {
        margin-bottom: 24px;
        font-size: 16px;
        color: #C3CFD9;
      }

      .txt_content_h {
        // line-height: 20px;
        // font-size: 14px;
        // color: #fff;
        // word-break: break-word;
        // white-space: pre-line;
      }
    }

    .all_btn {
      display: flex;
      align-items: center;
      justify-content: center;

      span {
        cursor: pointer;
        margin-right: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #4181EE;
      }

      img {
        width: 19px;
      }
    }
  }
}

@media (max-width: 768px) {
  .announcement {
    .dialog_content {
      margin: 0 20px;
      gap: 12px;
      padding: 19px 7px 13px 7px;

      .close_box {
        position: absolute;
        top: 0px;
        right: 0px;
        width: 45px;
        height: 45px;

        .close_img {
          width: 15px;
        }
      }

      .column_title {
        padding-left: 8px;
        font-size: 14px;
      }

      :deep(.el-carousel_style .el-carousel__container) {
        border-radius: 8px;
      }

      .img_box {
        gap: 0px;
        height: 100%;

        img {
          width: 100%;
          border-radius: 8px;
        }
      }

      .txt_content_box {
        padding: 18px 5px 18px 11px;
        border-radius: 8px;
      }

      .txt_content {
        height: 216px;

        .txt_content_title {
          margin-bottom: 8px;
          font-size: 13px;
        }

        .txt_content_title2 {
          margin-bottom: 16px;
          font-size: 12px;
        }

        .txt_content_h {
          line-height: 18px;
          font-size: 12px;
        }
      }

      .all_btn {
        span {
          margin-right: 5px;
          font-size: 12px;
        }

        img {
          width: 15px;
        }
      }
    }
  }
}
</style>
