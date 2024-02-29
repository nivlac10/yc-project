<template>
	<el-upload class="avatar-uploader" :show-file-list="false" :before-upload="beforeAvatarUpload">
		<img v-if="props.img" :src="state.img" class="avatar" />
		<el-icon v-else class="avatar-uploader-icon">
			<Plus />
		</el-icon>
	</el-upload>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed, nextTick } from "vue";
import { ElMessage, type UploadProps } from 'element-plus'
import { } from "process";

const props = defineProps({
	img: String
})
const emit = defineEmits(["getImgData"])

const state = reactive({
	img: props.img,
})
let flag = true;
watch(() => props.img, (n) => {
	console.log('watch', n);
	if (flag) {
		flag = false;
		state.img = props.img;
	}

})

const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
	//@ts-ignore
	console.log(rawFile.type)
	if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/jpg' && rawFile.type !== 'image/png' && rawFile.type !== 'image/svg+xml') {
		ElMessage.error('请上传图片格式!')
		return false
	} else if (rawFile.size / 1024 / 1024 > 2) {
		ElMessage.error('图片大小不能大于2MB!')
		return false
	}
	state.img = URL.createObjectURL(rawFile!)
	emit('getImgData', rawFile)
	// if (rawFile.type !== 'image/jpeg') {
	// 	// ElMessage.error('Avatar picture must be JPG format!')
	// 	return false
	// } 
	// return true
}
</script>

<style lang="scss" scoped>
:deep(.el-upload) {
	border: 1px dashed var(--el-border-color);
	border-radius: 6px;

	.avatar {
		height: auto;
		width: 100%;
		display: block;
	}

	.avatar-uploader .el-upload {
		cursor: pointer;
		position: relative;
		overflow: hidden;
		transition: var(--el-transition-duration-fast);
	}

	.avatar-uploader .el-upload:hover {
		border-color: var(--el-color-primary);
	}

	.el-icon.avatar-uploader-icon {
		font-size: 28px;
		color: #8c939d;
		width: 178px;
		height: 178px;
		text-align: center;
	}

}
</style>
