<template>
  <div class="activityPopup">
    <el-dialog
      v-model="dialogVisible"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <!-- :width="store.state.status.isPc ? '757px' : '100%'" -->
      <div class="activityPopup_content">
        <img
          class="content_img"
          :src="currentData['img_url']"
          alt=""
          @click.stop="
            jumpRoute(currentData),
              (dialogVisible = false),
              (store.state.status.announcementShow = false)
          "
        />
        <img
          class="close_img"
          src="@assets/images/public/Off_b.png"
          alt=""
          @click.stop="popupCloseClick"
        />
      </div>
    </el-dialog>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { getCookie, getImageUrl, setcookie } from "@/utils/baseFun";
import { jumpRoute } from "@/utils/pageUtile";

export default defineComponent({
  name: "activityPopup",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      dialogVisible: true,
      list: store.state.conf.all_conf.san_plate_alert_list,
      currentData: {},
      currentIdx: 0,
    });

    // 关闭按钮操作
    const popupCloseClick = () => {
      if (state.currentIdx >= state.list.length) return (state.dialogVisible = false);
      getData();
    };

    const getData = () => {
      if (state.list.length > 0) {
        state.dialogVisible = true;
      } else {
        state.dialogVisible = false;
        return;
      }

      // 获取当前数据
      state.currentData = state.list[state.currentIdx];
      state.currentIdx += 1;

      // 判断用户是否充值
      if (state.currentData["user_type"] == 1) {
        if (store.state.user.token) {
          if (store.state.user.first_pay_type != 1) {
            state.currentData = {};
            popupCloseClick();
            return;
          }
        }
      }

      // 判断是否当天内显示一次
      if (state.currentData["close_type"] == 1) {
        if (!getCookie(`activityPopup${state.currentData["id"]}`)) {
          // 当天剩余时间 分钟
          const time = (
            (new Date(new Date().setHours(23, 59, 59, 999)).getTime() -
              new Date().getTime()) /
            1000 /
            60
          ).toFixed(0);
          setcookie(`activityPopup${state.currentData["id"]}`, true, time);
        } else {
          state.currentData = {};
          popupCloseClick();
        }
      }
    };
    getData();

    return { ...toRefs(state), store, t, popupCloseClick, jumpRoute };
  },
});
</script>
<style lang="scss" scoped>
.activityPopup {
  .activityPopup_content {
    img {
      cursor: pointer;
      margin: 0 auto;
      display: block;
    }

    .content_img {
      width: 416px;
      margin-bottom: 39px;
    }

    .close_img {
      width: 34px;
    }
  }
}

@media (max-width: 768px) {
  .activityPopup {
    .activityPopup_content {
      .content_img {
        width: 301px;
        margin-bottom: 20px;
      }

      .close_img {
        width: 30px;
      }
    }
  }
}
</style>
