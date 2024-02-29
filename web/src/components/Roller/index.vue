<template>
	<div class="Roller">
		<el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false">
			<div class="bg">
				<img src="@/assets/images/Roller/Off.png" alt="" class="close" @click="showRoller(false)">
				<img src="@/assets/images/Roller/query.png" alt="" class="help"
					@click="() => { helpPop = true; dialogVisible = false }">

				<div class="head">
					<div>
						<img src="@/assets/images/Roller/Star.png" alt="">
						<img src="@/assets/images/Roller/Star.png" alt="">
						<img src="@/assets/images/Roller/Star.png" alt="">
					</div>

					<p text="Slot Grátis">{{ t('Roller.SlotGrátis') }}</p>
					<div>
						<img src="@/assets/images/Roller/Star.png" alt="">
						<img src="@/assets/images/Roller/Star.png" alt="">
						<img src="@/assets/images/Roller/Star.png" alt="">
					</div>
				</div>
				<div class="slot">
					<div v-for="(v, i) in state.slotArr">
						<!-- <p v-for="(val, idx) in v.arr">{{ val }}</p> -->
						<!-- <img src="@/assets/images/Roller/roll-num.png" alt="" :style="`transform:translateY(${v.translateY})`"> -->
						<p v-if="i == flagIdx && flag">,</p>
						<div v-else class=" imgDiv"
							:style="` animation-timing-function: ease-out; background-position-y:${v.backgroundY}px`">

						</div>
					</div>

				</div>
				<div :class="{ btn: true, btnBg2: rollerNum < 1, btnBg: rollerNum >= 1, scaleUpCenter: btnClick }"
					@click="play">
					<!-- {{ btnState == '0' ? 'Gire de grátis x1' : btnState == '1' ?
						'Girando...' : btnState == '4' ? ' Loading...' : 'VOCÊ Venceu !' }} -->
					{{ t('Roller.GiredegrátisX') }}{{ rollerNum }}
				</div>
				<!-- <div v-else-if="btnState == '3'" class="btn2">
					<p>Próximo Bônus de Slot Grátis em</p>
					<span> <el-countdown title="" format="HH:mm:ss" :value="Date.now() + rollerTime * 1000"
							@finish="finish" /></span> 
				</div>-->
				<!-- <div v-else-if="btnState == '4'" class="btn2">
                    loading...
                </div> -->
				<img src="@/assets/images/Roller/Shiftlever.png" alt="" class="Shiftlever">
				<div class="bottom">
					<div class="font">
						{{ userBetAmount }}/{{ needAmount }}
					</div>
					<div class="bottom_bg" :style="`width: ${betCodeRate}%`"></div>
				</div>
			</div>
		</el-dialog>
		<el-dialog v-model="helpPop" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false">
			<div class="helpPop">
				<div class="helpPop_head">
					{{ t('signIn.Regras') }}
					<img src="@/assets/images/public/Shutdown.png" alt="" class="helpPop_head_close"
						@click="() => { helpPop = false; dialogVisible = true }">
				</div>
				<div class="body">
					<div class="title">{{ t('Roller.Condições') }}</div>
					<p class="txt">{{ t('Roller.CondiçõesTxt1') }}</p>
					<span class="txt">{{ t('Roller.CondiçõesTxt2') }} <div class="yellow">10.000,00
						</div> {{ t('Roller.reais') }}</span>

					<div class="title">{{ t('Roller.Aregradoscaçaníqueisdasorte') }}</div>
					<p class="txt">{{ t('Roller.AregradoscaçaníqueisdasorteTxt1') }}</p>
					<span class="txt">{{ t('Roller.AregradoscaçaníqueisdasorteTxt2', { needAmount: needAmount }) }}<div
							class="yellow">
							{{ t('Roller.AregradoscaçaníqueisdasorteTxt3') }}</div></span>

					<div class="title">{{ t('Roller.Termoscondições') }}</div>
					<p class="txt">{{ t('Roller.TermoscondiçõesTxt1') }}</p>
					<p class="txt">{{ t('Roller.TermoscondiçõesTxt2') }}</p>
					<span class="txt">{{ t('Roller.TermoscondiçõesTxt3') }}</span>
				</div>
			</div>
		</el-dialog>
	</div>
