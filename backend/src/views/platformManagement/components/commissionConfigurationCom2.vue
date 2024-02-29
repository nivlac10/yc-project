<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button type="primary" @click="editRow('add')">添加</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="task_id" label="任务ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="task_name" label="任务名称" header-align="center" :align="'center'" />
        <el-table-column prop="num" label="邀请人数" header-align="center" :align="'center'" />
        <el-table-column prop="money" label="金额" header-align="center" :align="'center'" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <popconfirm @confirmClick="deleteRow(scope.row.task_id)" />
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
        <el-form-item label="任务名称" prop="task_name">
          <el-input v-model="state.ruleForm.task_name" />
        </el-form-item>
        <el-form-item label="邀请人数" prop="num">
          <el-input v-model="state.ruleForm.num" type="number" />
        </el-form-item>
        <el-form-item label="奖励金额" prop="money">
          <el-input v-model="state.ruleForm.money" type="number" />
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
import popconfirm from "@/components/popconfirm/index.vue"
import { add_invite_task_post, delete_invite_task_post, invite_task_list_post, update_invite_task_post } from "@/api/platformManagement";
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  tableData: [],
  pageForm: {
    page: 1,
    limit: 20,
    total: 0
  },
  ruleForm: {
    task_name: '',
    num: null,
    money: null
  },
  rules: {
    task_name: [{ required: true, message: '', trigger: 'blur' },],
    num: [{ required: true, message: '', trigger: 'blur' },],
    money: [{ required: true, message: '', trigger: 'blur' },],
  },
})
const ruleFormRef = ref<FormInstance>()

// 获取数据
const getData = async () => {
  state.loading = true
  invite_task_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res.count
    state.tableData = res.data
    state.loading = false
  })
}
getData();// 获取数据

// 添加||编辑
const editRow = (type: string, row?: any) => {
  resetForm(ruleFormRef.value) // 重置表单
  if (type == 'add') state.operationType = 'add'
  else {
    state.operationType = 'edit'
    state.ruleForm = { ...row }
  }
  state.dialogFormVisible = true
}
// 删除
const deleteRow = async (task_id: number) => {
  delete_invite_task_post({ task_id: task_id }).then(res => {
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
      if (state.operationType == 'add') requestApi = add_invite_task_post
      else requestApi = update_invite_task_post
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

<style lang="scss" scoped></style>

