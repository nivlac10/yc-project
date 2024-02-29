<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-input v-model="state.pageForm.uid" placeholder="请输入用户名或uid" style="width: 200px;" clearable
        v-if="props.userIDShow" />
      <el-select v-model="state.pageForm.pay_id" class="m-2" placeholder="所有支付" clearable>
        <el-option v-for="item in state.withdrawList" :label="item['pay_name']" :value="item['pay_id']" />
      </el-select>
      <el-select v-model="state.pageForm.status" class="m-2" placeholder="所有订单" clearable>
        <el-option v-for="item in state.ordersList" :label="item['label']" :value="item['value']" />
      </el-select>
      <el-select v-model="state.pageForm.money_type" class="m-2" placeholder="所有金额" clearable>
        <el-option v-for="item in state.moneyNumList" :label="item['label']" :value="item['value']" />
      </el-select>
      <el-input v-model="state.pageForm.min_money" placeholder="最小金额" style="width: 200px;" clearable />
      <el-input v-model="state.pageForm.max_money" placeholder="最大金额" style="width: 200px;" clearable />
      <el-select v-model="state.pageForm.sort_index" class="m-2" placeholder="默认排序">
        <el-option v-for="item in state.sort_List" :key="item['label']" :label="item['label']" :value="item['val']" />
      </el-select>
      <el-select v-model="state.pageForm.order_index" class="m-2" placeholder="排序方式">
        <el-option v-for="item in state.order_List" :key="item['label']" :label="item['label']" :value="item['val']" />
      </el-select>
      <div>
        <datetime @def="timeChange" />
      </div>

      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <div class="allBtn">
        <el-button type="primary" @click="OperationSelected(1)" v-permission="['1']">通过</el-button>
        <el-button type="danger" @click="OperationSelected(2)" v-permission="['1']">没收</el-button>
        <el-button type="warning" @click="OperationSelected(3)" v-permission="['1']">驳回</el-button>
      </div>

      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" @selection-change="getAllId"
        show-summary :summary-method="getSummaries">
        <el-table-column type="selection" width="55" fixed="left" v-permission="['1']" />
        <el-table-column prop="nickname" label="用户名" header-align="center" :align="'center'" fixed="left" width="180"
          v-if="props.userIDShow">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.nickname}(${scope.row.uid})` }}</el-button>
          </template>

        </el-table-column>
        <el-table-column prop="collection_name" label="提现人名称" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="pay_name" label="支付" header-align="center" :align="'center'" width="120">
          <template #default="scope">
            <el-button type="primary" style="width: 100%;" @click="showPop(scope.row.uid, '用户游戏汇总')">{{
              scope.row.pay_name }}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="pay_order_number" label="订单号" header-align="center" :align="'center'" width="200">
          <template #default="scope">
            <el-button type="primary" style="width: 100%;" @click="showPop(scope.row.id, '订单详情')">
              {{ scope.row.pay_order_number }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="withdraw_name" label="提现类型" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="money" label="提现金额" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="auto_flag_str" label="订单状态" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="status_str" label="订单状态" header-align="center" :align="'center'"
          width="120"></el-table-column> <el-table-column prop="add_time" label="下单时间" header-align="center"
          :align="'center'" width="160" />
        <el-table-column prop="success_time" label="回调时间" header-align="center" :align="'center'" width="160" />
        <el-table-column prop="machine_num" label="设备注册数" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="ip_num" label="ip注册数" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="total_money" label="总充值" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="total_withdraw" label="总提现" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="r_w" label="充值-提现" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="c_name" label="包名" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="c_name" label="审核原因" header-align="center" :align="'center'" width="120" />
        <el-table-column prop="c_name" label="操作" header-align="center" :align="'center'" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230">
          <template #default="scope">
            <el-button type="primary" v-permission="['1']" @click="pass(scope.row.id)"
              v-if="scope.row.status == 3">通过</el-button>
            <el-button type="danger" v-permission="['1']" @click="confiscated(scope.row.id)"
              v-if="scope.row.status == 3">没收</el-button>
            <el-button type="warning" v-permission="['1']" @click="reject(scope.row.id)"
              v-if="scope.row.status == 3">驳回</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-card uno-margin-top>
      <div class="pager-wrapper">
        <pagination :pageForm="state.pageForm" @def="getData" />
      </div>
    </el-card>
    <el-dialog v-model="state.dialogFormVisible" :title="state.popTitle" :draggable="true">
      <payPop :uid="state.uid" v-if="state.dialogFormVisible && state.popTitle == '用户游戏汇总'"></payPop>
      <orderPop :id="state.uid" v-if="state.dialogFormVisible && state.popTitle == '订单详情'"></orderPop>
      <!-- <gameRecordListPop :uid="state.uid" v-if="state.dialogFormVisible && state.popTitle == '用户游戏记录'"> -->
      <!-- </gameRecordListPop> -->
    </el-dialog>
  </div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import { ElLoading, type FormInstance } from 'element-plus'
import { withdraw_list_post, withdraw_pay_list, adopt_user_withdraw_post, refuse_user_withdraw_post, cancel_user_withdraw_post } from "../../api/paymentManagement";
import datetime from "@/components/datetime/index.vue"
import { goToUserInfo } from "@/utils/baseFun"
import payPop from "./components/payPop.vue";
import orderPop from "./components/orderDetailsPop.vue";
import gameRecordListPop from "./components/gameRecordListPop.vue";
import pagination from "@/components/pagination/index.vue"
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
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  agent_list: [], // 渠道列表
  timeArr: '',
  tableData: [],
  popTitle: '',
  total: [],
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    stime: '',// 起始日期
    etime: '',// 结束日期
    uid: props.uid,
    pay_id: null,
    money_type: null,
    status: null,
    min_money: null,
    max_money: null,
    sort_index: 'a.id',
    order_index: 'desc'
  },
  popData: [],
  allId: [],
  uid: '',
  withdrawList: [],
  ordersList: [
    { label: '下单成功', value: 0 },
    { label: '提现成功', value: 1 },
    { label: '提现失败', value: 2 },
    { label: '人工审核', value: 3 },
    { label: '成功后失败', value: 4 },
    { label: '拒绝提现', value: 5 },
    { label: '下单失败', value: 6 },
  ],
  moneyNumList: [
    { label: '余额', value: 0 },
    { label: '佣金', value: 1 },
    { label: '后台手动提现', value: 2 },
  ],
  sort_List: [
    { val: 'a.id', label: "默认排序" },
    { val: 'a.uid', label: "UID" },
    { val: 'a.order_number', label: "订单号" },
    { val: 'a.money', label: "提现金额" },
    { val: 'a.add_time', label: "下单时间" },
  ],
  order_List: [
    { val: 'desc', label: "降序" },
    { val: 'asc', label: "升序" }
  ],
})

const getSelectSelect = async () => {
  let data = await withdraw_pay_list({});
  state.withdrawList = data['pay'];

}
getSelectSelect();
// 获取数据
const getData = async () => {
  state.loading = true
  state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
  withdraw_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res.total['con'];
    state.total = res.total
    if (res.data) {
      res.data.map((data) => {
        switch (data['status']) {
          case 0:
            data['status_str'] = "下单成功"
            break;
          case 1:
            data['status_str'] = "提现成功"

            break;
          case 2:

            data['status_str'] = "提现失败"
            break;
          case 3:

            data['status_str'] = "人工审核"
            break;
          case 4:

            data['status_str'] = "成功后失败"
            break;
          case 5:

            data['status_str'] = "拒绝提现"
            break;
          case 6:

            data['status_str'] = "下单失败"
            break;

          default:
            break;
        }
      })
    }
    state.tableData = res.data;
  })
  state.loading = false;
}
const timeChange = (time) => {
  state.timeArr = time
  getData()
}

// 搜索数据
const searchData = () => {
  state.pageForm.page = 1;
  getData();// 获取数据
}

const showPop = async (uid, title) => {
  state.uid = uid;
  state.popTitle = title;
  state.dialogFormVisible = true;
}

//通过
const pass = (id) => {
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(245, 245, 245, 0.7)',
  })
  adopt_user_withdraw_post({ id }).then((data) => {
    loading.close()
    getNewData(data.code);
  });

}
// 没收
const confiscated = (id) => {
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(245, 245, 245, 0.7)',
  })
  refuse_user_withdraw_post({ id }).then((data) => {
    loading.close()
    getNewData(data.code);
  });
}
// 驳回
const reject = async (id) => {
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(245, 245, 245, 0.7)',
  })
  let data = await cancel_user_withdraw_post({ id }).then((data) => {
    loading.close()
    getNewData(data.code);
  });
}

const getNewData = (code) => {
  if (code == 1) {
    getData();
  }
}

const getAllId = (v: any) => {
  state.allId = [];
  if (v.length > 0) {
    v.map((val: any) => {
      if (val.status == 3) {
        state.allId.push(val.id);
      }
    })
  } else {
    state.allId = [];
  }


}

const OperationSelected = (val) => {

  switch (val) {
    case 1:
      state.allId.map((val) => {
        pass(val)
      })
      break;
    case 2:
      state.allId.map((val) => {
        confiscated(val)
      })
      break;
    case 3:
      state.allId.map((val) => {
        reject(val)
      })
      break;
    default:
      break;
  }
}

const getSummaries = (param) => {
  const { columns, data } = param;
  const sums = [];


  (sums[0] as any) = '合计';


  (sums[6] as any) = state.total['money'];
  return sums
}
</script>

<style lang="scss" scoped>
:deep(.el-dialog) {
  width: 70%;
}

.allBtn {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}
</style>

