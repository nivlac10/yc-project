<template>
  <div class="home-container layout-pd">
    <el-collapse v-model="state.activeNames">
      <el-collapse-item name="1" v-show="isAdmin">
        <template #title>
          <div style="font-size: 24px; font-weight: 600; margin-left: 20px;">日数据</div>
        </template>
        <el-card class="box-card-top">
          <div>
            <span>渠道：</span>
            <el-select v-model="state.searchForm.cid" placeholder="渠道">
              <el-option label="全部" value="" />
              <el-option v-for="item in agent_list" :key="item.cid" :label="item.username" :value="item.cid" />
            </el-select>
          </div>
          <el-date-picker v-model="state.searchForm.day" type="date" placeholder="Pick a day" value-format="YYYY-MM-DD" />
          <el-button type="primary" @click="searchData">搜索</el-button>
        </el-card>
        <el-row :gutter="15" class="home-card-one mb5">
          <el-col :xs="24" :sm="12" :md="12" :lg="8" :xl="8" v-for="(v, k) in state.homeOne" :key="k"
            :class="{ 'home-media home-media-lg': k > 1, 'home-media-sm': k === 1 }">
            <div class="home-card-item flex" uno-margin-top>
              <!-- :class="` home-one-animation${k}`" -->
              <div class="flex-margin flex w100">
                <div class="flex-auto">
                  <div class="font26 title">{{ v.title }}</div>
                  <div class="flex card_max_box">
                    <div class="card_box" v-for="(item, index) in v.data">
                      <p>{{ item.title }}</p>
                      <p>{{ item.num }} <span class="font550 unit">{{ item.unit }}</span> </p>
                    </div>
                  </div>
                </div>
                <!-- <div class="home-card-item-icon flex" :style="{ background: `var(${v.color2})` }">
              <i class="flex-margin font32" :class="v.num4" :style="{ color: `var(${v.color3})` }"></i>
            </div> -->
              </div>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="15" class="home-card-two mb5">
          <el-col :xs="24" :sm="14" :md="14" :lg="12" :xl="8">
            <div class="home-card-item" style="height:300px">
              <div class="home-card-item-title mb5">提现数据</div>
              <el-table :data="state.withdraw_Data" style="width: 100%;color: black;">
                <el-table-column prop="row_name" label="名称" header-align="center" :align="'center'" />
                <el-table-column prop="withdraw_money" label="提现总额" header-align="center" :align="'center'" />
                <el-table-column prop="w_r_gap" label="充提差" header-align="center" :align="'center'" />
                <el-table-column prop="withdraw_lv" label="提现率" header-align="center" :align="'center'">
                  <template #default="scope">
                    {{ scope.row.withdraw_lv }}%
                  </template>
                </el-table-column>
                <el-table-column prop="withdraw_user_sum" label="提现人数" header-align="center" :align="'center'" />
              </el-table>
            </div>
          </el-col>
          <el-col :xs="24" :sm="10" :md="10" :lg="12" :xl="16">
            <div class="home-card-item" style="height:300px">
              <div class="home-card-item-title mb">充值数据</div>

              <el-table :data="state.recharge_Data" style="width: 100%;color: black;">
                <el-table-column prop="row_name" label="名称" header-align="center" :align="'center'" />
                <el-table-column prop="pay_money" label="付费金额" header-align="center" :align="'center'" />
                <el-table-column prop="pay_user_sum" label="付费人数" header-align="center" :align="'center'" />
                <el-table-column prop="pay_lv" label="付费率" header-align="center" :align="'center'">
                  <template #default="scope">
                    {{ scope.row.pay_lv }}%
                  </template>
                </el-table-column>
                <el-table-column prop="pay_arppu" label="付费ARPPU" header-align="center" :align="'center'" />
                <el-table-column prop="pay_arpu" label="活跃ARPU" header-align="center" :align="'center'" />
              </el-table>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="15" class="home-card-two mb5">
          <el-col :xs="24" :sm="10" :md="10" :lg="8" :xl="8" class="home-media">
            <div class="home-card-item">
              <water-drop-chart chartBox="admin_019"
                :title="`打码数据 \n 总压分:${state.bet_data_obj['total_bet']} 输赢:${state.bet_data_obj['total_real_shu_yin']} 总赢分:${state.bet_data_obj['total_shu_ying']}`"
                :rate="state.bet_data_obj['bet_data_total']" />
            </div>
          </el-col>
          <el-col :xs="24" :sm="14" :md="14" :lg="16" :xl="16">
            <div class="home-card-item">
              <columnar-polyline-chart chartBox="admin_12321321" title="充提数据" :yAxisName="['金额(R$)', '']"
                :xAxisLabelList="state.r_w_money_list_xAxisLabelList" :dataList="state.r_w_money_list"
                :colorList="['#fe9a8b', '#9E87FF', '#EE0909']" lineSymbolSize="0" />
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="15" class="home-card-three">
          <el-col :xs="24" :sm="10" :md="10" :lg="8" :xl="8">
            <div class="home-card-item" style="overflow-y: scroll;">
              <div class="home-card-item-title">赠送数据</div>
              <div class="give_data_box">
                <ul>
                  <li v-for="(v, k) in state.give_data" :key="k">
                    <div>{{ v['title'] }}</div>
                    <div>{{ v['num'] }}<span>{{ v['unit'] }}</span></div>
                  </li>
                </ul>
              </div>
            </div>
          </el-col>
          <el-col :xs="24" :sm="14" :md="14" :lg="16" :xl="16" class="home-media">
            <div class="home-card-item">
              <line-chart chartBox="admin_123245" title="毛利走向" yAxisName="金额(R$)"
                :xAxisLabelList="state.profit_obj.profit_list_xAxisLabelList" :dataList="state.profit_obj.profit_list"
                :colorList="['#EE0909', '#9E87FF', '#09EE0D']" lineSymbolSize="0" uno-margin-top />
            </div>
          </el-col>
        </el-row>

      </el-collapse-item>
      <el-collapse-item name="2" v-permission="['1', '3']">
        <template #title>
          <div style="font-size: 24px; font-weight: 600; margin-left: 20px;">数据总览</div>
        </template>
        <data-screening />
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup lang="ts" name="home">
import { reactive, onMounted, ref, watch, nextTick, onActivated, markRaw } from 'vue';
import * as echarts from 'echarts';
import { storeToRefs } from 'pinia';
import confStore from "@/store/modules/conf";
import { admin_home } from "@/api/adminHome";
import { it } from 'node:test';
import lineChart from "@/components/echarts/lineChart.vue"
import columnarPolylineChart from '@/components/echarts/columnarPolylineChart.vue';
import waterDropChart from '@/components/echarts/waterDropChart.vue';
import dataScreening from "./dataScreening.vue"
import { useUserStore } from "@/store/modules/user"
// import { useThemeConfig } from '/@/stores/themeConfig';
// import { useTagsViewRoutes } from '/@/stores/tagsViewRoutes';
// 定义变量内容
const userStore = useUserStore()
const isAdmin = userStore.roles.includes("1")
const homeBarRef = ref();
// const storesTagsViewRoutes = useTagsViewRoutes();
// const storesThemeConfig = useThemeConfig();
// const { themeConfig } = storeToRefs(storesThemeConfig);
// const { isTagsViewCurrenFull } = storeToRefs(storesTagsViewRoutes);

