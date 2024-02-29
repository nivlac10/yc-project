<template>
    <div class="app-container">
        <el-card class="box-card box-card-top">

            <div>
                <datetime @def="timeChange" />
            </div>
            <div style="width: 100%;">
                <el-input v-model="state.searchForm.uid" placeholder="请输入用户名或uid" style="width: 200px;" clearable />

                <el-select v-model="state.searchForm.cid" class="m-2" placeholder="渠道" clearable>
                    <el-option v-for="item in state.agent_list" :key="item['cid']" :label="item['username']"
                        :value="item['cid']" />
                </el-select>
                <el-select v-model="state.searchForm.bonus_type" class="m-2" placeholder="奖金类型" clearable>
                    <el-option v-for="item in state.bonus_type_list" :key="item['label']" :label="item['value']"
                        :value="item['label']" />
                </el-select>
                <el-select v-model="state.searchForm.get_type" class="m-2" placeholder="领取类型" clearable>
                    <el-option v-for="item in state.get_type_list" :key="item['label']" :label="item['value']"
                        :value="item['label']" />
                </el-select>
                <el-select v-model="state.searchForm.status" class="m-2" placeholder="领取状态" clearable>
                    <el-option v-for="item in state.status" :key="item['label']" :label="item['value']"
                        :value="item['label']" />
                </el-select>
                <el-button type="primary" @click="searchData">搜索</el-button>
            </div>
        </el-card>
        <el-card class="box-card" uno-margin-top>
            <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
                :summary-method="getSummaries">
                <el-table-column prop="uid" label="用户" header-align="center" :align="'center'" fixed="left" width="180">
                    <template #default="scope">
                        <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
                            `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="day" label="日期" header-align="center" :align="'center'" sortable />
                <el-table-column prop="unlock_time" label="可领取日期" header-align="center" :align="'center'" sortable />
                <el-table-column prop="get_time" label="领取时间" header-align="center" :align="'center'">
                    <template #default="scope">
                        {{ scope.row.get_time ? scope.row.get_time : "未领取" }}
                    </template>
                </el-table-column>
                <el-table-column prop="bonus_type" label="奖金类型" header-align="center" :align="'center'"
                    :formatter="bonusFormatter" />
                <el-table-column prop="get_type" label="领取类型" header-align="center" :align="'center'"
                    :formatter="getFormatter" sortable />
                <el-table-column prop="bonus" label="金额" header-align="center" :align="'center'" sortable />
                <el-table-column prop="status" label="领取状态" header-align="center" :align="'center'">
                    <template #default="scope">
                        <span v-if="scope.row.status == 0">未领取</span>
                        <span v-if="scope.row.status == 1" style="color: green;">已领取</span>
                        <span v-if="scope.row.status == 2" style="color: red;">已过期</span>
                        <span v-if="scope.row.status == 3" style="color:aqua">等待领取</span>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>
        <el-card uno-margin-top>
            <div class="pager-wrapper">
                <pagination :pageForm="state.searchForm" @def="getData" />
            </div>
        </el-card>
    </div>
</template>
<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { storeToRefs } from 'pinia';
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import { vip_bonus_log_list } from '@/api/vipsystemManagement'
import { goToUserInfo } from "@/utils/baseFun"
import pagination from "@/components/pagination/index.vue"
import datetime from "@/components/datetime/index.vue"
import confStore from "@/store/modules/conf";

const store = confStore();
const router = useRouter();
let { agent_list } = storeToRefs(store);
const state = reactive({
    loading: false, // table loading
    operationType: 'add', // add || edit
    dialogFormVisible: false,
    timeArr: '',
    tableData: [],
    agent_list: [],
    searchForm: {
        page: 1,
        limit: 20,
        total: 0,
        uid: '',
        cid: '',
        bonus_type: '',
        get_type: '',
        stime: '',
        etime: '',
        status: null
    },
    total_money: 0,
    bonus_type_list: [
        { label: 1, value: "立即反水" },
        { label: 2, value: "拆分反水" }
    ],
    get_type_list: [
        { label: 0, value: "拆分反水" },
        { label: 1, value: "打码反水" },
        { label: 2, value: "每日反水" },
        { label: 3, value: "每周反水" },
        { label: 4, value: "每月反水" },
        { label: 5, value: "vip晋级" }
    ],
    status: [
        { label: 1, value: "已领取" },
        { label: 0, value: "未领取" },
    ]
})
const ruleFormRef = ref<FormInstance>()
state.agent_list = store.agent_list

// 获取数据
const getData = async () => {
    state.loading = true
    vip_bonus_log_list({ ...state.searchForm }).then(res => {
        if (res['code'] == 1) {
            state.tableData = res['data']
            state.searchForm.total = res['count']
            state.total_money = res['total_money']
        }
    })
    state.loading = false
}

// 日期选择
const timeChange = (time) => {
    state.searchForm.stime = time[0]
    state.searchForm.etime = time[1]
    getData()
}

// 搜索方法
const searchData = () => {
    getData()
}

const bonusFormatter = (row) => {
    if (row.bonus_type == 1) return '立即反水'
    else return '拆分反水'
}

const getFormatter = (row) => {
    if (row.get_type == 0) return '拆分反水'
    else if (row.get_type == 1) return '打码反水'
    else if (row.get_type == 2) return '每日反水'
    else if (row.get_type == 3) return '每周反水'
    else if (row.get_type == 4) return '每月反水'
    else if (row.get_type == 5) return 'vip晋级'
}


const getSummaries = (param) => {
    const { columns, data } = param;
    const sums = [];


    (sums[0] as any) = '合计';


    (sums[6] as any) = state.total_money;
    return sums
}

</script>
<style lang="scss" scoped></style>