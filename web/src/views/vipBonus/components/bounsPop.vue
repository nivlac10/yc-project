<template>
	<div class="bonus_pop">
		<div class="bonus_pop_head">
			<div>{{ moneyFormat(props.now_bonus + props.split_bonus) }}</div>
			<div v-if="props.comIdx == 1">{{t('vipBonus.ReivindicarBônusCashback')}}</div>
			<div v-else-if="props.comIdx == 2">{{t('vipBonus.ReivindicarDiário')}}</div>
			<div v-else-if="props.comIdx == 3">{{t('vipBonus.ReivindicarBônusSemanal')}}</div>
			<div v-else-if="props.comIdx == 4">{{t('vipBonus.ReivindicarMensal')}}</div>
			<div v-else-if="props.comIdx == 5">{{t('vipBonus.ReivindicarNível')}}</div>
		</div>
		<div class="bonus_pop_centent">
			<div class="bonus_pop_centent_box">
				<div class="centent_box_title">
					{{ state.now_rate.toFixed(2) }}% {{ t('vipBonus.AdicionadoConta') }}
				</div>
				<img src="@assets/images/vipBonus/purse.png" alt="">
				<div class="amount">{{ moneyFormat((props.now_bonus)) }}</div>
			</div>
			<div class="bonus_pop_centent_box">
				<div class="centent_box_title">
					{{ state.split_rate.toFixed(2) }}% {{t('vipBonus.AdicionadoaoCalendário')}}
				</div>
				<img src="@assets/images/vipBonus/calendar.png" alt="">
				<div class="amount">{{ moneyFormat((props.split_bonus)) }}</div>
			</div>
		</div>
		<div class="bonus_pop_rules">
			<div v-if="props.comIdx == 1">
				{{ t('vipBonus.vipBoxPopTxt') }}
			</div>
			<div v-else-if="props.comIdx == 2">
				{{ t('vipBonus.vipBoxPopTxt2') }}
			</div>
			<div v-else-if="props.comIdx == 3">
				{{ t('vipBonus.vipBoxPopTxt3') }}

			</div>
			<div v-else-if="props.comIdx == 4">
				{{ t('vipBonus.vipBoxPopTxt4') }}
			
			</div>
			<div v-else-if="props.comIdx == 5">
				{{ t('vipBonus.vipBoxPopTxt5') }}

			</div>
		</div>
		<div class="bonus_pop_btn" @click="emit('closePop')">{{ t('btnName.Confirmar') }}</div>
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from "vue";
import * as echarts from "echarts";
import { defineEmits } from 'vue'
import { moneyFormat } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
const { t } = useI18n();
const props = defineProps({
	comIdx: {
		type: Number,
		default: 0
	},
	now_bonus: {
		type: Number,
		default: 0
	},
	split_bonus: {
		type: Number,
		default: 0
	}
})
const state = reactive({
	now_rate: 0,
	split_rate: 0
})
// 定义派发事件
const emit = defineEmits(['closePop'])

// function init() {
//     // 基于准备好的dom，初始化echarts实例
//     var myChart = echarts.init(document.getElementById('main'));
//     // 指定图表的配置项和数据
//     let option = {


//         series: [
//             {
//                 name: 'Access From',
//                 type: 'pie',
//                 radius: ['60%', '75%'],
//                 avoidLabelOverlap: false,
//                 itemStyle: {
//                     // borderRadius: 10,
//                     borderColor: '#404958',
//                     borderWidth: 4
//                 },
//                 color: ['#4FD112', '#F8BF2E'],
//                 label: {
//                     show: false,
//                     position: 'center'
//                 },
//                 emphasis: {
//                     label: {
//                         show: false,
//                         fontSize: 9,
//                         fontWeight: 'bold'
//                     }
//                 },
//                 labelLine: {
//                     show: false
//                 },
//                 data: [

//                     { value: props.now_bonus, name: 'Union Ads' },
//                     { value: props.split_bonus, name: 'Video Ads2' },

//                 ]
//             }
//         ]
//     };
//     // 使用刚指定的配置项和数据显示图表。
//     myChart.setOption(option);
// }

onMounted(() => {
	// init();
	let total_bonus = props.now_bonus + props.split_bonus
	let rate_num = total_bonus / 100
	state.now_rate = props.now_bonus / rate_num
	state.split_rate = props.split_bonus / rate_num

})

</script>

<style scoped lang="scss">
.bonus_pop {
	width: 453px;
	padding: 32px 23px 50px 23px;
	background: #202330;
	box-sizing: border-box;
	border-radius: 12px;

	.bonus_pop_head {
		margin-bottom: 20px;
		padding: 30px 0 23px 0;
		border-radius: 10px;
		border: 1px solid rgba(178, 182, 197, 0.3);
		text-align: center;
		color: #FFFFFF;
		font-weight: 600;

		div:nth-child(1) {
			margin-bottom: 22px;
			font-size: 22px;
		}

		div:nth-child(2) {
			font-size: 18px;
		}
	}

	.bonus_pop_centent {
		margin-bottom: 27px;

		.bonus_pop_centent_box {
			position: relative;
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 9px 17px 9px 11px;
			border-radius: 10px;
			border: 1px solid rgba(178, 182, 197, 0.3);

			&:nth-child(1) {
				margin-bottom: 22px;
			}

			&:nth-child(2) {
				.amount {
					color: #F8BF2E;
				}
			}

			.centent_box_title {
				position: absolute;
				top: 0;
				left: 14px;
				transform: translate(0%, -50%);
				font-size: 16px;
				font-weight: 400;
				color: #B2B6C5;
				background: #202330;
				padding: 0 2px;
			}

			img {
				width: 42px;
			}

			.amount {
				font-size: 20px;
				font-weight: 400;
				color: #82F44E;
			}
		}
	}

	.bonus_pop_rules {
		margin-bottom: 38px;
		font-size: 16px;
		color: #B2B6C5;
		line-height: 19px;
		div{
			white-space: pre-wrap;
		}
	}

	.bonus_pop_btn {
		cursor: pointer;
		height: 54px;
		line-height: 54px;
		text-align: center;
		font-size: 22px;
		font-weight: 600;
		color: #FFFFFF;
		background: #4181EE;
		border-radius: 30px;
	}
}

@media (max-width: 768px) {
	.bonus_pop {
		width: 335px;
		padding: 24px 17px 36px 17px;

		.bonus_pop_head {
			margin-bottom: 20px;
			padding: 30px 0 23px 0;
			border-radius: 8px;

			div:nth-child(1) {
				margin-bottom: 16px;
				font-size: 16px;
			}

			div:nth-child(2) {
				font-size: 14px;
			}
		}

		.bonus_pop_centent {
			margin-bottom: 19px;

			.bonus_pop_centent_box {
				padding: 7px 13px 7px 7px;
				border-radius: 8px;

				&:nth-child(1) {
					margin-bottom: 16px;
				}

				.centent_box_title {
					left: 9px;
					font-size: 12px;
				}

				img {
					width: 32px;
				}

				.amount {
					font-size: 16px;
				}
			}
		}

		.bonus_pop_rules {
			margin-bottom: 35px;
			font-size: 12px;
			line-height: 14px;
		}

		.bonus_pop_btn {
			height: 40px;
			line-height: 40px;
			font-size: 16px;
			border-radius: 22px;
		}
	}
}
</style>