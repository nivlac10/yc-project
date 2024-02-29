<template>
	<div>
		<div class="LifetimeReferralBonus">
			<div class="title">
				<p class="">{{ t('vipBonus.RECOMPENSASCALENDÁRIO') }}</p>
				<infoPop :title="t('vipBonus.ComoReceberSuasCalendário')"
					:content="t('vipBonus.ComoReceberSuasCalendárioTxt')">
				</infoPop>
			</div>
			<div class="head">
				<div class="headItem">
					<div class="headItemItem">
						<p class="check">
							{{ moneyFormat(state.total_money) }}
						</p>
						<span>
							{{ t('vipBonus.AguardandoResgate') }}
						</span>
					</div>

					<div class="headItemItem">
						<p>
							{{ moneyFormat(store.state.user.vip_earnings) }}
						</p>
						<span>
							{{ t('vipBonus.Recebida') }}
						</span>
					</div>
					<!-- <div class="Line"></div>-->

				</div>
				<div class="headItem rit">
					<p @click="showPage"> {{ t('vipBonus.VerBônusPendentesparaResgate') }}</p>
					<div class="pagination">
						<img src="@/assets/images/public/popover_return.png" alt="" @click="ChangeCarouselPage('left')">
						<img src="@/assets/images/public/popover_return.png" alt="" @click="ChangeCarouselPage('rit')">
					</div>
				</div>
			</div>
			<div class="body">
				<el-carousel ref="calendarCarousel" :autoplay="false" arrow="never" :loop="false" indicator-position="none"
					:initial-index="state.initialIndex">
					<el-carousel-item v-for="(item, index) in state.list" :key="index" :name="index">
						<!-- <el-row :gutter="store.state.status.isPc ? 24 : 10">
                <el-col v-for="(item2, index2) in (item as any)" :key="index2" :xs="12" :sm="6" :md="6" :lg="6"
                    :xl="6"> -->
						<!-- <vip-box :data="item2" />  -->
						<!-- <div class="bodyItem">
                        <p>July 31</p>
                        <span>R$ 0.00</span>
                        <span>No Reward</span>
                    </div> -->
						<div class="bodyBox">
							<div class="bodyBox_item" v-for="(item2, index2) in (item as any)" :key="index2">
								<rewards-com @def="getList" :data="item2" v-if="item2['total_bonus']" />
								<div :class="{ pendingRewards_ul_li_no_data: true, check: item2.state == 0 || item2.day == getDate(0) }"
									v-else>
									<div class="date">
										<div class="title_date">{{ getDate(0) == item2['day'] ? t('vipBonus.Hoje') :
											englishFormatDate(item2['day']) }}
										</div>
										<div class="txt">
											<span>{{ t('base.currencySymbol') }} 0,00</span>
										</div>
									</div>
									<div class="no_data">
										<p> {{ t('vipBonus.Sem') }}</p>
										<p>{{ t('vipBonus.Recompensa') }}</p>
									</div>
									<div></div>
								</div>

							</div>
						</div>


						<!-- </el-col>
            </el-row> -->
					</el-carousel-item>
				</el-carousel>
			</div>


			<pending-rewards v-if="state.pendingRewardsShow" />

			<div class="bottom">
				<p><span @click="jump('/vipBonus/vipDetails')"> {{ t('vipBonus.Explicaçãosobre') }}</span>
					<img src="@/assets/images/vipBonus/arrow.png" alt="">
				</p>

			</div>

			<div v-if="state.isBonusPop" class="bounsPop_box  mask" @click="state.isBonusPop = false">
				<div class="pop_box" @click.stop>
					<bounsPop :comIdx="state.comIdx" :now_bonus="state.now_bonus_pop" :split_bonus="state.split_bonus_pop"
						@close-pop="state.isBonusPop = false"></bounsPop>
				</div>
			</div>
		</div>

		<div class="body body2">
			<div class="bodyItem bodyItem2">
				<div class="bodyItemLeft">
					<div class="bodyItem2_top">
						<span>{{ t('bonusCabinet.BônusCashback') }}</span>

						<infoPop :title="t('bonusCabinet.BônusCashback')" :content="t('bonusCabinet.p_id_5')">
						</infoPop>
					</div>
					<img src="../../../assets/images/header/Chest.png" alt="" class="img">
				</div>

				<!-- <div class="btn sl_box_shadow ">
                    <img src="../../../assets/images/refer/RETIRADA.png" alt="">
                    <p>ADICIONAR</p>
                </div> -->

				<!-- <el-tooltip class="box-item" effect="dark" :content="'Abriu a fechadura às ' + state.now_time" placement="top"
					:disabled="state.now_bonus.time <= 0">
					<div @click="get_bonus(1)" class="btn sl_box_shadow">
						<div v-if="state.now_bonus.state == 0" class="btnMask"></div>
						<img src="../../../assets/images/refer/RETIRADA.png" alt="">
						<p>Adicionar {{ state.now_bonus.money > 0 ? 'R$ ' + state.now_bonus.money.toFixed(2) : '' }}</p>
					</div>
				</el-tooltip> -->

				<el-tooltip class="box-item" effect="customized"
					:content="t('bonusCabinet.Abriuafechaduraàs') + store.state.vipBonusState.now_time" placement="top"
					:disabled="store.state.vipBonusState.now_bonus.time <= 0" popper-class="el-tooltip_bg">
					<div @click="get_bonus(1)" class="btn sl_box_shadow">
						<div v-if="store.state.vipBonusState.now_bonus.state == 0" class="btnMask"></div>
						<img src="../../../assets/images/refer/RETIRADA.png" alt="">
						<p>{{ t('btnName.Adicionar') }} {{ store.state.vipBonusState.now_bonus.money > 0 ?
							moneyFormat(store.state.vipBonusState.now_bonus.money) : '' }}</p>
					</div>
				</el-tooltip>

				<!-- <el-tooltip class="box-item" effect="dark" :content="'Abriu a fechadura às ' + store.state.vipBonusState.now_time"
					placement="top" :disabled="store.state.vipBonusState.now_bonus.time <= 0">
				</el-tooltip> -->

				<!-- <el-popover placement="top" trigger="hover" popper-class="el_popover_style" :teleported="false" :hide-after="0"
					width="220">
					<template #reference>
						<div @click="get_bonus(1)" class="btn sl_box_shadow">
							<div v-if="store.state.vipBonusState.now_bonus.state == 0" class="btnMask"></div>
							<img src="../../../assets/images/refer/RETIRADA.png" alt="">
							<p>Adicionar {{ store.state.vipBonusState.now_bonus.money > 0 ? 'R$ ' +
								store.state.vipBonusState.now_bonus.money.toFixed(2) : '' }}</p>
						</div>
					</template>
					<div class="popover_content">
						<div class="popover_content_txt">
							Abriu a fechadura às {{ store.state.vipBonusState.now_time }}
						</div>
					</div>
				</el-popover> -->

			</div>
			<div class="bodyItem bodyItem2">
				<div class="bodyItemLeft">
					<div class="bodyItem2_top">
						<span>{{ t('bonusCabinet.BônusDiário') }}</span>

						<infoPop :title="t('bonusCabinet.BônusDiário')" :content="t('bonusCabinet.p_id_6')">
						</infoPop>
					</div>

					<img src="../../../assets/images/header/Chest2.png" alt="" class="img">
				</div>
				<div :class="{ btn: true, sl_box_shadow: store.state.vipBonusState.day_bonus.time == 0, no_bonus_box: store.state.vipBonusState.day_bonus.time > 0 }"
					@click="get_bonus(2)">
					<img v-if="state.btn_loading_2" src="@assets/images/public/btn_loading.gif" alt="">
					<div v-if="store.state.vipBonusState.day_bonus.state == 0" class="btnMask"></div>
					<img v-if="store.state.vipBonusState.day_bonus.state == 0 && store.state.vipBonusState.day_bonus.time != 0"
						src="../../../assets/images/header/RETIRADA@2x.png" alt="">
					<img v-else src="../../../assets/images/refer/RETIRADA.png" alt="">
					<p v-if="store.state.vipBonusState.day_bonus.state == 1">{{ t('btnName.Adicionar') }}</p>
					<p v-if="store.state.vipBonusState.day_bonus.time > 0"
						style="color: #B2B6C5;transform: translateY(2px);">{{
							store.state.vipBonusState.day_time
						}}</p>
					<p
						v-if="store.state.vipBonusState.day_bonus.state == 0 && store.state.vipBonusState.day_bonus.time == 0">
						{{ t('btnName.Adicionar') }}</p>
				</div>
			</div>

			<div class="bodyItem bodyItem2">
				<div class="bodyItemLeft">
					<div class="bodyItem2_top">
						<span>{{ t('bonusCabinet.BônusSemanal') }}</span>

						<infoPop :title="t('bonusCabinet.BônusSemanal')" :content="t('bonusCabinet.p_id_7')">
						</infoPop>
					</div>

					<img src="../../../assets/images/header/Chest3.png" alt="" class="img">
				</div>
				<div class="btn sl_box_shadow" @click="get_bonus(3)">
					<img v-if="state.btn_loading_3" src="@assets/images/public/btn_loading.gif" alt="">
					<div v-if="store.state.vipBonusState.week_bonus.state == 0" class="btnMask"></div>
					<img src="../../../assets/images/refer/RETIRADA.png" alt="">
					<p>{{ t('btnName.Adicionar') }}</p>
				</div>
			</div>

			<div class="bodyItem bodyItem2">
				<div class="bodyItemLeft">
					<div class="bodyItem2_top">
						<span>{{ t('bonusCabinet.BônusMensal') }}</span>

						<infoPop :title="t('bonusCabinet.BônusMensal')" :content="t('bonusCabinet.p_id_8')">
						</infoPop>
					</div>

					<img src="../../../assets/images/header/Chest4.png" alt="" class="img">
				</div>
				<div class="btn sl_box_shadow" @click="get_bonus(4)">
					<img v-if="state.btn_loading_4" src="@assets/images/public/btn_loading.gif" alt="">
					<div v-if="store.state.vipBonusState.month_bonus.state == 0" class="btnMask"></div>
					<img src="../../../assets/images/refer/RETIRADA.png" alt="">
					<p>{{ t('btnName.Adicionar') }}</p>
				</div>
			</div>

		</div>

		<receive-bonus />
	</div>
