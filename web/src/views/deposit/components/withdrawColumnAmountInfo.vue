<template>
  <div class="withdrawColumnAmountInfo">
    <div class="withdraw_amount">
      <div class="l_box">
        <div>{{ t('deposit.Valorsacável') }}</div>
        <div>{{ moneyFormat(setWithdrawableAmount) }}</div>
      </div>
      <div class="r_box">
        <div>
          <span>{{ t('deposit.PrecisaAposta') }}</span>
          <span>{{ percentage }}%</span>
        </div>
        <el-progress class="el-progress_box" :stroke-width="18" :percentage="percentage" status="exception"
          color="#4181EE">
          <!-- <span>{{ percentage }}%</span> -->
          <span>
            {{ moneyFormat(remain_code_amount) }}/{{ moneyFormat(store.state.user.need_code_amount) }}
          </span>
        </el-progress>
        <div class="limpar_btn_max_box">
          <!-- <div class="view_mais" @click="jump"><span>Ver Mais</span></div> -->
          <div class="limpar_btn" @click="user_code_empty"
            :style="store.state.user.money <= 0.5 && store.state.user.remain_code_amount > 0 ? 'background: #C01544;' : 'background: rgba(60,62,80,0.5);'">
            <div></div>
            <span>{{ t('deposit.Zerar') }}</span>
            <div>
              <!-- :width="store.state.status.isPc ? '334px' : ''"> -->
              <el-popover placement="top" trigger="click" popper-class="el_popover_style" :teleported="false" width="80%">
                <template #reference>
                  <van-icon name="question" />
                </template>
                <div class="popover_content">
                  <div class="popover_content_title">{{ t('deposit.DescriçãodeZerar') }}</div>
                  <div class="popover_content_txt">{{ t('deposit.popover_txt') }}
                  </div>
                </div>
              </el-popover>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import {
  reactive,
  toRefs,
  getCurrentInstance,
  defineComponent,
  computed,
} from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { DepositAndWithdraw } from "@/api/DepositAndWithdraw";
import { debounce, SuccessNotiFun, getUserInfo, getUserInfoNoLoad, moneyFormat } from "@/utils/baseFun";
import withdrawalInformation from "./withdrawalInformation.vue";
import { ElLoading } from 'element-plus'
import { useI18n } from "vue-i18n";
import { UserService } from "@/api/user";
export default defineComponent({
  name: "withdrawColumnAmountInfo",
  components: { withdrawalInformation },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      percentage: 0,
      remain_code_amount: 0
    });

    // 可提现金额
    const setWithdrawableAmount = computed(() => {
      if (store.state.user.remain_code_amount >= 0)
        return store.state.user.with_money;
      else return 0;
    });

    // 设置进度条
    const setPercentage = () => {
      var now_code =
        store.state.user.need_code_amount - store.state.user.remain_code_amount;
      if (store.state.user.remain_code_amount <= 0) {
        state.percentage = 100;
      } else if (now_code <= 0) {
        state.percentage = 0;
        now_code = 0;
      } else {
        let rate = store.state.user.need_code_amount / 100;
        state.percentage = Math.round(now_code / rate);
      }
      state.remain_code_amount = now_code == 0 ? now_code : now_code.toFixed(2) as any
    };
    function user_code_empty() {
      if (store.state.user.money <= 0.5 && store.state.user.remain_code_amount > 0) {
        UserService.user_code_empty().then((res) => {
          if (res.data.code == 1) {
            // store.state.status.depositShow = false
            getUserInfo()
          }
        })
      }
    }
    setPercentage();
    // getUserInfoNoLoad()

    const jump = () => {
      proxy.$mitt.emit("depositComShow", 2);
    }

    return {
      ...toRefs(state),
      store,
      t,
      setWithdrawableAmount,
      user_code_empty,
      moneyFormat,
      jump
    };
  },
});
</script>
<style  lang="scss" scoped>
.popover_content {
  .popover_content_title {
    margin-bottom: 8px;
    font-size: 14px;
    font-weight: bold;
    color: #F3B343;
  }

  .popover_content_txt {
    // margin-bottom: 14px;
    font-size: 12px;
    color: #B2B6C5;
    line-height: 16px;
    white-space: pre-wrap;
    // word-break: break-word;
    // word-wrap: break-word;
  }
}

.withdrawColumnAmountInfo {
  margin-bottom: 18px;
  padding: 11px 13px;
  border: 1px solid #4C4F5D;
  border-radius: 6px;
  white-space: normal;

  .withdraw_amount {
    display: flex;
    flex-direction: column;
    gap: 15px;

    >div {
      padding: 11px 15px;
      border-radius: 6px;
      text-align: center;
      box-sizing: border-box;
      width: 100%;
    }

    .l_box {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background-color: #2F3445;
      font-size: 14px;
      background: var(--theme-button-background);

      div:nth-child(1) {
        white-space: normal;
        color: #B2B6C5;
      }

      div:nth-child(2) {
        color: #82F44E;
      }
    }

    .r_box {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
      padding: 0;

      >div {
        display: flex;
        justify-content: space-between;

        >span {
          font-size: 14px;
          font-weight: 500;
          color: var(--auxiliary-font-color-9);
        }
      }

      .el-progress_box {}
    }
  }
}

.limpar_btn_max_box {
  display: flex;
  justify-content: flex-end !important;
  gap: 8px;

  // justify-content: ju;
  .view_mais {
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    font-size: 12px;
    color: #FFFFFF;
    // line-height: 24px;
    background: rgba(65, 129, 238, 0.5);
    border-radius: 17px;
    border: 1px solid #4181EE;
  }

  .limpar_btn {
    flex-shrink: 0;
    width: 116px;
    background-color: #3C3E50;
  }

  // display: grid !important;
  // grid-template-columns: 1fr 1fr;
}

.limpar_btn {
  padding: 5px;
  display: flex;
  // justify-content: center;
  border-radius: 100px;
  // justify-content: space-evenly;
  justify-content: space-between;
  align-items: center;
  // width: 100%;

  span {
    color: #B2B6C5;
    font-size: 14px;
    font-weight: 600;
  }

  div {
    color: var(--auxiliary-font-color-9);
  }
}



@media (max-width: 768px) {
  .withdrawColumnAmountInfo {
    padding: 11px 8px;

    .withdraw_amount {
      >div {
        padding: 11px 8px;
      }

      .l_box {
        font-size: 12px;
      }

      .r_box {
        >div {
          >span {
            font-size: 12px;
          }
        }
      }
    }
  }
}
</style>
