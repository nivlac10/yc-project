<template>
  <div class="app-container">

    <el-card class="box-card box-card-top">

      <datetime @def="timeChange" />
      <div>
        <el-input v-model="state.searchForm.nickname" placeholder="请输入用户名或uid" style="width: 200px;" clearable />
        <el-input v-model="state.searchForm.username" placeholder="请输入提现人" style="width: 200px;" clearable />
        <el-input v-model="state.searchForm.CPF" placeholder="请输入提现人CPF" style="width: 200px;" clearable />
        <el-select v-model="state.searchForm.vip_lv" class="m-2" placeholder="vip等级" clearable>
          <el-option v-for="item in state.vip_lv_list" :label="item['vip_lv'].toString()" :value="item['vip_lv']" />
        </el-select>
        <el-select v-model="state.searchForm.cid" class="m-2" placeholder="所有渠道" clearable>
          <el-option v-for="item in state.agent_list" :label="item['username']" :value="item['cid']" />
        </el-select>
        <el-select v-model="state.searchForm.sort" class="m-2" placeholder="默认排序">
          <el-option v-for="item in state.sortList" :label="item['label']" :value="item['value']" />
        </el-select>
        <el-select v-model="state.searchForm.line" class="m-2" placeholder="全部" clearable>
          <el-option v-for="item in state.onlineList" :label="item['label']" :value="item['value']" />
        </el-select>
        <el-select v-model="state.searchForm.order" class="m-2" placeholder="全部" clearable>
          <el-option v-for="item in state.order" :label="item['label']" :value="item['value']" />
        </el-select>
        <el-input v-model="state.searchForm.min_money" placeholder="请输入最小充值金额" style="width: 200px;" clearable />
        <el-input v-model="state.searchForm.max_money" placeholder="请输入最大充值金额" style="width: 200px;" clearable />
        <el-input v-model="state.searchForm.min_total_bet" placeholder="请输入最小打码量" style="width: 200px;" clearable />
        <el-input v-model="state.searchForm.max_total_bet" placeholder="请输入最大打码量" style="width: 200px;" clearable />

        <el-button type="primary" @click="searchData">搜索</el-button>
      </div>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
        :summary-method="getSummaries">
        <el-table-column prop="uid" label="UID" header-align="center" :align="'center'" fixed="left" width="180">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
          </template>

        </el-table-column>
        <el-table-column prop="vip_lv" label="vip等级" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="team_one_user_num" label="代理一级人数" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="phone" label="联系方式" header-align="center" :align="'center'" width="200">
          <template #default="scope">
            手机号：{{ scope.row.phone }}
            <br>
            邮箱：{{ scope.row.email }}
          </template>
        </el-table-column>
        <el-table-column prop="team_recharge" label="团队总充值" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="total_bet" label="总打码量" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="total_num" label="注单数" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="total_real_shu_ying" label="实际输赢" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="username" label="提现信息" header-align="center" :align="'center'" width="200">
          <template #default="scope">
            提现人：{{ scope.row.username }}
            <br>
            CPF：{{ scope.row.CPF }}
          </template>
        </el-table-column>
        <el-table-column prop="commission" label="佣金" header-align="center" :align="'center'" width="120" />;
        <el-table-column prop="money" label="余额" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="total_money" label="总充值" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="total_withdraw" label="总提现" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="give_money" label="总赠送" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="total_commission" label="总佣金" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="bname" label="包名" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="cur_game" label="在线游戏" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="add_time" label="注册时间" header-align="center" :align="'center'" width="140" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230"
          v-permission="['1']">
          <template #default="scope">
            <el-button type="primary" @click="recharge(scope.row)">充值</el-button>
            <el-button type="warning" @click="disabled(scope.row.uid, scope.row.status)">{{ scope.row.status == 1 ? '禁用' :
              '启用' }}</el-button>
            <popconfirm @confirmClick="deleteRow(scope.row.uid)" />
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <pagination :pageForm="state.pageForm" @def="getData"></pagination>


    <el-dialog v-model="state.dialogFormVisible" title="用户充值" :draggable="true">
      <el-form ref="ruleFormRef" :model="state.ruleForm" :rules="state.rules" label-width="120px" class="demo-ruleForm"
        status-icon>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="state.ruleForm.username" disabled />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="state.ruleForm.nickname" disabled />
        </el-form-item>
        <el-form-item label="余额" prop="money">
          <el-input v-model="state.ruleForm.money" disabled />
        </el-form-item>
        <el-form-item label="充值金额" prop="Rmoney">
          <el-input v-model="state.ruleForm.Rmoney" />
        </el-form-item>
        <el-form-item label="打码量" prop="remain_code_amount">
          <el-input v-model="state.ruleForm.remain_code_amount" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleFormRef)">Create</el-button>
          <el-button @click="cancel">cancel</el-button>
          <!-- <el-button @click="resetForm(ruleFormRef)">Reset</el-button> -->
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import pagination from "@/components/pagination/index.vue"
import { user_list_post, delete_user_post, update_user_status_post, user_recharge_post } from "../../api/userManagenment";
import popconfirm from "@/components/popconfirm/index.vue"
import confStore from "@/store/modules/conf";
import { goToUserInfo } from "@/utils/baseFun"
import { number } from "echarts";
import datetime from "@/components/datetime/index.vue"

