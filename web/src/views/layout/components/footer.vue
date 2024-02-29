<template>
  <div class="footer ">
    <div class="top_box">
      <div class="demo-collapse">
        <el-collapse v-model="activeName" accordion>
          <el-collapse-item :title="t('home.Casion')" name="0">
            <div class="list">
              <ul>
                <li v-for="(item, index) in casionList" :key="index" @click="item.jump_index">
                  {{ item.label }}
                </li>
              </ul>
            </div>
          </el-collapse-item>
          <el-collapse-item :title="t('home.MemberRewards')" name="1">
            <div class="list">
              <ul>
                <li v-for="(item, index) in memberRewardsList" :key="index" @click="item.jump_index">
                  {{ item.label }}
                </li>
              </ul>
            </div>
          </el-collapse-item>

          <el-collapse-item :title="t('home.ABOUTUS')" name="2">
            <div class="list">
              <ul>
                <li v-for="(item, index) in aboutUsList" :key="index" @click="item.jump_index">
                  {{ item.label }}
                </li>
              </ul>
            </div>
          </el-collapse-item>
          <el-collapse-item :title="t('home.Help')" name="3">
            <div class="list">
              <ul>
                <li v-for="(item, index) in helpList" :key="index" @click="item.jump_index">
                  {{ item.label }}
                </li>
              </ul>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
      <el-row :gutter="10">
        <el-col :xs="24" :sm="15" :md="15" :lg="24" :xl="24">
          <el-row class="hidden-xs-only">
            <el-col :xs="5" :sm="5" :md="5" :lg="5" :xl="5">
              <div class="list">
                <div class="title">{{ t('footer.JogosdeCasino') }}</div>
                <ul>
                  <li v-for="(item, index) in casionList" :key="index" @click="item.jump_index">
                    {{ item.label }}
                  </li>
                </ul>
              </div>
            </el-col>
            <el-col :xs="4" :sm="4" :md="4" :lg="4" :xl="4">
              <div class="list">
                <div class="title">{{ t('footer.Bônus') }}</div>
                <ul>
                  <li v-for="(item, index) in promotionsList" :key="index">
                    {{ item.label }}
                  </li>
                </ul>
              </div>
            </el-col>
            <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6">
              <div class="list">
                <div class="title">{{ t('footer.Promoções') }}</div>
                <ul>
                  <li v-for="(item, index) in memberRewardsList" :key="index" @click="item.jump_index">
                    {{ item.label }}
                  </li>
                </ul>
              </div>
            </el-col>
            <el-col :xs="7" :sm="7" :md="7" :lg="5" :xl="5">
              <div class="list">
                <div class="title">{{ t('footer.SobreNós') }}</div>
                <ul>
                  <li v-for="(item, index) in aboutUsList" :key="index" @click="item.jump_index">
                    {{ item.label }}
                  </li>
                </ul>
              </div>
            </el-col>
            <el-col :xs="7" :sm="7" :md="7" :lg="4" :xl="4">
              <div class="list">
                <div class="title">{{ t('footer.Ajuda') }}</div>
                <ul>
                  <li v-for="(item, index) in helpList" :key="index" @click="item.jump_index">
                    {{ item.label }}
                  </li>
                </ul>
              </div>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </div>
    <div class="bottom_box">
      <div class="bottom_box2">
        <div class="bottom_box2_top" v-if="store.state.status.isPc">
          <img src="@assets/images/footer/PIX_icon.png" alt="">
          <div>
            <img src="@assets/images/footer/brasileiros.png" alt="">
            <p>{{ t('footer.DeBrasileiros') }}</p>
          </div>
          <img src="@assets/images/footer/SIQ_icon.png" alt="">
        </div>
        <div class="bottom_box2_top_app" v-else>
          <div class="bottom_box2_top_app_top">
            <img src="@assets/images/footer/PIX_icon.png" alt="">
            <img src="@assets/images/footer/SIQ_icon.png" alt="">
          </div>

          <el-divider />
          <div>
            <img src="@assets/images/footer/brasileiros.png" alt="">
            <p>{{ t('footer.DeBrasileiros') }}</p>
          </div>
        </div>
        <el-divider v-if="store.state.status.isPc" />
        <div class="bottom_box2_body">
          <div class="bottom_box2_body_font">
            <div>
              <img src="@assets/images/footer/18_icon.png" alt="">
              <img src="@assets/images/footer/GC_icon.png" alt="" @click="jumpTo">
            </div>
            <div>
              <p>
                {{ t('footer.p1', { data: store.state.conf.all_conf.platform['platform_path'] }) }}
                <span @click="jumpTo">{{ t('footer.GLH') }}</span>
              </p>
              <p>{{ t('footer.p2', { data: store.state.conf.all_conf.platform['platform_path'] }) }}</p>
            </div>
          </div>
          <!-- <div class="bottom_box2_body_img">
            <img :src="v" alt="" v-for="v in imgList">
          </div> -->
        </div>
        <el-divider />
        <div class="bottom_box2_botom">
          <img :src="store.state.conf.all_conf.platform['platform_title_icon_url']" alt="">
          <p>{{ t('footer.p3', { data: store.state.conf.all_conf.platform['platform_url'] }) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { getImageUrl } from "@/utils/baseFun";
export default defineComponent({
  name: "footer_com",
  setup() {
    const store = useStore();
    const { t } = useI18n();
    const router = useRouter()
    const state = reactive({
      imgList: [
        getImageUrl('footer/PG_icon.png'),
        getImageUrl('footer/pragmatic_play.png'),
        getImageUrl('footer/relax.png'),
        getImageUrl('footer/home_bottom_evoplay_icon.png'),
        getImageUrl('footer/evolution_icon.png'),
        getImageUrl('footer/yggdrasil.png'),
        getImageUrl('footer/JILI.png'),
        getImageUrl('footer/FUNKYGAMES.png'),
      ],
      casionList: [
        {
          label: computed(() => t('gameText.TodosOsJogos')),
          jump_index: () => {
            router.push("/")
          }
        },
        {
          label: computed(() => t('gameType.Slot')),
          jump_index: () => {
            router.push({
              path: "/", query: {
                type: 0
              }
            })
          }
        },
        {
          label: computed(() => t('gameType.Pescaria')),
          jump_index: () => {
            router.push({
              path: "/", query: {
                type: 3
              }
            })
          }
        },
        {
          label: computed(() => t('gameType.JogosMesa')),
          jump_index: () => {
            router.push({
              path: "/", query: {
                type: 1
              }
            })
          }
        },
        {
          label: computed(() => t('gameType.AoVivo')),
          jump_index: () => {
            router.push({
              path: "/", query: {
                type: 2
              }
            })
          }
        },
      ],
      promotionsList: [
        { label: computed(() => t('gameText.TodosOsJogos')) },

      ],

      memberRewardsList: [
        {
          label: computed(() => t('sidebar.BônusVIP')),
          jump_index: () => {
            router.push("/vipBonus")
          }
        },
        {
          label: computed(() => t('footer.GabineteBônus')),
          jump_index: () => {
            router.push("/bonusCabinet")
          }
        },
        {
          label: computed(() => t('headerUser.BônusdeConvite')),
          jump_index: () => {
            router.push("/refer")
          }
        },

        // {
        //   label: "Betting bonuc",
        //   jump_index: () => {
        //     router.push("/bettingBouns")
        //   }
        // },
        // {
        //   label: "Bônus de Convite",
        //   jump_index: () => {
        //     router.push("/refer")
        //   }
        // },
      ],
      aboutUsList: [
        // {
        //   label: "About BIGWIN777",
        //   jump_index: () => {
        //     router.push({
        //       path: "/help", query: {
        //         l_index: 0,
        //         r_index: 0
        //       }
        //     })
        //   }
        // },
        {
          label: computed(() => t('footer.Supplier')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 1
              }
            })
          }
        },
        {
          label: computed(() => t('footer.Withdrawallimit')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 2
              }
            })
          }
        },
        {
          label: computed(() => t('footer.Withdrawalfee')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 3
              }
            })
          }
        },
        {
          label: computed(() => t('footer.Bonuspolicy')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 4
              }
            })
          }
        },
        {
          label: computed(() => t('footer.Commonproblem')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 5
              }
            })
          }
        },
      ],

      helpList: [
        // { label: "Live support" },
        // { label: "Help center" },
        {
          label: computed(() => t('footer.SobreNós')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 0
              }
            })
          }
        },
        {
          label: computed(() => t('footer.CassinoResponsáveis')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 1
              }
            })
          }
        },
        {
          label: computed(() => t('footer.TermosdeServiço')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 2
              }
            })
          }
        },
        {
          label: computed(() => t('footer.PolíticadePrivacidade')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 3
              }
            })
          }
        },
        {
          label: computed(() => t('footer.PolíticaKYC')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 4
              }
            })
          }
        },
        {
          label: computed(() => t('footer.Contralavagemdedinheiro')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 5
              }
            })
          }
        },
        {
          label: computed(() => t('footer.AutoExclusão')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 6
              }
            })
          }
        },
        {
          label: computed(() => t('footer.ProteçãodosMenores')),
          jump_index: () => {
            router.push({
              path: "/help", query: {
                l_index: 0,
                r_index: 7
              }
            })
          }
        },
      ],
      activeName: "0",
    });
    function jumpTo() {
      router.push("/Certificate")
    }
    return { ...toRefs(state), t, store, jumpTo };
  },
});
</script>
<style  lang="scss" scoped>
:deep(.el-divider--horizontal) {
  border-top: 2px solid #3C3C57;
}

