<template>
  <div class="refer_max_box">
    <barckTitle></barckTitle>
    <!-- <activity />
    <rule-description /> -->
    <div class="newRefer">
      <div class="title">
        <img src="@/assets/images/refer/newRefer/people@2x.png" alt="">
        <span class="sl_font">bônus de convite</span>
      </div>
      <div class="title2">
        Inscreva-se e completa qualquer valor de deposito e você pode obter um conhecimento adicional de convites, com cada inscrição de um cliente mais, você pode ganhar mais.
      </div>

      <ranking />

      <div class="title3 Pctitle3" v-if="store.state.user.token && store.state.user.token !== ''"
        style="background: transparent;">
        <!-- <img src="@/assets/images/refer/newRefer/megaphone.png" alt="" class="title3LeftImg"> -->
        <div class="title3LeftImg QR_code">
          <vueQr :text="inviteLink"></vueQr>
          <div class="sl_box_shadow" style="border-radius: 8px;" @click="saveImg">clique em salvar</div>
        </div>

        <QR_code_com :text="inviteLink" ref="QR_code_com" style="position: absolute; z-index: -1;" />

        <div class="islogin">
          <div class="left">
            <div class="isloginTxt">{{ t('refer.YOURINVITELINK') }}</div>
            <div class="leftInput">
              {{ inviteLink }}
              <img src="@/assets/images/refer/newRefer/Copy_btn.png" alt="" @click="copy(inviteLink)">
            </div>
            <div class="isloginTxt">
              {{ t('refer.SHAREWITH') }}
            </div>
            <div class="ritImg">
              <img src="@/assets/images/refer/newRefer/home_Facebook_icon@2x.png" alt="" @click="linkJump(0)">
              <img src="@/assets/images/refer/newRefer/home_Telegram_icon@2x.png" alt="" @click="linkJump(1)">
              <img src="@/assets/images/refer/newRefer/home_phone_icon@2x.png" alt="" @click="linkJump(2)">
            </div>
          </div>
          <div class="rit">
            <div class="top_box">
              <div>
                <p>{{ t('account.NumberOfInvitees') }}</p>
                <div class="ritInput">
                  <img src="@/assets/images/refer/newRefer/icon.png" alt="">
                  <p><span>{{ share_valid_number }}</span></p>
                </div>
              </div>
              <div>
                <p>{{ t('refer.COMMISSIONS') }}</p>
                <div class="ritInput">
                  <img src="@/assets/images/language/brazil.png" alt="">
                  <p>{{ t('base.currencySymbol') }}<span>{{ store.state.user.commission }}</span></p>
                </div>
              </div>
            </div>
            <div class="btns">
              <div></div>
              <div class="sl_box_shadow" @click="trabShows(true)">RETIRADA</div>
              <!-- <div class="sl_box_shadow" @click="transfershow = true">TRANSFERIR</div> -->
            </div>
          </div>
        </div>
        <!-- <img src="@/assets/images/refer/newRefer/Money_bag.png" alt="" class="title3RitImg"> -->
      </div>
      <div class="title3" v-else>
        <img src="@/assets/images/refer/newRefer/megaphone.png" alt="" class="title3LeftImg">
        <div class="notLogin sl_box" @click="toSign">
          {{ t('refer.GETBONUS') }}
        </div>
        <img src="@/assets/images/refer/newRefer/Money_bag.png" alt="" class="title3RitImg">
      </div>
      <!-- <newActivity></newActivity> -->
      <my-invite-bonus />
      <refer-list />
      <el-dialog v-model="trabShow" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
        :width="store.state.status.isPc ? '512px' : '100%'">
        <pop></pop>
      </el-dialog>
      <el-dialog v-model="transfershow" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
        :width="store.state.status.isPc ? '512px' : '100%'">
        <transferPop></transferPop>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { reactive, toRefs, getCurrentInstance, defineComponent, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import activity from "./components/activity.vue";
import ruleDescription from "./components/ruleDescription.vue";
import { useI18n } from "vue-i18n";
import { useStore } from "@/store/index";
import { copy, downloadIamge } from "@/utils/baseFun";
import newActivity from "./components/newActivity.vue";
import pop from '@/components/Pop-ups/pop.vue'
import transferPop from './components/transferPop.vue'
import vueQr from 'vue-qr/src/packages/vue-qr.vue'
import referList from "./components/referList.vue";
import ranking from "./components/ranking.vue";
import myInviteBonus from "./components/myInviteBonus.vue"
import QR_code_com from "./components/QR_code.vue";
import barckTitle from "@/components/back/index.vue";
export default defineComponent({
  name: "refer",
  components: { activity, ruleDescription, newActivity, transferPop, pop, vueQr, referList, ranking, myInviteBonus, QR_code_com , barckTitle},
  setup(props) {
    // route 配置
    const route = useRoute();
    // router 配置
    const router = useRouter();
    // i18n 配置
    const { t } = useI18n();

    const store = useStore();

    const { proxy } = getCurrentInstance();
    //  变量
    const state = reactive({
      share_valid_number: 0,
      inviteLink: '',
      trabShow: false,
      transfershow: false,
    });

    proxy.$mitt.on('setNumberOfInvitees', (val) => {
      // if (val >= 200) state.share_valid_number = 200
      // else state.share_valid_number = val
      state.share_valid_number = val
    })

    state.inviteLink = store.state.conf.all_conf.share_conf.url + store.state.user.uid
    function trabShows(data) {
      state.trabShow = data;
    }

    proxy.$mitt.on("tabShow", (data) => {
      trabShows(data)
    });

    proxy.$mitt.on("transfershow", (data) => {
      state.transfershow = data;
    });
    function toSign() {
      store.dispatch('status/setLoginShow', true)
    }

    const linkJump = (str) => {
      if (str == 0) window.open(`https://www.facebook.com/sharer.php?u=${state.inviteLink}`)
      else if (str == 1) window.open(`https://web.telegram.org/#/im?tg=${state.inviteLink}`)
      else if (str == 2) window.open(`https://wa.me/?text=${state.inviteLink}`)
    }

    // 保存图片
    const QR_code_com = ref(null)
    const saveImg = () => {
      QR_code_com.value.toSave()
    }
    return { ...toRefs(state), t, store, copy, trabShows, toSign, linkJump, QR_code_com, saveImg };
  },
});
</script>

<style  lang="scss" scoped>
@media (max-width: 768px) {
  .newRefer {
    width: calc(100% - 38px);
    padding: 0 14px;
    box-sizing: border-box;

    >div {
      width: 100% !important;
    }

    .title {
      // width: calc(100% - 28px) !important;
      // margin-left: 0 !important;
      // margin-top: 25px !important;

      span {
        font-size: 22px !important;
      }

      img {
        width: 30px !important;
        height: 30px !important;
        margin-right: 10px !important;
      }
    }


    .title2 {
      margin-bottom: 16px;
      // width: calc(100% - 27px) !important;
      margin-left: 0px !important;
      margin-top: 11px !important;
      font-size: 13px !important;
      text-align: center;
    }

    .title3 {
      // width: calc(100% - 38px) !important;
      height: 78px !important;

      .title3LeftImg {
        width: 48px !important;
        height: 44px !important;
        left: 10px !important;
        top: 10px !important;
      }

      .title3RitImg {
        width: 50px !important;
        height: 33px !important;
        right: -7px !important;
      }
    }

    .QR_code {
      text-align: center;

      img {
        margin-bottom: 5px !important;
        border-radius: 16px;
        width: 72px !important;
      }

      div {
        padding: 5px !important;
        font-size: 12px !important;
        border-radius: 20px;
      }
    }

    .Pctitle3 {
      height: auto !important;

      .isloginTxt {
        margin-top: 9px !important;
      }

      .title3LeftImg {
        width: 87px !important;
        height: 80px !important;
        left: 12px !important;
        top: 5px !important;


      }

      .left {
        height: 124px;
        margin-bottom: 20px;


        .leftInput {
          margin-top: 4px !important;
          width: 189px !important;
          height: 30px !important;
          font-size: 12px !important;

          img {
            width: 30px !important;
          }
        }

        .ritImg {
          img {
            width: 23px !important;
            height: 23px !important;
          }
        }
      }

      .rit {
        padding: 10px 10px 0 10px !important;
        height: 124px;

        .top_box {
          p {
            font-size: 13px !important;
          }
        }

        .btns {

          div {
            // width: 123px !important;
            height: 24px !important;
            font-size: 12px !important;
          }

        }

        .ritInput {
          // width: 252px !important;
          height: 30px !important;



          img {
            width: 20px !important;
            height: 15px !important;
          }

          p {
            font-size: 14px !important;

            span {
              margin-right: 8px !important;
              font-size: 14px !important;
            }
          }
        }
      }

      .isloginTxt {
        font-size: 13px !important;
      }
    }

    .notLogin {
      width: 200px !important;
      height: 40px !important;
      font-size: 16px !important;
      border-radius: 4px !important;
    }

    .islogin {
      display: flex !important;
      flex-direction: column !important;
    }
  }
}

.refer_max_box {
  flex-direction: column;
  width: 100%;
}

.newRefer {
  width: 100%;
  display: flex;
  flex-direction: column;

  .title {
    display: flex;
    justify-content: flex-start;

    span {
      font-size: 42px;
      font-weight: bold;
      text-align: center;
      display: flex;
      align-items: center;
    }

    img {
      width: 78px;
      height: 78px;
      // margin-right: 40px;
      transform: scale(1.5);
    }
  }

  .title2 {
    width: calc(100% - 92px);
    margin-left: 92px;
    margin: 40px 0 40px 0;
    // width: 1020px;
    text-align: left;
    font-size: 22px;
    color: var(--auxiliary-font-color-9);
  }


  .title3 {
    width: 100%;
    height: 230px;
    background: url(@/assets/images/refer/newRefer/banner.png) no-repeat;
    background-size: 100% 100%;
    color: #fff;
    margin: 20px 0;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;

    .title3LeftImg {
      position: absolute;
      top: 46px;
      left: 41px;
      width: 161px;
      height: 147px;
    }

    .title3RitImg {
      position: absolute;
      top: 50px;
      right: 11px;
      width: 131px;
      height: 88px;
    }

    .notLogin {
      width: 435.4px;
      height: 85.61px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 36px;
      color: #000;
      font-weight: bold;
    }

    .islogin {
      width: 100%;
      // margin-left: 194px;
      display: grid;
      grid-template-columns: calc(60% - 32px) 1fr;
      column-gap: 32px;
      height: 100%;
      // display: flex;

      .left {
        background: linear-gradient(90deg, #5229B0 0%, #583BF3 100%);
        border-radius: 12px;
        padding-left: 35%;

        .leftInput {
          width: 352px;
          position: relative;
          display: flex;
          align-items: center;
          padding-left: 18px;
          font-size: 22px;
          color: #fff;
          border-radius: 7.5px;
          margin-top: 17px;
          width: 370.83px;
          height: 54.53px;
          border: 2px solid;
          border-image: linear-gradient(135deg, rgba(97, 30, 246, 1), rgba(181, 10, 238, 1)) 2 2;
          background: linear-gradient(128deg, #411B85 0%, #2A1C50 100%);
          cursor: pointer;

          img {
            position: absolute;
            right: 0;
            top: 0;
            width: 56px;
          }
        }

        .ritImg {
          margin-top: 8px;
          display: flex;
          column-gap: 20px;

          img {
            width: 42.85px;
            height: 42.85px;
          }
        }

      }

      .rit {
        background: linear-gradient(90deg, #7C3CB3 0%, #593BF3 100%);
        border-radius: 12px;
        padding: 40px 30px 34px 30px;

        .top_box {
          display: flex;
          align-items: center;
          gap: 10px;

          >div {
            width: 100%;

            p {
              text-align: left;
              font-size: 16px;
              font-weight: bold;
              margin-bottom: 10px;
            }

            .ritInput {
              display: flex;
              align-items: center;
              justify-content: space-between;
              padding: 0 10px 0 10px;
              // width: 355px;
              height: 58px;
              border-image: linear-gradient(135deg, rgba(97, 30, 246, 1), rgba(181, 10, 238, 1)) 2 2;
              background: linear-gradient(128deg, #411B85 0%, #2A1C50 100%);
              border-radius: 8px;

              p {
                font-size: 22px;
                margin: 0;
                font-weight: 500;

                span {
                  font-size: 22px;
                }
              }

              img {
                width: 40px;
                height: 28px;
              }


            }
          }
        }

        .btns {
          display: flex;
          margin-top: 26px;

          div {
            width: 100%;
            height: 40px;
            font-size: 20px;
            font-weight: bold;
            color: #1B1D29;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
          }

        }

        .btns>div:first-child {
          margin-right: 17px;
        }

      }
    }

    .isloginTxt {
      margin-top: 17px;
      color: #FFFFFF;
      font-size: 22px;
      font-weight: bold;
      font-family: DIN Next LT Pro-Bold, DIN Next LT Pro;
    }



  }

  .Pctitle3 {
    .QR_code {
      text-align: center;

      img {
        margin-bottom: 10px;
        border-radius: 16px;
        width: 137px;
      }

      div {
        cursor: pointer;
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
        color: #1B1D29;
        border-radius: 20px;
      }
    }

    .title3LeftImg {
      position: absolute;
      top: 20px;
      left: 41px;
      width: 161px;
      height: 147px;
    }

    .title3RitImg {
      position: absolute;
      top: 246px;
      right: -7px;
      width: 55px !important;
      height: 37px !important;
    }
  }

}
</style>
      