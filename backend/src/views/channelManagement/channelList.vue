<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button type="primary" @click="editRow('add')">添加</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="cid" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="username" label="应用名称" header-align="center" :align="'center'" />
        <el-table-column prop="verify_str" label="审核模式" header-align="center" :align="'center'" />
        <el-table-column prop="pro_name" label="代理" header-align="center" :align="'center'" />
        <el-table-column prop="service_name" label="客服" header-align="center" :align="'center'" />
        <el-table-column prop="user_key" label="谷歌KEY" header-align="center" :align="'center'" />
        <el-table-column prop="is_apk_str" label="apk" header-align="center" :align="'center'" />
        <el-table-column prop="fb_access_token" label="FB回传Token" header-align="center" :align="'center'">
          <template #default="scope">
            <el-tooltip class="box-item" effect="dark" :content="scope.row.fb_access_token" placement="top">
              <div style="overflow: hidden; height: 40px;">
                {{ scope.row.fb_access_token }}
              </div>
            </el-tooltip>

          </template>

        </el-table-column>
        <el-table-column prop="fb_pixel_id" label="FB回传PixId" header-align="center" :align="'center'" />
        <el-table-column prop="re_ratio" label="回传概率(1=100%)" header-align="center" :align="'center'" />
        <el-table-column prop="add_time" label="添加时间" header-align="center" :align="'center'" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="250">
          <template #default="scope">
            <div style="display: flex; align-items: center;gap: 10px; flex-wrap: wrap;justify-content: center;">
              <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
              <el-button type="warning" @click="disableRow(scope.row)">{{ scope.row.status == 0 ? '开启' : '禁用'
              }}</el-button>
              <div v-permission="['1']">
                <popconfirm @confirmClick="deleteRow(scope.row.cid)" />
              </div>
              <el-button type="success" @click="testBackhaul(scope.row.cid)">测试回传</el-button>
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
        <el-form-item label="渠道名称" prop="username">
          <el-input v-model="state.ruleForm.username" />
        </el-form-item>
        <el-form-item label="审核模式" prop="verify_flag">
          <el-select v-model="state.ruleForm.verify_flag">
            <el-option label="否" :value="0" />
            <el-option label="是" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否下载apk" prop="is_apk">
          <el-select v-model="state.ruleForm.is_apk">
            <el-option label="否" :value="0" />
            <el-option label="是" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="FB Pixle ID" prop="fb_pixel_id">
          <el-input v-model="state.ruleForm.fb_pixel_id" placeholder="请输入FB Pixle ID" />
        </el-form-item>
        <el-form-item label="FB Token" prop="fb_access_token">
          <el-input v-model="state.ruleForm.fb_access_token" placeholder="请输入FB Token" />
        </el-form-item>
        <el-form-item label="上报概率" prop="re_ratio">
          (1=100%)
          <el-input v-model="state.ruleForm.re_ratio" placeholder="请输入上报概率" />
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
import { add_agent_post, agent_list_post, delete_agent_post, update_agent_post, update_agent_statue_post, test_backhaul_post } from "@/api/channelManagement/index"

const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  pageForm: {
    page: 1,
    limit: 20,
    total: 0
  },
  tableData: [],
  ruleForm: {
    username: '',
    verify_flag: 0,
    aid: 1,
    is_apk: 0,
    re_ratio: 0.7,
    fb_access_token: "",
    fb_pixel_id: ""
  },
  rules: {
    username: [{ required: true, message: '', trigger: 'blur' },],
    verify_flag: [{ required: true, message: '', trigger: 'blur' },],
  }
})
const ruleFormRef = ref<FormInstance>()

// 获取数据
const getData = async () => {
  state.loading = true
  agent_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res['count']
    state.tableData = res['data']
    state.loading = false
  })
}
getData();// 获取数据

const testBackhaul = async (cid) => {
  test_backhaul_post({ cid }).then(res => {

  })
  // }
}

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
// 禁用
const disableRow = (row: any) => {
  update_agent_statue_post({ cid: row.cid, status: row.status == 1 ? 0 : 1 }).then(res => {
    if (res['code'] == 1) getData();// 获取数据
  })
}
// 删除
const deleteRow = async (cid: number) => {
  delete_agent_post({ cid: cid }).then(res => {
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
  await formEl.validate((valid, fields) => {
    if (valid) {
      let requestApi;
      if (state.operationType == 'add') requestApi = add_agent_post({ ...state.ruleForm })
      else requestApi = update_agent_post({ ...state.ruleForm })
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