</template>

<script setup lang="ts">
import {
	reactive,
	computed,
	watch,
	toRefs,
	nextTick,
	getCurrentInstance,
	defineComponent,
	onMounted,
	ref,
	onBeforeUnmount
} from "vue";
import { useStore } from "@/store/index";
import { VipService } from "@/api/vip";
import { getUserInfoNoLoad, getDate, sliceArr, englishFormatDate, moneyFormat } from '@/utils/baseFun';
import infoPop from "./infoPop.vue";
import rewardsCom from "./rewardsCom.vue";
import router from "@/router";
import pendingRewards from "../childrens/pendingRewards.vue";
import bounsPop from '@/views/vipBonus/components/bounsPop.vue';
import receiveBonus from "./receiveBonus.vue"
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const { proxy } = getCurrentInstance() as any;

const store = useStore();
const state = reactive({
	// day_time: '00:00',
	list: [1, 2, 3, 4, 5],
	now_bonus_pop: 0,
	split_bonus_pop: 0,
	total_money: 0,
	isBonusPop: false,
	comIdx: 0,
	initialIndex: 0,
	pendingRewardsShow: false,
	btn_loading_2: false,
	btn_loading_3: false,
	btn_loading_4: false,
})
let btnsStatus = ref();

const calendarCarousel = ref(null);

