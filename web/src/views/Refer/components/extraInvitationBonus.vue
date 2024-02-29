<template>
	<div class="extraInvitationBonus">
		<img class="tag_img" src="@assets/images/refer/newRefer/tag.png" alt="">
		<div class="column">
			<div class="b_top">
				<span>{{ t('refer.ExtraBônusdeConvite') }}</span>
				<img src="@assets/images/public/query.png" alt="" @click="dialogVisible = true">
			</div>
		</div>
		<div class="receive_list">
			<div class="list">
				<ul>
					<li v-for="(item, index) in (bounsList as any)" :key="index" :class="{ state1: item.state == 1 }">
						<div class="li_money">{{ t('base.currencySymbol') }}<span>{{ item.money }}</span></div>
						<div class="li_gold_img">
							<img class="gold" src="@assets/images/refer/newRefer/Gold_icon.png" alt="" v-if="item.state !== 2">

							<img class="gold" src="@assets/images/refer/newRefer/complete.png" alt="" v-if="item.state == 2">
						</div>
						<div class="li_num">
							<img src="@assets/images/refer/newRefer/icon.png" alt="">
							<span>{{ item.invite_num }}/{{ item.num }}</span>
						</div>
						<div @click="getBouns(item)">
							<span
								:class="{ btn: true, no_receive: item.state == 0, sl_box_shadow_green: item.state == 1, yes_receive: item.state == 2 }">{{
									item.state
									== 2 ? t('btnName.Concluir') : t('btnName.Receber') }}</span>
						</div>
					</li>
					<!-- <li class="reward_1"  @click="getBouns(bounsList2[0])">
						<div class="li_title_money">RECOMPENSA DE ATÉ <span>R${{bounsList2[0]['money']}}</span></div>
						<div class="li_num">
							<img src="@assets/images/refer/newRefer/icon.png" alt="">
							<span>{{bounsList2[0]['invite_num']}}/{{ bounsList2[0]['num']}}</span>
						</div>
						<img class="li_img_1" src="@assets/images/refer/newRefer/money.png" alt="">
					</li>
					<li class="reward_2"  @click="getBouns(bounsList2[1])">
						<div class="li_title_money">BÔNUS ADICIONAL DE ATÉ <span>R${{bounsList2[1]['money']}}</span></div>
						<div class="li_num">
							<img src="@assets/images/refer/newRefer/icon.png" alt="">
							<span>{{bounsList2[1]['invite_num']}}/{{ bounsList2[1]['num']}}</span>
						</div>
						<img class="li_img_1" src="@assets/images/refer/newRefer/Champion.png" alt="">
					</li> -->
				</ul>
			</div>
			<p>{{ t('refer.TorneseFaçadepósitooguecincovezes') }}</p>
		</div>

		<el-dialog v-model="dialogVisible" :show-close="false" :close-on-press-escape="false"
			:width="store.state.status.isPc ? '400px' : '100%'" @click="dialogVisible = false">
			<div class="dialog_content">
				<div class="dialog_content_title">
					<span>{{ t('refer.ExtraBônusdeConvite') }}</span>
					<img src="@assets/images/public/Shutdownx.png" alt="">
				</div>
				<div class="dialog_content_column">
					<div>{{ t('refer.NúmeroDeConvites') }}</div>
					<div>{{ t('refer.Recompensas') }}</div>
				</div>
				<ul>
					<li v-for="(v, i) in data">
						<div>{{ v.num }}</div>
						<div>{{ t('base.currencySymbol') }}{{ v.money }}</div>
					</li>
				</ul>
			</div>
		</el-dialog>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, onBeforeUnmount, watch, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { ReferService } from "@/api/refer";
import { debounce, getUserInfo, moneyFormat } from "@/utils/baseFun";
import promptPopup from "@/components/promptPopup/index";

