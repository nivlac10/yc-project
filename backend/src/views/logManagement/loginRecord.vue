<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <div>
        <el-select v-model="state.selectVal" class="m-2" placeholder="Select" clearablen>
          <el-option v-for="item in state.options" :key="item['id']" :label="item['username']"
            :value="item['username']" />
        </el-select>
      </div>
      <div>
        <!-- <span>时间：</span> -->
        <!-- <el-date-picker v-model="state.timeArr" type="daterange" range-separator="To" start-placeholder="Start date"
          end-placeholder="End date" value-format="YYYY-MM-DD" /> -->
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="id" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="username" label="用户名" header-align="center" :align="'center'" />
        <el-table-column prop="ip" label="登陆IP" header-align="center" :align="'center'" />
        <el-table-column prop="time" label="登陆时间" header-align="center" :align="'center'" sortable />
        <el-table-column prop="status" label="登陆状态" header-align="center" :align="'center'" />
        <el-table-column prop="name" label="登陆详情" header-align="center" :align="'center'" />
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
import { login_log_post } from "../../api/logManagement";
import { admin_list_post } from "../../api/SystemManagement/user";
import pagination from "@/components/pagination/index.vue"
import datetime from "@/components/datetime/index.vue"
// import { get_power_class_post, add_power_class_post, delete_power_class } from "@/api/SystemManagement/module";

const router = useRouter();
const state = reactive({
  loading: false, // table loading
  selectVal: '',
  options: [],
  timeArr: [],
  tableData: [],
  pageForm: {
    page: 1,
    limit: 20,
    total: 0
  },
})

admin_list_post({}).then(res => {
  state.options = res.data
})

// 获取数据
const getData = async () => {
  state.loading = true
  const obj = {
    uname: state.selectVal,
    stime: state.timeArr ? state.timeArr[0] : '',
    etime: state.timeArr ? state.timeArr[1] : '',
    limit: state.pageForm.limit,
    page: state.pageForm.page
  }
  login_log_post({ ...obj }).then(res => {
    state.pageForm.total = res.count
    state.tableData = res.data
    state.loading = false
  })
}

// 搜索数据
const searchData = () => {
  state.pageForm.page = 1
  getData();// 获取数据
}
getData()

function timeChange(time) {
  state.timeArr = time
  getData()
}
</script>

<style lang="scss" scoped></style>

