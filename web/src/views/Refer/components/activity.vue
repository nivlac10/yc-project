<template>
  <div class="refer_max_box">
    <div class="box">
      <div class="flex_box share_head">
        <img :src="lv_img" alt="" />
        <span>Nível {{ userState.share_lv }}</span>
        <button @click="jumpServic" v-if="!userState.share_valid_number <=
          all_conf.invite_recharge_bonus_list[userState.share_lv].number
        " class="cursor_p">
          Atualizar
          {{
            userState.share_valid_number +
            "/" +
            all_conf.invite_recharge_bonus_list[userState.share_lv].number
          }}
        </button>
        <button @click="jumpServic" v-else class="cursor_p active">
          Atualizar
          {{
            userState.share_valid_number +
            "/" +
            all_conf.invite_recharge_bonus_list[userState.share_lv].number
          }}
        </button>
      </div>
      <div class="share_body">
        <div class="share_data_box">
          <div class="share_data">
            <img src="@/assets/images/refer/home_Friends_icon@2x.png" alt="" />
            <span class="number">
              {{ userState.share_valid_number }}
            </span>
            <span> Número de Depósito </span>
          </div>
          <div class="submit_btn cursor_p" @click="(withdrType = 1),
            (isDeposit = false),
            trabShow = true
          ">
            Saque
          </div>
        </div>
        <div class="share_data_box">
          <div class="share_data">
            <img src="@/assets/images/refer/home_species1_icon@2x.png" alt="" />
            <span class="number">
              {{ userState.commission }}
            </span>
            <span> Comissões </span>
          </div>
          <div class="submit_btn cursor_p" @click="transfershow = true">
            Transferir
          </div>
        </div>
      </div>
    </div>
    <div class="box fx_max_box">
      <div class="fx_box">
        <div class="fx_l">
          <img src="@/assets/images/refer/home_horn_icon@2x.png" alt="" />
        </div>
        <div class="fx_r">
          <span class="fx_title">Seu link de convite</span>
          <div class="fx_copy_box">
            <!-- <span>https://bigwin777.comawdasdasdasdas</span> -->
            <input readonly class="fx_url" type="text" :value="all_conf.share_conf.url + userState.uid" />
            <img class="cursor_p" src="@/assets/images/refer/home_Copy_button@2x.png" alt="" @click="copyShraInfo" />
          </div>
          <div class="fx_share_box">
            <span class="title">Compartilhar com:</span>

            <div class="img_content">
              <img @click="linkJump('f')" class="cursor_p" src="@/assets/images/refer/home_Facebook_icon@2x.png" alt="" />
              <img @click="linkJump('w')" class="cursor_p" src="@/assets/images/refer/home_phone_icon@2x.png" alt="" />
            </div>
          </div>
        </div>
      </div>
      <span class="fx_botm_box">Comissões de Primeiro Depósitos(atual):
        <span style="color: #75ed3d">R${{
          all_conf.invite_recharge_bonus_list[userState.share_lv - 1]
            .commission
        }}</span></span>
    </div>
    <div class="box bonus_box">
      <div class="title">
        <span class="sl_font">Comissões extras</span>
        <img @click="ruleShow = true" class="cursor_p" src="@/assets/images/refer/home_question_mark_icon@2x.png"
          alt="" />
      </div>
      <div class="bonus_body">
        <div class="bonus felx_center cursor_p" v-for="(item, index) in inviteList" :key="item + index">
          <div class="felx_center" @click="receive_invite_task(item)">
            <img src="@/assets/images/refer/home_species1_icon@2x.png" alt="" />
            <span>{{ item.money }} {{ t('base.currency') }}</span>
          </div>
          <span :class="item.state != 1 ? 'sl_font_F' : 'sl_font'">{{ userState.share_valid_number }}/{{ item.num
          }}</span>
        </div>
      </div>
    </div>
    <!-- <van-overlay :show="true" /> -->

    <div class="activityRules_popup" v-if="ruleShow">
      <div class="popup_content">
        <div class="popup_header">
          <div class="popup_title">Comissões Extras</div>
          <div class="popup_close cursor_p" @click="ruleShow = false">X</div>
        </div>
        <div class="popup_list">
          <div class="describe">
            À medida que aumenta o número de membros que completam a primeiro
            depósito, você pode obter Comissões Extras.
          </div>
          <div class="tabble">
            <table>
              <tr>
                <th>Número de Depósito</th>
                <th>Comissões Extras</th>
              </tr>
              <tr v-for="(item, index) in ruleList" :key="item + index">
                <td>{{ item.num }}</td>
                <td>{{ item.money }}</td>
              </tr>
            </table>
          </div>
        </div>
      </div>
    </div>
    <el-dialog v-model="trabShow" :before-close="handleClose" :show-close="false" :close-on-click-modal="false"
      :close-on-press-escape="false" :width="store.state.status.isPc ? '512px' : '100%'">
      <pop></pop>
    </el-dialog>
    <el-dialog v-model="transfershow" :before-close="handleClose" :show-close="false" :close-on-click-modal="false"
      :close-on-press-escape="false" :width="store.state.status.isPc ? '512px' : '100%'">
      <transferPop></transferPop>
    </el-dialog>

    <!-- <div class="activityRules_popup" v-if="trabShow">
     
    </div>
    <div class="activityRules_popup" v-if="transfershow">
     
    </div> -->
  </div>
