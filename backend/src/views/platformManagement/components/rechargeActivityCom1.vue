<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- <el-select v-model="state.searchForm.status" class="m-2" placeholder="状态">
        <el-option label="全部" value="" />
        <el-option v-for="item in state.options" :key="item['id']" :label="item['username']" :value="item['username']" />
      </el-select>
      <el-button type="primary" @click="editRow('add')">搜索</el-button> -->
      <el-button type="primary" @click="editRow('add')">新增活动简介</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="id" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="info" label="简介内容" header-align="center" :align="'center'">
          <template #default="scope">
            <el-tooltip class="box-item" effect="dark" :content="scope.row.info" placement="top-start">
              <div class="text_hiding">
                {{ scope.row.info }}
              </div>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="sort_index" label="排序" header-align="center" :align="'center'" sortable />
        <el-table-column prop="add_time" label="时间" header-align="center" :align="'center'" sortable />
        <el-table-column prop="name" label="状态" header-align="center" :align="'center'" :formatter="statusFormatter" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="warning" @click="setStatus(scope.row)">{{ scope.row.status == 1 ? '禁用' : '开启' }}</el-button>
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
        <el-form-item label="内容" prop="info">
          <el-input v-model="state.ruleForm.info" :autosize="{ minRows: 4, maxRows: 8 }" type="textarea" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_index">
          <el-input v-model="state.ruleForm.sort_index" type="number" />
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
import { add_slogan_post, delete_slogan_post, recharge_activity_slogan_post, update_slogan_post, update_slogan_status_post } from "@/api/platformManagement";
import popconfirm from "@/components/popconfirm/index.vue"
import pagination from "@/components/pagination/index.vue"

const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  options: [],
  searchForm: {
    status: ''
  },
  pageForm: {
    page: 1,
    limit: 20,
    total: 0
  },
  tableData: [],
  ruleForm: {
    info: '',
    sort_index: ''
  },
  rules: {
    info: [
      { required: true, message: '', trigger: 'blur' },
    ],
    sort_index: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
})
const ruleFormRef = ref<FormInstance>()

const statusFormatter = (row) => {
  if (row.status == 0) return '禁用'
  else return '开启'
}

// 获取数据
const getData = async () => {
  state.loading = true
  recharge_activity_slogan_post({ ...state.pageForm }).then(res => {
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

// 设置状态
const setStatus = (row) => {
  update_slogan_status_post({ id: row.id, status: row.status == 1 ? 0 : 1 }).then(res => {
    if (res.code == 1) getData();// 获取数据
  })
}

// 删除
const deleteRow = async (id: number) => {
  delete_slogan_post({ id: id }).then(res => {
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
      if (state.operationType == 'add') requestApi = add_slogan_post
      else requestApi = update_slogan_post
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

