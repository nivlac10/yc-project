<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-input v-model="state.pageForm.uid" placeholder="请输入用户名或uid" style="width: 200px;" clearable />
      <el-select v-model="state.pageForm.user_type" class="m-2" placeholder="请选择">
        <el-option v-for="item in state.order_list" :key="item['label']" :label="item['value']" :value="item['label']" />
      </el-select>
      <datetime @def="timeChange" />
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
        :summary-method="getSummaries">
        <el-table-column prop="day" label="日期" header-align="center" :align="'center'" width="120px" fixed="left" />
        <el-table-column prop="uid" label="用户名" header-align="center" :align="'center'" fixed="left" width="180">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="total_bet" label="每日打码" header-align="center" :align="'center'" width="150px" sortable />
        <el-table-column prop="total_recharge" label="充值金额" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="recharge_num" label="充值成功笔数" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="total_withdraw" label="提现金额" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="withdraw_num" label="提现笔数" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_one_user_num" label="一级人数" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_two_user_num" label="二级人数" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_three_user_num" label="三级人数" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_one_recharge" label="一级充值" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_two_recharge" label="二级充值" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_three_recharge" label="三级充值" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_one_recharge_user_num" label="一级充值人数" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_two_recharge_user_num" label="二级充值人数" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_three_recharge_user_num" label="三级充值人数" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_one_withdraw" label="一级提现" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_two_withdraw" label="二级提现" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_three_withdraw" label="三级提现" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_one_withdraw_user_num" label="一级提现人数" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_two_withdraw_user_num" label="二级提现人数" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_three_withdraw_user_num" label="三级提现人数" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_one_bet" label="一级打码" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_two_bet" label="二级打码" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_three_bet" label="三级打码" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_one_win" label="一级赢分" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_two_win" label="二级赢分" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_three_win" label="三级赢分" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_one_real_win" label="一级实际输赢" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_two_real_win" label="二级实际输赢" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_three_real_win" label="三级实际输赢" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_one_bet_num" label="一级注单数" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_two_bet_num" label="二级注单数" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_three_bet_num" label="三级注单数" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_one_bet_user_num" label="一级团队人数" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_two_bet_user_num" label="二级团队人数" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="team_three_bet_user_num" label="三级团队人数" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_one_bet_brokerage" label="一级打码佣金" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_two_bet_brokerage" label="二级打码佣金" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_three_bet_brokerage" label="三级打码佣金" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_recharge_brokerage" label="邀请首冲佣金" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="team_invite_task_brokerage" label="邀请任务佣金" header-align="center" :align="'center'"
          width="150px" sortable />
        <el-table-column prop="total_win" label="总赢分" header-align="center" :align="'center'" width="150px" sortable />
        <el-table-column prop="total_num" label="注单数" header-align="center" :align="'center'" width="150px" sortable />
        <el-table-column prop="give_money" label="总赠送" header-align="center" :align="'center'" width="150px" sortable />
        <el-table-column prop="vip_up" label="vip晋升赠送" header-align="center" :align="'center'" width="150px" sortable />
        <el-table-column prop="vip_day" label="vip日赠送" header-align="center" :align="'center'" width="150px" sortable />
        <el-table-column prop="vip_week" label="vip周赠送" header-align="center" :align="'center'" width="150px" sortable />
        <el-table-column prop="vip_month" label="vip月赠送" header-align="center" :align="'center'" width="150px" sortable />
        <el-table-column prop="first_recharge_give" label="首次充值赠送" header-align="center" :align="'center'" width="150px"
          sortable />
        <el-table-column prop="day_first_recharge_give" label="每日首次充值赠送" header-align="center" :align="'center'"
          width="150px" />
        <el-table-column prop="system_give" label="系统赠送" header-align="center" :align="'center'" width="150px" sortable />

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
import { user_day_report_list_post } from "@/api/dataReport";
import { goToUserInfo } from "@/utils/baseFun"
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  timeArr: '',
  tableData: [],
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    user_type: 0,
    uid: '',
    stime: '',
    etime: '',
  },
  total: [],
  order_list: [
    { label: 0, value: '默认排序' },
    { label: 1, value: '一级人数' },
    { label: 2, value: '一级充值' },
    { label: 3, value: '首次赠送' },
    { label: 4, value: '充值金额' },
    { label: 5, value: '打码量' }
  ],
})
const ruleFormRef = ref<FormInstance>()