</template>
<script >
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";
import { useRoute, useRouter } from "vue-router";
import { copy, getImageUrl, getUserInfo, toast } from "@/utils/baseFun";
import { ReferService } from "@/api/refer";
import { UserService } from "@/api/user";
import { useI18n } from "vue-i18n";
import pop from '@/components/Pop-ups/pop.vue'
import transferPop from './transferPop.vue'
import withdrawSettings from "@/views/deposit/components/withdrawSettings.vue";
// import depositWithdrawalStore from "@/store/depositWithdrawal";
export default defineComponent({
  name: "activity",
  components: {
    pop,
    withdrawSettings,
    transferPop,
  },
  setup(props) {
    const store = useStore();
    // route 配置
    const route = useRoute();
    // router 配置
    const router = useRouter();

    const { t } = useI18n();

    const { proxy } = getCurrentInstance();
    // const payState = depositWithdrawalStore();
    const all_conf = store.state.conf.all_conf;

    let { depositWithdrawalShow, withdrType, isDeposit } = [false, 1, false];
    // storeToRefs(payState);
    //  变量
    const state = reactive({
      trabShow: false,
      ruleShow: false, // 规则列表显示
      ruleList: [], // 规则列表
      inviteList: [],
      money: 0,
      lv_img: getImageUrl(`Refer/level_${store.state.user.share_lv}.png`),
      userState: store.state.user,
      transfershow: false,
    });
    const linkJump = (val) => {
      if (val == "f") {
        // console.log(
        //   all_conf.share_conf.title +
        //   "\n" +
        //   all_conf.share_conf.detail +
        //   "\n" +
        //   all_conf.share_conf.url +
        //   state.userState.uid
        // );
        window.open(
          "https://www.facebook.com/sharer.php?u=" +
          escape(all_conf.share_conf.url + state.userState.uid)
        );
      } else if (val == "w")
        window.open(
          "https://api.whatsapp.com/send/?text=" +
          escape(
            all_conf.share_conf.title +
            "\n" +
            all_conf.share_conf.detail +
            "\n" +
            all_conf.share_conf.url +
            state.userState.uid
          )
        );
    };
    // 获取邀请规则
    const getUserInviteState = () => {
      ReferService.get_user_invite_state().then((res) => {
        state.ruleList = res.data.data;
        var arr = state.ruleList;
        var number = state.userState.share_valid_number;
        // var number = 45000;
        // state.ruleList[8].state = 1;

        for (let i = 0; i < arr.length; i++) {
          const element = arr[i];
          // 可领取
          if (element.state == 1 && i < arr.length - 3) {
            state.inviteList = [element, arr[i + 1], arr[i + 2]];
            return;
          } else if (element.state == 1 && i > arr.length - 3) {
            state.inviteList = [
              arr[arr.length - 3],
              arr[arr.length - 2],
              arr[arr.length - 1],
            ];
            return;
          }
          // 没有可领取的
          if (number < arr[0].num) {
            state.inviteList = [element, arr[i + 1], arr[i + 2]];
            return;
          } else if (number >= arr[arr.length - 3].num) {
            state.inviteList = [
              arr[arr.length - 3],
              arr[arr.length - 2],
              arr[arr.length - 1],
            ];
          } else if (number >= element.num) {
            state.inviteList = [element, arr[i + 1], arr[i + 2]];
          }
        }
        // state.inviteList.reverse().reverse();
        // console.log(arr);
        // console.log(state.inviteList);
      });
    };
    getUserInviteState();
    // 领取邀请
    const receive_invite_task = (item) => {
      if (item["state"] != 1) return;
      ReferService.user_receive_invite_task({ task_id: item["task_id"] }).then(
        (res) => {
          if (res.data.code == 1) {
            getUserInfo();
            toast("Receba o sucesso!");
            item["state"] = 2;
          }
          getUserInviteState(); // 获取邀请规则
        }
      );
    };
    // 跳转客服
    const jumpServic = () => {
      if (
        state.userState.share_valid_number >=
        all_conf.invite_recharge_bonus_list[state.userState.share_lv].number
      ) {
        window.open("https://t.me/bigwin777_romina");
      } else {
        toast("O número de pessoas convidadas não atingiu o mínimo.!");
      }
    };
    // 佣金转余额
    const transferMoney = () => {
      UserService.user_transfer_commission({ money: state.money }).then(
        (res) => {
          if (res.data.code == 1) {
            getUserInfo();
            state.trabShow = false;
          }
        }
      );
    };
    const copyShraInfo = () => {
      let text =
        all_conf.share_conf.title +
        "\n" +
        all_conf.share_conf.detail +
        "\n" +
        all_conf.share_conf.url +
        state.userState.uid;
      copy(text);
    };

    function trabShows(data) {
      state.trabShow = data;
    }

    proxy.$mitt.on("tabShow", (data) => {
      trabShows(data)
    });

    proxy.$mitt.on("transfershow", (data) => {
      state.transfershow = data;
    });
    return {
      ...toRefs(state),
      linkJump,
      getImageUrl,
      all_conf,
      receive_invite_task,
      jumpServic,
      transferMoney,
      depositWithdrawalShow,
      withdrType,
      isDeposit,
      copyShraInfo,
      t,
      store,
    };
  },
});
</script>
<style  lang="scss" scoped>
@media (max-width: 768px) {
  .refer_max_box {
    grid-template-columns: 1fr !important;
  }

  .bonus_box .bonus_body .bonus span {
    font-size: 12px !important;
  }

  .fx_share_box {
    margin-bottom: 20px !important;
  }

  .fx_botm_box {
    font-size: 13px !important;
  }

  .fx_copy_box {
    max-width: 200px !important;
  }

  .activityRules_popup {
    .popup_content {
      width: 100% !important;

      .popup_header {
        padding: 15px 0 !important;

        .popup_close {
          top: 15px !important;
          right: 20px !important;
          font-size: 20px !important;
        }
      }
    }
  }
}

