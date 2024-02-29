<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button type="primary" @click="editRow('add')">添加集成商</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="id" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="名称" label="Name" header-align="center" :align="'center'" />
        <el-table-column prop="添加日期" label="时间" header-align="center" :align="'center'" sortable />
        <el-table-column prop="状态" label="状态" header-align="center" :align="'center'" sortable>
          <template #default="scope">
            {{ scope.row['状态'] == 1 ? "启用" : "禁用" }}
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editRow('edit', scope.row.id)">编辑</el-button>
            <el-button type="warning" size="small" @click="updataRow(scope.row.id, scope.row['状态'])">{{ scope.row['状态'] ==
              1 ? '禁用' : '启用' }}</el-button>
            <el-button type="danger" size="small" @click="deleteRow(scope.row.id)">删除</el-button>
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
        <el-form-item label="厂商名" prop="name">
          <el-input v-model="state.ruleForm.name" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleFormRef)">确定添加</el-button>
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
import { usePagination } from "@/hooks/usePagination"
import { factory_list_post, add_factory_post, delete_factory_post, update_factory_post, update_factory_status } from "@/api/IntegratorManagement/index"

const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  id: 0,
  tableData: [
    {
      cid: '1',
      date: '2016-05-02',
      name: '王小虎',
    },
  ],
  ruleForm: {
    name: '',
  },
  rules: {
    name: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
})
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination();// 分页

const ruleFormRef = ref<FormInstance>()



// 获取数据
const getData = async () => {
  state.loading = true
  let data = await factory_list_post({ page: paginationData.currentPage, limit: paginationData.pageSize });
  state.tableData = data['data'];
  paginationData.total = data['count']
  state.loading = false
}


//分页
watch(() => paginationData.currentPage, (val: number) => {
  getData();// 获取数据
}, { deep: true, immediate: true })

// 添加||编辑
const editRow = (type: string, id?: number) => {
  if (type == 'add') state.operationType = 'add'
  else state.operationType = 'edit'
  if (id) {
    state.id = id;
  }
  resetForm(ruleFormRef.value) // 重置表单
  state.dialogFormVisible = true
}
// 取消
const cancel = () => {
  state.dialogFormVisible = false
}
// 删除
const deleteRow = async (cid: number) => {
  let data = await delete_factory_post({ factory_id: cid });
  console.log(data);
  refreshData(data['code'])

}
// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      if (state.operationType == 'add') {
        add()
      } else {
        updata()
      }



    } else {
      console.log('error submit!', fields)
    }
  })
}

//添加
const add = async () => {
  let data = await add_factory_post({ factory_name: state.ruleForm.name });
  console.log(data);
  refreshData(data['code'])
}

//编辑
const updata = async () => {
  let data = await update_factory_post({ factory_name: state.ruleForm.name, factory_id: state.id });
  console.log(data);
  refreshData(data['code'])
}

//启用禁用表单
const updataRow = async (id, status) => {
  console.log(state);

  let data = await update_factory_status({ factory_id: id, status: status == 1 ? 0 : 1 });
  console.log(data);
  refreshData(data['code'])


}

//更新数据
const refreshData = (code: number) => {
  if (code == 1) {
    cancel();
    getData();
  }
}

// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>

<style lang="scss" scoped></style>

