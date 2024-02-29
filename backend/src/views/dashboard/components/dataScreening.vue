<template>
	<div class="">
		<el-card class="box-card box-card-top">
			<div>
				<span>渠道：</span>
				<el-select v-model="state.pageForm.cid" placeholder="渠道">
					<el-option label="全部" value="" />
					<el-option v-for="item in agent_list" :key="item.cid" :label="item.username" :value="item.cid" />
				</el-select>
				<el-checkbox v-model="state.pageForm.is_show" style="padding-left: 10px;width: 10%;">显示所有渠道</el-checkbox>
				<!-- <el-date-picker v-model="state.searchForm.day" type="date" placeholder="Pick a day" value-format="YYYY-MM-DD" /> -->
			</div>
			<datetime @def="timeChange" />
			<el-button type="primary" @click="searchData">搜索</el-button>
			<el-button type="primary" @click="exportData" v-permission="['1']">导出Exel</el-button>

		</el-card>
		<el-card class="box-card" uno-margin-top>
			<el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary
				:summary-method="getSummaries" fixed="left">
				<el-table-column prop="day" label="日期" header-align="center" :align="'center'" sortable width="120px"
					fixed="left" />
				<!-- <el-table-column prop="name" label="安装数" header-align="center" :align="'center'" /> -->
				<el-table-column prop="username" label="渠道" header-align="center" :align="'center'" width="120px"
					v-if="state.cid_show">
					<template #default="scope">
						{{ scope.row.username }}({{ scope.row.cid }})
					</template>
				</el-table-column>
				<el-table-column prop="user_total_money" label="用户总余额" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="user_num" label="新增注册用户" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="old_user_life" label="老用户日活" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="totals_num" label="总用户日活" header-align="center" :align="'center'" width="120px" />
				<!-- <el-table-column prop="name" label="注册率" header-align="center" :align="'center'" /> -->
				<el-table-column prop="game_num" label="总玩家日活" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="new_game_num" label="新玩家日活" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="old_game_num" label="老玩家日活" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="recharge_money" label="当日付费总额" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="recharge_fee" label="充值手续费" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="total_user_num" label="当日付费总人数" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="user_avg_money" label="当日人均付费金额" header-align="center" :align="'center'"
					width="150px" />
				<el-table-column prop="recharge_ratio" label="当日整体付费率" header-align="center" :align="'center'"
					width="130px" />
				<!-- <el-table-column prop="name" label="当日整体付费ARPPU" header-align="center" :align="'center'" />
				<el-table-column prop="name" label="当日整体活跃ARPU" header-align="center" :align="'center'" /> -->
				<el-table-column prop="new_user_recharge" label="新增付费金额" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="new_user_num" label="新增付费人数" header-align="center" :align="'center'" width="130px" />
				<el-table-column prop="new_user_avg_money" label="新增人均付费金额" header-align="center" :align="'center'"
					width="150px" />
				<el-table-column prop="new_user_ratio" label="新增付费率" header-align="center" :align="'center'"
					width="130px" />
				<!-- <el-table-column prop="name" label="新增付费ARPPU" header-align="center" :align="'center'" />
				<el-table-column prop="name" label="新增活跃ARPU" header-align="center" :align="'center'" /> -->
				<el-table-column prop="old_user_recharge" label="老用户付费金额" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="old_user_num" label="老用户付费人数" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="old_user_avg_money" label="老用户人均付费金额" header-align="center" :align="'center'"
					width="150px" />
				<el-table-column prop="old_user_ratio" label="老用户付费率" header-align="center" :align="'center'"
					width="130px" />
				<!-- <el-table-column prop="name" label="老用户付费ARPPU" header-align="center" :align="'center'" />
				<el-table-column prop="name" label="老用户活跃ARPU" header-align="center" :align="'center'" /> -->
				<el-table-column prop="new_user_withdraw_num" label="新增提现人数" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="old_user_withdraw_num" label="老用户提现人数" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="total_withdraw_num" label="当日提现总人数" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="new_user_withdraw" label="新增提现金额" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="old_user_withdraw" label="老用户提现金额" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="withdraw_money" label="当日提现总额" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="withdraw_fee" label="提现手续费" header-align="center" :align="'center'" width="130px" />
				<el-table-column prop="new_r_w" label="新用户充提差" header-align="center" :align="'center'" width="130px" />
				<el-table-column prop="old_r_w" label="老用户充提差" header-align="center" :align="'center'" width="130px" />
				<el-table-column prop="total_r_w" label="当日总充提差" header-align="center" :align="'center'" width="130px" />
				<el-table-column prop="new_w_ratio" label="新用户提现率" header-align="center" :align="'center'" width="130px" />
				<el-table-column prop="old_w_ratio" label="老用户提现率" header-align="center" :align="'center'" width="130px" />
				<el-table-column prop="total_w_ratio" label="整体提现率" header-align="center" :align="'center'" width="130px" />
				<el-table-column prop="total_give_money" label="赠送金额" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="recharge_achieve" label="充值成就" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="vip_up" label="VIP晋级" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="vip_now" label="VIP立即返水" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="vip_split" label="vip拆分返水" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="vip_day" label="VIP每日" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="vip_week" label="VIP每周" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="vip_month" label="VIP每月" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="roller_money" label="转轮赠送" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="download_bonus" label="下载奖励" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="sign_bonus" label="用户签到" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="loss_bonus" label="用户破产补助" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="user_rebate" label="用户返水" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="give_code_money" label="兑换码赠送" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="user_first_recharge" label="用户首充" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="user_day_first_recharge" label="用户每日首充" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="system_give" label="系统赠送" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="total_brokerage_money" label="总佣金" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="first_recharge_brokerage" label="首充佣金" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="invite_task_brokerage" label="任务佣金" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="one_bet_brokerage" label="一级返佣" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="two_bet_brokerage" label="二级返佣" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="three_bet_brokerage" label="三级返佣" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="total_bet" label="总押" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="total_shu_ying" label="总赢" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="total_cover_charge" label="游戏抽水" header-align="center" :align="'center'"
					width="120px" />
				<el-table-column prop="total_real_shu_ying" label="用户输赢" header-align="center" :align="'center'"
					width="120px" />
			</el-table>
		</el-card>
		<el-card uno-margin-top>
			<div class="pager-wrapper">
				<pagination :pageForm="state.pageForm" @def="getData" />
			</div>
		</el-card>
		<el-dialog v-model="state.dialogFormVisible" title="数据导出选择字段" :draggable="true">

			<el-form ref="ruleFormRef" label-width="20px" class="demo-ruleForm" status-icon>
				<el-form-item>
					<el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllChange">全选
					</el-checkbox>

				</el-form-item>
				<el-form-item>
					<el-checkbox-group v-model="checkedCities" @change="handleCheckedCitiesChange">
						<el-checkbox v-for="city in cities" :key="city.val" :label="city.label" class="checkbox_fields">{{
							city.label
						}}</el-checkbox>
					</el-checkbox-group>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="submitForm()">确定</el-button>
					<el-button @click="cancel">取消</el-button>
				</el-form-item>
			</el-form>
		</el-dialog>
	</div>
