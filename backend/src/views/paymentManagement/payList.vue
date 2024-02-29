<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <datetime @def="timeChange" />
      <div style="width: 100%;">
        <el-input v-model="state.searchForm.uid" placeholder="请输入用户名或uid或订单号" style="width: 22%; height: 40px;" clearable
          v-if="props.userIDShow" />
        <el-select v-model="state.searchForm.status" class="m-2" placeholder="所有订单" clearable>
          <el-option v-for="item in state.statusArr" :key="item['label']" :label="item['value']" :value="item['label']" />
        </el-select>
        <el-select v-model="state.searchForm.cid" class="m-2" placeholder="所有应用" clearable>
          <el-option v-for="item in state.channelArr" :key="item['cid']" :label="item['username']" :value="item['cid']" />
        </el-select>
        <el-select v-model="state.searchForm.pay_id" class="m-2" placeholder="所有支付" clearable>
          <el-option v-for="item in state.payArr" :key="item['pay_id']" :label="item['pay_name']"
            :value="item['pay_id']" />
        </el-select>
        <el-select v-model="state.searchForm.sort_index" class="m-2" placeholder="默认排序" clearable>
          <el-option v-for="item in state.sort_List" :key="item['label']" :label="item['label']" :value="item['val']" />
        </el-select>
        <el-select v-model="state.searchForm.order_index" class="m-2" placeholder="排序方式" clearable>
          <el-option v-for="item in state.order_List" :key="item['label']" :label="item['label']" :value="item['val']" />
        </el-select>
        <el-button type="primary" @click="searchData">搜索</el-button>
      </div>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
        :summary-method="getSummaries">
        <el-table-column prop="uid" label="用户" header-align="center" :align="'center'" fixed="left" width="180"
          v-if="props.userIDShow">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="pay_name" label="支付" header-align="center" :align="'center'" width="120">
          <template #default="scope">
            <el-button type="primary" style="width: 100%;" @click="showPop(scope.row.uid, '用户游戏汇总')">{{
              scope.row.pay_name }}</el-button>
          </template>
        </el-table-column>

        <el-table-column prop="order_number" label="平台订单号" header-align="center" :align="'center'" width="200">
          <template #default="scope">
            <el-button type="primary" style="width: 100%;" @click="showPop(scope.row.id, '订单详情')">
              {{ scope.row.order_number }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="money" label="充值金额" header-align="center" :align="'center'" />
        <el-table-column prop="status_str" label="状态" header-align="center" :align="'center'" />
        <el-table-column prop="agent" label="渠道" header-align="center" :align="'center'" />
        <el-table-column prop="merchant_param" label="来源" header-align="center" :align="'center'" />
        <el-table-column prop="user_ip" label="IP" header-align="center" :align="'center'" />
        <el-table-column prop="add_time" label="下单时间" header-align="center" :align="'center'" />
        <el-table-column prop="notify_time" label="回调时间" header-align="center" :align="'center'" />
      </el-table>
    </el-card>

    <pagination :pageForm="state.searchForm" @def="getData"></pagination>

    <el-dialog v-model="state.dialogFormVisible" :title="state.popTitle" :draggable="true">
      <payPop :uid="state.uid" v-if="state.dialogFormVisible && state.popTitle == '用户游戏汇总'"></payPop>
      <payOrderPop :id="state.uid" v-if="state.dialogFormVisible && state.popTitle == '订单详情'">
      </payOrderPop>
      <!-- <gameRecordListPop :uid="state.uid" v-if="state.dialogFormVisible && state.popTitle == '用户游戏记录'"> -->
      <!-- </gameRecordListPop> -->
    </el-dialog>
  </div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import { usePagination } from "@/hooks/usePagination"
import { recharge_list_post, recharge_conf_list_post } from "../../api/paymentManagement";
import datetime from "@/components/datetime/index.vue"
import { goToUserInfo } from "@/utils/baseFun"
import pagination from "@/components/pagination/index.vue"
import payOrderPop from "./components/payOrderDetails.vue";
import { stat } from "fs";
const router = useRouter();
const props = defineProps({
  userIDShow: {
    type: Boolean,
    default: true
  },
  uid: {
    type: String,
    default: null
  }
})
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination() // 分页
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  timeArr: '',
  uid: '',
  popTitle: '',
  type: '充值列表',
  searchForm: {
    page: 1,
    limit: 20,
    total: 0,
    stime: '',// 起始日期
    etime: '',// 结束日期
    cid: '',// 渠道
    uid: props.uid,
    pay_id: '',
    status: '',
    sort_index: 'a.id',
    order_index: 'desc'

  },
  tableData: [],
  tableTotal: [],
  statusArr: [
    { label: 0, value: '下单成功' },
    { label: 1, value: '充值成功' },
    { label: 2, value: '充值失败' },
    { label: 3, value: '下单失败' },
  ],
  sort_List: [
    { val: 'a.id', label: "序号" },
    { val: 'a.order_number', label: "订单号" },
    { val: 'a.money', label: "充值金额" },
    { val: 'a.add_time', label: "下单时间" },
  ],
  order_List: [
    { val: 'desc', label: "降序" },
    { val: 'asc', label: "升序" }
  ],
  channelArr: [],
  payArr: [],
})
const ruleFormRef = ref<FormInstance>()

// 获取选择数据
const getSelectData = () => {
  // 渠道
  recharge_conf_list_post({ limit: 999, page: 1 }).then(res => {
    state.channelArr = res['channel']
    state.payArr = res['pay']
  })
}
getSelectData()// 获取选择数据


// 获取数据
const getData = async () => {
  state.loading = true
  state.searchForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.searchForm.etime = state.timeArr ? state.timeArr[1] : ''
  recharge_list_post({ ...state.searchForm }).then(res => {
    state.searchForm.total = res.count;
    state.tableData = res.data;
    state.tableTotal = res.total_money;

  }).finally(() => {
    state.loading = false;
  })
}

const timeChange = (time) => {
  state.timeArr = time
  getData()
}

// 搜索数据
const searchData = () => {
  paginationData.currentPage = 1
  getData();// 获取数据
}

// 分页
watch(() => paginationData.currentPage, (val: number) => {
  getData();// 获取数据
}, { deep: true, immediate: true })

// 添加||编辑
const editRow = (type: string) => {
  if (type == 'add') state.operationType = 'add'
  else state.operationType = 'edit'
  resetForm(ruleFormRef.value) // 重置表单
  state.dialogFormVisible = true
}
// 删除
const deleteRow = async (cid: number) => {

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
      console.log('submit!')
    } else {
      console.log('error submit!', fields)
    }
  })
}
// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

//支付
const showPop = async (uid, title) => {
  state.uid = uid;
  state.popTitle = title;
  state.dialogFormVisible = true;
}

const getSummaries = (param) => {
  const { columns, data } = param;
  const sums = [];


  (sums[0] as any) = '合计';

  (sums[3] as any) = state.tableTotal;

  return sums
}
</script>

<style lang="scss" scoped></style>

