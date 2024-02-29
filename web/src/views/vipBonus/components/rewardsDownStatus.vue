<template>
	<div class="rewardsDownStatus">
		<div class="btn" v-if="(dataObj.state == 0 || dataObj.state == 1) && !flag2">
			<div class="sl_box_shadow_green" v-if="flag" @click="receiveBonus(dataObj.day)">
				<div>
					<span>{{ receiveAmount < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(receiveAmount) }}</span>
							<img src="@assets/images/vipBonus/Lightning.png" alt="">
				</div>
			</div>
			<div class="total_num" v-else>{{ receiveNum }} / {{ dataObj.data.length }}</div>
		</div>
		<div class="claim" v-else-if="dataObj.state == 2 || flag2">
			<div class="txt">
				{{ t('vipBonus.Reclame') }} <span>{{ dataObj.wait_bonus < 0.01 ? `<${t('base.currencySymbol')} 0,01` : moneyFormat(dataObj.wait_bonus) }}</span> {{ t('bonusCabinet.Em') }}
			</div>
			<div class="time_box">
				<el-countdown title="" format="HH:mm:ss" :value="Date.now() + dataObj.time * 1000" @finish="finish" />
				<el-popover placement="top" trigger="hover" popper-class="el_popover_style" :teleported="false" width="330">
					<template #reference>
						<!-- <van-icon name="question" /> -->
						<img src="@assets/images/public/query.png" alt="">
					</template>
					<div class="popover_content">
						<div class="popover_content_txt">
							{{ t('vipBonus.Asquantiasresgatáveissãodesbloqueadasdia') }}
						</div>
					</div>
				</el-popover>
			</div>
		</div>
		<div class="thelock" v-else-if="dataObj.state == 3">
			<img src="@assets/images/vipBonus/Thelock.png" alt="">
		</div>
		<!-- <div class="claim" v-else-if="dataObj.state == 1">
			<div class="txt">
				Claim <span>R$0.55</span> in
			</div>
			<el-countdown title="" format="HH:mm:ss" :value="Date.now() + dataObj.time" @finish="finish" />
		</div> -->

		<!-- <el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
			append-to-body width="350px"> -->

		<!-- </el-dialog> -->
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { VipService } from "@/api/vip";
import { debounce, getUserInfo, moneyFormat } from "@/utils/baseFun";
export default defineComponent({
	name: "rewardsDownStatus",
	props: {
		dataObj: Object,
		dataObj2: Object
	},
	setup(props) {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			dataObj: props.dataObj as any,
			flag: false, // 按钮||次数
			flag2: false, // 显示下次领取时间
			receiveAmount: 0, // 可领取金额
			receiveNum: 0, // 领取次数
		});

		// 时间结束
		const finish = () => {
			proxy.$mitt.emit('getVipFinish')
		};

		const getBonus = () => {
			var arr: Array<object> = []
			// 领取次数
			state.receiveNum = 0
			state.dataObj.data.forEach(item => {
				if (item.status == 0) arr.push(item)
				else if (item.status == 1) state.receiveNum += 1
			});

			if (arr.length == 0) state.flag = false
			else {
				// 领取的金额
				state.flag = true
				state.receiveAmount = 0
				arr.forEach(item => {
					state.receiveAmount += item['bonus']
				});
			}
		}

		watch(() => props.dataObj, (val) => {
			state.flag2 = false // 设置默认值
			state.dataObj = val
			getBonus()
			// 设置当天下次领取时间
			for (let i = 0; i < (props.dataObj2 as any).length; i++) {
				const element = (props.dataObj2 as any)[i];
				if (element.status == 0) return state.flag2 = false
				else if (element.status == 3) state.flag2 = true
			}
		}, { deep: true, immediate: true })


		const receiveBonus = (day: string) => {
			const fun = () => {
				VipService.user_get_split_bonus({ day: day }).then(res => {
					if (res.data.code == 1) {
						proxy.$mitt.emit('receiveBonus', res.data.money)
						proxy.$mitt.emit('getVipFinish')
						getUserInfo()
					}
				})
			}
			debounce(fun)
		}
		return { ...toRefs(state), store, t, props, finish, getBonus, receiveBonus, moneyFormat };
	},
});
</script>
<style  lang="scss" scoped>
.rewardsDownStatus {
	text-align: center;

	.btn {
		.sl_box_shadow_green {
			padding: 12px 18px;
			display: inline-block;

			div {
				display: flex;
				align-items: center;

				span {
					margin-right: 6px;
					font-size: 15px;
					font-weight: bold;
					color: #252633;
				}

				img {
					width: 16px;
				}
			}
		}

		.total_num {
			font-size: 14px;
			color: #B2B6C5;
		}
	}

	.thelock {
		img {
			width: 20px;
		}
	}

	.claim {
		.txt {
			margin-bottom: 4px;
			font-size: 14px;
			color: #B2B6C5;

			span {
				color: #75ED3D;
			}
		}

		.time_box {
			display: flex;
			align-items: center;
			justify-content: center;

			img {
				cursor: pointer;
				margin-left: 8px;
				width: 18px;
				transform: translateY(2px);
			}
		}

		:deep(.el-statistic) {
			.el-statistic__number {
				font-size: 16px;
				font-weight: 600;
				color: #FFFFFF;
			}
		}
	}

	:deep(.el-overlay) {
		background: rgba($color: #000000, $alpha: 0.5);
	}
}


@media (max-width: 768px) {
	.rewardsDownStatus {
		.btn {
			.sl_box_shadow_green {
				padding: 12px 14px;

				div {
					span {
						font-size: 13px;
					}

					img {
						width: 12px;
					}
				}
			}

			.total_num {
				font-size: 12px;
			}
		}

		.thelock {
			img {
				width: 20px;
			}
		}

		.claim {
			.txt {
				font-size: 12px;
			}

			.time_box {
				img {
					margin-left: 6px;
					width: 16px;
				}
			}

			:deep(.el-statistic) {
				.el-statistic__number {
					font-size: 14px;
				}
			}
		}
	}
}
</style>
  