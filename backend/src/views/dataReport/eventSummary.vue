<template>
	<div class="app-container">
		<el-card class="box-card box-card-top">
			<el-select v-model="state.pageForm.cid" class="m-2" placeholder="请选择">
				<el-option label="所有渠道" value=""></el-option>
				<el-option v-for="item in state.agent_list" :key="item['cid']" :label="item['username']" :value="item['cid']" />
			</el-select>
			<datetime @def="timeChange" />
			<el-button type="primary" @click="searchData">搜索</el-button>
		</el-card>
		<el-card class="box-card" uno-margin-top>
			<el-table v-loading="state.loading" :data="state.tableData" style="width: 100%">
				<el-table-column prop="name" label="事件" header-align="center" :align="'center'" />
				<el-table-column prop="num" label="数量" header-align="center" :align="'center'" />
			</el-table>
		</el-card>
		<!-- <el-card uno-margin-top>
			<div class="pager-wrapper">
				<pagination :pageForm="state.pageForm" @def="getData" />
			</div>
		</el-card> -->
	</div>
</template>
  
<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import pagination from "@/components/pagination/index.vue"
import popconfirm from "@/components/popconfirm/index.vue"
import { agent_list_post } from "@/api/channelManagement";
import datetime from "@/components/datetime/index.vue"
import { event_report_total_post } from "@/api/dataReport";
const router = useRouter();
const state = reactive({
	loading: false, // table loading
	agent_list: [],
	timeArr: '',
	tableData: [],
	pageForm: {
		page: 1,
		limit: 20,
		total: 0,
		cid: '',
		stime: '',
		etime: '',
	},
})
const ruleFormRef = ref<FormInstance>()

// 获取选择数据
const getSelectData = () => {
	// 渠道
	agent_list_post({ limit: 999, page: 1 }).then((res: any) => {
		state.agent_list = res.data
	})
}
getSelectData()// 获取选择数据

// 获取数据
const getData = async () => {
	state.loading = true
	event_report_total_post({ ...state.pageForm }).then(res => {
		state.pageForm.total = res.count
		state.tableData = res.data
		state.loading = false
	})
}

const timeChange = (time) => {
	state.timeArr = time
	state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
	state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
	getData()
}

// 搜索数据
const searchData = () => {
	getData()
}
</script>
  
<style lang="scss" scoped></style>
  
  