<template>
  <div>
    <el-dialog v-model="state.isShow" :title="props.title" :draggable="true">
      <el-form ref="ruleFormRef" :model="state.ruleForm" :rules="state.rules" label-width="120px" class="demo-ruleForm"
        status-icon>
        <el-form-item :label="v['label']" :prop="v['key']" v-for="(v,i) in tableData">
          <slot name="form_item"></slot>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm()">{{submit}}</el-button>
          <el-button @click="cancel">取消</el-button>
          <!-- <el-button @click="resetForm(ruleFormRef)">Reset</el-button> -->
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, watch, computed } from "vue";

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  //弹窗 form item
  tableData:{
    default: [{}],
  },
  //提交按钮名称
  submit:{
    type: String,
    default: '确定',
  }
})
let state = reactive({
  ruleForm: {

  },
  rules: {

  },
  isShow: false,
})


const emit = defineEmits(['def'])
const submitForm = ()=>{
    emit('def',state.ruleForm)
}

for (const key in props.tableData) {
  props.tableData['key'] = key;
  state.ruleForm[key] = props[key];
  state.rules[key] = [{ required: true, message: '', trigger: 'blur' },]
}

const cancel = ()=>{
  state.isShow = false;
}
</script>

<style lang="scss" scoped></style>
