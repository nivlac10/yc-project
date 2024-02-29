<template>
    <br />
    <el-card class="box-card box-card-top">
        <el-select v-model="state.pageForm.vip_lv" class="m-2" placeholder="vip等级" clearable>
            <el-option v-for="item in state.vipList" :label="item['vip_lv']" :value="item['vip_lv']" :key="item" />
        </el-select>
        <el-button type="primary" @click="searchData">搜索</el-button>
    </el-card>

    <!-- 反水打码日志 -->
    <el-card class="box-card" uno-margin-top>
        <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
            <el-table-column prop="id" label="id" header-align="center" :align="'center'" />
            <el-table-column prop="vip_lv" label="vip等级" header-align="center" :align="'center'" />
            <el-table-column prop="lv" label="奖励等级" header-align="center" :align="'center'" sortable />
            <el-table-column prop="bonus" label="奖金" header-align="center" :align="'center'" sortable />
            <el-table-column prop="need_code_amount" label="打码量" header-align="center" :align="'center'" sortable />
            <el-table-column fixed="right" label="操作" header-align="center" :align="'center'">
                <template #default="scope">
                    <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
                </template>
            </el-table-column>
        </el-table>
    </el-card>

    <el-card uno-margin-top>

    </el-card>
    <el-dialog v-model="state.dialogFormVisible" :title="state.operationType == 'add' ? '添加' : '编辑'" :draggable="true">
        <el-form ref="ruleFormRef" :model="state.ruleForm" :rules="state.rules" label-width="120px" class="demo-ruleForm"
            status-icon>
            <el-form-item label="vip等级" prop="vip_lv">
                <el-select v-model="state.ruleForm.vip_lv" class="m-2" placeholder="vip等级" clearable>
                    <el-option v-for="item in state.vipList" :label="item['vip_lv']" :value="item['vip_lv']" :key="item" />
                </el-select>
            </el-form-item>
            <el-form-item label="领取等级" prop="lv">
                <el-input v-model="state.ruleForm.lv" />
            </el-form-item>
            <el-form-item label="打码量" prop="need_code_amount">
                <el-input v-model="state.ruleForm.need_code_amount" />
            </el-form-item>
            <el-form-item label="奖励" prop="bonus">
                <el-input v-model="state.ruleForm.bonus" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm(ruleFormRef)">Create</el-button>
                <el-button @click="cancel">cancel</el-button>
                <!-- <el-button @click="resetForm(ruleFormRef)">Reset</el-button> -->
            </el-form-item>
        </el-form>
    </el-dialog>
</template>
  
<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import { vip_lv_low_list, vip_lv_list, edit_vip_lv_low } from "../../../api/vipsystemManagement";
import datetime from "@/components/datetime/index.vue"
import pagination from "@/components/pagination/index.vue"

const router = useRouter();

const state = reactive({
    loading: false, // table loading
    operationType: 'add', // add || edit
    dialogFormVisible: false,
    agent_list: [], // 渠道列表
    timeArr: '',
    pageForm: {
        page: 1,
        limit: 20,
        total: 0,
        vip_lv: '',
    },
    tableData: [],
    ruleForm: {
        vip_lv: '',
        lv: '',
        bonus: '',
        need_code_amount: '',
    },
    rules: {
        vip_lv: [{ required: true, message: '', trigger: 'blur' },],
        lv: [{ required: true, message: '', trigger: 'blur' },],
        bonus: [{ required: true, message: '', trigger: 'blur' },],
        need_code_amount: [{ required: true, message: '', trigger: 'blur' },],
    },
    vipList: [],
})
const ruleFormRef = ref<FormInstance>()

// 获取选择数据
const getSelectData = () => {
    vip_lv_list({ limit: 999, page: 1 }).then((res: any) => {
        state.vipList = res.data
    })
}
getSelectData()// 获取选择数据


// 获取数据
const getData = async () => {
    state.loading = true
    vip_lv_low_list({ ...state.pageForm }).then(res => {
        // state.pageForm.total = res.count
        state.tableData = res.data
        state.loading = false
    })
}
getData()


// 搜索数据
const searchData = () => {
    getData();// 获取数据
}

// 添加||编辑
const editRow = (type: string, row: any) => {
    resetForm(ruleFormRef.value) // 重置表单
    if (type == 'add') state.operationType = 'add'
    else state.operationType = 'edit'
    state.ruleForm = row
    state.dialogFormVisible = true
}
// 删除
const deleteRow = async (cid: number) => {

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
            if (state.operationType == 'edit')
                edit_vip_lv_low({ ...state.ruleForm }).then(res => {
                    if (res.code == 1) {
                        cancel()
                        getData();// 获取数据
                    }
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
  
  