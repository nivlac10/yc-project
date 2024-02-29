<template>
	<div class="myInviteBonus">
		<div class="column">
			<div class="b_top">Bônus Diário por Indicação</div>
			<div class="b_bottom">
				<span>Daily Time-limited Event Evento Diário de Tempo Limitado：</span>
				<span>{{ hours }}:{{ minutes }}:{{ seconds }}</span>
			</div>
		</div>
		<div class="receive_list">
			<div class="list">
				<ul>
					<div class="progress_box">
						<div class="progress_box_n">
							<div class="progress_box_t"></div>
						</div>
					</div>
					<li v-for="(item, index) in (bounsList as any)" :key="index">
						<div><span>{{t('base.currencySymbol')}} {{ item.money }}</span></div>
						<div>
							<img src="@assets/images/refer/gold.png" alt="">
						</div>
						<div>
							<img src="@assets/images/refer/newRefer/icon.png" alt="">
							<span>{{ item.invite_num }} / {{ item.num }}</span>
						</div>
						<div @click="getBouns(item)">
							<span
								:class="{ btn: true, no_receive: item.state == 0, sl_box_shadow_green: item.state == 1, yes_receive: item.state == 2 }">{{
									item.state
									== 2 ? 'Concluir' : 'Receber' }}</span>
						</div>
					</li>
					<li>
						<div><span>{{t('base.currencySymbol')}} {{ bonus.toString().split('.')[0] }}</span></div>
						<div>
							<img src="@assets/images/refer/chips.png" alt="">
						</div>
						<div>
							<img src="@assets/images/refer/newRefer/icon.png" alt="">
							<span>{{ beyondNum > 0 ? beyondNum : 0 }} / 1</span>
						</div>
						<div class="btn">Recebimento Automático</div>
					</li>
				</ul>
			</div>
			<p>
				Ao concluir as tarefas de indicação acima e convidar mais 1 pessoa, você receberá {{t('base.currencySymbol')}} {{
					bonus.toString().split('.')[0] }}, a comissão
				será
				depositada automaticamente em sua conta.
			</p>
		</div>
		<!-- <el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
			:width="store.state.status.isPc ? '644px' : '100%'">
			<div class="content_box">
				<img class="close_img" src="@assets/images/public/Shut_down.png" alt="" @click="closeBtn">
				<div class="txt">{{ t('refer.CONGRATULATIONSGETINVITATIONBONUS') }}</div>
				<div class="amount_txt">
					<img src="@assets/images/signIn/Maskgroup.png" alt="">
					<span class="sl_font">{{ dialogVisibleAmount }} {{ t('base.currency') }}</span>
				</div>
			</div>
		</el-dialog> -->
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, onBeforeUnmount, watch, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { ReferService } from "@/api/refer";
import { debounce, getUserInfo } from "@/utils/baseFun";
import promptPopup from "@/components/promptPopup/index";

