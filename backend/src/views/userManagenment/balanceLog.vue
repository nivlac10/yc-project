<template>
  <div class="app-container">
    <el-card class="box-card box-card-top">
      <el-input v-model="state.searchForm.uid" placeholder="请输入用户名或uid" style="width: 200px;" clearable
        v-if="props.userIDShow" />

      <el-select v-model="state.searchForm.money_type" class="m-2" placeholder="金额类型" clearable>
        <el-option v-for="item in state.money_type_list" :key="item['code']" :label="item['name']"
          :value="item['code']" />
      </el-select>
      <el-select v-model="state.searchForm.log_type" class="m-2" placeholder="请选择" clearable>
        <el-option v-for="item in state.log_type_list" :key="item['label']" :label="item['value']"
          :value="item['label']" />
      </el-select>
      <div>
        <datetime @def="timeChange" />
      </div>
      <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
        <el-table-column prop="uid" label="用户名" header-align="center" :align="'center'" width="180"
          v-if="props.userIDShow">
          <template #default="scope">
            <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
              `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
          </template>

        </el-table-column>
        <el-table-column prop="money_type_str" label="金额类型" header-align="center" :align="'center'"/>
        <el-table-column prop="log_type" label="变动类型" header-align="center" :align="'center'" />
        <el-table-column prop="money" label="金额" header-align="center" :align="'center'" />
        <el-table-column prop="before_money" label="变动前余额" header-align="center" :align="'center'" />
        <el-table-column prop="after_money" label="变动后余额" header-align="center" :align="'center'" />
        <el-table-column prop="add_time" label="时间" header-align="center" :align="'center'" />
      </el-table>
    </el-card>

    <el-card uno-margin-top>
      <div class="pager-wrapper">
        <pagination :pageForm="state.searchForm" @def="getData" />
      </div>
    </el-card>

  </div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import { usePagination } from "@/hooks/usePagination"
import { money_type_list_post, money_log_list_post } from "../../api/userManagenment";
import datetime from "@/components/datetime/index.vue"
import pagination from "@/components/pagination/index.vue"
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
const router = useRouter();
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination() // 分页
const state = reactive({
  loading: false, // table loading
  operationType: 'add', // add || edit
  dialogFormVisible: false,
  money_type_list: [],
  log_type_list: [
    { label: '', value: '变动类型' },
    { label: 0, value: '余额' },
    { label: 1, value: '佣金' }
  ], // 渠道列表
  timeArr: '',
  searchForm: {
    page: 1,
    limit: 20,
    total: 0,
    stime: '',// 起始日期
    etime: '',// 结束日期
    uid: props.uid,//用户
    money_type: '',// 金额类型
    log_type: '',//日志类型
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
  gameTypeList: [],
})
const ruleFormRef = ref<FormInstance>()

// 获取选择数据
const getSelectData = () => {
  // 渠道
  money_type_list_post({}).then(res => {
    state.money_type_list = res['data']
  })

}
getSelectData()// 获取选择数据


// 获取数据
const getData = async () => {
  state.loading = true
  state.searchForm.stime = state.timeArr ? state.timeArr[0] : ''
  state.searchForm.etime = state.timeArr ? state.timeArr[1] : ''
  money_log_list_post({ ...state.searchForm }).then(res => {
    state.searchForm.total = res['count']
    state.tableData = res['data']
  }).finally(() => {
    state.loading = false
  })
}

const moneyTypeFormatter = (row) => {
  for (var item in state.money_type_list) {
    if (item == row.money_type) {
      console.log(item, row.money_type)
      console.log(state.money_type_list[item])
      return state.money_type_list[item]['name']
    }
  }
}

// 搜索数据
const searchData = () => {
  getData();// 获取数据
}

const timeChange = (time) => {
  state.timeArr = time
  getData()
}

// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>

<style lang="scss" scoped></style>