const ChangeCarouselPage = (direction) => {
	if (direction == 'left') {
		(calendarCarousel as any).value.prev()
	} else {
		(calendarCarousel as any).value.next();
	}
}

//获取奖金按钮状态
const getData = async () => {
	if (store.state.user.token != '') {
		let data = await VipService.get_user_vip_bonus_state({});
		btnsStatus.value = data.data.data;
		const obj = {
			now_bonus: data.data.data.now_bonus,
			week_bonus: data.data.data.week_bonus,
			month_bonus: data.data.data.month_bonus,
			day_bonus: data.data.data.day_bonus,
			split_bonus: data.data.data.split_bonus,
			lv_up_bonus: data.data.data.lv_up_bonus,
			badgeShow: data.data.bonus_num > 0 ? true : false,
			bonus_num: data.data.bonus_num,
		}
		store.dispatch("vipBonusState/setData", obj);
	}
}

getData();

// 领取立即反水
const get_bonus = (index) => {
	switch (index) {
		case 1:
			if (store.state.vipBonusState.now_bonus.time <= 0 && store.state.vipBonusState.now_bonus.state == 1) {
				VipService.user_get_now_vip_bonus().then((res) => {
					if (res.data.code == 1) {
						getData()
						getUserInfoNoLoad()
						proxy.$mitt.emit('getVipFinish')
						state.isBonusPop = true
						state.now_bonus_pop = res.data.bonus
						state.split_bonus_pop = res.data.split_bonus
						state.comIdx = index
					}
				})
			}
			break;
		case 2:
			if (store.state.vipBonusState.day_bonus.state == 1 && store.state.vipBonusState.day_bonus.money > 0) {
				state.btn_loading_2 = true
				VipService.user_get_day_vip_bonus().then((res) => {
					if (res.data.code == 1) {
						getData()
						getUserInfoNoLoad()
						proxy.$mitt.emit('getVipFinish')
						state.isBonusPop = true
						state.now_bonus_pop = res.data.bonus
						state.split_bonus_pop = res.data.split_bonus
						state.comIdx = index
						state.btn_loading_2 = false
					}
				})
			}
			break;
		case 3:
			if (store.state.vipBonusState.week_bonus.state == 1 && store.state.vipBonusState.week_bonus.money > 0) {
				state.btn_loading_3 = true
				VipService.user_get_week_vip_bonus().then((res) => {
					if (res.data.code == 1) {
						getData()
						getUserInfoNoLoad()
						proxy.$mitt.emit('getVipFinish')
						state.isBonusPop = true
						state.now_bonus_pop = res.data.bonus
						state.split_bonus_pop = res.data.split_bonus
						state.comIdx = index
						state.btn_loading_3 = false
					}
				})
			}
			break;
		case 4:
			if (store.state.vipBonusState.month_bonus.state == 1 && store.state.vipBonusState.month_bonus.money > 0) {
				state.btn_loading_4 = true
				VipService.user_get_month_vip_bonus().then((res) => {
					if (res.data.code == 1) {
						getData()
						getUserInfoNoLoad()
						proxy.$mitt.emit('getVipFinish')
						state.isBonusPop = true
						state.now_bonus_pop = res.data.bonus
						state.split_bonus_pop = res.data.split_bonus
						state.comIdx = index
						state.btn_loading_4 = false
					}
				})
			}
			break;
		default:
			break;
	}


}

