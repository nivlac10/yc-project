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
                <el-select v-model="state.pageForm.order" class="m-2" placeholder="排序" clearable>
                    <el-option v-for="item in state.order_list" :key="item" :label="item.label" :value="item.val" />
                </el-select>
                <el-select v-model="state.pageForm.order_type" class="m-2" placeholder="排序方式" clearable>
                    <el-option v-for="item in state.order_type" :key="item" :label="item.label" :value="item.val" />
                </el-select>
                <el-button type="primary" @click="getData()">搜索</el-button>
            </div>
        </el-card>
        <el-card class="box-card" uno-margin-top>
            <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
                :summary-method="getSummaries">
                <el-table-column prop="uid" label="用户" header-align="center" :align="'center'" sortable>
                    <template #default="scope">
                        <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
                            `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="username" label="渠道" header-align="center" :align="'center'" sortable />
                <el-table-column prop="money" label="赠送金额" header-align="center" :align="'center'" sortable />
                <el-table-column prop="user_sum" label="总次量" header-align="center" :align="'center'" sortable />
                <el-table-column prop="add_time" label="日期" header-align="center" :align="'center'" sortable />
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
import confStore from "@/store/modules/conf";
import { roller_money_log_post } from "@/api/logrecordManagement"
import datetime from "@/components/datetime/index.vue"
import { goToUserInfo } from "@/utils/baseFun"

const router = useRouter();
const store = confStore();
const state = reactive({
    loading: false, // table loading
    operationType: 'add', // add || edit
    dialogFormVisible: false,
    agent_list: computed(() => store.agent_list), // 渠道列表
    tableData: [],
    pageForm: {
        page: 1,
        limit: 20,
        total: 0,
        uid: '',
        cid: '',
        order: null,
        order_type: null,
        stime: '',
        etime: ''
    },
    total_money: 0,
    timeArr: '',
    order_type: [
        { val: 'asc', label: '升序' },
        { val: 'desc', label: '降序' },
    ],
    order_list: [
        { val: 'a.add_time', label: '默认排序' },
        { val: 'user_sum', label: '总次量' },
        { val: 'a.money', label: '赠送金额' },
    ]
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
    roller_money_log_post({ ...state.pageForm }).then(res => {
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
  
  