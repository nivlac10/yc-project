<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button type="primary" @click="editRow('add')">添加</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="aid" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="username" label="登陆账号" header-align="center" :align="'center'" />
        <el-table-column prop="nickname" label="昵称" header-align="center" :align="'center'" />
        <el-table-column prop="user_key" label="谷歌密钥" header-align="center" :align="'center'" />
        <el-table-column prop="add_time" label="添加时间" header-align="center" :align="'center'" sortable />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230px">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="warning" @click="setStatus(scope.row)">{{ scope.row.status == 0 ? '开启' : '禁用'
            }}</el-button>
            <div v-permission="['1']">

              <popconfirm @confirmClick="deleteRow(scope.row.aid)" />
            </div>
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
        <el-form-item label="代理人账号" prop="username">
          <el-input v-model="state.ruleForm.username" :disabled="state.operationType == 'edit'" />
        </el-form-item>
        <el-form-item label="合伙人昵称" prop="nickname">
          <el-input v-model="state.ruleForm.nickname" />
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
import { add_proxy_post, delete_proxy_post, proxy_list_post, update_proxy_list_post, proxy_detail_post } from "@/api/channelManagement";

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
    username: '',
    nickname: '',
    aid: ''
  },
  rules: {
    username: [{ required: true, message: '', trigger: 'blur' },],
    nickname: [{ required: true, message: '', trigger: 'blur' },],
  },
})
const ruleFormRef = ref<FormInstance>()

// 获取数据
const getData = async () => {
  state.loading = true
  proxy_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res['count']
    state.tableData = res['data']
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

// 设置状态
const setStatus = (row) => {
  update_proxy_list_post({ aid: row.aid, status: row.status == 1 ? 0 : 1 }).then(res => {
    if (res['code'] == 1) getData();// 获取数据
  })
}

// 删除
const deleteRow = async (aid: number) => {
  delete_proxy_post({ aid: aid }).then(res => {
    if (res['code'] == 1) getData();// 获取数据
  })
}

// 取消
const cancel = () => {
  state.dialogFormVisible = false
}

// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  console.log(state.ruleForm)
  await formEl.validate((valid, fields) => {
    if (valid) {
      let requestApi;
      if (state.operationType == 'add') requestApi = add_proxy_post({ ...state.ruleForm })
      else requestApi = proxy_detail_post({ ...state.ruleForm })
      requestApi.then(res => {
        if (res.code == 1) getData();// 获取数据
        state.dialogFormVisible = false
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

