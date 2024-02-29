<template>
  <div class="game_max_box_one" @click="jumpgame()">
    <div class="game_box_max">
      <div class="img_box">
        <img src="@/assets/images/gamePlay/gamebg.png" @click="openGame" class="game_icon_bg" />
        <img v-lazy="props.data.icon" @click="openGame" class="game_icon" />
        <div class="is_top tag" v-if="props.data.is_top == 1">
          <span>TOP</span>
        </div>
        <!-- <div class="is_hot tag" v-if="props.data.is_hot == 1">
          <span>HOT</span>
        </div> -->
      </div>

      <div class="flag_box" @click.stop="CollectGames" v-if="props.data.tag_show">
        <img src="@/assets/images/gamePlay/start.svg" alt="" v-if="props.data.tag == 0" />
        <img src="@/assets/images/gamePlay/start_active.svg" alt="" v-else />
      </div>
      <div class="mask_box" v-if="store.state.status.isPc && props.data.status != 2">
        <div class="rtp_box" v-if="props.data.rtp > 0">
          <span>{{ t('gameText.RTP') }} {{ props.data.rtp }}%</span>
        </div>
        <div class="f_name_box">
          <span>{{ props.data.f_name }}</span>
        </div>
        <div class="game_name_box">
          <span>{{ props.data.game_name }}</span>
        </div>
        <div class="ms_box">

          <img src="@/assets/images/gamePlay/play.png" @click="openGame" class="play_icon" />
        </div>
        <!-- <van-text-ellipsis :content="props.data.game_name" class="game_name" /> -->
      </div>
    </div>
  </div>
</template>
<script>
import { reactive, toRefs } from "vue";
import { getTypeGameList } from "@/utils/gameDataUtils";
import { useStore } from "@/store/index";
import { useRouter } from "vue-router";
import { whetherCollectGames } from "@/utils/gameUtils";
import { useI18n } from "vue-i18n";

export default {
  name: "gameBox",
  components: {
  },
  props: {
    data: {
      type: Object,
    },
  },
  setup(props) {
    const store = useStore();
    const { t } = useI18n();
    const router = useRouter();
    //  变量
    const state = reactive({
      // game_data: props.data
    });
    const jumpgame = () => {
      if (store.state.user.token) {
        store.state.status.allGameShow = false
        router.push({
          name: "playGame",
          params: {
            gid: props.data.gid
          }
        })
      } else {
        store.dispatch('status/setLoginShow', true)
      }
    }
    const CollectGames = () => {
      if (store.state.user.token) {
        whetherCollectGames(props.data.gid, props.data.tag)
        props.data.tag = props.data.tag == 1 ? 0 : 1;
      } else {
        store.dispatch('status/setLoginShow', true)
      }
    }
    return { ...toRefs(state), t, store, props, jumpgame, CollectGames };
  },
};
</script>
<style  lang="scss" scoped>
.game_max_box_one {
  display: flex;
  // margin: 0 6px;
}

@media (max-width:750px) {


  .tag {
    left: 0;
    position: absolute;
    top: 0;
    padding: 3px 10px !important;
    border-bottom-right-radius: 15px;

    span {
      font-weight: 550;
      color: #fff !important;
      font-size: 13px !important;
    }
  }
}

.game_name {
  font-weight: 600;
  width: 80%;
  text-align: center;
  font-size: 18px !important;
  overflow: hidden;
}

.game_box_max {
  position: relative;
  width: 100%;
  background-color: #203148;
  border-radius: 8px;
  overflow: hidden;
}

.img_box {
  display: flex;
  width: 100%;
  position: relative;
  overflow: hidden;

  .game_icon_bg {
    width: 100%;
  }

  .game_icon {
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    // border-radius: 15px;
    transform: scale(1);
    object-fit: cover;
    // object-fit: cover;
  }

  .tag {
    left: 0;
    position: absolute;
    top: 0;
    padding: 5px 10px;
    border-bottom-right-radius: 15px;

    span {
      color: #fff !important;
      font-size: 16px;
    }
  }

  .is_top {
    // background-image: url(data:image/png;base64,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);
    // background-size: 100% 100%;
    background-color: #ED0A45;

  }

  .is_hot {
    // background-image: url(data:image/png;base64,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);
    // background-size: 100% 100%;
    background-color: #FF7503;
  }
}

