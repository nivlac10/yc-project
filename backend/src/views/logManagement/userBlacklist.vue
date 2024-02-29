<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-input v-model="state.input" placeholder="请输入用户名或uid" style="width: 200px;" />
      <el-button type="primary" @click="searchData">搜索</el-button>
      <el-button type="primary" @click="editRow('add')">添加黑名单</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="id" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="uid" label="用户名" header-align="center" :align="'center'" width="180">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
          </template>

        </el-table-column>
        <el-table-column prop="info" label="备注" header-align="center" :align="'center'" />
        <el-table-column prop="type" label="类型" header-align="center" :align="'center'">
          <template #default="scope">
            {{ scope.row.type == 0 ? '个人' : '团队' }}
          </template>
        </el-table-column>
        <el-table-column prop="add_time" label="添加时间" header-align="center" :align="'center'" sortable />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230"
          v-permission="['1']">
          <template #default="scope">
            <el-button type="primary" @click="deleteRow(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-card uno-margin-top>
      <div class="pager-wrapper">
        <pagination :pageForm="state.pageForm" @def="getData"></pagination>
      </div>
    </el-card>
    <el-dialog v-model="state.dialogFormVisible" :title="state.operationType == 'add' ? '添加' : '编辑'" :draggable="true">
      <el-form ref="ruleFormRef" :model="state.ruleForm" :rules="state.rules" label-width="120px" class="demo-ruleForm"
        status-icon>
        <el-form-item label="用户" prop="uid">
          <el-input v-model="state.ruleForm.uid" placeholder="请输入用户uid" />
        </el-form-item>
        <el-form-item label="备注" prop="info">
          <el-input v-model="state.ruleForm.info" placeholder="请输入用户备注" />
        </el-form-item>
        <el-form-item label="黑名单类型" prop="type">
          <el-select v-model="state.ruleForm.type" class="m-2" placeholder="黑名单类型" clearable>
            <el-option v-for="item in state.type_list" :label="item.label" :value="item.val" />
          </el-select>
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
import { black_list_post, add_black_post, delete_unusual_user_post } from "../../api/logManagement";
import pagination from "@/components/pagination/index.vue"
import { goToUserInfo } from "@/utils/baseFun"
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  input: '',
  tableData: [],
  ruleForm: {
    uid: '',
    info: '',
    type: '',
    status: 0
  },
  pageForm: {
    page: 1,
    limit: 20,
    total: 0
  },
  rules: {
    uid: [
      { required: true, message: '', trigger: 'blur' },
    ],
    info: [
      { required: true, message: '', trigger: 'blur' },
    ],
    type: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
  type_list: [
    { val: 0, label: "个人" },
    { val: 1, label: "团队" }
  ]
})
const ruleFormRef = ref<FormInstance>()

// 获取数据
const getData = async () => {
  state.loading = true
  const obj = { username: state.input, limit: state.pageForm.limit, page: state.pageForm.page }
  black_list_post({ ...obj }).then(res => {
    state.pageForm.total = res.count
    state.tableData = res.data
    state.loading = false
    console.log(res);
  })
}
getData()
// 搜索数据
const searchData = () => {
  state.pageForm.page = 1
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
const deleteRow = async (id: number) => {
  delete_unusual_user_post({ id: id }).then(res => {
    getData()
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
      add_black_post({ ...state.ruleForm }).then(res => {
        if (res.code == 1) {
          state.pageForm.page = 1
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

