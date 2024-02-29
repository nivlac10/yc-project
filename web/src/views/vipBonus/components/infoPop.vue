<template>
	<div>
		<el-popover placement="top-start" :title="props.title" trigger="hover" :teleported="false" :content="props.content">
			<template #reference>
				<div class="btnTitle">
					<img src="@assets/images/public/query.png" alt="">
				</div>
			</template>
		</el-popover>
	</div>
</template>

<script setup lang="ts">
const props = defineProps({
	title: {
		type: String,
	},
	content: {
		type: String,
	}
})

</script>

<style scoped>
:deep(.el-popover.el-popper) {
	background: #252633;
	border: none;
	font-size: 14px;
	color: #B2B6C5;
	word-wrap: break-word;
	white-space: pre-wrap;
	width: 454px !important;
	border-radius: 8px;
}

:deep(.el-popper.is-light .el-popper__arrow::before) {
	border: #252633;
	background: #252633;
}

:deep(.el-popover__title) {
	padding-left: 5px;
	color: #F3B343;
	font-size: 16px;
	font-weight: bold;
}

.btnTitle {}

img {
	cursor: pointer;
	width: 21px;
}

@media (max-width:768px) {
	.btnTitle {
		width: 16px;
		height: 16px;
		font-size: 15px;
	}

	:deep(.el-popover.el-popper) {
		width: 95% !important;
		font-size: 12px;

	}


	:deep(.el-popover__title) {

		font-size: 14px;

	}

	img {
		width: 16px;
	}

}
</style>