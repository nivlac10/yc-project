<template>
  <div class="gameColumn hidden-xs-only">
    <div class="left_box">
      <div :class="{ box: true, active: activeIdx == index }" v-for="(item, index) in columnList" :key="index"
        @click="tabChange(item, index), activeIdx = index">
        <img :src="item.img" alt="" />
        <span>{{ item.title }}</span>
        <div class="number_box" v-if="activeIdx == index && item.num">
          <span>{{ item.num }}</span>
        </div>
      </div>
    </div>
    <div class="slelct_max_box">
      <div class="slelct_left_box">
        <noticVant v-if="props.pageData.isHome"></noticVant>
        <changeGameListDataType v-else @def="changeGameListDataType" :gameListType="props.pageData.gameListType" />
      </div>
      <div class="right_box">
        <factorySelect @def="changeFactory"></factorySelect>
        <searchGameName @def="changeGameName"></searchGameName>
      </div>
    </div>
  </div>

  <div class="phone_box">
    <div class="phone_column_box">
      <noticVant v-if="props.pageData.isHome"></noticVant>
      <changeGameListDataType v-else @def="changeGameListDataType" />
      <div class="demo-collapse-coumn">
        <el-collapse v-model="activeName" accordion>
          <el-collapse-item title="Casion" name="1">
            <template #title>
              <div class="select_box">
                <div class="selected_column">
                  <div class="l_box">
                    <img :src="columnList[activeIdx].img" alt="" />
                    <span>{{ columnList[activeIdx].title }}</span>
                  </div>
                </div>
              </div>
            </template>
            <div class="list" style="margin-top: 20px">
              <div class="tab_list">
                <ul>
                  <li v-for="(item, index) in columnList" :key="index" :class="{ active_tab: activeIdx == index }"
                    @click="tabChange(item, index), (activeName = 'activeName')">
                    <img :src="item.img" alt="" />
                    <span>{{
                      item.title
                    }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
      <factorySelect @def="changeFactory"></factorySelect>
      <searchGameName @def="changeGameName"></searchGameName>
    </div>
  </div>
</template>
<script>
import { reactive, toRefs, getCurrentInstance, defineComponent, computed, watch } from "vue";
import { useStore } from "@/store/index";
import { getImageUrl } from "@/utils/baseFun";
import { get_game_data } from "@/utils/gameUtils";
import noticVant from "@/components/noticVant/index.vue"
import changeGameListDataType from "@/components/changeGameListDataType/index.vue"
import factorySelect from "@/components/factorySelect/index.vue"
import searchGameName from "@/components/searchGameName/index.vue"
import { useI18n } from "vue-i18n";

export default defineComponent({
  name: "gameColumn",
  components: {
    noticVant,
    changeGameListDataType,
    factorySelect,
    searchGameName
  },
  props: {
    pageData: {
      type: Object,
    },
    index: {
      type: String
    }
  },
  setup(props, { emit }) {
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      activeIdx: 0,
      columnList: [
        {
          img: getImageUrl("home/home_Classification_LOBBY_icon@3x.png"),
          title: computed(() => t('gameType.Salão')),
          num: get_game_data(null, null, null, 0, 0, 0, 0, 0).count,
          type: null,
          is_home: true,
          is_tag: 0,
          is_top: 0,
          is_hot: 0
        },
        {
          img: getImageUrl("home/home_Classification_tiny spot_icon@3x.png"),
          title: computed(() => t('gameType.Coletar')),
          num: 0,
          type: null,
          is_home: false,
          is_tag: 1
        },
        {
          img: getImageUrl("home/home_Classification_777_icon.png"),
          title: computed(() => t('gameType.Slot')),
          num: get_game_data(null, 0, null, 0, 0, 0, 0, 0).count,
          type: 0,
          is_home: false,
          is_tag: 0
        },
        {
          img: getImageUrl("home/home_live.png"),
          title: computed(() => t('gameType.AoVivo')),
          num: get_game_data(null, 2, null, 0, 0, 0, 0, 0).count,
          type: 2,
          is_home: false,
          is_tag: 0
        },
        {
          img: getImageUrl("home/home_Classification_fish_icon@3x.png"),
          title: computed(() => t('gameType.Pescaria')),
          num: get_game_data(null, 3, null, 0, 0, 0, 0, 0).count,
          type: 3,
          is_home: false,
          is_tag: 0
        },
        {
          img: getImageUrl("home/home_Classification_TABLE_icon@3x.png"),
          title: computed(() => t('gameType.JogosMesa')),
          num: get_game_data(null, 1, null, 0, 0, 0, 0, 0).count,
          type: 1,
          is_home: false,
          is_tag: 0
        },
      ],
      activeName: "0",
      pageData: {
        game_id: null,
        isHome: true,
        game_type: null,
        is_tag: 0,
        game_name: null,
        is_top: 0,
        is_hot: 0,
      }
    });
    watch(() => props.index, () => {

      state.activeIdx = props.index
    }, {
      deep: true
    }
    )
    const tabChange = (item, index) => {
      state.activeIdx = index;
      props.pageData.isHome = item.is_home
      props.pageData.is_tag = item.is_tag
      props.pageData.game_type = item.type
      if (index == 1) {
        item.num = get_game_data(null, null, null, null, 0, 1, 0, 0).count
      }
      changeData()
    };
    // 
    const changeGameName = (v) => {
      if (v) {
        props.pageData.isHome = false
        props.pageData.game_name = v
      } else {
        props.pageData.game_name = null
        if (state.activeIdx == 0) {
          props.pageData.isHome = true
        }
      }
      emit("def", props.pageData)
    }
    // 切换厂商
    const changeFactory = (item) => {
      props.pageData.game_id = item.game_id;
      if (item.game_id == null && state.activeIdx == 0) {

        props.pageData.isHome = true
      } else {

        props.pageData.isHome = false
      }
      changeData()
    };
    const changeData = () => {
      let data = props.pageData
      emit("def", data)
    }
    const changeGameListDataType = (index) => {
      switch (index) {
        case 0:
          props.pageData.is_hot = 0
          props.pageData.is_top = 0
          break;
        case 1:
          props.pageData.is_hot = 1
          props.pageData.is_top = 0
          break;
        case 2:
          props.pageData.is_hot = 0
          props.pageData.is_top = 1
          break;
        default:
          break;
      }
      emit("def", props.pageData)
    }
    return { ...toRefs(state), tabChange, changeFactory, changeGameListDataType, changeGameName, props };
  },
});
</script>
<style  lang="scss" scoped>
.slelct_max_box {
  display: flex;
  justify-content: space-between;
  gap: 10px;

  .slelct_left_box {
    width: 50%;
  }

  .right_box {
    width: 50%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    column-gap: 10px;

  }
}

