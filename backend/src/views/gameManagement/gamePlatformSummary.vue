<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-select v-model="state.pageForm.cid" class="m-2" placeholder="所有渠道" clearable>
        <el-option v-for="item in state.agent_list" :key="item['cid']" :label="item['username']" :value="item['cid']" />
      </el-select>
      <el-select v-model="state.pageForm.game_id" class="m-2" placeholder="平台名称" clearable>
        <el-option v-for="item in state.factory_details_list" :key="item['game_id']" :label="item['game_name']"
          :value="item['game_id']" />
      </el-select>
      <el-select v-model="state.pageForm.sort_index" class="m-2" placeholder="">
        <el-option label="默认排序" value="game_id" />
        <el-option label="压分" value="total_bet" />
        <el-option label="平台id" value="my_game" />
      </el-select>
      <div>
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
                :summary-method="getSummaries">
        <el-table-column prop="game_name" label="游戏" header-align="center" :align="'center'" />
        <el-table-column prop="total_bet" label="压分" header-align="center" :align="'center'" />
        <el-table-column prop="total_shu_ying" label="赢分" header-align="center" :align="'center'" />
        <el-table-column prop="gl" label="运行概率" header-align="center" :align="'center'" />
        <el-table-column prop="total_real_shu_ying" label="输赢" header-align="center" :align="'center'" />
        <el-table-column prop="total_num" label="注单数" header-align="center" :align="'center'" />
        <el-table-column prop="user_num" label="在线人数" header-align="center" :align="'center'" />
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
import { game_day_data_post, game_list_post } from "../../api/gameManagement";
import { agent_list_post } from "../../api/channelManagement";
import datetime from "@/components/datetime/index.vue"
import pagination from "@/components/pagination/index.vue"
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  agent_list: [], // 渠道列表
  factory_details_list: [], // 平台名称列表
  timeArr: '',
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    stime: '',// 起始日期
    etime: '',// 结束日期
    game_id: '',// 游戏
    cid: '',// 渠道
    sort_index: 'game_id', // 排序列明
  },
  tableData: [],
  totalData:{
    total_bet:0,
    total_shu_ying:0,
    gl:0,
    total_real_shu_ying:0,
    total_num:0,
    user_num:0,
  },
})

// 获取选择数据
const getSelectData = () => {
  // 渠道
  agent_list_post({ limit: 999, page: 1 }).then(res => {
    state.agent_list = res['data']
  })
  // 游戏平台 集成商详情接口
  game_list_post({ limit: 999, page: 1 }).then(res => {
    state.factory_details_list = res['data']
  })
}
getSelectData()// 获取选择数据


// 获取数据
const getData = async () => {
  state.loading = true
  state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
  game_day_data_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res['count']
    state.tableData = res['data']
    state.totalData=res['total']
    state.loading = false
    console.log(state.totalData)
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


    (sums[1] as any) = state.totalData.total_bet;
    (sums[2] as any) = state.totalData.total_shu_ying;
    (sums[3] as any) = state.totalData.gl;
    (sums[4] as any) = state.totalData.total_real_shu_ying;
    (sums[5] as any) = state.totalData.total_num;
    (sums[6] as any) = state.totalData.user_num;
    return sums
}

</script>

<style lang="scss" scoped></style>

