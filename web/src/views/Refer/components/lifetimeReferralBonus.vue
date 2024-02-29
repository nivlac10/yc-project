<template>
	<div class="lifetimeReferralBonus">
		<div class="column_title">
			<div>{{ t('refer.BônusIndicaçãoVitalício') }}</div>
			<div>{{ t('refer.Quantocomissõesvocêganha') }}</div>
		</div>
		<div class="content_b">
			<div class="level_img">
				<img v-show="store.state.status.isPc" src="@assets/images/refer/level_pc.png" alt="">
				<img v-show="!store.state.status.isPc" src="@assets/images/refer/level_phone.png" alt="">
			</div>
			<ul>
				<li>
					<div class="t_box">
						<div class="title">{{ t('refer.Nível1') }}</div>
						<el-popover placement="top" trigger="click" width="50%" popper-class="el_popover_style"
							:teleported="false" >
							<template #reference>
							    <img src="../../../assets/images/refer/query.png" alt="" class="Conta">
							</template>
							<div class="popover_content">
								<div class="popover_content_header">{{ t('refer.Nível1TXTpopTitle') }}</div>
								<div class="popover_content_txt">
									<p>{{ t('refer.Nível1TXTpopTxt') }}</p>
									<p>{{ t('refer.Nível2TXTpopTxt') }}
									</p>
								</div>
							</div>
						</el-popover>
					</div>
					<div class="b_box">
						{{ t('refer.Nívelecomissão') }}
					</div>
				</li>
				<li>
					<div class="t_box">
						<div class="title">{{ t('refer.Nível') }}2</div>
						<el-popover placement="top" trigger="click" width="50%" popper-class="el_popover_style"
							:teleported="false">
							<template #reference>
								<img src="../../../assets/images/refer/query.png" alt="" class="Conta">
							</template>
							<div class="popover_content">
								<div class="popover_content_header">{{ t('refer.Nível2TXTpopTitle') }}</div>
								<div class="popover_content_txt">
									<p>{{t('refer.Amigosconvidadospeloseus')}}</p>
									<p>{{t('refer.Amigosconvidadospeloseus2')}}</p>
								</div>
							</div>
						</el-popover>
					</div>
					<div class="b_box">
						{{ t('refer.IndicadosNível2deIndicados') }}
					</div>
				</li>
				<li>
					<div class="t_box">
						<div class="title">{{ t('refer.Nível') }} 3</div>
						<el-popover placement="top" trigger="click" width="50%" popper-class="el_popover_style"
							:teleported="false">
							<template #reference>
							    <img src="../../../assets/images/refer/query.png" alt="" class="Conta">
							</template>
							<div class="popover_content">
								<div class="popover_content_header">{{ t('refer.Nível3TXTpopTitle') }}</div>
								<div class="popover_content_txt">
									<p>{{t('refer.AmigosconvidadospelosseusIndicados')}}
									</p>
									<p>{{t('refer.AmigosconvidadospelosseusIndicados2')}}</p>
								</div>
							</div>
						</el-popover>
					</div>
					<div class="b_box">
						{{ t('refer.AmigosconvidadospelosseusIndicados3') }}
					</div>
				</li>
			</ul>
		</div>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
export default defineComponent({
	name: "lifetimeReferralBonus",
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({});
		return { ...toRefs(state), store, t, };
	},
});
</script>
<style  lang="scss" scoped>
.lifetimeReferralBonus {
	margin: 16px 0;
	padding: 30px 12px 12px 12px;
	background: #202431;
	border-radius: 12px;
	.Conta{
		width: 24px;
	}
	.column_title {
		margin-bottom: 31px;
		padding-left: 15px;
		color: #B2B6C5;

		div:nth-child(1) {
			margin-bottom: 24px;
			font-size: 24px;
			font-weight: bold;
		}

		div:nth-child(2) {
			font-size: 16px;
		}
	}

	.content_b {
		padding-bottom: 24px;
		background: #2F3445;
		border-radius: 12px;

		.level_img {
			padding: 0 12px;
			img {
				width: 100%;
			}
			margin-bottom: 24px;
		}

		ul {
			display: flex;
			gap: 24px;
			padding: 0 18px;

			li {
				width: 100%;
				padding: 25px 18px 18px 18px;
				background: #3C4256;
				box-shadow: 0px 4px 17px 0px #252C37;
				border-radius: 12px;

				.t_box {
					display: flex;
					align-items: center;
					justify-content: space-between;
					margin-bottom: 21px;

					.title {
						font-size: 22px;
						font-weight: bold;
						color: #FFFFFF;
					}

					i {
						cursor: pointer;
						font-size: 24px;
						color: #C3CFD9;
					}

					:deep(.el_popover_style) {
						border: none;
						border-radius: 12px;
						font-size: 20px;
						background: var(--auxiliary-background-14);
						width: 335px !important;
						.popover_content {
						
							.popover_content_header {
								margin-bottom: 12px;
								font-size: 20px;
								font-weight: bold;
								color: #F3B343;
							}

							.popover_content_txt {
								font-size: 14px;
								font-weight: 400;
								color: #B2B6C5;
							}
						}

						.el-popper__arrow {
							&::before {
								background: var(--auxiliary-background-14);
								border: none;
							}
						}
					}
				}

				.b_box {
					font-size: 18px;
					font-weight: 500;
					color: #B2B4B9;
					line-height: 23px;
				}
			}
		}
	}
}

@media (max-width: 768px) {
	.lifetimeReferralBonus {
		margin: 12px 0;
		padding: 18px 6px 6px 6px;
		border-radius: 12px;

		.Conta{
		width: 16px;
	}
		.column_title {
			margin-bottom: 15px;
			padding-left: 10px;

			div:nth-child(1) {
				margin-bottom: 14px;
				font-size: 16px;
			}

			div:nth-child(2) {
				font-size: 12px;
			}
		}

		.content_b {
			padding-bottom: 6px;
			border-radius: 12px;

			.level_img {
				padding: 0 6px;
				img {
					width: 100%;
					
				}
				margin-bottom: 12px;
			}

			ul {
				flex-direction: column;
				gap: 12px;
				padding: 0 6px;

				li {
					padding: 13px 15px;
					border-radius: 12px;
					box-sizing: border-box;

					.t_box {
						margin-bottom: 12px;

						.title {
							font-size: 14px;
						}

						i {
							font-size: 20px;
						}

						:deep(.el_popover_style) {

							.popover_content {
								.popover_content_header {
									margin-bottom: 6px;
									font-size: 15px;
								}

								.popover_content_txt {
									font-size: 12px;
								}
							}
						}
					}

					.b_box {
						font-size: 12px;
						line-height: 15px;
					}
				}
			}
		}
	}
}
</style>
  