const showPage = () => {
	state.pendingRewardsShow = true
}
proxy.$mitt.on('pendingRewardsShow', () => {
	state.pendingRewardsShow = false
	getList()
})
//获取日历数据
const getList = () => {
	VipService.get_user_split_bonus_list().then(res => {
		state.total_money = res.data.total_money
		// 设置默认时间
		let arr = [];
		// if (store.state.status.isPc) {
		var index = 0;
		var index2 = 0;
		for (let i = 0; i < 7; i++) {
			index -= 1
			arr.unshift({ day: getDate(index) } as never)
			if (arr[i]['day'] == getDate(0)) {
				(arr[i] as any).state = 0;
			}
		}
		for (let i = 0; i < 8; i++) {
			arr.push({ day: getDate(index2) } as never)
			if (arr[i]['day'] == getDate(0)) {
				(arr[i] as any).state = 0;
			}
			index2 += 1
		}
		// } else {
		// 	var index = 0;
		// 	for (let i = 0; i < 6; i++) {
		// 		arr.push({ day: getDate(index) } as never)
		// 		if (arr[i]['day'] == getDate(0)) {
		// 			(arr[i] as any).state = 0;
		// 		}
		// 		index += 1
		// 	}
		// }
		if (res.data.data.length == 0) {
			// (state.list[1] as any) = {day : getDate(0)};
			state.list = sliceArr([...arr], store.state.status.isPc ? 5 : 2);
		} else {
			var num = store.state.status.isPc ? 5 : 2
			if (res.data.data.length < 5) {
				// for (let i = 0; i < arr.length; i++) {
				// 	const element = arr[i];
				// 	for (let j = 0; j < res.data.data.length; j++) {
				// 		let element2 = { ...res.data.data[j] };
				// 		// 给默认数据赋值
				// 		if (element['day'] == element2['day']) {
				// 			arr[i] = element2 as never
				// 		}
				// 	}
				// }
				// state.list = sliceArr([...arr], num);
				setListData(arr, res, num)
			} else {
				let flag: boolean = false
				res.data.data.forEach(item => {
					if (item.day == getDate(0)) {
						flag = true
					}
				});
				if (flag) state.list = sliceArr([...res.data.data], num);
				else {
					// for (let i = 0; i < arr.length; i++) {
					// 	const element = arr[i];
					// 	for (let j = 0; j < res.data.data.length; j++) {
					// 		let element2 = { ...res.data.data[j] };
					// 		// 给默认数据赋值
					// 		if (element['day'] == element2['day']) {
					// 			arr[i] = element2 as never
					// 		}
					// 	}
					// }
					// state.list = sliceArr([...arr], num);
					setListData(arr, res, num)
				}
			}
		}
		setActiveItem() // 设置轮播图索引
	})
}
getList()

