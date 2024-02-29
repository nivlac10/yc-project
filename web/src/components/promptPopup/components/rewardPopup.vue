<template>
	<div class="rewardPopup" v-if="domShow">
		<el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
			:width="store.state.status.isPc ? '400px' : '100%'" top="200px">
			<div class="dialog_content">
				<div class="true_box">
					<div class="tips">{{ props.title }}</div>
					<div class="content_box">
						<img src="@assets/images/signIn/gold.png" alt="">
						<div>{{ moneyFormat(props.amount) }}</div>
						<p>{{ props.tips }}</p>
					</div>
					<div class="btn" @click="btnClick">
						<span>{{ props.btnName }}</span>
					</div>
				</div>
			</div>
		</el-dialog>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { store } from "@/store/index";
import { getUserInfo, moneyFormat } from "@/utils/baseFun";

export default defineComponent({
	name: "rewardPopup",
	props: {
		title: {
			type: String,
			default: 'Check-in Sucesso !'
		},
		amount: {
			type: Number,
			default: 0
		},
		tips: {
			type: String,
			default: 'O bônus já foi transferido para o saldo da conta'
		},
		btnName: {
			type: String,
			default: 'Confirmar'
		}
	},
	setup(props, { emit }) {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const state = reactive({
			domShow: true,
			dialogVisible: true
		});

		const btnClick = () => {
			state.domShow = false
			getUserInfo()
		}

		return { ...toRefs(state), store, props, btnClick, moneyFormat };
	},
});
</script>
<style  lang="scss" scoped>
.rewardPopup {
	.dialog_content {
		padding: 42px 20px 50px 20px;
		box-sizing: border-box;
		background: rgba(32, 35, 48, 0.94);
		border-radius: 12px;
		text-align: center;

		.true_box {
			.tips {
				margin-bottom: 33px;
				font-size: 24px;
				font-weight: 600;
				color: #FFFFFF;
			}

			.content_box {
				margin-bottom: 33px;
				padding: 41px 13px;
				background: #2F3445;
				border-radius: 12px;

				img {
					display: block;
					margin: 0 auto;
					width: 68px;
				}

				div {
					padding: 30px 0 27px 0;
					font-size: 24px;
					font-weight: 600;
					color: #F8BF2E;
				}

				p {
					font-size: 16px;
					font-weight: 600;
					color: #B2B6C5;
					line-height: 19px;
				}
			}

			.btn {
				cursor: pointer;
				padding: 10px 0;
				font-size: 18px;
				font-weight: 600;
				color: #FFFFFF;
				background: #59C591;
				border-radius: 37px;
			}
		}
	}
}

@media (max-width: 768px) {
	.rewardPopup {
		.dialog_content {
			margin: 0 10px;
			padding: 40px 20px 34px 20px;

			.true_box {
				.tips {
					font-size: 16px;
				}

				.content_box {
					margin-bottom: 27px;
					padding: 33px 11px;

					img {
						width: 56px;
					}

					div {
						padding: 24px 0 22px 0;
						font-size: 20px;
					}

					p {
						font-size: 14px;
						line-height: 16px;
					}
				}

				.btn {
					cursor: pointer;
					padding: 12px 0;
					font-size: 16px;
					border-radius: 30px;
				}
			}
		}
	}
}
</style>
  