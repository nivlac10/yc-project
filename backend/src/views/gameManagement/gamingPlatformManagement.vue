<template>
  <div class="app-container">
    <!-- head -->
    <el-card class="box-card box-card-top">
      <el-input v-model="state.pageForm.gid" placeholder="请输入平台名称或id" style="width: 15%; height: 40px;" />

      <el-select v-model="state.pageForm.factory_id" class="m-2" placeholder="集成商名称" size="large" clearable>
        <el-option v-for="item in state.factoryList" :key="item['factory_id']" :label="item['factory_name']"
          :value="item['factory_id']" />
      </el-select>

      <el-select v-model="state.pageForm.game_type" class="m-2" placeholder="所有类型" size="large" clearable>
        <el-option v-for="item in state.typeList" :key="item['label']" :label="item['value']" :value="item['label']" />
      </el-select>

      <el-select v-model="state.pageForm.status" class="m-2" placeholder="平台状态" size="large" clearable>
        <el-option v-for="item in state.stateList" :key="item['label']" :label="item['value']" :value="item['label']" />
      </el-select>

      <el-button type="primary" @click="editRow('add')" style="height: 40px;">添加平台</el-button>
      <el-button type="primary" @click="searchData" style="height: 40px;">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="game_id" label="平台ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="game_name" label="平台名称" header-align="center" :align="'center'" />
        <el-table-column prop="cover" label="平台封面" header-align="center" :align="'center'">
          <template #default="scope">
            <el-image :src="scope.row.cover" :fit="'contain'">
              <template #error>
                <div class="image-slot">
                  <el-icon><icon-picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="factory_name" label="集成商" header-align="center" :align="'center'" />
        <el-table-column prop="game_type" label="厂商分类" header-align="center" :align="'center'"
          :formatter="typeFormatter" />
        <el-table-column prop="status" label="状态" header-align="center" :align="'center'" :formatter="statusFormatter" />
        <el-table-column prop="sort_index" label="排序" header-align="center" :align="'center'" sortable />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="warning" size="small" @click="updataRow(scope.row.game_id, scope.row.status)">{{
              scope.row.status
              ==
              1 ? '禁用' : '启用' }}</el-button>
            <el-button type="danger" size="small" @click="deleteRow(scope.row.game_id)">删除</el-button>
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
        <el-form-item label="集成商" prop="integratorName">
          <el-select v-model="state.ruleForm.factory_id" placeholder="集成商名称" size="large" clearable>
            <el-option v-for="item in state.factoryList" :key="item['factory_id']" :label="item['factory_name']"
              :value="item['factory_id']" />
          </el-select>
        </el-form-item>
        <el-form-item label="平台名称" prop="game_name">
          <el-input v-model="state.ruleForm.game_name" />
        </el-form-item>
        <el-form-item label="封面" prop="cover">
          <!-- @vue-ignore -->
          <el-upload v-model:file-list="state.ruleForm.fileList" class="upload-demo" :limit="1"
            :http-request="handleRequest">
            <el-button type="primary">Click to upload</el-button>
          </el-upload>
        </el-form-item>

        <el-form-item label="游戏分类" prop="gameType">
          <el-select v-model="state.ruleForm.game_type" placeholder="所有分类" size="large" clearable>
            <el-option v-for="item in state.typeList" :key="item.label" :label="item.label" :value="item.val" />
          </el-select>
        </el-form-item>

        <el-form-item label="排序" prop="game_name">
          <el-input v-model="state.ruleForm.sort_index" />
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
import { ElMessage, UploadProps, type FormInstance, type FormRules, UploadUserFile } from 'element-plus'
import { usePagination } from "../../hooks/usePagination"
import { game_conf_post, game_list_post, add_game_post, game_detail_post, update_game_status_post, delete_game_post } from "@/api/gameManagement";
import { Picture as IconPicture } from '@element-plus/icons-vue'
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  id: 0,
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    gid: '',//厂商id
    game_type: '',//游戏类型
    status: '',//状态
    factory_id: ''//总厂商id
  },
  tableData: [],
  ruleForm: {
    game_id: '',
    game_name: '',
    factory_id: '',
    game_type: '',
    sort_index: '',
    status: '',
  },
  rules: {
    game_name: [
      { required: true, message: '', trigger: 'blur' },
    ],
    factory_id: [
      { required: true, message: '', trigger: 'blur' },
    ],
    game_type: [
      { required: true, message: '', trigger: 'blur' },
    ],

    sort_index: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
  platformNameOrIdValue: '',
  factoryList: [],
  typeList: [
    { val: 0, label: 'URl地址' },
    { val: 1, label: 'html嵌入' }
  ],
  stateList: [{ value: '禁用', label: '0' }, { value: '启用', label: '1', }],
  stateValue: '',
})

