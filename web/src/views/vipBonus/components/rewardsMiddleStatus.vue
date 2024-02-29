<template>
	<div class="rewardsMiddleStatus">
		<el-popover placement="top" trigger="hover" popper-class="el_popover_style" :teleported="false" :hide-after="0"
			:width="setWidth">
			<template #reference>
				<img v-if="dataObj.status == 0" src="@assets/images/vipBonus/usable.png" alt="" @click="showRewardsPop(true)">
				<img v-else-if="dataObj.status == 1" src="@assets/images/vipBonus/Claimed.png" alt=""
					@click="showRewardsPop(true)">
				<img v-else-if="dataObj.status == 2" src="@assets/images/vipBonus/unclaimed.png" alt=""
					@click="showRewardsPop(true)">
				<img v-else-if="dataObj.status == 3" src="@assets/images/vipBonus/await.png" alt="" @click="showRewardsPop(true)">
			</template>
			<div class="popover_content">
				<div class="popover_content_txt" v-if="dataObj.status == 0">
					<span style="color: #fff;">{{ dataObj.bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(dataObj.bonus) }}</span>
							<span>{{ t('vipBonus.desbloqueiaàs') }} </span>
							<span style="color: #fff;">{{ dataObj.unlock_time }}</span>
							<span style="color: #75ED3D;"> {{ t('vipBonus.Disponível') }}</span>
				</div>
				<div class="popover_content_txt" v-else-if="dataObj.status == 1">
					<span style="color: #fff;">{{ dataObj.bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(dataObj.bonus) }}</span>
							<span> {{ t('vipBonus.NãoReivindicado') }} </span>
							<span style="color: #fff;">{{ timeFormatter }}</span>
							<span style="color: #75ED3D;"> {{ t('vipBonus.NãoReivindicado') }}</span>
				</div>
				<div class="popover_content_txt" v-else-if="dataObj.status == 2">
					<span style="color: #fff;">{{ dataObj.bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(dataObj.bonus) }}</span>
							<span> {{ t('vipBonus.NãoReivindicado') }} </span>
							<span style="color: #fff;">{{ dataObj.unlock_time }} · </span>
							<span style="color: #ED7163;">{{ t('vipBonus.NãoReivindicado') }}</span>
				</div>
				<div class="popover_content_txt" v-else-if="dataObj.status == 3">
					<span style="color: #fff;">{{ dataObj.bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(dataObj.bonus) }}</span>
							<span> {{ t('vipBonus.Desbloqueioàs') }} </span>
							<span style="color: #fff;">{{ dataObj.unlock_time }}</span>
				</div>
			</div>
		</el-popover>
	</div>

	<all-rewards-pop v-if="showPop" :dataObj2="props.dataObj2" @closePop="showRewardsPop" />
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import allRewardsPop from "./allRewardsPop.vue";
import { moneyFormat } from "@/utils/baseFun";
export default defineComponent({
	name: "rewardsMiddleStatus",
	components: { allRewardsPop },
	props: {
		dataObj: Object,
		dataObj2: Object
	},
	setup(props) {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			dataObj: props.dataObj as any,
			showPop: false
		});

		const showRewardsPop = (val: boolean) => {
			state.showPop = val
		}

		const timeFormatter = computed(() => {
			return (props.dataObj as any).unlock_time.slice(0, 5)
		})

		watch(() => props.dataObj, (val) => {
			state.dataObj = val
		}, { deep: true, immediate: true })

		const setWidth = () => computed(() => {
			if (state.dataObj.status == 0) return 250
			else if (state.dataObj.status == 1) return 330
			else if (state.dataObj.status == 2) return 330
			else if (state.dataObj.status == 3) return 330
		})

		return { ...toRefs(state), store, t, props, showRewardsPop, timeFormatter, setWidth, moneyFormat };
	},
});
</script>
<style  lang="scss" scoped>
.rewardsMiddleStatus {
	img {
		width: 100%;
	}
}

@media (max-width: 768px) {}
</style>
  