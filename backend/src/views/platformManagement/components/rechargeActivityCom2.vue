<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <div>
        <span>类型</span>
        <el-select v-model="state.searchForm.type" class="m-2" placeholder="类型">
          <el-option label="全部" value="" />
          <el-option v-for="(item, index) in state.type_list" :label="item.type_name" :value="item.type" />
        </el-select>
      </div>
      <div>
        <span>状态</span>
        <el-select v-model="state.searchForm.status" class="m-2" placeholder="状态">
          <el-option label="全部" value="" />
          <el-option label="关闭" value="0" />
          <el-option label="开启" value="1" />
        </el-select>
      </div>
      <el-input v-model="state.searchForm.name" placeholder="活动名称" style="width: 200px;" />
      <div>
        <!-- <span style="margin-right: 5px;">起始时间</span> -->
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
      <el-button type="primary" @click="editRow('add')">新增充值活动</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="recharge_activity_id" label="活动ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="recharge_activity_name" label="活动名称" header-align="center" :align="'center'" />
        <el-table-column prop="recharge_activity_type" label="活动类型" header-align="center" :align="'center'"
          :formatter="recharge_activity_type_formatter" />
        <el-table-column prop="recharge_activity_ladder" label="充值阶梯" header-align="center" :align="'center'" />
        <el-table-column prop="start_time" label="活动时间" header-align="center" :align="'center'" width="160">
          <template #default="scope">
            <div>{{ scope.row.start_time }}</div>
            <div>~</div>
            <div>{{ scope.row.over_time }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="活动状态" header-align="center" :align="'center'"
          :formatter="statusFormatter" />
        <el-table-column prop="add_time" label="创建时间" header-align="center" :align="'center'" sortable width="160" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="260">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="primary" @click="showClaimDetails(true, scope.row.recharge_activity_id)">领取详情</el-button>
            <popconfirm @confirmClick="deleteRow(scope.row.recharge_activity_id)" />
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-card uno-margin-top>
      <div class="pager-wrapper">
        <pagination :pageForm="state.pageForm" @def="getData" />
      </div>
    </el-card>
    <el-dialog v-model="state.dialogFormVisible" :title="state.operationType == 'add' ? '添加' : '编辑'" :draggable="true">
      <el-form ref="ruleFormRef" :model="state.ruleForm" :rules="state.rules" label-width="120px" class="demo-ruleForm"
        status-icon>
        <el-form-item label="活动名称" prop="recharge_activity_name">
          <el-input v-model="state.ruleForm.recharge_activity_name" />
        </el-form-item>
        <el-form-item label="充值类型" prop="recharge_activity_type">
          <el-select v-model="state.ruleForm.recharge_activity_type" placeholder="" @change="clearAllDomain">
            <el-option v-for="(item, index) in state.type_list" :label="item.type_name" :value="item.type" />
          </el-select>
        </el-form-item>
        <el-form-item label="活动时间" prop="timeArr">
          <el-date-picker v-model="state.ruleForm.timeArr" type="daterange" range-separator="To"
            start-placeholder="Start date" end-placeholder="End date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="活动状态" prop="status">
          <el-select v-model="state.ruleForm.status" placeholder="">
            <el-option label="关闭" :value="0" />
            <el-option label="开启" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="打码倍率" prop="bet_rate">
          <el-input v-model="state.ruleForm.bet_rate" type="number" />
        </el-form-item>
        <el-form-item v-for="(domain, index) in  dynamicValidateForm.domains" :key="domain.id" style="margin-bottom: 0;"
          :label="index == 0 ? '设置充值阶梯' : ''" prop="" rules="">
          <table border=" 1px">
            <tr>
              <td>
                <div style="width: 60px;">充值金币:</div>
              </td>
              <td v-if="state.ruleForm.recharge_activity_type == 0 || state.ruleForm.recharge_activity_type == 2">
                <div style="display: flex;">
                  <el-input v-model="domain.min_recharge" type="number" placeholder="最小充值" />
                  <span> ~ </span>
                  <el-input v-model="domain.max_recharge" type="number" placeholder="最大充值" />
                </div>
              </td>
              <td v-if="state.ruleForm.recharge_activity_type == 1 || state.ruleForm.recharge_activity_type == 3">
                <el-select v-model="domain.recharge_amount" class="m-2" placeholder="选择充值金额">
                  <el-option v-for=" item  in  state.pay_money_list " :key="item" :label="item" :value="item" />
                </el-select>
              </td>
              <td>
                <div style="width: 60px;">赠送金币:</div>
              </td>
              <td>
                <div style="display: flex;"><el-input v-model="domain.send_rate" type="number"
                    placeholder="赠送比例" /><span>%</span></div>
              </td>
              <td>
                <el-button class="mt-2" @click.prevent="removeDomain(domain)">删除</el-button>
              </td>
            </tr>
          </table>
        </el-form-item>
        <el-form-item>
          <el-button @click="addDomain">新增阶梯</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleFormRef)">Create</el-button>
          <el-button @click="cancel">cancel</el-button>
          <!-- <el-button @click="resetForm(ruleFormRef)">Reset</el-button> -->
        </el-form-item>
      </el-form>
    </el-dialog>

    <!-- 领取记录 -->
    <claim-details v-if="state.dialogFormVisible2" :recharge_activity_id="state.recharge_activity_id"
      @showClaimDetails="showClaimDetails" />
  </div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import { recharge_activity_list_post, recharge_activity_type_list_post, add_recharge_activity_post, update_recharge_activity_post, delete_recharge_activity_post } from "@/api/platformManagement";
