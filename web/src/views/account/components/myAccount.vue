<template>
  <div class="myAccount">
    <div class="myAccount_box">
      <div class="user_box">
        <div class="edit_img">
          <svg-icon name="edit" hover @click="comShowIdx = 0" />
        </div>
        <div class="user_avatar">
          <img :src="getImageUrl(
            `avatar/headsculpture_img_${store.state.user.header_img}.png`
          )
            " alt="" />
          <div>{{ store.state.user.nickname }}</div>
        </div>
        <div class="user_info">
          <div class="user_info_box">
            <div class="label">{{ t('account.IDdousuário') }}</div>
            <div class="info"><span>{{ store.state.user.uid }}</span><svg-icon name="copy" hover
                @click="copy(store.state.user.uid.toString())" />
            </div>
          </div>
          <div class="user_info_box">
            <div class="label">{{ t('account.Telefone') }}</div>
            <div class="info"><span>{{ store.state.user.phone ? '+' : '' }}{{ store.state.user.phone }}</span></div>
          </div>
          <div class="user_info_box">
            <div class="label">{{ t('account.Email') }}</div>
            <div class="info"><span>{{ store.state.user['email'] }}</span></div>
          </div>
        </div>
        <div class="user_date">{{ t('account.DatadeCadastro') }}{{ store.state.user['add_time'] }}</div>
      </div>
      <div class="account_total_box">
        <withdraw-column-amount-info />
        <div class="account_total_box_info">
          <div class="account_total_box_info_title">{{ t('account.Totaldaconta') }}</div>
          <ul>
            <li>
              <div>{{ t('account.Depósito') }}</div>
              <div>{{ moneyFormat(store.state.user.total_money) }}</div>
            </li>
            <li>
              <div>{{ t('account.Retirar') }}</div>
              <div>{{ moneyFormat(store.state.user.total_withdraw) }}</div>
            </li>
            <li>
              <div>{{ t('account.Aposta') }}</div>
              <div>{{ moneyFormat(store.state.user.total_bet) }}</div>
            </li>
            <li>
              <div>{{ t('account.Bônus') }}</div>
              <div>{{ moneyFormat(store.state.user.give_money) }}</div>
            </li>
            <li>
              <div>{{ t('account.Comissão') }}</div>
              <div>{{ moneyFormat(store.state.user.total_commission) }}</div>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="favorite_games">
      <div class="favorite_games_column">
        <img src="@assets/images/account/like.png" alt="">
        <span>{{ t('account.JogosFavoritos') }}</span>
      </div>
    </div>
    <flag-game />


    <set-avatar v-if="comShowIdx == 0" />
    <set-phone-number v-else-if="comShowIdx == 1" />
    <set-email v-else-if="comShowIdx == 2" />
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { copy, getImageUrl, levelPercent, moneyFormat } from "@/utils/baseFun";
import setPhoneNumber from "./setPhoneNumber.vue";
import setEmail from "./setEmail.vue";
import setAvatar from "./setAvatar.vue";
import { useI18n } from "vue-i18n";
import withdrawColumnAmountInfo from "@views/deposit/components/withdrawColumnAmountInfo.vue"
import flagGame from "@views/home/homeType/flag.vue"

