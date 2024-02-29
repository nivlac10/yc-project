<!--
 * @Author: haosan 123@qq.com
 * @Date: 2023-08-25 21:20:36
 * @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 * @LastEditTime: 2023-10-31 16:16:48
 * @FilePath: \web1.1\src\components\message\message.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
	<Transition name="down">
		<div class="my-message" :style="style[type]" v-show='isShow' @click="isShow = false">
			<!-- 上面绑定的是样式 -->
			<!-- 不同提示图标会变 -->
			<!-- <i class="iconfont" :class="[style[type].icon]"></i> -->
			<div class="box">
				<img :src="[style[type].icon]" />
				<div>
					<div class="text">{{ text }}</div>
					<div class="tips" v-if="tips != ''">{{ tips }}</div>
				</div>
			</div>
		</div>
	</Transition>
</template>
<script>
import { onMounted, ref } from 'vue'
import { getImageUrl } from "@/utils/baseFun";
export default {
	name: 'notificationPopup',
	props: {
		text: {
			type: String,
			default: ''
		},
		type: {
			type: String,
			// warn 警告  error 错误  success 成功
			default: 'warn'
		},
		tips: {
			type: String,
			default: ''
		}
	},
	setup() {
		// 定义一个对象，包含三种情况的样式，对象key就是类型字符串
		const style = {
			warn: {
				icon: getImageUrl('public/mistake.png'),
				color: '#E6A23C',
				backgroundColor: 'rgb(253, 246, 236)',
				borderColor: 'rgb(250, 236, 216)'
			},
			error: {
				icon: getImageUrl('public/mistake.png'),
				color: '#fff',
				backgroundColor: '#EB4859',
				// borderColor: 'rgb(253, 226, 226)'
			},
			success: {
				icon: getImageUrl('public/Shut_down_g.png'),
				color: '#fff',
				backgroundColor: '#1CB83D',
				borderColor: 'rgb(225, 243, 216)'
			}
		}
		// console.log(style.warn);
		// 控制动画
		const isShow = ref(false)
		// 组件模板渲染成功后触发
		onMounted(() => {
			isShow.value = true
		})
		return { style, isShow }
	}
}
</script>
<style scoped lang="scss">
.down {
	&-enter {
		&-from {
			transform: translate3d(0, -75px, 0);
			opacity: 0;
		}

		&-active {
			transition: all 0.5s linear;
		}

		&-to {
			transform: none;
			opacity: 1;
		}
	}
}

.my-message {
	// width: 169px;
	transition: all 0.5s linear;
	// height: 40px;
	position: fixed;
	z-index: 9999;
	left: 50%;
	transform: translateX(-50%);
	// top: 10%;
	// margin-left: -150px;
	top: 25px;
	padding: 10px 22px 12px 25px;
	min-width: 322px;
	// border: 1px solid #e4e4e4;
	background: #f5f5f5;
	color: #999;
	display: flex;
	justify-content: flex-start;
	align-items: center;
	border-radius: 22px;
	box-sizing: border-box;

	.box {
		display: flex;

		img {
			width: 24px;
			height: 24px;
			margin-right: 13px;
		}

		.text {
			font-size: 20px;
			padding-top: 3px;
			vertical-align: middle;
			white-space: nowrap;
			font-weight: 600;
		}

		.tips {
			padding-top: 9px;
			font-size: 14px;
			line-height: 18px;
		}
	}
}

@media (max-width: 768px) {
	.my-message {
		padding: 10px 22px 12px 25px;
		min-width: 300px;

		.box {
			display: flex;

			img {
				width: 18px;
				height: 18px;
				margin-right: 10px;
			}

			.text {
				font-size: 16px;
				padding-top: 2px;
			}

			.tips {
				padding-top: 6px;
				font-size: 14px;
				line-height: 18px;
			}
		}
	}
}
</style>
   