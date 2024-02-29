<template>
  <div class="dailyBettingBonus">
    <div class="t_img">
      <img src="@assets/images/dailyBettingBonus/Group.png" alt="">
    </div>
    <div class="content_box">
      <div class="list">
        <div class="box">
          <ul>
            <li v-for="(item, index) in inProgressList" :key="index">
              <div class="c_box">
                <div class="describe">Aposta Válida Acumulativa {{ item.need_code_amount }}</div>
                <el-progress class="el-progress_box" :stroke-width="store.state.status.isPc ? 24 : 12"
                  :color="needAmount(item) == 100 ? '#1CB83D' : '#F6AF2D'" :percentage="needAmount(item)"
                  status="exception">
                  <span>
                    {{ bet_code < item.need_code_amount ? bet_code : item.need_code_amount }}/{{ item.need_code_amount }}
                      </span>
                </el-progress>
              </div>
              <div class="btn_box">
                <div class="l_box">
                  <img src="@assets/images/dailyBettingBonus/Group_g.png" alt="">
                  <div>{{ t('base.currencySymbol') }}{{ item.money }}</div>
                </div>
                <div
                  :class="{ r_box: true, sl_box_shadow: true, r_box_claim: item.state == 1, r_box_finish: item.state == 2 }"
                  @click="claimTask(item)">
                  {{
                    item.state == 0 ? t('dailyBettingBonus.PLAYGAME')
                    : item.state == 1 ? t('dailyBettingBonus.CLAIM')
                      : t('dailyBettingBonus.RECEIVED')
                  }}
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <activities />
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { UserService } from "@/api/user";
import { getUserInfo, toPercent } from "@/utils/baseFun";
import activities from "./activities.vue";

export default defineComponent({
  name: "dailyBettingBonus",
  components: { activities },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      tabIdx: 0,
      tabList: computed(() => [t('dailyBettingBonus.INPROGRESS'), t('dailyBettingBonus.FINISH')]),
      inProgressList: [
        { id: 1, money: 1, need_code_amount: 500, state: 0 },
        { id: 2, money: 2, need_code_amount: 1000, state: 0 },
        { id: 3, money: 3, need_code_amount: 2000, state: 0 },
        { id: 4, money: 7, need_code_amount: 5000, state: 0 },
        { id: 5, money: 17, need_code_amount: 10000, state: 0 },
        { id: 6, money: 27, need_code_amount: 20000, state: 0 },
        { id: 7, money: 77, need_code_amount: 50000, state: 0 },
        { id: 8, money: 127, need_code_amount: 100000, state: 0 },
        { id: 9, money: 177, need_code_amount: 200000, state: 0 },
        { id: 10, money: 277, need_code_amount: 300000, state: 0 }
      ],
      finishList: [],
      bet_code: 0,
    });
    const getList = () => {
      UserService.get_bet_day_task_list().then(res => {
        state.inProgressList = []
        state.finishList = []
        state.bet_code = res.data.bet_code
        state.inProgressList = res.data.data
      })
    }
    getList()

    const needAmount = (item) => {
      return toPercent(state.bet_code, item.need_code_amount)
    }

    const claimTask = (item) => {
      if (item.state == 0) {
        router.push('/')
        store.state.status.dailyBettingBonusShow = false
        return
      } else if (item.state == 1)
        UserService.receive_bet_day_task_bonus({ id: item.id }).then(res => {
          if (res.data.code == 1) {
            getList()
            getUserInfo()
          }
        })
      else return
    }
    const jump = () => {
      proxy.$mitt.emit("comShow", 1)
    }
    return { ...toRefs(state), store, t, jump, claimTask, needAmount, };
  },
});
</script>
<style  lang="scss" scoped>
.dailyBettingBonus {
  .t_img {
    margin-bottom: 24px;

    img {
      width: 100%;
    }
  }

  .content_box {
    margin-bottom: 24px;
    padding: 32px 34px;
    width: 100%;
    border-radius: 24px;
    background: #202330;
    box-sizing: border-box;

    .list {
      .box {
        ul {
          li {
            display: flex;
            gap: 100px;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding: 23px 16px;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(90, 70, 158, 0.3) 0%, #5A469E 100%);

            &:nth-last-child(1) {
              margin-bottom: 0;
            }

            .c_box {
              margin-right: 18px;
              width: 60%;

              .describe {
                margin-bottom: 10px;
                font-weight: 500;
                color: var(--theme-font-color-fff);
                font-size: 20px;
              }

              :deep(.el-progress_box) {
                .el-progress-bar__outer {
                  background: var(--theme-box-background);

                  .el-progress-bar__inner {
                    background: var(--auxiliary-font-color-19);
                  }
                }

                .el-progress__text {
                  font-size: 18px !important;
                }
              }
            }

            .btn_box {
              display: flex;
              align-items: center;
              justify-content: space-between;
              width: 40%;

              .l_box {
                display: flex;
                align-items: center;

                img {
                  margin-right: 6px;
                  width: 40px;
                }

                div {
                  font-size: 24px;
                  font-weight: bold;
                  color: var(--theme-font-color-fff);
                }
              }


              .r_box {
                cursor: pointer;
                padding: 12px 8px;
                min-width: 76px;
                font-size: 22px;
                font-weight: bold;
                color: var(--auxiliary-font-color-10);
                text-align: center;

                &.r_box_claim {
                  background: #52FB59 !important;
                  box-shadow: inset 0px 12px 12px 0px rgba(86, 245, 121, 0.54), inset 14px -12px 12px 0px rgba(86, 245, 131, 0.58), inset -10px 0px 17px 0px rgba(86, 245, 140, 0.67), inset 0px -19px 24px 0px rgba(86, 245, 140, 0.25), inset 0px -4px 0px 0px #1BBF3F !important;
                }

                &.r_box_finish {
                  cursor: default;
                  color: #1CB83D !important;
                  background: none !important;
                  box-shadow: none !important;
                }
              }
            }
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .dailyBettingBonus {

    .t_img {
      margin-bottom: 16px;
    }

    .content_box {
      margin-bottom: 16px;
      padding: 12px 10px;
      border-radius: 8px;

      .list {
        .box {
          ul {
            li {
              gap: 10px;
              margin-bottom: 8px;
              padding: 12px 10px;
              border-radius: 8px;

              &:nth-last-child(1) {
                margin-bottom: 0;
              }

              .c_box {
                margin-right: 0px;
                width: 70%;

                .describe {
                  font-size: 12px;
                }

                :deep(.el-progress_box) {
                  .el-progress__text {
                    font-size: 12px !important;
                  }
                }
              }

              .btn_box {
                display: flex;
                align-items: flex-end;
                flex-direction: column-reverse;
                width: 30%;
                gap: 3px;

                .l_box {
                  img {
                    margin-right: 3px;
                    width: 16px;
                  }

                  div {
                    font-size: 12px;
                  }
                }


                .r_box {
                  min-width: 80px;
                  font-size: 12px;
                }
              }
            }
          }
        }
      }
    }
  }
}
</style>