const store = confStore();
let { agent_list, factory_list, factory_details_list, external_game_list, gameType } = storeToRefs(store);
const state = reactive({
  agent_list: [],
  searchForm: {
    cid: null,
    day: null
  },
  global: {
    homeChartOne: null,
    homeChartTwo: null,
    homeCharThree: null,
    dispose: [null, '', undefined],
  } as any,
  homeOne: [],
  give_data: [],
  r_w_money_list: [],
  r_w_money_list_xAxisLabelList: [],
  recharge_Data: [],
  withdraw_Data: [],
  profit_obj: {
    profit_list: [],
    profit_list_xAxisLabelList: []
  },
  bet_data_obj: {},
  myCharts: [],
  charts: {
    theme: '',
    bgColor: '',
    color: '#303133',
  },
  activeNames: ['1', '2']
});
state.agent_list = store.agent_list


function getHomeData() {
  admin_home({ ...state.searchForm }).then((res) => {
    state.homeOne = res.card
    state.give_data = res.give_data.data
    // 充提数据
    state.r_w_money_list = res.r_w_money_list.rw_data
    state.r_w_money_list_xAxisLabelList = res.r_w_money_list.table
    const setDataType = () => {
      state.r_w_money_list[0].type = 'line'
      state.r_w_money_list[1].type = 'line'
      state.r_w_money_list[2].type = 'line'
    }
    setDataType()
    // 毛利走向
    state.profit_obj.profit_list = res.profit_list.rw_data
    state.profit_obj.profit_list_xAxisLabelList = res.profit_list.table
    // 水滴图
    state.bet_data_obj = res.bet_data
    state.bet_data_obj['bet_data_total'] = parseFloat((res.bet_data.total_shu_ying / (res.bet_data.total_bet / 100) / 100).toFixed(2))
    state.recharge_Data = res.recharge_Data
    state.withdraw_Data = res.withdraw_Data
    console.log(state.recharge_Data)
    console.log(state.withdraw_Data)
  })
}
getHomeData()

