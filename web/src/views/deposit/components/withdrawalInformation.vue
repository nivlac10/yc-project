<template>
  <div class="withdrawalInformation">
    <div class="withdraw_mode">
      <div class="txt_box">
        <div class="l_box">
          <div class="header_box">
            <div>Conta de PX</div>
            <div>
              <el-popover :placement="store.state.status.isPc ? 'right' : 'bottom'" trigger="click" width="329px"
                popper-class="el_popover_style" :teleported="false">
                <template #reference>
                  <van-icon name="question" />
                </template>
                <div class="popover_content">
                  <div class="popover_content_header">Conta de PX</div>
                  <div class="popover_content_txt">
                    {{ t('deposit.popover_Filling') }}
                  </div>
                </div>
              </el-popover>
            </div>
          </div>
          <div class="c_box">
            <div>
              <span>{{t('refer.Nome')}}:</span>
              <span class="text_hiding">{{ store.state.user.username }}</span>
            </div>
            <div>
              <span>TIPO：</span>
              <span class="text_hiding">CPF</span>
            </div>
            <div>
              <span>CPF：</span>
              <span class="text_hiding">{{ store.state.user.CPF }}</span>
            </div>
          </div>
          <div class="setting_btn" @click="settings(1)">{{ t('base.SETTINGS') }} ></div>
        </div>
        <div class="r_box">
          <div class="header_box">
            <div>{{ t('deposit.popover_WithdrawalQuota') }}</div>
            <div>
              <el-popover :placement="store.state.status.isPc ? 'right' : 'bottom'" trigger="click" width="329px"
                popper-class="el_popover_style" :teleported="false">
                <template #reference>
                  <van-icon name="question" />
                </template>
                <div class="popover_content">
                  <div class="popover_content_header">{{ t('deposit.popover_WithdrawalQuota') }}</div>
                  <div class="popover_content_txt">
                    {{ t('deposit.popover_Withdrawal') }}
                  </div>
                  <div class="popover_content_btn"
                    @click="$router.push('/vipBonus'), store.dispatch('status/setDepositShow', false)">{{
                      t('deposit.READMORE') }} ></div>
                </div>
              </el-popover>
            </div>
          </div>
          <div class="c_box">
            <div>
              <div>{{ t('vipBonus.DailyWithdrawals') }}</div>
              <div>{{ store.state.conf.all_conf.vip_conf[store.state.user.vip_lv].day_max_withdraw }}</div>
            </div>
            <div>
              <div>{{ t('vipBonus.SingleWithdrawalLimit') }}</div>
              <div>{{ store.state.conf.all_conf.vip_conf[store.state.user.vip_lv].max_withdraw }}</div>
            </div>
            <div>
              <div>{{ t('vipBonus.withdrawalsperDay') }}</div>
              <div>{{ store.state.conf.all_conf.vip_conf[store.state.user.vip_lv].withdraw_num }}</div>
            </div>
          </div>
          <!-- <div class="setting_btn" @click="$router.push('/vipBonus'), store.dispatch('status/setDepositShow', false)">{{ t('deposit.READMORE') }} ></div> -->
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
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "withdrawalInformation",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({});

    const settings = (val: number) => {
      proxy.$mitt.emit("depositComShow", val);
    };
    return {
      ...toRefs(state),
      t,
      store,
      settings,
    };
  },
});
</script>
<style  lang="scss" scoped>
.withdrawalInformation {
  margin-bottom: 16px;

  .withdraw_mode {
    .txt_box {
      display: flex;
      margin-right: 16px;
      gap: 16px;

      .l_box,
      .r_box {
        width: 50%;
        flex-shrink: 0;
        position: relative;
        background: var(--auxiliary-background-14);
        border-radius: 0px 0px 8px 8px;

        .header_box {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 6px 15px;
          background: var(--auxiliary-background-23);
          border-radius: 8px 8px 0px 0px;

          >div:nth-child(1) {
            font-size: 17px;
            font-weight: 500;
            color: #FFFFFF;
          }

          >div:nth-child(2) {
            cursor: pointer;
            color: var(--auxiliary-font-color-9);
            font-size: 30px;
          }
        }

        .c_box {
          height: 100%;
          padding: 16px 15px 12px 15px;
          box-sizing: border-box;
        }

        .setting_btn {
          cursor: pointer;
          position: absolute;
          right: 15px;
          bottom: 12px;
          font-size: 14px;
          font-weight: 500;
          color: var(--auxiliary-font-color-27);
        }
      }

      .l_box {
        .c_box {
          >div {
            display: flex;
            margin-bottom: 12px;

            span:nth-child(1) {
              font-size: 18px;
              font-weight: 500;
              color: var(--auxiliary-font-color-14);
            }

            span:nth-child(2) {
              display: inline-block;
              width: 100%;
              font-size: 18px;
              font-weight: 500;
              color: var(--auxiliary-font-color-7);
            }
          }
        }
      }

      .r_box {
        .c_box {
          >div {
            div {
              margin-bottom: 12px;
            }

            div:nth-child(1) {
              color: var(--auxiliary-font-color-14);
              font-size: 16px;
              font-weight: 500;
            }

            div:nth-child(2) {
              color: var(--theme-font-color-fff);
              font-size: 15px;
              font-weight: 500;
            }
          }
        }
      }
    }
  }

  // :deep(.el_popover_style) {
  //   background: var(--auxiliary-background-14);
  //   border: none;
  //   border-radius: 12px;

  //   .popover_content {
  //     .popover_content_header {
  //       margin-bottom: 12px;
  //       font-size: 20px;
  //       font-weight: bold;
  //       color: var(--theme-font-color-fff);
  //     }

  //     .popover_content_txt {
  //       font-size: 14px;
  //       font-weight: 400;
  //       color: var(--auxiliary-font-color-9);
  //       line-height: 16px;
  //     }

  //     .popover_content_btn {
  //       text-align: right;
  //       cursor: pointer;
  //       font-size: 14px;
  //       font-weight: 500;
  //       color: var(--auxiliary-font-color-27);
  //     }
  //   }

  //   .el-popper__arrow {
  //     &::before {
  //       background: var(--auxiliary-background-14);
  //       border: none;
  //     }
  //   }
  // }
}

