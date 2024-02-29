<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button type="primary" @click="editRow('add')">新增兑换码</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="code_id" label="code_id" header-align="center" :align="'center'" sortable width="110" />
        <el-table-column prop="code_name" label="名称" header-align="center" :align="'center'" width="110" />
        <el-table-column prop="code" label="兑换码" header-align="center" :align="'center'" width="110" />
        <el-table-column prop="code_url" label="领取链接" header-align="center" :align="'center'" width="140" />

        <el-table-column prop="code_num" label="兑换码数量" header-align="center" :align="'center'" width="110" />
        <el-table-column prop="receive_num" label="领取数量" header-align="center" :align="'center'" width="110" />
        <el-table-column prop="min_money" label="最小随机金额" header-align="center" :align="'center'" width="110" />
        <el-table-column prop="max_money" label="最大随机金额" header-align="center" :align="'center'" width="110" />
        <el-table-column prop="fixed_money" label="固定金额" header-align="center" :align="'center'" width="110" />
        <el-table-column prop="recharge_str" label="是否需要充值" header-align="center" :align="'center'" width="110" />
        <el-table-column prop="random_str" label="是否使用随机金额" header-align="center" :align="'center'" width="110" />
        <el-table-column prop="status" label="状态" header-align="center" :align="'center'" width="110" />
        <el-table-column prop="end_time" label="过期时间" header-align="center" :align="'center'" width="105" />
        <el-table-column prop="add_time" label="添加时间" header-align="center" :align="'center'" width="105" />

        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="240">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="warning" @click="setStatus(scope.row)">{{ scope.row.status == '禁用' ? '启用' : '禁用'
            }}</el-button>
            <el-button type="danger" @click="deleteRow(scope.row.code_id)">删除</el-button>
          </template>
        </el-table-column>
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
        <el-form-item label="名称" prop="code_name">
          <el-input v-model="state.ruleForm.code_name" />
        </el-form-item>
        <el-form-item label="code码数量" prop="code_num">
          <el-input v-model="state.ruleForm.code_num" />
        </el-form-item>
        <el-form-item label="是否需要充值" prop="is_recharge">
          <el-select v-model="state.ruleForm.is_recharge" class="m-2" placeholder="是否热门" clearable>
            <el-option v-for="item in state.recharge_statue" :label="item['label']" :value="item['val']" :key="item" />
          </el-select>
        </el-form-item>

        <el-form-item label="是否随机金额" prop="is_random">
          <el-select v-model="state.ruleForm.is_random" class="m-2" placeholder="是否热门" clearable>
            <el-option v-for="item in state.random_statue" :label="item['label']" :value="item['val']" :key="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="最小随机金额" prop="min_money">
          <el-input v-model="state.ruleForm.min_money" />
        </el-form-item>
        <el-form-item label="最大随机金额" prop="max_money">
          <el-input v-model="state.ruleForm.max_money" />
        </el-form-item>
        <el-form-item label="固定金额" prop="fixed_money">
          <el-input v-model="state.ruleForm.fixed_money" />
        </el-form-item>
        <el-form-item label="截至日期" prop="end_time">
          <el-date-picker v-model="state.ruleForm.end_time" type="date" placeholder="Pick a day"
            value-format="YYYY-MM-DD" />

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
import { dayjs, type FormInstance, type FormRules } from 'element-plus'
import { usePagination } from "@/hooks/usePagination"
import {
  give_code_post, detail_give_code_post, add_gift_post, update_give_code_status_post, delete_give_code_post
} from "@/api/platformManagement";
import store from "@/store";
import { formatDateTime } from "@/utils";


const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  jumpTargetList: [
    { val: 0, label: '无' },
    { val: 1, label: '窗口跳转' },
    { val: 2, label: '游戏' },
    { val: 3, label: '内部网页' },
    { val: 4, label: '外部网页' }
  ],
  tableData: [],
  ruleForm: {
    code_name: "",
    code_num: "",
    is_recharge: "",
    is_random: "",
    max_money: "",
    min_money: '',
    fixed_money: '',
    end_time: '',
  },
  rules: {
    code_name: [
      { required: true, message: '', trigger: 'blur' },
    ],
    code_num: [
      { required: true, message: '', trigger: 'blur' },
    ],
    is_recharge: [
      { required: true, message: '', trigger: 'blur' },
    ],
    is_random: [
      { required: true, message: '', trigger: 'blur' },
    ],
    max_money: [
      { required: true, message: '', trigger: 'blur' },
    ],
    min_money: [
      { required: true, message: '', trigger: 'blur' },
    ],
    fixed_money: [
      { required: true, message: '', trigger: 'blur' },
    ],
    end_time: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
  recharge_statue: [
    { val: 1, label: '需要' },
    { val: 0, label: '不需要' },
  ],

  random_statue: [
    { val: 1, label: '否' },
    { val: 0, label: '是' },
  ],
})
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination() // 分页
const ruleFormRef = ref<FormInstance>()

const typeFormatter = (row) => {
  if (row.type == 0) return '无'
  else if (row.type == 1) return '窗口跳转'
  else if (row.type == 2) return '游戏'
  else if (row.type == 3) return '内部网页'
  else if (row.type == 4) return '外部网页'
}

// 获取数据
const getData = async () => {
  // state.loading = true
  const obj = {
    limit: paginationData.pageSize,
    page: paginationData.currentPage
  }
  give_code_post({ ...obj }).then(res => {
    console.log(res);
    for (let i = 0; i < res.data.length; i++) {
      let e = res.data[i];
      e.code_url = `https://www.bigwin777.io/coupon?r=${e.code}`;
      e.recharge_str = dataAsName(e.is_recharge, 0, '不需要', '需要');
      e.random_str = e.is_random == 0 ? '是' : '否'
      e.status = dataAsName(e.status, 0, '禁用', '启用');
      e.end_time = formatDateTime(e.end_time);
    }
    paginationData.total = res.count
    state.tableData = res?.data
    state.loading = false
  })
}

/**
 *
 * @param e 原数据
 * @param condition 判断条件
 * @param name 为真时返回值
 * @param name2 为假时返回值
 */
function dataAsName(e, condition, name, name2) {
  if (e == condition) {
    return name;
  } else {
    return name2
  }
}
// 分页
watch(() => paginationData.currentPage, (val: number) => {
  getData();// 获取数据
}, { deep: true, immediate: true })

// 设置状态
const setStatus = (row) => {
  update_give_code_status_post({ code_id: row.code_id, status: row.status == '禁用' ? 1 : 0 }).then(res => {
    refreshData(res.code)
  })
}

// 添加||编辑
const editRow = (type: string, row?: any) => {
  resetForm(ruleFormRef.value) // 重置表单
  if (type == 'add') {

    state.operationType = 'add';
  } else {
    state.operationType = 'edit';
    row.status = row.status == '禁用' ? 1 : 0;
    console.log(row.status);

    state.ruleForm = { ...row }
  }
  state.dialogFormVisible = true
}
// 删除
const deleteRow = async (id: number) => {
  delete_give_code_post({ code_id: id }).then(res => {
    refreshData(res.code)
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
      state.ruleForm.end_time = dayjs(new Date(state.ruleForm.end_time)).format("YYYY-MM-DD");

      if (state.operationType == 'add') requestApi = add_gift_post
      else requestApi = detail_give_code_post
      requestApi({ ...state.ruleForm }).then(res => {
        refreshData(res.code)
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


//更新数据
const refreshData = (code: number) => {
  if (code == 1) {
    cancel();
    getData();
  }
}
</script>

<style lang="scss" scoped></style>

