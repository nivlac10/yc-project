<template>
  <div class="vipBox">
    <div class="level_flag_top" v-if="isSign">
      <div class="finish_level" v-show="finishFlag">
        {{ t("vipBonus.FINISH") }}
      </div>
      <div class="currey_level" v-show="currentLevelFlag">
        {{ t("vipBonus.MYLEVEL") }}
      </div>
      <div class="next_level" v-show="nextLevelFlag">
        {{ t("vipBonus.NEXTLEVEL") }}
      </div>
    </div>
    <div class="level_img">
      <img :src="getImageUrl(`vipBonus/level_${(data as any).vip_lv}.png`)" alt="" /> 
    </div>
    <div class="title">{{ levelName((data as any).vip_lv) }}</div>
    <div :class="{ bg_box: !showBgBox }">
      <div :class="{ bg_box: showBgBox }">
        <div class="vip_column_box">
          {{ t("vipBonus.LEAVEL") }} {{ (data as any).vip_lv }}
        </div>
        <div class="progress_false" v-if="!isSign || !showBgBox">
          <div class="txt">
            <div>{{ t("vipBonus.Recharge") }}</div>
            <div>{{ (data as any).recharge }} {{ t("base.currency") }}</div>
          </div>
          <div class="txt">
            <div>{{ t("vipBonus.BetAmount") }}</div>
            <div>{{ (data as any).bet }} {{ t("base.currency") }}</div>
          </div>
        </div>
        <div class="progress_true" v-else>
          <div class="txt">
            <div>{{ t("vipBonus.Recharge") }}</div>
          </div>
          <el-progress class="el-progress_box" :stroke-width="16" :percentage="rechargePercent" status="exception">
            <span>{{ store.state.user.total_money }}/{{ rechargeNextLvVal }}</span>
          </el-progress>
          <div class="txt">
            <div>{{ t("vipBonus.BetAmount") }}</div>
          </div>
          <el-progress class="el-progress_box" :stroke-width="16" :percentage="betPercent" status="exception">
            <span>{{ store.state.user.total_bet }}/{{ betNextLvVal }}</span>
          </el-progress>
        </div>
      </div>
      <!-- <div :class="{ bg_box: showBgBox }">
        <div class="column_title">{{ t("vipBonus.VIPBonus") }}</div>
        <div class="txt">
          <div>{{ t("vipBonus.LevelBonus") }}</div>
          <div>{{ data.day_bonus }} {{t('base.currency')}}</div>
        </div>
        <div class="txt">
          <div>{{ t("vipBonus.WeeklyBonus") }}</div>
          <div>{{ data.week_bonus }} {{t('base.currency')}}</div>
        </div>
        <div class="txt">
          <div>{{ t("vipBonus.MonthlyBonus") }}</div>
          <div>{{ data.month_bonus }} {{t('base.currency')}}</div>
        </div>
      </div> -->
      <div :class="{ bg_box: showBgBox }">
        <div class="column_title">{{ t("vipBonus.Memberprivilege") }}</div>
        <div class="txt">
          <div>{{ t("vipBonus.WithdrawFee") }}</div>
          <div>{{ (data as any).pay_fee }}%</div>
        </div>
        <div class="txt">
          <div>{{ t("vipBonus.DailyWithdrawals") }}</div>
          <div>{{ (data as any).day_max_withdraw }}</div>
        </div>
        <div class="txt">
          <div>{{ t("vipBonus.SingleWithdrawalLimit") }}</div>
          <div>{{ (data as any).max_withdraw }}</div>
        </div>
        <div class="txt">
          <div>{{ t("vipBonus.NumberOfWithdrawalsPer") }}</div>
          <div>{{ (data as any).withdraw_num }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { getImageUrl, levelName, toPercent } from "@/utils/baseFun";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import {
  reactive,
  toRefs,
  getCurrentInstance,
  defineComponent,
  onMounted,
  computed,
} from "vue";
export default defineComponent({
  name: "vipBox",
  props: {
    data: Object,
  },
  setup(props) {
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      isSign: store.state.user.token,
      data: props.data,
      finishFlag: store.state.user.vip_lv > (props.data as any).vip_lv,
      currentLevelFlag: store.state.user.vip_lv == (props.data as any).vip_lv,
      nextLevelFlag: store.state.user.vip_lv + 1 == (props.data as any).vip_lv,
      rechargePercent: 0,
      rechargeNextLvVal: 0,
      betPercent: 0,
      betNextLvVal: 0,
    });
    const showBgBox = computed(() => {
      return (
        (state.finishFlag || state.currentLevelFlag || state.nextLevelFlag) &&
        state.isSign
      );
    });

    // 百分比
    const percentFun = () => {
      const vip_conf = store.state.conf.all_conf.vip_conf;
      const vip_lv = store.state.user.vip_lv;
      var idx = 0;

      if (state.finishFlag) {
        idx = (state.data as any).vip_lv + 1;
      } else if (state.currentLevelFlag) {
        if (vip_lv >= vip_conf.length - 1) idx = vip_lv;
        else idx = vip_lv + 1;
      } else if (state.nextLevelFlag) {
        if (vip_lv >= vip_conf.length - 1) idx = vip_lv;
        else {
          if (store.state.user.vip_lv + 1 == (props.data as any).vip_lv) {
            idx = (state.data as any).vip_lv + 1;
          }
        }
      } else return;

      state.rechargePercent = toPercent(
        store.state.user.total_money,
        vip_conf[idx].recharge
      );
      state.rechargeNextLvVal = vip_conf[idx].recharge;

      state.betPercent = toPercent(
        store.state.user.total_bet,
        vip_conf[idx].bet
      );
      state.betNextLvVal = vip_conf[idx].bet;
    };
    percentFun();

    return { ...toRefs(state), store, t, levelName, getImageUrl, showBgBox };
  },
});
</script>
<style  lang="scss" scoped>
.vipBox {
  padding: 22px 11px 15px 11px;
  border-radius: 14px;
  background: var(--theme-box-background);
  overflow: hidden;

  .level_flag_top {

    .finish_level,
    .currey_level,
    .next_level {
      margin: -22px -11px 20px -11px;
      padding: 5px 0 10px 18px;
      font-size: 23px;
      font-weight: bold;
      font-style: italic;
      color: var(--auxiliary-font-color-12);
    }

    .finish_level {
      color: var(--theme-font-color-fff);
      background: var(--auxiliary-background-12);
    }

    .currey_level {
      background: var(--auxiliary-background-9);
    }

    .next_level {
      background: var(--auxiliary-background-10);
    }
  }

  .level_img {
    display: flex;
    justify-content: center;

    img {
      width: 68px;
      height: 60px;
    }
  }

  .title {
    padding: 10px 0;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    color: var(--theme-font-color-fff);
  }

  .bg_box {
    overflow: hidden;
    padding: 0 11px 10px 11px;
    margin-bottom: 16px;
    background: var(--auxiliary-background-8);
    border-radius: 12px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

    .vip_column_box {
      margin: 0 -11px 12px -11px;
      height: 28px;
      text-align: center;
      line-height: 28px;
      font-size: 14px;
      font-weight: 500;
      color: var(--auxiliary-font-color-9);
      background: var(--auxiliary-background-7);
    }

    .column_title {
      padding: 15px 0;
      font-size: 14px;
      font-weight: 500;
      color: var(--auxiliary-font-color-11);
    }

    .progress_false,
    .progress_true {
      :deep(.el-progress) {
        margin-bottom: 15px;
      }
    }

    .txt {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;

      div:nth-child(1) {
        font-size: 13px;
        color: var(--auxiliary-font-color-9);
      }

      div:nth-child(2) {
        font-size: 13px;
        font-weight: 500;
        color: var(--theme-font-color-fff);

        &.color_1 {
          color: var(--auxiliary-font-color-7);
        }
      }
    }
  }
}
</style>
