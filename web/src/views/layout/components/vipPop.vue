<template>
	<div v-show="store.state.user.token != ''">
		<div class="Recompensas" @click="shhowPop">
			<el-badge :value="store.state.vipBonusState.bonus_num" class="item" type="success"
				:hidden="!store.state.vipBonusState.badgeShow">
				<img src="@/assets/images/header/cashback-monthly.png" alt="">
			</el-badge>
			<p>{{ t('bonusCabinet.RECOMPENSAS') }}</p>
			<img src="@/assets/images/header/Vector.png" alt="" class="arr" />
			<!-- <img src="@/assets/images/header/Vector.png" alt="" class="arr"
				:style="isShowPop ? '  transform: rotate(180deg);  ' : '  transform: rotate(0deg);  '"> -->
		</div>

		<div :class="{ popShow: isShowPop, mask: true }" @click="isShowPop = false">
			<div class="pop" @click.stop>
				<div class="item">
					<div class="left">
						<img src="@/assets/images/bonusCabinet/calendar.png" alt="">
						<div class="txt imgTxt">
							<p>{{ t('signIn.Checkindiário') }}</p>
							<img :src="vipImg" alt="" @click="showVipPop">
						</div>
					</div>
					<div class="btn2 sl_box_shadow" @click="get_bonus(5)">
						<div v-if="store.state.vipBonusState.sgin_data['state'] !== 1" class="btn_mask"></div>
						<div v-if="store.state.vipBonusState.sgin_data['state'] == 1" style="display: flex;">
							<img v-if="state.btn_loading_checkIn" src="@assets/images/public/btn_loading.gif" alt="">
							<p v-if="store.state.vipBonusState.sgin_data['money'] == 0">{{ t('btnName.checkin') }}</p>
							<p v-else>{{ t('base.currencySymbol') }} {{ store.state.vipBonusState.sgin_data['money'] }}</p>
						</div>
						<el-countdown v-else title="" format="HH:mm:ss"
							:value="Date.now() + (store.state.vipBonusState.sgin_data['time'] * 1000)" @finish="finish" />
					</div>

				</div>
				<div class="item">
					<div class="left">
						<img src="@/assets/images/header/Goldcoin.png" alt="">
						<div class="txt">
							<p>{{ t('bonusCabinet.Calendário') }}</p>
							<p style="color: #75ED3D;font-weight: 400;">{{ t('bonusCabinet.Pendentes') }} {{
								moneyFormat(store.state.vipBonusState.split_bonus.total_money)
							}}</p>
							<!-- <span class="check">Pending: ₱ 0.00</span> -->
						</div>
					</div>
					<div class="btn2 btn2_item_1 sl_box_shadow_green" @click="router.push('/vipBonus'), isShowPop = false">

						<div v-if="store.state.vipBonusState.split_bonus.state == 0" class="btn_mask"></div>
						<p v-if="store.state.vipBonusState.split_bonus.money > 0">{{ t('btnName.Receber') }} {{
							store.state.vipBonusState.split_bonus.money > 0 ?
							store.state.vipBonusState.split_bonus.money < 0.01 ? `<${moneyFormat(0.01)}` :
								moneyFormat(store.state.vipBonusState.split_bonus.money) : '' }}</p>
								<p v-if="store.state.vipBonusState.split_bonus.wait_money > 0">
									{{ t('btnName.Receber') }} {{
										store.state.vipBonusState.split_bonus.wait_money > 0 ?
										store.state.vipBonusState.split_bonus.wait_money < 0.01 ? `<${moneyFormat(0.01)}` :
											moneyFormat(store.state.vipBonusState.split_bonus.wait_money) : '' }} </p>
										<p
											v-if="store.state.vipBonusState.split_bonus.state == 0 && store.state.vipBonusState.split_bonus.time == 0">
											{{ t('btnName.Receber') }}</p>
										<p class="btn2_item_1_p"
											v-if="store.state.vipBonusState.split_bonus.state == 0 && store.state.vipBonusState.split_bonus.time > 0">
											{{ t('bonusCabinet.Em') }} {{
												state.split_time }}
										</p>

					</div>

				</div>

				<div class="item">
					<div class="left">
						<img src="@/assets/images/header/Chest.png" alt="">
						<div class="txt">
							<p>{{ t('bonusCabinet.BônusCashback') }}</p>
						</div>
					</div>
					<el-tooltip class="box-item" effect="customized"
						:content="'Abriu a fechadura às ' + store.state.vipBonusState.now_time" placement="top"
						:disabled="store.state.vipBonusState.now_bonus.time <= 0" popper-class="el-tooltip_bg">
						<div @click="get_bonus(1)" class="btn2 sl_box_shadow">
							<div v-if="store.state.vipBonusState.now_bonus.state == 0" class="btn_mask"></div>
							<img src="../../../assets/images/refer/RETIRADA.png" alt="">
							<p>{{ t('btnName.Adicionar') }} {{ store.state.vipBonusState.now_bonus.money > 0 ?
								moneyFormat(store.state.vipBonusState.now_bonus.money) : '' }}</p>
						</div>
					</el-tooltip>
				</div>

				<div class="item">
					<div class="left">
						<img src="@/assets/images/header/Chest2.png" alt="">
						<div class="txt">
							<p>{{ t('bonusCabinet.BônusDiário') }}</p>
						</div>
					</div>
					<div :class="{ btn2: true, sl_box_shadow: store.state.vipBonusState.day_bonus.time == 0, no_bonus_box: store.state.vipBonusState.day_bonus.time > 0 }"
						@click="get_bonus(2)">
						<img v-if="state.btn_loading_2" src="@assets/images/public/btn_loading.gif" alt="">
						<div v-if="store.state.vipBonusState.day_bonus.state == 0" class="btn_mask"></div>
						<img v-if="store.state.vipBonusState.day_bonus.state == 0 && store.state.vipBonusState.day_bonus.time != 0"
							src="../../../assets/images/header/RETIRADA@2x.png" alt="">
						<img v-else src="../../../assets/images/refer/RETIRADA.png" alt="">
						<p v-if="store.state.vipBonusState.day_bonus.state == 1">{{ t('btnName.Adicionar') }}</p>
						<p v-if="store.state.vipBonusState.day_bonus.time > 0">{{ store.state.vipBonusState.day_time }}</p>
						<p
							v-if="store.state.vipBonusState.day_bonus.state == 0 && store.state.vipBonusState.day_bonus.time == 0">
							{{ t('btnName.Adicionar') }}</p>
					</div>
				</div>

				<div class="item">
					<div class="left">
						<img src="@/assets/images/header/Chest3.png" alt="">
						<div class="txt">
							<p>{{ t('bonusCabinet.BônusSemanal') }}</p>
							<p>{{ t('bonusCabinet.Lançadoàssegundafeiras') }}</p>
						</div>
					</div>
					<div class="btn2 sl_box_shadow" @click="get_bonus(3)">
						<img v-if="state.btn_loading_3" src="@assets/images/public/btn_loading.gif" alt="">
						<div v-if="store.state.vipBonusState.week_bonus.state == 0" class="btn_mask"></div>
						<img src="../../../assets/images/refer/RETIRADA.png" alt="">
						<p>{{ t('btnName.Adicionar') }}</p>
					</div>

				</div>
				<div class="item">
					<div class="left">
						<img src="@/assets/images/header/Chest4.png" alt="">
						<div class="txt">
							<p>{{ t('bonusCabinet.BônusMensal') }}</p>
							<p>{{ t('bonusCabinet.Lançadonoiníciodecadamês') }}</p>
						</div>
					</div>
					<div class="btn2 sl_box_shadow" @click="get_bonus(4)">
						<img v-if="state.btn_loading_4" src="@assets/images/public/btn_loading.gif" alt="">
						<div v-if="store.state.vipBonusState.month_bonus.state == 0" class="btn_mask"></div>
						<img src="../../../assets/images/refer/RETIRADA.png" alt="">
						<p>{{ t('btnName.Adicionar') }}</p>
					</div>

				</div>
				<div class="toVip" @click="router.push('/vipBonus'), isShowPop = false" style="cursor: pointer;">
					<p>{{ t('bonusCabinet.Verifiqueapáginadebônus') }} <img src="@/assets/images/vipBonus/arrow.png" alt="">
					</p>
				</div>
			</div>

		</div>
		<div v-if="isBonusPop" class="bounsPop_box  mask" @click="isBonusPop = false">
			<div class="pop_box" @click.stop>
				<bounsPop :comIdx="state.comIdx" :now_bonus="state.now_bonus_pop" :split_bonus="state.split_bonus_pop"
					@close-pop="isBonusPop = false"></bounsPop>
			</div>
		</div>
	</div>

