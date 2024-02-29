<template>
	<div class="depositInstructions">
		<div class="content_box">
			<img class="close_btn" src="@assets/images/public/Shutdownx.png" alt="" @click="closeCom">
			<div class="header">
				<img src="@assets/images/public/popover_return.png" alt="" @click="jump">
				<div class="title">{{ t('btnName.Instruções') }}</div>
			</div>
			<div class="rule_title">{{ t('deposit.t1') }}</div>
			<p>{{ t('deposit.p1') }}</p>
			<div class="rule_title">{{ t('deposit.t2') }}</div>
			<p>{{ t('deposit.p2') }}</p>
			<div class="rule_title">{{ t('deposit.t3') }}</div>
			<p>{{ t('deposit.p3') }}</p>
			<div class="btn" @click="jumpRouter">{{ t('deposit.VertodososníveisVIP') }}</div>
		</div>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
export default defineComponent({
	name: "activities",
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const store = useStore();
		const { t } = useI18n();
		const state = reactive({
			dialogVisible: true,
		});
		const closeCom = () => {
			store.dispatch('status/setDepositShow', false)
		}
		const jump = () => {
			proxy.$mitt.emit("depositComShow", 0);
		}

		const jumpRouter = () => {
			closeCom()
			router.push('/vipBonus/allLevels')
		}

		return { ...toRefs(state), store, t, jump, closeCom, jumpRouter };
	},
});
</script>
<style  lang="scss" scoped>
.depositInstructions {
	.content_box {
		position: relative;
		padding: 36px 20px 38px 20px;
		width: 100%;
		border-radius: 16px;
		background: #202330;
		box-sizing: border-box;

		.close_btn {
			cursor: pointer;
			position: absolute;
			top: 21px;
			right: 19px;
			width: 20px;
		}

		.header {
			display: flex;
			align-items: center;
			margin-bottom: 24px;

			img {
				cursor: pointer;
				margin-right: 14px;
				width: 32px;
			}

			.title {
				font-size: 18px;
				font-weight: bold;
				color: var(--theme-font-color-fff);
			}
		}

		.rule_title {
			margin-bottom: 12px;
			font-size: 14px;
			font-weight: 600;
			color: #F3B343;
		}

		p {
			margin-bottom: 16px;
			font-size: 12px;
			color: #B2B6C5;
			line-height: 18px;
			white-space: pre-wrap;
		}

		.btn {
			cursor: pointer;
			text-align: center;
			line-height: 40px;
			font-size: 16px;
			font-weight: 600;
			color: #FFFFFF;
			background: #4181EE;
			border-radius: 138px;
		}
	}
}

@media (max-width: 768px) {
	.depositInstructions {
		margin: 0 11px;

		.content_box {
			position: relative;
			padding: 36px 20px 40px 20px;

			.close_btn {
				top: 14px;
				right: 19px;
				width: 18px;
			}

			.header {
				img {
					cursor: pointer;
					margin-right: 8px;
					width: 30px;
				}

				.title {
					font-size: 17px;
				}
			}

			p {
				font-size: 12px;
			}
		}
	}
}
</style>
  