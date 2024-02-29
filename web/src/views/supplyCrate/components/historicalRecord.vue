<template>
  <div class="historicalRecord">
      <div class="content_box">
        <!-- <img class="close_btn" src="@assets/images/public/popover_error_icon.png" alt="" @click="closeCom"> -->
        <!-- <div class="header">
          <img src="@assets/images/public/popover_return.png" alt="" @click="jump">
          <div class="title">
            {{ t('supplyCrate.HISTORICALRECORD') }}
          </div>
        </div> -->
        <div class="action_bar">
          <div>
            <!-- <select-box :options="options" @selectChange='selectChange' /> -->
          </div>
          <div class="quantity">
            <span>{{ t('supplyCrate.Quantity') }}</span>
            <span>{{ bonus }} {{ t('base.currency') }}</span>
          </div>
        </div>
        <div class="tab_column">
          <div>{{ t('supplyCrate.TIME') }}</div>
          <div>{{ t('supplyCrate.Bonus') }}</div>
        </div>
        <div class="list">
          <ul v-if="list && list.length > 0">
            <li v-for="(item, index) in (list as any)" :key="'i' + index">
              <div>{{ item.add_time }}</div>
              <div>{{ item.give_money }} {{ t('base.currency') }}</div>
            </li>
          </ul>
          <div class="no_data" v-else>{{ t('supplyCrate.NORECORD') }}</div>
        </div>
        <div class="paging">
          <div class="prev" @click="pagingChange('prev')"><van-icon name="arrow-left" /></div>
          <div class="txt">{{ currentPage + 1 }}/{{ limit == 0 ? 1 : limit }}</div>
          <div class="next" @click="pagingChange('next')"><van-icon name="arrow" /></div>
        </div>
      </div>
  
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import selectBox from "@/components/selectBox/selectBox.vue";
import { sliceArr } from "@/utils/baseFun";
import { UserService } from "@/api/user";
export default defineComponent({
  name: "historicalRecord",
  components: { selectBox },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({

      options: [
        { label: 'Today', value: 0, },
        { label: 'Yesterday', value: 1, },
        { label: '7 Day', value: 2, },
        { label: '15 Day', value: 3, },
        { label: '30 Day', value: 4, },
      ],
      bonus: 0,
      list: [],
      limit: 0,
      currentPage: 0,
    });
    const closeCom = () => {
      store.dispatch('status/setSupplyCrateShow', false)
    }
    const jump = () => {
      proxy.$mitt.emit("supplyCrateComShow", 0)
    }

    const selectChange = (item) => {
    }

    UserService.get_loss_receive_record().then(res => {
      state.bonus = res.data.bonus
      state.list = res.data.data
      pagingChange('prev')
    })

    const pagingChange = (val: string) => {
      let arr2 = sliceArr([...state.list], 10)
      state.limit = arr2.length
      if (val == 'prev') {
        if (state.currentPage <= 0) state.currentPage = 0
        else state.currentPage -= 1
      } else {
        if (state.currentPage >= state.limit - 1) state.currentPage = state.limit - 1
        else state.currentPage += 1
      }
      state.list = arr2[state.currentPage]
    }

    return { ...toRefs(state), store, t, jump, selectChange, pagingChange, closeCom };
  },
});
</script>
<style  lang="scss" scoped>
.historicalRecord {
  .content_box {
    position: relative;
    // padding: 56px 28px 40px 28px;
    width: 100%;
    border-radius: 16px;
    background: var(--theme-box-background);
    box-sizing: border-box;

    .close_btn {
      cursor: pointer;
      position: absolute;
      top: 23px;
      right: 28px;
      width: 25px;
    }

    .header {
      display: flex;
      align-items: center;
      margin-bottom: 25px;

      img {
        cursor: pointer;
        margin-right: 15px;
        width: 30px;
      }

      .title {
        font-size: 26px;
        font-weight: bold;
        color: var(--auxiliary-font-color-18);
      }
    }

    .action_bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      .quantity {
        font-size: 17px;
        font-weight: bold;

        span:nth-child(1) {
          margin-right: 9px;
          color: var(--auxiliary-font-color-9);
        }

        span:nth-child(2) {
          color: var(--auxiliary-font-color-7);
        }
      }
    }

    .tab_column {
      display: flex;
      justify-content: space-between;
      margin-bottom: 6px;
      padding: 10px 0;
      background: var(--auxiliary-background-14);
      border-radius: 8px 8px 0px 0px;

      div {
        width: 100%;
        font-size: 20px;
        font-weight: 500;
        color: var(--auxiliary-font-color-9);
        text-align: center;
      }
    }

    .list {
      position: relative;
      min-height: 312px;
      margin-bottom: 16px;
      background: var(--auxiliary-background-14);
      border-radius: 0px 0px 8px 8px;

      ul {
        position: relative;
        z-index: 10;
        padding: 16px;
        min-height: 312px;

        li {
          display: flex;
          justify-content: space-between;
          margin-bottom: 15px;

          &:nth-last-child(1) {
            margin-bottom: 0;
          }

          div {
            font-size: 14px;
            font-weight: 500;
            color: var(--auxiliary-font-color-9);
            text-align: left;
          }

          div:nth-child(1) {
            width: 100%;
          }

          div:nth-child(2) {
            width: 40%;
            color: var(--auxiliary-font-color-7);
            text-align: left;
          }
        }
      }

      .no_data {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 18px;
        font-weight: bold;
        color: var(--auxiliary-font-color-9);
      }
    }

    .paging {
      display: flex;
      justify-content: center;
      align-items: center;

      .prev,
      .next {
        cursor: pointer;
        padding: 10px;
        border-radius: 6px;
        background: var(--auxiliary-background-21);

        :deep(.van-icon) {
          font-weight: bold;
          color: var(--auxiliary-font-color-9);
        }
      }

      .txt {
        padding: 0 22px;
        font-size: 18px;
        color: var(--auxiliary-font-color-9);
        font-weight: bold;
      }
    }
  }
}

@media (max-width: 768px) {
  .historicalRecord {
    .content_box {
      padding: 36px 20px 20px 20px;
      border-radius: 0;

      .close_btn {
        top: 14px;
        right: 19px;
        width: 18px;
      }

      .header {
        display: flex;
        align-items: center;
        margin-bottom: 10px;

        img {
          cursor: pointer;
          margin-right: 8px;
          width: 30px;
        }

        .title {
          font-size: 17px;
        }
      }

      .action_bar {
        .quantity {
          font-size: 12px;
        }
      }

      .tab_column {
        div {
          font-size: 14px;
        }
      }

      .list {
        min-height: 200px;

        ul {
          position: relative;
          z-index: 10;
          padding: 16px;
          min-height: 200px;

          li {
            margin-bottom: 10px;

            div {
              font-size: 12px;
            }
          }
        }

        .no_data {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          font-size: 18px;
          font-weight: bold;
          color: var(--auxiliary-font-color-9);
        }
      }

      .paging {
        display: flex;
        justify-content: center;
        align-items: center;

        .prev,
        .next {
          cursor: pointer;
          padding: 6px;
        }

        .txt {
          font-size: 14px;
        }
      }
    }
  }
}
</style>