const router = useRouter();
const store = confStore();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  agent_list: computed(() => store.agent_list), // 渠道列表
  vip_lv_list: computed(() => store.vipLvList), //vip等级列表
  onlineList: [
    { label: '全部', value: '' },
    { label: '在线', value: 1 },
  ],
  sortList: [
    { label: '默认排序', value: 0 },
    { label: '充值金额', value: 1 },
    { label: '提现金额', value: 2 },
    { label: '余额', value: 3 },
    { label: '一级人数', value: 4 },
    { label: '总佣金', value: 5 },
    { label: '打码量', value: 6 },
    { label: '团队总充值', value: 7 },
    { label: '注册时间', value: 8 },
    { label: '注单数', value: 9 },
    { label: '实际输赢', value: 10 },
    { label: '佣金', value: 11 },
  ],
  order: [
    { label: '降序', value: 'desc' },
    { label: '升序', value: 'asc' }
  ],
  currentData: {},
  pageForm: {
    page: 1,
    limit: 20,
    total: 0
  },
  searchForm: {
    min_money: null,//最小充值金额
    max_money: null,//最大充值金额
    line: null,// 是否在线
    sort: 0,// 排序
    cid: null,// 渠道
    nickname: null,//用户名
    username: null,
    CPF: null,
    vip_lv: null,//vip等级id
    min_total_bet: null,
    max_total_bet: null,
    order: 'desc',
    stime: null,
    etime: null

  },
  tableData: [],
  tableTotal: [],
  ruleForm: {
    nickname: '',
    username: '',
    money: '',
    Rmoney: '',
    remain_code_amount: ''
  },
  rules: {

  },
  timeArr: '',
  gameTypeList: [],
})
const ruleFormRef = ref<FormInstance>()

const timeChange = (time) => {
  state.timeArr = time
  getData()
}

// 获取数据
const getData = async () => {
  state.loading = true
  state.searchForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.searchForm.etime = state.timeArr ? state.timeArr[1] : ''
  user_list_post({ page: state.pageForm.page, limit: state.pageForm.limit, ...state.searchForm }).then(res => {
    state.pageForm.total = res.count
    state.tableData = res.data;
    state.tableTotal = res.total;
    state.loading = false
  })
}

const getSummaries = (param) => {
  const { columns, data } = param;
  const sums = [];
  (sums[0] as any) = '合计';
  (sums[5] as any) = state.tableTotal['total_bet'];
  (sums[6] as any) = state.tableTotal['total_num'];
  (sums[7] as any) = state.tableTotal['total_real_shu_ying'];
  (sums[9] as any) = state.tableTotal['commission'];
  (sums[10] as any) = state.tableTotal['money'];
  (sums[11] as any) = state.tableTotal['total_money'];
  (sums[12] as any) = state.tableTotal['total_withdraw'];
  (sums[13] as any) = state.tableTotal['give_money'];
  (sums[14] as any) = state.tableTotal['total_commission'];
  // console.log(columns, data);
  return sums
}


// 搜索数据
const searchData = () => {
  state.pageForm.page = 1;
  getData();// 获取数据
}
// getData();


// 添加||编辑
const recharge = (val: any) => {
  state.ruleForm = val;
  state.ruleForm.remain_code_amount = '';
  state.dialogFormVisible = true
}

// 删除
const deleteRow = async (uid: number) => {
  let data = await delete_user_post({
    uid: uid
  })
  refreshData(data.code);
}

// 取消
const cancel = () => {
  state.dialogFormVisible = false
}

// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      userRecharge();
      console.log('submit!')
    } else {
      console.log('error submit!', fields)
    }
  })
}

//更新数据
const refreshData = (code: number) => {
  if (code == 1) {
    cancel();
    getData();
  }
}


//禁用
const disabled = async (uid: any, status: any) => {
  if (status == 1) status = 0;
  else if (status == 0) status = 1;
  let data = await update_user_status_post({ uid, status })
  refreshData(data.code);
}

//充值
const userRecharge = async () => {
  let data = await user_recharge_post({ uid: state.ruleForm['uid'], money: state.ruleForm['Rmoney'], remain_code_amount: state.ruleForm.remain_code_amount });

  refreshData(data.code);

}
</script>

<style lang="scss" scoped></style>

