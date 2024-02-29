<template>
    <div class="app-container">
        <el-card class="box-card box-card-top">
            <datetime @def="timeChange" />
            <div>
                <el-input v-model="state.pageForm.uid" placeholder="请输入用户名" style="width: 200px;" clearable />
                <el-input v-model="state.pageForm.code_id" placeholder="请输入codeID" style=" width: 200px" clearable />
                <span>渠道：</span>
                <el-select v-model="state.pageForm.cid" placeholder="渠道" clearable>
                    <el-option label="全部" value="" />
                    <el-option v-for="item in agent_list" :key="item.cid" :label="item.username" :value="item.cid" />
                </el-select>
                <el-button type="primary" @click="getData()">搜索</el-button>
            </div>
        </el-card>
        <el-card class="box-card" uno-margin-top>
            <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
                :summary-method="getSummaries">
                <el-table-column prop="id" label="id" header-align="center" :align="'center'" sortable />
                <el-table-column prop="code_id" label="codeID" header-align="center" :align="'center'" sortable />
                <el-table-column prop="code" label="code码" header-align="center" :align="'center'" sortable />
                <el-table-column prop="username" label="渠道" header-align="center" :align="'center'" />
                <el-table-column prop="uid" label="用户" header-align="center" :align="'center'" width="180">
                    <template #default="scope">
                        <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
                            `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="give_money" label="金额" header-align="center" :align="'center'" sortable />
                <el-table-column prop="add_time" label="时间" header-align="center" :align="'center'" sortable />
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
import popconfirm from "@/components/popconfirm/index.vue"
import { give_code_log_list_post } from '@/api/logrecordManagement/index'
import datetime from "@/components/datetime/index.vue"
import { goToUserInfo } from "@/utils/baseFun"
import { storeToRefs } from 'pinia';
import confStore from "@/store/modules/conf";
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
        total_money: 0,
        uid: '',
        start_time: '',
        end_time: '',
        code_id: '',
        cid: '',

    },
    timeArr: '',

})
const ruleFormRef = ref<FormInstance>()

//选择时间
const timeChange = (time) => {
    state.timeArr = time
    getData()
}
// 获取数据
const getData = async () => {
    state.loading = true
    state.pageForm.start_time = state.timeArr ? state.timeArr[0] : ''
    state.pageForm.end_time = state.timeArr ? state.timeArr[1] : ''
    give_code_log_list_post({ ...state.pageForm }).then(res => {
        state.tableData = res['data']
        state.pageForm.total = res['count']
        state.pageForm.total_money = res['total_money']
    })
    state.loading = false
}
getData();// 获取数据

const getSummaries = (param) => {
    const { columns, data } = param;
    const sums = [];


    (sums[0] as any) = '合计';
    (sums[5] as any) = state.pageForm.total_money
    return sums
}
</script>
  
<style lang="scss" scoped></style>
  
  