export default defineComponent({
  name: "myAccount",
  components: { setPhoneNumber, setAvatar, setEmail, withdrawColumnAmountInfo, flagGame },
  setup() {
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const { proxy } = getCurrentInstance() as any;
    const state = reactive({
      activeName1: "1",
      activeName2: "0",
      comShowIdx: -1,
      vip_conf: store.state.conf.all_conf.vip_conf[store.state.user.vip_lv],
    });

    proxy.$mitt.on("showCom", (val: number) => {
      state.comShowIdx = val;
    });

    const routerJump = (url: string) => {
      router.push(url);
    };

    const bindingClick = () => {
      if (!store.state.user['email']) state.comShowIdx = 2
      else state.comShowIdx = 1
    }
    return {
      ...toRefs(state),
      store,
      t,
      getImageUrl,
      copy,
      levelPercent,
      routerJump,
      bindingClick,
      moneyFormat
    };
  },
});
</script>
<style  lang="scss" scoped>
.myAccount {
  .myAccount_box {
    margin-bottom: 32px;
    display: flex;
    gap: 17px;

    .user_box,
    .account_total_box {
      width: 389px;
      font-size: 14px;
      color: #B2B6C5;
      box-sizing: border-box;
    }

    .user_box {
      padding: 16px 20px;
      background: #202431;
      border-radius: 12px;

      .edit_img {
        text-align: right;

        .svg-icon {
          cursor: pointer;
          width: 20px;
          height: 20px;
        }
      }

      .user_avatar {
        margin-bottom: 44px;
        text-align: center;

        img {
          margin-bottom: 20px;
          width: 92px;
        }
      }

      .user_info {
        .user_info_box {
          display: flex;
          align-items: center;
          margin-bottom: 16px;

          .label {
            margin-right: 12px;
            width: 94px;
            flex-shrink: 0;
            white-space: nowrap;
            text-align: right;
          }

          .info {
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 36px;
            padding: 0 12px;
            width: 100%;
            background: #1B1F29;
            border-radius: 6px;
            border: 1px solid rgba(178, 182, 197, 0.3);
            overflow-x: scroll;


            .svg-icon {
              cursor: pointer;
              width: 17px;
              height: 17px;
            }
          }
        }
      }

      .user_date {
        text-align: right;
      }
    }

    .account_total_box {
      :deep(.withdrawColumnAmountInfo) {
        padding: 25px 20px;
        background: #202431;
        border-radius: 12px;
        border: none;

        .r_box {
          gap: 20px;
        }
      }

      .account_total_box_info {
        height: 200px;
        padding: 16px 20px;
        background: #202431;
        border-radius: 12px;
        box-sizing: border-box;

        .account_total_box_info_title {
          margin-bottom: 15px;
          font-size: 16px;
          color: #FFFFFF;
        }

        ul {
          li {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;

            div {}
          }
        }
      }
    }
  }

  .favorite_games {
    margin-bottom: 15px;

    .favorite_games_column {
      display: flex;
      align-items: center;

      img {
        margin-right: 4px;
        width: 40px;
      }

      span {
        font-size: 18px;
        font-weight: 600;
        color: #98ABD0;
      }
    }
  }

  :deep(.gameOutBox) {
    border-radius: 12px;
  }
}

@media (max-width: 768px) {
  .myAccount {
    margin-bottom: 18px;

    .myAccount_box {
      flex-direction: column;
      gap: 12px;

      .user_box,
      .account_total_box {
        width: 100%;
        font-size: 13px;
      }

      .user_box {
        position: relative;
        padding: 16px 12px;
        background: #202431;
        border-radius: 8px;

        .edit_img {
          .svg-icon {
            position: absolute;
            top: 14px;
            right: 18px;
            width: 18px;
            height: 18px;
          }
        }

        .user_avatar {
          margin-bottom: 19px;

          img {
            margin-bottom: 12px;
            width: 62px;
          }
        }

        .user_info {
          .user_info_box {
            margin-bottom: 10px;

            .label {
              margin-right: 17px;
              width: 80px;
            }

            .info {
              display: flex;
              align-items: center;
              justify-content: space-between;
              height: 30px;

              .svg-icon {
                cursor: pointer;
                width: 17px;
                height: 17px;
              }
            }
          }
        }

        .user_date {
          text-align: right;
        }
      }

      .account_total_box {
        :deep(.withdrawColumnAmountInfo) {
          padding: 14px 12px;

          .r_box {
            gap: 12px;
          }
        }

        .account_total_box_info {
          height: auto;
          padding: 14px 15px;

          .account_total_box_info_title {
            margin-bottom: 11px;
            font-size: 14px;
          }
        }
      }
    }
  }

  .favorite_games {
    margin-bottom: 8px;

    .favorite_games_column {
      img {
        margin-right: 5px;
        width: 28px;
      }

      span {
        font-size: 14px;
      }
    }
  }

  :deep(.gameOutBox) {
    border-radius: 8px;
  }
}
</style>
