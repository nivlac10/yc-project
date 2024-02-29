<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-select v-model="state.searchForm.sort_index" class="m-2" placeholder="充值排序" clearable>
        <el-option label="充值" value="0" />
        <el-option label="提现" value="1" />
      </el-select>
      <div>
        <el-select v-model="state.searchForm.status" class="m-2" placeholder="所有状态" clearable>
          <el-option v-for="item in state.statusList" :label="item['label']" :value="item['val']" :key="item" />
        </el-select>
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
      <el-button type="primary" @click="editRow('add', {})">添加</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="pay_id" label="支付Id" header-align="center" :align="'center'" />
        <el-table-column prop="pay_name" label="支付名称" header-align="center" :align="'center'" />
        <el-table-column prop="pay_ratio" label="支付费率" header-align="center" :align="'center'" />
        <el-table-column prop="withdraw_ratio" label="代付费率" header-align="center" :align="'center'" />
        <el-table-column prop="min_payment_money" label="最小充值金额" header-align="center" :align="'center'" />
        <el-table-column prop="max_payment_money" label="最大充值金额" header-align="center" :align="'center'" />
        <el-table-column prop="min_transfer_money" label="最小提现金额" header-align="center" :align="'center'" />
        <el-table-column prop="max_transfer_money" label="最大提现金额" header-align="center" :align="'center'" />
        <el-table-column prop="status_str" label="充值开关" header-align="center" :align="'center'">
          <template #default="scope">
            <el-switch v-model="scope.row.status_str" class="ml-2"
              style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" @change="openRecharge(scope.row)" />
          </template>

        </el-table-column>
        <el-table-column prop="with_flag_str" label="提现开关" header-align="center" :align="'center'">
          <template #default="scope">
            <el-switch v-model="scope.row.with_flag_str" class="ml-2"
              style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" @change="openWithdraw(scope.row)" />
          </template>
        </el-table-column>
        <el-table-column prop="sort_index" label="充值权重" header-align="center" :align="'center'" />
        <el-table-column prop="withdraw_index" label="提现权重" header-align="center" :align="'center'" />
        <el-table-column prop="pay_type" label="充值方式" header-align="center" :align="'center'" :formatter="payTypeStr" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="160">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="danger" @click="deleteRow(scope.row.pay_id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-card uno-margin-top>
      <div class="pager-wrapper">
        <el-pagination background :page-sizes="paginationData.pageSizes" :total="paginationData.total"
          :page-size="paginationData.pageSize" :currentPage="paginationData.currentPage" @size-change="handleSizeChange"
          @current-change="handleCurrentChange" />
      </div>
    </el-card>
    <el-dialog v-model="state.dialogFormVisible" :title="state.operationType == 'add' ? '添加' : '编辑'" :draggable="true">
      <el-form ref="ruleFormRef" :model="state.ruleForm" :rules="state.rules" label-width="120px" class="demo-ruleForm"
        status-icon>
        <el-form-item label="支付名称" prop="pay_name">
          <el-input v-model="state.ruleForm.pay_name" />
        </el-form-item>

        <el-form-item label="支付费率(%)" prop="pay_ratio">
          <el-input v-model="state.ruleForm.pay_ratio" />
        </el-form-item>
        <el-form-item label="代付费率(%)" prop="withdraw_ratio">
          <el-input v-model="state.ruleForm.withdraw_ratio" />
        </el-form-item>
        <el-form-item label="充值权重" prop="sort_index">
          <el-input v-model="state.ruleForm.sort_index" />
        </el-form-item>
        <el-form-item label="提现权重" prop="withdraw_index">
          <el-input v-model="state.ruleForm.withdraw_index" />
        </el-form-item>
        <el-form-item label="页面回调" prop="callback_url">
          <el-input v-model="state.ruleForm.callback_url" />
        </el-form-item>
        <el-form-item label="后台回调" prop="recharge_url">
          <el-input v-model="state.ruleForm.recharge_url" />
        </el-form-item>
        <el-form-item label="提现回调" prop="withdraw_conf_url">
          <el-input v-model="state.ruleForm.withdraw_conf_url" />
        </el-form-item>
        <el-form-item label="充值开关" prop="status">
          <el-select v-model="state.ruleForm.status" class="m-2" placeholder="Select">
            <el-option v-for="item in state.statusList" :key="item.label" :label="item.label" :value="item.val" />
          </el-select>
        </el-form-item>
        <el-form-item label="提现开关" prop="with_flag">
          <el-select v-model="state.ruleForm.with_flag" class="m-2" placeholder="Select">
            <el-option v-for="item in state.withflagList" :key="item.label" :label="item.label" :value="item.val" />
          </el-select>
        </el-form-item>
        <el-form-item label="支付方式" prop="pay_type">
          <el-select v-model="state.ruleForm.pay_type" class="m-2" placeholder="Select">
            <el-option v-for="item in state.paytypeList" :key="item.label" :label="item.label" :value="item.val" />
          </el-select>
        </el-form-item>
        <el-form-item label="最小充值金额" prop="min_payment_money">
          <el-input v-model="state.ruleForm.min_payment_money" />
        </el-form-item>
        <el-form-item label="最大充值金额" prop="max_payment_money">
          <el-input v-model="state.ruleForm.max_payment_money" />
        </el-form-item>
        <el-form-item label="最小提现金额" prop="min_transfer_money">
          <el-input v-model="state.ruleForm.min_transfer_money" />
        </el-form-item>
        <el-form-item label="最大提现金额" prop="max_transfer_money">
          <el-input v-model="state.ruleForm.max_transfer_money" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleFormRef)">立即更新</el-button>
          <el-button @click="cancel">取消</el-button>
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
import { usePagination } from "@/hooks/usePagination"
import { pay_list_post, add_pay_post, pay_detail_post, update_pay_statue_post, open_withdraw_channel_post, delete_pay_channel_post } from "../../api/paymentManagement";


