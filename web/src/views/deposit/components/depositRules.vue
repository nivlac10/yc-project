<template>
	<div class="depositRules">
		<el-dialog class="loginDialog" v-model="dialogVisible" :show-close="false" :close-on-click-modal="false"
			:close-on-press-escape="false" :width="store.state.status.isPc ? '512px' : '100%'">
			<div class="content_box">
				<img class="close_btn" src="@assets/images/public/popover_error_icon.png" alt="" @click="closeCom">
				<div class="header">
					<img src="@assets/images/public/popover_return.png" alt="" @click="jump">
					<div class="title">Regras de Depósito</div>
				</div>
				<p>1.O valor de depósito mínimo é de 20 BRL</p>
				<p>2.Os novos usuários podem obter 20% valor de primeiro depósito como bônus.</p>
				<p>3.Receberá 10% valor de depósito primeiro diariamente como bônus</p>
				<p>4.Se tiver quaisquer dúvidas para seu depósito, por favor, entre em contato com o nosso serviço de
					atendimento online.</p>
			</div>
		</el-dialog>
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
		return { ...toRefs(state), store, t, jump, closeCom };
	},
});
</script>
<style  lang="scss" scoped>
.depositRules {
	.content_box {
		position: relative;
		padding: 56px 28px 40px 28px;
		width: 100%;
		border-radius: 16px;
		background: var(--theme-box-background);
		box-sizing: border-box;

		.close_btn {
			cursor: pointer;
			position: absolute;
			top: 23px;
			right: 28px;
			width: 25px;
		}

		.header {
			display: flex;
			align-items: center;
			margin-bottom: 25px;

			img {
				cursor: pointer;
				margin-right: 15px;
				width: 30px;
			}

			.title {
				font-size: 26px;
				font-weight: bold;
				color: var(--theme-font-color-fff);
			}
		}

		p {
			margin-bottom: 5px;
			font-size: 14px;
			font-weight: 500;
			line-height: 20px;
			color: #7992A7;
		}
	}
}

@media (max-width: 768px) {
	.depositRules {
		.content_box {
			position: relative;
			padding: 36px 20px 40px 20px;
			border-radius: 0;

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
  