<template>
    <div class="app-container">
        <el-card class="box-card box-card-top">
            <el-input v-model="state.pageForm.uid" placeholder="请输入用户名或uid" style="width: 200px;" clearable />

            <el-select v-model="state.pageForm.cid" class="m-2" placeholder="所有渠道" clearable>
                <el-option v-for="item in state.agent_list" :key="item['cid']" :label="item['username']"
                    :value="item['cid']" />
            </el-select>
            <div>
                <datetime @def="timeChange" />
            </div>
            <el-button type="primary" @click="searchData">搜索</el-button>
        </el-card>
        <el-card class="box-card" uno-margin-top>
            <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
                <el-table-column prop="id" label="ID" header-align="center" :align="'center'" sortable />
                <el-table-column prop="username" label="渠道" header-align="center" :align="'center'" sortable />
                <el-table-column prop="uid" label="用户" header-align="center" :align="'center'" width="180">
                    <template #default="scope">
                        <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
                            `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="money" label="金额" header-align="center" :align="'center'" sortable />
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
import { goToUserInfo } from "@/utils/baseFun"
import popconfirm from "@/components/popconfirm/index.vue"
import { dezhou_bonus_log_post } from "@/api/logrecordManagement/index"
import datetime from "@/components/datetime/index.vue"
import confStore from "@/store/modules/conf";

const store = confStore();
const router = useRouter();
const state = reactive({
    loading: false, // table loading
    operationType: 'add', // add || edit
    dialogFormVisible: false,
    agent_list: [], // 渠道列表
    tableData: [
        {
            cid: '1',
            date: '2016-05-02',
            name: '王小虎',
        },
    ],
    pageForm: {
        page: 1,
        limit: 20,
        total: 0,
        cid: null,
        uid: '',
        stime: '',
        etime: ''
    },
    timeArr: ''
})
state.agent_list = store.agent_list
const ruleFormRef = ref<FormInstance>()

// 获取数据
const getData = async () => {
    state.loading = true
    state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
    state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
    dezhou_bonus_log_post({ ...state.pageForm }).then(res => {
        state.tableData = res["data"]
        state.pageForm.total = res["count"]
    })
    state.loading = false
}
getData();// 获取数据

const timeChange = (time) => {
    state.timeArr = time
    getData()
}

// 搜索数据
const searchData = () => {
    getData();// 获取数据
}

</script>
  
<style lang="scss" scoped></style>
  
  