<template>
	<div class="questionPopup">
		<el-popover placement="top" trigger="hover" popper-class="el_popover_style" :teleported="false" width='329px'>
			<template #reference>
				<img src="@assets/images/public/query.png" alt="">
			</template>
			<div class="popover_content">
				<div class="popover_content_title">{{ data['title'] }}</div>
				<div class="popover_content_txt">{{ data['info'] }}</div>
				<div class="btn" @click="jump(data['path'])">
					<span>{{ t('bonusCabinet.VERIFIQUEOSDETALHES') }}</span>
					<img src="@assets/images/public/arrow_two_black.png" alt="">
				</div>
			</div>
		</el-popover>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { RollerService } from "@/api/Roller";

export default defineComponent({
	name: "questionPopup",
	props: {
		id: Number
	},
	setup(props) {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			list: [
				{
					id: 1, title: computed(() => t('bonusCabinet.BônusEntrada')), info: computed(() => t('bonusCabinet.p_id_1')),
					path: '/vipBonus'
				},
				{
					id: 3, title: computed(() => t('bonusCabinet.BônusPerdido')), info: computed(() => t('bonusCabinet.p_id_3')),
					path: '/supplyCrate'
				},
				{
					id: 5, title: computed(() => t('bonusCabinet.BônusCashback')), info: computed(() => t('bonusCabinet.p_id_5')),
					path: '/vipBonus'
				},
				{
					id: 6, title: computed(() => t('bonusCabinet.BônusDiário')), info: computed(() => t('bonusCabinet.p_id_6')),
					path: '/vipBonus'
				},
				{
					id: 7, title: computed(() => t('bonusCabinet.BônusSemanal')), info: computed(() => t('bonusCabinet.p_id_7')),
					path: '/vipBonus'
				},
				{
					id: 8, title: computed(() => t('bonusCabinet.BônusMensal')), info: computed(() => t('bonusCabinet.p_id_8')),
					path: '/vipBonus'
				},
				{
					id: 9, title: computed(() => t('bonusCabinet.BônusAvançodeNível')), info: computed(() => t('bonusCabinet.p_id_9')),
					path: '/vipBonus'
				},
				{
					id: 11, title: computed(() => t('bonusCabinet.SlotGrátis')), info: '',
					path: 'slot'
				},
			],
			data: {},
			needAmount: 0,
		});
		state.list.forEach((item) => {
			if (item.id == props.id) return state.data = item
		});
		if (props.id == 11) {
			let item = state.list.find(obj => obj.id === props.id)
			RollerService.roller_money_state().then((res) => {
				const obj = {
					id: item?.id,
					title: item?.title,
					info: computed(() => t('bonusCabinet.p_id_11', { amount: res.data.need_amount })) as any,
					path: item?.path
				}
				state.data = obj
			});
		}



		const jump = (path) => {
			if (path == 'deposit') store.state.status.depositShow = true
			else if (path == 'slot') store.dispatch("status/setRollerShow", true)
			else router.push(path)
		}

		return { ...toRefs(state), store, t, props, jump };
	},
});
</script>
<style  lang="scss" scoped>
.questionPopup {
	img {
		margin-left: 24px;
		cursor: pointer;
		width: 20px;
	}

	:deep(.el-popover.el-popper) {
		// word-break: normal;
	}

	.popover_content {
		.popover_content_title {
			margin-bottom: 8px;
			font-size: 16px;
			font-weight: bold;
			color: #F3B343;
		}

		.popover_content_txt {
			margin-bottom: 17px;
			font-size: 14px;
			color: #B2B6C5;
			line-height: 20px;
			white-space: pre-wrap;
			// word-break: break-word;
			// word-wrap: break-word;
		}

		.btn {
			user-select: none;
			cursor: pointer;
			display: flex;
			align-items: center;
			justify-content: center;
			padding: 7px 0;
			background: #FFC746;
			border-radius: 8px;

			span {
				margin-right: 3px;
				font-size: 12px;
				font-weight: 600;
				color: #1B1D29;
			}

			img {
				margin-left: 3px;
				width: 15px;
			}
		}
	}
}

@media (max-width: 768px) {
	.questionPopup {
		img {
			margin-left: 6px;
			width: 13px;
		}

		.popover_content {
			.popover_content_title {
				margin-bottom: 9px;
				font-size: 14px;
			}

			.popover_content_txt {
				font-size: 12px;
				line-height: 18px;
			}
		}
	}
}
</style>
  