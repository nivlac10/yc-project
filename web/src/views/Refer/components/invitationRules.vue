<template>
	<div class="invitationRules">
		<!-- <div class="rule_box">
			<div class="rule_box_title">Como Ganhar o Bônus Diário por Indicação?</div>
			<p>Ao convidar seus amigos:</p>
			<p>1. Eles devem concluir o registro usando seu link de convite.</p>
			<p>2. Realizar um depósito de qualquer valor e fazer pelo menos 5 apostas em qualquer jogo (sem valor mínimo).
			</p>
			<p>3. Para resgatar o bônus de indicação, clique em "Sair" e faça o resgate manualmente.</p>
			<p>4. O número de indicações e o valor do bônus serão recalculados diariamente às 00:00.</p>
			<p>5. Importante: Caso o bônus não seja resgatado até às 00:00, ele será considerado como renunciado e não
				poderá
				ser reemitido.</p>
		</div> -->
		<div class="rule_box">
			<div class="rule_box_title">{{ t('refer.COMOGANHARINDICAÇÃOVITALÍCIO') }}</div>
			<div class="rule-box_title_2">
				{{t('refer.Esteseráseufluxoderenda')}}
			</div>
		<p>{{t('refer.EsteseráseufluxoderendaTxt')}}</p>
		<p>{{t('refer.EsteseráseufluxoderendaTxt2')}}</p>
		</div>
		<div class="to_top" @click="goTop">
			<img src="@assets/images/public/Frame.png" alt="">
			<span>{{ t('refer.VoltaraoTopo') }}</span>
			<img src="@assets/images/public/Frame.png" alt="">
		</div>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
export default defineComponent({
	name: "invitationRules",
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({});

		const goTop = () => {
			const contentBox = document.getElementById('content_box');
			if (contentBox) {
				if (window.innerWidth <= 768) {
					window.scrollTo({
						top: 0,
						behavior: 'smooth'
					});
				} else {
					contentBox.scrollTop = 0;
				}
			}
		}

		return { ...toRefs(state), store, t, goTop };
	},
});
</script>
<style  lang="scss" scoped>

.invitationRules {
	padding: 16px 0;

	.rule_box {
		margin-bottom: 26px;
		padding: 36px 29px;
		background: #202431;
		border-radius: 24px;

		.rule_box_title {
			margin-bottom: 15px;
			font-size: 24px;
			font-weight: bold;
			color: var(--theme-checkbox-font-color);
		}

		.rule-box_title_2 {
			margin-bottom: 16px;
			font-size: 18px;
			font-weight: 500;
			color: #B2B6C5;
			line-height: 34px;
			white-space: pre-wrap;
		}

		p {
			font-size: 18px;
			font-weight: 500;
			color: #B2B6C5;
			line-height: 30px;
			white-space: pre-wrap;
		}
	}

	.to_top {
		cursor: pointer;
		display: flex;
		justify-content: center;
		gap: 24px;
		align-items: center;

		img {
			width: 22px;
		}

		span {
			font-size: 22px;
			font-weight: bold;
			color: #98ABD0;
		}
	}
}

@media (max-width: 768px) {
	.invitationRules {
		padding: 0;

		.rule_box {
			margin-bottom: 24px;
			padding: 16px 12px;
			border-radius: 12px;

			.rule_box_title {
				margin-bottom: 8px;
				font-size: 14px;
			}

			.rule-box_title_2 {
				margin-bottom: 10px;
				font-size: 12px;
				line-height: 16px;
			}

			p {
				font-size: 12px;
				line-height: 18px;
			}
		}

		.to_top {
			gap: 6px;

			img {
				width: 14px;
			}

			span {
				font-size: 16px;
			}
		}
	}
}
</style>
  