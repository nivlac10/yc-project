<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button type="primary" @click="editRow('add', {})">添加</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="bid" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="img_url" label="轮播图" header-align="center" :align="'center'">
          <template #default="scope">

            <el-image :src="scope.row.img_url" :fit="'contain'" style="width: 50%;">
              <template #error>
                <div class="image-slot">
                  <el-icon><icon-picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="type_name" label="跳转类型" header-align="center" :align="'center'" sortable>
        </el-table-column>
        <el-table-column prop="url" label="1支付弹窗/路由/网址" header-align="center" :align="'center'" />
        <el-table-column prop="sort_index" label="排序" header-align="center" :align="'center'" sortable />
        <el-table-column prop="add_time" label="时间" header-align="center" :align="'center'" />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="warning" @click="updataRow(scope.row.bid, scope.row.status)">{{ scope.row.status ==
              1 ? '禁用' : '启用' }}</el-button>
            <el-button type="danger" @click="deleteRow(scope.row.bid)">删除</el-button>
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
        status-icon uno-padding-left-20>
        <el-form-item label="轮播图" prop="integratorName" v-show="state.operationType !== 'add'">

          <el-image :src="state.currentData['img_url']" :fit="'contain'" style="width: 25%;">
            <template #error>
              <div class="image-slot">
                <el-icon><icon-picture /></el-icon>
              </div>
            </template>
          </el-image>
        </el-form-item>
        <el-form-item :label="state.operationType !== 'add' ? '封面' : '轮播图'">
          <!-- @vue-ignore -->
          <el-upload v-model:file-list="state.ruleForm.fileList" class="upload-demo" :limit="1"
            :http-request="handleRequest">
            <el-button type="primary">Click to upload</el-button>
          </el-upload>
        </el-form-item>


        <el-form-item label="跳转类型">
          <el-select v-model="state.ruleForm.type" placeholder="所有分类" size="large" clearable @change="cahnge_select(v)">
            <el-option v-for="item in state.jumpTypeList" :key="item['value']" :label="item['label']"
              :value="item['value']" />
          </el-select>
        </el-form-item>

        <el-form-item label="排序">
          <el-input v-model="state.ruleForm.sort_index" />
        </el-form-item>
        <el-form-item label="跳转地址">
          (窗口跳转 1 支付弹窗 或者路由 例如代理页面：/Refer)
          <el-input v-model="state.ruleForm.url" />
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
import type { FormInstance, FormRules, UploadUserFile } from 'element-plus'
import { usePagination } from "@/hooks/usePagination"
import { banner_list_post, update_banner_status_post, delete_banner_post, detail_banner_post, add_banner_post } from "@/api/platformManagement/index"
import confStore from "@/store/modules/conf";

const store = confStore();
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  tableData: [],
  ruleForm: {
    type: '',
    sort_index: '',
    fileList: '',
    url: '',
  },
  rules: {

  },
  currentData: [],
  jumpTypeList: [
    { label: '无', value: 0 },
    { label: '窗口跳转', value: 1 },

    { label: '游戏', value: 2 },

    { label: '内部网页', value: 3 },

    { label: '外部网页', value: 4 }
  ],

})
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination() // 分页
const ruleFormRef = ref<FormInstance>()

// 获取数据
const getData = async () => {
  state.loading = true
  // paginationData.total = res.data.total
  let data = await banner_list_post({ page: paginationData.currentPage });
  data.data.map(v => {
    for (let i = 0; i < state.jumpTypeList.length; i++) {
      if (v.type == state.jumpTypeList[i].value) {
        v.type_name = state.jumpTypeList[i].label
      }

    }
  })
  state.tableData = data.data;
  state.loading = false
}

// 分页
watch(() => paginationData.currentPage, (val: number) => {
  getData();// 获取数据
}, { deep: true, immediate: true })

// 添加||编辑
const editRow = (type: string, data?) => {
  if (type == 'add') state.operationType = 'add'
  else state.operationType = 'edit'
  resetForm(ruleFormRef.value) // 重置表单

  state.currentData = data;
  state.ruleForm = data;
  state.dialogFormVisible = true
}
// 删除
const deleteRow = async (id: number) => {
  let data = await delete_banner_post({ bid: id })
  refreshData(data['code'])
}

//启用禁用表单
const updataRow = async (id, status) => {

  let data = await update_banner_status_post({ bid: id, status: status == 1 ? 0 : 1 });
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

// 取消
const cancel = () => {
  state.dialogFormVisible = false
}
//编辑
const updata = async () => {
  let data = new FormData();
  if (fileList) {
    data.append('img_url', fileList.file);
  }
  data.append('bid', state.currentData['bid']);
  data.append('type', state.ruleForm.type);
  data.append('url', state.ruleForm.url);
  data.append('sort_index', state.ruleForm.sort_index);
  let res = await detail_banner_post(data);
  console.log(res);
  refreshData(res['code'])
}
//添加
const add = async () => {
  let data = new FormData();
  if (fileList) {
    data.append('img_url', fileList.file);
  }
  data.append('bid', state.currentData['bid']);
  data.append('type', state.ruleForm.type);
  data.append('url', state.ruleForm.url);
  data.append('sort_index', state.ruleForm.sort_index);
  let res = await add_banner_post(data);
  refreshData(res['code'])
}

// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      if (state.operationType == 'add') {
        add();
      } else {
        updata();
      }
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

let fileList: any;
const cahnge_select = (val) => {
  console.log(val);

}

const handleRequest = (e) => {
  console.log(e);
  fileList = e;
  console.log(e)

}
</script>

<style lang="scss" scoped></style>

