<template>
	<div>
		<div class="sidebar">
			<div class="title">{{ t('help.CentrodeAjuda') }}</div>
			<div class="list">
				<ul>
					<li v-for=" (v, i) in list[0]" :key="v" @click="isClick([0, i])">
						<span
							:style="`color:${clickIndex[0] == 0 && clickIndex[1] == i ? 'var(--theme-checkbox-font-color)' : 'var( --auxiliary-font-color-9);'}`">{{
								v.value }}</span>
					</li>
				</ul>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useI18n } from "vue-i18n";
import { useStore } from '@/store/index';
import { useRoute } from 'vue-router';
const { t } = useI18n();
const Store = useStore();
const route = useRoute()
const clickIndex = computed(() => Store.state.help.index);
const list = computed(() => [
	[
		computed(() => t('footer.SobreNós')),
		computed(() => t('footer.CassinoResponsáveis')),
		computed(() => t('footer.TermosdeServiço')),
		computed(() => t('footer.PolíticadePrivacidade')),
		computed(() => t('footer.PolíticaKYC')),
		computed(() => t('footer.Contralavagemdedinheiro')),
		computed(() => t('footer.AutoExclusão')),
		computed(() => t('footer.ProteçãodosMenores')),
	],

]);


function isClick(v) {
	clickIndex.value = v;
	Store.commit('help/setIndex', v);
}
watch(() => route.query.l_index, () => {
	if (route.query.l_index) {

		isClick([route.query.l_index, route.query.r_index])
	}
}, {
	deep: true
})

</script>

<style  lang="scss" scoped>
.sidebar {
	padding: 0px 0 10px;
	width: 100%;
	height: 75vh;
	overflow-y: scroll;
	background: var(--theme-menu-background);
	border-radius: 12px;

	.title {
		font-size: 14px;
		font-weight: bold;
		width: calc(100% - var(--help-left-padding-left));
		height: 42px;
		background: #2F3445;
		padding-left: var(--help-left-padding-left);
		display: flex;
		align-items: center;
		color: #B2B6C5;
	}

	.list {
		margin: 25px 0 25px 0;
		padding-left: var(--help-left-padding-left);

		ul {
			li {
				cursor: pointer;
				display: flex;
				align-items: center;
				margin-bottom: 12px;

				span {
					font-size: 14px;
					color: var(--theme-font-color-fff);
					vertical-align: middle;
				}
			}
		}
	}

}
</style>