<template>
	<div class="spin" id="spin">

		<div class="spinBox">
			<div class="bg top"></div>
			<div class="bg bottom"></div>
			<div class="spinBox2">
				<img src="@/assets/images/spin/Ontheleft.png" alt="" class="Ontheleft">
				<img src="@/assets/images/spin/right.png" alt="" class="OntheRit">
				<img src="@/assets/images/spin/Diamond.png" alt="" class="diamond_a_img">
				<img src="@/assets/images/spin/Diamond.png" alt="" class="diamond_b_img">
				<img src="@/assets/images/spin/Star.png" alt="" class="star_a_img">
				<img src="@/assets/images/spin/Star.png" alt="" class="star_b_img">
				<img src="@/assets/images/spin/Star.png" alt="" class="star_c_img">
				<img src="@/assets/images/spin/Star.png" alt="" class="star_d_img">
				<img src="@/assets/images/spin/GoldCoin.png" alt="" class="coin_a_img">
				<img src="@/assets/images/spin/GoldCoin.png" alt="" class="coin_b_img">
				<!-- <img src="@/assets/images/spin/GoldCoin.png" alt="" class="coin_c_img"> -->
				<img src="@/assets/images/spin/chip.png" alt="" class="chips_a_img">
				<img src="@/assets/images/spin/chip.png" alt="" class="chips_b_img">
				<div class="head">
					<img class="logo" :src="store.state.conf.all_conf.platform['platform_title_icon_url']" alt="" >
					<div class="spin_box">
						<div :class="{ turntable: true, spin_rotate: is_spin_rotate }">
							<img src="@/assets/images/spin/Turntableoutsieframe.png" alt="" class="Turntableoutsieframe">
							<div class="turntable_item" v-for="v in bouns">
								<span>{{ v.money }}</span>
								<img :src="v.img" alt=""
									:class="{ iphone: v.money == 'IPHONE 14', switch: v.money == 'SWITCH' }">
							</div>

						</div>
						<div class="point_img">
							<div class="light_wrap">
								<div :class="{ point_light: true, pointBg: is_spin_rotate }"></div>
							</div>
							<img src="@/assets/images/spin/Turntableoutsidethebox.png" alt=""
								:class="{ spin_point: true, scale_up_hor_left: is_spin_rotate }">
						</div>
						<img src="@/assets/images/spin/RotaryCenter.png" alt="" class="spin_center"
							@click="is_spin_rotate = true">
						<img src="@/assets/images/spin/word.png" alt="" class="spin_btn">

						<img src="@/assets/images/spin/purse.png" alt="" class="amount_img">
						<img src="@/assets/images/spin/coco.png" alt="" class="coco_img">
						<div class="Button" @click="run">
							GIRE AGORA
						</div>
					</div>

				</div>
				<div class="payment">
					<div class="nosso">NOSSO PAGAMENTO</div>
					<img src="@/assets/images/deposit/pix.png" alt="" class="pix_img">
					<div class="info">
						<div class="info_item">
							<img src="@/assets/images/spin/ooo.png" alt="" class="">
							<p>REGISTRAR</p>
							<a :href="store.state.conf.all_conf.platform['platform_path']">{{ store.state.conf.all_conf.platform['platform_path'] }}</a>
						</div>
						<div class="info_item">
							<img src="@/assets/images/spin/DEPÓSITO.png" alt="" class="">
							<p>DEPÓSITO</p>
							<span>Com o PIX Pay</span>
						</div>
						<div class="info_item">
							<img src="@/assets/images/spin/RECOMPENSA.png" alt="" class="">
							<p>RECOMPENSA</p>
							<span>Ganhe Bônus e Divirta-se!</span>
						</div>
					</div>
				</div>
				<div class="bottom_font">
					<p>{{ `Participe de Nossa Comunidade \n no Telegram` }}</p>
					<a :href="store.state.conf.all_conf.tg_channel_url"><span>➡️ {{ store.state.conf.all_conf.tg_channel_url
					}}</span></a>
				</div>
			</div>

		</div>
		<el-dialog v-model="dialogFormVisible" align-center>
			<spinPop @close="cloes"></spinPop>
		</el-dialog>
		<footerCom></footerCom>

		<audio id="audio" autoplay></audio>
		<div class="toTop" @click="toTop">
			<img src="@/assets/images/spin/arrow.png" alt="" class="">
			<p>Topo</p>
		</div>
	</div>
