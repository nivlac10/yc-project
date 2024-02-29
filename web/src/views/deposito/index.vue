<template>
  <div>
    <el-drawer v-model="showDeposito" direction="rtl" :size="size" :close-on-press-escape="false" @close="close">
      <template #header> </template>
      <div class="deposito">
        <div class="head">
          <img src="@/assets/images/deposito/home_nav_horn_icon@2x.png" alt="" />
          {{ t('deposito.DEPOSITO') }}
          <img src="@/assets/images/deposito/view_icon@2x.png" alt="" @click="close" />
        </div>
        <div class="body">
          <div v-if="list.length > 0">
            <el-collapse v-model="activeName" accordion>
              <el-collapse-item title="Consistency" name="1">
                <div>{{ t('deposito.p1') }}</div>
                <div>{{ t('deposito.p2') }}</div>
              </el-collapse-item>

            </el-collapse>
          </div>
          <div v-else class="nodate">{{ t("deposito.SEMMAIS") }}</div>
        </div>
        <div class="btns">
          <div class="btn del" @click="debounce(deletes, 1000)">
            {{ t("deposito.DELETE") }}
          </div>
          <div class="btn rev" @click="debounce(getData, 1000)">
            {{ t("deposito.RECEIVE") }}
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script lang="ts">
import { useI18n } from "vue-i18n";
import { ref, computed, watch, defineComponent, onMounted } from "vue";
import { useStore } from "@/store/index";
import { deposito } from "@/api/deposito";
import { debounce } from "@/utils/baseFun";
export default defineComponent({
  name: "deposito",
  setup() {
    const { t } = useI18n();
    const store = useStore();
    const showDeposito = computed(() => store.state.status.showDeposito);
    let size = ref(store.state.status.isPc ? "20%" : "70%");
    let list = ref([]);
    const activeName = ref('1')
    function close() {

      store.commit("status/setShowDeposito", false);
    }

    async function getData() {
      if (store.state.user.token) {
        debounce(async () => {
          // let a = await deposito.get_msg_list();
        }, 1000);
      }



    }
    // onMounted(() => {
    getData();
    // });


    async function deletes() {
      let a = await deposito.get_msg_list();
    }

    return { close, deletes, debounce, getData, t, list, showDeposito, size, activeName };
  },
});
</script>
<style lang="scss" scoped>
:deep(.el-overlay) {
  height: calc(100% - 80px);
  top: 80px;
}

:deep(.el-drawer__header) {
  display: none;
}

:deep(.el-drawer__body) {
  padding: 0 !important;
}

.deposito {
  height: 100%;
  width: 100%;

  .head {
    width: calc(100% - 28px);
    padding-left: 14px;
    padding-right: 14px;
    height: 44px;
    background: #855AF6;
    background-size: 100% 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;

    font-size: 20px;
    font-weight: bold;
    color: #fff;

    img {
      width: 35px;
      height: 35px;
    }
  }

  .body {
    width: 100%;
    height: calc(100% - 142px);
    background: var(--theme-box-background);

    .nodate {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      color: var(--auxiliary-font-color-9);
      font-size: 20px;
      font-weight: 600;
    }
  }

  .btns {
    width: 100%;
    height: 98px;
    background: #12151c;
    display: flex;
    align-items: center;
    justify-content: center;

    .btn {
      width: 138.96px;
      height: 37.15px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-weight: 600;
      font-size: 16px;
    }

    .del {
      background: url(@/assets/images/deposito/DELETE_icon@2x.png) no-repeat;
      background-size: 100% 100%;
      margin-left: 14px;
    }

    .rev {
      background: url(@/assets/images/deposito/Receive_btn@2x.png) no-repeat;
      background-size: 100% 100%;
    }
  }
}

@media (max-width: 768px) {
  :deep(.el-overlay) {
    height: calc(100% - 132px) !important;
  }

  :deep(.el-overlay) {
    height: calc(100% - 44px);
    top: 44px;
  }

  .deposito {
    .head {
      height: 36px !important;
      font-size: 15px !important;

      img {
        width: 24px !important;
        height: 24px !important;
      }
    }

    .body {
      height: calc(100% - 99px) !important;

      .nodate {
        font-size: 12.88px !important;
      }
    }

    .btns {
      height: 63px !important;

      .btn {
        font-size: 13px !important;
      }
    }
  }
}
</style>