</template>

<script setup lang="ts">
import { ref, reactive, getCurrentInstance, watch, onBeforeUnmount, computed } from 'vue';
import { debounce, getUserInfo } from "@/utils/baseFun";
import { useStore } from "@/store/index";
import { VipService } from "@/api/vip";
import { getUserInfoNoLoad, moneyFormat, getImageUrl } from '@/utils/baseFun';
import { useRouter } from "vue-router";
import bounsPop from '@/views/vipBonus/components/bounsPop.vue';
import { useI18n } from "vue-i18n";
import { UserService } from '@/api/user';
import promptPopup from '@/components/promptPopup';
import { ElNotification } from 'element-plus'

const { proxy } = getCurrentInstance() as any;
const store = useStore();
const router = useRouter();
const { t } = useI18n();

const state = reactive({
	split_time: '00:00',
	now_bonus_pop: 0,
	split_bonus_pop: 0,
	comIdx: 0,
	btn_loading_2: false,
	btn_loading_3: false,
	btn_loading_4: false,
	btn_loading_checkIn: false,
	count: 0,
	signIndata: {},
})
let isBonusPop = ref(false)
let isShowPop = ref(false);
let vipImg = ref(getImageUrl(`vipBonus/level_${store.state.user.vip_lv}.png`));
let checkInBtnStatus = ref(0);
const getData = async () => {
	if (store.state.user.token != '') {
		let signIndata = await UserService.get_sign_list();
		signIndata.data['time'] = calculateSecondsUntilMidnight();
		let data = await VipService.get_user_vip_bonus_state({});
		const obj = {
			now_bonus: data.data.data.now_bonus,
			week_bonus: data.data.data.week_bonus,
			month_bonus: data.data.data.month_bonus,
			day_bonus: data.data.data.day_bonus,
			split_bonus: data.data.data.split_bonus,
			lv_up_bonus: data.data.data.lv_up_bonus,
			badgeShow: data.data.bonus_num > 0 ? true : false,
			bonus_num: data.data.bonus_num,
			sgin_data: signIndata.data,
		}

		store.dispatch("vipBonusState/setData", obj);

	}
}
getData();

