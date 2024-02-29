<template>
	<el-card uno-margin-top>
		<div class="pager-wrapper">
			<el-pagination v-model:current-page="props.pageForm['page']" v-model:page-size="props.pageForm['limit']"
				:page-sizes="[20, 25, 50, 100]" :small="false" :disabled="false" :background="true"
				layout="total, sizes, prev, pager, next, jumper" :total="props.pageForm['total']" @size-change="handleSizeChange"
				@current-change="handleCurrentChange" />
		</div>
	</el-card>
</template>
<script>
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
export default defineComponent({
	name: "index",
	props: {
		pageForm: {
			type: Object
		}
	},
	setup(props, { emit }) {
		const state = reactive({
			currentPage: 5,
			pageSize: 100,
			total: 400
		});
		const handleSizeChange = (val) => { 
			props.pageForm.limit = val
			emit("def")
		}
		const handleCurrentChange = (val) => {
			props.pageForm.page = val
			emit("def")
		}
		return { ...toRefs(state), handleSizeChange, handleCurrentChange, props };

	},
});
</script>
<style  lang="scss" scoped>
.index {}
</style>
  