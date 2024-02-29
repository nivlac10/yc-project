<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button type="primary" @click="editRow('add')">添加</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%"  height="100%">
        <el-table-column prop="id" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="username" label="用户名" header-align="center" :align="'center'" />
        <el-table-column prop="userinfo" label="备注" header-align="center" :align="'center'" />
        <el-table-column prop="user_key" label="谷歌密钥" header-align="center" :align="'center'" width="360">
          <template #default="scope">
            <el-button type="primary" @click="copy(scope.row.user_key)">{{ scope.row.user_key }}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="loginnum" label="登陆次数" header-align="center" :align="'center'" />
        <el-table-column prop="logintime" label="最后登陆时间" header-align="center" :align="'center'" sortable />
        <el-table-column prop="loginip" label="最近登陆IP" header-align="center" :align="'center'" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="400">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="success" @click="editRow('reset', scope.row)">重置密钥</el-button>
            <el-button type="warning" @click="disableRow(scope.row)">{{ scope.row.status == 1 ? '禁用' : '开启' }}</el-button>
            <popconfirm @confirmClick="deleteRow(scope.row.id)" />
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
        <el-form-item label="角色" prop="admintype" v-if="state.operationType == 'add'">
          <el-select v-model="state.ruleForm.admintype" placeholder="">
            <el-option :label="item.label" :value="item.val" v-for="(item, index) in state.typeList" :key="item.label" />
          </el-select>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="state.ruleForm.username" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="state.operationType == 'add'">
          <el-input v-model="state.ruleForm.password" />
        </el-form-item>
        <el-form-item label="备注" prop="userinfo">
          <el-input v-model="state.ruleForm.userinfo" />
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
import { admin_list_post, add_admin_post, delete_admin_one, update_admin_post, update_admin_statue_post, reset_admin_secret } from "@/api/SystemManagement/user";
import popconfirm from "@/components/popconfirm/index.vue"
import { copy } from "@/utils/baseFun"
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  tableData: [],
  ruleForm: {
    username: '',
    password: '',
    admintype: '',
    userinfo: '',
  },
  pageForm: {
    page: 1,
    limit: 20,
    total: 0
  },
  typeList: [
    { val: 2, label: '管理员' },
    { val: 3, label: '运营' },
    { val: 4, label: '财务' },
    { val: 5, label: '德州用户' },
  ],
  rules: {
    username: [
      { required: true, message: '', trigger: 'blur' },
    ],
    password: [
      { required: true, message: '', trigger: 'blur' },
    ],
    admintype: [
      { required: true, message: '', trigger: 'blur' },
    ],
    userinfo: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
})
const ruleFormRef = ref<FormInstance>()

// 获取数据
const getData = async () => {
  state.loading = true
  // paginationData.total = res.data.total
  admin_list_post({ ...state.pageForm }).then(res => {
    state.tableData = res.data
  })
  state.loading = false
}
getData();// 获取数据

// 添加||编辑
const editRow = (type: string, row?: any) => {
  if (type == 'add') {
    state.operationType = 'add'
    state.ruleForm = {} as any
    state.dialogFormVisible = true
  } else if (type == 'reset') {
    reset_admin_secret({ uid: row.id }).then((res) => {
      if (res.code == 1) {
        getData()
      }

    })
  }
  else if (type == 'edit') {
    state.operationType = 'edit'
    state.ruleForm = row
    state.dialogFormVisible = true
  }
  resetForm(ruleFormRef.value) // 重置表单
}
// 禁用
const disableRow = (row: any) => {
  update_admin_statue_post({ uid: row.id, status: row.status == 1 ? 0 : 1 }).then(res => {
    if (res.code == 1) {
      getData()
    };// 获取数据
  })
}
// 删除
const deleteRow = (uid: number) => {
  delete_admin_one({ uid: uid }).then(res => {
    if (res.code == 1) {
      getData()
    };// 获取数据
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
      let requestApi;
      if (state.operationType == 'add') requestApi = add_admin_post({ ...state.ruleForm })
      else requestApi = add_admin_post({ ...state.ruleForm })
      requestApi.then(res => {
        if (res.code == 1) {
          getData();
        }// 获取数据
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

