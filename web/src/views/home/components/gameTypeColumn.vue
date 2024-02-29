<template>
	<div class="gameTypeColumn">
		<div class="columnb_box">
			<router-link v-for="(v, i) in columnList" :to="v.path" class="link_box" active-class="link_box_activ">
				<svg-icon :name="v.activeIcon" class="active"></svg-icon>
				<svg-icon :name="v.icon" class="no_active"></svg-icon>
				<span>{{ v.title }}</span>
			</router-link>
		</div>
		<seacrhGameName @def="changeGameName"></seacrhGameName>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { useStore } from "@/store/index";
import seacrhGameName from "@/components/searchGameName/index.vue"
import { useI18n } from "vue-i18n";

export default defineComponent({
	name: "index",
	components: {
		seacrhGameName
	},
	setup(props, { emit }) {
		const store = useStore();
		const { t, locale } = useI18n();
		const state = reactive({
			columnList: [
				{
					title: computed(() => t('gameType.Salão')),
					icon: "home",
					activeIcon: "home_active",
					path: "/clHome"
				},
				{
					title: computed(() => t('gameType.Coletar')),
					icon: "Coletar",
					activeIcon: "Coletar_active",
					path: "/flag"
				},
				{
					title: computed(() => t('gameType.InHouse')),
					icon: "in-house_active",
					activeIcon: "in-house",
					path: "/in-house"
				},
				{
					title: computed(() => t('gameType.Popular')),
					icon: "hot_icon",
					activeIcon: "hot_active",
					path: "/hot"
				},
				{
					title: computed(() => t('gameType.Slot')),
					icon: "slot",
					activeIcon: "slot_active",
					path: "/gameType/0"
				},
				// {
				// 	title: computed(() => t('gameType.JogosMesa')),
				// 	icon: "table",
				// 	activeIcon: "table_active",
				// 	path: "/gameType/1"
				// },
				// {
				// 	title: computed(() => t('gameType.Pescaria')),
				// 	icon: "fish",
				// 	activeIcon: "fish_active",
				// 	path: "/gameType/3"
				// },
				// {
				// 	title: computed(() => t('gameType.AoVivo')),
				// 	icon: "live",
				// 	activeIcon: "live_active",
				// 	path: "/gameType/2"
				// },
				// {
				// 	title: "Esportes",
				// 	icon: "Esportes",
				// 	activeIcon: "Esportes_active",
				// 	path: "/gameType/5"
				// },
			],
			active_index: 0
		});
		const changeGameName = (data) => {
			emit("def", data)
		}
		return { ...toRefs(state), changeGameName };
	},
});
</script>
<style  lang="scss" scoped>
@media (max-width: 750px) {
	.gameTypeColumn {
		background-color: rgba($color: #000000, $alpha: 0.0) !important;
		padding: 12px 0px !important;
		padding-top: 0 !important;
		flex-direction: column !important;
		gap: 12px !important;
		margin-bottom: 0px !important;
	}

	.columnb_box {
		overflow-x: scroll;
		width: 100%;

		.link_box {
			display: flex;
			flex-direction: column;
			align-items: center;
			background-color: #2F3445;
			width: 75px !important;
			flex-shrink: 0;
			border-radius: 8px;
			height: 64px !important;
			justify-content: center;

			// gap: 5px;

			svg {
				font-size: 30px !important;
			}

			span {
				font-size: 12px !important;
				// color: #98ABD0;
			}
		}
	}

}

.gameTypeColumn {
	background: #202431;
	border-radius: 16px 16px 16px 16px;
	padding: 10px 20px;
	margin-bottom: 20px;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.columnb_box {
	display: flex;
	gap: 10px;

	.link_box {
		display: flex;
		flex-direction: column;
		align-items: center;
		background-color: #2F3445;
		width: 90px;
		border-radius: 8px;
		height: 70px;
		justify-content: center;

		&:hover {
			background-color: #4181EE;

			.active {
				display: block;
			}

			.no_active {
				display: none;
			}

			span {
				color: #fff;
			}
		}

		// gap: 5px;
		.active {
			display: none;
		}

		svg {
			font-size: 44px;
			color: #98ABD0;
		}

		span {
			font-size: 14px;
			color: #98ABD0;
		}
	}

	.link_box_activ {
		background-color: #4181EE;

		.active {
			display: block;
		}

		.no_active {
			display: none;
		}

		svg {
			color: #fff;
		}

		span {
			color: #fff;
		}
	}
}

:deep(.search_box) {
	height: 44px;
}
</style>
  