export default defineComponent({
	name: "extraInvitationBonus",
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			dialogVisible: false,
			bounsList: [{ num: 5 }, { num: 15 }, { num: 30 }, { num: 80 }, { num: 200 }, { num: 500 }, { num: 1000 }],
			num: 0,
			bonus: 0,
			beyondNum: 0,
			bounsList2: [{ num: 500 }, { num: 1000 }],
			data: [{ money: 3, num: 5 }],
		});

		const getPercent = (num, total) => {
			num = parseFloat(num);
			total = parseFloat(total);
			if (isNaN(num) || isNaN(total)) {
				return "-";
			}
			return total <= 0 ? 0 : Math.round((num / total) * 10000) / 100.0;
		}


		//获取佣金列表
		const getData = async () => {
			let res = await ReferService.get_user_invite_state();
			state.num = res.data.num;
			state.bonus = res.data.bonus;
			state.bounsList = res.data.data;
			// state.bounsList = JSON.parse(JSON.stringify(res.data.data));
			// state.bounsList2 = state.bounsList.splice(-2,2);
			state.data = res.data.data;
			let dataNum = state.num;
			res.data.data.map(v => {
				dataNum -= v.num;
			})
			state.beyondNum = dataNum;
			nextTick(() => {
				getAward()
			})
			proxy.$mitt.emit("setNumberOfInvitees", res.data.num)
			proxy.$mitt.emit('getListData', res.data.data)
		}

		// 获取邀请奖励
		const getAward = () => {
			let total: any = getPercent(200 / 5, 200);
			let num = state.num; // 邀请人数
			let arr = [...state.bounsList]
			// 设置进度条进度
			for (let i = 0; i < arr.length; i++) {
				const item = arr[i];
				if (num <= item.num) {
					let progressNum: number = num * (total / item.num) + i * total;
					(document.querySelector('.progress_box_t') as any).style = `width: ${progressNum}%`
					break;
				} else if (num >= 200) {
					(document.querySelector('.progress_box_t') as any).style = `width: ${100}%`
				}
			}
		}
		//领取奖金
		function getBouns(v) {
			if (store.state.user.token && store.state.user.token !== '') {
				if (v.state == 1) {
					debounce(async () => {
						let res = await ReferService.user_receive_invite_task({ task_id: v.task_id });
						if (res.data.code == 1) {
							promptPopup('rewardPopup', { amount: v['money'], title: t('refer.CONGRATULATIONSGETINVITATIONBONUS') })
							v.state = 2
						}
					}, 500)
				}

			} else {
				store.dispatch('status/setLoginShow', true)
			}
		}
		getData();

		watch(() => store.state.user.token, () => {
			getData();
		})

		return { ...toRefs(state), store, t, getBouns, moneyFormat };
	},
});
</script>
<style  lang="scss" scoped>
.extraInvitationBonus {
	position: relative;
	margin-bottom: 16px;
	padding: 24px 0 18px 0;
	background: #202431;
	border-radius: 12px;
	overflow: hidden;

	.tag_img {
		position: absolute;
		top: 0;
		left: 0;
		width: 63px;
	}

	.column {
		display: flex;
		align-items: center;
		padding-left: 36px;
		margin-bottom: 36px;

		.b_top {
			font-size: 18px;
			color: #FFFFFF;
		}

		img {
			cursor: pointer;
			margin-left: 11px;
			width: 18px;
		}
	}

	.state1 {
		border: 2px solid #1BBF3F !important;
	}

	.receive_list {
		.list {
			padding: 0 24px;
			margin-bottom: 18px;

			ul {
				position: relative;
				display: flex;
				justify-content: space-between;
				align-items: center;
				gap: 16px;
				overflow-y: hidden;

				li {
					border: 2px solid rgba(0, 0, 0, 0);
					position: relative;
					padding: 10px 0;
					display: flex;
					flex-direction: column;
					width: 145px;
					height: auto;
					background: #2A2F40;
					border-radius: 4px;
					border: 3px solid transparent;
					box-sizing: border-box;

					>div {
						display: flex;
						align-items: center;
						justify-content: center;
					}

					.btn {
						padding: 10px 15px;
						margin-top: 10px;
						cursor: pointer;
					}

					.no_receive {
						background: #3C4256;
						color: #B2B6C5;
						border-radius: 10px;
					}

					.yes_receive {
						// background: #75ED3D;
						color: #75ED3D;
						border-radius: 10px;
					}

					.li_money {
						font-size: 14px;
						color: #FFFFFF;
					}

					.li_gold_img {
						display: flex;
						flex-direction: column;

						.gold {
							width: 30px;
							margin: 18px 0 16px 0;
						}
					}

					.li_num {
						img {
							margin-right: 4px;
							width: 21px;
						}

						span {
							font-size: 14px;
							color: #9599A7;
						}
					}
				}

				.reward_1,
				.reward_2 {
					display: flex;
					flex-direction: column;
					justify-content: space-between;
					padding-left: 16px;
					width: 201px;

					.li_title_money {
						width: 67%;
						display: block;
						font-size: 14px;
						font-weight: 600;
						color: #FFFFFF;
						line-height: 24px;

						span {
							color: #FCC03A;
						}
					}

					.li_num {
						justify-content: flex-start;
					}

					.li_img_1 {
						position: absolute;
						bottom: 0;
						right: 0;
						width: 90px;
					}
				}

				.reward_2 {
					width: 257px;

					.li_img_1 {
						position: absolute;
						top: 50%;
						right: 13px;
						transform: translate(0, -50%);
						width: 87px;
					}
				}
			}
		}

		p {
			margin: 0 auto;
			width: 80%;
			text-align: center;
			font-size: 16px;
			color: #f12c4c;
			line-height: 23px;
		}
	}

	.dialog_content {
		padding: 14px 0 31px 0;
		width: 100%;
		background: #202431;
		border-radius: 8px;

		.dialog_content_title {
			position: relative;
			margin-bottom: 27px;
			text-align: center;

			span {
				font-size: 16px;
				font-weight: 600;
				color: #FFFFFF;
			}

			img {
				cursor: pointer;
				position: absolute;
				top: 50%;
				right: 12px;
				transform: translateY(-50%);
				width: 21px;
			}
		}

		.dialog_content_column {
			display: flex;
			margin-bottom: 20px;

			div {
				width: 50%;
				font-size: 14px;
				font-weight: 600;
				text-align: center;
				color: #98ABD0;
			}
		}

		ul {
			li {
				display: flex;
				margin-bottom: 20px;

				&:nth-last-child(1) {
					margin-bottom: 0;
				}

				div {
					width: 50%;
					text-align: center;
					font-size: 18px;
					color: #FFFFFF;
				}
			}
		}
	}
}

