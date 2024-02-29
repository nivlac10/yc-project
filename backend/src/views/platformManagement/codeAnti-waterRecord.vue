<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">

      <el-button type="primary" @click="editRow('add')">添加打码反水奖励</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%; height: 100%;">
        <el-table-column prop="id" label="ID" header-align="center" :align="'center'" />
        <el-table-column prop="money" label="奖金" header-align="center" :align="'center'" />
        <el-table-column prop="need_code_amount" label="所需打码量" header-align="center" :align="'center'" />
        <el-table-column prop="status" label="状态" header-align="center" :align="'center'" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="warning" @click="updataStatus(scope.row.id, scope.row.status)">{{ scope.row.status == '启用' ?
              '禁用' : '启用' }}</el-button>
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
        <el-form-item label="奖金" prop="money">
          <el-input v-model="state.ruleForm.money" />
        </el-form-item>
        <el-form-item label="打码量" prop="need_code_amount">
          <el-input v-model="state.ruleForm.need_code_amount" />
        </el-form-item>
        <el-form-item label="状态" prop="status" v-show="state.operationType == 'edit'">
          <el-input v-model="state.ruleForm.status" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleFormRef)">确定</el-button>
          <el-button @click="cancel">取消</el-button>
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
import { bet_task_list_post, add_bet_task_post, update_bet_task_post, update_bet_task_status_post } from "../../api/platformManagement";
import pagination from "@/components/pagination/index.vue"
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

  },
  currentData: {},
  tableData: [],
  ruleForm: {
    money: '',
    need_code_amount: '',
    status: '',
  },
  rules: {
    name: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
  gameTypeList: [],
})
const ruleFormRef = ref<FormInstance>()


// 获取数据
const getData = async () => {
  state.loading = true
  bet_task_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res.count;
    state.tableData = res.data;
    state.loading = false;
    //状态别名
    state.tableData.map((v, i) => {
      state.tableData[i]['status'] = v.status == 1 ? '启用' : '禁用';
    })
  })
}

getData();
// 添加||编辑
const editRow = (type: string, data?: any) => {
  resetForm(ruleFormRef.value) // 重置表单
  if (type == 'add') state.operationType = 'add';
  else {
    state.ruleForm = data;
    state.operationType = 'edit';
  }

  state.dialogFormVisible = true
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
      let api;

      if (state.operationType == 'add') api = add_bet_task_post;
      else api = update_bet_task_post;

      if (state.ruleForm.status == '启用') {
        //@ts-ignore
        state.ruleForm.status = 1;
      } else {
        //@ts-ignore
        state.ruleForm.status = 0;
      }

      api({ ...state.ruleForm }).then((res: any) => {
        console.log(res);
        refreshData(res.code);

      })

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

//修改状态
const updataStatus = async (id, status) => {
  if (status == '启用') {
    //@ts-ignore
    status = 0;
  } else {
    status = 1;
  }
  let data = await update_bet_task_status_post({ id, status })
  refreshData(data.code);
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

