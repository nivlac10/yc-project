<template>
  <div class="gameList">
    <div class="sl_font">{{ f_data.game_name }} {{ t('gameText.Jogos') }}</div>
    <div class="gameList_column">
      <saerchGameName @def="changeGameName"> </saerchGameName>

      <!-- <div class="el-select_style">
        <el-select v-model="type" :teleported="false" :popper-append-to-body="false">
          <el-option label="ALL" value="0" />
          <el-option label="Alphabetical A-Z" value="1" />
          <el-option label="Alphabetical Z-A" value="2" />
        </el-select>
      </div> -->
    </div>
    <gameList :gameList="gameList" @def="loadMore"></gameList>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "@/store/index";
import selectBox from "./selectBox.vue";
import saerchGameName from "@/components/searchGameName/index.vue"
import gameList from "@/components/gameList/index.vue";
import { get_game_data, get_game_data_by_game_id, get_game_list_by_f_name } from "@/utils/gameUtils";
import factorySelect from "@/components/factorySelect/index.vue";
import { debounce } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";

export default defineComponent({
  name: "gameList",
  components: { selectBox, gameList, factorySelect, saerchGameName },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const route = useRoute();
    const state = reactive({
      type: "shanghai",
      searchVal: '',
      gameList: [],
      game_id: 0,
      page: 1,
      limit: 24,
      f_data: {
        game_name: ""
      },
      game_name: null,

    });
    state.game_id = route.params.game_id as any
    // @ts-ignore
    state.f_data = get_game_data_by_game_id(state.game_id)
    function loadMore() {
      let data = get_game_data(state.game_id, null, state.game_name, null, null, null, state.page, state.limit).allGameList as any;
      state.page += 1;
      for (let i = 0; i < data.length; i++) {
        // @ts-ignore
        state.gameList.push(data[i])

      }
      state.searchVal = '';

    }
    loadMore()
    const changeGameName = (v: any) => {
      state.page = 1
      state.gameList = []
      if (v) {
        state.game_name = v
      } else {
        state.game_name = null
      }
      loadMore()
    }
    return { ...toRefs(state), t, store, loadMore, changeGameName };
  },
});
</script>
<style  lang="scss" scoped>
.gameList {
  .back {
    display: none;
    padding-top: 15px;

    div {
      cursor: pointer;
      padding: 8px 11px;
      background: var(--theme-navigationbar-background);
      color: var(--auxiliary-font-color-9);
      font-size: 12px;
      border-radius: 8px;
    }
  }

  .sl_font {
    padding: 40px 0 30px 0;
    font-size: 34px;
    font-weight: bold;
  }

  .gameList_column {
    display: flex;
    gap: 20px;

    >div:nth-child(1) {
      width: 100%;
    }

    >div:nth-child(2) {
      width: 20%;
    }

    .search_box {
      position: relative;

      img {
        position: absolute;
        top: 50%;
        transform: translate(0, -50%);
        left: 13px;
      }

      :deep(.el-input) {
        height: 42px;

        .el-input__wrapper {
          padding: 0;
          background: transparent;
          box-shadow: none;
        }

        .el-input__inner {
          height: 100%;
          padding-left: 50px;
          background: transparent;
          border: 2px solid #585e77;
          border-radius: 12px;
          color: var(--theme-font-color-fff);
        }
      }
    }
  }




}

@media (max-width: 768px) {
  .gameList {
    .back {
      display: flex;
    }

    .sl_font {
      padding: 15px 0 18px 0;
      font-size: 16px;
      // color: var(--theme-font-color-fff) !important;
      // text-shadow: none !important;
    }

    .gameList_column {
      display: flex;
      gap: 10px;

      >div:nth-child(1) {
        // width: 70%;
      }

      >div:nth-child(2) {
        width: 30%;
      }

      .search_box {
        position: relative;

        img {
          z-index: 1;
          width: 24px;
        }

        :deep(.el-input) {
          height: 30px;

          .el-input__wrapper {}

          .el-input__inner {
            height: 100%;
            padding-left: 50px;
            background: transparent;
            border: none;
            border-radius: 8px;
            color: var(--theme-font-color-fff);
            background: var(--theme-box-background);

            &::placeholder {
              font-size: 12px;
            }
          }
        }
      }

      .el-select_style {
        :deep(.el-input__inner) {
          --el-input-inner-height: calc(30px);
        }
      }
    }

    .loadMore {
      div {
        cursor: pointer;
        padding: 14px 45px;
        font-size: 16px;
      }
    }


  }
}
</style>
