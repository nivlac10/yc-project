<template>
	<div class="depositPopup" v-if="domShow">
		<el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
			:width="store.state.status.isPc ? '400px' : '100%'" top="200px">
			<div class="dialog_content">
				<div class="true_box">
					<div class="content_box">
						<img src="@assets/images/promptPopup/purse.png" alt="">
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
import { store } from "@/store/index";

export default defineComponent({
	name: "depositPopup",
	props: {
		type: {
			type: Number,
			default: 0
		},
		tips: {
			type: String,
			default: ''
		},
		btnName: {
			type: String,
			default: 'Confirmar'
		},
	},
	setup(props, { emit }) {
		const { proxy } = getCurrentInstance() as any;

		const state = reactive({
			domShow: true,
			dialogVisible: true,
		});

		const btnClick = () => {
			store.state.status.depositShow = true
			state.domShow = false
		}

		return { ...toRefs(state), store, props, btnClick };
	},
});
</script>
<style  lang="scss" scoped>
.depositPopup {
	.dialog_content {
		padding: 45px 40px;
		box-sizing: border-box;
		background: #202431;
		border-radius: 12px;
		text-align: center;

		.true_box {
			.content_box {
				img {
					display: block;
					margin: 0 auto;
					width: 50px;
				}

				p {
					padding: 24px 0 37px 0;
					font-size: 16px;
					font-weight: 600;
					color: #B2B6C5;
					line-height: 19px;
				}
			}

			.btn {
				cursor: pointer;
				margin: 0 20px;
				padding: 12px 0;
				font-size: 18px;
				font-weight: 600;
				color: #FFFFFF;
				background: #CB394F;
				border-radius: 37px;
			}
		}
	}
}

@media (max-width: 768px) {
	.depositPopup {
		.dialog_content {
			margin: 0 10px;
			padding: 40px 22px;

			.true_box {
				.content_box {
					img {
						width: 40px;
					}

					p {
						font-size: 14px;
						line-height: 16px;
					}
				}

				.btn {
					margin: 0 25px;
					padding: 12px 0;
					font-size: 16px;
					border-radius: 30px;
				}
			}
		}
	}
}
</style>
  