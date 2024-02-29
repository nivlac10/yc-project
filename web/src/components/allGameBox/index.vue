<template>
	<div>
		<div class="factory">
			<div v-for="(item, index) in factory_list" :key="index"
				:class="{ factory_box: true, factory_active: factoryIndex == index }"
				@click="changeFactory(item), factoryIndex = index">
				<span>{{ item['game_name'] }}</span>
			</div>
		</div>
		<div class="changeGameSelectData">
			<searchGameName @def="changeGameName"></searchGameName>
			<selectGameTypeBox :options="options" @selectChange="selectChange"></selectGameTypeBox>
		</div>
		<gameList class="gamePopCss" :gameList="game_list" :count="count" @def="getGamedata()"></gameList>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch, computed } from "vue";
import { useStore } from "@/store/index";
import { useRouter, useRoute } from "vue-router";
import gameList from "@/components/gameList/index.vue"
import { get_game_data } from "@/utils/gameUtils";
import searchGameName from "@/components/searchGameName/index.vue"
import selectGameTypeBox from "../selectGameTypeBox/index.vue";
import { useI18n } from "vue-i18n";

export default defineComponent({
	name: "gameType",
	props: {
		game_id: {
			type: Number,
			default: null
		}
	},
	components: {
		gameList,
		searchGameName,
		selectGameTypeBox
	},
	setup(props) {
		const store = useStore();
		const { t, locale } = useI18n();
		const route = useRoute();
		const state = reactive({
			game_list: [],
			count: 0,
			factory_list: [
				{
					game_name: computed(() => t('gameText.Todo')),
					game_id: null
				}
			],
			pageFrom: {
				page: 1,
				limit: 28,
				gameName: "",
				game_type: null,
				game_id: null
			},
			factoryIndex: 0,
			loading: true,
			options: [
				{ label: computed(() => t('gameText.TodosOsJogos')), value: null },
				{ label: computed(() => t('gameType.Slot')), value: 0 },
				{ label: computed(() => t('gameType.JogosMesa')), value: 1 },
				{ label: computed(() => t('gameType.AoVivo')), value: 2 },
				{ label: computed(() => t('gameType.Pescaria')), value: 3 }
			]

		});
		// @ts-ignore
		state.pageFrom.game_id = props.game_id
		state.pageFrom.limit = store.state.status.isPc ? 28 : 30;
		// 监听路由
		watch(() => props.game_id, (newData, oldData) => {
			state.game_list = []
			state.factory_list = [
				{
					game_name: computed(() => t('gameText.Todo')) as any,
					game_id: null
				}
			]
			state.factoryIndex = 0
			state.pageFrom = {
				page: 1,
				limit: store.state.status.isPc ? 28 : 12,
				gameName: "",
				game_type: null,
				// @ts-ignore
				game_id: newData
			}
			resettingFactory()
			getGamedata()
		})

		// 重置厂商默认选中
		function resettingFactory() {
			let factory_list = store.state.conf.game_list.factory_list
			for (let index = 0; index < factory_list.length; index++) {
				const element = factory_list[index];
				if (element.game_id == props.game_id) {
					state.factoryIndex = index + 1
				}
				// @ts-ignore
				state.factory_list.push(element)
			}
		}
		resettingFactory()
		function getGamedata() {
			let game_data = get_game_data(state.pageFrom.game_id, state.pageFrom.game_type, state.pageFrom.gameName, null, null, null, state.pageFrom.page, state.pageFrom.limit) as never;
			let game_list = game_data['allGameList'] as any

			for (let index = 0; index < game_list.length; index++) {
				const element: never = game_list[index] as never;
				state.game_list.push(element)
			}
			state.count = game_data['count']
			state.pageFrom.page++
		}
		getGamedata()
		function changeFactory(item) {
			state.game_list = []
			state.pageFrom.game_id = item.game_id
			state.pageFrom.page = 1
			getGamedata()
		}
		const changeGameName = (v) => {
			if (v) {
				state.pageFrom.gameName = v
			} else {
				//@ts-ignore
				state.pageFrom.gameName = null
			}
			state.game_list = []
			state.pageFrom.page = 1
			getGamedata()
		}
		const selectChange = (v) => {
			state.game_list = []
			state.pageFrom.game_type = v.value
			state.pageFrom.page = 1
			getGamedata()
		}
		return { ...toRefs(state), t, store, getGamedata, changeFactory, changeGameName, selectChange };
	},
});
</script>
<style lang="scss">
.changeGameSelectData {
	display: grid;
	grid-template-columns: 3fr 1fr;
	gap: 12px;
	margin-bottom: 23px;
	height: 40px;

}

:deep(.search_box) {
	height: auto !important;
	background-color: #1B1F29 !important;
}

@media screen and (max-width: 768px) {
	.changeGameSelectData {
		grid-template-columns: 1fr 1fr !important;
	}
}
</style>