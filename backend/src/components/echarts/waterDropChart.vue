<template>
	<div :id="props.chartBox" v-resize="handleResize" style="width: 100%;height: 350px;"></div>
</template>
  
<script lang="ts" setup>
import { onMounted, reactive, nextTick, watch } from "vue";
import * as echarts from "echarts";
import 'echarts-liquidfill/src/liquidFill.js';

const props = defineProps({
	title: String,
	chartBox: String,
	rate: Number
})

const state = reactive({
	chartBoxEL: '',
})

watch(() => props, (val) => {
	nextTick(() => {
		initWaterDropChart()
	})
}, { deep: true, immediate: true })


// 水滴图
const initWaterDropChart = () => {
	if (state.chartBoxEL) (state.chartBoxEL as any).dispose()
	const chartBox = echarts.init(document.getElementById(props.chartBox) as any);
	state.chartBoxEL = chartBox as any

	var value = props.rate
	var data = [value, value, value, value, value]
	var option = {
		title: {
			text: props.title,
			textStyle: { fontSize: '15', color: '#303133' },
		},
		graphic: [{
			type: 'group',
			left: 'center',
			top: '65%',
			children: [{
				type: 'text',
				z: 100,
				left: '10',
				top: 'middle',
				style: {
					fill: '#fff',
					text: '概率',
					font: '20px Microsoft YaHei'
				}
			}]
		}],
		series: [
			{
				type: 'liquidFill',
				radius: '80%',
				center: ['center', '55%'],
				data: data,
				backgroundStyle: {
					borderWidth: 5,
					borderColor: 'rgba(19, 206, 194, 0.5)',
					color: 'rgb(255,0,255,0.01)'
				},
				label: {
					normal: {
						formatter: (value * 100).toFixed(2) + '%',
						textStyle: {
							fontSize: 50
						}
					}
				}
			}
		]
	}

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
  