</template>
  
<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import { ElMessage, FormInstance } from 'element-plus'
import pagination from "@/components/pagination/index.vue"
import popconfirm from "@/components/popconfirm/index.vue"
import { storeToRefs } from 'pinia';
import confStore from "@/store/modules/conf";
import { home_data_post } from "@/api/adminHome";
import datetime from "@/components/datetime/index.vue"
import axios from "axios";
let url = import.meta.env.VITE_BASE_API
const store = confStore();
let { agent_list, factory_list, factory_details_list, external_game_list, gameType } = storeToRefs(store);

const router = useRouter();
const state = reactive({
	loading: false, // table loading
	timeArr: '',
	tableData: [],
	pageForm: {
		page: 1,
		limit: 20,
		total: 0,
		cid: '',
		is_show: false,
		stime: '',
		etime: '',
	},
	dialogFormVisible: false,
	cid_show: true,
	total: [],

})
const checkAll = ref(false)
const isIndeterminate = ref(true)
const checkedCities = ref([])
const cities = [
	{ val: 'day', label: '日期' },
	{ val: 'username', label: '渠道' },
	{ val: 'user_total_money', label: '用户总余额' },
	{ val: 'user_num', label: '新增注册用户' },
	{ val: 'old_user_life', label: '老用户日活' },
	{ val: 'totals_num', label: '总用户日活' },
	{ val: 'game_num', label: '总玩家日活' },
	{ val: 'new_game_num', label: '新玩家日活' },
	{ val: 'old_game_num', label: '老玩家日活' },
	{ val: 'recharge_money', label: '当日付费总额' },
	{ val: 'recharge_fee', label: '充值手续费' },
	{ val: 'total_user_num', label: '当日付费总人数' },
	{ val: 'user_avg_money', label: '当日人均付费金额' },
	{ val: 'recharge_ratio', label: '当日整体付费率' },
	{ val: 'new_user_recharge', label: '新增付费金额' },
	{ val: 'new_user_num', label: '新增付费人数' },
	{ val: 'new_user_avg_money', label: '新增人均付费金额' },
	{ val: 'new_user_ratio', label: '新增付费率' },
	{ val: 'old_user_recharge', label: '老用户付费金额' },
	{ val: 'old_user_num', label: '老用户付费人数' },
	{ val: 'old_user_avg_money', label: '老用户人均付费金额' },
	{ val: 'old_user_ratio', label: '老用户付费率' },
	{ val: 'new_user_withdraw_num', label: '新增提现人数' },
	{ val: 'old_user_withdraw_num', label: '老用户提现人数' },
	{ val: 'total_withdraw_num', label: '当日提现总人数' },
	{ val: 'new_user_withdraw', label: '新增提现金额' },
	{ val: 'old_user_withdraw', label: '老用户提现金额' },
	{ val: 'withdraw_money', label: '当日提现总额' },
	{ val: 'withdraw_fee', label: '提现手续费' },
	{ val: 'new_r_w', label: '新用户充提差' },
	{ val: 'old_r_w', label: '老用户充提差' },
	{ val: 'total_r_w', label: '当日总充提差' },
	{ val: 'new_w_ratio', label: '新用户提现率' },
	{ val: 'old_w_ratio', label: '老用户提现率' },
	{ val: 'total_w_ratio', label: '整体提现率' },
	{ val: 'total_give_money', label: '赠送金额' },
	{ val: 'recharge_achieve', label: '充值成就' },
	{ val: 'vip_up', label: 'VIP晋级' },
	{ val: 'vip_now', label: 'VIP立即返水' },
	{ val: 'vip_split', label: 'vip拆分返水' },
	{ val: 'vip_day', label: 'VIP每日' },
	{ val: 'vip_week', label: 'VIP每周' },
	{ val: 'vip_month', label: 'VIP每月' },
	{ val: 'roller_money', label: '转轮赠送' },
	{ val: 'download_bonus', label: '下载奖励' },
	{ val: 'sign_bonus', label: '用户签到' },
	{ val: 'loss_bonus', label: '用户破产补助' },
	{ val: 'user_rebate', label: '用户返水' },
	{ val: 'give_code_money', label: '兑换码赠送' },
	{ val: 'user_first_recharge', label: '用户首充' },
	{ val: 'user_day_first_recharge', label: '用户每日首充' },
	{ val: 'system_give', label: '系统赠送' },
	{ val: 'total_brokerage_money', label: '总佣金' },
	{ val: 'first_recharge_brokerage', label: '首充佣金' },
	{ val: 'invite_task_brokerage', label: '任务佣金' },
	{ val: 'one_bet_brokerage', label: '一级返佣' },
	{ val: 'two_bet_brokerage', label: '二级返佣' },
	{ val: 'three_bet_brokerage', label: '三级返佣' },
	{ val: 'total_bet', label: '总押' },
	{ val: 'total_shu_ying', label: '总赢' },
	{ val: 'total_cover_charge', label: '游戏抽水' },
	{ val: 'total_real_shu_ying', label: '用户输赢' }
]