</template>

<script setup lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, ref } from "vue";
import { getImageUrl, getUserInfo, moneyFormat } from "@/utils/baseFun";
import footerCom from "../layout/components/footer.vue";
import spinPop from "./components/spinPop.vue";
import { useStore } from "@/store/index";
import { useRouter } from "vue-router";


const router = useRouter();
const store = useStore();

const { proxy } = getCurrentInstance() as any;
let is_spin_rotate = ref(false);
let dialogFormVisible = ref(false);
let bouns = ref([
	{
		img: getImageUrl('spin/iPhone14.png'),
		money: 'IPHONE 14',
	},
	{
		img: getImageUrl('spin/silver.png'),
		money: 'R$ 0,20',
	},
	{
		img: getImageUrl('spin/gold.png'),
		money: 'R$ 100,00',
	},
	{
		img: getImageUrl('spin/silver.png'),
		money: 'R$ 0,30',
	},
	{
		img: getImageUrl('spin/gold.png'),
		money: 'R$ 1000,00',
	},
	{
		img: getImageUrl('spin/silver.png'),
		money: 'R$ 0,50',
	},
	{
		img: getImageUrl('spin/switch.png'),
		money: 'SWITCH',
	},
	{
		img: getImageUrl('spin/silver.png'),
		money: 'R$ 1,00',
	},
	{
		img: getImageUrl('spin/gold.png'),
		money: 'R$ 5000,00',
	},
	{
		img: getImageUrl('spin/silver.png'),
		money: 'R$ 5,00',
	},
	{
		img: getImageUrl('spin/gold.png'),
		money: 'R$ 50,00',
	},
	{
		img: getImageUrl('spin/silver.png'),
		money: 'R$ 10,00',
	},
])

const run = () => {
	let audio = document.getElementById('audio');

	if (is_spin_rotate.value) {
		dialogFormVisible.value = true;
	} else {
		//@ts-ignore
		audio.src = getImageUrl('spin/spin.mp3') as any;
		//@ts-ignore
		audio.currentTime = 3;
		//@ts-ignore
		audio.play();
		setTimeout(() => {

			dialogFormVisible.value = true;

			setTimeout(() => {
				//@ts-ignore
				audio.pause();
			}, 1500);

		}, 5000);
	}

	is_spin_rotate.value = true;
}

const cloes = () => {
	let c = localStorage.getItem('c')
	let flag = true
	if (c) {
		store.state.conf.all_conf['c_list'].forEach(item => {
			if (item.c == localStorage.getItem('c') && item.is_apk == 1) {
				let apkUrl = store.state.conf.all_conf.android_url + "c" + c + ".apk"
				window.open(apkUrl)
				flag = false
			}
		});
	}
	if (flag) {
		// dialogFormVisible.value = false;
		if (store.state.user.token) {
			router.push('/')
		} else {
			store.dispatch('status/setLoginShow', true)
			proxy.$mitt.emit("showLoginBox", 1);
		}
	}
}

const toTop = () => {
	// const contentBox = document.getElementById('spin');
	// //@ts-ignore
	// console.log(contentBox.scrollTop);

	// if (contentBox) {
	//     if (window.innerWidth <= 768) {
	window.scrollTo({
		top: 0,
		behavior: 'smooth'
	});
	// } else {
	//     contentBox.scrollTop = 0;
	// }
	// }
}
</script>

<style scoped lang="scss">
a {
	cursor: pointer;
}

:deep(.footer) {
	background: #1A1C20;

	.bottom_box {
		background: #1A1C20;
	}
}

