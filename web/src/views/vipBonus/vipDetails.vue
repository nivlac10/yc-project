<template>
	<div class="vipDetails">
		<back :backNameShow="false" :title="t('vipBonus.VIPNíveisCalendárioBônus')"></back>
		<img class="top_img" src="@/assets/images/vipBonus/vipDetails.png" alt="">
		<div class="max_box">
			<p>{{ t('vipBonus.NíveisRecompensasCalendário') }}</p>
			<span>{{ t('vipBonus.NíveisRecompensasCalendárioTxt') }}</span>
			<span>➡️ Telegram: <a style="color: #329AFB;" target="_blank"
					:href="store.state.conf.all_conf.tg_channel_url">{{
						store.state.conf.all_conf.tg_channel_url }}</a> </span>
		</div>
		<div class="max_box">
			<p>{{ t('vipBonus.ComoRecompensasCalendário') }}</p>
			<span>
				{{ t('vipBonus.ComoRecompensasCalendárioTxt') }}
			</span>
			<div class="min_box vipDetails2_box">
				<img class="vipDetails2" src="@/assets/images/vipBonus/vipDetails2.png" alt="">
				<span>
					{{ t('vipBonus.AquiestaaparênciadoCalendário') }}
				</span>
			</div>
		</div>
		<div class="max_box" v-if="store.state.status.isPc">
			<p>{{ t('vipBonus.DetalhamentosdasRecompensasCalendário') }}</p>
			<span>
				{{ t('vipBonus.DetalhamentosdasRecompensasCalendárioTxt') }}
			</span>
			<div class="min_box bonus_box">
				<img src="@/assets/images/header/Chest.png" alt="">
				<div>
					<p style="font-size: 22px;">{{ t('bonusCabinet.BônusCashback') }}</p>
					<span>
						{{ t('vipBonus.Semprequeapostarvocêreceberáimediatamente') }}
					</span>
				</div>
			</div>
			<div class="min_box bonus_box">

				<img src="@/assets/images/header/Chest2.png" alt="">
				<div>
					<p style="font-size: 22px;">{{ t('bonusCabinet.BônusDiário') }}</p>
					<span>
						{{ t('vipBonus.Oferecemosaosusuáriosbônusdiáriosgenerosos') }}
					</span>
				</div>

			</div>
			<div class="min_box bonus_box">

				<img src="@/assets/images/header/Chest3.png" alt="">
				<div>
					<p style="font-size: 22px;">{{ t('vipBonus.BônusSemana') }}</p>
					<span>
						{{ t('vipBonus.BônusSemanaTxt') }}
					</span>
				</div>

			</div>
			<div class="min_box bonus_box">
				<img src="@/assets/images/header/Chest4.png" alt="">
				<div>

					<p style="font-size: 22px;">{{ t('bonusCabinet.BônusMensal') }}</p>
					<span>
						{{ t('vipBonus.lendármêseumeasearltimasbôn') }}
					</span>
				</div>

			</div>
		</div>
		<div class="max_box" v-else>
			<p>{{ t('vipBonus.DetalhamentosdasRecompensasCalendário') }}</p>
			<span>
				{{ t('vipBonus.Nesteguiavamosexplicartodosos') }}
			</span>
			<div class="min_box bonus_box">
				<div> <img src="@/assets/images/header/Chest.png" alt="">
					<p style="font-size: 22px;">{{ t('bonusCabinet.BônusCashback') }}</p>
				</div>
				<span>
					{{ t('vipBonus.Semprequeapostarvocêreceberáimediatamentebônus') }}
				</span>

			</div>
			<div class="min_box bonus_box">
				<div>
					<img src="@/assets/images/header/Chest2.png" alt="">
					<p style="font-size: 22px;">{{ t('bonusCabinet.BônusDiário') }}</p>
				</div>
				<span>
					{{ t('vipBonus.Oferecemosiáriosgenerososquesão') }}
				</span>

			</div>
			<div class="min_box bonus_box">
				<div>
					<img src="@/assets/images/header/Chest3.png" alt="">
					<p style="font-size: 22px;">{{ t('bonusCabinet.BônusSemanal') }}</p>
				</div>
				<span>
					{{ t('vipBonus.enquantoosrestantesserãoadicionadoscalendário') }}
				</span>


			</div>
			<div class="min_box bonus_box">
				<div>
					<img src="@/assets/images/header/Chest4.png" alt="">
					<p style="font-size: 22px;">{{ t('bonusCabinet.BônusMensal') }}</p>
				</div>
				<span>
					{{ t('vipBonus.lendármêseumeasearltimasbôn') }}
				</span>

			</div>
		</div>
		<div class="max_box">
			<p>
				{{ t('vipBonus.BônusNível') }}
			</p>
			<span>
				{{ t('vipBonus.BônusNívelTxt') }}
			</span>
			<div class="min_box vip_lv_box">
				<div>
					<img src="@/assets/images/vipBonus/level_0.png" alt="">
					<span :style="`color:${fontColorList[0]}`">{{ t('vipBonus.Novatos') }}</span>
				</div>
				<div>
					<img src="@/assets/images/vipBonus/level_1.png" alt="">
					<span :style="`color:${fontColorList[1]}`">{{ t('vipBonus.Bronze') }}</span>
				</div>
				<div>
					<img src="@/assets/images/vipBonus/level_2.png" alt="">
					<span :style="`color:${fontColorList[2]}`">{{ t('vipBonus.Prata') }}</span>
				</div>
				<div>
					<img src="@/assets/images/vipBonus/level_3.png" alt="">
					<span :style="`color:${fontColorList[3]}`">{{ t('vipBonus.Ouro') }}</span>
				</div>
				<div>
					<img src="@/assets/images/vipBonus/level_4.png" alt="">
					<span :style="`color:${fontColorList[4]}`">{{ t('vipBonus.Platina') }}</span>
				</div>
				<div>
					<img src="@/assets/images/vipBonus/level_5.png" alt="">
					<span :style="`color:${fontColorList[5]}`">{{ t('vipBonus.Diamante') }}</span>
				</div>
				<div>
					<img src="@/assets/images/vipBonus/level_6.png" alt="">
					<span :style="`color:${fontColorList[6]}`">{{ t('vipBonus.DiamantedeSangue') }}</span>
				</div>
				<div>
					<img src="@/assets/images/vipBonus/level_7.png" alt="">
					<span :style="`color:${fontColorList[7]}`">{{ t('vipBonus.Vibranium') }}</span>
				</div>
			</div>
		</div>
		<div class="btn">
			<div @click="jump">
				{{ t('btnName.Obterbônus') }}
			</div>
		</div>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";
