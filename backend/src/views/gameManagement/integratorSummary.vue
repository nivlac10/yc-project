<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-select v-model="state.pageForm.cid" class="m-2" placeholder="所有渠道" clearable>
        <el-option v-for="item in state.agent_list" :key="item['cid']" :label="item['username']" :value="item['cid']" />
      </el-select>
      <div>
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="factory_name" label="集成商" header-align="center" :align="'center'" />
        <el-table-column prop="total_bet" label="压分" header-align="center" :align="'center'" />
        <el-table-column prop="total_shu_ying" label="赢分" header-align="center" :align="'center'" />
        <el-table-column prop="gl" label="运行概率" header-align="center" :align="'center'" />
        <el-table-column prop="total_real_shu_ying" label="输赢" header-align="center" :align="'center'" />
        <el-table-column prop="total_num" label="注单数" header-align="center" :align="'center'" />
        <el-table-column prop="ol_num" label="在线人数" header-align="center" :align="'center'" />
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
import { factory_game_total_post } from "../../api/gameManagement";
import { agent_list_post } from "../../api/channelManagement";
import { factory_list_post } from "../../api/IntegratorManagement";
import datetime from "@/components/datetime/index.vue"
import pagination from "@/components/pagination/index.vue"
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  agent_list: [], // 渠道列表
  timeArr: '',
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    stime: '',// 起始日期
    etime: '',// 结束日期
    cid: '',// 渠道
  },
  tableData: [],
  ruleForm: {
    name: '',
  },
  rules: {
    name: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
})
const ruleFormRef = ref<FormInstance>()

// 获取选择数据
const getSelectData = () => {
  // 渠道
  agent_list_post({ limit: 999, page: 1 }).then(res => {
    state.agent_list = res['data']
  })
}
getSelectData()// 获取选择数据


// 获取数据
const getData = async () => {
  state.loading = true
  state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
  factory_game_total_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res['count']
    state.tableData = res['data']
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

</script>

<style lang="scss" scoped></style>