import { resetRouter } from "@/router";
import claimDetails from "./claimDetails.vue"
import popconfirm from "@/components/popconfirm/index.vue"
import pagination from "@/components/pagination/index.vue"
import datetime from "@/components/datetime/index.vue"
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  dialogFormVisible2: false,
  pay_money_list: [],
  type_list: [],
  timeArr: '',
  searchForm: {
    status: '',
    type: '',
    stime: '',
    etime: '',
    name: '',
  },
  pageForm: {
    page: 1,
    limit: 20,
    total: 0
  },
  tableData: [],
  ruleForm: {
    recharge_activity_name: '',// 活动名称
    recharge_activity_type: 0,// 活动类型
    start_time: '',// 起始日期
    over_time: '',// 结束日期
    timeArr: '', // 时间数组
    status: 1,// 活动状态
    bet_rate: 5,// 打码倍率
    ladder_list: '',// 充值阶梯
  },
  rules: {
    recharge_activity_name: [{ required: true, message: '', trigger: 'blur' },],
    recharge_activity_type: [{ required: true, message: '', trigger: 'blur' },],
    // start_time: [{ required: true, message: '', trigger: 'blur' },],
    // over_time: [{ required: true, message: '', trigger: 'blur' },],
    timeArr: [{ required: true, message: '', trigger: 'blur' },],
    status: [{ required: true, message: '', trigger: 'blur' },],
    bet_rate: [{ required: true, message: '', trigger: 'blur' },],
    ladder_list: [{ required: true, message: '', trigger: 'blur' },],
  },

  recharge_activity_id: 0,
})
const ruleFormRef = ref<FormInstance>()
const dynamicValidateForm = reactive<{
  domains: DomainItem[]
}>({
  domains: [
    {
      id: 1,
      min_recharge: null,
      max_recharge: null,
      recharge_amount: null,
      send_rate: null,
      send_amount: null,
      send_type: null
    },
  ],
})
interface DomainItem {
  id: number
  min_recharge: number
  max_recharge: number
  recharge_amount: number
  send_rate: number
  send_amount: number
  send_type: number
}

const addDomain = () => {
  dynamicValidateForm.domains.push({
    id: Date.now(),
    min_recharge: 0,
    max_recharge: 0,
    recharge_amount: 0,
    send_rate: 0,
    send_amount: 0,
    send_type: state.ruleForm.recharge_activity_type
  })
}

const clearAllDomain = () => {
  dynamicValidateForm.domains = []
  addDomain()
}

// 获取类型
recharge_activity_type_list_post({}).then(res => {
  state.pay_money_list = res.pay_money_list
  state.type_list = res.type_list
})

// 获取数据
const getData = async () => {
  state.loading = true
  const obj = {
    limit: state.pageForm.limit,
    page: state.pageForm.page,
    status: state.searchForm.status,
    type: state.searchForm.type,
    stime: state.timeArr ? state.timeArr[0] : '',
    etime: state.timeArr ? state.timeArr[1] : '',
    name: state.searchForm.name,
  }
  recharge_activity_list_post({ ...obj }).then(res => {
    state.pageForm.total = res.count
    state.tableData = res.data
    state.loading = false
  })
}
getData();// 获取数据

const timeChange = (time) => {
  state.timeArr = time
  getData()
}

// 搜索数据
const searchData = () => {
  getData();// 获取数据
}

const statusFormatter = (row) => {
  if (row.status == 0) return '禁用'
  else return '启用'
}

const recharge_activity_type_formatter = (row) => {
  if (row.recharge_activity_type == 0) return '单次充值赠送(范围阶梯)'
  else return '单次充值赠送(指定额度阶梯)'
}

const removeDomain = (item: DomainItem) => {
  const index = dynamicValidateForm.domains.indexOf(item)
  if (index !== -1) {
    dynamicValidateForm.domains.splice(index, 1)
  }
}

// 添加||编辑
const editRow = (type: string, row?: any) => {
  resetForm(ruleFormRef.value) // 重置表单
  if (type == 'add') {
    state.operationType = 'add'
    clearAllDomain()
  }
  else {
    state.operationType = 'edit'
    state.ruleForm = { ...row }
    state.ruleForm.timeArr = [state.ruleForm.start_time, state.ruleForm.over_time] as any
    dynamicValidateForm.domains = [...state.ruleForm.ladder_list] as any
  }
  state.dialogFormVisible = true
}

// 显示领取记录
const showClaimDetails = (val, recharge_activity_id?: number) => {
  state.dialogFormVisible2 = val
  if (recharge_activity_id) state.recharge_activity_id = recharge_activity_id
}

// 删除
const deleteRow = async (id: number) => {
  delete_recharge_activity_post({ recharge_activity_id: id }).then(res => {
    if (res.code == 1) getData();// 获取数据
  })
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
      let requestApi = null;
      if (state.operationType == 'add') requestApi = add_recharge_activity_post
      else requestApi = update_recharge_activity_post
      state.ruleForm.start_time = state.ruleForm.timeArr ? state.ruleForm.timeArr[0] : ''
      state.ruleForm.over_time = state.ruleForm.timeArr ? state.ruleForm.timeArr[1] : ''
      state.ruleForm.ladder_list = JSON.stringify(dynamicValidateForm.domains)
      requestApi({ ...state.ruleForm }).then(res => {
        if (res.code == 1) {
          getData();// 获取数据
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

<style lang="scss" scoped>
table {
  border-collapse: collapse;
  border-color: #f5f5f5;

  tr {
    td {
      padding: 10px;
    }
  }
}
</style>

