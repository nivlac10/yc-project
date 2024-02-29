<template>
  <div class="pagination">
    <div class="paging">
      <div class="prev" @click="pagingChange('prev')"><van-icon name="arrow-left" /></div>
      <div class="txt">{{ page }} / {{ totalPage }}</div>
      <div class="next" @click="pagingChange('next')"><van-icon name="arrow" /></div>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { debounce } from "@/utils/baseFun";

export default defineComponent({
  name: "about",
  props: {
    pageForm: {
      type: Object,
    },
  },
  setup(props, { emit }) {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      limit: props.pageForm?.limit, // 每页条数
      count: props.pageForm?.count, // 总条数
      page: props.pageForm?.page, // 当前页码
      totalPage: 0, // 总页码
    });

    watch(() => props.pageForm, (val: any) => {
      if (val.page != state.page) state.page = val.page
      if (val.count == 0) {
        state.totalPage = 1
      } else {
        if (val.count % state.limit == 0) {
          state.totalPage = val.count / state.limit;
        } else {
          state.totalPage = ((val.count - (val.count % state.limit)) / state.limit) + 1;
        }
      }
    }, { deep: true, immediate: true })

    const pagingChange = (val: string) => {
      const fun = () => {
        if (val == 'prev') {
          if (state.page <= 1) state.page = 1
          else {
            state.page -= 1
            emit('changePage', 'page', state.page)
          }
        } else {
          if (state.page >= state.totalPage) state.page = state.totalPage
          else {
            state.page += 1;
            emit('changePage', 'page', state.page)
          }
        }
      }
      debounce(fun)
    }

    return { ...toRefs(state), store, t, pagingChange };
  },
});
</script>
<style  lang="scss" scoped>
.pagination {
  padding: 10px 0;

  .paging {
    display: flex;
    justify-content: center;
    align-items: center;

    .prev,
    .next {
      cursor: pointer;
      padding: 10px;
      border-radius: 6px;
      background: #2D3144;

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

@media (max-width: 768px) {
  .pagination {
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
</style>