const { paginationData, handleCurrentChange, handleSizeChange } = usePagination();// 分页

const ruleFormRef = ref<FormInstance>()


let fileList: any;

const statusFormatter = (row) => {
  if (row.status == 0) return '禁用'
  else return '启用'
}

const typeFormatter = (row) => {
  if (row.game_type == 0) return 'URl地址'
  else if (row.game_type == 1) return 'html嵌入'
}

const handleRequest = (e) => {
  console.log(e);
  fileList = e;
}


// 获取数据
const getData = async () => {
  state.loading = true
  game_list_post({ ...state.pageForm }).then((res: any) => {
    state.pageForm.total = res.count;
    state.tableData = res.data;
    // setSelectList(res.data);
  }).finally(() => {
    state.loading = false
  })
}


const setSelect = () => {
  game_conf_post({}).then(res => {
    state.factoryList = res['data']
  })
}


//初始化
const initialize = async () => {
  await getData();
  setSelect()
}
initialize()

// 分页
watch(() => paginationData.currentPage, (val: number) => {
  getData();// 获取数据
}, { deep: true, immediate: true })

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



// 取消
const cancel = () => {
  state.dialogFormVisible = false
}
// 删除
const deleteRow = async (game_id: number) => {
  let data = await delete_game_post({ game_id: game_id });
  refreshData(data['code'])

}
// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      let requestApi = null;
      if (state.operationType == 'add') {
        add();
      }
      else {
        updata();
      }
      // requestApi({ file: fileList.file, ...state.ruleForm }).then(res => {
      //   refreshData(res.code)
      // })
    } else {
      console.log('error submit!', fields)
    }
  })
}

//编辑
const updata = async () => {
  let data = new FormData();
  if (fileList) {
    data.append('file', fileList.file);
  }
  data.append('game_id', state.ruleForm.game_id);
  data.append('game_name', state.ruleForm.game_name);
  data.append('sort_index', state.ruleForm.sort_index);
  data.append('game_type', state.ruleForm.game_type);
  data.append('factory_id', state.ruleForm.factory_id);
  data.append('status', state.ruleForm.status);
  let res = await game_detail_post(data);
  refreshData(res['code'])
}

//添加
const add = async () => {
  let data = new FormData();
  if (fileList) {
    data.append('file', fileList.file);
  }
  data.append('game_name', state.ruleForm.game_name);
  data.append('sort_index', state.ruleForm.sort_index);
  data.append('game_type', state.ruleForm.game_type);
  data.append('factory_id', state.ruleForm.factory_id);
  data.append('status', state.ruleForm.status);
  let res = await add_game_post(data);
  refreshData(res['code'])
}

//启用禁用表单
const updataRow = async (id, status) => {
  let data = await update_game_status_post({ game_id: id, status: status == 1 ? 0 : 1 });
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

// 搜索数据
const searchData = () => {
  getData();// 获取数据
}

function selectByNameOrId(arr, v) {
  if (typeof (state.platformNameOrIdValue) == 'number') {
    if (v.factory_id == state.platformNameOrIdValue) {
      arr.push(v);
    }
  } else {
    console.log(v.game_name.toLowerCase(), (state.platformNameOrIdValue as any).toLowerCase());

    if (v.game_name.toLowerCase().includes((state.platformNameOrIdValue as any).toLowerCase())) {
      arr.push(v);
    }
  }
}


</script>

<style lang="scss" scoped>
.coverImg {
  width: 50%;
  height: 50%;
}
</style>

