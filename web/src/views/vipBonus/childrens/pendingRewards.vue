<template>
	<el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
		:width="store.state.status.isPc ? '1387px' : '100%'">
		<div class="pendingRewards">
			<div class="pendingRewards_title">
				<div class="l_box">
					{{ t('vipBonus.AguardandoResgate') }} <span>{{ moneyFormat(total_money) }}</span>
				</div>
				<div class="r_box">
					<div class="img_box">
						<img src="@assets/images/public/popover_return.png" alt="" @click="changeDate(0)">
						<img class="img_2" src="@assets/images/public/popover_return.png" alt="" @click="changeDate(1)">
					</div>
					<img class="close_img" src="@assets/images/public/Shutdown.png" alt="" @click="jump"
						v-if="store.state.status.isPc">
					<el-affix :offset="120" z-index="1" v-else>
						<img class="close_img" src="@assets/images/public/Shutdown.png" alt="" @click="jump">
					</el-affix>
				</div>
			</div>
			<div class="year_txt">{{ currentYear }}</div>
			<ul class="pendingRewards_ul">
				<li v-for="(v, i) in (list as any)" :key="i">
					<rewards-com :data="v" v-if="v.total_bonus" />
					<div :class="{ pendingRewards_ul_li_no_data: true, pendingRewards_ul_li_no_data_border: v.state == 0 }"
						v-else>
						<div class="date">
							<div class="title_date">{{ getDate(0) == v.day ? t('vipBonus.Hoje') : englishFormatDate(v.day)
							}}</div>
							<div class="txt">
								<span>{{ t('base.currencySymbol') }} 0.00</span>
							</div>
						</div>
						<div class="no_data">
							<p> {{ t('vipBonus.Sem') }}</p>
							<p>{{ t('vipBonus.Recompensa') }}</p>
						</div>
						<div></div>
					</div>
				</li>
			</ul>
		</div>
	</el-dialog>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch, nextTick } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import rewardsCom from "../components/rewardsCom.vue";
import { VipService } from "@/api/vip";
import { debounce, englishFormatDate, getDate, moneyFormat } from "@/utils/baseFun";

