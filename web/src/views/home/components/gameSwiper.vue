<template>
  <div class="gameSwiper">
    <div class="game_swiper_head">
      <div class="s_left" v-if="props.listType == 1">
        <img src="@/assets/images/home/TOP_icon@3x.png" alt="" />
        <span>{{ t('gameText.Topo') }}</span>
      </div>
      <div class="s_left" v-if="props.listType == 2">
        <img src="@/assets/images/home/HOT_icon@3x.png" alt="" />
        <span>{{ t('gameType.Popular') }}</span>
      </div>
      <div class="s_left" v-if="props.listType == 3">
        <img src="@/assets/images/home/home_Classification_fish_icon@3x.png" alt="" />
        <span>{{ t('gameType.Pescaria') }}</span>
      </div>
      <div class="s_left" v-if="props.listType == 4">
        <img src="@/assets/images/home/home_Classification_TABLE_icon@3x.png" alt="" />
        <span>{{ t('gameType.JogosMesa') }}</span>
      </div>
      <div class="s_left" v-if="props.listType == 5">
        <img src="@/assets/images/home/home_live.png" alt="" />
        <span>{{ t('gameType.AoVivo') }}</span>
      </div>
      <div class="s_left" v-if="props.listType == 6">
        <img src="@/assets/images/home/home_Classification_777_icon.png" alt="" />
        <span>{{ t('gameType.Slot') }}</span>
      </div>
      <div class="s_right">
        <div class="view_all" @click="changeHomeData">{{ t('home.Viewall') }}</div>
        <div class="btn">
          <div class="btn_c" @click="prevSwiper">
            <svg viewBox="64 64 896 896" focusable="false" data-icon="left" width="1em" height="1em" fill="currentColor"
              aria-hidden="true">
              <path
                d="M724 218.3V141c0-6.7-7.7-10.4-12.9-6.3L260.3 486.8a31.86 31.86 0 000 50.3l450.8 352.1c5.3 4.1 12.9.4 12.9-6.3v-77.3c0-4.9-2.3-9.6-6.1-12.6l-360-281 360-281.1c3.8-3 6.1-7.7 6.1-12.6z">
              </path>
            </svg>
          </div>
          <div class="btn_c" @click="nextSwiper">
            <svg viewBox="64 64 896 896" focusable="false" data-icon="right" width="1em" height="1em" fill="currentColor"
              aria-hidden="true">
              <path
                d="M765.7 486.8L314.9 134.7A7.97 7.97 0 00302 141v77.3c0 4.9 2.3 9.6 6.1 12.6l360 281.1-360 281.1c-3.9 3-6.1 7.7-6.1 12.6V883c0 6.7 7.7 10.4 12.9 6.3l450.8-352.1a31.96 31.96 0 000-50.4z">
              </path>
            </svg>
          </div>
        </div>
      </div>
    </div>
    <swiper :loop="true" class="mySwiper" @swiper="onSwiper" @slideChange="onSlideChange" style="" effect="fade">
      <swiper-slide v-for="(item, i) in game_list" class="swper_list_box">
        <gameBox v-for="game in item" :data="game" class="game_box"></gameBox>
      </swiper-slide>
    </swiper>
  </div>
</template>
<script lang="ts">
import {
  reactive,
  toRefs,
  getCurrentInstance,
  defineComponent,
  ref,
  onMounted,
} from "vue";
import { useStore } from "@/store/index";
import gameBox from "./gameBox.vue";
import { Swiper, SwiperSlide } from 'swiper/vue';
import { get_game_data } from "@/utils/gameUtils";
import 'swiper/css';
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "gameSwiper",
  components: {
    gameBox,
    Swiper,
    SwiperSlide
  },
  props: {
    listType: {
      type: Number,
      default: 1,
    },
  },

  setup(props, { emit }) {
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      setActiveItem: 2,
      game_list: [],
      game_count: 0,
      swiperDom: null,
      swiperIndex: 0,
    });
    // 获取数据  数组切割
    function gameData() {
      let game_data: any = [];
      let limit = store.state.status.isPc ? 12 : 6;
      if (props.listType == 1) {
        game_data = get_game_data(null, null, null, 1, null, null, 1, 24) as never;
      }
      if (props.listType == 2) {
        game_data = get_game_data(null, null, null, null, 1, null, 1, 24) as never;
      }
      if (props.listType == 3) {
        game_data = get_game_data(null, 3, null, null, null, null, 1, 24) as never;
      }
      if (props.listType == 4) {
        game_data = get_game_data(null, 1, null, null, null, null, 1, 24) as never;
      }
      if (props.listType == 5) {
        game_data = get_game_data(null, 2, null, null, null, null, 1, 24) as never;
      }
      if (props.listType == 6) {
        game_data = get_game_data(null, 0, null, null, null, null, 1, 24) as never;
      }
      // console.log(game_data);

      let count = game_data.allGameList.length / limit;
      let page = 0;
      for (let i = 0; i < count; i++) {
        let new_arr = [];
        let offset = page * limit;
        for (let j = 0; j < game_data.allGameList.length; j++) {
          if (offset <= j && j < offset + limit) {
            new_arr.push(game_data.allGameList[j] as never);
          }
        }
        page++;
        state.game_list.push(new_arr as never);
      }
    }
    gameData();
    let _this: any = "";
    let carousel = ref(null);

    const onSwiper = (swiper) => {
      state.swiperDom = swiper;
      // console.log(swiper);
    };
    const onSlideChange = () => {
    };
    // 上一页
    const nextSwiper = () => {
      // @ts-ignore
      state.swiperDom.slideNext();
    }
    const prevSwiper = () => {
      // @ts-ignore
      state.swiperDom.slidePrev();

    }
    const changeHomeData = () => [
      emit("def")
    ]
    return { ...toRefs(state), onSwiper, onSlideChange, prevSwiper, nextSwiper, props, changeHomeData, t };
  },
});
</script>
<style  lang="scss" scoped>
// }50px
@media (max-width: 750px) {
  .swper_list_box {
    grid-template-columns: repeat(3, 1fr) !important;
  }

  .game_max_box {
    display: grid;
    grid-template-columns: repeat(3, 1fr) !important;
  }
}

.game_max_box {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  column-gap: 10px;
  width: 100%;
}

:deep(.swiper-wrapper) {
  gap: 1px;
}

.swper_list_box {
  display: inline-grid;
  grid-template-columns: repeat(6, 1fr);
  grid-row-gap: 10px;
  grid-column-gap: 10px;
  width: 100%;
}

.gameSwiper {
  font-size: 18px;
  color: #fff;
  font-weight: 600;
  margin: 20px 0;

  .game_swiper_head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 20px 0;

    .s_left {
      display: flex;
      align-items: center;
      gap: 10px;

      img {
        width: 45px;
      }

      span {
        font-size: 18px;
        font-weight: 550;
      }
    }

    .s_right {
      display: flex;
      align-items: center;
      gap: 10px;

      .view_all {
        cursor: pointer;
        padding: 6px 15px;
        background-color: var(--theme-button-background);
        border-radius: 5px;
        color: #585E77;
        font-size: 12px;
      }

      .btn {
        display: flex;
        align-items: center;
        gap: 10px;

        .btn_c {
          cursor: pointer;
          padding: 5px;
          background-color: var(--theme-button-background);
          color: #fff;
          font-size: 15px;
          border-radius: 5px;
          color: #585E77;
        }
      }
    }
  }
}
</style>
  