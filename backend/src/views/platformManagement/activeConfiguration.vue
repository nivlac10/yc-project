<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button type="primary" @click="editRow('add')">添加</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="aid" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="info" label="活动内容" header-align="center" :align="'center'" width="200">
          <template #default="scope">
            <el-tooltip class="box-item" effect="dark" :content="scope.row.info" placement="top-start">
              <div class="text_hiding">
                {{ scope.row.info }}
              </div>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" header-align="center" :align="'center'" width="200" />
        <el-table-column prop="img_url" label="活动图片" header-align="center" :align="'center'" width="150">
          <template #default="scope">
            <el-image :src="scope.row.img_url" :zoom-rate="1.2" :preview-src-list="[scope.row.icon_url]"
              :initial-index="4" fit="cover" preview-teleported />
          </template>
        </el-table-column>
        <el-table-column prop="icon_url" label="图标icon" header-align="center" :align="'center'">
          <template #default="scope">
            <el-image :src="scope.row.icon_url" :zoom-rate="1.2" :preview-src-list="[scope.row.icon_url]"
              :initial-index="4" fit="cover" preview-teleported />
          </template>
        </el-table-column>
        <el-table-column prop="type" label="跳转目标" header-align="center" :align="'center'" :formatter="typeFormatter" />
        <el-table-column prop="url" label="1/支付弹窗/路由/网址" header-align="center" :align="'center'" />
        <el-table-column prop="button_name" label="按钮名称" header-align="center" :align="'center'" />
        <el-table-column prop="sort_index" label="排序" header-align="center" :align="'center'" sortable />
        <el-table-column prop="add_time" label="时间" header-align="center" :align="'center'" sortable width="100" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="warning" @click="setStatus(scope.row)">{{ scope.row.status == 0 ? '激活' : '禁用' }}</el-button>
            <popconfirm @confirmClick="deleteRow(scope.row.aid)" />
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-card uno-margin-top>
      <div class="pager-wrapper">
        <pagination :pageForm="state.pageForm" @def="getData" />
      </div>
    </el-card>
    <el-dialog v-model="state.dialogFormVisible" :title="state.operationType == 'add' ? '添加' : '编辑'" :draggable="true"
      destroy-on-close>
      <el-form ref="ruleFormRef" :model="state.ruleForm" :rules="state.rules" label-width="120px" class="demo-ruleForm"
        status-icon>
        <el-form-item label="标题" prop="title">
          <el-input v-model="state.ruleForm.title" />
        </el-form-item>
        <el-form-item label="内容" prop="info">
          <!-- <el-input v-model="state.ruleForm.info" :autosize="{ minRows: 4, maxRows: 8 }" type="textarea" /> -->
          <editorText @def="changeInfo" :info="state.ruleForm.info"></editorText>
        </el-form-item>
        <el-form-item label="活动图片" prop="img_url">
          <img-upload :img="state.ruleForm.img_url ? state.ruleForm.img_url : ''" @getImgData="get_img_url" />
        </el-form-item>
        <el-form-item label="图片icon" prop="icon_url">
          <img-upload :img="state.ruleForm.icon_url ? state.ruleForm.icon_url : ''" @getImgData="get_icon_url" />
        </el-form-item>
        <el-form-item label="按钮名称" prop="button_name">
          <el-input v-model="state.ruleForm.button_name" />
        </el-form-item>
        <el-form-item label="跳转目标" prop="type">
          <el-select v-model="state.ruleForm.type" class="m-2" placeholder="Select">
            <el-option v-for="item in state.jumpTargetList" :key="item.label" :label="item.label" :value="item.val" />
          </el-select>
        </el-form-item>
        <el-form-item label="跳转地址" prop="url">
          <el-input v-model="state.ruleForm.url" />
          <div>(窗口跳转 1 支付弹窗 或者路由 例如代理页面：/Refer)</div>
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
import pagination from "@/components/pagination/index.vue"
import popconfirm from "@/components/popconfirm/index.vue"
import { activity_list_post, activity_add_post, activity_update_post, activity_delete_post, activity_Disable_post } from "../../api/platformManagement";
import imgUpload from "@/components/imgUpload/index.vue"
import confStore from "@/store/modules/conf";
import editorText from "@/components/editorText/index.vue"
const store = confStore();
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
  jumpTargetList: [
    { val: 0, label: '无' },
    { val: 1, label: '窗口跳转' },
    { val: 2, label: '游戏' },
    { val: 3, label: '内部网页' },
    { val: 4, label: '外部网页' }
  ],
  ruleForm: {
    title: "", // 标题
    icon_url: "", // icon
    img_url: "", // 图片
    info: "", // 信息
    type: "", //  0无 1窗口跳转 2游戏 3内部网页 4外部网页
    url: "", // 窗口（1支付2代理）
    sort_index: "", // 排序
    button_name: '', // 按钮名称
  },
  rules: {
    title: [{ required: true, message: '', trigger: 'blur' },],
    icon_url: [{ required: true, message: '请上传图片', trigger: 'blur' },],
    img_url: [{ required: true, message: '请上传图片', trigger: 'blur' },],
    info: [{ required: true, message: '', trigger: 'blur' },],
    type: [{ required: true, message: '', trigger: 'blur' },],
    url: [{ required: true, message: '', trigger: 'blur' },],
    sort_index: [{ required: true, message: '', trigger: 'blur' },],
    button_name: [{ required: true, message: '', trigger: 'blur' },],
  },
  dropCol: [
    {
      label: "站号",
      prop: "stationNe",
      show: true
    },
    {
      label: "设备名称",
      prop: "lineNo",
      show: true
    },
    {
      label: "设备类型",
      prop: "businessType",
      show: true
    },
    {
      label: "子架-槽位-端口",
      prop: "port",
      show: true
    },
    {
      label: "告警名称",
      prop: "alarmNe",
      show: true
    },
    {
      label: "告警处理建议",
      prop: "advice",
      show: true
    },
    {
      label: "告警时间",
      prop: "aTime",
      show: true
    },
    {
      label: "清除时间",
      prop: "cTime",
      show: true
    },
    {
      label: "确认时间",
      prop: "nTime",
      show: true
    },
    {
      label: "确认人",
      prop: "verify",
      show: true
    },
    {
      label: "备注",
      prop: "remark",
      show: false
    }
  ]

})
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
  state.loading = true
  activity_list_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res.count
    state.tableData = res.data
    state.loading = false
  })
}
getData();// 获取数据

// 获取图片数据
const get_img_url = (val: string) => {
  state.ruleForm.img_url = val
}
const get_icon_url = (val: string) => {
  state.ruleForm.icon_url = val
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


// 设置状态
const setStatus = (row) => {
  activity_Disable_post({ aid: row.aid, status: row.status == 1 ? 0 : 1 }).then(res => {
    if (res.code == 1) getData();// 获取数据
  })
}

// 删除
const deleteRow = async (aid: number) => {
  activity_delete_post({ aid: aid }).then(res => {
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
      if (state.operationType == 'add') requestApi = activity_add_post
      else requestApi = activity_update_post
      // -------
      let data = new FormData();
      for (var i in state.ruleForm) {
        data.append(i, state.ruleForm[i]);
      }
      // -------
      console.log(data);

      requestApi(data).then(res => {
        if (res.code == 1) {
          state.ruleForm.img_url = ''
          state.ruleForm.icon_url = ''
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
const changeInfo = (res) => {
  state.ruleForm.info = res
  return state.ruleForm.info
}
</script>

<style lang="scss" scoped></style>

