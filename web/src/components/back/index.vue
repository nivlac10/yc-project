<template>
	<div>
		<div class="break">
			<div class="l_box" @click="breakToHome">
				<img src="@/assets/images/public/arrow_right.png" alt="">
				<p v-show="props.backNameShow">{{ t('btnName.voltar') }}</p>
			</div>
			<div class="title">
				<img v-show="props.img" :src="props.img" alt="">
				<span>{{ props.title }}</span>
			</div>
			<div></div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

const props = defineProps({
	backNameShow: {
		type: Boolean,
		default: true
	},
	img: {
		type: String,
		default: ''
	},
	title: {
		type: String,
		default: ''
	}
})
const router = useRouter();
const { t } = useI18n();

const breakToHome = () => {
	router.push('/')
}

</script>

<style scoped lang="scss">
.break {
	position: relative;
	border-radius: 12px;
	background: #202330;
	width: 100%;
	height: 58px;
	margin: 32px 0 16px 0;
	display: flex;
	justify-content: center;
	align-items: center;

	>div {
		// width: 100%;
	}

	.l_box {
		position: absolute;
		left: 0;
		cursor: pointer;
		display: flex;
		align-items: center;

		img {
			transform: rotate(180deg) scale(0.6);
			margin-left: 10px;
			margin-top: 2px;
		}

		p {
			color: #C3CFD9;
			font-size: 24px;
			font-weight: bold;
		}
	}

	.title {
		display: flex;
		align-items: center;
		text-align: center;

		img {
			margin-right: 12px;
			width: 25px;
		}

		span {
			font-size: 24px;
			font-weight: bold;
			color: #F8BF2E;
		}
	}
}

@media (max-width: 768px) {
	.break {
		height: 32px;
		border-radius: 8px;
		margin: 12px 0;

		.l_box {
			img {
				width: 18px;
				transform: rotate(180deg) scale(1);
				margin-right: 10px;
			}

			p {
				font-size: 16px;
			}
		}

		.title {
			img {
				margin-right: 8px;
				width: 20px;
			}

			span {
				font-size: 16px;
			}
		}
	}

}
</style>