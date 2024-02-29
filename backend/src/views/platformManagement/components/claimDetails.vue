<template>
	<div class="app-container">
		<el-dialog v-model="state.dialogFormVisible" title="领取记录" :draggable="true" @close="closeChange">
			<el-input v-model="state.pageForm.uid" placeholder="用户ID：搜索多个用 , 隔开" style="width: 100%;" />
			<div style="display: flex;align-items: center;gap: 10px;padding: 10px 0;">
				<datetime @def="timeChange" />
				<el-button type="primary" @click="searchData">搜索</el-button>
			</div>
			<div style="margin-bottom: 10px;">
				<el-button type="success">领取金额：{{ state.total_money }}</el-button>
			</div>
			<el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
				<el-table-column prop="uid" label="用户ID" header-align="center" :align="'center'" sortable />
				<el-table-column prop="recharge_activity_name" label="活动名称" header-align="center" :align="'center'" />
				<el-table-column prop="recharge_money" label="充值金额" header-align="center" :align="'center'" />
				<el-table-column prop="send_amount" label="赠送金额" header-align="center" :align="'center'" />
				<el-table-column prop="add_time" label="领取时间" header-align="center" :align="'center'" sortable />
			</el-table>
			<div class="pager-wrapper">
				<pagination :pageForm="state.pageForm" @def="getData" />
			</div>
		</el-dialog>
	</div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import { recharge_activity_log_list_post } from "@/api/platformManagement";
import { resetRouter } from "@/router";
import pagination from "@/components/pagination/index.vue"
import datetime from "@/components/datetime/index.vue"
const router = useRouter();
const props = defineProps({
	recharge_activity_id: Number
})

const emit = defineEmits(["showClaimDetails"])

const state = reactive({
	loading: false, // table loading
	operationType: 'add', // add || edit
	dialogFormVisible: true,
	pay_money_list: [],
	type_list: [],
	timeArr: '',
	pageForm: {
		limit: 20,
		page: 1,
		total: 0,
		uid: '',
		recharge_activity_id: props.recharge_activity_id,
		stime: '',
		etime: ''
	},
	tableData: [],
	total_money: 0,
})

// 获取数据
const getData = async () => {
	state.loading = true
	state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
	state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
	recharge_activity_log_list_post({ ...state.pageForm }).then(res => {
		if (res.code == 1) {
			state.tableData = res.data
			state.total_money = res.total_money
			state.pageForm.total = res.count
			state.loading = false
		}
	}).catch(() => {
		state.loading = false
	})
}
getData();// 获取数据

const timeChange = (time) => {
	state.timeArr = time
	getData()
}

const searchData = () => {
	getData()
}

const closeChange = () => {
	state.dialogFormVisible = false
	emit('showClaimDetails', state.dialogFormVisible)
}

</script>

<style lang="scss" scoped>
table {
	border-collapse: collapse;
	border-color: #f5f5f5;

	tr {
		td {
			padding: 10px;
		}
	}
}
</style>

