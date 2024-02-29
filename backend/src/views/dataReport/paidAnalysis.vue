<template>
	<div class="app-container">
		<el-card class="box-card box-card-top">
			<el-select v-model="state.pageForm.cid" class="m-2" placeholder="请选择">
				<el-option label="所有渠道" value=""></el-option>
				<el-option v-for="item in state.agent_list" :key="item['cid']" :label="item['username']"
					:value="item['cid']" />
			</el-select>
			<datetime @def="timeChange" />
			<el-button type="primary" @click="searchData">搜索</el-button>
		</el-card>
		<el-card class="box-card" uno-margin-top>
			<el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary>
				<el-table-column prop="day" label="日期" header-align="center" :align="'center'" width="120px" fixed="left" />
				<el-table-column prop="user_num" label="注册数" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d1" label="第一天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d2" label="第二天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d3" label="第三天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d4" label="第四天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d5" label="第五天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d6" label="第六天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d7" label="第七天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d8" label="第八天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d9" label="第九天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d10" label="第十天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d11" label="第十一天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d12" label="第十二天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d13" label="第十三天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d14" label="第十四天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d15" label="第十五天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d16" label="第十六天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d17" label="第十七天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d18" label="第十八天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d19" label="第十九天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d20" label="第二十天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d21" label="第二十一天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d22" label="第二十二天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d23" label="第二十三天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d24" label="第二十四天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d25" label="第二十五天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d26" label="第二十六天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d27" label="第二十七天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d28" label="第二十八天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d29" label="第二十九天" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="d30" label="第三十天" header-align="center" :align="'center'" width="120px" />
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
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import pagination from "@/components/pagination/index.vue"
import popconfirm from "@/components/popconfirm/index.vue"
import { agent_list_post } from "@/api/channelManagement";
import datetime from "@/components/datetime/index.vue"
import { user_payment_detail_post } from "@/api/dataReport";
import { TableRow } from "element-tiptap";
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
	user_payment_detail_post({ ...state.pageForm }).then(res => {
		state.pageForm.total = res.count
		state.tableData = res.data
		for (let index = 0; index < state.tableData.length; index++) {
			state.tableData[index].d2 = parseFloat(state.tableData[index].d1) + parseFloat(state.tableData[index].d2)
			state.tableData[index].d3 = parseFloat(state.tableData[index].d2) + parseFloat(state.tableData[index].d3)
			state.tableData[index].d4 = parseFloat(state.tableData[index].d3) + parseFloat(state.tableData[index].d4)
			state.tableData[index].d5 = parseFloat(state.tableData[index].d4) + parseFloat(state.tableData[index].d5)
			state.tableData[index].d6 = parseFloat(state.tableData[index].d5) + parseFloat(state.tableData[index].d6)
			state.tableData[index].d7 = parseFloat(state.tableData[index].d6) + parseFloat(state.tableData[index].d7)
			state.tableData[index].d8 = parseFloat(state.tableData[index].d7) + parseFloat(state.tableData[index].d8)
			state.tableData[index].d9 = parseFloat(state.tableData[index].d8) + parseFloat(state.tableData[index].d9)
			state.tableData[index].d10 = parseFloat(state.tableData[index].d9) + parseFloat(state.tableData[index].d10)
			state.tableData[index].d11 = parseFloat(state.tableData[index].d10) + parseFloat(state.tableData[index].d11)
			state.tableData[index].d12 = parseFloat(state.tableData[index].d11) + parseFloat(state.tableData[index].d12)
			state.tableData[index].d13 = parseFloat(state.tableData[index].d12) + parseFloat(state.tableData[index].d13)
			state.tableData[index].d14 = parseFloat(state.tableData[index].d13) + parseFloat(state.tableData[index].d14)
			state.tableData[index].d15 = parseFloat(state.tableData[index].d14) + parseFloat(state.tableData[index].d15)
			state.tableData[index].d20 = parseFloat(state.tableData[index].d15) + parseFloat(state.tableData[index].d20)
			state.tableData[index].d25 = parseFloat(state.tableData[index].d20) + parseFloat(state.tableData[index].d25)
			state.tableData[index].d30 = parseFloat(state.tableData[index].d25) + parseFloat(state.tableData[index].d30)
			state.tableData[index].dother = parseFloat(state.tableData[index].d30) + parseFloat(state.tableData[index].dother)
		}
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
  
  