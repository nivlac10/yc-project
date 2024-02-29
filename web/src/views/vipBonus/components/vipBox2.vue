<template>
	<div class="vipBox2">
		<div class="title">
			<P v-if="props.data?.id == props.currentId">
				{{ t('vipBonus.nívelanterior') }}
			</P>
			<P v-else-if="props.data?.id == props.nextId">
				{{ t('vipBonus.próximo') }}
			</P>
			<p v-else></p>
			<span :style="{ color: props.data?.color }">{{ props.data?.name }} {{ props.data?.vip_lv == 0 ?
				'' : props.data?.lv }}</span>
		</div>
		<el-progress type="circle" :percentage="props.data?.rate ? props.data?.rate : 0" :color="props.data?.color"
			:stroke-width="store.state.status.isPc ? '20' : '18'" stroke-linecap="dashboard">
			<img :src="props.data?.img" alt="" width="60">
		</el-progress>
		<div class="progressTxt">
			<p :style="`color:${props.data?.color}`">{{ moneyFormat(store.state.user.total_bet) }}</p>
			<span>&nbsp;/&nbsp;{{ moneyFormat(props.data?.need_code_amount) }} </span>
		</div>
		<div class="progressTxtBottomTxt">
			{{ t('vipBonus.deApostasAcumuladas') }}
		</div>
		<div class="vipInfo">
			<p class="vipInfo_title">	{{ t('vipBonus.Limitederetirada') }}</p>
			<div class="vipInfo_item">
				<p>	{{ t('vipBonus.Taxaderetiradarate') }}</p>
				<span>{{ props.data?.pay_fee }}%</span>
			</div>
			<div class="vipInfo_item">
				<p>	{{ t('vipBonus.Limitederetiradadiária') }}</p>
				<span>{{ props.data?.day_max_withdraw }}</span>
			</div>
			<div class="vipInfo_item">
				<p>	{{ t('vipBonus.Vezesderetiradadiária') }}</p>
				<span>{{ props.data?.withdraw_num }}</span>
			</div>
			<div class="Line"></div>
			<p class="vipInfo_bottom">	{{ t('vipBonus.BônusdeNívelApostadeUpgrade') }}0,2%</p>
		</div>

		<div class="bottom" @click="get_bonus()">
			<div
				:class="{ btn: true, sl_box_shadow: props.data?.state !== 2, btn_f: props.data?.state == 2, btnMask: props.data?.state == 0 }">
				<img v-if="props.data?.state !== 2" src="../../../assets/images/refer/RETIRADA.png" alt="">
				<!-- <img v-if="props.data?.state !== 1" src="../../../assets/images/header/RETIRADA@2x.png" alt=""> -->
				<p>{{ props.data?.state == 2 ? t('btnName.Concluir') : t('btnName.Receber') }} {{ moneyFormat(props.data?.bonus) }}</p>
			</div>
		</div>
		<el-dialog v-model="state.isBonusPop" :append-to-body="true">
			<div v-if="state.isBonusPop" class="bounsPop_box  mask" @click="state.isBonusPop = false">
				<div class="pop_box" @click.stop>
					<bounsPop :comIdx="5" :now_bonus="state.now_bonus_pop" :split_bonus="state.split_bonus_pop"
						@close-pop="state.isBonusPop = false"></bounsPop>
				</div>
			</div>
		</el-dialog>
	</div>
</template>

<script setup lang="ts">
import {
	defineEmits,
	reactive
} from "vue";
import { store } from '@/store';
import { VipService } from "@/api/vip";
import { getUserInfoNoLoad, moneyFormat } from "@/utils/baseFun";
import bounsPop from '@/views/vipBonus/components/bounsPop.vue';
import { useI18n } from "vue-i18n";

const {t} = useI18n();
const state = reactive({
	now_bonus_pop: 0,
	split_bonus_pop: 0,
	isBonusPop: false,
	lvIndex: 0,
	currentId: 0,
	nextId: 0,
})
const props = defineProps({
	data: {
		type: Object
	},
	currentId: {
		type: Number,
		default: 0
	},
	nextId: {
		type: Number,
		default: 0
	}
})

// console.log(props.data2);

// console.log(state.nextId, state.currentId);
const emit = defineEmits(['def'])
// let percentage = props.data?.bet /

