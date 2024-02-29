<template>
    <div class="app-container">
        <el-card class="box-card box-card-top">
            <datetime @def="timeChange" />
            <div style="width: 100%;">
                <el-input v-model="state.pageForm.uid" placeholder="请输入uid或者用户名" style="width: 200px;" clearable />
                <el-select v-model="state.pageForm.cid" class="m-2" placeholder="所有渠道" clearable>
                    <el-option v-for="item in state.agent_list" :label="item['username']" :value="item['cid']"
                        :key="item" />
                </el-select>
                <el-button type="primary" @click="getData()">搜索</el-button>
            </div>
        </el-card>
        <el-card class="box-card" uno-margin-top>
            <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
                :summary-method="getSummaries">
                <el-table-column prop="id" label="ID" header-align="center" :align="'center'" sortable />
                <el-table-column prop="uid" label="用户" header-align="center" :align="'center'" sortable>
                    <template #default="scope">
                        <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
                            `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="username" label="渠道" header-align="center" :align="'center'" />
                <el-table-column prop="money" label="奖金" header-align="center" :align="'center'" />
                <el-table-column prop="recharge_money" label="充值金额" header-align="center" :align="'center'" />
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
import confStore from "@/store/modules/conf";
import { goToUserInfo } from "@/utils/baseFun"
import datetime from "@/components/datetime/index.vue"
import { recharge_bonus_log_post } from "@/api/logrecordManagement"

const router = useRouter();
const store = confStore();
const state = reactive({
    loading: false, // table loading
    operationType: 'add', // add || edit
    dialogFormVisible: false,
    tableData: [],
    agent_list: computed(() => store.agent_list),
    pageForm: {
        page: 1,
        limit: 20,
        total: 0,
        uid: null,
        cid: '',
        stime: null,
        etime: null,
    },
    ruleForm: {
        name: '',
    },
    rules: {
        name: [{ required: true, message: '', trigger: 'blur' },],
    },
    timeArr: '',
    count_money: '',
    count_recharge_money: '',
})
const ruleFormRef = ref<FormInstance>()

const timeChange = (time) => {
    state.timeArr = time
    getData()
}

// 获取数据
const getData = async () => {
    state.loading = true
    state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
    state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
    recharge_bonus_log_post({ ...state.pageForm }).then(res => {
        state.tableData = res.data
        state.pageForm.total = res.count
        state.count_money = res.count_money
        state.count_recharge_money = res.count_recharge_money
    })
    state.loading = false
}
getData();// 获取数据


const getSummaries = (param) => {
    const { columns, data } = param;
    const sums = [];


    (sums[0] as any) = '合计';

    (sums[3] as any) = state.count_money;

    (sums[4] as any) = state.count_recharge_money;
    return sums
}
</script>
  
<style lang="scss" scoped></style>
  
  