.cursor_p {
  cursor: pointer;
}

.transf_popup {
  position: absolute;
  top: 50%;
  left: 50%;
  z-index: 1;
  transform: translate(-50%, -50%);
  width: 462px;
  background: #1e1e2d;
  border-radius: 16px;
  overflow: hidden;
  padding: 38px 25px 0 25px;

  .popup_header {
    position: relative;
    padding: 0 0 26px 0;
    display: flex;
    justify-content: space-between;

    .popup_title {
      font-weight: 500;
      font-size: 24px;
      text-align: center;
      color: #FBD31E;
    }

    .popup_close {
      font-weight: 500;
      font-size: 20px;

      img {
        width: 26px;
        height: 26px;
      }
    }
  }

  .popup_body {
    display: flex;
    flex-direction: column;
    gap: 16px;

    .money_box {
      font-size: 18px;
      font-weight: 500;
      border: none;
      background-color: #232c3a;
      padding: 5px 10px;
      border-radius: 5px;
    }

    button {
      font-size: 18px;
      color: #fff;
      font-weight: 500;
      background-color: #894dff;
      border-radius: 5px;
      padding: 15px;
    }
  }
}

.tran_c {
  width: 250px;
}

.sl_font {
  color: #fff15b;
  text-shadow: 0 0 10px #fff15b;
}

.sl_font_F {
  color: #fff;
}

