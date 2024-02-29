<template>
	<div class="ranking">
		<div class="ranking_box">
			<div class="ranking_box_l">
				<div class="title">PRÊMIOS RECEBIDOS ATÉ AGORA</div>
				<div class="m1">
					<div class="label">Bônus já pagos</div>
					<div class="money"><span>R$ {{ total_commission }}</span></div>
				</div>
				<div class="m2">
					<div class="label">Total De Convidados</div>
					<div class="money">
						<img src="@assets/images/refer/newRefer/home_Friends_icon.png" alt="">
						<span>{{ total_num }}</span>
					</div>
				</div>
			</div>
			<div class="ranking_box_r">
				<div :class="{ first: index == 1, second: index == 0, third: index == 2 }"
					v-for="(item, index) in  (top3 as any) " :key="index">
					<div class="avatar">
						<img class="avatar_img" :src="getImageUrl(`avatar/headsculpture_img_${item.icon}.png`)" alt="">
						<img class="rank_img" :src="getImageUrl(`refer/newRefer/crown_${index == 0 ? 2 : index == 1 ? 1 : 3}.png`)"
							alt="">
					</div>
					<div class="user_id text_hiding">{{ item.nickname }}</div>
					<div class="member_num">
						<img src="@assets/images/refer/newRefer/icon.png" alt="">
						<span>{{ item.invite_num }}</span>
					</div>
					<div class="amount">R$ {{ item.money }}</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { ReferService } from "@/api/refer";
import { getImageUrl } from "@/utils/baseFun";

export default defineComponent({
	name: "ranking",
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			total_commission: 0,
			total_num: 0,
			top3: []
		});

		const getData = () => {
			ReferService.get_commission_total_data().then(res => {
				state.top3 = [res.data.data.top3[1] as never, res.data.data.top3[0] as never, res.data.data.top3[2] as never]
				state.total_commission = res.data.data.total_commission
				state.total_num = res.data.data.total_num
			})
		}
		getData()

		return { ...toRefs(state), store, t, getImageUrl };
	},
});
</script>
<style  lang="scss" scoped>
.ranking {
	padding: 20px;
	border-radius: 12px;
	background: linear-gradient(90deg, #5213EB 0%, #9229DD 40%, #7317F1 100%);

	.ranking_box {
		display: flex;
		gap: 30px;

		.ranking_box_l {
			width: 100%;

			.title {
				margin-bottom: 24px;
				font-size: 32px;
				font-weight: bold;
				color: var(--theme-font-color-fff);
			}

			.m1,
			.m2 {
				padding: 15px 0;
				text-align: center;
				box-sizing: border-box;

				.label {
					margin-bottom: 20px;
					font-size: 18px;
					font-weight: bold;
					color: rgba(255, 255, 255, 0.8);
				}

				.money {
					display: flex;
					align-items: center;
					justify-content: center;

					img {
						margin-right: 11px;
						width: 34px;
					}

					span {
						font-size: 30px;
						font-weight: bold;
						color: var(--auxiliary-font-color-28);
					}
				}
			}

			.m1 {
				margin-bottom: 9px;
				background: url(@assets/images/refer/newRefer/Group.png) no-repeat;
				background-size: 100% 100%;
			}

			.m2 {
				background: url(@assets/images/refer/newRefer/Group_2.png) no-repeat;
				background-size: 100% 100%;
			}
		}

		.ranking_box_r {
			background: url(@assets/images/refer/newRefer/Maskgroup.png);
			background-size: 100% 100%;
			width: 687px;
			display: flex;
			justify-content: space-around;
			flex-shrink: 0;

			.first,
			.second,
			.third {
				text-align: center;

				.avatar {
					position: relative;
					margin: 0 auto;
					margin-bottom: 10px;
					border: 4px solid #FFAC4F;
					width: 100px;
					border-radius: 50%;

					.avatar_img {
						display: block;
						width: 100%;
					}

					.rank_img {
						position: absolute;
						top: 0;
						right: 0;
						transform: translateY(-60%);
						width: 55px;
					}
				}

				.user_id {
					display: inline-block;
					width: 70%;
					font-size: 20px;
					font-weight: 500;
					color: rgba(255, 255, 255, 0.9);
				}

				.member_num {
					display: flex;
					justify-content: center;
					align-items: center;
					padding: 10px 0;

					img {
						margin-right: 7px;
						width: 21px;
					}

					span {
						font-size: 15px;
						font-weight: bold;
						color: var(--theme-font-color-fff);
					}
				}

				.amount {
					font-size: 22px;
					font-weight: bold;
					color: var(--auxiliary-font-color-28);
					text-align: center;
				}
			}

			.first {
				transform: translateY(10%);

				.amount {
					font-size: 38px;
				}
			}

			.second,
			.third {
				transform: translateY(20%);
			}

			.second {
				.avatar {
					border-color: #B0B0B0;
				}
			}

			.third {
				.avatar {
					border-color: #E4C6A5;
				}
			}
		}
	}
}

@media (max-width: 768px) {
	.ranking {
		padding: 0;
		background: transparent;

		.ranking_box {
			flex-wrap: wrap-reverse;
			gap: 12px;

			.ranking_box_l {
				padding: 12px;
				border-radius: 12px;
				background: linear-gradient(90deg, #5213EB 0%, #9229DD 40%, #7317F1 100%);

				.title {
					margin-bottom: 11px;
					font-size: 15px;
				}

				.m1,
				.m2 {
					padding: 14px 0 12px 0;

					.label {
						margin-bottom: 22px;
						font-size: 13px;
					}

					.money {
						img {
							margin-right: 8px;
							width: 25px;
						}

						span {
							font-size: 23px;
						}
					}
				}
			}

			.ranking_box_r {
				width: 100%;
				height: 155px;

				.first,
				.second,
				.third {
					.avatar {
						width: 50px;

						.rank_img {
							width: 28px;
						}
					}

					.user_id {
						font-size: 12px;
					}

					.member_num {
						padding: 5px 0;

						img {
							margin-right: 3px;
							width: 13px;
						}

						span {
							font-size: 12px;
						}
					}

					.amount {
						font-size: 14px;
					}
				}

				.first {
					transform: translateY(10%);

					.member_num {
						padding: 5px 0;
					}

					.amount {
						font-size: 20px;
					}
				}

				.second,
				.third {
					transform: translateY(20%);
				}
			}
		}
	}
}
</style>
  