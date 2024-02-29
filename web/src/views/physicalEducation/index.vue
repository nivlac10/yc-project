<template>
  <div class="physicalEducation" v-if="showElFlag">
    <div class="physicalEducation_top_info">
      <div class="physicalEducation_top_info_left">
        <div class="physicalEducation_top_info_left_title">Bem-vindo ao AFB Sports！</div>
        <div class="physicalEducation_top_info_left_info">
          Nossa casa de apostas intuitiva é feita tanto para jogadores novos quanto
          experientes.
        </div>
        <div class="physicalEducation_top_info_left_btn">
          <div class="btn" @click="jumpGame">Começar o Jogo</div>
          <!-- <div class="img" v-for="(item, index) in physicalEducationImg" :key="index">
            <img :src="item.img" alt="">
          </div>
          <div class="img">
            <span>Todos</span>
          </div> -->
        </div>
      </div>
      <div class="physicalEducation_top_info_right">
        <img src="@assets/images/physicalEducation/Neymar.png" alt="" />
      </div>
    </div>
    <div class="physicalEducation_pix">
      <div class="physicalEducation_pix_info">Método De Pagamento Preferido</div>
      <div class="physicalEducation_pix_center">
        <div><img src="@assets/images/physicalEducation/pix.png" alt="" /></div>
      </div>
      <div class="physicalEducation_pix_btn" @click="jumpDeposit">Iniciar Depósito</div>
    </div>
    <div class="physicalEducation_img_info">
      <div class="physicalEducation_img_info_title">Vantagem</div>
      <div class="physicalEducation_img_info_imgList">
        <div
          class="physicalEducation_img_info_imgList_box"
          v-for="(item, index) in imgList"
          :key="index"
        >
          <img :src="item.img" alt="" />
          <div class="physicalEducation_img_info_imgList_box_title">{{ item.title }}</div>
          <div class="physicalEducation_img_info_imgList_box_info">{{ item.info }}</div>
        </div>
      </div>
    </div>
  </div>
  <div class="iframe_box" v-else>
    <iframe :src="iframe_url" frameborder="0" />
  </div>
</template>
<script lang="ts">
import {
  reactive,
  toRefs,
  getCurrentInstance,
  defineComponent,
  onBeforeUnmount,
} from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { getImageUrl, getUserInfo } from "@/utils/baseFun";
import { GameService } from "@/api/game";

