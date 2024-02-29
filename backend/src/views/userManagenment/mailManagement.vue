<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-input v-model="state.searchForm.uid" placeholder="请输入用户名或uid" style="width: 200px;" clearable />

      <el-select v-model="state.searchForm.receive_status" class="m-2" placeholder="领取状态" clearable>
        <el-option v-for="item in state.receive_status_list" :key="item['label']" :label="item['value']"
          :value="item['label']" />
      </el-select>
      <div>
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">

        <el-table-column prop="uid" label="UID" header-align="center" :align="'center'" fixed="left" width="180">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" header-align="center" :align="'center'" />
        <el-table-column prop="content" label="内容" header-align="center" :align="'center'" />
        <el-table-column prop="money" label="金额" header-align="center" :align="'center'" />
        <el-table-column prop="remain_money" label="打码金额" header-align="center" :align="'center'" />
        <el-table-column prop="receive_status" label="可领取状态" header-align="center" :align="'center'" />
        <el-table-column prop="add_time" label="添加时间" header-align="center" :align="'center'" />
      </el-table>
    </el-card>

    <el-card uno-margin-top>
      <div class="pager-wrapper">
        <pagination :pageForm="state.searchForm" @def="getData" />
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
import { usePagination } from "@/hooks/usePagination"
import { email_list_post } from "../../api/userManagenment";
import pagination from "@/components/pagination/index.vue"
import datetime from "@/components/datetime/index.vue"
import { goToUserInfo } from "@/utils/baseFun"

const router = useRouter();
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination() // 分页
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  timeArr: '',
  searchForm: {
    page: 1,
    limit: 20,
    total: 0,
    stime: '',// 起始日期
    etime: '',// 结束日期
    uid: '',// 渠道
    receive_status: '',//领取状态
  },
  receive_status_list: [
    { label: '', value: '领取状态' },
    { label: '0', value: '无' },
    { label: '1', value: '未领取' },
    { label: '2', value: '已领取' }
  ], // 领取状态列表
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


const timeChange = (time) => {
  state.timeArr = time
  getData()
}


// 获取数据
const getData = async () => {
  state.loading = true
  state.searchForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.searchForm.etime = state.timeArr ? state.timeArr[1] : ''
  email_list_post({ ...state.searchForm }).then(res => {
    state.searchForm.total = res["count"]
    state.tableData = res["data"]
  }).finally(() => {
    state.loading = false
  })
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

