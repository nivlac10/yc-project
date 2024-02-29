<template>
  <div :id="props.chartBox" v-resize="handleResize" style="width: 100%;height: 350px;"></div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, nextTick, watch } from "vue";
import * as echarts from "echarts";

const props = defineProps({
  title: String,
  chartBox: String,
  yAxisName: String,
  xAxisLabelList: Array,
  colorList: Array,
  dataList: Array,
  lineSymbolSize: {
    type: String,
    default: 6
  }
})

const state = reactive({
  chartBoxEL: '',
})

watch(() => props, (val) => {
  nextTick(() => {
    initLineChart()
  })
}, { deep: true, immediate: true })

const setSeries = (dataObj: any, color: string) => {
  return {
    name: dataObj.title,
    type: 'line',
    symbolSize: props.lineSymbolSize,
    symbol: 'circle',
    smooth: true,
    data: dataObj.arr,
    lineStyle: { color: color },
    itemStyle: { color: color, borderColor: color },
    areaStyle: {
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: `${color}b3` },
        { offset: 1, color: `${color}03` },
      ]),
    }
  }
}

// 折线图
const initLineChart = () => {
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
    grid: { top: 70, right: 20, bottom: 30, left: '7%' },
    tooltip: { trigger: 'axis' },
    legend: { right: 0 },
    xAxis: {
      data: props.xAxisLabelList,
    },
    yAxis: [
      {
        type: 'value',
        name: props.yAxisName,
        splitLine: { show: true, lineStyle: { type: 'dashed', color: '#f5f5f5' } },
      },
    ],
    series: [
    ],
  };

  let seriesArr = []
  for (let i = 0; i < props.dataList.length; i++) {
    const element = props.dataList[i];
    seriesArr.push(setSeries(element, props.colorList[i] as any))
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
