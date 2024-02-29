<template>
  <div class="gamePage">
    <div :class="{ game_max_box: true, full_state: fullState }" v-if="store.state.status.isPc">
      <div class="gamePage_column">
        <div class="gamePage_column_l_box">
          <span>{{ gameData.game_name }}</span>
          <span>[{{ gameData.f_name }}]</span>
        </div>
        <div class="logo_img">
          <!-- <img src="@assets/images/footer/logo.png" alt=""> -->
          <span>{{ store.state.conf.all_conf.platform['platform_path'] }}</span>
        </div>
        <div class="gamePage_column_r_box">
          <div>
          </div>
          <div @click="CollectGames" class="star_box">
            <img v-if="gameData.tag == 0" src="@assets/images/home/star.png" alt="" />
            <img v-if="gameData.tag == 1" src="@assets/images/home/star_t.png" alt="" />
          </div>
          <img @click="fullState = !fullState" src="@assets/images/home/amplify.png" alt="" />
        </div>
      </div>
      <div class="game">

        <div class="game_bg_mask_box" v-if="gamePlay == false">
          <div class="mask_box">
            <div></div>
            <img :src="gameData.icon" alt="">
          </div>
          <div class="info_box">
            <div class="play_or_demo">
              <div class="sl_box_shadow play_box_pc" @click="getGameUrl()">
                <img src="@/assets/images/gamePlay/play.png" alt="">
                <span style="color:#000">{{ t('gameText.JogoReal') }}</span>
              </div>
              <div v-if="gameData.is_demo == 1" class="play_box_pc" style="background: #585E77;margin-left: 10px;"
                @click="getGameUrl(2)">
                <img src="@/assets/images/gamePlay/play.png" alt="">
                <span style="color:#fff">{{ t('gameText.Jogosgrátis') }}</span>
              </div>
            </div>

          </div>

        </div>
        <iframe :src="game_url" frameborder="0" class="game_iframe" v-else></iframe>
      </div>
    </div>
    <div class="phone_game_box" v-else>
      <div class="game_info_max_box">
        <div class="game_info_top">
          <div class="info_left">
            <img :src="gameData.icon" alt="">
          </div>
          <div class="info_right">
            <div class="game_name_box">
              <span class="game_name">{{ gameData.game_name }}</span>
              <span class="f_name"> {{ gameData.f_name }}</span>
            </div>
            <div @click="CollectGames" class="tag_box">
              <img v-if="gameData.tag == 0" src="@assets/images/home/star.png" alt="" />
              <img v-if="gameData.tag == 1" src="@assets/images/home/star_t.png" alt="" />
              <span>{{ t('gameText.Favorito') }}</span>
            </div>

          </div>
        </div>
        <div class="sl_box_shadow play_box" @click="getGameUrl()">
          <img src="@/assets/images/gamePlay/play.png" alt="">
          <span style="color:#000">{{ t('gameText.JogoReal') }}</span>
        </div>
        <div v-if="gameData.is_demo == 1" class="play_box" style="background: #585E77;" @click="getGameUrl(2)">
          <img src="@/assets/images/gamePlay/play.png" alt="">
          <span style="color:#fff">{{ t('gameText.Jogosgrátis') }}</span>
        </div>
      </div>
      <div class="phone_play_iframe" v-if="gamePlay">
        <div class="phone_play_hader">
          <div class="phone_header_column">
            <img src="@/assets/images/public/arrow_right.png" alt="" @click="closeIfram">
            <div>{{ store.state.conf.all_conf.platform['platform_path'] }}</div>
            <div></div>
          </div>
          <!-- <div class="close_game" @click="gamePlay = false">
            <img src="@/assets/images/public/Shutdown.png" alt="">
            <div class="game_name_box">
              <span>{{ gameData.game_name }}</span>
              <span>[{{ gameData.f_name }}]</span>
            </div>
          </div> -->
          <!-- <div @click="CollectGames" class="star_box">
            <img v-if="gameData.tag == 0" src="@assets/images/home/star.png" alt="" />
            <img v-if="gameData.tag == 1" src="@assets/images/home/star_t.png" alt="" />
          </div> -->
        </div>
        <iframe :src="game_url" style="width: 100%;height: 100%;" frameborder="0"></iframe>
      </div>
    </div>

    <!-- <div class="more_column">
      <div>MAIS DE {{ gameData.f_name }}</div>
      <div @click="toGameList">
        <span>Ver tudo</span>
        <img src="@assets/images/public/arrow_icon.png" alt="" />
      </div>
    </div>
    <div class="gameList">
      <gameBox v-for="v in gameList" :data="v"></gameBox>
    </div> -->
    <div style="margin-top: 48px;" class="more_column">
      <span>{{ t('gameText.TodosOsJogos') }}</span>
      <allGameBox :game_id="gameData.game_id"></allGameBox>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch, onBeforeUnmount } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "@/store/index";