.footer {
  padding: 60px 0 0 0;

  .top_box {
    margin-bottom: 30px;
    max-width: 1200px;
    min-width: 900px;
    margin: 0 auto;

    .demo-collapse {
      display: none;

      :deep(.el-collapse) {
        border: none;

        .el-collapse-item__header {
          background: transparent;
          border: none;
          font-size: 18px;
          color: var(--theme-font-color-fff);

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

      .list {
        ul {
          li {
            margin-bottom: 8px;
            font-size: 18px;
            color: var(--auxiliary-font-color-4);
          }
        }
      }
    }

    .logo {
      display: flex;
      flex-direction: column;
      gap: 20px;

      .logo_span {
        color: #fff;
        font-size: 40px;
        font-weight: 600;

        .logo_777 {
          font-weight: 600;
        }
      }

      p {
        width: 365px;
        font-size: 21px;
        color: var(--theme-font-color-fff);
        line-height: 26px;
      }
    }

    .list {
      .title {
        margin-bottom: 22px;
        font-size: 16px;
        font-weight: 500;
        color: #98ABD0;
      }

      ul {
        li {
          cursor: pointer;
          margin-bottom: 8px;
          font-size: 14px;
          color: #585E77;

          &:hover {
            color: #98ABD0;
          }
        }
      }
    }
  }

  .bottom_box {
    background: #1D1D29;
    margin-top: 40px;
    padding: 40px 0 50px 0;

    .bottom_box2 {
      max-width: 1200px;
      min-width: 900px;
      margin: 0 auto;
      padding-bottom: 60px;

      .bottom_box2_top_app {
        display: flex;
        flex-direction: column;
        justify-items: center;
        align-items: center;
        margin-top: 25px;

        .bottom_box2_top_app_top>img:nth-child(1) {
          width: 155px;
        }

        .bottom_box2_top_app_top>img:nth-child(2) {
          width: 114px;
        }
      }


      .bottom_box2_top_app>div:nth-child(3) {
        display: flex;
        flex-direction: column;
        justify-items: center;
        align-items: center;

        p {
          margin-top: 12px;
        }

        img {
          width: 69px;
        }
      }

      .bottom_box2_top {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        justify-items: center;
        align-items: center;
      }

      .bottom_box2_top>img:nth-child(1) {
        width: 174px;
      }

      .bottom_box2_top>img:nth-child(3) {
        width: 127px;
      }

      .bottom_box2_top>div {
        display: flex;
        flex-direction: column;
        align-items: center;

        img {
          width: 77px;
        }

        p {
          margin-top: 13px;
          color: #C3CFD9;
          font-size: 20px;
        }
      }

      .bottom_box2_body {
        .bottom_box2_body_font {
          display: flex;
          margin-bottom: 23px;

          div {
            p {
              font-size: 16px;
              color: #7992A7;
              line-height: 23px;
              font-weight: 400;
              margin-bottom: 13px;

              span {
                color: #3EA0F1;
                text-decoration: underline;
                text-decoration-color: #3EA0F1;
              }
            }
          }
        }

        .bottom_box2_body_font>div:nth-child(1) {
          display: flex;
          align-items: center;
          margin-right: 14px;

          img {
            margin-right: 23px;
          }
        }

        .bottom_box2_body_img {
          display: grid;
          grid-template-columns: repeat(8, 1fr);
          align-items: center;
          justify-items: center;
        }

      }

      .bottom_box2_botom {
        display: flex;
        flex-direction: column;
        align-items: center;

        p {
          margin-top: 13px;
          color: #7992A7;
          font-size: 17px;
        }
      }
    }

    .img_list_1,
    .img_list_2 {
      display: flex;
      align-items: center;
    }

    .img_list_1 {
      margin-bottom: 40px;

      img {
        margin-right: 20px;
      }
    }

    .img_list_2 {
      img {
        margin-right: 30px;
      }
    }

    p {
      font-size: 17px;
      color: var(--auxiliary-font-color-9);
    }
  }
}

@media screen and (max-width: 768px) {
  .footer {
    padding: 60px 12px 30px 12px;

    .top_box {
      width: 100%;
      max-width: auto !important;
      min-width: auto !important;

      .demo-collapse {
        display: block;
      }
    }

    .bottom_box2 {
      padding-bottom: 60px;
      width: 100%;
      max-width: auto !important;
      min-width: auto !important;

      .bottom_box2_body {
        .bottom_box2_body_font {
          flex-direction: column;
        }

        .bottom_box2_body_font>div:nth-child(1) {
          margin: 39px 0 34px 0;
        }

        .bottom_box2_body_img {
          display: flex !important;
          flex-wrap: wrap;
          justify-content: center;
          gap: 5%;

          // grid-template-columns: repeat(3,1fr);
          img {
            margin-bottom: 5px;
          }
        }
      }

      .bottom_box2_botom {
        img {
          width: 282px;
        }

        p {
          font-size: 14px;
        }
      }
    }

    .bottom_box {
      padding: 0;
      background: transparent;

      .img_list_1,
      .img_list_2 {
        flex-wrap: wrap;
        justify-content: center;
        margin-bottom: 16px;
      }

      .img_list_1 {
        img {
          margin-right: 20px;
        }
      }

      .img_list_2 {
        img {
          margin-right: 30px;
        }
      }

      p {
        font-size: 15px;
        text-align: center;
      }
    }
  }
}
</style>
