<template>
    <div class="app-container">
        <el-card class="box-card box-card-top">
            <datetime @def="timeChange" />
            <el-input v-model="state.pageForm.uid" placeholder="请输入uid或者用户名" style="width: 200px;" clearable />


            <el-button type="primary" @click="getData()">搜索</el-button>
        </el-card>
        <el-card class="box-card" uno-margin-top>
            <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
                :summary-method="getSummaries">
                <el-table-column prop="id" label="id" header-align="center" :align="'center'" sortable />
                <el-table-column prop="nickname" label="用户名" header-align="center" :align="'center'" width="220">
                    <template #default="scope">
                        <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
                            `${scope.row.nickname}(${scope.row.uid})` }}</el-button>
                    </template>

                </el-table-column>
                <el-table-column prop="money" label="金额" header-align="center" :align="'center'" sortable />
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
import { goToUserInfo } from "@/utils/baseFun"
import datetime from "@/components/datetime/index.vue"
import { invite_task_log_post } from "@/api/logrecordManagement"

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
        uid: null
    },
    total_money: 0,
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
    state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
    state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
    invite_task_log_post({ ...state.pageForm }).then(res => {
        state.tableData = res.data
        state.pageForm.total = res.count
        state.total_money = res.count_money
    })
    state.loading = false
}
getData();// 获取数据

const getSummaries = (param) => {
    const { columns, data } = param;
    const sums = [];


    (sums[0] as any) = '合计';


    (sums[2] as any) = state.total_money;
    return sums
}
</script>
  
<style lang="scss" scoped></style>
  
  