export default defineComponent({
  name: "physicalEducation",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      physicalEducationImg: [
        { img: getImageUrl("physicalEducation/soccer.png") },
        { img: getImageUrl("physicalEducation/mma.png") },
        { img: getImageUrl("physicalEducation/volleyball.png") },
      ],
      imgList: [
        {
          img: getImageUrl("physicalEducation/balance.png"),
          title: "Jogo Justo 100% Confiável",
          info:
            "Tem Um Sistema De Fair Play Líder Mundial Que Utiliza A Mesma Tecnologia SHA25 Da BTC, Todos Os Dados São Reais E Rastreáveis!",
        },
        {
          img: getImageUrl("physicalEducation/Golden_pig.png"),
          title: "100% Real 1:1",
          info:
            "Plataforma Com Ativos Correspondendo À Taxa De Câmbio Em Tempo Real Do Brasil, Garantindo Assim O Interesse De Todos Os Brasileiros.",
        },
        {
          img: getImageUrl("physicalEducation/VIP.png"),
          title: "Retirada VIP24 / 7 Para PIX",
          info:
            "Todos Os Usuários Da Plataforma Podem Desfrutar Do Serviço VIP, Retirando Dinheiro Via PIX 24 Horas Por Dia, 7 Dias Por Semana, Em Qualquer Lugar E A Qualquer Momento.",
        },
        {
          img: getImageUrl("physicalEducation/Savings_account.png"),
          title: "100% De Segurança E Proteção",
          info:
            "A Plataforma Colabora Com Vários Bancos Brasileiros Para Garantir A Segurança Dos Fundos Dos Usuários.",
        },
      ],
      showElFlag: true,
      iframe_url: "",
      playState: false,
    });

    const jumpGame = () => {
      if (store.state.user.token) {
        state.showElFlag = false;
        GameService.get_game_play_url({ gid: 1817 }).then((res) => {
          state.iframe_url = res.data.url;
          state.playState = true;
          store.dispatch("status/setPlayIngState", true);
        });
      } else store.dispatch("status/setLoginShow", true);
    };

    const jumpDeposit = () => {
      if (store.state.user.token) store.state.status.depositShow = true;
      else store.dispatch("status/setLoginShow", true);
    };
    onBeforeUnmount(() => {
      if (state.playState) {
        getUserInfo();
        store.dispatch("status/setPlayIngState", false);
      } else {
        store.dispatch("status/setPlayIngState", false);
      }
    });
    return { ...toRefs(state), store, t, jumpGame, jumpDeposit };
  },
});
</script>
<style lang="scss" scoped>
.physicalEducation {
  padding-top: 20px;

  .physicalEducation_top_info {
    display: flex;
    margin-bottom: 18px;
    height: 338px;
    box-sizing: border-box;
    overflow: hidden;
    background-color: #202431;

    .physicalEducation_top_info_left {
      padding: 32px 0 0 54px;
      width: 517px;
      flex-shrink: 0;

      .physicalEducation_top_info_left_title {
        font-size: 36px;
        font-weight: 600;
        color: #ffffff;
      }

      .physicalEducation_top_info_left_info {
        padding: 26px 0 57px 0;
        font-size: 17px;
        color: #ffffff;
        line-height: 26px;
      }

      .physicalEducation_top_info_left_btn {
        display: flex;
        gap: 12px;

        .btn {
          cursor: pointer;
          padding: 0 27px;
          flex-shrink: 0;
          line-height: 48px;
          font-size: 14px;
          font-weight: 600;
          color: #ffffff;
          background: #f12c4c;
          border-radius: 4px;
        }

        .img {
          display: flex;
          align-items: center;
          justify-content: center;
          height: 48px;
          min-width: 70px;
          border-radius: 4px;
          border: 1px solid rgba(77, 84, 93, 0.85);
          box-sizing: border-box;

          img {
            width: 30px;
          }

          span {
            font-size: 12px;
            color: #adb1cb;
          }
        }
      }
    }

    .physicalEducation_top_info_right {
      padding-top: 20px;

      img {
        position: relative;
        left: -10%;
        display: block;
        width: 100%;
        height: 318px;
        transform: scaleX(1.2);
      }
    }
  }

  .physicalEducation_pix {
    display: flex;
    margin-bottom: 56px;
    padding: 16px 24px 16px 54px;
    justify-content: space-between;
    align-items: center;
    background: #202431;

    > div {
      width: 100%;
    }

    .physicalEducation_pix_info {
      font-size: 16px;
      font-weight: 600;
      color: #ffffff;
    }

    .physicalEducation_pix_center {
      div {
        position: relative;
        width: 111px;

        &::before {
          content: "";
          position: absolute;
          left: 50%;
          bottom: -35%;
          transform: translate(-50%, 0);
          width: 449px;
          height: 60px;
          background-image: url(@assets/images/physicalEducation/dot.png);
          background-size: 100% 100%;
        }

        img {
          display: block;
          width: 100%;
        }
      }
    }

    .physicalEducation_pix_btn {
      cursor: pointer;
      width: 170px;
      padding: 17px 29px;
      box-sizing: border-box;
      flex-shrink: 0;
      font-size: 14px;
      font-weight: 600;
      color: #ffffff;
      background: #f12c4c;
      border-radius: 4px;
    }
  }

  .physicalEducation_img_info {
    .physicalEducation_img_info_title {
      position: relative;
      margin-bottom: 70px;
      font-size: 22px;
      font-weight: 600;
      text-align: center;
      color: #ffffff;

      &::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 153px;
        height: 6px;
        transform: translate(-50%, 0);
        background-image: url(@assets/images/physicalEducation/Decoration.png);
        background-size: 100% 100%;
      }
    }

    .physicalEducation_img_info_imgList {
      display: flex;
      flex-wrap: wrap;

      .physicalEducation_img_info_imgList_box {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 92px;
        width: 50%;

        img {
          width: 352px;
        }

        .physicalEducation_img_info_imgList_box_title {
          padding: 44px 0 24px 0;
          font-size: 20px;
          font-weight: 600;
          color: #ffffff;
        }

        .physicalEducation_img_info_imgList_box_info {
          width: 393px;
          text-align: center;
          font-size: 14px;
          font-weight: 600;
          color: #98abd0;
          line-height: 21px;
        }
      }
    }
  }
}