const handleCheckAllChange = (val: boolean) => {
	if (val) {
		const arr = []
		for (let i = 0; i < cities.length; i++) {
			arr[i] = cities[i].label
		}
		checkedCities.value = arr
	} else {
		checkedCities.value = []
	}
	// checkedCities.value = val ? cities : []
	isIndeterminate.value = false
}
const handleCheckedCitiesChange = (value: string[]) => {
	const checkedCount = value.length
	checkAll.value = checkedCount === cities.length
	isIndeterminate.value = checkedCount > 0 && checkedCount < cities.length
}


const ruleFormRef = ref<FormInstance>()
// 获取数据
const getData = async () => {
	state.loading = true
	state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
	state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
	home_data_post({ ...state.pageForm }).then(res => {
		console.log(res);
		
		if (state.pageForm.is_show) state.cid_show = true
		else state.cid_show = false
		state.pageForm.total = res.count
		state.total = res.total
		state.tableData = res.data
		state.loading = false
	})
}

const exportData = () => {

	state.dialogFormVisible = true,

		checkAll.value = true,
		handleCheckAllChange(true)

	// window.location.href = url + "/export_home_data_post?cid=" + state.pageForm.cid + "&is_show=" + state.pageForm.is_show + "&stime=" + state.pageForm.stime + "&etime=" + state.pageForm.etime;
	// state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
	// state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
	// window.location.href = url + "/export_home_data_post?cid=" + state.pageForm.cid + "&is_show=" + state.pageForm.is_show + "&stime=" + state.pageForm.stime + "&etime=" + state.pageForm.etime;
	// axios({
	// 	method: 'get',
	// 	url: url + '/export_home_data_post', // 替换为你的 Flask 服务器地址
	// 	responseType: 'blob', // 指定响应数据类型为二进制流
	// })
	// 	.then(response => {
	// 		let year = new Date().getFullYear(); //获取当前时间的年份
	// 		let month = new Date().getMonth() + 1; //获取当前时间的月份
	// 		let day = new Date().getDate(); //获取当前时间的天数
	// 		let filename = '数据总览' + year + "-" + month + "-" + day
	// 		const url = window.URL.createObjectURL(new Blob([response.data]));
	// 		const link = document.createElement('a');
	// 		link.href = url;
	// 		link.setAttribute('download', filename + '.xlsx');
	// 		document.body.appendChild(link);
	// 		link.click();
	// 		document.body.removeChild(link);
	// 	})
	// 	.catch(error => {
	// 		console.error('Error downloading Excel file:', error);
	// 	});
}