const searchData = () => {
  getHomeData()
}



// 批量设置 echarts resize
const initEchartsResizeFun = () => {
  nextTick(() => {
    for (let i = 0; i < state.myCharts.length; i++) {
      setTimeout(() => {
        state.myCharts[i].resize();
      }, i * 1000);
    }
  });
};
// 批量设置 echarts resize
const initEchartsResize = () => {
  window.addEventListener('resize', initEchartsResizeFun);
};


// 页面加载时
onMounted(() => {
  initEchartsResize();
});
// 由于页面缓存原因，keep-alive
onActivated(() => {
  initEchartsResizeFun();
});

</script>

<style scoped lang="scss">
$homeNavLengh: 8;

.card_max_box {
  display: flex;
  // gap: 20px;
  justify-content: space-between;
  width: 100%;

  .card_box {
    padding-right: 10px;
    text-align: center;

    .unit {
      color: #51A3FC;
      font-size: 12px;
    }
  }
}

.title {
  font-weight: 550;
}

.flex-auto {
  .font30 {
    font-size: 30px;
    font-weight: 550;
  }

  .font16 {
    font-size: 18px;
    font-weight: 550;
  }

  .mt10 {
    font-size: 18px;
    font-weight: 600;
  }
}



.home-container {
  overflow: hidden;
  margin: 10px;
  display: flex;
  flex-direction: column;
  gap: 20px;

  .home-card-one,
  .home-card-two,
  .home-card-three {
    .home-card-item {
      width: 100%;
      height: 130px;
      border-radius: 4px;
      transition: all ease 0.3s;
      padding: 20px;
      overflow: hidden;
      background: var(--el-color-white);
      color: var(--el-text-color-primary);
      border: 1px solid var(--next-border-color-light);

      &:hover {
        box-shadow: 0 2px 12px var(--next-color-dark-hover);
        transition: all ease 0.3s;
      }

      &-icon {
        width: 70px;
        height: 70px;
        border-radius: 100%;
        flex-shrink: 1;

        i {
          color: var(--el-text-color-placeholder);
        }
      }

      &-title {
        font-size: 15px;
        font-weight: bold;
        height: 30px;
      }
    }
  }

  .home-card-one {
    @for $i from 0 through 3 {
      .home-one-animation#{$i} {
        opacity: 0;
        animation-name: error-num;
        animation-duration: 0.5s;
        animation-fill-mode: forwards;
        animation-delay: calc($i/4) + s;
      }
    }
  }

  .home-card-two,
  .home-card-three {
    .home-card-item {
      height: 400px;
      width: 100%;
      overflow: hidden;

      .home-monitor {
        height: 100%;

        .flex-warp-item {
          width: 25%;
          height: 111px;
          display: flex;

          .flex-warp-item-box {
            margin: auto;
            text-align: center;
            color: var(--el-text-color-primary);
            display: flex;
            border-radius: 5px;
            background: var(--next-bg-color);
            cursor: pointer;
            transition: all 0.3s ease;

            &:hover {
              background: var(--el-color-primary-light-9);
              transition: all 0.3s ease;
            }
          }

          @for $i from 0 through $homeNavLengh {
            .home-animation#{$i} {
              opacity: 0;
              animation-name: error-num;
              animation-duration: 0.5s;
              animation-fill-mode: forwards;
              animation-delay: calc($i/10) + s;
            }
          }
        }
      }
    }
  }
}

.give_data_box {
  // height: 400px;

  ul {
    display: flex;
    flex-wrap: wrap;
    padding: 0;
    // overflow-y: scroll;

    li {
      cursor: pointer;
      width: calc(25% - 10px);
      height: auto;
      list-style: none;
      padding: 20px 10px;
      box-sizing: border-box;
      background: #f5f5ff;
      margin: 5px;
      text-align: center;

      &:hover {
        background: #ebf5ff;
      }

      div:nth-child(1) {
        margin-bottom: 20px;
        font-size: 14px;
      }

      div:nth-child(2) {
        span {
          font-size: 12px;
        }
      }
    }
  }
}

:deep(.el-collapse-item__wrap) {
  background: transparent;
}
</style>