const router = useRouter();
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination() // 分页
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  payList: [],
  statusList: [{ label: '正常', val: 1 }, { label: '关闭', val: 0 }],
  withflagList: [{ label: '正常', val: 1 }, { label: '关闭', val: 0 }],
  paytypeList: [{ label: '二维码', val: 0 }, { label: '网页', val: 1 }, { label: '打开网站', val: 2 }],
  timeArr: '',
  searchForm: {
    page: paginationData.currentPage,
    limit: paginationData.pageSize,
    sort_index: '',
    status: '',
  },
  tableData: [],
  currentData: {},
  ruleForm: {
    pay_name: "",
    sort_index: "",
    callback_url: '',
    recharge_url: '',
    withdraw_conf_url: '',
    pay_ratio: "",
    withdraw_ratio: "",
    max_payment_money: '',
    max_transfer_money: '',
    min_payment_money: '',
    min_transfer_money: '',
    withdraw_index: '',
    status: 0,
    with_flag: '',
    pay_type: 1,
  },
  rules: {
    name: [
      { required: true, message: '', trigger: 'blur' },
    ],
    pay_ratio: [
      { required: true, message: '', trigger: 'blur' },
    ],
    withdraw_ratio: [
      { required: true, message: '', trigger: 'blur' },
    ],
    type: [
      { required: true, message: '', trigger: 'blur' },
    ],
    sort_index: [
      { required: true, message: '', trigger: 'blur' },
    ],
    withdraw_index: [
      { required: true, message: '', trigger: 'blur' },
    ],
    callback_url: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
  rechargeSwitch: true,
  paySwitch: true,
})
const ruleFormRef = ref<FormInstance>()



// 获取数据
const getData = async () => {
  state.loading = true;

  pay_list_post({ ...state.searchForm }).then(res => {
    paginationData.total = res.count
    state.tableData = res.data;
    state.tableData.map((v: any) => {
      if (v.with_flag == 1) {
        v.with_flag_str = true;
      } else {
        v.with_flag_str = false;
      }

      if (v.status == 1) {
        v.status_str = true;
      } else {
        v.status_str = false;
      }
    })
    state.loading = false;
  });
}

// 搜索数据
const searchData = () => {
  paginationData.currentPage = 1
  getData();// 获取数据
}

//更新数据
const refreshData = (code: number) => {
  if (code == 1) {
    cancel();
    getData()// 获取选择数据
  }
}
// 分页
watch(() => paginationData.currentPage, (val: number) => {
  getData();// 获取数据
}, { deep: true, immediate: true })


const payTypeStr = (row) => {
  console.log(row.pay_type)
  if (row.pay_type == 0) {
    return "二维码"
  } else if (row.pay_type == 1) {
    return "网页"
  } else if (row.pay_type == 2) {
    return "打开网站"
  }
}

// 添加||编辑
const editRow = (type: string, data?) => {
  if (type == 'add') state.operationType = 'add'
  else state.operationType = 'edit'
  resetForm(ruleFormRef.value) // 重置表单
  if (data) {
    state.ruleForm = data as any;
  }


  state.dialogFormVisible = true
}

// 取消
const cancel = () => {
  state.dialogFormVisible = false
}


// 启用支付
const openRecharge = (row) => {
  if (row.status_str) {
    row.status = 1
  } else {
    row.status = 0
  }

  update_pay_statue_post({ pay_id: row.pay_id, status: row.status }).then(res => {
    refreshData(res.code)
  })
}

// 启用提现
const openWithdraw = (row) => {
  if (row.with_flag_str) {
    row.with_flag = 1
  } else {
    row.with_flag = 0
  }
  open_withdraw_channel_post({ pay_id: row.pay_id, status: row.with_flag }).then(res => {
    refreshData(res.code)
  })
}

// 删除支付通道
const deleteRow = (id) => {
  delete_pay_channel_post({ pay_id: id }).then(res => {
    refreshData(res.code)
  })
}

// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      let requestApi = null;
      if (state.operationType == 'add') requestApi = add_pay_post
      else requestApi = pay_detail_post
      requestApi({ ...state.ruleForm }).then(res => {
        if (res.code == 1) {
          refreshData(res.code)
          state.dialogFormVisible = false
        }
      })
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

</script>

<style lang="scss" scoped></style>