// 取消
const cancel = () => {
	state.dialogFormVisible = false
}

// 提交表单
const submitForm = () => {
	state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
	state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
	const field_headers_list = []
	let a = 0
	for (let j = 0; j < cities.length; j++) {
		for (let i = 0; i < checkedCities.value.length; i++) {
			if (checkedCities.value[i] == cities[j].label) {
				if (cities[j].label == '渠道' && state.pageForm.is_show != true) { }
				else {
					field_headers_list[a] = cities[j]
					a++
				}
				break;
			}
		}
	}
	// 构建请求参数
	const requestData = {
		cid: state.pageForm.cid,
		is_show: state.pageForm.is_show, // 根据需要设置其他参数
		stime: state.pageForm.stime,
		etime: state.pageForm.etime,
		field_headers_list: JSON.stringify(field_headers_list),
		// 其他参数...
	};

	// 发送 POST 请求
	axios.post(url + '/export_home_data_post', requestData, { responseType: 'blob' })
		.then(response => {
			let year = new Date().getFullYear(); //获取当前时间的年份
			let month = new Date().getMonth() + 1; //获取当前时间的月份
			let day = new Date().getDate(); //获取当前时间的天数
			let filename = '数据总览' + year + "-" + month + "-" + day
			console.log(response.data);

			// 处理成功响应，比如下载文件
			const blob = new Blob([response.data], { type: 'application/octet-stream' });
			const link = document.createElement('a');
			link.href = window.URL.createObjectURL(blob);
			link.download = filename + '.xlsx';
			link.click();
		})
		.catch(error => {
			// 处理错误
			console.error(error);
		});
	// + "&field_headers_list=" + 

	// window.location.href = url + "/export_home_data_post?cid=" + state.pageForm.cid + "&is_show=" + state.pageForm.is_show + "&stime=" + state.pageForm.stime + "&etime=" + state.pageForm.etime;
	state.dialogFormVisible = false
}

const getSummaries = (param) => {
	const { columns, data } = param;
	const sums = [];


	(sums[0] as any) = '合计';
	for (let i = 0; i < cities.length; i++) {
		if (i != 0) {
			if (state.pageForm.is_show == true) {
				(sums[i] as any) = state.total[cities[i].val];
			} else {
				if (cities[i].val != 'username') {
					(sums[i - 1] as any) = state.total[cities[i].val];
				}
			}
			// console.log(cities[i].val, 111);
			// (sums[i] as any) = state.total[cities[i].val];
		}
	}

	return sums
}

const timeChange = (time) => {
	state.timeArr = time
	getData()
}

const searchData = () => {
	getData()
}
</script>
  
<style lang="scss" scoped>
.checkbox_fields {
	width: 120px;
}
</style>
  
  