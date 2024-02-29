<template>
  <div class="supplyCrate">
    <div class="content_box">
      <div class="title_box">
        <div class="column_box">
          <div>
            <div :class="{ money_txt: true, txt_true: loss_money > 0, txt_false: loss_money < 0 }">
              {{ t('base.currencySymbol') }} {{ loss_money }}
            </div>
            <div class="t_box">
              <span>{{ t('supplyCrate.PerdadeOntem') }}</span>
            </div>
          </div>
          <div>
            <div :class="{ money_txt: true, txt_true: bonus > 0, txt_false: bonus < 0 }">
              {{ t('base.currencySymbol') }} {{ bonus }}
            </div>
            <div class="t_box">
              <span>{{ t('supplyCrate.FundodeAjudadeHoje') }}</span>
            </div>
          </div>
        </div>
        <div class="btn">
          <div @click="jump(comShow)">
            {{ t('supplyCrate.História') }}
          </div>
          <div :class="{ btn_g: receiveStatus == 1 }" @click="receiveRewards">
            {{ t('btnName.Receber') }}
          </div>
        </div>
      </div>
      <div v-if="comShow == 0">
        <!-- supplyCrate -->
        <div class="tab_column">
          <div>{{ t('supplyCrate.AmountOfLoss') }}</div>
          <div>{{ t('supplyCrate.Bonus') }}</div>
        </div>
        <div class="list">
          <ul>
            <li v-for="(item, index) in list as any" :key="item + index">
              <div>≥ {{ item.loss_money }} {{ t('base.currency') }}</div>
              <div>{{ item.bonus }} {{ t('base.currency') }}</div>
            </li>
          </ul>
        </div>
      </div>
      <historical-record v-if="comShow == 1" />

    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { UserService } from "@/api/user";
import { debounce, getUserInfo, toPercent } from "@/utils/baseFun";
import historicalRecord from "./historicalRecord.vue"
export default defineComponent({
  name: "supplyCrate",
  components: { historicalRecord },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      comShow: 0,
      tabIdx: 0,
      list: [
        { bonus: 3, loss_money: -50 },
        { bonus: 5, loss_money: -100 },
        { bonus: 15, loss_money: -300 },
        { bonus: 50, loss_money: -1000 },
        { bonus: 150, loss_money: -3000 },
        { bonus: 300, loss_money: -6000 },
        { bonus: 500, loss_money: -10000 },
        { bonus: 1500, loss_money: -30000 },
        { bonus: 2500, loss_money: -50000 },
        { bonus: 5000, loss_money: -100000 }
      ],
      receiveStatus: 0,
      bonus: 0,
      loss_money: 0,
    });
    const closeCom = () => {
      store.dispatch('status/setSupplyCrateShow', false)
    }
    const jump = (val: number) => {
      if (val == 1) val = 0;
      else if (val == 0) val = 1;
      console.log(val);

      state.comShow = val;
    }


    const getList = () => {
      UserService.get_loss_money_bouns_list().then(res => {
        state.list = res.data.data
        state.receiveStatus = res.data.state
        state.bonus = res.data.bonus
        state.loss_money = res.data.loss_money
      })
    }
    getList()

    // 领取奖励
    const receiveRewards = () => {
      if (state.receiveStatus != 1) return
      const fun = () => {
        UserService.receive_loss_bonus().then(res => {
          getUserInfo()
          getList()
        })
      }
      debounce(fun)
    }
    return { ...toRefs(state), store, t, jump, closeCom, receiveRewards };
  },
});
</script>
<style  lang="scss" scoped>
.supplyCrate {
  .content_box {
    position: relative;
    padding: 33px 22px 20px 22px;
    width: 100%;
    border-radius: 16px;
    background: var(--theme-box-background);
    box-sizing: border-box;

    .title_box {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      column-gap: 10px;
      margin: 35px 0 35px 0;
    }

    .column_box {
      display: flex;
      gap: 18px;

      >div {
        width: 100%;
        padding: 8px 0 15px 11px;
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.6);

        .t_box {
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 5px;

          img {
            margin-right: 19px;
            width: 23px;
          }

          span {
            font-size: 13px;
            font-weight: 500;
            color: var(--auxiliary-font-color-9);
          }
        }

        .money_txt {
          text-align: center;
          font-size: 32px;
          line-height: 38px;
          font-weight: bold;
          color: var(--auxiliary-font-color-20);

          &.txt_true {
            color: var(--auxiliary-font-color-7);
          }

          &.txt_false {
            color: var(--auxiliary-font-color-22);
          }
        }
      }
    }

    .btn {
      display: flex;
      gap: 18px;
      justify-content: space-around;

      div {
        cursor: pointer;
        width: 226px;
        height: 58px;
        // padding: 12px 0;
        border-radius: 12px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;

      }

      div:nth-child(1) {
        color: var(--theme-font-color-fff);
        background: var(--auxiliary-background-18);
      }

      div:nth-child(2) {
        color: var(--auxiliary-font-color-21);
        background: var(--auxiliary-background-20);

        &.btn_g {
          background: var(--auxiliary-font-color-7);
        }
      }
    }

    .tab_column {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      padding: 10px 0;
      background: #2D3144;
      border-radius: 8px 8px 0px 0px;

      div {
        width: 100%;
        font-size: 20px;
        font-weight: 500;
        color: var(--auxiliary-font-color-9);
        text-align: center;
      }
    }

    .list {
      margin-bottom: 10px;
      border-radius: 0px 0px 8px 8px;
      background: #2D3144;

      ul {
        li {
          display: flex;
          justify-content: space-between;
          margin-bottom: 8px;
          padding: 8px 0;
          border-radius: 8px;

          div {
            width: 100%;
            font-size: 16px;
            font-weight: 500;
            color: var(--auxiliary-font-color-9);
            text-align: center;
          }

          div:nth-child(2) {
            color: var(--auxiliary-font-color-7);
          }
        }
      }
    }


  }
}

@media (max-width: 768px) {
  .supplyCrate {
    .content_box {
      padding: 18px 20px 16px 20px;
      border-radius: 0;

      .title_box {
        display: block;
      }

      .column_box {
        width: 100%;

        >div {
          padding: 6px 0 15px 6px;

          .t_box {

            img {
              margin-right: 9px;
              width: 16px;
            }

            span {
              font-size: 12px;
            }
          }

          .money_txt {
            font-size: 17px;
          }
        }
      }

      .btn {
        padding: 12px 0 16px 0;
        width: 100%;

        div {
          height: 26px;
          padding: 11px 0;
          font-size: 13px;
        }
      }

      .tab_column {
        div {
          font-size: 15px;
        }
      }

      .list {
        ul {
          li {
            div {
              font-size: 12px;
            }
          }
        }
      }


    }
  }
}
</style>
