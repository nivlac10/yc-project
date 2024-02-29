<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-select v-model="state.searchForm.pay_id" class="m-2" placeholder="所有渠道" clearable>
        <el-option v-for="item in state.pay_list" :key="item['pay_id']" :label="item['pay_name']"
          :value="item['pay_id']" />
      </el-select>
      <div>
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
        :summary-method="getSummaries">
        <el-table-column prop="day" label="日期" header-align="center" :align="'center'" />
        <el-table-column prop="pay_name" label="支付名称" header-align="center" :align="'center'" />
        <el-table-column prop="num" label="下单数" header-align="center" :align="'center'" />
        <el-table-column prop="order_ratio" label="下单成功" header-align="center" :align="'center'" />
        <el-table-column prop="res_ratio" label="支付成功" header-align="center" :align="'center'" />
        <el-table-column prop="money" label="成功金额" header-align="center" :align="'center'" />
        <!-- <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit')">编辑</el-button>
            <el-button type="warning" @click="editRow('edit')">禁用</el-button>
            <el-button type="danger" @click="deleteRow(scope.row.cid)">删除</el-button>
          </template>
        </el-table-column> -->
      </el-table>
    </el-card>
    <el-card uno-margin-top>
      <div class="pager-wrapper">
        <el-pagination background :page-sizes="paginationData.pageSizes" :total="paginationData.total"
          :page-size="paginationData.pageSize" :currentPage="paginationData.currentPage" @size-change="handleSizeChange"
          @current-change="handleCurrentChange" />
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
import { pay_day_data_post } from "../../api/paymentManagement";
import datetime from "@/components/datetime/index.vue"
import { pay_list_post } from "../../api/paymentManagement";
const router = useRouter();
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination() // 分页
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  pay_list: [], // 渠道列表
  timeArr: '',
  searchForm: {
    page: paginationData.currentPage,
    limit: paginationData.pageSize,
    stime: '',// 起始日期
    etime: '',// 结束日期
    pay_id: '',// 支付
  },
  tableData: [],
  tableTotal: [],
  ruleForm: {
    name: '',
  },
  rules: {
    name: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
})
const ruleFormRef = ref<FormInstance>()

// 获取选择数据
const getSelectData = () => {
  //支付
  pay_list_post({ limit: 999, page: 1 }).then(res => {
    state.pay_list = res['data']
  })
}
getSelectData()// 获取选择数据


// 获取数据
const getData = async () => {
  state.loading = true
  state.searchForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.searchForm.etime = state.timeArr ? state.timeArr[1] : ''
  pay_day_data_post({ ...state.searchForm }).then(res => {
    paginationData.total = res.count;
    state.tableData = res.data;
    state.tableTotal = res.total;
    state.loading = false;
  })
}

const timeChange = (time) => {
  state.timeArr = time
  getData()
}

// 搜索数据
const searchData = () => {
  paginationData.currentPage = 1
  getData();// 获取数据
}

// 分页
watch(() => paginationData.currentPage, (val: number) => {
  getData();// 获取数据
}, { deep: true, immediate: true })

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


  (sums[2] as any) = state.tableTotal['num'];


  (sums[3] as any) = state.tableTotal['or_num'];


  (sums[4] as any) = state.tableTotal['res_num'];

  (sums[5] as any) = state.tableTotal['money'];



  // console.log(columns, data);
  return sums
}
</script>

<style lang="scss" scoped></style>

