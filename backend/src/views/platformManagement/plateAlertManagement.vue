<template>
    <div class="app-container">
        <el-card class="box-card">
            <el-button type="primary" @click="editRow('add')">添加</el-button>
        </el-card>
        <el-card class="box-card" uno-margin-top>
            <el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
                <el-table-column prop="id" label="ID" header-align="center" :align="'center'" sortable />
                <el-table-column prop="img_url" label="活动图片" header-align="center" :align="'center'" width="150">
                    <template #default="scope">
                        <el-image :src="scope.row.img_url" :zoom-rate="1.2" :preview-src-list="[scope.row.icon_url]"
                            :initial-index="4" fit="cover" preview-teleported />
                    </template>
                </el-table-column>
                <el-table-column prop="type" label="跳转目标" header-align="center" :align="'center'"
                    :formatter="typeFormatter" />
                <el-table-column prop="url" label="1/支付弹窗/路由/网址" header-align="center" :align="'center'" />
                <el-table-column prop="close_type" label="关闭类型" header-align="center" :align="'center'" sortable>
                    <template #default="scope">
                        {{ scope.row.close_type == 0 ? '刷新弹窗' : '关闭隔日弹' }}
                    </template>
                </el-table-column>
                <el-table-column prop="user_type" label="用户类型" header-align="center" :align="'center'" sortable>
                    <template #default="scope">
                        {{ scope.row.user_type == 0 ? '全体用户' : '未充值用户' }}
                    </template>
                </el-table-column>
                <el-table-column prop="sort_index" label="排序" header-align="center" :align="'center'" sortable />
                <el-table-column prop="add_time" label="时间" header-align="center" :align="'center'" sortable width="100" />
                <el-table-column fixed="right" label="操作" header-align="center" :align="'center'" width="230">
                    <template #default="scope">
                        <el-button type="primary" @click="editRow('edit', scope.row)">编辑</el-button>
                        <el-button type="warning" @click="setStatus(scope.row)">{{ scope.row.status == 0 ? '激活' : '禁用'
                        }}</el-button>
                        <popconfirm @confirmClick="deleteRow(scope.row.id)" />
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
            <el-form ref="ruleFormRef" :model="state.ruleForm" :rules="state.rules" label-width="120px"
                class="demo-ruleForm" status-icon>
                <el-form-item label="图片" prop="img_url">
                    <img-upload :img="state.ruleForm.img_url ? state.ruleForm.img_url : ''" @getImgData="get_img_url" />
                </el-form-item>
                <el-form-item label="跳转目标" prop="type">
                    <el-select v-model="state.ruleForm.type" class="m-2" placeholder="Select">
                        <el-option v-for="item in state.jumpTargetList" :key="item.label" :label="item.label"
                            :value="item.val" />
                    </el-select>
                </el-form-item>
                <el-form-item label="跳转地址" prop="url">
                    <el-input v-model="state.ruleForm.url" />
                    <div>(窗口跳转 1 支付弹窗 或者路由 例如代理页面：/Refer)</div>
                </el-form-item>
                <el-form-item label="关闭类型" prop="url">
                    <el-select v-model="state.ruleForm.close_type" class="m-2" placeholder="Select">
                        <el-option v-for="item in state.closeList" :key="item" :label="item.label" :value="item.val" />
                    </el-select>
                </el-form-item>
                <el-form-item label="用户类型" prop="url">
                    <el-select v-model="state.ruleForm.user_type" class="m-2" placeholder="Select">
                        <el-option v-for="item in state.userList" :key="item" :label="item.label" :value="item.val" />
                    </el-select>
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
import { plate_alert_list_post, add_plate_alert_post, detail_plate_alert_post, update_plate_alert_status_post, delete_plate_alert_post } from "../../api/platformManagement";
import imgUpload from "@/components/imgUpload/index.vue"
import confStore from "@/store/modules/conf";
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
    closeList: [
        { val: 0, label: '刷新弹窗' },
        { val: 1, label: '关闭隔日弹' },
    ],
    userList: [
        { val: 0, label: '全体用户' },
        { val: 1, label: '未充值用户' },
    ],
    ruleForm: {
        img_url: null, // 图片
        type: null, //  0无 1窗口跳转 2游戏 3内部网页 4外部网页
        url: null, // 窗口（1支付2代理）
        sort_index: null, // 排序
        close_type: null,
        user_type: null,
    },
    rules: {
        img_url: [{ required: true, message: '请上传图片', trigger: 'blur' },],
        type: [{ required: true, message: '', trigger: 'blur' },],
        url: [{ required: true, message: '', trigger: 'blur' },],
        sort_index: [{ required: true, message: '', trigger: 'blur' },],
        close_type: [{ required: true, message: '', trigger: 'blur' },],
        user_type: [{ required: true, message: '', trigger: 'blur' },],
    },
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
    plate_alert_list_post({ ...state.pageForm }).then(res => {
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
    update_plate_alert_status_post({ id: row.id, status: row.status == 1 ? 0 : 1 }).then(res => {
        if (res.code == 1) getData();// 获取数据
    })
}

// 删除
const deleteRow = async (id: number) => {
    delete_plate_alert_post({ id: id }).then(res => {
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
            if (state.operationType == 'add') requestApi = add_plate_alert_post
            else requestApi = detail_plate_alert_post
            // -------
            let data = new FormData();
            for (var i in state.ruleForm) {
                data.append(i, state.ruleForm[i]);
            }
            // -------
            requestApi(data).then(res => {
                if (res.code == 1) {
                    state.ruleForm.img_url = ''
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
  
  