const setListData = (arr: Array<any>, res: any, num: number) => {
	for (let i = 0; i < arr.length; i++) {
		const element = arr[i];
		for (let j = 0; j < res.data.data.length; j++) {
			let element2 = { ...res.data.data[j] };
			// 给默认数据赋值
			if (element['day'] == element2['day']) {
				arr[i] = element2 as never
			}
		}
	}
	state.list = sliceArr([...arr], num);
}

// 设置轮播图索引
const setActiveItem = () => {
	for (let i = 0; i < state.list.length; i++) {
		const element: Array<any> = state.list[i] as any;
		for (let j = 0; j < element.length; j++) {
			const element2 = element[j];
			if (element2['state'] == 0 || element2['day'] == getDate(0)) {
				nextTick(() => {
					(calendarCarousel.value as any).setActiveItem(i)
				})
			}
		}
	}
}

watch(
	() => store.state.status.isPc,
	(val: boolean) => {
		state.list = sliceArr(state.list, val ? 5 : 2);
	},
	{ deep: true, immediate: true }
);

const jump = (path) => {
	router.push(path)
}

proxy.$mitt.on('getVipFinish', () => { getList() })

onBeforeUnmount(() => {
})
</script>

<style scoped lang="scss">
:deep(.el_popover_style) {
	// min-width: 220px !important;
	// width: 100% !important;
	// padding: 0 !important;
	border: none !important;
	border-radius: 8px !important;
	font-size: 20px !important;
	background: #2F3445 !important;
	box-shadow: 0px 0px 12px 0px rgba(0, 0, 0, .4) !important;

	.popover_content {
		padding: 0px 0;
		// white-space: nowrap;

		.popover_content_txt {
			// display: flex;
			width: 100% !important;
			font-size: 14px !important;
			font-weight: 400 !important;
			color: var(--auxiliary-font-color-9) !important;

		}
	}

	.el-popper__arrow {
		&::before {
			background: #2F3445 !important;
			border: none !important;
		}
	}
}

:deep(.is-guttered) {
	display: flex;
	justify-content: center;
}

:deep(.el-carousel__container) {
	height: 250px;
}

.bounsPop_box {
	display: flex !important;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	width: 100%;
	height: 100%;

	.pop_box {
		position: relative;
	}
}

