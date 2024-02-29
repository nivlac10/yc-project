<template>
	<el-popconfirm :title="props.title" @confirm="confirm">
		<template #reference>
			<el-button type="danger">{{ props.buttonName }}</el-button>
		</template>
	</el-popconfirm>
</template>

<script lang="ts" setup >
import { reactive, ref, watch, computed } from "vue";
import { useRouter } from "vue-router"

const props = defineProps({
	title: {
		type: String,
		default: '您确定要删除吗？'
	},
	buttonName: {
		type: String,
		default: '删除'
	}
})
const emit = defineEmits(["confirmClick"])
const router = useRouter();
const state = reactive({

})

const confirm = () => {
	emit('confirmClick')
}
</script>

<style lang="scss" scoped></style>

