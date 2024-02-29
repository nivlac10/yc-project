<template>
	<div class="box" v-show="index">
		<p class="title" v-show="list[index[0]][index[1]]?.title">{{ list[index[0]][index[1]]?.title?.value }}</p>
		<p class="title2" v-show="list[index[0]][index[1]]?.title2">{{ list[index[0]][index[1]]?.title2?.value }}</p>
		<div v-show="list[index[0]][index[1]]?.font?.length > 0">
			<p class="font" v-for="(v, i) in list[index[0]][index[1]]?.font">{{ v.value }}</p>
		</div>

		<ul v-show="list[index[0]][index[1]]?.li?.length > 0">
			<li v-for="(v, i) in list[index[0]][index[1]]?.li">
				<p>{{ v.value }}</p>
			</li>
		</ul>

		<div v-show="list[index[0]][index[1]]?.li2?.length > 0">
			<p v-for="(v, i) in list[index[0]][index[1]]?.li2" class="li2">{{ v.value }}</p>
		</div>

		<div v-show="list[index[0]][index[1]]?.li3?.length > 0" class="title">
			<div v-for="v in list[index[0]][index[1]]?.li3" :key="v + 'li3'">
				<p class="title2" v-show="v?.title" style="margin-top: 32px;">{{ v.title.value }} </p>
				<p class="font" v-show="v?.font"> {{ v.font.value }}</p>
				<ul v-show="v?.li?.length > 0">
					<li v-for="(v, i) in v?.li" :key="i + v + 'li3'">
						<p>{{ v.value }}</p>
					</li>
				</ul>
			</div>
		</div>
		<privacyPolicy v-show="list[index[0]][index[1]]?.child"></privacyPolicy>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from "vue-i18n";
import { useStore } from '@/store/index';
import privacyPolicy from "./privacyPolicy.vue";
const store = useStore();
const { t } = useI18n();

let index = computed(() => store.state.help.index);
const list = computed(() => [
	[
		{
			title: computed(() => t('footer.SobreNós')),
			font: [
			computed(() => t('help.SobreNósFont',{url:store.state.conf.all_conf.platform['platform_url']})),
			],
		},
		{
			title: computed(() => t('help.CassinosResponsáveis')),
			font: [
			computed(() => t('help.CassinosResponsáveisFont')),
			],
		},
		{
			title: computed(() => t('help.TermosdeServiço')),
			font: [
			computed(() => t('help.TermosdeServiçoFont',{url:store.state.conf.all_conf.platform['platform_url'],title:store.state.conf.all_conf.platform['platform_title']})),
			],
		},
		{
			title: computed(() => t('help.PolíticadePrivacidade')),
			font: [
			computed(() => t('help.PolíticadePrivacidadeFont',{url:store.state.conf.all_conf.platform['platform_url']})),
			],
			child: true,
		},
		{
			title: computed(() => t('help.PolíticaKYC')),
			font: [
			computed(() => t('help.PolíticaKYCFont')),
			],
		},
		{
			title:  computed(() => t('help.Contralavagemdedinheiro')),
			font: [
			computed(() => t('help.ContralavagemdedinheiroFont')),
			],
		},
		{
			title:  computed(() => t('help.AutoExclusão')),
			font: [
			computed(() => t('help.AutoExclusãoFont')),
			],
		},
		{
			title: computed(() => t('help.ProteçãodosMenores')),
			font: [
			computed(() => t('help.ProteçãodosMenoresFont')),
			],
		},
	],
])

// console.log(list.value[index.value[0]][index.value[1]]?.li2);

</script>

<style lang="scss" scoped>
@media (max-width:768px) {
	.box {
		background: transparent !important;
		width: 100% !important;
		margin: 0 !important;
		padding: 0 !important;

		p {
			max-width: 100% !important;
		}

		.title {
			font-size: 18px !important;
			margin-bottom: 11px !important;
			margin-top: 14px !important;
		}

		.title2 {
			font-size: 13px !important;
			margin-bottom: 6px !important;
		}

		.font {
			font-size: 12px !important;
			line-height: 18px !important;
			margin-bottom: 9px !important;
		}

		ul {
			margin-top: 20px !important;

			li {
				margin-bottom: 4px !important;
				margin-left: 20px !important;

				p {
					font-size: 14px !important;
					line-height: 20px !important;
				}
			}

			li::marker {
				width: 6px !important;
				height: 6px !important;
			}
		}
	}
}

.box {
	word-wrap: break-word;
	padding: 0px 0 10px 0;
	width: calc(100% - 80px);
	background: var(--theme-box-background);
	border-radius: 12px;
	padding-left: 40px;
	padding-right: 40px;
	color: #fff;

	height: 75vh;
	overflow-y: scroll;

	p {
		// max-width: calc(100% - 137px);
		margin: 0;
		white-space: pre-wrap;
	}

	.title {
		color: var(--theme-checkbox-font-color);
		font-size: 18px;
		font-weight: bold;
		margin-bottom: 21px;
		margin-top: 30px;
	}

	.title2 {
		color: #B2B6C5;
		font-size: 22px;
		font-weight: bold;
		margin-bottom: 15px;
	}

	.font {
		color: #B2B6C5;
		font-size: 14px;
		line-height: 20px;
		font-weight: 400;
		margin-bottom: 7px;
	}

	ul {
		margin-top: 20px;
		margin-bottom: 20px;

		li {
			list-style-type: disc;
			color: #B2B6C5;
			margin-bottom: 6px;
			margin-left: 25px;

			p {
				line-height: 33px;
				font-size: 20px;
				font-weight: 500;
			}
		}

		li::marker {
			width: 8px;
			height: 8px;
		}
	}

	.li2 {
		line-height: 33px;
		font-size: 20px;
		font-weight: 500;
		color: #B2B6C5;
		margin-bottom: 6px;
	}
}
</style>