.LifetimeReferralBonus {
	width: 100%;
	background: #202431;
	border-radius: 12px;
	padding: 28px 24px 23px 24px;
	box-sizing: border-box;

	.title {
		display: flex;
		align-items: center;
		padding-left: 8px;

		p {
			color: #B2B6C5;
			font-size: 24px;
			line-height: 35px;
			font-weight: bold;
			margin-right: 10px;
		}
	}


	:deep(.rewardsCom) {
		min-height: 100%;
		width: 100%;

		.rewardsDownStatus {
			.total_num {
				// transform: translateY(-4px);
			}
		}
	}

	.head {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		width: 100%;
		column-gap: 20px;
		margin-bottom: 16px;
		padding-left: 8px;
		box-sizing: border-box;

		.headItem {
			height: 100%;
			// background: rgba(44, 51, 63, 1);
			// border-radius: 20px;
			// display: grid;
			// grid-template-columns: 1fr 1fr;
			display: flex;
			align-items: center;
			justify-items: self-start;
			box-sizing: border-box;
			// margin-left: 17px;

			.headItemItem {
				cursor: pointer;
				color: #fff;
				display: flex;
				// flex-direction: column;
				flex-direction: row-reverse;
				column-gap: 10PX;
				justify-content: center;
				align-items: center;
				padding: 8px 0;
				margin-right: 27px;
				color: #B2B6C5;

				p {
					font-size: 16px;
					font-weight: bold;
					text-align: center;
				}

				span {
					font-size: 16px;
					text-align: center;
				}
			}

			.headItemItem:nth-child(2) {
				p {
					font-size: 14px;
					text-align: center;
				}
			}

			.check {
				color: rgba(117, 237, 61, 1);
				font-size: 20px !important;
			}

			.Line {
				width: 4px;
				height: 60px;
				background: rgba(102, 109, 121, 1);
				border-radius: 2px;
			}


		}

		.rit {
			display: flex;
			justify-content: flex-end;

			p {
				color: #F3B343;
				// border-bottom: 2px solid #F3B343;
				cursor: pointer;
			}
		}
	}

	.pagination {
		display: flex;
		align-items: center;
		column-gap: 20px;
		margin-left: 20px;

		img {
			width: 41px;
			height: 41px;
			cursor: pointer;

			&:nth-child(2) {
				transform: rotate(-180deg);
			}
		}
	}


	.pendingRewards_ul_li_no_data {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		height: 100%;
		max-height: 250px;
		width: 100%;
		padding: 20px 10px 10px 10px;
		box-sizing: border-box;
		background: #2F3445;
		border-radius: 12px;
		border: 2px solid transparent;

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
				font-weight: 500;
				color: #686D7B;

				span {
					color: #686D7B;
				}
			}
		}

		.no_data {
			text-align: center;
			font-size: 14px;
			font-weight: 400;
			color: #686D7B;
			line-height: 16px;
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

.body {
	box-sizing: border-box;
	border-radius: 20px;

	.bodyBox {
		display: grid;
		grid-template-columns: repeat(5, 1fr);
		width: 100%;
		height: 100%;
		gap: 16px;
		column-gap: 16px;
	}

	.bodyItem {
		height: 290px;
		border-radius: 12px;
		background: #404958;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		p {
			color: #B2B6C5;
			font-size: 16px;
			font-weight: bold;
			margin-bottom: 37px;

		}

		span {
			color: #B2B6C5;
			font-size: 16px;
			// margin-bottom: 56px;
		}
	}

	.no_bonus_box {
		background-color: transparent !important;
		padding: 10px 14px !important;
		display: flex;
		gap: 5px;
		box-sizing: border-box;
		// width: 179px;
		height: 54px;

		.btnMask {
			display: none !important;
		}

		p {
			color: #B2B6C5 !important;
		}
	}

	.check {

		border: 4px solid #52FB59;

		box-shadow: 0px 0px 5px 0px rgba(148, 239, 90, 0.4);
	}

	.bodyItem2 {
		display: flex;
		flex-direction: column;
		justify-content: flex-start;

		.bodyItemLeft {
			display: flex;
			align-items: center;
			flex-direction: column;
			width: 100%;
		}

		p {
			margin: 0;
		}

		.bodyItem2_top {
			display: flex;
			justify-content: space-between;
			align-items: center;
			width: 100%;
			padding: 24px 24px 0 24px;
			box-sizing: border-box;

			>div {
				display: inline-block;
				vertical-align: middle;
				margin-left: 7px;
			}

			// div {
			// 	width: 24px;
			// 	height: 24px;
			// 	background: #C3CFD9;
			// 	border-radius: 50%;
			// 	display: flex;
			// 	justify-content: center;
			// 	align-items: center;
			// 	font-weight: bold;
			// 	font-size: 20px;
			// 	color: #404958;
			// 	cursor: pointer;
			// 	margin-left: 5px;
			// }
		}

		.img {
			margin-top: 27px;
			width: 138px;
			margin-bottom: 10px;
		}

		.btn {
			cursor: pointer;
			display: flex;
			align-items: center;
			justify-content: center;
			padding: 14px 15px 17px 15px;
			border-radius: 12px;
			position: relative;
			min-width: 178px;

			p {
				color: #1B1D29;
				font-size: 16px;
				font-weight: bold;
				transform: translateY(2px);
				flex-shrink: 0;
			}

			img {
				width: 18.74px;
				margin-right: 8px;
			}

			.btnMask {
				content: "";
				cursor: pointer;
				background: rgba(5, 5, 5, 0.432);
				position: absolute;
				top: 0;
				left: 0;
				width: 100%;
				height: 100%;
				z-index: 2;
				border-radius: 12px;
			}
		}
	}
}


