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
            <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
                <el-table-column prop="uid" label="用户" header-align="center" :align="'center'" sortable>
                    <template #default="scope">
                        <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
                            `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="username" label="渠道" header-align="center" :align="'center'" sortable />
                <el-table-column prop="add_time" label="日期" header-align="center" :align="'center'" sortable />
                <el-table-column prop="before_code" label="变动前打码量" header-align="center" :align="'center'" sortable />
                <el-table-column prop="after_money" label="变动后打码量" header-align="center" :align="'center'" sortable />
                <el-table-column prop="code_type" label="变动类型" header-align="center" :align="'center'" sortable
                    :formatter="codeTypeStr" />
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
import { bet_code_log_list_post } from '../../api/logrecordManagement'
import pagination from "@/components/pagination/index.vue"
import confStore from "@/store/modules/conf";
import datetime from "@/components/datetime/index.vue"
import { goToUserInfo } from "@/utils/baseFun"

const router = useRouter();
const store = confStore();
const state = reactive({
    loading: false, // table loading
    dialogFormVisible: false,
    agent_list: computed(() => store.agent_list), // 渠道列表
    tableData: [],
    pageForm: {
        page: 1,
        limit: 20,
        total: 0,
        cid: null,
        uid: null,
        stime: null,
        etime: null,
    },
    timeArr: ''
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
    bet_code_log_list_post({ ...state.pageForm }).then(res => {
        state.pageForm.total = res.count
        state.tableData = res.data
    }).finally(() => {
        state.loading = false
    })
}
getData();// 获取数据


// 删除
const codeTypeStr = (row) => {
    if (row.code_type == 1) {
        return '用户打码'
    }
}

// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}
</script>
  
<style lang="scss" scoped></style>
  
  