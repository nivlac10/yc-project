<template>
	<div
		:class="{ el_input_box: true, noneInput: isHead, input_txt_red: props.inputRed == 0, input_txt_green: props.inputRed == 2, showInput: !isHead, inputFoucs: isInputFoucs }">
		<el-input :class="{ input_box_style: true, }" v-model="data" placeholder="" @change="inputChangeData"
			@focus="changeInputState('focus')" @blur="changeInputState('blur')" :disabled="props.isDisabled"
			:type="props.inputType" :show-password="inputType == 'password' ? true : false">
			<template #prepend>
				<p class="head" :style="`display:${props.isHead ? 'none' : 'block'}`">{{ props.headTxt }}</p>
				<slot name="head"></slot>
			</template>
			<template #append v-if="props.showBottom">
				<slot name="append">

				</slot>
			</template>
		</el-input>
		<slot name="bottom">

		</slot>
		<div
			:class="{ input_txt: true, input_box_hover: inputFoucs, input_txt_red: props.inputRed == 0, input_txt_green: props.inputRed == 2 }">
			{{
				props.popTxt

			}}
		</div>
	</div>
</template>
<script lang="ts">
import {
	reactive,
	toRefs,
	getCurrentInstance,
	defineComponent,
	computed,
	watch
} from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { stat } from "fs";

export default defineComponent({
	name: "referInput",
	props: {
		inputFoucs: null,
		inputRed: null,// 0 = 红色; 1 = 初始状态; 2 = 绿色
		isHead: {
			type: Boolean,
			default: true,
		},
		data: null,
		headTxt: null,
		popTxt: null,
		isDisabled: {
			type: Boolean,
			default: false
		},
		inputType: {
			type: String,
			default: 'text'
		},
		inputName: null,
		showBottom:{
			type: Boolean,
			default: false,
		}
	},
	setup(props, { emit }) {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const store = useStore();
		const { t } = useI18n();
		const state = reactive({
			inputTxtRed: computed(() => props.inputRed),
			inputFoucs: computed(() => props.inputFoucs),
			data: '',
			show: computed(() => props.isHead),
			change_state: false,
			isInputFoucs: false,

		});

		if (props.data) {
			state.data = JSON.parse(JSON.stringify(props.data));
		}

		console.log('state.data', state.data);


		const changeInputState = (val) => {
			if (props.inputName) {
				emit('changeInputState', val, state.data, props.inputName);
			}
			else {
				emit('changeInputState', val, state.data);
			}

			state.isInputFoucs = true;
		}

		const inputChangeData = () => {
			if (props.inputName) {
				emit('inputChangeData', state.data, props.inputName)
			} else {
				emit('inputChangeData', state.data)
			}

		}



		const changeShow = () => {
			state.change_state = true
			emit('inputChangeData', state.data)
			emit('changeInputState', true, state.data)
		}
		const changeInput = () => {
			let flag = false
			if (state.data) {
				state.change_state = true
				flag = true
			} else {
				state.change_state = false
				flag = false
			}
			emit('inputChangeData', state.data)
			emit('changeInputState', flag, state.data)
		}
		return {
			...toRefs(state),
			props,
			store,
			changeInputState,
			inputChangeData,
			t,
			changeInput,
			changeShow

		};
	},
});
</script>
<style  lang="scss" scoped> // :deep(.el-input-group){
 //      border-radius: 6px;
 //      background-color: #202330;
 //      box-shadow: 0 0 0 1px #7EC050 inset !important;
 //    }
 .inputFoucs {
 	.el-input-group {
 		box-shadow: 0 0 0 1px #fff inset;
 	}

 }

 .head {
 	// width: 100%;
 	text-align: left;
 }

 :deep(.el-input__wrapper input) {
 	// padding-left: 20px;
 }

 :deep(.el-input__wrapper) {

 	background: none;
 	box-shadow: none;

 	input {
 		color: #fff;
 		--el-input-inner-height: 40px;
 		font-size: 14px;
 	}

 }

 :deep(.el-input-group__prepend) {
 	background: none;
 	box-shadow: none;
 	padding: 0 0 0 13px;
 	height: 40px;
 }

 .el_input_box {
 	position: relative !important;

 	.input_box_style {
 		position: relative;
 		display: grid;
 		grid-template-columns: 20% 1fr;

 		:deep(.el-input__wrapper) {
 			input {
 				color: #fff;
 				//  padding-left: 104px !important;
 				--el-input-inner-height: 40px;
 				font-size: 14px;
 				border: #B2B6C5;
 				border-radius: 8px;

 			}



 			&::placeholder {
 				color: #B2B6C5;
 				font-size: 14px;
 			}
 		}
 	}

 	.input_txt {
 		position: absolute;
 		top: 12px;
 		left: 95px;
 		font-size: 14px;
 		background: #202330;
 		padding: 1px 5px;
 		box-sizing: border-box;
 		color: #B2B6C5;
 		pointer-events: none;
 		border: none;
 		transition: all .2s linear // display: none;
 	}

 	.input_box_hover {
 		color: #B2B6C5;
 		top: -12px;
 		left: -2.5% !important;
 		transform: scale(0.8);
 	}

 }

 @media (max-width: 768px) {

 	.el_input_box {
 		.input_box_style {
 			:deep(.el-input__wrapper) {
 				input {
 					//  padding-left: 80px !important;
 					--el-input-inner-height: calc(29px);
 					color: #fff !important;

 					&::placeholder {
 						font-size: 12px;
 					}
 				}
 			}
 		}
 	}

 	.input_txt {
 		left: 40px ;
 	}
 }
</style>
  