export default defineComponent({
	name: "myInviteBonus",
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			dialogVisible: false,
			dialogVisibleAmount: 0,
			hours: 0,
			minutes: 0,
			seconds: 0,
			bounsList: [{ num: 5 }, { num: 15 }, { num: 30 }, { num: 80 }, { num: 200 }],
			num: 0,
			bonus: 0,
			beyondNum: 0,
		});

		const getPercent = (num, total) => {
			num = parseFloat(num);
			total = parseFloat(total);
			if (isNaN(num) || isNaN(total)) {
				return "-";
			}
			return total <= 0 ? 0 : Math.round((num / total) * 10000) / 100.0;
		}



		//计算时间
		const countDown = (time) => {
			let nowTime = +new Date(); // 返回的是当前时间总的毫秒数
			let inputTime = +new Date(time); // 返回的是用户输入时间总的毫秒数
			let times = (inputTime - nowTime) / 1000; // times是剩余时间总的秒数 
			let h = parseInt((times / 60 / 60 % 24).toString()); //时
			(h as any) = h < 10 ? '0' + h : h;
			let m = parseInt((times / 60 % 60).toString()); // 分
			(m as any) = m < 10 ? '0' + m : m;
			let s = parseInt((times % 60).toString()); // 当前的秒
			(s as any) = s < 10 ? '0' + s : s;
			state.hours = h;
			state.minutes = m;
			state.seconds = s;
		}
		countDown(new Date().setHours(24, 0, 0, 0));
		let timer = setInterval(() => {
			countDown(new Date().setHours(24, 0, 0, 0));
		}, 1000);
		onBeforeUnmount(() => {
			clearInterval(timer);
		});

		//获取佣金列表
		const getData = async () => {
			let res = await ReferService.get_user_invite_state();
			state.num = res.data.num;
			state.bonus = res.data.bonus
			state.bounsList = res.data.data;
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

		const closeBtn = () => {
			state.dialogVisible = false
			getUserInfo()
		}

		return { ...toRefs(state), store, t, closeBtn, getBouns, };
	},
});
</script>
<style  lang="scss" scoped>
.myInviteBonus {
	margin-bottom: 16px;
	padding: 24px 12px;
	background: #202431;
	border-radius: 12px;

	.column {
		padding-left: 15px;

		.b_top {
			font-size: 24px;
			font-weight: bold;
			color: #B2B6C5;
		}

		.b_bottom {
			padding: 16px 0;

			span {
				font-size: 16px;
			}

			span:nth-child(1) {
				color: #B2B6C5;
			}

			span:nth-last-child(1) {
				font-weight: 500;
				color: #75ED3D;
				font-size: 22px;
			}
		}
	}

	.receive_list {
		padding: 30px;
		background: #2F3445;
		border-radius: 12px;
		overflow: hidden;

		.list {
			margin-bottom: 26px;

			ul {
				position: relative;
				display: flex;
				justify-content: space-between;
				align-items: center;
				gap: 30px;
				overflow-y: hidden;

				.progress_box {
					position: absolute;
					left: -8%;
					top: 30%;
					width: 82%;

					&::after {
						content: '';
						position: absolute;
						top: -5%;
						left: 0;
						z-index: 2;
						height: 120%;
						width: 20%;
						background: #2F3445;
					}

					.progress_box_n {
						position: relative;
						width: 100%;
						height: 14px;
						background: rgba(255, 255, 255, 0.06);
						overflow: hidden;



						.progress_box_t {
							width: 0;
							height: 100%;
							background: #1CB83D;
						}
					}
				}

				li {
					position: relative;
					z-index: 2;
					display: flex;
					flex-direction: column;
					width: 100%;

					>div {
						display: flex;
						align-items: center;
						justify-content: center;

						&:nth-child(1) {
							font-size: 22px;
							color: #FFFFFF;
						}

						&:nth-child(2) {
							display: flex;
							flex-direction: column;

							img {
								width: 70px;
								margin: 15px 0;
							}
						}

						&:nth-child(3) {
							margin-bottom: 18px;

							img {
								margin-right: 15px;
								width: 26px;
							}

							span {
								font-size: 20px;
								font-weight: bold;
								color: #FFFFFF;
							}
						}

						&:nth-last-child(1) {
							font-size: 16px;
							font-weight: bold;
							color: #D0D0D2;
							text-align: center;
							line-height: 20px;

							span {
								display: inline-block;
								padding: 12px 22px;
								font-size: 16px;
							}
						}
					}

					&:last-child {

						height: 200px;
					}

					.btn {
						font-size: 20px;
						font-weight: bold;
						color: #FFFFFF;

						&.no_receive {
							background: #3C4256;
							border-radius: 10px;
						}

						&.yes_receive {
							color: var(--auxiliary-font-color-7);
						}

						&.sl_box_shadow_green {
							cursor: pointer;
							color: #12151C;
						}
					}
				}
			}
		}

		p {
			margin: 0 auto;
			width: 80%;
			text-align: center;
			font-size: 16px;
			color: #B2B4B9;
			line-height: 23px;
		}
	}

	.info_txt {
		cursor: pointer;
		margin-top: 30px;
		text-align: center;
		font-size: 22px;
		font-weight: bold;
		color: #F3B343;
	}

	.content_box {
		position: relative;
		padding: 50px 20px 61px 20px;
		background: url(@assets/images/Refer/newRefer/Pop-up.png) no-repeat;
		background-size: 100% 100%;
		text-align: center;

		.close_img {
			cursor: pointer;
			position: absolute;
			top: 11px;
			right: 11px;
			width: 30px;
		}

		.txt {
			margin-bottom: 22px;
			font-size: 36px;
			font-weight: 800;
			color: var(--theme-font-color-fff);
			line-height: 48px;
		}

		.amount_txt {
			display: flex;
			justify-content: center;
			align-items: center;
			gap: 11px;

			img {
				width: 66px;
			}

			span {
				font-size: 45px;
			}
		}
	}

	.bottom {
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;
		margin-top: 20px;

		p {
			color: #4181EE;
			font-size: 16px;
			font-weight: bold;
			text-align: center;
			display: flex;
			align-items: center;

		}

		img {
			width: 19px;
			height: 21px;
		}


	}
}

@media (max-width: 768px) {
	.myInviteBonus {
		margin-bottom: 12px;
		padding: 18px 6px 13px 7px;
		border-radius: 12px;

		.column {
			padding-left: 14px;

			.b_top {
				font-size: 14px;
			}

			.b_bottom {
				padding: 12px 0;

				span {
					font-size: 12px;
				}

				span:nth-last-child(1) {
					font-size: 12px;
				}
			}
		}

		.receive_list {
			padding: 19px 14px;
			border-radius: 12px;

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

					.progress_box {
						position: absolute;
						left: -10%;
						top: 28%;

						.progress_box_n {
							height: 10px;
						}
					}

					li {
						>div {
							&:nth-child(1) {
								font-size: 12px;
								font-weight: 500;

							}

							&:nth-child(2) {
								img {
									width: 46px;
								}
							}

							&:nth-child(3) {
								margin-bottom: 12px;

								img {
									margin-right: 5px;
									width: 16px;
								}

								span {
									font-size: 12px;
									font-weight: 500;

								}
							}

							&:nth-last-child(1) {

								border-radius: 6px !important;

								span {
									padding: 8px;
									font-size: 8px;
									font-weight: 500;

								}
							}
						}

						&:last-child {

							height: 148.5px;
						}

						.btn {
							font-weight: 500;
							font-size: 12px !important;
							border-radius: 8px !important;
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

		.info_txt {
			margin-top: 18px;
			font-size: 13px;
		}

		.content_box {
			margin: 0 15px;
			padding: 45px 0 50px 0;

			.close_img {
				width: 22px;
			}

			.txt {
				font-size: 22px;
				line-height: 32px;
			}

			.amount_txt {
				display: flex;
				justify-content: center;
				align-items: center;
				gap: 11px;

				img {
					width: 47px;
				}

				span {
					font-size: 32px;
				}
			}
		}

		.bottom {

			p {
				display: block;
				font-size: 12px;
			}

			span {
				font-size: 12px;
				margin: 0;
			}

			img {
				vertical-align: middle;
				margin-top: -2px;
				width: 15.5px;
				height: 17px;
			}
		}
	}
}
</style>
  