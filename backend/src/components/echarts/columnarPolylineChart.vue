<template>
	<div :id="props.chartBox" v-resize="handleResize" style="width: 100%;height: 350px;"></div>
</template>
  
<script lang="ts" setup>
import { onMounted, reactive, nextTick, watch } from "vue";
import * as echarts from "echarts";

const props = defineProps({
	title: String,
	chartBox: String,
	yAxisName: Array,
	xAxisLabelList: Array,
	colorList: Array,
	dataList: Array,
	lineSymbolSize: {
		type: String,
		default: 12
	}
})

const state = reactive({
	chartBoxEL: '',
})

watch(() => props, (val) => {
	nextTick(() => {
		initBarChart()
	})
}, { deep: true, immediate: true })

const setSeries = (type: string = 'line', dataObj: any, color: string) => {
	if (type == 'line')
		return {
			name: dataObj.title,
			type: 'line',
			smooth: true,
			showSymbol: true,
			symbol: 'emptyCircle',
			symbolSize: props.lineSymbolSize,
			yAxisIndex: 0,
			// areaStyle: {
			// 	color: new echarts.graphic.LinearGradient(
			// 		0,
			// 		0,
			// 		0,
			// 		1,
			// 		[
			// 			{ offset: 0, color: 'rgba(199, 237, 250,0.5)' },
			// 			{ offset: 1, color: 'rgba(199, 237, 250,0.2)' },
			// 		],
			// 		false
			// 	),
			// },
			itemStyle: {
				color: color,
			},
			data: dataObj.arr,
		}
	else if (type == 'bar') return {
		name: dataObj.title,
		type: 'bar',
		barWidth: 30,
		yAxisIndex: 1,
		itemStyle: {
			color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
				{ offset: 0, color: 'rgba(108,80,243,0.3)' },
				{ offset: 1, color: 'rgba(108,80,243,0)' },
			]),
			//柱状图圆角
			borderRadius: [30, 30, 0, 0],
		},
		data: dataObj.arr,
	}
}

// 柱状图
const initBarChart = () => {

	if (state.chartBoxEL) (state.chartBoxEL as any).dispose()
	const chartBox = echarts.init(document.getElementById(props.chartBox) as any);
	state.chartBoxEL = chartBox as any
	const option = {
		backgroundColor: '',
		title: {
			text: props.title,
			x: 'left',
			textStyle: { fontSize: '15', color: '#303133' },
		},
		tooltip: { trigger: 'axis' },
		legend: { right: 0 },
		grid: { top: 70, right: 80, bottom: 30, left: 80 },
		xAxis: [
			{
				type: 'category',
				data: props.xAxisLabelList,
				boundaryGap: true,
				axisTick: { show: false },
			},
		],
		yAxis: [
			{
				name: props.yAxisName[0],
				nameLocation: 'middle',
				nameTextStyle: { padding: [3, 4, 50, 6] },
				splitLine: { show: true, lineStyle: { type: 'dashed', color: '#f5f5f5' } },
				axisLine: { show: false },
				axisTick: { show: false },
				axisLabel: { color: '#303133', formatter: '{value} ' },
			},
			{
				name: props.yAxisName[1],
				nameLocation: 'middle',
				nameTextStyle: { padding: [50, 4, 5, 6] },
				splitLine: { show: false },
				axisLine: { show: false },
				axisTick: { show: false },
				axisLabel: { color: '#303133', formatter: '{value} ' },
			},
		],
		series: [],
	};
	let seriesArr = []
	for (let i = 0; i < props.dataList.length; i++) {
		const element = props.dataList[i];
		seriesArr.push(setSeries(element['type'], element, props.colorList[i] as any))
	}
	option.series = seriesArr

	chartBox.setOption(option);
};

const handleResize = ({ width, height }) => {
	(state.chartBoxEL as any).resize()
}

</script>
  
<style lang="scss" scoped>
.center {
	height: 100%;
}
</style>
  