@media (max-width: 768px) {
	.extraInvitationBonus {
		margin-bottom: 12px;
		padding: 18px 6px 13px 7px;
		border-radius: 12px;

		.column {
			padding-left: 14px;

			.b_top {
				font-size: 14px;
				margin-left: 20px;
			}
		}

		.receive_list {
			.list {
				margin-bottom: 18px;
				overflow-x: scroll;
				margin-right: -14px;
				padding-right: 10px;

				ul {
					gap: 12px;
					min-width: fit-content;
					margin-right: 10px;
					width: 160%;

					li {
						height: auto;
						width: 100px;

						.li_money {
							font-size: 12px;
							font-weight: 500;

						}

						.li_gold_img {
							.gold {
								margin: 10px 0;
							}

							img {
								width: 46px;
							}
						}

						.li_num {
							img {
								margin-right: 5px;
								width: 16px;
							}

							span {
								font-size: 12px;
								font-weight: 500;

							}
						}
					}
				}
			}

			p {
				width: 90%;
				font-size: 12px;
				line-height: 14px;
			}
		}

		.dialog_content {
			margin: 0 12px;
			padding: 18px 0 29px 0;

			.dialog_content_title {
				margin-bottom: 21px;
			}

			ul {
				li {
					margin-bottom: 16px;

					div {
						font-size: 16px;
					}
				}
			}
		}
	}
}
</style>
  