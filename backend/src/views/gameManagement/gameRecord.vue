<template>
  <div class="app-container">

    <el-card class="box-card box-card-top">

      <el-select v-model="state.pageForm.cid" class="m-2" placeholder="所有渠道" clearable v-if="props.userIDShow">
        <el-option v-for="item in state.agent_list" :key="item['cid']" :label="item['username']" :value="item['cid']" />
      </el-select>
      <el-select v-model="state.pageForm.my_game" class="m-2" placeholder="集成商名称" clearable>
        <el-option v-for="item in state.factory_list" :key="item['factory_id']" :label="item['factory_name']"
          :value="item['factory_id']" />
      </el-select>
      <el-select v-model="state.pageForm.game_id" class="m-2" placeholder="平台名称" clearable>
        <el-option v-for="item in state.factory_details_list" :key="item['game_id']" :label="item['game_name']"
          :value="item['game_id']" />
      </el-select>
      <el-row class="demo-autocomplete">
        <el-col :span="12">
          <el-autocomplete v-model="game_value" :fetch-suggestions="querySearch" clearable class="inline-input w-50"
            placeholder="所有游戏" />
        </el-col>
      </el-row>

      <div>
        <datetime @def="timeChange" />
      </div>
      <el-input v-model="state.pageForm.uid" placeholder="用户名或uid或注单号" style="width: 200px;" clearable
        v-if="props.userIDShow" />
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="game_number" label="注单号" header-align="center" :align="'center'" sortable />
        <el-table-column prop="uid" label="用户昵称" header-align="center" :align="'center'" width="180"
          v-if="props.userIDShow">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
          </template>

        </el-table-column>
        <el-table-column prop="game_name" label="游戏" header-align="center" :align="'center'" />
        <el-table-column prop="game_id" label="游戏平台" header-align="center" :align="'center'"
          :formatter="gameNameFormatter" />
        <el-table-column :prop="state.is_win ? 'bet' : 'betting'" label="压分" header-align="center" :align="'center'" />
        <el-table-column prop="before_money" label="注单前" header-align="center" :align="'center'" />
        <el-table-column prop="after_money" label="注单后" header-align="center" :align="'center'" />
        <el-table-column prop="shu_ying" label="赢分" header-align="center" :align="'center'" />
        <el-table-column prop="gl" label="运行概率" header-align="center" :align="'center'" />
        <el-table-column prop="real_shu_ying" label="输赢" header-align="center" :align="'center'" />
        <el-table-column :prop="state.is_win ? 'bet' : 'code_size'" label="打码量" header-align="center" :align="'center'" />
        <el-table-column prop="game_number" label="局号" header-align="center" :align="'center'" />
        <el-table-column prop="add_time" label="时间" header-align="center" :align="'center'" sortable />
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
        <pagination :pageForm="state.pageForm" @def="getData" />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed, onMounted } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import { user_game_log_list_post, game_bet_log_post, external_game_list_post, game_log_conf_post } from "../../api/gameManagement";
import datetime from "@/components/datetime/index.vue"
import pagination from "@/components/pagination/index.vue"
import internal from "stream";
import { goToUserInfo } from "@/utils/baseFun"

const props = defineProps({
  userIDShow: {
    type: Boolean,
    default: true
  },
  uid: {
    type: String,
    default: null
  }
})
const pName = localStorage.getItem("pName")
const router = useRouter();
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  agent_list: [], // 渠道列表
  factory_list: [], // 集成商列表
  factory_details_list: [], // 平台名称列表
  external_game_list: [],
  timeArr: '',
  is_win: false,
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    stime: '',// 起始日期
    etime: '',// 结束日期
    gid: '',// 游戏
    uid: props.uid,// 用户
    cid: '',// 渠道
    game_id: '', // 总厂商
    my_game: '', // 厂商
    sort_index: 1,
    sort_field: "add_time"
  },
  tableData: [],
  ruleForm: {
    name: '',
  },
  rules: {
    name: [
      { required: true, message: '', trigger: 'blur' },
    ],
  },
})
interface RestaurantItem {
  value: string
  gid: string
}
const game_value = ref('')
const ruleFormRef = ref<FormInstance>()
const restaurants = ref<RestaurantItem[]>([])
// 值改变时筛选游戏并返回
const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? restaurants.value.filter(createFilter(queryString))
    : restaurants.value
  // call callback function to return suggestions
  cb(results)
}

// 筛选游戏
const createFilter = (queryString: string) => {
  return (restaurant: RestaurantItem) => {
    return (
      restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    )
  }
}

// 获取选择数据
onMounted(() => {
  console.log(pName)
  if (pName == "bigwin777") {
    state.is_win = false
  } else {
    state.is_win = true 
  }
  game_log_conf_post({ limit: 999, page: 1 }).then(res => {
    state.agent_list = res['channel']
    state.factory_list = res['factory_list']
    state.factory_details_list = res['game_list']
    restaurants.value = res['external_game_list']
    console.log(state.factory_details_list)
  })
})

// 获取游戏id
const getgameid = () => {
  state.pageForm.gid = ''
  for (let i = 0; i < restaurants.value.length; i++) {
    if (restaurants.value[i].value == game_value.value) {
      state.pageForm.gid = restaurants.value[i].gid
      break;
    }
    ;
  }
}

// 获取数据
const getData = async () => {
  state.loading = true
  state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
  getgameid()
  if (state.is_win) {
    game_bet_log_post({ ...state.pageForm }).then(res => {
      console.log(state.pageForm)
      state.pageForm.total = res['count']
      state.tableData = res['data']
    }).finally(() => {
      state.loading = false
    })
  } else {
    user_game_log_list_post({ ...state.pageForm }).then(res => {
      state.pageForm.total = res['count']
      state.tableData = res['data']
    }).finally(() => {
      state.loading = false
    })
  }
}


const gameNameFormatter = (row) => {
  for (let i = 0; i < state.factory_details_list.length; i++) {
    if (row.game_id == state.factory_details_list[i].game_id) {
      return state.factory_details_list[i].game_name
    }
  }
}

const timeChange = (time) => {
  state.timeArr = time
  getData()
}

// 搜索数据
const searchData = () => {
  getData();// 获取数据
}


// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>

<style lang="scss" scoped></style>