@media (max-width: 768px) {
  .withdrawalInformation {
    .withdraw_mode {
      .txt_box {
        margin-right: 11px;
        gap: 11px;

        .l_box,
        .r_box {
          width: 50%;
          flex-shrink: 0;
          position: relative;
          background: var(--auxiliary-background-14);
          border-radius: 0px 0px 8px 8px;

          .header_box {
            padding: 6px 9px;

            >div:nth-child(1) {
              font-size: 12px;
            }

            >div:nth-child(2) {
              font-size: 20px;
            }
          }

          .c_box {
            height: 100%;
            padding: 12px 9px 12px 9px;
            box-sizing: border-box;
          }

          .setting_btn {
            right: 9px;
            font-size: 12px;
          }
        }

        .l_box {
          .c_box {
            >div {
              display: flex;
              margin-bottom: 12px;

              span:nth-child(1) {
                font-size: 12px;
              }

              span:nth-child(2) {
                font-size: 12px;
              }
            }
          }
        }

        .r_box {
          .c_box {
            >div {
              div {
                margin-bottom: 6px;
              }

              div:nth-child(1) {
                font-size: 12px;
              }

              div:nth-child(2) {
                font-size: 12px;
              }
            }
          }
        }
      }
    }

    // :deep(.el_popover_style) {
    //   border-radius: 6px;

    //   .popover_content {
    //     .popover_content_header {
    //       margin-bottom: 9px;
    //       font-size: 12px;
    //     }

    //     .popover_content_txt {
    //       font-size: 12px;
    //       line-height: 14px;
    //     }

    //     .popover_content_btn {
    //       font-size: 12px;
    //     }
    //   }
    // }
  }
}
</style>
