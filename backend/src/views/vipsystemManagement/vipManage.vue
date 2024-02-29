<template>
    <div class="app-container">
        <el-card class="box-card">
            <el-button type="primary" @click="editRow('add')">添加</el-button>
        </el-card>
        <el-card class="box-card" uno-margin-top>
            <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
                <el-table-column prop="vip_lv" label="vip等级" header-align="center" :align="'center'" />
                <el-table-column prop="recharge" label="vip充值" header-align="center" :align="'center'" sortable />
                <el-table-column prop="bet" label="vip下注" header-align="center" :align="'center'" sortable />
                <el-table-column prop="withdraw_num" label="提现次数" header-align="center" :align="'center'" sortable />
                <el-table-column prop="max_withdraw" label="最大提现" header-align="center" :align="'center'" sortable />
                <el-table-column prop="pay_fee" label="付费率" header-align="center" :align="'center'" sortable />
                <el-table-column prop="day_max_withdraw" label="每天最大提现额" header-align="center" :align="'center'" sortable />
                <el-table-column prop="lv_reward_split_day" label="等级拆分天数" header-align="center" :align="'center'"
                    sortable />
                <el-table-column prop="lv_reward_now_rate" label="等级立即领取金额" header-align="center" :align="'center'"
                    sortable />
                <el-table-column prop="lv_reward_split_rate" label="等级拆分比例" header-align="center" :align="'center'"
                    sortable />
                <el-table-column prop="date" label="立即反水" header-align="center" :width="200" :align="'center'" sortable>
                    <template #default="scope">
                        {{ `反水比例:${scope.row.bet_bonus_rate}%;` }}
                        <br>
                        {{ `拆分天数:${scope.row.bet_bonus_split_day}天；` }}
                        <br>
                        {{ ` 立即领取比例:${scope.row.bet_bonus_now_rate}%； ` }}
                        <br>
                        {{ ` 拆分比利:${scope.row.bet_bonus_split_rate}%； ` }}
                        <br>
                        {{ `保留天数:${scope.row.bet_bonus_save_time}天；` }}
                    </template>
                </el-table-column>
                <el-table-column prop="date" label="日打码" header-align="center" :width="200" :align="'center'" sortable>
                    <template #default="scope">

                        {{ `反水比例:${scope.row.day_bet_bonus_rate}%;` }}
                        <br>
                        {{ `拆分天数:${scope.row.day_bet_bonus_split_day}天；` }}
                        <br>
                        {{ ` 立即领取比例:${scope.row.day_bet_bonus_now_rate}%； ` }}
                        <br>
                        {{ ` 拆分比利:${scope.row.day_bet_bonus_split_rate}%； ` }}
                        <br>
                        {{ `保留天数:${scope.row.day_bet_bonus_save_time}天；` }}
                    </template>
                </el-table-column>
                <el-table-column prop="date" label="周打码" header-align="center" :width="200" :align="'center'" sortable>
                    <template #default="scope">
                        {{ `反水比例:${scope.row.week_bet_bonus_rate}%;` }}
                        <br>
                        {{ `拆分天数:${scope.row.week_bet_bonus_split_day}天；` }}
                        <br>
                        {{ ` 立即领取比例:${scope.row.week_bet_bonus_now_rate}%； ` }}
                        <br>
                        {{ ` 拆分比利:${scope.row.week_bet_bonus_split_rate}%； ` }}
                        <br>
                        {{ `保留天数:${scope.row.week_bet_bonus_save_time}天；` }}
                    </template>
                </el-table-column>
                <el-table-column prop="date" label="月打码" header-align="center" :width="200" :align="'center'" sortable>
                    <template #default="scope">
                        {{ `反水比例:${scope.row.month_bet_bonus_rate}%;` }}
                        <br>
                        {{ `拆分天数:${scope.row.month_bet_bonus_split_day}天；` }}
                        <br>
                        {{ ` 立即领取比例:${scope.row.month_bet_bonus_now_rate}%； ` }}
                        <br>
                        {{ ` 拆分比利:${scope.row.month_bet_bonus_split_rate}%； ` }}
                        <br>
                        {{ `保留天数:${scope.row.month_bet_bonus_save_time}天；` }}
                    </template>
                </el-table-column>
                <el-table-column fixed="right" label="操作" header-align="center" :align="'center'">
                    <template #default="scope">
                        <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>

        <el-dialog v-model="state.dialogFormVisible" :title="state.operationType == 'add' ? '添加' : '编辑'" :draggable="true">
            <el-form ref="ruleFormRef" :model="state.ruleForm" :rules="state.rules" label-width="150px"
                class="demo-ruleForm-inline" status-icon>
                <el-form-item label="会员等级" prop="vip_lv">
                    <el-input v-model="state.ruleForm.vip_lv" />
                </el-form-item>
                <el-form-item label="vip充值" prop="recharge">
                    <el-input v-model="state.ruleForm.recharge" />
                </el-form-item>
                <el-form-item label="vip下注" prop="bet">
                    <el-input v-model="state.ruleForm.bet" />
                </el-form-item>
                <el-form-item label="每天最大提现额" prop="day_max_withdraw">
                    <el-input v-model="state.ruleForm.day_max_withdraw" />
                </el-form-item>
                <el-form-item label="等级拆分天数" prop="lv_reward_split_day">
                    <el-input v-model="state.ruleForm.lv_reward_split_day" />
                </el-form-item>
                <el-form-item label="等级立即领取金额" prop="lv_reward_now_rate">
                    <el-input v-model="state.ruleForm.lv_reward_now_rate" />
                </el-form-item>
                <el-form-item label="等级拆分比例" prop="lv_reward_split_rate">
                    <el-input v-model="state.ruleForm.lv_reward_split_rate" />
                </el-form-item>

                <el-form-item label="立即反水：反水比例" prop="bet_bonus_rate" class="item-FSBL" label-width="220px">
                    <el-input v-model="state.ruleForm.bet_bonus_rate" />
                </el-form-item>
                <el-form-item label="拆分天数" prop="bet_bonus_split_day" class="item-CFTS" label-width="120px">
                    <el-input v-model="state.ruleForm.bet_bonus_split_day" />
                </el-form-item>
                <el-form-item label="立即领取比例" prop="bet_bonus_now_rate" class="item-LQBL" label-width="120px">
                    <el-input v-model="state.ruleForm.bet_bonus_now_rate" />
                </el-form-item>
                <el-form-item label="拆分比例" prop="bet_bonus_split_rate" class="item-CFBL" label-width="220px">
                    <el-input v-model="state.ruleForm.bet_bonus_split_rate" />
                </el-form-item>
                <el-form-item label="保留时间" prop="bet_bonus_save_time" class="item-BLSJ" label-width="120px">
                    <el-input v-model="state.ruleForm.bet_bonus_save_time" />
                </el-form-item>

                <el-form-item label="日打码：反水比例" prop="day_bet_bonus_rate" class="item-FSBL" label-width="220px">
                    <el-input v-model="state.ruleForm.day_bet_bonus_rate" />
                </el-form-item>
                <el-form-item label="拆分天数" prop="day_bet_bonus_split_day" class="item-CFTS" label-width="120px">
                    <el-input v-model="state.ruleForm.day_bet_bonus_split_day" />
                </el-form-item>
                <el-form-item label="立即领取比例" prop="day_bet_bonus_now_rate" class="item-LQBL" label-width="120px">
                    <el-input v-model="state.ruleForm.day_bet_bonus_now_rate" />
                </el-form-item>
                <el-form-item label="拆分比利" prop="day_bet_bonus_split_rate" class="item-CFBL" label-width="220px">
                    <el-input v-model="state.ruleForm.day_bet_bonus_split_rate" />
                </el-form-item>
                <el-form-item label="保留天数" prop="day_bet_bonus_save_time" class="item-BLSJ" label-width="120px">
                    <el-input v-model="state.ruleForm.day_bet_bonus_save_time" />
                </el-form-item>

                <el-form-item label="周打码：反水比例" prop="week_bet_bonus_rate" class="item-FSBL" label-width="220px">
                    <el-input v-model="state.ruleForm.week_bet_bonus_rate" />
                </el-form-item>
                <el-form-item label="拆分天数" prop="week_bet_bonus_split_day" class="item-CFTS" label-width="120px">
                    <el-input v-model="state.ruleForm.week_bet_bonus_split_day" />
                </el-form-item>
                <el-form-item label="立即领取比例" prop="week_bet_bonus_now_rate" class="item-LQBL" label-width="120px">
                    <el-input v-model="state.ruleForm.week_bet_bonus_now_rate" />
                </el-form-item>
                <el-form-item label="反水拆分比利" prop="week_bet_bonus_split_rate" class="item-CFBL" label-width="220px">
                    <el-input v-model="state.ruleForm.week_bet_bonus_split_rate" />
                </el-form-item>
                <el-form-item label="保留天数" prop="week_bet_bonus_save_time" class="item-BLSJ" label-width="120px">
                    <el-input v-model="state.ruleForm.week_bet_bonus_save_time" />
                </el-form-item>
                <el-form-item label="月打码：反水比例" prop="month_bet_bonus_rate" class="item-FSBL" label-width="220px">
                    <el-input v-model="state.ruleForm.month_bet_bonus_rate" />
                </el-form-item>
                <el-form-item label="拆分天数" prop="month_bet_bonus_split_day" class="item-CFTS" label-width="120px">
                    <el-input v-model="state.ruleForm.month_bet_bonus_split_day" />
                </el-form-item>
                <el-form-item label="立即领取比例" prop="month_bet_bonus_now_rate" class="item-LQBL" label-width="120px">
                    <el-input v-model="state.ruleForm.month_bet_bonus_now_rate" />
                </el-form-item>
                <el-form-item label="反水拆分比利" prop="month_bet_bonus_split_rate" class="item-CFBL" label-width="220px">
                    <el-input v-model="state.ruleForm.month_bet_bonus_split_rate" />
                </el-form-item>
                <el-form-item label="保留天数" prop="month_bet_bonus_save_time" class="item-BLSJ" label-width="120px">
                    <el-input v-model="state.ruleForm.month_bet_bonus_save_time" />
                </el-form-item>
                <el-form-item label="提现次数" prop="withdraw_num">
                    <el-input v-model="state.ruleForm.withdraw_num" />
                </el-form-item>
                <el-form-item label="最大提现" prop="max_withdraw">
                    <el-input v-model="state.ruleForm.max_withdraw" />
                </el-form-item>
                <el-form-item label="付费率" prop="pay_fee">
                    <el-input v-model="state.ruleForm.pay_fee" />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm(ruleFormRef)">Create</el-button>
                    <el-button @click="cancel">cancel</el-button>
                    <!-- <el-button @click="resetForm(ruleFormRef)">Reset</el-button> -->
                </el-form-item>
            </el-form>
        </el-dialog>
        <vipLow></vipLow>
    </div>