.gameColumn {
  display: flex;
  flex-direction: column;
  gap: 10px;

  .left_box {
    display: flex;
    align-items: center;
    border-radius: 13px;

    background: var(--theme-navigationbar-background);
    // height: 100%;

    .box {
      // height: 100%;
      cursor: pointer;
      display: flex;

      align-items: center;
      // margin-right: 30px;  
      padding: 10px 20px;

      border-radius: 13px;
      gap: 10px;

      &.active {
        // background-color: ;
        background-image: linear-gradient(#222230, #312851, #553E94);
      }

      .number_box {
        background-color: #fff;
        padding: 2px 10px;
        border-radius: 5px;

        span {
          font-size: 14px !important;
          font-weight: 600 !important;
          color: var(--auxiliary-background-18) !important;
        }
      }

      img {
        width: 40px;
      }

      span {
        // margin-left: 4px;
        font-size: 17px;
        color: var(--theme-font-color-fff);
        margin-bottom: -3px;
      }
    }
  }
}



.phone_box {
  display: none;

  .phone_column_box {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .demo-collapse-coumn {
    // margin-bottom: 12px;

    :deep(.el-collapse) {
      border: none;
      background: var(--theme-button-background);
      border-radius: 8px;

      .el-collapse-item__header {
        height: 42px;
        background: transparent;
        border: none;
        font-size: 18px;
        color: var(--theme-font-color-fff);
        align-items: center;

        .el-collapse-item__arrow {
          font-size: 20px;
          font-weight: bold;
          color: var(--auxiliary-font-color-1);
        }
      }

      .el-collapse-item__wrap {
        background: transparent;
        border: none;
      }
    }

    .tab_list {

      ul {
        padding: 10px;
        display: flex;
        flex-direction: column;
        gap: 5px;

        li {
          display: flex;
          align-items: center;
          // width: 100%;
          border-radius: 8px;
          padding: 5px;
          gap: 10px;

          &.active_tab {
            background-color: var(--theme-box-background);
          }

          img {
            // margin-right: 9px;
            // width: 40px;
            width: 30px;
          }

          span {
            color: var(--auxiliary-font-color-9);
          }
        }
      }
    }
  }



  .select_box {
    width: 100%;
    border-radius: 8px;

    .selected_column {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 14px;
      // background: var(--auxiliary-background-6);
      border-radius: 8px;
      height: 100%;
      width: 100%;
      background-image: linear-gradient(#222230, #312851, #553E94);

      .l_box {
        display: flex;
        align-items: center;
        height: 42px;
        gap: 10px;

        img {
          width: 30px;
        }

        span {
          font-size: 14px;
          font-weight: 500;
          // margin-bottom: -3px;
        }
      }

      .r_box {}
    }
  }
}

@media screen and (max-width: 768px) {
  .search_box {
    background: var(--auxiliary-background-6);
    border-radius: 8px;

    :deep(.el-input) {
      width: 100%;
      height: 42px;

      .el-input__inner {
        border: none;
      }
    }
  }

  .phone_box {
    display: block;
  }
}
</style>