const get_bonus = () => {
	if (props.data?.state == 1) {
		VipService.user_get_vip_up_bonus({ id: props.data.id }).then((res) => {
			// console.log(res);
			if (res.data.code == 1) {
				emit('def')
				getUserInfoNoLoad()
				state.isBonusPop = true
				state.now_bonus_pop = res.data.bonus
				state.split_bonus_pop = res.data.split_bonus
			}
		})
	}
}

</script>

<style scoped lang="scss">
.bounsPop_box {
	display: flex !important;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	width: 100%;
	height: 100%;

	.pop_box {
		position: relative;
	}
}


.btnMask {
	position: relative;
}

.btnMask::after {
	content: "";
	cursor: pointer;
	background: rgba(5, 5, 5, 0.432);
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	z-index: 2;
	// left: 0;
	// top: 0;
	// border: 1px solid;
	border-radius: 12px;
}

.sl_box_shadow {
	p {
		color: #000 !important;

	}
}

.vipBox2 {
	width: 100%;
	background: #2F3445;
	border-radius: 16px;
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 24px 12px;
	box-sizing: border-box;

	.title {
		display: flex;
		flex-direction: column;
		align-items: center;
		// margin-bottom: 22px;
		gap: 10px;

		p {
			color: #B2B6C5;
			font-size: 16px;
			font-weight: bold;
			// margin-bottom: 14px;
			height: 16px;
		}

		span {
			font-weight: bold;
			font-size: 14px;
			color: #D8A791;
		}
	}

	.progressTxt {
		display: flex;
		align-items: center;
		margin: 14px 0 2px 0;
		font-size: 14px;

		p {
			color: #E0A685;
		}

		span {
			color: #B2B6C5;
		}
	}

	.progressTxtBottomTxt {
		color: #fff;
		font-size: 14px;
		margin-top: 4px;
		margin-bottom: 6px;
	}

	.vipInfo {
		box-sizing: border-box;
		padding: 15px 15px 18px 15px;
		width: 100%;
		background: #3C4256;
		border-radius: 9.25px;
		column-gap: 13px;

		.vipInfo_title {
			color: #F3B343;
			font-size: 14px;

		}

		div {
			margin-top: 13px;
		}

		.vipInfo_item {
			display: flex;
			align-items: center;
			color: #B2B6C5;
			justify-content: space-between;
			font-size: 14px;

			p {
				color: #B2B6C5;
			}
		}

		.Line {
			width: 100%;
			border: 1px dashed #666D79;
		}

		.vipInfo_bottom {
			color: #B2B6C5;
			font-size: 14px;
			text-align: center;
			margin-top: 12px;
		}
	}

	.bottom {
		margin-top: 16px;

		.btn {
			cursor: pointer;
			display: flex;
			align-items: center;
			justify-content: center;
			padding: 14px 33px 17px 20px;
			border-radius: 12px;

			&.btn_f {
				.sl_box_shadow {
					background: transparent !important;
					box-shadow: none;
					color: #B2B6C5;

					div {
						img {
							display: none;
						}
					}
				}
			}

			p {
				color: #B2B6C5;
				font-size: 16px;
				font-weight: bold;
			}

			img {
				width: 20px;
				margin-right: 8px;
			}
		}

	}
}

:deep(.el-progress-circle__track) {
	stroke: #3A3E4B !important;
}

:deep(.el-progress--circle, .el-progress--dashboard) {
	width: 162px;
	height: 162px;
	margin: 0;
	display: flex;
	justify-content: center;
}



@media (max-width: 768px) {
	:deep(.el-progress--circle, .el-progress--dashboard) {
		width: 140px;
		height: 140px;
	}

	.btnMask::after {
		// border-radius: 6px;

	}

	.vipBox2 {
		border-radius: 12px;
		padding: 24px 12px 20px 13px;

		.title {
			p {
				font-size: 14px;
			}

			span {
				font-size: 16px;
			}
		}

		.vipInfo {
			font-size: 12px;

			.vipInfo_item {
				font-size: 12px;
			}

			.vipInfo_bottom {
				font-size: 12px;
			}
		}

		.bottom {
			.btn {
				// border-radius: 6px;

				img {
					width: 18.75px;
				}

				p {
					// color: #1B1D29;
					font-size: 15px;
				}
			}
		}
	}
}
</style>