.bonus_box {
  gap: 16px;
  display: flex;
  flex-direction: column;

  .title {
    display: flex;
    justify-content: space-between;
    align-items: center;

    span {
      font-size: 18px;
      line-height: 21px;
      font-weight: 500;
    }

    img {
      width: 20px;
    }
  }

  .felx_center {
    align-items: center;
    display: flex;
    flex-direction: column;
  }

  .bonus_body {
    display: flex;
    justify-content: space-between;
    font-size: 14px;

    .bonus {
      display: flex;
      flex-direction: column;
      gap: 16px;

      div {
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 16px;
        background-color: #232c3a;
        border-radius: 15px;

        img {
          width: 50px;
        }

        span {
          font-size: 14px;
        }
      }

      span {
        font-size: 16px;
        font-weight: 500;
      }
    }
  }
}

.fx_max_box {
  display: flex;
  flex-direction: column;

  .fx_box {
    display: grid;
    grid-template-columns: 30% 70%;
    gap: 16px;
    width: 100%;

    .fx_l {
      img {
        width: 100%;
      }
    }

    .fx_r {
      display: flex;
      flex-direction: column;
      gap: 16px;
      width: 100%;

      .fx_title {
        font-size: 14px;
        color: var(--auxiliary-font-color-9);
        font-weight: 500;
        display: flex;
      }

      .fx_copy_box {
        display: flex;
        background: #5b626c;
        justify-content: space-between;
        align-items: center;
        position: relative;
        border-radius: 5px;
        max-width: 210px;

        .fx_url {
          font-size: 17px;
          font-weight: 500;
          margin-left: 5px;
          background-color: rgba(0, 0, 0, 0);
          border: none;
          width: 100%;
        }

        img {
          position: absolute;
          right: -13px;
          width: 63px;
        }
      }
    }
  }

  .fx_botm_box {
    color: var(--auxiliary-font-color-9);
    font-size: 16px;
    font-weight: 500;
  }

  .fx_share_box {
    display: flex;
    flex-direction: column;
    gap: 18px;
    margin-bottom: 30px;

    .title {
      font-size: 14px;
      font-weight: 500;
      color: var(--auxiliary-font-color-9);
    }

    .img_content {
      display: flex;
      gap: 10px;

      img {
        width: 40px;
      }
    }
  }
}

.refer_max_box {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
  margin: 24px 0;

  .flex_box {
    display: flex;
    align-items: center;
  }

  .share_body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;

    .share_data_box {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .share_data {
      display: flex;
      flex-direction: column;
      padding: 10px 10px;
      border: 1px solid rgba(255, 255, 255, 0.4);
      border-radius: 16px;

      img {
        width: 25px;
        max-width: auto;
        height: 25px;
      }

      span {
        font-size: 10px;
        text-align: center;
      }

      .number {
        font-size: 30px;
        margin-bottom: 16px;
      }
    }

    .submit_btn {
      font-size: 16px;
      background: #894dff;
      padding: 10px 0;
      text-align: center;
      border-radius: 10px;
    }
  }

  .share_head {
    font-size: 18px;
    gap: 16px;
    font-weight: 500;
    margin-bottom: 16px;

    img {
      width: 40px;
    }

    span {
      color: var(--auxiliary-font-color-9);
    }

    button {
      border: none;
      color: #5b626c;
      padding: 5px 10px;
      background-color: #232c3a;
      border-radius: 5px;
      font-size: 14px;
    }

    .active {
      color: #fff;
      background-color: #894dff;
    }
  }

  .box {
    border-radius: 15px;
    background-color: #161f2d;
    padding: 16px;
    color: #fff;
  }
}

.activityRules_popup {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 999999;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;

  .popup_content {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 1;
    transform: translate(-50%, -50%);
    width: 750px;
    background: #1e1e2d;
    border-radius: 16px;
    overflow: hidden;

    .popup_header {
      position: relative;
      padding: 30px 0;

      .popup_title {
        font-weight: 500;
        font-size: 18px;
        text-align: center;
      }

      .popup_close {
        position: absolute;
        top: 20px;
        right: 50px;
        font-weight: 500;
        font-size: 40px;
      }
    }

    .popup_list {
      padding: 20px 20px;
      background: #292938;

      .describe {
        margin-bottom: 20px;
        font-weight: 500;
        line-height: 20px;
        font-size: 16px;
      }

      .tabble {
        table {
          width: 100%;
          font-size: 16px;
          text-align: center;
          border: 1px solid #2b3a46;

          tr,
          th,
          td {
            border: 1px solid #2b3a46;
            padding: 10px 0;
          }
        }
      }
    }
  }
}
</style>
    