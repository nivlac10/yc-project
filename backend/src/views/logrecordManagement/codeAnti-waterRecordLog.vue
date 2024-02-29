<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-input v-model="state.pageForm.uid" placeholder="请输入用户名或uid" style="width: 200px;" clearable />
      <el-input v-model="state.pageForm.task_id" placeholder="请输入任务id" style="width: 200px;" clearable />
      <div>
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>

    <!-- 反水打码日志 -->
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%; " show-summary
        :summary-method="getSummaries">
        <el-table-column prop="uid" label="用户" header-align="center" :align="'center'" width="180">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
          </template>

        </el-table-column>
        <el-table-column prop="task_id" label="任务id" header-align="center" :align="'center'" />
        <el-table-column prop="nickname" label="用户名" header-align="center" :align="'center'" />
        <el-table-column prop="bet" label="打码量" header-align="center" :align="'center'" />
        <el-table-column prop="add_time" label="领取时间" header-align="center" :align="'center'" />
        <el-table-column prop="money" label="领取金额" header-align="center" :align="'center'" />
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
import { bet_task_log_list_post } from "../../api/logrecordManagement";
import datetime from "@/components/datetime/index.vue"
import pagination from "@/components/pagination/index.vue"
import { goToUserInfo } from "@/utils/baseFun"

const router = useRouter();

const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  agent_list: [], // 渠道列表
  timeArr: '',
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    stime: '',// 起始日期
    etime: '',// 结束日期
    uid: '',
    task_id: '',
  },
  total_money: 0,
  tableData: [],
  gameTypeList: [],
})
const ruleFormRef = ref<FormInstance>()



// 获取数据
const getData = async () => {
  state.loading = true
  state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
  bet_task_log_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res.count
    state.tableData = res.data
    state.total_money = res.count_money
    state.loading = false
  })
}

const timeChange = (time) => {
  state.timeArr = time
  getData()
}

// 搜索数据
const searchData = () => {
  getData();// 获取数据
}

const getSummaries = (param) => {
  const { columns, data } = param;
  const sums = [];


  (sums[0] as any) = '合计';


  (sums[5] as any) = state.total_money;
  return sums
}
// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>

<style lang="scss" scoped></style>

