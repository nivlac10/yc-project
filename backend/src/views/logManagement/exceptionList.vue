<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <div>
        <datetime @def="timeChange" />
      </div>
        <el-input v-model="state.pageForm.uid" placeholder="请输入用户名或uid" style="width: 200px;" clearable />
        <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="id" label="UID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="uid" label="用户名" header-align="center" :align="'center'" width="180">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
          </template>

        </el-table-column>
        <el-table-column prop="ip" label="IP" header-align="center" :align="'center'" />
        <el-table-column prop="info" label="详情" header-align="center" :align="'center'" />
        <el-table-column prop="add_time" label="新增时间" header-align="center" :align="'center'" sortable />
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
import { unusual_user_log_post } from "../../api/logManagement";
import pagination from "@/components/pagination/index.vue"
import datetime from "@/components/datetime/index.vue"
import { goToUserInfo } from "@/utils/baseFun"
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  timeArr: '',
  tableData: [],
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    uid : ''
  },
})

// 获取数据
const getData = async () => {
  state.loading = true
  const obj = {
    limit: state.pageForm.limit,
    page: state.pageForm.page,
    uid: state.pageForm.uid,
    stime: state.timeArr ? state.timeArr[0] : '',
    etime: state.timeArr ? state.timeArr[1] : ''
  }
  unusual_user_log_post({ ...obj }).then(res => {
    state.pageForm.total = res.count
    state.tableData = res.data
    state.loading = false
  })
}

// 搜索数据
const searchData = () => {
  getData();// 获取数据
}

const timeChange = (time) => {
  state.timeArr = time
  getData()
}

</script>

<style lang="scss" scoped></style>