.body2 {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: 16px;
	padding: 16px 0;

	.bodyItem {
		background: #202431;
	}

}



@media (max-width:768px) {

	:deep(.el-carousel__container) {
		height: 220px;
	}

	.LifetimeReferralBonus {
		padding: 18px 6px 12px 6px;
		border-radius: 12px;

		.title {
			margin-left: 0px;
			margin-bottom: 18px;

			p {
				line-height: 16px;
				font-size: 14px;
				margin-right: 16px;
			}


		}

		.head {
			grid-template-columns: 1fr;
			row-gap: 12px;
			height: auto;
			padding: 0;

			.headItem {
				border-radius: 12px;
				flex-direction: column;
				align-items: baseline;
				background: #2F3445;
				padding: 11px 12px;

				p {
					font-size: 14px;
					line-height: 16.41px;

				}

				.headItemItem:nth-child(2) {
					p {
						font-size: 12px;
					}
				}

				.check {
					font-size: 16px !important;
				}

				.headItemItem {
					padding: 5px 0;

					p {
						font-size: 12px;
					}

					span {
						font-size: 12px;
					}
				}
			}

			.rit {
				flex-direction: row;
				align-items: center;
				justify-content: space-between;
				padding: 0px 6px 0 8px;

				p {
					border: none;
				}
			}
		}


		.pendingRewards_ul_li_no_data {
			height: 220px;
			width: 100%;

			// max-height: 170px;
			.date {
				.title_date {
					margin-bottom: 11px;
					font-size: 12px;
				}

				.txt {
					font-size: 12px;
				}
			}
		}




		.pagination {
			margin-left: 0px;
			padding: 11px 9px;
			column-gap: 5px;

			img {
				width: 28px;
				height: 28px;
			}
		}

		.no_bonus_box {
			width: 97px;
			height: 38px;
		}

		.bottom {

			p {
				display: block;
				font-size: 13px;
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

	.body {
		grid-template-columns: repeat(2, 1fr);
		padding: 0;
		border-radius: 12px;
		margin-top: 12px;

		.bodyBox {
			grid-template-columns: repeat(2, 1fr);
			gap: 13px;
			display: flex;
			// justify-content: center;

			.bodyBox_item {
				width: 50%;

				.rewardsCom {
					width: 100%;
				}
			}
		}

		.bodyItem {
			height: 160px;

			p {
				margin-bottom: 8px;
				font-size: 13px;

			}

			span {
				margin-bottom: 36px;
				font-size: 12px;
			}
		}

		.check {
			border: 2px solid #52FB59;
		}

		.bodyItem2 {
			background: transparent;
			flex-direction: row;
			justify-content: space-between;
			height: auto;
			align-items: center;

			.bodyItemLeft {
				width: auto;
				display: flex;
				flex-direction: row-reverse;
			}

			.img {
				width: 39px;
				height: 39px;
				margin: 0;
			}

			.btn {
				padding: 13px 8px;
				min-width: 91px;
				border-radius: 8px;

				p {
					font-size: 12px;
					margin: 0;
					transform: translateY(0);
				}

				img {
					width: 12px;
					margin-right: 3px;
				}

				.btnMask {
					content: "";
					cursor: pointer;
					background: rgba(5, 5, 5, 0.432);
					position: absolute;
					top: 0;
					left: 0;
					width: 100%;
					height: 100%;
					z-index: 2;
					border-radius: 8px;
				}
			}

			.bodyItem2_top {
				display: block;
				padding: 4px;
				gap: 10px;
				justify-content: left !important;

				p {
					margin: 0;
				}

				// div {
				// 	width: 15px !important;
				// 	height: 15px !important;
				// 	font-size: 12px;
				// 	margin: 0 2px 0 2px;
				// }

			}

		}
	}

	.body2 {
		grid-template-columns: repeat(1, 1fr);
		padding: 15px 9px;
		// row-gap: 10px;
		background: #202431;
		margin-bottom: 12px;
	}
}

:deep(.el-row) {
	height: 100% !important;
}
</style>