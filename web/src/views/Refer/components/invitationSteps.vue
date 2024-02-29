<template>
	<div class="invitationSteps">
		<div class="total_prizes_distributed_so_far">
			<div class="total_prizes_distributed_so_far_title">{{ t('refer.TOTALDEPRÊMIOSDISTRIBUÍDOSATÉOMOMENTO') }}</div>
			<ul>
				<li v-for="i in 3">
					<div>
						<img v-show="i == 1" src="@assets/images/refer/gold.png" alt="">
						<img v-show="i == 2" src="@assets/images/refer/silver.png" alt="">
						<img v-show="i == 3" src="@assets/images/refer/chips.png" alt="">
					</div>
					<div>
						<p v-if="i == 1">{{ t('refer.Bônusdiárioporindicação') }}</p>
						<p v-if="i == 2">{{ t('refer.VitalícioorIndicação') }}</p>
						<p v-if="i == 3">{{ t('refer.TotaldePessoasIndicadas') }}</p>
						<p>{{ i == 3 ? '' : t('base.currencySymbol') }} {{ data[i - 1] ? moneyFormat(data[i - 1], false) : 0
						}}</p>
					</div>
				</li>
			</ul>
		</div>
		<div class="invitationSteps_title">{{ t('refer.TRÊSETAPASCONVITE') }}</div>
		<ul class="invitationSteps_ul">
			<li v-for="(item, index) in list" :key="index" :style="{ background: `url(${imgs[index]}) ` }">
				<div class="li_title">{{ item.title }}</div>
				<div class="li_info">{{ item.info }}</div>
				<img class="arrow" v-show="index < 2" src="@assets/images/public/arrow_r.png" alt="">
			</li>
		</ul>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { ReferService } from "@/api/refer";
import { moneyFormat, getImageUrl } from "@/utils/baseFun";
export default defineComponent({
	name: "invitationSteps",
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			list: [
				{ title: computed(() => t('refer.COMPARTILHELINKREGISTRE')), info: computed(() => t('refer.Seussiteeconcluemoregistro')) },
				{ title: computed(() => t('refer.AMIGOSFAZEMDEPÓSITO')), info: computed(() => t('refer.AMIGOSFAZEMDEPÓSITOTxt')) },
				{ title: computed(() => t('refer.RECEBAOSEUBÔNUS')), info: computed(() => t('refer.RECEBAOSEUBÔNUSTxt')) }
			],
			data: [],
			imgs: [
				store.state.status.isPc ? getImageUrl('refer/newRefer/procedure_1.png') : getImageUrl('refer/app1.png'),
				store.state.status.isPc ? getImageUrl('refer/newRefer/procedure_2.png') : getImageUrl('refer/app2.png'),
				store.state.status.isPc ? getImageUrl('refer/newRefer/procedure_3.png') : getImageUrl('refer/app3.png'),
			],
		});

		const getData = async () => {
			let data = await ReferService.get_invite_total_data();
			console.log(data);
			if (data.data.code == 1) {
				(state.data as any)[0] = data.data.data.task_bonus.toString().split('.')[0];
				(state.data as any)[1] = data.data.data.bet_bonus.toString().split('.')[0];
				(state.data as any)[2] = data.data.data.user_num;
			}


		}
		getData();
		return { ...toRefs(state), store, t, moneyFormat };
	},
});
</script>
<style  lang="scss" scoped>
.invitationSteps {
	padding: 16px 0;
	margin-bottom: 10px;

	.total_prizes_distributed_so_far {
		margin-bottom: 26px;
		padding: 36px 12px 24px 12px;
		background: #202431;
		border-radius: 12px;

		.total_prizes_distributed_so_far_title {
			margin-bottom: 24px;
			padding-left: 15px;
			font-size: 24px;
			font-weight: bold;
			color: #B2B6C5;
		}

		ul {
			display: flex;
			gap: 24px;

			li {
				display: flex;
				align-items: center;
				padding: 20px 20px;
				width: 100%;
				background: #3C4256;
				border-radius: 12px;

				div:nth-child(1) {
					img {
						width: 81px;
						margin-right: 17px;

					}
				}

				div:nth-child(2) {
					p:nth-child(1) {
						margin-bottom: 16px;
						font-size: 16px;
						font-weight: 800;
						color: #B2B6C5;
					}

					p:nth-child(2) {
						font-size: 24px;
						font-weight: bold;
						color: #F3B343;
					}
				}
			}
		}
	}

	.invitationSteps_title {
		margin-bottom: 16px;
		font-size: 24px;
		font-weight: bold;
		color: #B2B6C5;
	}

	.invitationSteps_ul {
		display: flex;
		gap: 12px;

		li {
			position: relative;
			padding: 34px 24px 0 24px;
			width: 100%;
			height: 275px;
			box-sizing: border-box;

			&:nth-child(1) {
				background: url(@assets/images/refer/newRefer/procedure_1.png) no-repeat;
				background-size: 100% 100% !important;
			}

			&:nth-child(2) {
				background: url(@assets/images/refer/newRefer/procedure_2.png) no-repeat;
				background-size: 100% 100% !important;
			}

			&:nth-child(3) {
				background: url(@assets/images/refer/newRefer/procedure_3.png) no-repeat;
				background-size: 100% 100% !important;
			}

			.li_title {
				margin-bottom: 29px;
				font-size: 24px;
				font-weight: bold;
				color: var(--theme-font-color-fff);
				line-height: 32px;
			}

			.li_info {
				font-size: 20px;
				font-weight: 500;
				color: #DED2F6;
				line-height: 22px;
			}

			.arrow {
				position: absolute;
				top: 50%;
				right: 0;
				z-index: 1;
				transform: translate(60%, -50%);
				width: 48px;
			}
		}
	}
}

@media (max-width: 768px) {
	.invitationSteps {
		padding-top: 0px;

		.total_prizes_distributed_so_far {
			margin-bottom: 16px;
			padding: 18px 6px 6px 6px;
			border-radius: 12px;

			.total_prizes_distributed_so_far_title {
				margin-bottom: 18px;
				padding-left: 8px;
				font-size: 14px;
			}

			ul {
				flex-direction: column;
				gap: 6px;

				li {
					justify-content: start;
					gap: 15px;
					border-radius: 8px;
					padding: 13px 0;
					padding-left: 27px;
					box-sizing: border-box;
					align-items: center;


					div:nth-child(1) {
						img {
							width: 40px;
							margin: 0;
						}
					}

					div:nth-child(2) {
						p:nth-child(1) {
							margin-bottom: 8px;
							font-size: 12px;
						}

						p:nth-child(2) {
							font-size: 14px;
						}
					}
				}
			}
		}

		.invitationSteps_title {
			margin-bottom: 12px;
			font-size: 16px;
		}

		.invitationSteps_ul {
			flex-direction: column;

			li {
				position: relative;
				padding: 20px 40px 0 15px;
				height: 153px;

				.li_title {
					margin-bottom: 12px;
					font-size: 16px;
					line-height: 24px;
				}

				.li_info {
					font-size: 14px;
					line-height: 17px;
					width: 80%;
				}

				.arrow {
					top: inherit;
					left: 50%;
					bottom: 0;
					transform: translate(-50%, 60%) rotate(90deg);
					width: 38px;
				}
			}
		}
	}
}
</style>
  