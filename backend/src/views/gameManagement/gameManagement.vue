<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-input v-model="state.pageForm.gid" placeholder="游戏名或ID" style="width: 200px;" clearable />
      <el-select v-model="state.pageForm.my_game" class="m-2" placeholder="集成商名称" clearable>
        <el-option v-for="item in state.IntegratorNameList" :label="item['factory_name']" :value="item['factory_id']"
          :key="item" />
      </el-select>
      <el-select v-model="state.pageForm.game_id" class="m-2" placeholder="平台名称" clearable>
        <el-option v-for="item in state.platformNameList" :label="item['game_name']" :value="item['game_id']"
          :key="item" />
      </el-select>
      <el-select v-model="state.pageForm.game_type" class="m-2" placeholder="所有分类" clearable>
        <el-option v-for="item in state.typeList" :label="item['type_name']" :value="item['type']" :key="item" />
      </el-select>
      <el-select v-model="state.pageForm.is_hot" class="m-2" placeholder="是否热门" clearable>
        <el-option v-for="item in state.hotList" :label="item['label']" :value="item['value']" />
      </el-select>
      <el-select v-model="state.pageForm.is_demo" class="m-2" placeholder="是否为demo游戏" clearable>
        <el-option v-for="item in state.hotList" :label="item['label']" :value="item['value']" />
      </el-select>
      <el-select v-model="state.pageForm.status" class="m-2" placeholder="禁用状态" clearable>
        <el-option v-for="item in state.stateList" :label="item['label']" :value="item['value']" />
      </el-select>
      <el-button type="primary" @click="searchData()">搜索</el-button>
      <el-button type="primary" @click="editRow('add')">添加游戏</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="gid" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="game_name" label="游戏名称" header-align="center" :align="'center'" />
        <el-table-column prop="icon" label="游戏封面" header-align="center" :align="'center'">
          <template #default="scope">
            <img :src="scope.row.icon" alt="" class="coverImg">
          </template>
        </el-table-column>
        <el-table-column prop="factory_name" label="集成商名称" header-align="center" :align="'center'" />
        <el-table-column prop="provider_game_id" label="key" header-align="center" :align="'center'" />
        <el-table-column prop="platform_name" label="平台名称" header-align="center" :align="'center'" />
        <el-table-column prop="game_type" label="分类" header-align="center" :align="'center'"
          :formatter="gameTypeFormatter" />
        <el-table-column prop="is_hot" label="是否热门" header-align="center" :align="'center'" sortable>
          <template #default="scope">
            {{ scope.row.is_hot == 0 ? "否" : "是" }}
          </template>
        </el-table-column>
        <el-table-column prop="is_demo" label="是否为demo游戏" header-align="center" :align="'center'" sortable>
          <template #default="scope">
            {{ scope.row.is_demo == 1 ? "是" : "否" }}
          </template>
        </el-table-column>
        <el-table-column prop="rtp" label="游戏的玩家回报率(%)" header-align="center" :align="'center'" sortable />
        <el-table-column prop="status" label="状态" header-align="center" :align="'center'" sortable>
          <template #default="scope">
            {{ scope.row.status == 0 ? "禁用" : "启用" }}
          </template>
        </el-table-column>
        <el-table-column prop="sort_index" label="排序" header-align="center" :align="'center'" sortable />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230">
          <template #default="scope">
            <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
            <el-button type="warning" @click="UpdateStatus(scope.row)">{{ scope.row.status == 0 ? "启用" : "禁用"
            }}</el-button>
            <el-button type="danger" @click="deleteRow(scope.row.gid)">删除</el-button>
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
        <el-form-item label="游戏名称" prop="game_name">
          <el-input v-model="state.ruleForm.game_name" style="width: 50%;" />
        </el-form-item>
        <el-form-item label="集成商" prop="my_game">
          <el-select v-model="state.ruleForm.my_game" class="m-2" placeholder="集成商名称" clearable>
            <el-option v-for="item in state.IntegratorNameList" :label="item['factory_name']" :value="item['factory_id']"
              :key="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="游戏平台" prop="game_id">
          <el-select v-model="state.ruleForm.game_id" class="m-2" placeholder="平台名称" clearable>
            <el-option v-for="item in state.platformNameList" :label="item['game_name']" :value="item['game_id']"
              :key="item" />
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="封面" prop="icon">
          <imgUpload :img="state.ruleForm.icon ? `${store.imgUrl}${state.ruleForm.icon}` : ''"
            @getImgData="get_icon_url" />
        </el-form-item> -->
        <el-form-item label="游戏分类" prop="game_type">
          <el-select v-model="state.ruleForm.game_type" class="m-2" placeholder="游戏分类" clearable>
            <el-option v-for="item in state.typeList" :label="item['type_name']" :value="item['type']" :key="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否top" prop="is_top">
          <el-select v-model="state.ruleForm.is_top" class="m-2" placeholder="是否top" clearable>
            <el-option v-for="item in state.topList" :label="item['label']" :value="item['value']" :key="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否热门" prop="is_hot">
          <el-select v-model="state.ruleForm.is_hot" class="m-2" placeholder="是否热门" clearable>
            <el-option v-for="item in state.hotList" :label="item['label']" :value="item['value']" :key="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否为demo游戏" prop="is_demo">
          <el-select v-model="state.ruleForm.is_demo" class="m-2" placeholder="是否热门" clearable>
            <el-option v-for="item in state.hotList" :label="item['label']" :value="item['value']" :key="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="屏幕状态" prop="screen">
          <el-select v-model="state.ruleForm.screen" class="m-2" placeholder="屏幕状态" clearable>
            <el-option v-for="item in state.screenList" :label="item['label']" :value="item['value']" :key="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="sort_index">
          <el-input v-model="state.ruleForm.sort_index" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleFormRef)">Create</el-button>
          <el-button @click="cancel">cancel</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import { external_game_list_post, external_game_conf_post, add_external_game_post, external_game_detail_post, update_external_game_status_post, delete_external_game_post } from "../../api/gameManagement/index"
