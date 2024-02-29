<template>
	<div class="date_time_box">
		<div class="time_select_box">
			<el-button size="small" v-for="(v, i) in selectList" @click="btnClick(v.datetype, v.dateset)">{{ v.label
			}}</el-button>
		</div>
		<div class="time_change">
			<el-button @click="btnClick('-1', 0)">前一天</el-button>
			<el-date-picker v-model="timeArr" type="datetimerange" :shortcuts="shortcuts" range-separator="To"
				start-placeholder="Start date" end-placeholder="End date" value-format="YYYY-MM-DD" @blur="changeTime" />
			<el-button @click="btnClick('+1', 0)">后一天</el-button>
		</div>
	</div>
</template>
<script lang="ts">
import { search_btn } from "@/api/adminHome";
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
export default defineComponent({
	name: "index",
	props: {
		time: {
			type: Array
		},
	},
	setup(props, { emit }) {
		//1、 得到今天、昨天、明天日期
		// dates为数字类型，0代表今日,-1代表昨日，1代表明日，返回yyyy-mm-dd格式字符串，dates不传默认代表今日。
		const getDate = (dates) => {
			var dd = new Date();
			var n = dates || 0;
			dd.setDate(dd.getDate() + n);
			var y = dd.getFullYear();
			var m: any = dd.getMonth() + 1;
			var d: any = dd.getDate();
			m = m < 10 ? "0" + m : m;
			d = d < 10 ? "0" + d : d;
			var day = y + "-" + m + "-" + d;
			return day;
		}
		const state = reactive({
			timeArr: '',
			selectList: [
				{ label: '今日', datetype: 0, dateset: 1 },
				{ label: '昨日', datetype: 0, dateset: 2 },
				{ label: '本周', datetype: 0, dateset: 3 },
				{ label: '上周', datetype: 0, dateset: 4 },
				{ label: '本月', datetype: 0, dateset: 5 },
				{ label: '上月', datetype: 0, dateset: 6 },
				{ label: '今年', datetype: 0, dateset: 7 },
				{ label: '去年', datetype: 0, dateset: 9 },
				{ label: '过去7天', datetype: 0, dateset: 10 },
				{ label: '过去30天', datetype: 0, dateset: 11 },
				{ label: '全部', datetype: 0, dateset: 8 },
			],
			form: {
				start_time: getDate(0),
				end_time: getDate(0),
				datetype: 0,
				dateset: 0,
			}
		});
		const btnClick = (datetype, dateset) => {
			state.form.datetype = datetype
			state.form.dateset = dateset
			search_btn({ ...state.form }).then(res => {
				state.timeArr = [res.start_day, res.end_day] as any
				changeTime(state.timeArr)
			})
		}
		btnClick(0, 1)

		const shortcuts = [
			{
				text: 'Last week',
				value: () => {
					const end = new Date()
					const start = new Date()
					start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
					return [start, end]
				},
			},
			{
				text: 'Last month',
				value: () => {
					const end = new Date()
					const start = new Date()
					start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
					return [start, end]
				},
			},
			{
				text: 'Last 3 months',
				value: () => {
					const end = new Date()
					const start = new Date()
					start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
					return [start, end]
				},
			},
		]
		const changeTime = (val) => {
			emit("def", state.timeArr)
		}
		return { ...toRefs(state), shortcuts, changeTime, props, btnClick };

	},
});
</script>
<style  lang="scss" scoped>
.time_change {
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 10px;
}

.date_time_box {
	display: flex;
	flex-direction: column;
	gap: 10px;
}

.time_select_box {
	display: flex;
	flex-wrap: wrap;
	gap: 5px;
}
</style>
  