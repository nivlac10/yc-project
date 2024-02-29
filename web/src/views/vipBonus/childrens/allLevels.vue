<template>
  <div class="allLevels">
    <back :backNameShow="false" :img="getImageUrl('vipBonus/vip_head_img.png')" :title="t('vipBonus.TODOSNÍVEISVIP')" />
    <div class="list">
      <ul class="list_ul">
        <li class="list_ul_li" v-for="(v, i) in vipList" :key="i" v-show="i < 6">
          <div class="list_ul_li_container">
            <div class="t_container hidden-xs-only">
              <div class="t_container_l_box">
                <div class="t_container_l_box_level">
                  <img :src="getImageUrl(`vipBonus/level_${i}.png`)" alt="">
                  <span :style="`color: ${fontColorList[i]}`">{{ levelName(i) }}</span>
                </div>
                <p class="t_container_l_box_level_p">{{ t('vipBonus.BônusdeNívelApostadeUpgrade') }} 0,2%</p>
              </div>
              <div class="t_container_r_box">
                <div>
                  <p>{{ v.pay_fee }}%</p>
                  <p>{{ t('vipBonus.Taxaderetirada') }}</p>
                </div>
                <div>
                  <p>{{ v.day_max_withdraw }}</p>
                  <p>{{ t('vipBonus.Limitederetiradadiária') }}</p>
                </div>
                <div>
                  <p>{{ v.withdraw_num }}</p>
                  <p>{{ t('vipBonus.Vezesderetiradadiária') }}</p>
                </div>
              </div>
            </div>
            <div class="b_container">
              <ul>
                <li v-for="(v2, i2) in store.state.status.isPc ? 5 : v.vip_low_lv.length" :key="i2">
                  <div class="t_data" v-if="v.vip_low_lv[i2]">
                    <img class="level_img" :src="getImageUrl(`vipBonus/level_${i}.png`)" alt="">
                    <div class="level_box_info">
                      <div class="level_name" :style="`color: ${fontColorList[i]}`">{{ levelName(i) }}
                        {{ i2 + 1 }}</div>
                      <div class="level_amount">{{ t('account.Aposta') }} {{ moneyFormat(v.vip_low_lv[i2].need_code_amount, true) }}
                      </div>
                      <el-progress class="el-progress_box" :color="fontColorList[i]"
                        :stroke-width="store.state.status.isPc ? 10 : 8"
                        :percentage="progressToPercent(v.vip_low_lv[i2].need_code_amount)" status="exception">
                        <span>
                          <!-- 0/0 -->
                        </span>
                      </el-progress>
                    </div>
                    <div :class="{ level_btn: true, level_btn_f: v.vip_low_lv[i2].state == 2 }">
                      <div class="sl_box_shadow" @click="receiveBtn(v.vip_low_lv[i2].state, v.vip_low_lv[i2].id)">
                        <div>
                          <img src="@assets/images/refer/RETIRADA.png" alt="">
                          <span>{{ v.vip_low_lv[i2].state == 2 ? t('btnName.Concluir') : t('btnName.Receber') }}</span>
                        </div>
                        <div>{{ moneyFormat(v.vip_low_lv[i2].bonus) }}</div>
                      </div>
                      <div class="mask" v-show="v.vip_low_lv[i2].state == 0"></div>
                    </div>
                  </div>
                  <div class="n_data" v-else>
                    <img src="@assets/images/vipBonus/default.png" alt="">
                  </div>
                </li>
              </ul>
              <p class="p_txt">{{ t('vipBonus.BônusdeNívelApostadeUpgrade') }} 0,2%</p>
              <div class="level_rule_box">
                <div class="level_rule_box_title">{{ t('vipBonus.Limitederetirada') }}</div>
                <div class="level_rule_box_info">
                  <div class="txt">
                    <div>{{ t('vipBonus.Taxaderetirada') }}</div>
                    <div>{{ v.pay_fee }}%</div>
                  </div>
                  <div class="txt">
                    <div>{{ t('vipBonus.Limitederetiradadiária') }}</div>
                    <div>{{ v.day_max_withdraw }}</div>
                  </div>
                  <div class="txt">
                    <div>{{ t('vipBonus.Vezesderetiradadiária') }}</div>
                    <div>{{ v.withdraw_num }}</div>
                  </div>{{ t('vipBonus.porcentagemdeBônusCashback') }}
                </div>
                <div class="rate_list">
                  <div class="rate_list_box">
                    <div :style="`color: ${v.bet_bonus_rate > 0 ? '#75ED3D' : ''};`">{{ v.bet_bonus_rate }}%</div>
                    <div>{{ t('vipBonus.porcentagemdeBônusCashback') }}</div>
                  </div>
                  <div class="rate_list_box">
                    <div :style="`color: ${v.day_bet_bonus_rate > 0 ? '#75ED3D' : ''};`">{{ v.day_bet_bonus_rate }}%</div>
                    <div>{{ t('vipBonus.porcentagemdeBônusDiário') }}</div>
                  </div>
                  <div class="rate_list_box">
                    <div :style="`color: ${v.week_bet_bonus_rate > 0 ? '#75ED3D' : ''};`">{{ v.week_bet_bonus_rate }}%</div>
                    <div>{{ t('vipBonus.porcentagemdeBônusSemanal') }}</div>
                  </div>
                  <div class="rate_list_box">
                    <div :style="`color: ${v.month_bet_bonus_rate > 0 ? '#75ED3D' : ''};`">{{ v.month_bet_bonus_rate }}%</div>
                    <div>{{ t('vipBonus.porcentagemeBônusMensal') }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <div class="last_level">
      <div class="last_level_container" v-for="(v, i) in vipList" :key="i" v-show="i >= 6">
        <div class="last_level_box">
          <div class="last_level_box_t hidden-xs-only">
            <div>
              <img :src="getImageUrl(`vipBonus/level_${i}.png`)" alt="">
              <span :style="`color: ${fontColorList[i]}`">{{ levelName(i) }}</span>
            </div>
            <p>{{ t('vipBonus.BônusdeNívelApostadeUpgrade') }} 0,2%</p>
          </div>
          <div class="last_level_box_b">
            <div class="last_level_box_b_l">
              <div class="t_data">
                <img class="level_img" :src="getImageUrl(`vipBonus/level_${i}.png`)" alt="">
                <div class="level_box_info">
                  <div class="level_name" :style="`color: ${fontColorList[i]}`">{{ levelName(i) }}</div>
                  <div class="level_amount">Aposta {{ moneyFormat(v.vip_low_lv[0]['need_code_amount']) }}</div>
                  <el-progress class="el-progress_box" :stroke-width="store.state.status.isPc ? 10 : 8"
                    :color="fontColorList[i]" :percentage="progressToPercent(v.vip_low_lv[0]['need_code_amount'])"
                    status="exception">
                    <span>
                      <!-- 0/0 -->
                    </span>
                  </el-progress>
                </div>
                <div :class="{ level_btn: true, level_btn_f: v.vip_low_lv[0].state == 2 }">
                  <div class="sl_box_shadow" @click="receiveBtn(v.vip_low_lv[0].state, v.vip_low_lv[0].id)">
                    <div>
                      <img src="@assets/images/refer/RETIRADA.png" alt="">
                      <span>{{ v.vip_low_lv[0].state == 2 ? 'ADICIONADA' : 'ADICIONAR' }}</span>
                    </div>
                    <div>{{ moneyFormat(v.vip_low_lv[0].bonus) }}</div>
                  </div>
                  <div class="mask" v-show="v.vip_low_lv[0].state == 0"></div>
                </div>
              </div>
            </div>
            <div class="last_level_box_b_r hidden-xs-only">
              <div class="txt">
                <p>{{ v.pay_fee }}%</p>
                <p>{{ t('vipBonus.Taxaderetirada') }}</p>
              </div>
              <div class="txt">
                <p>{{ v.day_max_withdraw }}</p>
                <p>{{ t('vipBonus.Limitederetiradadiária') }}</p>
              </div>
              <div class="txt">
                <p>{{ v.withdraw_num }}</p>
                <p>{{ t('vipBonus.Vezesderetiradadiária') }}</p>
              </div>
            </div>
          </div>
          <p class="p_txt">{{ t('vipBonus.BônusdeNívelApostadeUpgrade') }} 0,2%</p>
          <div class="level_rule_box">
            <div class="level_rule_box_title">{{ t('vipBonus.Limitederetirada') }}</div>
            <div class="level_rule_box_info">
              <div class="txt">
                <div>{{ t('vipBonus.Taxaderetirada') }}</div>
                <div>{{ v.pay_fee }}%</div>
              </div>
              <div class="txt">
                <div>{{ t('vipBonus.Limitederetiradadiária') }}</div>
                <div>{{ v.day_max_withdraw }}</div>
              </div>
              <div class="txt">
                <div>{{ t('vipBonus.Vezesderetiradadiária') }}</div>
                <div>{{ v.withdraw_num }}</div>
              </div>
            </div>
            <div class="rate_list">
              <div class="rate_list_box">
                <div :style="`color: ${v.bet_bonus_rate > 0 ? '#75ED3D' : ''};`">{{ v.bet_bonus_rate }}%</div>
                <div>{{ t('vipBonus.porcentagemdeBônusCashback') }}</div>
              </div>
              <div class="rate_list_box">
                <div :style="`color: ${v.day_bet_bonus_rate > 0 ? '#75ED3D' : ''};`">{{ v.day_bet_bonus_rate }}%</div>
                <div>{{ t('vipBonus.porcentagemdeBônusDiário') }}</div>
              </div>
              <div class="rate_list_box">
                <div :style="`color: ${v.week_bet_bonus_rate > 0 ? '#75ED3D' : ''};`">{{ v.week_bet_bonus_rate }}%</div>
                <div>{{ t('vipBonus.porcentagemdeBônusSemanal') }}</div>
              </div>
              <div class="rate_list_box">
                <div :style="`color: ${v.month_bet_bonus_rate > 0 ? '#75ED3D' : ''};`">{{ v.month_bet_bonus_rate }}%</div>
                <div>{{ t('vipBonus.porcentagemeBônusMensal') }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-dialog v-model="isBonusPop" :append-to-body="true">
      <div class="bounsPop_box" @click="isBonusPop = false">
        <div class="pop_box" @click.stop>
          <bounsPop :comIdx="5" :now_bonus="now_bonus_pop" :split_bonus="split_bonus_pop"
            @close-pop="isBonusPop = false" />
        </div>
      </div>
    </el-dialog>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import back from "@com/back/index.vue"
import { getImageUrl, toPercent, levelName, getUserInfo, debounce, moneyFormat } from "@/utils/baseFun";
import { VipService } from "@/api/vip";
import bounsPop from '@/views/vipBonus/components/bounsPop.vue';

export default defineComponent({
  name: "allLevels",
  components: { back, bounsPop },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore(); 
    const state = reactive({
      vipList: store.state.conf.all_conf.vip_conf,
      fontColorList: ['#DBA786', '#DBA786', '#C3D3FF', '#E4C274', '#8BD5F1', '#E284D0', '#EC5B60', '#9EF6EE'],
      now_bonus_pop: 0,
      split_bonus_pop: 0,
      isBonusPop: false
    });

    const getList = () => {
      VipService.get_user_vip_up_bonus_state().then(res => {
        for (let i = 0; i < res.data.data.length; i++) {
          let element1 = res.data.data[i];
          for (let j = 0; j < store.state.conf.all_conf.vip_conf.length; j++) {
            let element2 = store.state.conf.all_conf.vip_conf[j];
            for (let k = 0; k < element2.vip_low_lv.length; k++) {
              let element3 = element2.vip_low_lv[k];
              if (element1.id == element3.id) {
                element3.state = element1.state
              }
            }
          }
        }
      })
    }
    getList()

    const progressToPercent = (val: number) => {
      return toPercent(store.state.user.total_bet, val)
    }

    const receiveBtn = (status: number, id: number) => {
      if (status != 1) return
      const fun = () => {
        VipService.user_get_vip_up_bonus({ id: id }).then(res => {
          if (res.data.code == 1) {
            getList()
            getUserInfo()
            state.isBonusPop = true
            state.now_bonus_pop = res.data.bonus
            state.split_bonus_pop = res.data.split_bonus
          }
        })
      }
      debounce(fun)
    }

    return { ...toRefs(state), store, t, getImageUrl, progressToPercent, levelName, receiveBtn, moneyFormat };
  },
});
</script>
<style  lang="scss" scoped>
.bounsPop_box {
  display: flex !important;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  height: 100%;

  .pop_box {
    position: relative;
  }
}

.allLevels {
  .list {
    .list_ul {
      .list_ul_li {
        margin-bottom: 16px;
        padding: 16px 24px;
        box-sizing: border-box;
        background: #202431;
        border-radius: 12px;

        .list_ul_li_container {
          .t_container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;

            .t_container_l_box {
              padding-left: 80px;

              .t_container_l_box_level {
                display: flex;
                align-items: center;

                img {
                  margin-right: 5px;
                  width: 60px;
                }

                span {
                  font-size: 24px;
                  font-weight: bold;
                  color: #DBA786;
                }
              }

              .t_container_l_box_level_p {
                font-size: 14px;
                font-weight: 500;
                color: #B2B6C5;
              }
            }

            .t_container_r_box {
              display: flex;
              justify-content: space-around;
              width: 681px;
              padding: 12px 0;
              background: #2F3445;
              border-radius: 12px;

              div {
                text-align: center;

                p:nth-child(1) {
                  margin-bottom: 13px;
                  font-size: 16px;
                  font-weight: bold;
                  color: #B2B6C5;
                }

                p:nth-child(2) {
                  font-size: 14px;
                  font-weight: 500;
                  color: #B2B6C5;
                }
              }
            }
          }

          .b_container {
            ul {
              display: grid;
              grid-template-columns: repeat(5, 1fr);
              column-gap: 16px;
              // row-gap: 16px;

              li {
                padding: 18px 0;
                box-sizing: border-box;
                background: #2F3445;
                border-radius: 12px;

                .n_data {
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  height: 100%;

                  img {
                    opacity: 0.3;
                    width: 115px;
                  }
                }
              }
            }

            .rate_list {
              display: flex;
              justify-content: space-between;
              padding: 24px 36px;
              margin-top: 17px;
              background: #2F3445;
              border-radius: 12px;

              .rate_list_box {
                text-align: center;
                color: #B2B6C5;

                div:nth-child(1) {
                  margin-bottom: 20px;
                  font-size: 20px;
                  font-weight: 600;
                }

                div:nth-child(2) {
                  font-size: 14px;
                }
              }
            }
          }
        }
      }
    }
  }

  .p_txt {
    display: none;
    padding: 16px 0 4px 0;
    font-size: 12px;
    text-align: center;
    color: #B2B6C5;
  }

  .level_rule_box {

    .level_rule_box_title,
    .level_rule_box_info {
      display: none;
    }
  }

  .t_data {
    text-align: center;

    .level_img {
      display: block;
      margin: 0 auto;
      width: 60px;
    }

    .level_name {
      font-size: 16px;
      font-weight: 600;
      color: #DBA786;
    }

    .level_amount {
      padding: 15px 0 11px 0;
      font-size: 13px;
      font-weight: bold;
      color: #B2B6C5;
    }

    :deep(.el-progress_box) {
      margin: 0 40px 24px 40px;

      .el-progress-bar__outer {
        background: #202431;

        .el-progress-bar__inner {
          background: none;
        }
      }
    }

    .level_btn {
      position: relative;
      display: inline-block;
      font-size: 16px;
      font-weight: bold;
      color: #252633;

      &.level_btn_f {
        .sl_box_shadow {
          background: transparent !important;
          box-shadow: none;
          color: #B2B6C5;

          div {
            img {
              display: none;
            }
          }
        }
      }

      .sl_box_shadow {
        // display: inline-block;
        padding: 7px 18px;
        height: 52px;
        box-sizing: border-box;
        border-radius: 12px;

        div:nth-child(1) {
          display: flex;
          justify-content: center;
          align-items: center;
          margin: 3px 0;

          img {
            margin-right: 5px;
            width: 16px;
          }

          span {
            font-weight: bold;
          }
        }

        div:nth-child(2) {
          font-weight: bold;
        }
      }

      .mask {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: 1;
        background: rgba($color: #000000, $alpha: 0.5);
        border-radius: 12px;
      }
    }
  }

  .last_level {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    column-gap: 32px;

    .last_level_container {
      padding: 15px 24px;
      border-radius: 12px;
      background: #202431;

      .last_level_box {
        .last_level_box_t {
          margin-bottom: 29px;

          div {
            display: flex;
            justify-content: center;
            align-items: center;

            img {
              margin-right: 5px;
              width: 60px;
            }

            span {
              font-size: 22px;
              font-weight: bold;
              color: #EC5B60;
            }
          }

          p {
            text-align: center;
            font-size: 16px;
            color: #B2B6C5;
          }
        }

        .last_level_box_b {
          display: flex;
          gap: 16px;

          .last_level_box_b_l {
            width: 218px;
            flex-shrink: 0;
          }

          .last_level_box_b_r {
            padding: 27px 0;
            width: 100%;
          }

          .last_level_box_b_l,
          .last_level_box_b_r {
            background: #2F3445;
            border-radius: 12px;

            .txt {
              text-align: center;

              &:nth-child(1),
              &:nth-child(2) {
                margin-bottom: 22px;
              }

              p:nth-child(1) {
                margin-bottom: 17px;
                font-size: 16px;
                font-weight: 600;
                color: #B2B6C5;
              }

              p:nth-child(2) {
                font-size: 14px;
                color: #B2B6C5;
              }
            }
          }
        }

        .rate_list {
          display: flex;
          justify-content: space-between;
          flex-wrap: wrap;
          padding: 28px 0;

          .rate_list_box {
            width: 50%;
            text-align: center;
            color: #B2B6C5;

            &:nth-child(1),
            &:nth-child(2) {
              margin-bottom: 31px;
            }

            div:nth-child(1) {
              margin-bottom: 20px;
              font-size: 20px;
              font-weight: 600;
            }

            div:nth-child(2) {
              font-size: 14px;
            }
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .allLevels {
    padding: 0 12px;

    .list {
      .list_ul {
        .list_ul_li {
          margin-bottom: 12px;
          padding: 6px;
          border-radius: 12px;

          .list_ul_li_container {
            padding: 16px 6px;
            border-radius: 12px;

            .b_container {
              ul {
                grid-template-columns: repeat(1, 1fr);
                row-gap: 16px;

                li {
                  padding: 0;
                  box-sizing: border-box;
                  background: transparent;
                }
              }

              .rate_list {
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                margin-top: 0;
                padding: 12px 0 0 0;

                .rate_list_box {
                  display: flex;
                  width: 100%;
                  justify-content: space-between;
                  flex-direction: row-reverse;
                  margin-bottom: 12px;

                  &:nth-child(1),
                  &:nth-child(2) {
                    margin-bottom: 12px;
                  }

                  &:nth-last-child(1) {
                    margin-bottom: 0;
                  }

                  div:nth-child(1) {
                    margin-bottom: 0px;
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
      }
    }

    .p_txt {
      display: block;
    }

    .level_rule_box {
      margin-top: 16px;
      padding: 13px 12px;
      background: #2F3445;
      border-radius: 8px;

      .level_rule_box_title {
        display: block;
        margin-bottom: 13px;
        font-size: 12px;
        color: #F3B343;
      }

      .level_rule_box_info {
        display: block;
        border-bottom: 1px dashed rgba(183, 187, 192, 0.32);

        .txt {
          margin-bottom: 12px;
          display: flex;
          justify-content: space-between;

          div:nth-child(1) {
            font-size: 12px;
            color: #B2B6C5;
          }

          div:nth-child(2) {
            font-size: 12px;
            font-weight: 600;
            color: #B2B6C5;
          }
        }
      }
    }

    .t_data {
      display: flex;
      align-items: center;
      justify-content: space-between;

      .level_img {
        display: block;
        margin: 0 3px 0 0;
        width: 42px;
        height: 42px;
        transform: translateY(-8px);
      }

      .level_box_info {
        width: 100%;
        margin-right: 18px;
        text-align: left;

        .level_name {
          font-size: 12px;
        }

        .level_amount {
          padding: 8px 0;
          font-size: 12px;
        }

        :deep(.el-progress_box) {
          margin: 0;

          .el-progress-bar__outer {
            background: #3A3E4B;
          }
        }
      }

      .level_btn {
        font-size: 12px;

        .sl_box_shadow {
          height: 42px;
          padding: 7px 10px;
          border-radius: 8px;

          div:nth-child(1) {
            margin: 2px 0;

            img {
              margin-right: 3px;
              width: 12px;
            }

            span {
              font-weight: bold;
            }
          }

          div:nth-child(2) {
            font-weight: bold;
          }
        }

        .mask {
          border-radius: 8px;
        }
      }
    }

    .last_level {
      display: grid;
      grid-template-columns: repeat(1, 1fr);
      row-gap: 12px;

      .last_level_container {
        padding: 6px;
        border-radius: 12px;

        .last_level_box {
          padding: 16px 6px;
          border-radius: 12px;

          .last_level_box_b {
            display: flex;
            gap: 0px;

            .last_level_box_b_l,
            .last_level_box_b_r {
              width: 100%;
              background: transparent;
            }
          }

          .rate_list {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            padding: 12px 0 0 0;

            .rate_list_box {
              display: flex;
              width: 100%;
              justify-content: space-between;
              flex-direction: row-reverse;
              margin-bottom: 12px;

              &:nth-child(1),
              &:nth-child(2) {
                margin-bottom: 12px;
              }

              &:nth-last-child(1) {
                margin-bottom: 0;
              }

              div:nth-child(1) {
                margin-bottom: 0px;
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
  }
}
</style>
  