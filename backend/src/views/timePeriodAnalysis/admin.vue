<template>
    <div class="app-container">
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
        <el-card class="box-card" uno-margin-top>
            <columnar-polyline-chart chartBox="timePeriodAnalysis_1" title="充提数据" :yAxisName="['人数', '金额(R$)']"
                :xAxisLabelList="state.xAxisLabelList" :dataList="state.recharge" :colorList="state.colorList" />
            <line-chart chartBox="timePeriodAnalysis_5" title="日活时段数据" yAxisName="人数" :xAxisLabelList="state.xAxisLabelList"
                :dataList="state.user_report" :colorList="state.colorList" uno-margin-top />
            <line-chart chartBox="timePeriodAnalysis_6" title="app日活" yAxisName="人数" :xAxisLabelList="state.xAxisLabelList"
                :dataList="state.app_hour_report" :colorList="state.colorList" uno-margin-top />
            <line-chart chartBox="timePeriodAnalysis_2" title="打码反水数据" yAxisName="人数" :xAxisLabelList="state.xAxisLabelList"
                :dataList="state.bet_task_report" :colorList="state.colorList" uno-margin-top />
            <line-chart chartBox="timePeriodAnalysis_3" title="补给箱领取数据" yAxisName="人数"
                :xAxisLabelList="state.xAxisLabelList" :dataList="state.loss_bonus_report" :colorList="state.colorList"
                uno-margin-top />
            <line-chart chartBox="timePeriodAnalysis_4" title="签到领取数据" yAxisName="人数" :xAxisLabelList="state.xAxisLabelList"
                :dataList="state.sign_hour_report" :colorList="state.colorList" uno-margin-top />
        </el-card>
    </div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed, onMounted, nextTick, markRaw } from "vue";
import { hour_report } from "@/api/statistics"
import * as echarts from "echarts";
import { storeToRefs } from "pinia";
import confStore from "@/store/modules/conf";
import lineChart from "@/components/echarts/lineChart.vue"
import columnarPolylineChart from '@/components/echarts/columnarPolylineChart.vue';

const state = reactive({
    searchForm: {
        cid: '',
        day: ''
    },
    agent_list: [],
    chartBoxEL: '',
    xAxisLabelList: [],
    colorList: ['#fe9a8b', '#9E87FF', '#EE0909'],
    dataList: [],
    recharge: [],
    bet_task_report: [],
    loss_bonus_report: [],
    sign_hour_report: [],
    user_report: [],
    app_hour_report: [],
})
const store = confStore();
let { agent_list, factory_list, factory_details_list, external_game_list, gameType } = storeToRefs(store);

state.agent_list = store.agent_list

const searchData = () => {
    getData()
}
onMounted(() => {
    // console.log('agent_list', store.agent_list);
});

const getData = () => {
    hour_report({ ...state.searchForm }).then(res => {
        state.recharge = res.recharge
        const setDataType = () => {
            state.recharge[0].type = 'line'
            state.recharge[1].type = 'bar'
            state.recharge[2].type = 'line'
        }
        setDataType()
        state.xAxisLabelList = res.table
        state.bet_task_report = res.bet_task_report
        state.loss_bonus_report = res.loss_bonus_report
        state.sign_hour_report = res.sign_hour_report
        state.user_report = res.user_report
        state.app_hour_report = res.app_hour_report
    })
}
getData()
</script>

<style lang="scss" scoped>
.box-card {
    overflow-x: scroll;

    .el-card__body {
        >div {
            // min-width: 800px
        }
    }
}
</style>
