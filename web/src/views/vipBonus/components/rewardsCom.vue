<template>
	<div :class="{ rewardsCom: true, rewardsCom_border: (props as any).data.state == 0 }">
		<rewards-up-status :dataObj="props.data" />
		<ul class="rewardsCom_ul" :style="`${setUlWidth((props as any).data.data.length)}; `"
			v-if="(props as any).data.state != 2 && (props as any).data.state != 3">
			<li v-for="(v, i) in (props as any).data.data" :key="i"
				:style="`width: ${setWidth((props as any).data.data.length)};`">
				<rewards-middle-status :dataObj="v" :dataObj2="(props as any).data.data" />
			</li>
		</ul>
		<img v-else class="gold_img" src="@assets/images/vipBonus/Gold_icon.png" alt="">
		<rewards-down-status :dataObj="props.data" :dataObj2="(props as any).data.data" />
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import rewardsUpStatus from "./rewardsUpStatus.vue";
import rewardsMiddleStatus from "./rewardsMiddleStatus.vue";
import rewardsDownStatus from "./rewardsDownStatus.vue";
export default defineComponent({
	name: "rewardsCom",
	components: { rewardsUpStatus, rewardsMiddleStatus, rewardsDownStatus },
	props: {
		data: Object
	},
	setup(props) {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			dataObj: props.data
		});

		const setUlWidth = (length: number) => {
			if (length >= 18) {
				return 'row-gap:0px;padding:5px 0;'
			}
		}

		const setWidth = (length: number) => {
			if (length <= 8) return `calc(22% - 6px)`
			else if (length > 8 && length <= 15) return `calc(20% - 6px)`
			else return `calc(15% - 6px)`
		}

		return { ...toRefs(state), store, t, props, setWidth, setUlWidth };
	},
});
</script>
<style lang="scss">
.el_popover_style {
	// min-width: 220px !important;
	// width: 100% !important;
	border: none !important;
	border-radius: 12px !important;
	font-size: 20px !important;
	background: #2F3445 !important;
	box-shadow: 0px 0px 12px 0px rgba(0, 0, 0, .4) !important;

	.popover_content {
		padding: 5px 0;
		// white-space: nowrap;

		.popover_content_txt {
			// display: flex;
			width: 100% ;
			font-size: 14px ;
			font-weight: 400 ;
			color: var(--auxiliary-font-color-9) ;

		}
	}

	.el-popper__arrow {
		&::before {
			background: #2F3445 !important;
			border: none !important;
		}
	}
}

.rewardsCom {
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	height: 225px;
	padding: 22px 0 15px 0;
	box-sizing: border-box;
	background: #2F3445;
	border-radius: 12px;
	border: 4px solid transparent;

	&.rewardsCom_border {
		border-color: #52FB59;
		box-shadow: 0px 0px 10px 0px rgba(148, 239, 90, 0.25);
	}

	.rewardsCom_ul {
		display: flex;
		justify-content: center;
		flex-wrap: wrap;
		padding: 0 10px;
		row-gap: 4px;
		justify-items: center;
		margin-right: -6px;
		overflow: scroll;

		>li {
			margin-right: 6px;
			width: calc(14.2857% - 6px);
		}
	}

	.gold_img {
		display: block;
		margin: 0 auto;
		padding: 36px 0 24px 0;
		width: 47px;

		img {}
	}
}

@media (max-width: 768px) {
	.rewardsCom {
		height: 200px;
		padding: 18px 0 10px 0;
		border: 2px solid transparent;

		.rewardsCom_ul {
			padding: 0 6px;
			row-gap: 0px;
		}

		.gold_img {
			padding: 21px 0 24px 0;
			width: 37px;

			img {}
		}
	}
}
</style>
  