import gameBox from "../components/gameBox.vue";
import { get_game_data, get_game_data_by_gid, whetherCollectGames } from "@/utils/gameUtils";
import { GameService } from "@/api/game";
import { getUserInfo } from "@/utils/baseFun";
import allGameBox from "@/components/allGameBox/index.vue"
import { ElNotification } from 'element-plus'
import { useI18n } from "vue-i18n";

export default defineComponent({
  components: { gameBox, allGameBox },
  name: "gamePage",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const route = useRoute()
    const store = useStore();
    const state = reactive({
      value: false,
      gameList: [],
      gameData: {
        game_id: 1,
        gid: 1,
        tag: 0,
        game_name: '',
        f_name: '',
        icon: '',
        is_demo: 0
      },
      loadingGame: true,
      game_url: "",
      fullState: false,
      gamePlay: false,
      playState: false
    });

    onBeforeUnmount(() => {
      if (state.playState) {
        getUserInfo()
        store.dispatch("status/setPlayIngState", false)
      } else {
        store.dispatch("status/setPlayIngState", false)
      }
    })
    store.dispatch("status/setPlayIngState", true)
    function inintData() {
      state.loadingGame = true
      state.gameData = get_game_data_by_gid(route.params.gid) as any
      state.gamePlay = false
      if (route.query.directGame) {
        getGameUrl()
      }
    }
    inintData()
    function getGameUrl(type?: number) {
      let apiStr: any
      if (type == 2) {
        if (store.state.user.vip_lv < 1) return ElNotification({
          message: t('gameText.Épossíveljogar'),
          type: 'warning',
          duration: 3000,
          offset: 65,
        })

        apiStr = GameService.get_demo_game_play_url
      }
      else apiStr = GameService.get_game_play_url

      state.gamePlay = true
      apiStr({ gid: state.gameData.gid }).then((res) => {
        if (res.data.code == 1) {
          state.game_url = res.data.url
          state.loadingGame = false
          state.playState = true
        }
      })
    }
    watch(() => route.params.gid, (newval, oldval) => {
      if (newval) {
        inintData()

      }
    }, {
      deep: true
    })

    state.gameList = get_game_data(state.gameData.game_id, null, null, null).allGameList as any;
    const CollectGames = () => {
      whetherCollectGames(state.gameData.gid, state.gameData.tag)
      state.gameData.tag = state.gameData.tag == 1 ? 0 : 1;
    }
    function toGameList() {
      router.push({
        name: 'gameList',
        params: {
          game_id: state.gameData.game_id
        }
      })
    }
    function closeIfram() {
      if (route.query.directGame) {
        router.push('/')
        return
      }
      state.gamePlay = false

    }
    return { ...toRefs(state), store, t, toGameList, CollectGames, getGameUrl, closeIfram };
  },
});
</script>
<style  lang="scss" scoped>
@media (max-width: 750px) {
  .gamePage {
    padding: 10px 10px !important;

  }

}

.phone_play_iframe {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  background-color: #000;
  display: flex;
  flex-direction: column;

  .phone_play_hader {
    display: flex;
    align-items: center;
    background-color: var(--theme-menu-background);
    padding: 5px 10px;
    height: 44px;
    box-sizing: border-box;
    gap: 20px;
    justify-content: space-between;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;

    .phone_header_column {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;

      img {
        transform: rotate(180deg);
        width: 16px;
      }

      div {
        font-size: 16px;
        font-weight: 600;
        color: #585E77;
      }
    }

    .close_game {
      padding: 5px 10px;
      background-color: var(--theme-button-background);
      border-radius: 3px;
      display: flex;
      align-items: center;
      gap: 20px;

      img {
        width: 20px;
      }
    }

    .game_name_box {
      display: flex;
      // flex-direction: column;
      gap: 10px;

      span:nth-child(1) {
        // margin-right: 17px;
        font-size: 14px;
        font-weight: bold;
        color: var(--theme-font-color-fff);
      }

      span:nth-child(2) {
        font-size: 13px;
        font-weight: 550;
        color: var(--auxiliary-font-color-2);
      }
    }
  }
}

.game_info_max_box {
  // background-color: var(--theme-navigationbar-background);
  border-radius: 13px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;


  .game_info_top {
    display: grid;
    grid-template-columns: 1fr 1fr;
    column-gap: 20px;

    .info_left {
      // padding: 10px 0;
      // height: 150px;
      border-radius: 6px;
      overflow: hidden !important;

      img {
        // height: 167px;

        width: 100%;
      }
    }

    .info_right {
      display: flex;
      flex-direction: column;
      margin: 10px 0;
      position: relative;
      gap: 20px;

      .game_name_box {
        display: flex;
        flex-direction: column;
        gap: 10px;

        .game_name {
          color: #fff;
          font-weight: 800;
          font-size: 18px;
        }

        .f_name {
          font-size: 12px;
          // font-weight: 600;
          color: #98ABD0;
        }
      }

      .tag_box {
        background-color: var(--theme-button-background);
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 10px;
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        border-radius: 100px;

        img {
          width: 30px;
        }

        span {
          font-size: 12px;
          // font-weight: 600;
          color: var(--auxiliary-font-color-3);
        }
      }

    }
  }


}

