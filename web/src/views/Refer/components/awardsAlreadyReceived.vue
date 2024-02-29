<template>
	<div class="awardsAlreadyReceived">
		<div class="awardsAlreadyReceived_title">{{ t('refer.RECEBAOSEUBÔNUS') }}</div>
		<div class="bets_list">
			<div class="bets_list_column">
				<div>{{ t('refer.Jogador') }}</div>
				<div>{{ t('refer.Horário') }}</div>
				<div>{{ t('refer.NúmeroVálidoConvites') }}</div>
				<div>{{ t('refer.Bônus') }}</div>
			</div>
			<ul>
				<transition-group name="Betroll" tag="p">
					<li v-for="(item, index) in (give_list as any)" :key="item">
						<div class="game_column">
							<img :src="getImageUrl(`avatar/headsculpture_img_${item.icon}.png`)" alt="" />
							<span class="text_hiding">{{ item.username }}</span>
						</div>
						<div class="font_column">{{ item.tiem }}</div>
						<div class="font_column">{{ item.num }}</div>
						<div class="font_column font_column_color">{{ item.bonus }}</div>
					</li>
				</transition-group>
				<div class="maskAwa"></div>
			</ul>
		</div>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, onBeforeUnmount, ref, onMounted, watch } from "vue";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { ReferService } from "@/api/refer";
import { getImageUrl } from "@/utils/baseFun";

export default defineComponent({
	name: "awardsAlreadyReceived",
	setup() {
		const store = useStore();
		const { t } = useI18n();
		const { proxy } = getCurrentInstance() as any;
		const state = reactive({
			task_list: null,
			give_list: [],
			pageFrom: {
				page: 1,
				limit: 10
			},
		});

		proxy.$mitt.on('getListData', async (val) => {
			// let res = await ReferService.get_user_invite_state();
			state.task_list = val;
		})
		const getData = async () => {
			let res = await ReferService.get_user_invite_state();
			state.task_list = res.data.data;
		}
		getData();
		console.log(state.task_list);

		// 随机添加佣金领取列表
		let randTime = 1500
		let giveListInte = setInterval(() => {
			let settiem = setTimeout(() => {
				loadGiveList()
				randTime = getRandom(500, 2000)
				clearTimeout(settiem)
			}, randTime);

		}, 1500);
		let randListNum = 10
		function loadGiveList() {
			if (state.task_list) {
				for (let index = 0; index < randListNum; index++) {
					// let loadDataTime = setTimeout(() => {
					let task_index = getRandom(0, state.task_list['length'])
					let task_conf = state.task_list[task_index]
					let data = {
						username: getRandom(1135468, 2649456),
						tiem: getRandom(2, 5) + 's',
						num: task_conf['num'],
						bonus: t('base.currencySymbol') + task_conf['money'],
						icon: getRandom(0, 18)
					}
					state.give_list.unshift(data as never)
					if (state.give_list.length > 10) {
						state.give_list.pop()
					}
					// }, 500);
					// clearTimeout(loadDataTime)
				}
				randListNum = getRandom(1, 4)
			}

		}
		// 获取随机数
		function getRandom(min, max) {
			let num = Math.random() * (max - min) + min
			return parseInt(num)
		}
		// 随机姓名
		function randomCoding() {
			var result = [];
			let n = 3;//这个值可以改变的，对应的生成多少个字母，根据自己需求所改
			for (var i = 0; i < n; i++) {
				//生成一个0到25的数字
				var ranNum = Math.ceil(Math.random() * 25);
				//大写字母'A'的ASCII是65,A~Z的ASCII码就是65 + 0~25;
				//然后调用String.fromCharCode()传入ASCII值返回相应的字符并push进数组里
				result.push(String.fromCharCode(65 + ranNum) as never);
			}
			return result.join('');
		}

		onBeforeUnmount(() => {
			clearInterval(giveListInte)
		})
		return { ...toRefs(state), t, getImageUrl };
	},
});
</script>
<style  lang="scss" scoped>
.awardsAlreadyReceived {
	// padding: 16px 0;
	margin-bottom: 24px;

	.awardsAlreadyReceived_title {
		margin-bottom: 20px;
		font-size: 24px;
		font-weight: bold;
		color: #B2B6C5;
	}

	.bets_list {
		height: 460px;
		overflow: hidden;
		border-radius: 24px;

		.bets_list_column {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 20px 80px;
			background: #202431;
			display: grid;
			grid-template-columns: repeat(4, 1fr);

			div {
				font-size: 16px;
				color: #B2B6C5;
				// font-weight: 550;


				&:nth-child(1) {
					// width: 40%;
				}

				&:nth-child(2) {
					text-align: center;
					// width: 20%;
				}

				&:nth-child(3) {
					// width: 27%;
				}

				&:nth-child(3) {
					text-align: center;
				}

				&:nth-child(4) {
					text-align: right;
					// width: 14%;
				}
			}
		}

		ul {
			position: relative;
			background: #2F3445;
			padding: 20px 80px;
			margin-bottom: 6px;
			box-sizing: border-box;
			height: 100%;

			li {
				// display: flex;
				// justify-content: space-between;
				display: grid;
				grid-template-columns: repeat(4, 1fr);
				align-items: center;
				border-radius: 10px;
				margin-bottom: 7px;

				&:nth-child(2) {
					text-align: right;
				}

				.game_column {
					display: flex;
					align-items: center;
					// width: 40%;

					img {
						margin-right: 10px;
						width: 29px;
						height: 29px;
					}

					span {
						display: inline-block;
						font-size: 15px;
						color: #B2B6C5;
					}
				}



				.font_column {
					// width: 20%;
					font-weight: bold;
					font-size: 15px;
					color: #B2B6C5;

					&:nth-child(2),
					&:nth-child(3) {
						text-align: center;
					}

					&:nth-child(4) {
						text-align: right;
					}

					&.font_column_color {
						color: var(--auxiliary-font-color-7);
					}
				}
			}


		}
	}

	.list_h {
		height: 660px;
		background: #1D1C43;
	}

	.maskAwa {
		position: absolute;
		bottom: 55px;
		height: 29px;
		width: 100%;
		border-radius: 12px;
		z-index: 1;
		background: #2F3445;
		left: 0;
	}
}

@media screen and (max-width: 768px) {


	.list_h {
		height: 495px !important;
	}

	.awardsAlreadyReceived {
		padding-top: 12px;

		.maskAwa {
			position: absolute;
			bottom: 0px;
			height: 74px;
			width: 100%;
			border-radius: 12px;
			z-index: 1;
			background: #2F3445;
		}

		.awardsAlreadyReceived_title {
			margin-bottom: 16px;
			font-size: 16px;
		}

		.bets_list {
			height: 324px !important;
			border-radius: 12px;
			margin-bottom: 12px;

			.bets_list_column {
				padding: 12px 12px;
				border-radius: 12px 12px 0px 0px;

				div {
					font-size: 10px;
				}
			}

			ul {
				padding: 8px 12px;

				li {
					.game_column {
						img {
							margin-right: 5px;
							width: 18px;
							height: 18px;
						}

						span {
							font-size: 12px;
							font-weight: 500;
						}
					}

					.font_column {
						font-size: 12px;
						font-weight: 500;
					}
				}
			}
		}
	}
}
</style>
