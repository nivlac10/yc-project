<template>
  <div class="app-container">
    <el-form :model="state.form" label-width="120px">
      <el-form-item label="邀请首充赠送">
        <el-input v-model="state.form.invit_recharge_gift" type="number" style="width: 150px;" />&nbsp;%
      </el-form-item>
      <el-form-item label="一级打码返佣">
        <el-input v-model="state.form.one_bet_rebate" type="number" style="width: 150px;" />&nbsp;%
      </el-form-item>
      <el-form-item label="二级打码返佣">
        <el-input v-model="state.form.two_bet_rebate" type="number" style="width: 150px;" />&nbsp;%
      </el-form-item>
      <el-form-item label="三级打码返佣">
        <el-input v-model="state.form.three_bet_rebate" type="number" style="width: 150px;" />&nbsp;%
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="setData">保存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup >
import { task_conf_list_post, update_data_conf } from "@/api/platformManagement";
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"

const router = useRouter();
const state = reactive({
  form: {
    invit_recharge_gift: '',// 邀请首充赠送
    one_bet_rebate: '',// 一级打码配置,
    two_bet_rebate: '',// 二级打码配置,
    three_bet_rebate: ''// 三级打码配置
  },
})

const getData = () => {
  task_conf_list_post({}).then(res => {
    state.form = res.data[0]
  })
}
getData()

const setData = () => {
  update_data_conf({ ...state.form }).then(res => {
    if (res.code == 1) getData()
  })
}
</script>

<style lang="scss" scoped></style>

