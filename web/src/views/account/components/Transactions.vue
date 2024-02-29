<template>
	<div class="Transactions">
		<div class="tabs">
			<div :class="{ active: tabIdx == index }" v-for="(item, index) in tabs" :key="index" @click="tabChange(index)">
				{{ item.title }}
			</div>
		</div>
		<div class="table">
			<div class="table_column">
				<div>{{ t('account.Tempo') }}</div>
				<div>{{ t('account.Valor') }}</div>
				<div>{{ t('account.Status') }}</div>
			</div>
			<div class="table_content">
				<ul v-if="list && list.length > 0">
					<li v-for="(item, index) in (list as any)" :key="item">
						<div>{{ item.add_time }}</div>
						<div>{{ moneyFormat(item.money) }}</div>
						<div
							:class="{ yellow: item.status == 0, green: item.status == 1, red: item.status != 0 && item.status != 1 }">
							{{
								item.status == 0 ? t('account.Emrevisão') :
								item.status == 1 ? t('account.Bemsucedido') :
									t('account.Fracassado') }}</div>
					</li>
				</ul>
				<div class="none_data" v-else>{{ t('account.OpaAindanãohádados') }}</div>
			</div>
		</div>
		<pagination :pageForm="pageForm" @changePage="changePage" />
	</div>
</template>

<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { getDate } from "@/utils/baseFun";
import { DepositAndWithdraw } from "@/api/DepositAndWithdraw";
import { debounce, moneyFormat } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
import pagination from "@com/pagination/index.vue"

export default defineComponent({
	name: "about",
	components: { pagination },
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const store = useStore();
		const { t } = useI18n();
		const state = reactive({
			tabs: [{ title: computed(() => t('account.Depósito')) }, { title: computed(() => t('account.Retirar')) }],
			tabIdx: 0,
			list: [],
			pageForm: {
				page: 1,
				limit: 10,
				count: 0,
			}
		});

		const getTableData = () => {
			debounce(async () => {
				let res = state.tabIdx == 0 ? await DepositAndWithdraw.get_user_order_list({ ...state.pageForm }) : await DepositAndWithdraw.get_user_order_withdraw_list({ ...state.pageForm });
				if (state.tabIdx == 1) {
					for (let i = 0; i < res.data.data.length; i++) {
						const element = res.data.data[i];
						if (element.status == 0) res.data.data[i].status = 1
					}
				}

				state.list = res.data.data
				state.pageForm.count = res.data.count
			})
		}
		getTableData()

		const tabChange = (idx: number) => {
			state.tabIdx = idx
			state.pageForm.page = 1
			getTableData()
		}

		const changePage = (val: string, val2: number) => {
			console.log(val, val2);

			state.pageForm.page = val2
			getTableData()
		}


		return { ...toRefs(state), t, store, moneyFormat, tabChange, changePage };
	},
});
</script>


<style lang="scss" scoped>
.Transactions {
	.tabs {
		display: flex;
		gap: 12px;
		margin-bottom: 16px;

		div {
			cursor: pointer;
			padding: 0 20px;
			line-height: 40px;
			text-align: center;
			background: #2F3445;
			border-radius: 8px;
			font-size: 14px;
			color: #98ABD0;
			border: 2px solid transparent;

			&.active,
			&:hover {
				color: #FFFFFF;
				background: rgba(65, 129, 238, 0.5);
				border: 2px solid #4181EE;
			}
		}
	}

	.table {
		.table_column {
			display: flex;
			line-height: 40px;
			background: #2F3445;
			border-radius: 12px 12px 0px 0px;

			div {
				width: 100%;
				text-align: center;
				font-size: 14px;
				color: #B2B6C5;
			}
		}

		.table_content {
			position: relative;
			min-height: 390px;
			box-sizing: border-box;
			background: #202431;
			border-radius: 0 0 12px 12px;

			ul {
				padding: 30px 0;

				li {
					display: flex;
					align-items: center;
					justify-content: space-between;
					margin-bottom: 20px;

					&:nth-last-child(1) {
						margin-bottom: 0;
					}

					div {
						text-align: center;
						width: 100%;
						font-size: 16px;
						color: #B2B6C5;
					}

					.green {
						color: #75ED3D;
					}

					.red {
						color: #FF7979;
					}

					.yellow {
						color: #F8BF2E;
					}
				}
			}

			.none_data {
				position: absolute;
				top: 50%;
				left: 50%;
				transform: translate(-50%, -50%);
				font-size: 16px;
				color: #B2B6C5;
			}
		}
	}
}

@media (max-width:768px) {
	.Transactions {
		.tabs {
			gap: 6px;
			margin-bottom: 12px;

			div {
				cursor: pointer;
				padding: 0 12px;
				line-height: 32px;
				border-radius: 6px;
				font-size: 12px;
				border: 1px solid transparent;

				&.active,
				&:hover {
					border: 1px solid #4181EE;
				}
			}
		}

		.table {
			.table_column {
				line-height: 32px;
				border-radius: 8px 8px 0px 0px;

				div {
					font-size: 12px;
				}
			}

			.table_content {
				min-height: 300px;
				border-radius: 0 0 8px 8px;

				ul {
					padding: 17px 0 17px 10px;

					li {
						margin-bottom: 16px;
						white-space: nowrap;

						div {
							font-size: 12px;
						}
					}
				}

				.none_data {
					font-size: 14px;
				}
			}
		}
	}
}
</style> 