.play_box {
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 10px;
  gap: 10px;
  cursor: pointer;

  img {
    width: 40px;
  }

  span {
    font-size: 18px;
    font-weight: 600;
    color: var(--auxiliary-font-color-3);
  }
}

.play_box_pc {
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px 30px;
  gap: 10px;
  cursor: pointer;

  img {
    width: 45px;
  }

  span {
    font-size: 18px;
    font-weight: 600;
    color: var(--auxiliary-font-color-3);
  }
}

.gamePage {
  padding: 30px 10px;

  .full_state {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    height: 100vh !important;
    width: 100vw;
    z-index: 10000;

  }

  .game_max_box {
    height: 66vh;
    display: flex;
    flex-direction: column;

    .gamePage_column {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      // justify-content: space-between;
      align-items: center;
      background: var(--theme-navigationbar-background);
      border-radius: 12px 12px 0px 0px;

      height: 68px;
      padding: 0px 36px;

      .gamePage_column_l_box {

        // padding: 5px 25px;
        display: flex;
        gap: 12px;

        span:nth-child(1) {
          font-size: 16px;
          color: var(--theme-font-color-fff);
        }

        span:nth-child(2) {
          font-size: 16px;
          font-weight: 500;
          color: #585E77;
        }
      }

      .logo_img {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        span {
          font-size: 20px;
          color: #585E77;
        }
      }

      .gamePage_column_r_box {

        display: flex;
        justify-content: right;
        align-items: center;
        gap: 10px;

        >div {
          display: flex;
          align-items: center;
          gap: 10px;

          :deep(.el-switch) {
            .el-switch__action {
              background: var(--theme-background);
            }
          }

          .mode {
            font-size: 20px;
            font-weight: 500;
            color: var(--auxiliary-font-color-2);
          }
        }

        img {
          cursor: pointer;
        }



        img {
          width: 30px;
          height: 30px;
        }
      }
    }

    .game {
      width: 100%;
      background-color: var(--theme-button-background);
      border-bottom-left-radius: 15px;
      border-bottom-right-radius: 15px;
      position: relative;
      overflow: hidden;
      // min-height: 64vh;
      height: 100%;

      .game_bg_mask_box {
        width: 100%;
        height: 100%;
        position: relative;

        .mask_box {
          width: 100%;
          height: 100%;
          // position: absolute;
          filter: blur(17px);
          // background-size:  cover !important;
          background-size: 100% 100% !important;

          div {
            position: absolute;
            z-index: 20;
            width: 100%;
            height: 100%;
            background-color: rgba($color: #000000, $alpha: 0.3) !important;
          }

          img {
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100%;
            z-index: 10;
            transform: translateY(-30%);
          }
        }

        .info_box {
          position: absolute;
          top: 0;
          left: 0;
          bottom: 0;
          // display: flex;
          width: 100%;
          height: 100%;

          .play_or_demo {
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
          }
        }
      }

      .game_iframe {
        // position: absolute;
        // top: 0;
        // left: 0;
        // right: 0;
        // bottom: 0;
        height: 100%;
        width: 100%;
        background: #000;
      }
    }
  }



  .star_box {
    img {
      width: 50px !important;
      height: 50px !important;
    }
  }

  .more_column {
    display: flex;
    flex-direction: column;
    // align-items: center;
    gap: 20px;
    margin-top: 20px;
    margin-bottom: 30px;

    span {
      font-size: 24px;
      color: #fff;
      font-weight: 600;
    }


  }

  .gameList {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    column-gap: 10px;
  }
}

@media (max-width: 768px) {
  .more_column {

    span {
      font-size: 18px !important;
    }


  }

  .gamePage {

    .gamePage_column {
      padding: 9px 10px;
      border-radius: 8px 8px 0px 0px;

      .gamePage_column_l_box {
        span:nth-child(1) {
          margin-right: 13px;
          font-size: 12px;
        }

        span:nth-child(2) {
          font-size: 12px;
        }
      }

      .gamePage_column_r_box {
        gap: 10px;

        >div {
          gap: 10px;

          :deep(.el-switch) {
            .el-switch__action {
              background: var(--theme-background);
            }
          }

          .mode {
            font-size: 12px;
          }
        }

        img:nth-child(2) {
          width: 24px;
          height: 24px;
        }

        img:nth-child(3) {
          width: 14px;
          height: 14px;
        }
      }
    }


    .gameList {
      grid-template-columns: repeat(3, 1fr);
      row-gap: 10px;
    }
  }
}
</style>