.iframe_box {
  position: fixed;
  width: 100vw;
  height: 100vh;
  left: 50%;
  transform: translate(-50%, 0);
  z-index: 1000;
  background-color: #12151c;
  height: calc(100vh - 80px);

  iframe {
    position: fixed;
    width: 1200px;
    height: 100%;
    left: 50%;
    transform: translate(-50%, 0);
    background-image: url(@assets/images/public/newLogo.gif);
    background-repeat: no-repeat;
    background-size: 66px 80px;
    background-position: 50% 50%;
  }
}

@media (max-width: 768px) {
  .iframe_box {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    transform: translate(0, 44px);
    height: calc(100% - 44px);

    iframe {
      height: 100%;
      width: 100%;
      background-size: 50px 61px;
    }
  }

  .physicalEducation {
    padding: 12px 12px 0 12px;

    .physicalEducation_top_info {
      display: flex;
      flex-direction: column;
      margin-bottom: 13px;
      height: auto;

      .physicalEducation_top_info_left {
        padding: 32px 22px 0 22px;
        width: 100%;
        box-sizing: border-box;

        .physicalEducation_top_info_left_title {
          font-size: 30px;
          line-height: 36px;
          text-align: center;
        }

        .physicalEducation_top_info_left_info {
          padding: 20px 0 32px 0;
          font-size: 14px;
          line-height: 21px;
          text-align: center;
        }

        .physicalEducation_top_info_left_btn {
          justify-content: space-between;
          flex-wrap: wrap;
          gap: 14px;

          .btn {
            width: 100%;
            text-align: center;
            box-sizing: border-box;
          }

          .img {
            height: 42px;
            width: calc(25% - 14px);

            img {
              width: 24px;
            }
          }
        }
      }

      .physicalEducation_top_info_right {
        padding-top: 29px;

        img {
          left: 0;
          width: 100%;
          height: auto;
          transform: scaleX(1);
        }
      }
    }

    .physicalEducation_pix {
      gap: 24px;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      margin-bottom: 38px;
      padding: 24px 0;

      > div {
        width: 100%;
        text-align: center;
      }

      .physicalEducation_pix_center {
        div {
          margin: 0 auto;
          position: relative;

          &::before {
            display: none;
          }

          img {
            display: block;
            width: 100%;
          }
        }
      }
    }

    .physicalEducation_img_info {
      .physicalEducation_img_info_title {
        margin-bottom: 41px;
      }

      .physicalEducation_img_info_imgList {
        padding: 0 20px;
        box-sizing: border-box;

        .physicalEducation_img_info_imgList_box {
          margin-bottom: 32px;
          width: 100%;

          img {
            width: 310px;
          }

          .physicalEducation_img_info_imgList_box_title {
            padding: 26px 0 16px 0;
            font-size: 18px;
          }

          .physicalEducation_img_info_imgList_box_info {
            width: auto;
            font-size: 12px;
          }
        }
      }
    }
  }
}
</style>