</template>

<script setup lang="ts">
import { ref, getCurrentInstance, reactive } from "vue";
import { RollerService } from "@/api/Roller";
import promptPopup from "@/components/promptPopup/index";
import { useStore } from "@/store/index";
import { ElNotification } from "element-plus";
import { useI18n } from "vue-i18n";
const store = useStore();
const { t } = useI18n();
let dialogVisible = ref(true);
const { proxy } = getCurrentInstance() as any;

let flag = ref(false);
let flagIdx = ref(null);
// let rollerTime = ref(0);
let helpPop = ref(false)

const state = reactive({
	slotArr: [
		{
			arr: [
				'?',
				'0',
				'1',
				'2',
				'3',
				'4',
				'5',
				'6',
				'7',
				'8',
				'9',
				'0',
			],

			backgroundY: -20,
			dh: true,
			timeID: null,
			time: 10,
		},
		{
			arr: [
				'?',
				'0',
				'1',
				'2',
				'3',
				'4',
				'5',
				'6',
				'7',
				'8',
				'9',
				'0',
			],

			backgroundY: -20,
			dh: true,
			timeID: null,
			time: 10,
		},
		{
			arr: [
				'?',
				'0',
				'1',
				'2',
				'3',
				'4',
				'5',
				'6',
				'7',
				'8',
				'9',
				'0',
			],

			backgroundY: -20,
			dh: true,
			timeID: null,
			time: 10,
		},
		{
			arr: [
				'?',
				'0',
				'1',
				'2',
				'3',
				'4',
				'5',
				'6',
				'7',
				'8',
				'9',
				'0',
				',',
			],

			dh: true,
			backgroundY: -20,
			timeID: null,
			time: 10,

		},
		{
			arr: [
				'?',
				'0',
				'1',
				'2',
				'3',
				'4',
				'5',
				'6',
				'7',
				'8',
				'9',
				'0',
			],

			dh: false,
			backgroundY: -20,
			timeID: null,
			time: 10,
		},
	],


})

let arrLengthPx = [
	'-20',
	'-114',
	'-208',
	'-302',
	'-397',
	'-489.4',
	'-584.4',
	'-678',
	'-773',
	'-867',
]

let btnState = ref('4');

let btnClick = ref(false);

const showRoller = (val) => {
	// dialogVisible.value = val
	store.dispatch("status/setRollerShow", false)
}
// 转轮可旋转次数
let rollerNum = ref(0)
// 转轮所需打码量
let needAmount = ref(0)
// 用户拥打码量 
let userBetAmount = ref(0)
// 转轮百分比
let betCodeRate = ref(0.0)

function getRollerState() {
	RollerService.roller_money_state().then((res) => {
		rollerNum.value = res.data.num
		needAmount.value = res.data.need_amount
		userBetAmount.value = res.data.bet_amount
		betCodeRate.value = res.data.bet_amount * (res.data.need_amount / 100)

	});
}
getRollerState()

let rollerState = 1
const play = () => {
	if (!store.state.user.token) return store.state.status.loginShow = true
	if (rollerNum.value < 1) {
		ElNotification({
			message: t('Roller.rollermsg'),
			type: 'warning',
			duration: 3000,
			offset: 65,
		})
		return
	}
	if (rollerState != 1) return
	rollerState = 0

	let money = 0;
	flagIdx.value = null;
	for (let i = 0; i < state.slotArr.length; i++) {

		state.slotArr[i].backgroundY = -20;
	}

	for (let i = 0; i < state.slotArr.length; i++) {
		(state.slotArr[i].timeID as any) = setInterval(() => {
			state.slotArr[i].backgroundY -= state.slotArr[i].time;
		}, 10)

	}

	RollerService.receive_roller_money().then((res: any) => {

		if (res.data.code == 1) {

			money = res.data.money;
			let length = money.toString().split('');
			setTimeout(() => {
				let idx = state.slotArr.length - money.toString().split('').length;
				// btnState.value = '2';
				let lengthIdx = 0;
				for (let i = 0; i < state.slotArr.length; i++) {
					state.slotArr[i].time = 4;

					setTimeout(() => {
						if (i >= idx) {
							if (length[lengthIdx] !== ',' && length[lengthIdx] !== '.') {
								// if (length[lengthIdx] !== '.') {
								state.slotArr[i].backgroundY = Number(arrLengthPx[length[lengthIdx]]);
							} else {
								flagIdx.value = i as any;
							}

							lengthIdx += 1;
						} else {
							state.slotArr[i].backgroundY = Number(arrLengthPx[0]);
						}
						clearInterval(state.slotArr[i].timeID as any);
						flag.value = true;

						if (i == state.slotArr.length - 1) {
							rollerState = 1
							promptPopup('rewardPopup', { title: t('promptPopup.title_VOCÊVENCEU'), amount: res.data.money, tips: t('promptPopup.tips_Obônusjá'), btnName: t('btnName.Confirmar') })
							// btnState.value = '3';
						}

					}, ((i + 1) * 450));


				}

				store.state.startData.bonusCabinet.roller_bonus_state = 0


			}, 2000);


		}
		getRollerState()


	}).finally(() => {


	})



}