export default defineComponent({
	name: "pendingRewards",
	components: { rewardsCom },
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const route = useRoute()
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			list: [],
			list2: [],
			listFlag: true,
			historyArr: [],
			dialogVisible: true,
			total_money: 0,
			currentYear: 0, // 当前年
			currentMonth: 0, // 当前月
			daysInCurrentMonth: 0, // 当前月天数
		});

		const jump = () => {
			// router.go(-1)
			proxy.$mitt.emit('pendingRewardsShow')
		}
		// 获取当前月份的所有天数
		const getDaysInMonth = (year, month) => {
			var lastDayOfMonth = new Date(year, month, 0).getDate();
			return lastDayOfMonth;
		}
		// 设置当前日期数据
		const getCurrentDate = () => {
			var currentDate = new Date();
			var currentYear = currentDate.getFullYear();
			var currentMonth = currentDate.getMonth() + 1;
			var daysInCurrentMonth = getDaysInMonth(currentYear, currentMonth);

			state.currentYear = currentYear
			state.currentMonth = currentMonth
			state.daysInCurrentMonth = daysInCurrentMonth
			// return [currentYear, currentMonth, daysInCurrentMonth]
		}
		getCurrentDate()

		const getDefaultData = () => {
			for (let i = 0; i < state.daysInCurrentMonth; i++) {
				state.list.push({ day: `${state.currentYear}-${state.currentMonth < 10 ? `0${state.currentMonth}` : state.currentMonth}-${i + 1 < 10 ? `0${i + 1}` : i + 1}` } as never)
				// 设置当天高亮
				if (state.list[i]['day'] == getDate(0)) {
					(state.list[i] as any).state = 0;
				}
			}
		}
		getDefaultData()

		const getList = () => {
			VipService.get_user_split_bonus_list().then(res => {
				state.total_money = res.data.total_money
				for (let i = 0; i < state.list.length; i++) {
					let element1 = state.list[i];
					for (let j = 0; j < res.data.data.length; j++) {
						let element2 = { ...res.data.data[j] };
						// 给默认数据赋值
						if (element1['day'] == element2['day']) {
							state.list[i] = element2 as never
						}
					}
				}
				state.list2 = [...state.list]
			})
		}
		getList()
		proxy.$mitt.on('getVipFinish', () => {
			state.list = state.list2 = []
			state.listFlag = true
			getDefaultData()
			getList()
		})

		// 修改日期
		const changeDate = (idx: number) => {
			if (idx == 0) {
				if (state.currentMonth > 1) state.currentMonth -= 1
				else {
					state.currentYear -= 1
					state.currentMonth = 12
				}
			} else {
				if (state.currentMonth < 12) state.currentMonth += 1
				else {
					state.currentYear += 1
					state.currentMonth = 1
				}
			}
			state.daysInCurrentMonth = getDaysInMonth(state.currentYear, state.currentMonth);
			state.list = []
			getDefaultData()
			debounce(getList)
		}

		return { ...toRefs(state), store, t, jump, getDate, englishFormatDate, changeDate, moneyFormat };
	},
});
</script>
<style lang="scss" scoped>
.pendingRewards {
	margin-top: 27px;
	padding: 0 24px 24px;
	border-radius: 21px;
	background: #202431;
	width: 100%;

	.pendingRewards_title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 32px 30px 32px 6px;
		box-sizing: border-box;

		.l_box {
			font-size: 18px;
			font-weight: 600;
			color: #B2B6C5;

			span {
				font-size: 20px;
				font-weight: 600;
				color: #75ED3D;
			}
		}

		.r_box {
			display: flex;
			align-items: center;

			.img_box {
				img {
					cursor: pointer;
					width: 41px;
					height: 41px;

					&.img_2 {
						margin: 0 19px 0 16px;
						transform: rotate(-180deg);
					}
				}
			}

			.close_img {
				cursor: pointer;
				opacity: 0.5;
				width: 20px;
				height: 20px;
			}
		}
	}

	.year_txt {
		margin-bottom: 10px;
		font-size: 20px;
		color: #B2B6C5;
		text-align: center;
	}

	.pendingRewards_ul {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		column-gap: 12px;
		row-gap: 12px;

		.pendingRewards_ul_li_no_data {
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			height: 225px;
			padding: 22px 10px 15px 10px;
			box-sizing: border-box;
			background: #2F3445;
			border-radius: 12px;
			border: 4px solid transparent;

			&.pendingRewards_ul_li_no_data_border {
				border-color: #52FB59;
				box-shadow: 0px 0px 10px 0px rgba(148, 239, 90, 0.4);
			}

			.date {
				text-align: center;

				.title_date {
					margin-bottom: 12px;
					font-size: 16px;
					font-weight: bold;
					color: #B2B6C5;
				}

				.txt {
					font-size: 14px;
					font-weight: 600;
					color: #686D7B;

					span {
						color: #686D7B;
					}
				}
			}

			.no_data {
				text-align: center;
				font-size: 14px;
				color: #686D7B;
				line-height: 16px;
			}
		}
	}
}

@media (max-width: 768px) {
	.pendingRewards {
		margin: 23px 10px 10px 10px;
		padding: 0 12px 12px;
		border-radius: 12px;

		.pendingRewards_title {
			padding: 18px 12px 18px 6px;

			.l_box {
				font-size: 12px;

				span {
					font-size: 14px;
				}
			}

			.r_box {
				display: flex;
				align-items: center;

				.img_box {
					img {
						width: 20px;
						height: 20px;

						&.img_2 {
							margin: 0 8px 0 12px;
						}
					}
				}

				.close_img {
					width: 18px;
					height: 18px;
				}

				:deep(.el-affix) {
					width: 18px !important;
					height: 18px !important;
				}
			}
		}

		.year_txt {
			font-size: 14px;
		}

		.pendingRewards_ul {
			grid-template-columns: repeat(2, 1fr);

			.pendingRewards_ul_li_no_data {
				height: 200px;
				padding: 18px 10px 10px 10px;
				border: 2px solid transparent;

				.date {
					.title_date {
						margin-bottom: 11px;
						font-size: 12px;
					}

					.txt {
						font-size: 12px;
					}
				}

				.no_data {
					font-size: 12px;
					line-height: 14px;
				}
			}
		}
	}
}
</style>