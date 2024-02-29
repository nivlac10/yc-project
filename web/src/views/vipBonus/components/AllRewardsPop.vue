<template>
	<el-dialog v-model="state.dialogVisible" :show-close="false" :close-on-click-modal="false"
		:close-on-press-escape="false" append-to-body :width="store.state.status.isPc ? '528px' : '100%'">
		<div class="content">
			<div class="pop">
				<div class="title">
					<p>{{ t('vipBonus.TodasasRecompensas') }}</p><img src="@/assets/images/public/Shutdown.png" alt="" @click="closePop">
				</div>
				<div class="body">
					<div class="body_box" v-for="(v, i) in props.dataObj2" :key="i">
						<div class="bodyItem" v-if="v.status == 0">
							<img src="@/assets/images/vipBonus/usable.png" alt="">
							<p> {{ v.bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(v.bonus) }} <span> {{ t('vipBonus.TodasasRecompensas') }} </span>
									{{
										v.unlock_time }} · <span class="green"> {{ t('vipBonus.Disponível') }} </span>
							</p>
						</div>
						<div class="bodyItem" v-else-if="v.status == 1">
							<img src="@/assets/images/vipBonus/Claimed.png" alt="">
							<p>{{ v.bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(v.bonus) }} <span> {{ t('vipBonus.desbloqueadosàs') }}
									</span>
									{{ timeFormatter(v.unlock_time) }} ·<span class="green"> {{ t('vipBonus.Reivindicado') }} </span>
							</p>
						</div>
						<div class="bodyItem" v-else-if="v.status == 2">
							<img src="@/assets/images/vipBonus/unclaimed.png" alt="">
							<p>{{ v.bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(v.bonus) }} <span> {{ t('vipBonus.desbloqueadosàs') }}</span>
									{{
										v.unlock_time }} · <span class="red">{{ t('vipBonus.NãoReivindicado') }}</span>
							</p>
						</div>
						<div class="bodyItem" v-else-if="v.status == 3">
							<img src="@/assets/images/vipBonus/await.png" alt="">
							<p>{{ v.bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(v.bonus) }} <span> {{ t('vipBonus.Desbloqueioàs') }} </span>
									{{
										v.unlock_time }}</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</el-dialog>
</template>

<script setup lang="ts">
import { computed, defineEmits, reactive } from 'vue'
import { store } from "@/store/index"
import { moneyFormat } from '@/utils/baseFun'
import { useI18n } from "vue-i18n";

const { t } = useI18n();

// 定义派发事件
const emit = defineEmits(['closePop'])

const props = defineProps({
	dataObj2: Object
})

const state = reactive({
	dialogVisible: true
})

const closePop = () => {
	emit('closePop', false)
}

const timeFormatter = (str: string) => {
	return str.slice(0, 5)
}

</script>

<style scoped lang="scss">
.pop {
	display: flex;
	flex-direction: column;
	justify-content: center;
	padding: 21px 0 12px 0;
	box-sizing: border-box;
	// box-shadow: inset 0px 1px 0px 0px rgba(255, 255, 255, 0.2), 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
	border-radius: 12px;
	background: #1B1C28;

	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0 20px 12px 27px;

		p {
			font-size: 20px;
			color: #fff;
			font-weight: 600;
		}

		img {
			cursor: pointer;
			width: 20px;
			margin-left: 29px;
			opacity: 0.5;
		}
	}
}

.body {
	max-height: 60vh;
	overflow-y: scroll;
	border-radius: 24px;
	padding: 12px;
	box-sizing: border-box;
	display: flex;
	flex-direction: column;
	gap: 8px;

	.bodyItem {
		padding: 8px 16px;
		box-sizing: border-box;
		border-radius: 12px;
		display: flex;
		align-items: center;
		background: #20232E;

		p {
			color: #C3CFD9;
			font-size: 16px;

			span {
				color: #C3CFD9;
			}

			.green {
				color: #75ED3D;
			}

			.red {
				color: #ED7163;
			}
		}

		img {
			margin-right: 17px;
			width: 26px;
		}

	}


}

@media (max-width: 768px) {
	.content {
		padding: 0 12px;
	}

	.pop {
		padding: 19px 0 8px 0;

		.title {
			padding: 0 12px 9px 15px;

			p {
				font-size: 16px;
			}
		}
	}

	.body {
		padding: 7px;
		gap: 6px;

		.bodyItem {
			padding: 8px 5px;
			box-sizing: border-box;
			border-radius: 12px;
			display: flex;
			align-items: center;
			background: #20232E;

			p {
				color: #C3CFD9;
				font-size: 12px;

				span {
					color: #C3CFD9;
				}

				.green {
					color: #75ED3D;
				}

				.red {
					color: #ED7163;
				}
			}

			img {
				margin-right: 5px;
				width: 18px;
			}

		}
	}
}
</style>