</template>
  
<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import { edit_vip_lv, vip_lv_list } from '@/api/vipsystemManagement/index';
import pagination from "@/components/pagination/index.vue"
import vipLow from './components/vipLowList.vue'

const router = useRouter();
const state = reactive({
    loading: false, // table loading
    operationType: 'add', // add || edit
    dialogFormVisible: false,
    tableData: [],
    pageForm: {
        page: 1,
        limit: 20,
        total: 0
    },

    ruleForm: {
        vip_lv: '',//会员等级
        recharge: '',//充值
        bet: '',//下注
        withdraw_num: '',//提现次数
        max_withdraw: '',//最大提现
        pay_fee: '',//付费率
        day_max_withdraw: '',//每日最大提现
        lv_reward_split_day: '',//等级拆分天数
        lv_reward_now_rate: '',//等级立即领取金额
        lv_reward_split_rate: '',//等级拆分比例

        bet_bonus_rate: '',//立即反水比例
        bet_bonus_split_day: '',//立即反水拆分天数
        bet_bonus_now_rate: '',//立即反水立即领取比例
        bet_bonus_split_rate: '',//立即反水拆分比例
        bet_bonus_save_time: '',//立即反水保留时间（单位天）

        day_bet_bonus_rate: '',//日打码反水比例
        day_bet_bonus_split_day: '',//日打码反水拆分天数
        day_bet_bonus_now_rate: '',//日打码立即领取比例
        day_bet_bonus_split_rate: '',//日打码反水拆分比例
        day_bet_bonus_save_time: '',//日打码保留时间（单位天）

        week_bet_bonus_rate: '',//周打码反水比例
        week_bet_bonus_split_day: '',//周打码反水拆分天数
        week_bet_bonus_now_rate: '',//周打码立即领取比例
        week_bet_bonus_split_rate: '',//周打码反水拆分比例
        week_bet_bonus_save_time: '',//周打码保留时间（单位天）

        month_bet_bonus_rate: '',//月打码反水比例
        month_bet_bonus_split_day: '',//月打码反水拆分天数
        month_bet_bonus_now_rate: '',//月打码立即领取比例
        month_bet_bonus_split_rate: '',//月打码反水拆分比例
        month_bet_bonus_save_time: '',//月打码保留时间（单位天）
    },
    rules: {
        name: [{ required: true, message: '', trigger: 'blur' },],
    },
})
const ruleFormRef = ref<FormInstance>()

// 获取数据
const getData = async () => {
    state.loading = true
    vip_lv_list({}).then(res => {
        state.tableData = res["data"]
    }).finally(() => {
        state.loading = false
    })
}
getData();// 获取数据

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

// 删除
const deleteRow = async (cid: number) => {
    // delete_proxy_post({ aid: aid }).then(res => {
    //   if (res['code'] == 1) getData();// 获取数据
    // })
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
            if (state.operationType == 'edit') requestApi = edit_vip_lv
            requestApi({ ...state.ruleForm }).then(res => {
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
  
<style lang="scss" scoped></style>
  
  