<template>
	<div class="receive_bonus_content" v-if="dialogVisible">
		<img src="@assets/images/vipBonus/Gold_icon.png" alt="">
		<span>Recebe {{ dialogAmount < 0.01 ? `<${t('base.currencySymbol')} 0.01` : t('base.currencySymbol') + dialogAmount.toFixed(2) }}</span>
				<img src="@assets/images/public/Shutdown.png" alt="" @click="dialogVisible = false">
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
export default defineComponent({
	name: "receiveBonus",
	setup(props) {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			dialogVisible: false,
			dialogAmount: 0
		});
		proxy.$mitt.on('receiveBonus', (val: number) => {
			state.dialogVisible = true
			state.dialogAmount = val
			setTimeout(() => {
				state.dialogVisible = false
			}, 3000);
		})
		return { ...toRefs(state), store, t, props };
	},
});
</script>
<style  lang="scss" scoped>
.receive_bonus_content {
	position: fixed;
	left: 20px;
	bottom: 100px;
	z-index: 99999;
	width: 272px;
	display: flex;
	align-items: center;
	justify-content: space-around;
	padding: 10px;
	box-sizing: border-box;
	background: #252633;
	border-radius: 8px;

	img:nth-child(1) {
		width: 35px;
	}

	span:nth-child(2) {
		font-size: 16px;
		font-weight: bold;
		color: #FFFFFF;
	}

	img:nth-child(3) {
		width: 11px;
		opacity: 0.5;
	}
}

@media (max-width: 768px) {
	.receive_bonus_content {
		position: fixed;
		left: 10px;
		bottom: 100px;
		width: 260px;
		padding: 11px 0;
		background: #252633;
		border-radius: 8px;

		img:nth-child(1) {
			width: 29px;
		}

		span:nth-child(2) {
			font-size: 15px;
		}

		img:nth-child(3) {
			width: 11px;
		}
	}
}
</style>
  