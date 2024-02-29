<template>
  <div class="invitationInformation">
    <div class="t_box">
      <div class="t_box_l">
        <div>
          {{ t('refer.NovoProjeto') }}
          <span>{{ t('refer.semlimite') }}</span>
        </div>
        <div><span>{{ t('base.currencySymbol') }} {{ parseInt(store.state.conf.all_conf.invit_recharge_gift) }}</span>
          {{ t('refer.paraconvidarnovato') }}</div>

        <div>{{ t('refer.Ganhe', {
          money:
            `${t('base.currencySymbol')}${parseInt(store.state.conf.all_conf.invit_recharge_gift)}`
        }) }}

        </div>
        <div>
          {{ t('refer.Ganhe2') }}
          <span @click="copy(store.state.conf.all_conf.share_conf['share_contact_email'])">{{
            store.state.conf.all_conf.share_conf['share_contact_email'] }}</span>
        </div>
      </div>
      <img src="@assets/images/refer/newRefer/Gold_Stack.png" alt="" />
    </div>
    <div class="c_box">
      <div class="c_box_link">
        <span>{{ t('refer.LinkdeIndicação') }}</span>
        <span>{{ inviteLink }}</span>
        <img src="@assets/images/public/Copy_icon_2.png" alt="" @click="copy(inviteLink)" />
      </div>
      <div class="c_box_QR_code">
        <div class="QR_code_box">
          <vueQr class="QR_code" :text="inviteLink"></vueQr>
        </div>
        <div class="c_box_QR_code_btn" @click="saveImg">{{ t('refer.Salvar') }}</div>
      </div>
      <div class="c_box_img_l">
        <span>{{ t('refer.Compartilhar') }}</span>
        <img src="@assets/images/refer/home_Facebook_icon@2x.png" alt="" @click="linkJump(0)" />
        <img src="@assets/images/refer/home_Telegram_icon@2x.png" alt="" @click="linkJump(1)" />
        <img src="@assets/images/refer/home_phone_icon@2x.png" alt="" @click="linkJump(2)" />
      </div>
    </div>
    <div class="my_reward">
      <div class="my_reward_column">
        <span>{{ t('refer.MinhaRecompensa') }}</span>
        <span @click="transfershow = true">{{ t('account.Retirada') }}</span>
      </div>
      <div class="my_reward_b">
        <div class="my_reward_b_l">
          <div class="my_reward_b_l_box">
            <div class="my_reward_b_l_box_top">
              <span>{{ store.state.user.team_one_user_num }}</span>{{ t('refer.pessoa') }}
            </div>
            <div class="my_reward_b_l_box_bottom">{{ t('refer.UsuáriosIndicados') }}</div>
          </div>
          <div class="my_reward_b_l_box">
            <div class="my_reward_b_l_box_top">
              <span>{{ store.state.user.share_valid_number }}</span>{{ t('refer.pessoa') }}
            </div>
            <div class="my_reward_b_l_box_bottom">{{ t('refer.Usuáriosdepositados') }}</div>
          </div>
        </div>
        <div class="my_reward_b_r">
          <div class="my_reward_b_l_box">
            <div class="my_reward_b_l_box_top">
              <span>{{ moneyFormat(store.state.user.total_commission) }}</span>{{ t('base.currencySymbol') }}
            </div>
            <div class="my_reward_b_l_box_bottom">{{ t('refer.BônusTotal') }}</div>
          </div>
          <div class="my_reward_b_l_box">
            <div class="my_reward_b_l_box_top">
              <span>{{ moneyFormat(store.state.user.commission) }}</span>{{ t('base.currencySymbol') }}
            </div>
            <div class="my_reward_b_l_box_bottom">{{ t('refer.BônusRestantes') }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <QR_code_com :text="inviteLink" ref="QR_code_com_ref" style="position: absolute; z-index: -1" />
  <el-dialog v-model="transfershow" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
    :width="store.state.status.isPc ? '512px' : '100%'">
    <CommissionWithdrawals v-if="transfershow"></CommissionWithdrawals>
  </el-dialog>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import vueQr from "vue-qr/src/packages/vue-qr.vue";
import QR_code_com from "./QR_code.vue";
import CommissionWithdrawals from "./CommissionWithdrawals.vue";
import { copy, moneyFormat } from "@/utils/baseFun";
import transferPop from "./transferPop.vue";

export default defineComponent({
  name: "invitationInformation",
  components: { QR_code_com, vueQr, transferPop, CommissionWithdrawals },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      inviteLink: "",
      transfershow: false,
    });

    state.inviteLink = store.state.conf.all_conf.share_conf["url"] + store.state.user.uid;

    // 保存图片
    const QR_code_com_ref = ref(null);
    const saveImg = () => {
      if (store.state.user.token && store.state.user.token !== "") {
        (QR_code_com_ref.value as any).toSave();
      } else {
        store.dispatch("status/setLoginShow", true);
      }
    };

    const linkJump = (str) => {
      if (str == 0)
        window.open(`https://www.facebook.com/sharer.php?u=${state.inviteLink}`);
      else if (str == 1)
        window.open(`https://web.telegram.org/#/im?tg=${state.inviteLink}`);
      else if (str == 2) window.open(`https://wa.me/?text=${state.inviteLink}`);
    };

    proxy.$mitt.on("transfershow", (data) => {
      state.transfershow = data;
    });

    const tabJump = () => {
      proxy.$mitt.emit("changeTabsIdx", 1);
    };

    return {
      ...toRefs(state),
      store,
      t,
      saveImg,
      QR_code_com_ref,
      linkJump,
      copy,
      tabJump,
      moneyFormat,

    };
  },
});
</script>
<style lang="scss" scoped>
.invitationInformation {
  margin-bottom: 18px;

  .t_box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 58px 10px 63px;
    background: #202431;
    border-radius: 4px;

    .t_box_l {
      div:nth-child(1) {
        position: relative;
        font-size: 32px;
        font-weight: 600;
        color: #ffffff;

        span {
          position: absolute;
          top: 10px;
          left: 550px;
          transform: rotate(15deg);
          padding: 5px 10px;
          display: inline-block;
          font-size: 14px;
          color: #202431;
          background: #6dff7c;
        }
      }

      div:nth-child(2) {
        padding: 16px 0 25px 0;
        font-size: 36px;
        font-weight: 600;
        color: #ffffff;

        span {
          color: #f12c4c;
        }
      }

      div:nth-child(3) {
        // width: 298px;
        font-size: 16px;
        color: #b2b6c5;
        line-height: 24px;
      }

      div:nth-child(4) {
        // width: 298px;
        margin-top: 15px;
        margin-bottom: 5px;
        font-size: 16px;
        color: #b2b6c5;
        line-height: 24px;

        span {
          color: #6dff7c;
        }
      }
    }

    img {
      width: 413px;
    }
  }

  .c_box {
    display: flex;
    gap: 36px;
    margin: 18px 0;
    padding: 25px 0 25px 32px;
    background: #202431;
    border-radius: 4px;

    .c_box_link {
      display: flex;
      align-items: center;
      gap: 20px;
      padding: 11px 17px;
      background: #151821;
      border-radius: 4px;
      font-size: 14px;

      span:nth-child(1) {
        color: #b2b6c5;
      }

      span:nth-child(2) {
        color: #ffffff;
      }

      img {
        cursor: pointer;
        width: 26px;
      }
    }

    .c_box_QR_code {
      display: flex;
      align-items: center;
      gap: 18px;

      .QR_code_box {
        padding: 5px;
        background: rgba(65, 129, 238, 0.2);
        border-radius: 4px;
        border: 1px solid rgba(65, 129, 238, 0.8);

        .QR_code {
          display: block !important;
          width: 36px;
          height: 36px;
        }
      }

      .c_box_QR_code_btn {
        cursor: pointer;
        padding: 17px 63px;
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
        background: #f12c4c;
        border-radius: 4px;
      }
    }

    .c_box_img_l {
      display: flex;
      align-items: center;
      gap: 10px;

      span {
        margin-right: 8px;
        font-size: 14px;
        color: #9396a4;
      }

      img {
        cursor: pointer;
        width: 40px;
      }
    }
  }

  .my_reward {
    padding: 18px 0 34px 0;
    background: #202431;
    border-radius: 4px;

    .my_reward_column {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 17px;
      padding: 0 24px 0 36px;

      span:nth-child(1) {
        font-size: 18px;
        color: #ffffff;
      }

      span:nth-child(2) {
        cursor: pointer;
        display: inline-block;
        padding: 14px 20px;
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
        background: #f12c4c;
        border-radius: 4px;
      }
    }

    .my_reward_b {
      display: flex;

      .my_reward_b_l,
      .my_reward_b_r {
        display: flex;
        justify-content: space-evenly;
        width: 100%;

        .my_reward_b_l_box {
          text-align: center;

          .my_reward_b_l_box_top {
            margin-bottom: 4px;
            font-size: 14px;
            color: #b2b6c5;

            span {
              margin-right: 8px;
              font-size: 34px;
              font-weight: 600;
              color: #ffffff;
              line-height: 43px;
            }
          }

          .my_reward_b_l_box_bottom {
            font-size: 14px;
            color: #b2b6c5;
          }
        }
      }

      .my_reward_b_r {
        position: relative;

        &::after {
          content: "";
          position: absolute;
          left: 0;
          width: 4px;
          height: 56px;
          background: #474a54;
        }

        .my_reward_b_l_box:nth-child(2) {
          .my_reward_b_l_box_top {
            color: #ffd703;

            span {
              color: #ffd703;
            }
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .invitationInformation {
    .t_box {
      gap: 11px;
      flex-direction: column;
      padding: 16px 17px 0 17px;

      .t_box_l {
        text-align: center;

        div:nth-child(1) {
          font-size: 20px;

          span {
            top: 30px;
            left: 220px;
          }
        }

        div:nth-child(2) {
          padding: 16px 0 25px 0;
          font-size: 25px;
          line-height: 27px;

          span {
            color: #f12c4c;
          }
        }

        div:nth-child(3) {
          width: auto;
          font-size: 14px;
        }

        div:nth-child(4) {
          width: auto;
          font-size: 14px;

          a {
            color: #6dff7c;
          }
        }
      }

      img {
        width: 100%;
      }
    }

    .c_box {
      flex-wrap: wrap;
      gap: 0;
      margin: 12px 0 28px 0;
      padding: 0;
      background: transparent;

      .c_box_link {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 11px 17px;
        margin-bottom: 28px;
        background: #202431;
        font-size: 12px;
      }

      .c_box_QR_code {
        display: flex;
        align-items: center;
        gap: 10px;
        width: 35%;

        .c_box_QR_code_btn {
          padding: 17px 7px;
        }
      }

      .c_box_img_l {
        width: 65%;
        gap: 8px;

        span {
          margin-right: -8px;
        }

        img {
          width: 32px;
        }
      }
    }

    .my_reward {
      padding: 10px 0 24px 0;

      .my_reward_column {
        padding: 0 8px 0 20px;

        span:nth-child(1) {
          font-size: 16px;
        }

        span:nth-child(2) {
          padding: 10px 17px;
          font-size: 13px;
        }
      }

      .my_reward_b {
        gap: 38px;
        flex-direction: column-reverse;

        .my_reward_b_l,
        .my_reward_b_r {
          display: flex;
          justify-content: space-evenly;
          width: 100%;

          .my_reward_b_l_box {
            .my_reward_b_l_box_top {
              font-size: 12px;

              span {
                margin-right: 6px;
                font-size: 30px;
                line-height: 36px;
              }
            }

            .my_reward_b_l_box_bottom {
              font-size: 12px;
            }
          }
        }

        .my_reward_b_r {
          &::after {
            bottom: -19px;
            left: 50%;
            transform: translate(-50%, 0);
            width: calc(100% - 24px);
            height: 2px;
          }
        }
      }
    }
  }
}
</style>
