<template>
    <div class="app-container">
        <el-card class="box-card box-card-top">
            <datetime @def="timeChange" />
            <div>
                <span>渠道：</span>
                <el-select v-model="state.pageForm.cid" placeholder="渠道">
                    <el-option label="全部" value="" />
                    <el-option v-for="item in agent_list" :key="item.cid" :label="item.username" :value="item.cid" />
                </el-select>
            </div>
            <el-button type="primary" @click="getData()">搜索</el-button>
        </el-card>
        <el-card class="box-card" uno-margin-top>
            <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
                :summary-method="getSummaries">
                <el-table-column prop="cid" label="ID" header-align="center" :align="'center'" sortable />
                <el-table-column prop="username" label="渠道" header-align="center" :align="'center'" />
                <el-table-column prop="week_number" label="周活" header-align="center" :align="'center'" sortable />
                <el-table-column prop="month_number" label="月活" header-align="center" :align="'center'" sortable />
            </el-table>
        </el-card>
        <el-card uno-margin-top>
            <div class="pager-wrapper">
                <pagination :pageForm="state.pageForm" @def="getData" />
            </div>
        </el-card>
    </div>
</template>
  
<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import pagination from "@/components/pagination/index.vue"
import datetime from "@/components/datetime/index.vue"
import { user_keep_log_post } from "@/api/logrecordManagement"
import confStore from "@/store/modules/conf";
import { storeToRefs } from 'pinia';
const store = confStore();
let { agent_list, factory_list, factory_details_list, external_game_list, gameType } = storeToRefs(store);

const router = useRouter();
const state = reactive({
    loading: false, // table loading
    operationType: 'add', // add || edit
    dialogFormVisible: false,
    tableData: [],
    pageForm: {
        page: 1,
        limit: 20,
        total: 0,
        stime: '',
        etime: '',
        cid: ''
    },
    total: [],
    timeArr: '',
})
//选择时间
const timeChange = (time) => {
    state.timeArr = time
    getData()
}
// 获取数据
const getData = async () => {
    state.loading = true
    user_keep_log_post({ ...state.pageForm }).then(res => {
        state.tableData = res.data
        state.pageForm.total = res.count
        state.total = res['total']
    })
    state.loading = false
}
getData();// 获取数据

const getSummaries = (param) => {
    const { columns, data } = param;
    const sums = [];


    (sums[0] as any) = '合计';
    (sums[2] as any) = state.total['week_number'];
    (sums[3] as any) = state.total['month_number'];
    return sums
}
</script>
  
<style lang="scss" scoped></style>
  
  