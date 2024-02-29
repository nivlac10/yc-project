<template>
  <div class="allRanks">
    <div class="close_btn" @click="back">
      <img src="@assets/images/vipBonus/Shut_down.png" alt="" />
    </div>
    <div class="title sl_font">{{ t("vipBonus.AllRanks") }}</div>
    <div class="list">
      <el-row :gutter="10">
        <el-col
          v-for="(item, index) in store.state.conf.all_conf.vip_conf"
          :key="item.vip_lv + index"
          :xs="24"
          :sm="6"
          :md="6"
          :lg="6"
          :xl="6"
        >
          <vip-box :data="item" />
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import vipBox from "../components/vipBox.vue";
export default defineComponent({
  name: "allRanks",
  components: { vipBox },
  setup() {
    const state = reactive({});
    const store = useStore();
    const { t } = useI18n();
    const router = useRouter();
    const back = () => {
      router.back();
    };
    return { ...toRefs(state), t, back, store };
  },
});
</script>
<style  lang="scss" scoped>
.allRanks {
  .close_btn {
    margin-top: 20px;
    cursor: pointer;
    display: flex;
    justify-content: flex-end;

    img {
      width: 42px;
    }
  }

  .title {
    margin-bottom: 42px;
    font-size: 30px;
    text-align: center;
    font-weight: bold;
  }

  .list {
    :deep(.el-row) {
      .el-col {
        margin-bottom: 26px;
      }
    }
  }
}

@media (max-width: 768px) {
  .close_btn {
    margin-right: -10px;
  }

  .allRanks {
    padding: 0 30px;
  }
}
</style>
