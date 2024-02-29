<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
    <el-input v-model="state.pageForm.uid" placeholder="请输入用户名或uid" style="width: 200px;" clearable />
    <el-input v-model="state.pageForm.task_id" placeholder="请输入task_id" style="width: 200px;" clearable />
      <div>
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>

    <!-- 反水打码日志 -->
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%; height: 40vh;">
        <el-table-column prop="uid" label="uid" header-align="center" :align="'center'" />
        <el-table-column prop="task_id" label="task_id" header-align="center" :align="'center'" />
        <el-table-column prop="nickname" label="用户名" header-align="center" :align="'center'" />
        <el-table-column prop="bet" label="打码量" header-align="center" :align="'center'" />
        <el-table-column prop="add_time" label="领取时间" header-align="center" :align="'center'" />
        <el-table-column prop="money" label="领取金额" header-align="center" :align="'center'" />
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
import {  bet_task_log_list_post } from "../../../api/platformManagement";
import datetime from "@/components/datetime/index.vue"

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
    uid:'',
    task_id:'',
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
  gameTypeList: [],
})
const ruleFormRef = ref<FormInstance>()

// 获取选择数据
const getSelectData = () => {
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
  bet_task_log_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res.count
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
</script>

<style lang="scss" scoped></style>

