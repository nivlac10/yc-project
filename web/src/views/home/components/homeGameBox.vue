<template>
  <div class="box_max_box">
    <div class="box_head">
      <slot></slot>
      <div class="mais_box">
        <div class="mais_font" @click="jumpRoute()">{{ t('btnName.Mais') }}</div>
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
    <div style="margin-bottom: 12px;" v-if="!store.state.status.isPc && $props.game_id != 20">
      <gameRtpBox></gameRtpBox>
    </div>
    <!-- <div class="game_list">
      <gameBox v-for="(v, i) in gameList" :key="v" :data="v"></gameBox>
    </div> -->
    <swiper :loop="true" class="mySwiper" @swiper="onSwiper" @slideChange="onSlideChange" style="" effect="fade">
      <swiper-slide v-for="(item, i) in gameList" class="game_list">
        <gameBox v-for="game in item" :data="game" class="game_box"></gameBox>
      </swiper-slide>
    </swiper>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, ref, defineComponent } from "vue";
import { store, useStore } from "@/store/index";
import gameBox from "./gameBox.vue";
import { get_game_data } from "@/utils/gameUtils";
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import router from "@/router";
import gameRtpBox from "@/components/gameRtpBox/index.vue"
import { useI18n } from "vue-i18n";

export default defineComponent({
  name: "index",
  components: { gameBox, SwiperSlide, Swiper, gameRtpBox },
  props: {
    jump_index: {
      type: Number,
      default: 0
    },
    game_id: {
      type: Number,
      default: 0
    },
    game_type: {
      type: Number,
      default: null
    },
  },
  setup(props) {
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      gameList: [],
      swiperDom: null
    });

    let gameData = null
    if (props.jump_index == 2) {
      let limit = store.state.status.isPc ? 63 : 37;
      gameData = get_game_data(null, null, null, 1, null, null, 1, limit) as any;
      if (gameData) {
        let pageLimit = store.state.status.isPc ? 21 : 9;
        splitArr(gameData['allGameList'], pageLimit)
      }
    }
    if (props.jump_index == 1) {
      let limit = store.state.status.isPc ? 63 : 37;
      gameData = get_game_data(null, null, null, null, 1, null, 1, limit) as any;
      if (gameData) {
        let pageLimit = store.state.status.isPc ? 21 : 6;
        splitArr(gameData['allGameList'], pageLimit)
      }
    }
    if (props.game_id != 0) {
      let limit = store.state.status.isPc ? 42 : 18;
      gameData = get_game_data(props.game_id, null, null, null, null, null, 1, limit) as any;
      if (gameData) {
        let pageLimit = store.state.status.isPc ? 14 : 6;
        splitArr(gameData['allGameList'], pageLimit)
      }
    }
    if (props.game_type != null) {
      let limit = store.state.status.isPc ? 42 : 18;
      gameData = get_game_data(null, props.game_type, null, null, null, null, 1, limit) as any;
      if (gameData) {
        let pageLimit = store.state.status.isPc ? 14 : 6;
        splitArr(gameData['allGameList'], pageLimit)
      }
    }
    function splitArr(arr, pageLimit) {
      let limit = pageLimit
      let count = arr.length / limit;
      let page = 0;
      let newArr = []
      for (let i = 0; i < count; i++) {
        let new_arr = [];
        let offset = page * limit;
        for (let j = 0; j < arr.length; j++) {
          if (offset <= j && j < offset + limit) {
            new_arr.push(arr[j] as never);
          }
        }
        page++;
        newArr.push(new_arr as never);
      }
      state.gameList = newArr
    }
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

    // 跳转页面
    const jumpRoute = () => {
      if (props.game_id != 0) {
        // router.push("/" + props.game_id)
        store.state.status.allGameShow = true
        store.state.status.game_id = props.game_id
      } else if (props.jump_index == 1) {
        router.push("/in-house")
      } else if (props.jump_index == 2) {
        router.push("/hot")
      } else if (props.game_type != null) {
        router.push("/gameType/" + props.game_type)
      }
    }
    return { ...toRefs(state), t, nextSwiper, prevSwiper, onSlideChange, onSwiper, jumpRoute, store };
  },
});
</script>
<style  lang="scss" scoped>
.box_max_box {

  background-color: #202431;
  color: #98ABD0;
  padding: 15px;
  border-radius: 16px;
  // display: flex;
  // flex-direction: column;
  gap: 13px;

  .box_head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0px;


    .mais_box {
      display: flex;
      align-items: center;
      gap: 10px;

      .mais_font {
        font-size: 18px;
        border: 1px solid #585E77;
        color: #585E77;
        border-radius: 8px;
        padding: 6px 16px;
        cursor: pointer;
      }

      .mais_font:hover {
        border: 1px solid #98ABD0 !important;
        color: #98ABD0;
      }

      .btn {
        display: flex;
        align-items: center;
        gap: 10px;
        justify-content: center;

        .btn_c {
          cursor: pointer;
          display: flex;
          align-items: center;
          padding: 6px;
          border: 1px solid #585E77;
          color: #fff;
          font-size: 16px;
          border-radius: 5px;
          color: #585E77;
        }

        .btn_c:hover {
          border: 1px solid #98ABD0 !important;
          color: #98ABD0;
        }
      }
    }
  }

  .game_list {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    grid-gap: 12px;
    width: 100%;
    // grid-row-gap: 12px;
    // width: 100%;
  }
}

@media (max-width: 750px) {
  .game_list {
    display: grid;
    grid-template-columns: repeat(3, 1fr) !important;
    grid-gap: 10px !important;
    // grid-column-gap: 4px;
    width: 100%;
  }

  .box_max_box {
    background-color: rgba($color: #000000, $alpha: 0.0);
    // background-color: #202431;
    color: #98ABD0;
    padding: 0px;
    border-radius: 16px;
    gap: 10px;

    .box_head {
      // background-color: #202431;   
    }
  }

  .mais_box {
    display: flex;
    align-items: center;
    gap: 6px;

    .mais_font {
      font-size: 12px !important;
      border: 1px solid #585E77;
      color: #585E77;
      border-radius: 6px !important;
      padding: 4px 12px !important;
      cursor: pointer;
    }

    .btn {
      display: flex;
      align-items: center;
      gap: 6px;
      justify-content: center;

      .btn_c {
        cursor: pointer;
        display: flex;
        align-items: center;
        padding: 4px !important;
        border: 1px solid #585E77;
        color: #fff;
        font-size: 12px !important;
        border-radius: 6px !important;
        color: #585E77;
      }
    }
  }
}
</style>
  