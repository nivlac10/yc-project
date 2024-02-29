<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">

      <el-select v-model="state.pageForm.sort_index" class="m-2" placeholder="">
        <el-option label="默认排序" value="day" />
        <el-option label="压分" value="total_bet" />
        <el-option label="赢分" value="total_shu_ying" />
        <el-option label="输赢" value="total_real_shu_ying" />
      </el-select>
      <div>
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
        :summary-method="getSummaries">

        <el-table-column prop="day" label="日期" header-align="center" :align="'center'" />
        <el-table-column prop="total_bet" label="压分" header-align="center" :align="'center'" />
        <el-table-column prop="total_shu_ying" label="赢分" header-align="center" :align="'center'" />
        <el-table-column prop="gl" label="运行概率" header-align="center" :align="'center'">
          <template #default="scope">
            {{ scope.row.gl.toFixed(2) }}%
          </template>
        </el-table-column>
        <el-table-column prop="total_num" label="注单数" header-align="center" :align="'center'" />
        <el-table-column prop="total_real_shu_ying" label="输赢" header-align="center" :align="'center'" />
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
import { game_id_data_post } from "@/api/adminHome/index"
import datetime from "@/components/datetime/index.vue"

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
    sort_index: 'day',
    stime: '',
    etime: ''
  },
  total: [],
  timeArr: ''
})
const ruleFormRef = ref<FormInstance>()

// 获取数据
const getData = async () => {
  state.loading = true
  state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
  game_id_data_post({ ...state.pageForm }).then(res => {
    state.tableData = res["data"]
    state.pageForm.total = res['count']['con']
    state.total = res['count']
  })
  state.loading = false
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


  (sums[1] as any) = state.total['total_bet'];
  (sums[2] as any) = state.total['total_shu_ying'];
  (sums[3] as any) = state.total['gl'];
  (sums[4] as any) = state.total['total_num'];
  (sums[5] as any) = state.total['total_real_shu_ying'];
  return sums
}


</script>
  
<style lang="scss" scoped></style>
  
  