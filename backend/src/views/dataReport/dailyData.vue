<template>
	<div class="">
		<el-card class="box-card box-card-top">
			<div>
				<span>渠道：</span>
				<el-select v-model="state.pageForm.cid" placeholder="渠道">
					<el-option label="全部" value="" />
					<el-option v-for="item in agent_list" :key="item.cid" :label="item.username" :value="item.cid" />
				</el-select>
			</div>
			<datetime @def="timeChange" />
			<!-- <el-date-picker v-model="state.searchForm.day" type="date" placeholder="Pick a day" value-format="YYYY-MM-DD" /> -->
			<el-button type="primary" @click="searchData">搜索</el-button>
		</el-card>
		<el-card class="box-card" uno-margin-top>
			<el-table v-loading="state.loading" :data="state.tableData" style="width: 100%" show-summary fixed="left">
				<el-table-column prop="day" label="日期" header-align="center" :align="'center'" sortable width="120px"
					fixed="left" />
				<!-- <el-table-column prop="name" label="安装数" header-align="center" :align="'center'" /> -->
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
				<el-table-column prop="total_game_life" label="当日付费总人数" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="recharge_ratio" label="当日整体付费率" header-align="center" :align="'center'"
					width="130px" />
				<!-- <el-table-column prop="name" label="当日整体付费ARPPU" header-align="center" :align="'center'" />
				<el-table-column prop="name" label="当日整体活跃ARPU" header-align="center" :align="'center'" /> -->
				<el-table-column prop="new_user_recharge" label="新增付费金额" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="new_user_num" label="新增付费人数" header-align="center" :align="'center'" width="130px" />
				<el-table-column prop="new_user_ratio" label="新增付费率" header-align="center" :align="'center'"
					width="130px" />
				<!-- <el-table-column prop="name" label="新增付费ARPPU" header-align="center" :align="'center'" />
				<el-table-column prop="name" label="新增活跃ARPU" header-align="center" :align="'center'" /> -->
				<el-table-column prop="old_user_recharge" label="老用户付费金额" header-align="center" :align="'center'"
					width="130px" />
				<el-table-column prop="old_user_num" label="老用户付费人数" header-align="center" :align="'center'"
					width="130px" />
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
				<el-table-column prop="vip_up" label="VIP晋级" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="vip_week" label="VIP每周" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="vip_month" label="VIP每月" header-align="center" :align="'center'" width="120px" />
				<el-table-column prop="user_rebate" label="VIP返水" header-align="center" :align="'center'" width="120px" />
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
	</div>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance, FormRules } from 'element-plus'
import { storeToRefs } from 'pinia';
import confStore from "@/store/modules/conf";
import { day_data_list_post } from "@/api/dataReport";
import datetime from "@/components/datetime/index.vue"
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
		stime: '',
		etime: '',
	},
})

// 获取数据
const getData = async () => {
	state.loading = true
	state.pageForm.stime = state.timeArr ? state.timeArr[0] : ''
	state.pageForm.etime = state.timeArr ? state.timeArr[1] : ''
	day_data_list_post({ ...state.pageForm }).then(res => {
		state.pageForm.total = res.count
		state.tableData = res.data
		state.loading = false
	})
}

const timeChange = (time) => {
	state.timeArr = time
	getData()
}

const searchData = () => {
	getData()
}
</script>

<style lang="scss" scoped></style>