const finish = () => {
	// btnState.value = '0'
}

proxy.$mitt.on("showRoller", (val: any) => {
	dialogVisible.value = val
});




</script>

<style lang="scss" scoped>
.Roller {
	position: relative;

	.bg {
		background: url(@/assets/images/Roller/airframe.png);

		background-size: 100% 100%;
		width: 374.96px;
		height: 371.55px;
		position: relative;
	}

	.close {
		position: absolute;
		top: -2%;
		right: -20px;
		width: 28px;
		cursor: pointer;
	}

	.help {
		position: absolute;
		top: calc(-2% + 35px);
		right: -20px;
		width: 28px;
		cursor: pointer;

		@media (max-width: 758px) {
			top: calc(-2% + 46px);
		}
	}

	.Shiftlever {
		position: absolute;
		right: -5px;
		top: 28%;
		width: 33.13px;
		cursor: pointer;
	}

	.head {
		position: absolute;
		top: 40px;
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		box-sizing: border-box;
		gap: 8px;

		div {
			display: flex;
			gap: 5px;
		}

		img {
			width: 12.74px;
		}

		p {
			font-size: 24px;
			font-weight: 800;
			background: linear-gradient(180deg, #F5E79A 0%, #F5E79A 49%, #F6C543 49%, #F6C543 100%);

			-webkit-background-clip: text;
			-webkit-text-fill-color: transparent;
		}

		p:before {
			content: attr(text);
			position: absolute;
			z-index: -1;
			text-shadow: 0px 1px 1px #832798;
		}
	}

	.slot {
		position: absolute;
		top: 34%;
		left: 50%;
		transform: translate(-50%, 0);
		width: 72%;
		font-size: 40px;
		color: #FFF;
		display: grid;
		grid-template-columns: repeat(5, 20%);
		height: 50px;
		overflow: hidden;
		justify-items: center;
		transition: all 1s linear;

		.imgDiv {
			background: url(@/assets/images/Roller/roll-num.png) center top repeat-y;
			width: 56px;
			height: 1034px;
			// background-position-y: -25px;
		}

		img {
			width: 100%
		}
	}

	.btn {
		width: 264px;
		height: 45px;

		border-radius: 11px 11px 11px 11px;
		position: absolute;
		left: 50%;
		top: 66%;
		transform: translate(-50%, 0);
		font-size: 18px;
		color: #fff;
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;


	}

	.btn2 {
		width: 300px;
		height: 45px;

		border-radius: 11px 11px 11px 11px;
		position: absolute;
		left: 50%;
		top: 66%;
		transform: translate(-50%, 0);
		font-size: 18px;
		color: #fff;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		cursor: pointer;

		p {
			color: rgba(255, 255, 255, 0.69);
			font-size: 16px;
			margin-bottom: 10px;
		}

		span {
			font-size: 18px;
			color: #FFFFFF;

			:deep(.el-statistic__content) {
				font-size: 18px;
				color: #FFFFFF;
			}
		}
	}

	.btnBg {
		background: #64B135;
		box-shadow: 0px 7px 0px 0px #4F882C;
	}

	.btnBg2 {
		background: #585B68;
		box-shadow: 0px 5px 0px 0px #373A41;
	}

	.bottom {
		width: 80%;
		height: 16px;
		border-radius: 8px;
		background: #21222B;
		position: absolute;
		left: 10%;
		bottom: 20px;
		transition: all 0.5s linear;

		@media (max-width:758px) {
			bottom: 10px;
		}

		.font {
			display: flex;
			align-items: center;
			color: #fff;
			font-size: 12px;
			position: absolute;
			height: 100%;
			left: 50%;
			transform: translate(-50%);
			z-index: 2;
		}

		.bottom_bg {
			// width: 50%;
			height: 100%;
			background: linear-gradient(90deg, #FDE672 0%, #FFC01E 100%);
			position: absolute;
			z-index: 1;
			border-radius: 8px;
		}
	}

}

.helpPop {
	width: 400px;
	height: 450px;
	background: #202431;
	border-radius: 8px;
	box-sizing: border-box;
	padding: 14px 27px 25px 27px;

	@media (max-width:758px) {
		width: 351px;
		height: 440px;
	}

	.helpPop_head {
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 16px;
		color: #fff;
		position: relative;

		.helpPop_head_close {
			position: absolute;
			right: 0;
			width: 20px;
		}
	}

	.body {
		width: 100%;
		height: 354px;
		font-size: 14px;
		overflow-x: auto;
		margin-top: 20px;

		.title {
			font-size: 14px;
			color: #fff;
			margin-top: 20px;
			margin-bottom: 16px;

			&:first-child {
				margin-top: 0;
			}
		}

		.txt {
			color: #B2B6C5;
			line-height: 21px;

			div {
				display: inline-block;
			}

			@media (max-width: 758px) {
				font-size: 12px;
				line-height: 18px;
			}
		}

		p {
			margin-bottom: 12px;
		}

		.yellow {
			color: #F8BF2E;
		}
	}

	.body::-webkit-scrollbar {
		display: block;
		width: 4px;
		background: rgb(0 0 0 / 0%);

	}

	.body::-webkit-scrollbar-thumb {
		background: #707070;
		width: 4px;
		height: 111px;
		// display: block;
	}
}

@media (max-width: 768px) {
	:deep(.el-dialog) {
		width: 100%;
		--el-dialog-margin-top: 25vh;

	}

	.Roller {
		.bg {

			width: 279px;
			height: 276.46px;

		}


		.head {
			position: absolute;
			top: 29px;
			width: 100%;
			// padding: 0 49px;
			gap: 8px;

			div {
				display: flex;
				gap: 3px;
			}

			img {
				width: 9.62px;
			}

			p {
				font-size: 18px;
				font-weight: 800;

			}


		}

		.slot {
			.imgDiv {
				width: 39px;
				object-fit: cover;
			}
		}

		.Shiftlever {
			width: 25px;
			height: 42.55px;
		}

		.btn {
			width: 199px;
			height: 34px;
			// box-shadow: 0px 4px 0px 0px;
			border-radius: 8px 8px 8px 8px;
			font-size: 14px;
		}

		.btn2 {
			width: 199px;
			height: 34px;

			p {
				font-size: 12px;
			}

			span {
				font-size: 16px;

				:deep(.el-statistic__content) {
					font-size: 16px;
				}
			}
		}

	}

}

.spin {
	animation: wheel-spin 1s infinite linear;
	/* 应用动画效果 */
}


@keyframes wheel-spin {
	0% {
		transform: translateY(0%);
	}

	100% {
		transform: translateY(-100%);
	}
}

.scaleUpCenter {
	-webkit-animation: scale-up-center 0.4s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
	animation: scale-up-center 0.4s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
}

@-webkit-keyframes scale-up-center {
	0% {
		-webkit-transform: scale(0.5);
		transform: scale(0.5);
	}

	100% {
		-webkit-transform: scale(1);
		transform: scale(1);
	}
}

@keyframes scale-up-center {
	0% {
		-webkit-transform: scale(0.5);
		transform: scale(0.5);
	}

	100% {
		-webkit-transform: scale(1);
		transform: scale(1);
	}
}
</style>