// // 获取选择数据
// const getSelectData = () => {
//   // 渠道
//   agent_list_post({ limit: 999, page: 1 }).then((res: any) => {
//     state.agent_list = res.data
//   })
// }
// getSelectData()// 获取选择数据

// 获取数据
const getData = async () => {
  state.loading = true
  user_day_report_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res.total['con']
    state.total = res.total
    state.tableData = res.data
  })
  state.loading = false
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

const getSummaries = (param) => {
  const { columns, data } = param;
  const sums = [];


  (sums[0] as any) = '合计';
  (sums[2] as any) = state.total['total_bet'];
  (sums[3] as any) = state.total['total_recharge'];
  (sums[4] as any) = state.total['recharge_num'];
  (sums[5] as any) = state.total['total_withdraw'];
  (sums[6] as any) = state.total['withdraw_num'];
  (sums[7] as any) = state.total['team_one_user_num'];
  (sums[8] as any) = state.total['team_two_user_num'];
  (sums[9] as any) = state.total['team_three_user_num'];
  (sums[10] as any) = state.total['team_one_recharge'];
  (sums[11] as any) = state.total['team_two_recharge'];
  (sums[12] as any) = state.total['team_three_recharge'];
  (sums[13] as any) = state.total['team_one_recharge_user_num'];
  (sums[14] as any) = state.total['team_two_recharge_user_num'];
  (sums[15] as any) = state.total['team_three_recharge_user_num'];
  (sums[16] as any) = state.total['team_one_withdraw'];
  (sums[17] as any) = state.total['team_two_withdraw'];
  (sums[18] as any) = state.total['team_three_withdraw'];
  (sums[19] as any) = state.total['team_one_withdraw_user_num'];
  (sums[20] as any) = state.total['team_two_withdraw_user_num'];
  (sums[21] as any) = state.total['team_three_withdraw_user_num'];
  (sums[22] as any) = state.total['team_one_bet'];
  (sums[23] as any) = state.total['team_two_bet'];
  (sums[24] as any) = state.total['team_three_bet'];
  (sums[25] as any) = state.total['team_one_win'];
  (sums[26] as any) = state.total['team_two_win'];
  (sums[27] as any) = state.total['team_three_win'];
  (sums[28] as any) = state.total['team_one_real_win'];
  (sums[29] as any) = state.total['team_two_real_win'];
  (sums[30] as any) = state.total['team_three_real_win'];
  (sums[31] as any) = state.total['team_one_bet_num'];
  (sums[32] as any) = state.total['team_two_bet_num'];
  (sums[33] as any) = state.total['team_three_bet_num'];
  (sums[34] as any) = state.total['team_one_bet_user_num'];
  (sums[35] as any) = state.total['team_two_bet_user_num'];
  (sums[36] as any) = state.total['team_three_bet_user_num'];
  (sums[37] as any) = state.total['team_one_bet_brokerage'];
  (sums[38] as any) = state.total['team_two_bet_brokerage'];
  (sums[39] as any) = state.total['team_three_bet_brokerage'];
  (sums[40] as any) = state.total['team_recharge_brokerage'];
  (sums[41] as any) = state.total['team_invite_task_brokerage'];
  (sums[42] as any) = state.total['total_win'];
  (sums[43] as any) = state.total['total_num'];
  (sums[44] as any) = state.total['give_money'];
  (sums[45] as any) = state.total['vip_up'];
  (sums[46] as any) = state.total['vip_day'];
  (sums[47] as any) = state.total['vip_week'];
  (sums[48] as any) = state.total['vip_month'];
  (sums[49] as any) = state.total['first_recharge_give'];
  (sums[50] as any) = state.total['day_first_recharge_give'];
  (sums[51] as any) = state.total['system_give'];
  return sums
}

</script>
  
<style lang="scss" scoped></style>