.rtp_box {
  position: absolute;
  left: 6% !important;
  top: 86% !important;
  z-index: 10;
  width: 100%;

  span {
    font-size: 12px;
    color: #fff;
  }
}

.flag_box {

  cursor: pointer;
  position: absolute;
  right: 6%;
  bottom: 5%;
  width: 25px;
  height: 25px;
  z-index: 10;
  background-color: rgba(#fff, 0.3);
  border-radius: 100px;
  display: flex;
  justify-content: center;
  align-items: center;

  img {
    width: 20px;
  }
}

.game_box_max:hover {
  .game_icon {
    animation-name: enlarge;
    /*关键帧名称*/
    animation-duration: 0.5s;
    transform: scale(1.1);
  }

  .mask_box {
    display: flex;
    -webkit-backdrop-filter: saturate(180%) blur(3px) !important;
    backdrop-filter: saturate(180%) blur(3px) !important;

    .play_icon {
      cursor: pointer;
      animation-name: scaleActive;
      /*关键帧名称*/
      animation-duration: 0.5s;
      /*动画所花费的时间*/
    }

    .f_name_box {
      -webkit-animation: slide-in-blurred-top 0.3s cubic-bezier(0.230, 1.000, 0.320, 1.000) both;
      animation: slide-in-blurred-top 0.3s cubic-bezier(0.230, 1.000, 0.320, 1.000) both;
    }
  }
}

.mask_box {
  // display: flex;
  display: none;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  justify-content: center;
  align-items: center;
  border-radius: 8px;

  cursor: pointer;

  .f_name_box {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 10px 0;
    background-color: var(--auxiliary-background-11);

    span {

      font-size: 16px;
      font-weight: 600;
    }
  }

  .game_name_box {
    span {
      font-size: 14px;
      font-weight: 600;
    }
  }

  .ms_box {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .play_icon {
    width: 45%;
    transition: all 0.4s ease-out 0.1s;
    animation-name: scaleDraw;
    /*关键帧名称*/
    // animation-duration: 0.3s; /*动画所花费的时间*/
  }

  div {
    position: absolute;
    top: 20%;
    color: #fff;
    font-weight: 600;
    font-size: 18px;
    text-overflow: ellipsis;
    white-space: nowrap;

    // left: 50%;
    // transform: translateX(-50%);
  }
}

@keyframes scaleDraw {

  /*定义关键帧、scaleDrew是需要绑定到选择器的关键帧名称*/
  100% {
    transform: scale(1);
    opacity: 1;
  }

  0% {
    transform: scale(1.3);
    /*开始为原始大小*/
    opacity: 0.5;
  }
}

@keyframes scaleActive {

  /*定义关键帧、scaleDrew是需要绑定到选择器的关键帧名称*/
  0% {
    transform: scale(1.3);
    /*开始为原始大小*/
    opacity: 0;
  }

  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@-webkit-keyframes slide-in-blurred-top {
  0% {
    -webkit-transform: translateY(-1000px) scaleY(2.5) scaleX(0.2);
    transform: translateY(-1000px) scaleY(2.5) scaleX(0.2);
    -webkit-transform-origin: 50% 0%;
    transform-origin: 50% 0%;
    -webkit-filter: blur(40px);
    filter: blur(40px);
    opacity: 0;
  }

  100% {
    -webkit-transform: translateY(0) scaleY(1) scaleX(1);
    transform: translateY(0) scaleY(1) scaleX(1);
    -webkit-transform-origin: 50% 50%;
    transform-origin: 50% 50%;
    -webkit-filter: blur(0);
    filter: blur(0);
    opacity: 1;
  }
}

@keyframes slide-in-blurred-top {
  0% {
    -webkit-transform: translateY(-1000px) scaleY(2.5) scaleX(0.2);
    transform: translateY(-1000px) scaleY(2.5) scaleX(0.2);
    -webkit-transform-origin: 50% 0%;
    transform-origin: 50% 0%;
    -webkit-filter: blur(40px);
    filter: blur(40px);
    opacity: 0;
  }

  100% {
    -webkit-transform: translateY(0) scaleY(1) scaleX(1);
    transform: translateY(0) scaleY(1) scaleX(1);
    -webkit-transform-origin: 50% 50%;
    transform-origin: 50% 50%;
    -webkit-filter: blur(0);
    filter: blur(0);
    opacity: 1;
  }
}
</style>
    