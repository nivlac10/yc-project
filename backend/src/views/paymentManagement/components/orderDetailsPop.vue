<template>
  <div>
    <el-form ref="popDataRef" :model="popData" label-width="120px" class="demo-popData" status-icon>
      <el-form-item label="UID" prop="uid">
        <el-input v-model="popData.uid" disabled />
      </el-form-item>
      <el-form-item label="昵称" prop="nickname">
        <el-input v-model="popData.nickname" disabled />
      </el-form-item>
      <el-form-item label="订单号" prop="order_number">
        <el-input v-model="popData.order_number" disabled />
      </el-form-item>
      <el-form-item label="支付订单号" prop="pay_order_number">
        <el-input v-model="popData.pay_order_number" disabled />
      </el-form-item>
      <el-form-item label="提现金额" prop="money">
        <el-input v-model="popData.money" disabled />
      </el-form-item>
      <el-form-item label="下单IP" prop="user_ip">
        <el-input v-model="popData.user_ip" disabled />
      </el-form-item>
      <el-form-item label="邮箱" prop="collection_email">
        <el-input v-model="popData.collection_email" disabled />
      </el-form-item>
      <el-form-item label="电话" prop="collection_mobile">
        <el-input v-model="popData.collection_mobile" disabled />
      </el-form-item>
      <el-form-item label="PIX" prop="pix">
        <el-input v-model="popData.pix" disabled />
      </el-form-item>
      <el-form-item label="收款账号" prop="pix_num">
        <el-input v-model="popData.pix_num" disabled />
      </el-form-item>
      <el-form-item label="用户税号(CPF)" prop="cpf">
        <el-input v-model="popData.cpf" disabled />
      </el-form-item>
      <el-form-item label="手续费" prop="rate">
        <el-input v-model="popData.rate" disabled />
      </el-form-item>
      <el-form-item label="发送金额" prop="send_money">
        <el-input v-model="popData.send_money" disabled />
      </el-form-item>
      <el-form-item label="支付名称" prop="pay_name">
        <el-input v-model="popData.pay_name" disabled />
      </el-form-item>
      <el-form-item label="支付详情" prop="err_msg">
        <el-input v-model="popData.err_msg" :autosize="{ minRows: 2, maxRows: 4 }" type="textarea"
          placeholder="Please input" disabled />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch, computed } from "vue";
import { withdraw_order_detail_post } from "../../../api/paymentManagement";

const props = defineProps({
  id: {
    default: null,
  }
});

let id = computed(() => props.id);
let popData = ref([]);
let loading = ref(false);
const popDataRef = ref<FormInstance>();






async function getData() {
  popData.value = [];
  loading.value = true;
  let data = null
  data = await withdraw_order_detail_post({ id: id.value });
  popData.value = data.data;
  popData.value['err_msg'] = JSON.stringify(popData.value['err_msg'])
  loading.value = false;
}
getData();
</script>

<style scoped>
.demo-popData {
  display: grid;
  /* grid-auto-columns: 1fr 1fr; */
  grid-template-columns: 1fr 1fr;
}
</style>