import back from "@/components/back/index.vue"
import router from "@/router";
import { useI18n } from "vue-i18n";
export default defineComponent({
	name: "vipDetails",
	components: {
		back
	},
	setup() {
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			fontColorList: ['#DBA786', '#DBA786', '#C3D3FF', '#E4C274', '#8BD5F1', '#E284D0', '#EC5B60', '#9EF6EE'],
		});

		const jump = () => {
			router.push('/vipBonus')
		}

		return { ...toRefs(state), store, jump, t };
	},
});
</script>
<style  lang="scss" scoped>
p {
	font-size: 24px;
	font-weight: 600;
	color: #F3B343;
	line-height: 28px;
}

div {
	display: flex;
	flex-direction: column;
	gap: 16px;
}

.min_box {
	background-color: #2F3445;
	border-radius: 16px;
	padding: 24px 36px;
}

span {
	font-weight: 400;
	color: #B2B6C5;
	line-height: 24px;
	font-size: 18px;
	// word-wrap: break-word;
	white-space: pre-wrap;
	// word-break: break-all;
	// line-break: normal;
	// line-break-after: ".";
	// word-break: break-all;
	word-wrap: break-word;
	word-break: keep-all;
}

.max_box {
	background-color: #202431;
	padding: 24px 36px;
	border-radius: 12px;

	>p {
		padding-left: 10px;
	}

	>span {
		padding-left: 10px;
	}
}

.top_img {
	margin-top: -16px;
	width: 100%;
	border-radius: 12px;
}

.bonus_box {
	display: flex;
	flex-direction: row;

	img {
		width: 154px;
		height: 154px;
	}

	span {
		font-size: 16px;

	}
}

.vip_lv_box {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	// align-items: center;

	div {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100px;

		img {
			width: 100%;
		}

		span {
			text-align: center;
		}
	}
}

.vipDetails2_box {
	max-width: 858px;
}

.btn {
	div {
		cursor: pointer;
		margin: 0 auto;
		width: 260px;
		height: 50px;
		line-height: 50px;
		text-align: center;
		font-size: 24px;
		font-weight: 600;
		color: #FFFFFF;
		background: #4181EE;
		border-radius: 12px;
	}
}

@media (max-width:750px) {
	.vipDetails {
		margin: 0 12px;
	}

	.vip_lv_box {
		display: grid !important;
		grid-template-columns: 1fr 1fr 1fr 1fr;
		gap: 5px !important;

		img {
			width: 56px !important;
		}

		div {
			gap: 0px !important;
			width: auto !important;
		}
	}

	.max_box {
		padding: 12px !important;
	}

	p {
		font-size: 16px !important;
	}

	span {
		font-size: 14px !important;
	}

	.bonus_box {
		flex-direction: column !important;
		align-items: center;

		div {
			display: flex !important;
			flex-direction: row;
			align-items: center;
			gap: 5px !important;
		}

		img {
			width: 38px !important;
			height: 38px !important;
		}
	}

	.min_box {
		padding: 8px !important;
		border-radius: 12px !important;

		span {
			font-size: 12px !important;
		}
	}

	div {
		display: flex;
		flex-direction: column;
		gap: 10px !important;
	}

	.btn {
		div {
			width: 150px;
			height: 36px;
			line-height: 36px;
			font-size: 16px;
			border-radius: 8px;
		}
	}
}
</style>
  