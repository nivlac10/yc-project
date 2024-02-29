<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <div>
        <datetime @def="timeChange" />
      </div>
      <div style="width: 100%;">
        <el-input v-model="state.pageForm.uid" placeholder="请输入用户名或uid" style="width: 200px;" clearable />
        <el-select v-model="state.pageForm.continue_day" class="m-2" placeholder="连续签到天数" clearable>
          <el-option v-for="item in state.continue_day_list" :key="item" :label="item['label']" :value="item['value']" />
        </el-select>
        <el-button type="primary" @click="searchData">搜索</el-button>
      </div>
    </el-card>

    <!-- 反水打码日志 -->
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%;" show-summary
        :summary-method="getSummaries">
        <el-table-column prop="uid" label="用户" header-align="center" :align="'center'" fixed="left" width="180">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
          </template>

        </el-table-column>
        <!-- <el-table-column prop="task_id" label="task_id" header-align="center" :align="'center'" /> -->
        <el-table-column prop="add_time" label="领取时间" header-align="center" :align="'center'" />
        <el-table-column prop="money" label="领取金额" header-align="center" :align="'center'" />
        <el-table-column prop="continue_day" label="连续签到天数" header-align="center" :align="'center'" />
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
        <el-form-item label="Activity name" prop="name">
          <el-input v-model="state.ruleForm.name" />
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
import { user_sign_list_post } from "../../api/logrecordManagement";
import datetime from "@/components/datetime/index.vue"
import pagination from "@/components/pagination/index.vue"
import { goToUserInfo } from "@/utils/baseFun"
const router = useRouter();

const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  agent_list: [], // 渠道列表
  timeArr: '',
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    stime: '',// 起始日期
    etime: '',// 结束日期
    uid: '',
    task_id: '',
    continue_day: null
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
  count_money: '',
  gameTypeList: [],
  continue_day_list: []
})
const ruleFormRef = ref<FormInstance>()

// 获取选择数据
const getSelectData = () => {
  for (let i = 1; i <= 30; i++) {
    state.continue_day_list.push({ label: i, value: i })
  }
  // 渠道
  // agent_list_post({ limit: 999, page: 1 }).then((res: any) => {
  //   state.agent_list = res.data
  // })
}
getSelectData()// 获取选择数据


// 获取数据
const getData = async () => {
  state.loading = true
  state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
  user_sign_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res.count
    state.count_money = res.count_money
    state.tableData = res.data
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
const getSummaries = (param) => {
  const { columns, data } = param;
  const sums = [];


  (sums[0] as any) = '合计';
  (sums[2] as any) = state.count_money;
  return sums
}
</script>

<style lang="scss" scoped></style>

