<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-button type="primary" @click="editRow('add')">添加游戏类型</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="id" label="id" header-align="center" :align="'center'" />
        <el-table-column prop="type_name" label="类型名称" header-align="center" :align="'center'" />
        <el-table-column prop="type" label="类型值" header-align="center" :align="'center'" />
        <!-- <el-table-column prop="icon_url" label="图标" header-align="center" :align="'center'">
          <template #default="scope">
            <el-image :src="`${store.imgUrl}${scope.row.icon_url}`" :zoom-rate="1.2"
              :preview-src-list="[`${store.imgUrl}${scope.row.icon_url}`]" :initial-index="4" fit="cover"
              preview-teleported />
          </template>
        </el-table-column> -->
        <el-table-column prop="sort_index" label="排序" header-align="center" :align="'center'" />
        <el-table-column prop="rakeback_open" label="打码反水" header-align="center" :align="'center'"
          :formatter="rakeback_open_Formatter" />
        <el-table-column prop="status" label="开启状态" header-align="center" :align="'center'"
          :formatter="statusFormatter" />
        <el-table-column prop="jump_route" label="路由跳转" header-align="center" :align="'center'" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="warning" @click="setStatus(scope.row)">{{ scope.row.status == 1 ? "关闭" : "开启"
            }}</el-button>
            <el-button type="danger" @click="deleteRow(scope.row)">删除</el-button>
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
        <el-form-item label="类型名称" prop="type_name">
          <el-input v-model="state.ruleForm.type_name" />
        </el-form-item>
        <!-- <el-form-item label="图片icon" prop="icon">
          <img-upload :img="state.ruleForm.icon ? `${store.imgUrl}${state.ruleForm.icon}` : ''"
            @getImgData="get_icon_url" />
        </el-form-item> -->
        <el-form-item label="类型值" prop="type">
          <el-input v-model="state.ruleForm.type" />
        </el-form-item>
        <el-form-item label="是否开启返水" prop="rakeback_open">
          <el-select v-model="state.ruleForm.rakeback_open" placeholder="所有分类" size="large" clearable>
            <el-option v-for="item in state.gameType_list" :key="item.label" :label="item.label" :value="item.val" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="state.ruleForm.status" placeholder="所有分类" size="large" clearable>
            <el-option v-for="item in state.status_list" :key="item.label" :label="item.label" :value="item.val" />
          </el-select>
        </el-form-item>
        <el-form-item label="跳转路由" prop="jump_route">
          <el-input v-model="state.ruleForm.jump_route" />
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
import { game_type_list_post, add_game_type_post, update_game_type_post, update_game_type_status_post, delete_game_type_post } from '@/api/gameManagement'
import pagination from "@/components/pagination/index.vue"
import confStore from "@/store/modules/conf";
import imgUpload from "@/components/imgUpload/index.vue"
const store = confStore();
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  options: [],
  timeArr: '',
  pageForm: {
    page: 1,
    limit: 20,
    total: 0
  },
  ruleForm: {
    type_name: "",//类型名称
    type: "",//类型值
    icon: "",//图标
    rakeback_open: "",//是否开启反水
    status: "",//状态
    sort_index: "",//排序
    jump_route: "",//跳转路由
  },
  rules: {
    type_name: [{ required: true, message: '', trigger: 'blur' },],
    type: [{ required: true, message: '', trigger: 'blur' },],
    icon: [{ required: true, message: '请上传图片', trigger: 'blur' },],
    rakeback_open: [{ required: true, message: '', trigger: 'blur' },],
    status: [{ required: true, message: '', trigger: 'blur' },],
    sort_index: [{ required: true, message: '', trigger: 'blur' },],
    jump_route: [{ required: true, message: '', trigger: 'blur' },],
  },
  gameType_list: [
    { val: 0, label: "关闭" },
    { val: 1, label: "开启" }
  ],
  status_list: [
    { val: 0, label: '关闭' },
    { val: 1, label: '开启' }
  ],
  tableData: [],
})
const ruleFormRef = ref<FormInstance>()

// const get_icon_url = (val: string) => {
//   state.ruleForm.icon = val
// }
const rakeback_open_Formatter = (row) => {
  if (row.rakeback_open == 0) return '关闭'
  else return '开启'
}
const statusFormatter = (row) => {
  if (row.status == 0) return '关闭'
  else return '开启'
}

// 获取数据
const getData = async () => {
  state.loading = true
  game_type_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res["count"]
    state.tableData = res["data"]
  }).finally(() => {
    state.loading = false
  })
}

getData()

// 添加||编辑
const editRow = (type: string, data?) => {
  if (type == 'add') state.operationType = 'add'
  else state.operationType = 'edit'

  resetForm(ruleFormRef.value) // 重置表单
  if (data) {
    state.ruleForm = data
  }
  state.dialogFormVisible = true
}
// 设置状态
const setStatus = (row) => {
  update_game_type_status_post({ id: row.id, status: row.status == 1 ? 0 : 1 }).then(res => {
    if (res['code'] == 1) getData();// 获取数据
  })
}
// 删除
const deleteRow = (row) => {
  delete_game_type_post({ id: row.id }).then(res => {
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
      let requestApi = null;
      state.ruleForm.icon = 'game_type/1681360201440g9bx9.png'
      if (state.operationType == 'add') requestApi = add_game_type_post
      else requestApi = update_game_type_post
      // -------
      let data = new FormData();
      for (var i in state.ruleForm) {
        data.append(i, state.ruleForm[i]);
      }
      // -------
      requestApi(data).then(res => {
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