import confStore from "@/store/modules/conf";
import pagination from "@/components/pagination/index.vue"
import imgUpload from "@/components/imgUpload/index.vue"
const router = useRouter();
const store = confStore();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  options: [],
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    game_id: '', // 游戏id
    gid: '', // 编码
    game_type: '',// 游戏类型
    my_game: '', // 厂商id
    is_hot: '', // 1是 0否
    is_demo: '',// 1是 0否
    status: '',  // 0 | 1
  },
  tableData: [],
  ruleForm: {
    game_name: '',//游戏名称
    my_game: '',//厂商id
    game_id: '',//游戏平台id
    icon: '',//封面
    game_type: '',//游戏类型
    screen: '',//0 自动 1 横屏 2 竖屏
    sort_index: '',//排序
    is_top: '',//是否排行
    is_hot: '',//是否热门
    is_demo: '',//是否demo游戏
    min_enter_money: '',//最少进入金额
    min_recharge_money: '',//最少充值金额
  },
  rules: {
    game_name: [
      { required: true, message: '', trigger: 'blur' },
    ],
    game_type: [
      { required: true, message: '', trigger: 'blur' },
    ],
    screen: [
      { required: true, message: '', trigger: 'blur' },
    ],
    sort_index: [
      { required: true, message: '', trigger: 'blur' },
    ],
    min_enter_money: [
      { required: true, message: '', trigger: 'blur' },
    ],
    min_recharge_money: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
  //下拉框数据
  hotList: [
    { value: 1, label: '是' },
    { value: 0, label: '否' }
  ],
  //下拉框数据
  topList: [
    { value: 1, label: '是' },
    { value: 0, label: '否' }
  ],
  stateList: [
    { value: 1, label: '启用' },
    { value: 0, label: '禁用' }
  ],
  screenList: [
    { value: 0, label: '自动' },
    { value: 1, label: '横屏' },
    { value: 2, label: '竖屏' }
  ],
  typeList: [

  ],
  platformNameList: [

  ],
  IntegratorNameList: [

  ],
  gameTypeList: [],
})
const ruleFormRef = ref<FormInstance>()


const get_icon_url = (val: string) => {
  state.ruleForm.icon = val
}
const setSelectList = async () => {
  state.typeList = store.gameType;
  external_game_conf_post({}).then(res => {
    state.IntegratorNameList = res['factory_list']
    state.platformNameList = res['game_list']
    state.gameTypeList = res['game_type_list']
  })
}

const gameTypeFormatter = (row) => {
  for (var i = 0; i < state.gameTypeList.length; i++) {
    if (state.gameTypeList[i].type == row.game_type) {
      return state.gameTypeList[i].type_name
    }
  }
}


// 获取数据
const getData = async () => {
  state.loading = true
  setSelectList();
  external_game_list_post({ ...state.pageForm }).then((res: any) => {
    state.pageForm.total = res.count;
    state.tableData = res.data;
  }).finally(() => {
    state.loading = false
  })
}
getData();// 获取数据


// 搜索数据
const searchData = () => {
  getData();// 获取数据
}

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
// 删除
const deleteRow = async (id: number) => {
  delete_external_game_post({ gid: id }).then(res => {
    if (res['code'] == 1) {
      getData()
    }
  })
}
// 禁用
const UpdateStatus = async (row: any) => {
  update_external_game_status_post({ gid: row.gid, status: row.status == 0 ? 1 : 0 }).then(res => {
    if (res['code'] == 1) {
      getData()
    }
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
      if (state.operationType == 'add') requestApi = add_external_game_post
      else requestApi = external_game_detail_post
      // -------
      let data = new FormData();
      for (var i in state.ruleForm) {
        data.append(i, state.ruleForm[i]);
      }
      // -------

      requestApi(data).then(res => {
        if (res.code == 1) {
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
</script>

<style lang="scss" scoped>
.coverImg {
  width: 50%;
  height: 50%;
}
</style>

