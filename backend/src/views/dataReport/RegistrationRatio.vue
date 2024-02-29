<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-select v-model="state.pageForm.cid" class="m-2" placeholder="请选择">
        <el-option label="所有渠道" value=""></el-option>
        <el-option v-for="item in state.agent_list" :key="item['cid']" :label="item['username']" :value="item['cid']" />
      </el-select>
      <datetime @def="timeChange" />
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
        :summary-method="getSummaries">
        <el-table-column prop="day" label="日期" header-align="center" :align="'center'" width="120px" fixed="left" />
        <el-table-column prop="num" label="总用户数" header-align="center" :align="'center'" />
        <el-table-column prop="phone_num" label="手机注册(百分比)" header-align="center" :align="'center'"
          :formatter="phone_num_formatter" />
        <el-table-column prop="face_num" label="Facebook注册(百分比)" header-align="center" :align="'center'"
          :formatter="face_num_formatter" />
        <el-table-column prop="email_num" label="邮箱注册(百分比)" header-align="center" :align="'center'"
          :formatter="email_num_formatter" />
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
import { agent_list_post } from "@/api/channelManagement";
import datetime from "@/components/datetime/index.vue"
import { user_day_report_post } from "@/api/dataReport";
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  agent_list: [],
  timeArr: '',
  tableData: [],
  totalData: {},
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    cid: '',
    stime: '',
    etime: '',
  },
})
const ruleFormRef = ref<FormInstance>()

// 获取选择数据
const getSelectData = () => {
  // 渠道
  agent_list_post({ limit: 999, page: 1 }).then((res: any) => {
    state.agent_list = res.data
  })
}
getSelectData()// 获取选择数据

const phone_num_formatter = (row) => {
  return `${row.phone_num}(${row.phone_ratio}%)`
}
const face_num_formatter = (row) => {
  return `${row.face_num}(${row.face_ratio}%)`
}
const email_num_formatter = (row) => {
  return `${row.email_num}(${row.email_ratio}%)`
}

const getSummaries = (param) => {
  const { columns, data } = param
  const sums: string[] = []
  columns.forEach((column, index) => {
    if (index === 0) return sums[index] = '合计'
    else if (index == 1) return sums[index] = `${state.totalData['num']}`
    else if (index == 2) return sums[index] = `${state.totalData['phone_num']}(${state.totalData['phone_ratio']}%)`
    else if (index == 3) return sums[index] = `${state.totalData['face_num']}(${state.totalData['face_ratio']}%)`
    else if (index == 4) return sums[index] = `${state.totalData['email_num']}(${state.totalData['email_ratio']}%)`
  })

  return sums
}

// 获取数据
const getData = async () => {
  state.loading = true
  user_day_report_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res.count
    state.tableData = res.data
    state.totalData = res.total
    state.loading = false
  })
}

const timeChange = (time) => {
  state.timeArr = time
  state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
  getData()
}

// 搜索数据
const searchData = () => {
  getData()
}
</script>
  
<style lang="scss" scoped></style>