// // 获取签到列表
// const getSignInList = async () => {
// 	let data = await UserService.get_sign_list();
// 	state.signIndata = data.data;
// };


const now_bonus_intervalId = setInterval(() => {
	now_updateCountdown(store.state.vipBonusState.now_bonus.time);
	if (store.state.vipBonusState.now_bonus.time > 0) {
		store.state.vipBonusState.now_bonus.time -= 1
	}
}, 1000);

function now_updateCountdown(targetTimeInSeconds) {
	if (targetTimeInSeconds <= 0) {
		store.state.vipBonusState.now_time = '00:00';
		// clearInterval(intervalId);  // 停止定时器
		return;
	}
	const hours = Math.floor(targetTimeInSeconds / 3600);
	const minutes = Math.floor((targetTimeInSeconds % 3600) / 60);
	const seconds = targetTimeInSeconds % 60;

	store.state.vipBonusState.now_time = `${hours < 10 ? `0${hours}` : hours}:${minutes < 10 ? `0${minutes}` : minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;
}

const day_bonus_intervalId = setInterval(() => {
	day_now_updateCountdown(parseInt(store.state.vipBonusState.day_bonus.time as any));
	if (store.state.vipBonusState.day_bonus.time > 0) {
		store.state.vipBonusState.day_bonus.time -= 1
	}
}, 1000);

function day_now_updateCountdown(targetTimeInSeconds) {
	if (targetTimeInSeconds <= 0) {
		store.state.vipBonusState.day_time = '00:00';
		// clearInterval(intervalId);  // 停止定时器
		return;
	}
	const hours = Math.floor(targetTimeInSeconds / 3600);
	const minutes = Math.floor((targetTimeInSeconds % 3600) / 60);
	const seconds = targetTimeInSeconds % 60;
	store.state.vipBonusState.day_time = `${hours < 10 ? `0${hours}` : hours}:${minutes < 10 ? `0${minutes}` : minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;
}

onBeforeUnmount(() => {
	console.log('onBeforeUnmount');

	clearInterval(day_bonus_intervalId);
	clearInterval(split_bonus_intervalId)
	clearInterval(now_bonus_intervalId)
})


const split_bonus_intervalId = setInterval(() => {
	split_updateCountdown(parseInt(store.state.vipBonusState.split_bonus.time as any));
	if (store.state.vipBonusState.split_bonus.time > 0) {
		store.state.vipBonusState.split_bonus.time -= 1
	}
}, 1000);

function split_updateCountdown(targetTimeInSeconds) {
	if (targetTimeInSeconds <= 0) {
		store.state.vipBonusState.split_time = state.split_time = '00:00';
		// clearInterval(intervalId);  // 停止定时器
		return;
	}
	const hours = Math.floor(targetTimeInSeconds / 3600);
	const minutes = Math.floor((targetTimeInSeconds % 3600) / 60);
	const seconds = targetTimeInSeconds % 60;

	store.state.vipBonusState.split_time = state.split_time = `${hours < 10 ? `0${hours}` : hours}:${minutes < 10 ? `0${minutes}` : minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;
}

const shhowPop = () => {
	if (isShowPop.value == false) {
		getData();
	}
	isShowPop.value = !isShowPop.value;
}

// 领取立即反水
const get_bonus = (index) => {
	if (!store.state.user.token) {
		store.dispatch('status/setLoginShow', true)
	}
	switch (index) {
		case 1:

			if (store.state.vipBonusState.now_bonus.time <= 0 && store.state.vipBonusState.now_bonus.state == 1) {
				VipService.user_get_now_vip_bonus().then((res) => {
					if (res.data.code == 1) {
						getData()
						vipEmit()
						isBonusPop.value = true
						state.now_bonus_pop = res.data.bonus
						state.split_bonus_pop = res.data.split_bonus
						state.comIdx = index
						if (!store.state.status.playIngState) {
							getUserInfoNoLoad()

						}
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
						vipEmit()
						isBonusPop.value = true
						state.now_bonus_pop = res.data.bonus
						state.split_bonus_pop = res.data.split_bonus
						state.comIdx = index
						state.btn_loading_2 = false
						if (!store.state.status.playIngState) {
							getUserInfoNoLoad()

						}
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
						vipEmit()
						isBonusPop.value = true
						state.now_bonus_pop = res.data.bonus
						state.split_bonus_pop = res.data.split_bonus
						state.comIdx = index
						state.btn_loading_3 = false
						if (!store.state.status.playIngState) {
							getUserInfoNoLoad()

						}
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
						vipEmit()
						isBonusPop.value = true
						state.now_bonus_pop = res.data.bonus
						state.split_bonus_pop = res.data.split_bonus
						state.comIdx = index
						state.btn_loading_4 = false
						if (!store.state.status.playIngState) {
							getUserInfoNoLoad()

						}
					}
				})
			}
			break;
		case 5:
			if (store.state.vipBonusState.sgin_data['state'] == 1) {
				if (store.state.vipBonusState.sgin_data['money'] == 0) {
					ElNotification({
						message: t('Pleaseincreaseyourviplevel'),
						type: 'warning',
						duration: 3000,
						offset: 65,
					})
					return;
				}
				state.btn_loading_checkIn = true
				const fun = () => {
					UserService.receive_sign_bonus().then((res) => {
						console.log('receive_sign_bonus', res);

						if (res.data.code == 1) {
							state.btn_loading_checkIn = false;
							promptPopup('rewardPopup', { title: t('signIn.Checkindiário'), amount: res.data.money, tips: t('signIn.Obônuscontinuaaaumentarà'), btnName: t('btnName.Confirmar') })
							store.dispatch("vipBonusState/init_sgin_data");
						}
					});
				}
				debounce(fun)
			}
			break;
		default:
			break;
	}


}

const vipEmit = () => {
	if (router.currentRoute.value.fullPath == '/vipBonus/pendingRewards') {
		proxy.$mitt.emit('getVipFinish')
	}
}



function calculateSecondsUntilMidnight() {
	const now = new Date();
	const midnight = new Date(
		now.getFullYear(),
		now.getMonth(),
		now.getDate() + 1, // 将日期设置为明天
		0, 0, 0, 0
	);

	return Math.floor((midnight.getTime() - now.getTime()) / 1000);
}
const finish = () => {
	store.dispatch("vipBonusState/init_sgin_data");
}

const showVipPop = ()=>{
    store.dispatch('status/setvipCheckIn',true);
}
</script>

<style scoped lang="scss">
:deep(.el_popover_style) {
	// min-width: 220px !important;
	// width: 100% !important;
	// padding: 0px 0;
	border: none !important;
	border-radius: 8px !important;
	font-size: 16px !important;
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

.Recompensas {
	padding: 0 7px;
	box-sizing: border-box;
	background: rgba(45, 49, 68, 0.6);
	width: 195px;
	height: 45px;
	border-radius: 6px;
	display: flex;
	align-items: center;
	box-sizing: border-box;
	cursor: pointer;
	margin-left: 16px;

	:deep(.el-badge) {
		.el-badge__content {
			transform: translate(8px, -4px);
			font-size: 12px;
			font-weight: bold;
			color: #000000;
			border: 2px solid #2D3144;
			box-shadow: 0px 1px 0px 0px rgba(117, 237, 61, 0.35);
			background: #75ED3D;

		}
	}

	img {
		width: 32px;
		height: 34px;
		margin: 0 4px 0 4px;
		vertical-align: middle;
	}

	p {
		font-size: 14px;
		// line-height: 24px;
		color: #fff;
	}

	.arr {
		width: 10.5px;
		height: 7.3px;
		margin-left: 12px;
	}

	.arr_top {
		display: inline-block;
		transition: rotate 1s linear;
	}


}

.bonus_pop {}

.toVip {
	width: 100%;
	// height: 48px;
	padding: 10px 0;
	display: flex;
	justify-content: center;
	align-items: center;
	background: rgba(40, 48, 64, 0.6);
	border-bottom-left-radius: 12px;
	border-bottom-right-radius: 12px;

	p {
		color: #4181EE;
		font-size: 16px;
		font-weight: bold;
		display: flex;
		align-items: center;
	}

	img {
		width: 19px;
		height: 21px;
	}
}

.pop {
	width: 445px;
	display: flex;
	flex-direction: column;
	position: absolute;
	top: 80px;
	left: 200px;
	background: #202431;
	border-radius: 12px;
	transition: 0.2s all ease;

	// height: 100%;
	.item {
		width: 100%;
		// display: flex;
		// align-items: center;
		// justify-content: space-between;
		padding: 13px 20px;
		box-sizing: border-box;
		display: grid;
		grid-template-columns: 2fr auto;
		align-items: center;


		.left {
			display: flex;
			align-items: center;

			img {
				width: 58.35px;
			}

			.txt {
				color: #fff;
				display: flex;
				flex-direction: column;
				margin-left: 12px;

				p {
					font-size: 16px;
					font-weight: bold;
					display: flex;
					align-items: center;

				}

				p:nth-child(2) {
					margin-top: 8px;
					font-size: 14px;
					color: #686D7B;
				}

				span {
					margin-top: 11px;
					font-size: 15px;
				}
			}

			.imgTxt {
				display: flex;
				flex-direction: row;
				align-items: center;
				gap: 18px;

				img {
					width: 50px;
					height: 50px;
				}
			}
		}


		.check {
			color: #75ED3D;
		}

		:deep(.el-button) {
			border: none;
			box-shadow: none;
		}

		:deep(.el-button>span) {
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;
			row-gap: 8px;
		}

		.no_bonus_box {
			// background-color: #222431;
			background: rgba($color: #000000, $alpha: 0);
			// padding: 10px 14px !important;
			display: flex;
			gap: 5px;
			box-sizing: border-box;
			// width: 130px;
			height: 52px;

			.btn_mask {
				display: none !important;
			}

			p {

				color: #B2B6C5 !important;
			}
		}

		.btn2 {
			cursor: pointer;
			display: flex;
			align-items: center;
			justify-content: center;
			flex-direction: row;
			padding: 14px 9px;
			border-radius: 10px;
			position: relative;
			min-width: 114px;
			height: 48px;
			box-sizing: border-box;

			p {
				color: #1B1D29;
				font-size: 14px;
				font-weight: bold;
			}

			img {
				width: 16px;
				margin-right: 5px;
			}
		}

		.btn2_item_1 {
			flex-direction: column;

			.btn2_item_1_p {
				margin-top: 5px;
			}
		}


		.btnMask {
			position: relative;
		}

		.btnMask::after {
			content: "";
			cursor: pointer;
			background: rgba(5, 5, 5, 0.432);
			position: absolute;
			// top: -1px;
			// left: -0.5px;
			width: calc(100%);
			height: calc(100%);
			z-index: 2;
			border: 1px solid;
			// border-radius: 6px;
			// border-radius: 2px;
		}
	}
}

.btn_mask {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(5, 5, 5, 0.432);
	border-radius: 8px;
}

.mask {
	display: none;
	z-index: -1 !important;
}

.popShow {
	display: flex;
}

.Countdown {
	box-sizing: border-box;
	background-size: 100% 100%;
	font-size: 21px;
	display: flex;
	align-items: center;

	.colon {
		margin-left: 2px;
		margin-right: 2px;
	}
}

@media (max-width:768px) {
	.mask {
		position: absolute;
		top: 0;
		height: 100vh;
	}

	.Recompensas {
		width: 135px;
		height: 30px;
		margin-left: 0;

		:deep(.el-badge) {
			.el-badge__content {
				width: 14px;
				height: 14px;
				padding: 0;
				line-height: 14px;
				transform: translate(17px, -9px);
				font-size: 12px;
				font-weight: bold;
				color: #000000;
				border: 2px solid #2D3144;
			}
		}

		p {
			font-size: 12px;
			transform: scale(0.9);
		}

		img {
			// padding: ;
			width: 17px;
			height: 17px;
			margin: 0 !important;
		}

		.arr {
			width: 8px;
			height: 5px;
			margin-left: 0px !important;
		}
	}

	.pop {
		width: 100%;
		left: 0;
		border-radius: 0 0 12px 12px;
		top: 44px;

		.item {

			.left {
				img {
					width: 52px;
				}

				.txt {
					p {
						font-size: 14px;

					}

					p:nth-child(2) {
						margin-top: 11px;
						font-size: 12px;
					}

					span {
						font-size: 13px;
						margin-top: 9px;
					}
				}

				.imgTxt {
					gap: 18px;

					img {
						width: 32px;
						height: 32px;
					}
				}
			}

			.no_bonus_box {
				width: 105px;
				height: 44px;
			}

			.btn2 {
				padding: 13px 6px;
				height: 40px;

				p {
					font-size: 12px;
				}

				img {
					width: 13px;
					// margin-right: 2px;
				}
			}

			.sl_box_shadow_green {
				padding: 0 15px;
			}
		}

	}

	.toVip {
		// height: 42px;

		p {
			font-size: 14px
		}

		span {
			font-size: 16px
		}
	}
}
</style>