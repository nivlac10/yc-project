<template>
	<div class="rewardsUpStatus">
		<div class="title_date">{{ getDate(0) == dataObj.day ?  t('refer.Hoje') : englishFormatDate(dataObj.day) }}</div>
		<div class="txt" v-if="dataObj.state == 0 || dataObj.state == 1">
			<span :class="{ span_color_2: receiveAmount == 0 }">{{ moneyFormat(receiveAmount) }}</span>&nbsp;/&nbsp;{{
				dataObj.total_bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(dataObj.total_bonus) }} </div>
				<div class="txt" v-if="dataObj.state == 2 || dataObj.state == 3">
					{{ t('vipBonus.Disponível') }}: <span>{{ dataObj.total_bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(dataObj.total_bonus) }}</span>
				</div>
		</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { englishFormatDate, getDate, moneyFormat } from "@/utils/baseFun";

export default defineComponent({
	name: "rewardsUpStatus",
	props: {
		dataObj: Object,
	},
	setup(props) {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			dataObj: props.dataObj as any
		});

		watch(() => props.dataObj, (val) => {
			state.dataObj = val
		}, { deep: true, immediate: true })

		const receiveAmount = computed(() => {
			let num: number = 0
			state.dataObj.data.forEach(item => {
				if (item.status == 1) num += item.bonus
			})
			return num
		})
		return { ...toRefs(state), store, t, props, receiveAmount, getDate, englishFormatDate, moneyFormat };
	},
});
</script>
<style lang="scss" scoped>
.rewardsUpStatus {
	text-align: center;

	.title_date {
		margin-bottom: 12px;
		font-size: 16px;
		color: #B2B6C5;
		font-weight: 600;
	}

	.txt {
		font-size: 14px;
		color: #B2B6C5;

		span {
			color: #75ED3D;
		}

		.span_color_2 {
			color: #C3CFD9;
		}
	}
}

@media (max-width: 768px) {
	.rewardsUpStatus {
		.title_date {
			margin-bottom: 11px;
			font-size: 12px;
		}

		.txt {
			font-size: 12px;

			span {
				color: #75ED3D;
			}

			.span_color_2 {
				color: #C3CFD9;
			}
		}
	}
}
</style>
  