.toTop {
	width: 3.375rem;
	height: 3.375rem;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	background: rgba(239, 239, 239, 0.1);
	border-radius: 6px;
	position: fixed;
	top: 772px;
	right: 19px;
	cursor: pointer;
	gap: 6px;

	span {
		color: #65BE3D;
	}

	p {
		color: #fff;
		font-size: 15.55px;
		font-weight: 400;
	}

	img {
		width: 1.2em;
		// height: 1.4em;
	}
}

.spin {
	background-color: #24262b;
	width: 100%;
	height: 100%;
	// padding-bottom: 59px;
	// overflow: hidden;


	.spinBox {
		position: relative;
		width: 100%;
		height: 100%;
		margin-bottom: 59px;

		// overflow: hidden;
		.bg {
			width: 59.625rem;
			height: 59.625rem;
			opacity: .24;
			-webkit-filter: blur(26px);
			filter: blur(26px);
			background-image: radial-gradient(circle at 50% 50%, #FF470D, rgba(0, 0, 0, 0) 76%);
			position: absolute;

		}

		.bottom {
			position: absolute;
			left: 50%;
			bottom: -10%;
			-webkit-transform: translateX(-50%);
			-ms-transform: translateX(-50%);
			transform: translate(-50%)
		}

		.top {
			position: absolute;
			left: 50%;
			top: 0;
			-webkit-transform: translateX(-50%);
			-ms-transform: translateX(-50%);
			transform: translate(-50%)
		}
	}



	.spinBox2 {
		position: relative;
		z-index: 2;

		.Ontheleft {
			max-width: 551px;
			width: 30%;
			position: absolute;
			left: 0;
			top: 0;
		}

		.OntheRit {
			max-width: 551px;
			width: 30%;
			position: absolute;
			right: 0;
			top: 0;
		}

		.diamond_a_img {
			width: 6.25rem;
			top: 11.9375rem;
			left: 5%;
			margin-left: 9.375rem;
			position: absolute;
			-webkit-transform: rotate(-50deg);
			-ms-transform: rotate(-50deg);
			transform: rotate(-50deg);
			z-index: 1;
		}

		.diamond_b_img {
			width: 6.25rem;
			top: 14.0625rem;
			right: 0%;
			margin-right: 16.25rem;
			position: absolute;
			z-index: 1;
		}

		.star_a_img {
			position: absolute;
			left: 5%;
			margin-left: 3.125rem;
			width: 3.625rem;
			top: 39.9375rem
		}

		.star_b_img {
			position: absolute;
			left: 50%;
			margin-left: -21.875rem;
			width: 3.625rem;
			top: 16.6875rem
		}

		.star_c_img {
			position: absolute;
			left: 55%;
			margin-left: 15.625rem;
			width: 3.625rem;
			top: 5.625rem
		}

		.star_d_img {
			position: absolute;
			right: 5%;
			margin-right: 3.125rem;
			width: 3.625rem;
			top: 32.5rem
		}

		.coin_a_img {
			position: absolute;
			top: 27.1875rem;
			left: 10%;
			width: 7.0625rem
		}

		.coin_b_img {
			position: absolute;
			top: 14.875rem;
			right: 5%;
			width: 7.0625rem
		}

		.coin_c_img {
			position: absolute;
			top: 44.6875rem;
			right: 8%;
			width: 7.0625rem
		}

		.chips_a_img {
			position: absolute;
			left: 50%;
			margin-left: -18.75rem;
			width: 2.5rem;
			top: 10.4375rem
		}

		.chips_b_img {
			position: absolute;
			top: 8.75rem;
			right: 20%;
			width: 2.5rem
		}

		.head {
			// display: flex;
			// justify-content: center;
			text-align: center;


			.logo {
				width: 278.33px;
				// height: 59.96px;
				margin: 22px 0 36px 0;
			}

			.spin_box {
				position: relative;
				width: 30rem;
				height: 30rem;
				margin: 0rem auto 0;

				// margin: auto;
				.turntable {
					translate: none;
					rotate: none;
					scale: none;
					transform: translate(0px, 0px);
					position: absolute;
					left: 0;
					top: 0;
					right: 0;
					bottom: 0;

					.Turntableoutsieframe {
						position: absolute;
						width: 100%;
						height: 100%;

						left: 0;
						right: 0;
					}



					.turntable_item {
						position: absolute;
						height: 1.5rem;
						width: 8.75rem;
						top: 50%;
						left: 50%;
						line-height: 1.5rem;
						margin-top: -.75rem;
						-webkit-transform-origin: -4.1875rem center;
						-ms-transform-origin: -4.1875rem center;
						transform-origin: -4.1875rem center;
						margin-left: 4.1875rem;
						color: #fff;
						font-size: 1rem;
						display: -webkit-box;
						display: -webkit-flex;
						display: -ms-flexbox;
						display: flex;
						-webkit-align-items: center;
						-webkit-box-align: center;
						-ms-flex-align: center;
						align-items: center;
						-webkit-box-pack: justify;
						-webkit-justify-content: space-between;
						-ms-flex-pack: justify;
						justify-content: space-between;

						span {
							-webkit-flex: auto;
							-ms-flex: auto;
							flex: auto;
							white-space: nowrap;
							font-size: 19.05px;
							font-weight: 600;
							color: #282731;
						}

						img {
							height: 38.39px;
							width: 38.39px;
						}

						.iphone {
							width: 27.51px;
							height: 54.04px;
						}

						.switch {
							width: 53.99px;
							height: 42.54px;
						}

						&:nth-child(3) {
							transform: rotate(30deg);
						}

						&:nth-child(4) {
							transform: rotate(60deg);
						}

						&:nth-child(5) {
							transform: rotate(90deg);
						}

						&:nth-child(6) {
							transform: rotate(120deg);
						}

						&:nth-child(7) {
							transform: rotate(150deg);
						}

						&:nth-child(8) {
							transform: rotate(180deg);
						}

						&:nth-child(9) {
							transform: rotate(210deg);
						}

						&:nth-child(10) {
							transform: rotate(240deg);
						}

						&:nth-child(11) {
							transform: rotate(270deg);
						}

						&:nth-child(12) {
							transform: rotate(300deg);
						}

						&:nth-child(13) {
							transform: rotate(330deg);
						}

						&:nth-child(14) {
							transform: rotate(360deg);
						}
					}
				}

				.coco_img {
					position: absolute;
					width: 19.375rem;
					right: -21.25rem;
					bottom: -3.125rem;
				}

				.amount_img {
					position: absolute;
					width: 14.375rem;
					left: -14.375rem;
					bottom: -3.125rem;
				}

				.spin_btn {
					position: absolute;
					left: 49%;
					top: 50%;
					width: 4.75rem;
					cursor: pointer;
					-webkit-transform: translate(-50%, -50%);
					-ms-transform: translate(-50%, 50%);
					transform: translate(-50%, -50%);
					-webkit-animation: spinpulse 2s infinite;
					animation: spinpulse 2s infinite;

				}

				.spin_center {
					position: absolute;
					top: 50%;
					left: 50%;
					-webkit-transform: translate(-50%, -50%);
					-ms-transform: translate(-50%, -50%);
					transform: translate(-50%, -50%);
					width: 8.75rem;
				}

				.point_img {
					position: absolute;
					height: 8.5rem;
					right: -2.625rem;
					top: 10.26rem;
					width: 16.0625rem;
					-webkit-transform-origin: left center;
					-ms-transform-origin: left center;
					transform-origin: left center;

					.light_wrap {
						overflow: hidden;
						position: absolute;
						height: 5.625rem;
						width: 12.6875rem;
						top: 1.75rem;

						.point_light {
							top: 2.1875rem;
							left: -1.875rem;
							position: absolute;
							width: .9375rem;
							height: 3.25rem;
							z-index: 6;
							overflow: hidden;
							background: -webkit-gradient(linear, left top, right top, color-stop(0%, rgba(255, 255, 255, 0)), color-stop(50%, rgba(255, 255, 255, .2)), color-stop(100%, rgba(255, 255, 255, 0)));
							-webkit-transform: skewX(-25deg);
							-ms-transform: skewX(-25deg);
							transform: skew(-25deg);
						}
					}

					.spin_point {

						width: 100%;

					}

				}

				.Button {
					background: url('../../assets/images/spin/Button.png');
					background-size: 100% 100%;
					width: 25rem;
					height: 9rem;
					position: absolute;
					bottom: -5.525rem;
					left: 50%;
					margin-left: -12.75rem;
					font-size: 40px;
					font-weight: bold;
					color: #0C0D41;
					display: flex;
					justify-content: center;
					align-items: center;
					-webkit-animation: toggleScale-s1wut3m0 2s infinite both;
					animation: toggleScale-s1wut3m0 2s infinite both;
					cursor: pointer;
				}

			}

		}

		.payment {
			margin-top: 177px;
			display: flex;
			align-items: center;
			flex-direction: column;

			.nosso {
				font-size: 32px;
				color: #65BE3D;
				font-weight: 500;
			}

			.pix_img {
				margin-top: 56px;
				width: 309px;
			}

			.info {
				margin-top: 124px;
				display: flex;
				align-items: center;
				gap: 238px;

				.info_item {
					display: flex;
					flex-direction: column;
					justify-content: center;
					align-items: center;

					img {
						width: 158px;
						margin-bottom: 23px;
					}

					p {
						font-size: 32px;
						color: #65BE3D;
						font-weight: 500;
						margin-bottom: 3px;
					}

					a {
						color: #3EA0F1;
						font-size: 18px;
						font-weight: 400;
					}

					span {
						color: #9BA7B4;
						font-size: 18px;
					}
				}
			}
		}

		.bottom_font {
			margin-top: 124px;
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;

			p {
				font-size: 32px;
				color: #65BE3D;
				margin-bottom: 22px;
				font-weight: 600;
			}

			span {
				color: #3EA0F1;
				font-size: 18px;
				cursor: pointer;
			}
		}
	}

	.spin_rotate {
		-webkit-animation: router 3s ease-out forwards;
		animation: router 3s ease-out forwards;
	}

	.pointBg {
		-webkit-animation: pointBg 4.7s linear forwards;
		animation: pointBg 4.7s linear forwards;
	}


	.scale_up_hor_left {
		-webkit-animation: scale-up-hor-left 3.7s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
		animation: scale-up-hor-left 3.7s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
	}



}

@-webkit-keyframes router {
	0% {

		transform: rotate(0deg);

		// animation-timing-function: ease-out;
	}



	100% {

		transform: rotate(2220deg);
		animation-timing-function: cubic-bezier(0.645, 0.045, 0.355, 1);
	}
}

@media (max-width:768px) {
	.toTop {

		position: absolute;
		top: 1280px;
		z-index: 5;
		// width: 32px;
		// height: 32px;
		gap: 3px;

		p {
			font-size: 8.15px
		}

		img {
			// width: 4.52px;
			// height: 2.36px;
		}

	}

	:deep(.el-dialog__body) {
		width: 351px;
		height: 260px;
	}

	:deep(.el-overlay-dialog) {
		justify-content: center;
		align-items: center;

		.is-align-center {
			width: 351px;
			margin: 0;
		}
	}

	.spin {
		.spinBox {
			margin-bottom: 32px;
			.spin_btn{
				animation: none !important;
			}
			.bg {
				width: 34.625rem;
				height: 22.625rem;
				max-width: 100%;
				opacity: 0.24;
				-webkit-filter: blur(26px);
				filter: blur(26px);
				background-image: radial-gradient(circle at 50% 50%, #FF470D, rgba(0, 0, 0, 0) 65%);

			}

			.top {
				// display: none;
			}

			.bottom {
				bottom: -7%;
				// display: none;
			}


		}

		.spinBox2 {
			.Ontheleft {}

			.OntheRit {}

			.diamond_a_img {
				display: none;
			}

			.diamond_b_img {
				display: none;
			}

			.star_a_img {
				display: none;
			}

			.star_b_img {
				display: none;
			}

			.star_c_img {
				display: none;
			}

			.star_d_img {
				display: none;
			}

			.coin_a_img {
				display: none;
			}

			.coin_b_img {
				display: none;
			}

			.coin_c_img {
				display: none;
			}

			.chips_a_img {
				display: none;
			}

			.chips_b_img {
				display: none;
			}

			.coco_img {
				display: none;
			}

			.amount_img {
				display: none;
			}

			.head {
				overflow: hidden;

				.logo {
					margin-top: 67px;
					margin-bottom: 25px;
					width: 202px;
					// height: 43.52px;
				}

				.spin_box {
					// width: 318px;
					// height: 318px;
					// width: 100%;
					// overflow: hidden;
					-webkit-transform: scale(.8);
					-ms-transform: scale(.8);
					transform: scale(.8);
					left: -5%;

					.turntable {


						// margin-left: -.9375rem;
						margin-top: 0;

						.turntable_item {
							position: absolute;
							height: 1.5rem;
							width: 8.75rem;
							top: 50%;
							left: 50%;
							line-height: 1.5rem;
							margin-top: -.75rem;
							-webkit-transform-origin: -4.1875rem center;
							-ms-transform-origin: -4.1875rem center;
							transform-origin: -4.1875rem center;
							margin-left: 4.1875rem;
							color: #fff;
							font-size: 1rem;
							display: -webkit-box;
							display: -webkit-flex;
							display: -ms-flexbox;
							display: flex;
							-webkit-align-items: center;
							-webkit-box-align: center;
							-ms-flex-align: center;
							align-items: center;
							-webkit-box-pack: justify;
							-webkit-justify-content: space-between;
							-ms-flex-pack: justify;
							justify-content: space-between;

							span {
								// font-size: 11.66px;
								-ms-flex: auto;
								flex: auto;
								white-space: nowrap;
								// width: 66px;
								font-size: 1rem;
								// text-align: left;
							}

							img {
								height: 2.125rem;
								width: 2.125rem;
							}
						}
					}

					.point_img {
						height: 8.5rem;
						right: -1.825rem;
						top: 10.5rem;
						width: 15.5625rem;

						.spin_point {
							width: 100%;
						}
					}

					.Button {
						background: url('../../assets/images/spin/ButtonApp.png');
						background-size: 100% 100%;
						font-size: 24px;
						bottom: -3.525rem;
						left: 59%;
						width: 283.3px;
						height: 99px;
					}
				}
			}

			.payment {
				margin-top: 79px;

				.info {
					flex-direction: column;
					gap: 40px;
					margin-top: 44px;

					.info_item {
						img {
							width: 120px;
							margin-bottom: 14px;
						}

						p {
							font-size: 24px;
							margin-bottom: 11px;
						}

						span {
							font-size: 14px;
						}

						&:nth-child(2) {
							img {
								width: 138px;
							}
						}
					}

				}

				.nosso {
					font-size: 24px;
				}

				.pix_img {
					margin-top: 27px;
					width: 207px;
				}
			}

			.bottom_font {
				margin-top: 42px;

				p {
					font-size: 18px;
					white-space: pre-wrap;
					text-align: center;
					line-height: 21px;
				}

				span {
					font-size: 16px;
				}
			}
		}

	}

	@-webkit-keyframes router {
		0% {

			transform: rotate(0deg);

			// animation-timing-function: ease-out;
		}



		100% {

			transform: rotate(2220deg);
			animation-timing-function: cubic-bezier(0.645, 0.045, 0.355, 1);
		}
	}
}



@-webkit-keyframes spinpulse {
	0% {
		-webkit-transform: translate(-50%, -50%) rotate(-5deg) scale3d(1, 1, 1);
		-ms-transform: translate(-50%, -50%) rotate(-5deg) scale3d(1, 1, 1);
		transform:  rotate(-5deg) scaleZ(1)
	}

	50% {
		-webkit-transform: translate(-50%, -50%) rotate(0deg) scale3d(1.1, 1.1, 1.1);
		-ms-transform: translate(-50%, -50%) rotate(0deg) scale3d(1.1, 1.1, 1.1);
		transform: rotate(0) scale3d(1.1, 1.1, 1.1)
	}

	to {
		-webkit-transform: translate(-50%, -50%) rotate(-5deg) scale3d(1, 1, 1);
		-ms-transform: translate(-50%, -50%) rotate(-5deg) scale3d(1, 1, 1);
		transform: rotate(-5deg) scale3d(1)
	}
} 

@keyframes spinpulse {
	0% {
		-webkit-transform: translate(-50%, -50%) rotate(-5deg) scale3d(1, 1, 1); 
		-ms-transform: translate(-50%, -50%) rotate(-5deg) scale3d(1, 1, 1);
		transform: translate(-50%, -50%)  scale3d(1)
	}

	50% {
		-webkit-transform: translate(-50%, -50%) rotate(0deg) scale3d(1.1, 1.1, 1.1);
		-ms-transform: translate(-50%, -50%) rotate(0deg) scale3d(1.1, 1.1, 1.1);
		transform: translate(-50%, -50%)  scale3d(1.1, 1.1, 1.1)
	}

	to {
		-webkit-transform: translate(-50%, -50%) rotate(-5deg) scale3d(1, 1, 1);
		-ms-transform: translate(-50%, -50%) rotate(-5deg) scale3d(1, 1, 1);
		transform: translate(-50%, -50%)  scale3d(1)
	}
}



@-webkit-keyframes toggleScale-s1wut3m0 {
	0% {
		-webkit-transform: scale(1);
		-ms-transform: scale(1);
		transform: scale(1)
	}

	50% {
		-webkit-transform: scale(.97);
		-ms-transform: scale(.97);
		transform: scale(.97)
	}

	to {
		-webkit-transform: scale(1);
		-ms-transform: scale(1);
		transform: scale(1)
	}
}

@keyframes toggleScale-s1wut3m0 {
	0% {
		-webkit-transform: scale(1);
		-ms-transform: scale(1);
		transform: scale(1)
	}

	50% {
		-webkit-transform: scale(.97);
		-ms-transform: scale(.97);
		transform: scale(.97)
	}

	to {
		-webkit-transform: scale(1);
		-ms-transform: scale(1);
		transform: scale(1)
	}
}


@keyframes pointBg {
	0% {
		transform: skew(-25deg);
	}

	80% {
		transform: skew(-25deg);
	}

	100% {
		transform: translate(263px, 0px) skew(-25deg, 0deg) scale(4, 4);
	}
}

@-webkit-keyframes scale-up-hor-left {
	0% {
		-webkit-transform: scaleX(1);
		transform: scaleX(1);
		-webkit-transform-origin: 0% 0%;
		transform-origin: 0% 0%;
	}

	75% {
		-webkit-transform: scaleX(1);
		transform: scaleX(1);
		-webkit-transform-origin: 0% 0%;
		transform-origin: 0% 0%;
	}

	83% {
		-webkit-transform: scaleX(1.25);
		transform: scaleX(1.25);
		-webkit-transform-origin: 0% 0%;
		transform-origin: 0% 0%;
	}

	100% {
		-webkit-transform: scaleX(1);
		transform: scaleX(1);
		-webkit-transform-origin: 0% 0%;
		transform-origin: 0% 0%;
	}
}

@keyframes scale-up-hor-left {
	0% {
		-webkit-transform: scaleX(1);
		transform: scaleX(1);
		-webkit-transform-origin: 0% 0%;
		transform-origin: 0% 0%;
	}

	75% {
		-webkit-transform: scaleX(1);
		transform: scaleX(1);
		-webkit-transform-origin: 0% 0%;
		transform-origin: 0% 0%;
	}

	83% {
		-webkit-transform: scaleX(1.25);
		transform: scaleX(1.25);
		-webkit-transform-origin: 0% 0%;
		transform-origin: 0% 0%;
	}

	100% {
		-webkit-transform: scaleX(1);
		transform: scaleX(1);
		-webkit-transform-origin: 0% 0%;
		transform-origin: 0% 0%;
	}
}
</style>