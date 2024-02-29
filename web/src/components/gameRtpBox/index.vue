<template>
	<div>
		<div class="rtp_max_box">
			<img src="@/assets/images/home/até.png" alt="">
			<span class="rtp">{{ t('gameType.RTPaté') }} <span class="ate"> {{ randomDouble }}%</span></span>
		</div>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
export default defineComponent({
	name: "",
	components: {

	},
	setup() {
		const store = useStore();
		const { t, locale } = useI18n();
		const state = reactive({
		});
		function getRandomDouble(min, max) {
			return Math.random() * (max - min) + min;
		}

		const min = 97;
		const max = 99;

		const randomDouble = getRandomDouble(min, max).toFixed(2);
		return { ...toRefs(state), store, t, randomDouble };
	},
});
</script>
<style  lang="scss" scoped>
.rtp_max_box {
	display: flex;
	justify-content: center;
	border-radius: 100px;
	align-items: center;
	background-color: #2F3445;
	// width: 100%;
	padding: 6px 13px;

	img {
		height: 18px;
	}

	.rtp {
		font-size: 12px;
		color: #98ABD0;
	}

	.ate {
		font-size: 14px;
		color: #F3B343;
	}
}
</style>
  