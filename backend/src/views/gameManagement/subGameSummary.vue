<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-select v-model="state.pageForm.cid" class="m-2" placeholder="所有渠道" clearable>
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

      <el-select v-model="state.pageForm.sort_index" class="m-2" placeholder="">
        <el-option label="默认排序" :value="null" />
        <el-option label="压分" value="total_bet" />
        <el-option label="游戏id" value="game_id" />
      </el-select>
      <div>
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="game_name" label="游戏" header-align="center" :align="'center'" />
        <el-table-column prop="factory_name" label="集成商" header-align="center" :align="'center'" />
        <el-table-column prop="platform_name" label="游戏平台" header-align="center" :align="'center'" />
        <el-table-column prop="total_bet" label="压分" header-align="center" :align="'center'" />
        <el-table-column prop="total_shu_ying" label="赢分" header-align="center" :align="'center'" />
        <el-table-column prop="gl" label="运行概率" header-align="center" :align="'center'" />
        <el-table-column prop="total_real_shu_ying" label="输赢" header-align="center" :align="'center'" />
        <el-table-column prop="total_num" label="注单数" header-align="center" :align="'center'" />
        <el-table-column prop="ol_num" label="在线人数" header-align="center" :align="'center'" />
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
import { external_game_total_post, game_list_post, external_game_list_post, game_log_conf_post } from "../../api/gameManagement";
import { agent_list_post } from "../../api/channelManagement";
import { factory_list_post } from "../../api/IntegratorManagement";
import datetime from "@/components/datetime/index.vue"
import pagination from "@/components/pagination/index.vue"

const router = useRouter();
const state = reactive({
  loading: false, // table loading
  agent_list: [], // 渠道列表
  factory_list: [], // 集成商列表
  factory_details_list: [], // 平台名称列表
  external_game_list: [], // 所有游戏
  timeArr: '',
  pageForm: {
    page: 1,
    limit: 20,
    total: 0,
    stime: '',// 起始日期
    etime: '',// 结束日期
    gid: '',// 游戏
    cid: '',// 渠道
    my_game: '', // 总厂商
    game_id: '', // 厂商
    sort_index: null, // 排序列明
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
  game_log_conf_post({ limit: 999, page: 1 }).then(res => {
    state.agent_list = res['channel']
    state.factory_list = res['factory_list']
    state.factory_details_list = res['game_list']
    restaurants.value = res['external_game_list']
  })
})

// 获取游戏id
const getgameid = () => {
  state.pageForm.gid=''
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
  external_game_total_post({ ...state.pageForm }).then(res => {
    state.pageForm.total = res['count']
    state.tableData = res['data']
    state.loading = false
  })
}

const timeChange = (time) => {
  state.timeArr = time
  getData()
}

// 搜索数据
const searchData = () => {
  getData();// 获取数据
}
</script>

<style lang="scss" scoped></style>

