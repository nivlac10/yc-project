<template>
	<div class="home_game_gap">
		<!-- <homeGameBox :game_id="22">
            <slot>
                <div class="game_box_title">
                    <span> Texas Hold em Poker </span>
                    <gameRtpBox style="margin-left: 16px;"  v-if="store.state.status.isPc">
                    </gameRtpBox>
                </div>
            </slot>
        </homeGameBox> -->
		<homeGameBox :jump_index="1">
			<slot>
				<div class="game_box_title">
					<svg-icon name="in-house_active"></svg-icon>
					<span>{{ t('gameType.InHouse') }}</span>
					<gameRtpBox style="margin-left: 16px;" v-if="store.state.status.isPc"></gameRtpBox>
				</div>
			</slot>
		</homeGameBox>
		<!-- <texasPoker></texasPoker> -->
		<homeGameBox :jump_index="2">
			<slot>
				<div class="game_box_title">
					<svg-icon name="hot_icon"></svg-icon>
					<span>{{ t('gameType.Popular') }}</span>
					<!-- <gameRtpBox style="margin-left: 16px;" v-if="store.state.status.isPc"></gameRtpBox> -->
				</div>
			</slot>
		</homeGameBox>



		<!-- <factory_list></factory_list>
		<homeGameBox :game_type="v.type" v-for="(v, i) in game_type">
			<slot>
				<div class="game_box_title">
					<span>{{ v['name'] }}</span>
					<gameRtpBox style="margin-left: 16px;" v-if="store.state.status.isPc"></gameRtpBox>
				</div>
			</slot>
		</homeGameBox> -->

		<homeGameBox v-for="(v, i) in factory_list" :key="v" :game_id="v['game_id']">
			<slot>
				<div class="game_box_title">
					<span>{{ v['game_name'] }}</span>
					<gameRtpBox style="margin-left: 16px;" v-if="store.state.status.isPc && v['game_id'] != 20">
					</gameRtpBox>
				</div>
			</slot>
		</homeGameBox>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { useStore } from "@/store/index";
import factory_list from "../components/factory_list.vue";
import homeGameBox from "../components/homeGameBox.vue";
import gameRtpBox from "@/components/gameRtpBox/index.vue"
// import texasPoker from "./texasPoker.vue"
import { useI18n } from "vue-i18n";

export default defineComponent({
	name: "clHome",
	components: { factory_list, homeGameBox, gameRtpBox },
	setup() {
		const store = useStore();
		const { t, locale } = useI18n();
		const state = reactive({
			factory_list: [],
			game_type: [
				{
					name: computed(() => t('gameType.Slot')),  // slot
					type: 0
				}, {
					name: computed(() => t('gameType.JogosMesa')), // table
					type: 1
				}, {
					name: computed(() => t('gameType.Pescaria')),  // 捕鱼
					type: 3
				}, {
					name: computed(() => t('gameType.AoVivo')),  // 真人视讯
					type: 2
				}
			]
		});
		state.factory_list = store.state.conf.game_list.factory_list as any;
		return { ...toRefs(state), t, store };
	},
});
</script>
<style  lang="scss" scoped>
.home_game_gap {
	display: flex;
	flex-direction: column;
	gap: 20px;
}

.game_box_title {
	display: flex;
	align-items: center;
	gap: 5px;

	span {
		font-size: 18px;
		font-weight: 400;
	}

	svg {
		font-size: 40px;
	}
}

@media (max-width: 768px) {
	.home_game_gap {
		gap: 16px !important;
	}

	.game_box_title {
		display: flex;
		align-items: center;
		gap: 5px;

		span {
			font-size: 14px !important;
			// font-weight: 400;
		}

		svg {
			font-size: 30px !important;
		}
	}
}
</style>
  