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
            <el-form-item label="充值金额" prop="money">
                <el-input v-model="popData.money" disabled />
            </el-form-item>
            <el-form-item label="下单IP" prop="user_ip">
                <el-input v-model="popData.user_ip" disabled />
            </el-form-item>
            <el-form-item label="姓名" prop="name">
                <el-input v-model="popData.name" disabled />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
                <el-input v-model="popData.email" disabled />
            </el-form-item>
            <el-form-item label="是否首充" prop="first_pay">
                <el-input v-model="popData.first_pay" :formatter="firstFormatter" disabled />
            </el-form-item>
            <el-form-item label="电话" prop="mobile">
                <el-input v-model="popData.mobile" disabled />
            </el-form-item>
            <el-form-item label="支付名称" prop="pay_name">
                <el-input v-model="popData.pay_name" disabled />
            </el-form-item>
            <el-form-item label="下单结果" prop="err_msg">
                <el-input v-model="popData.err_msg" :autosize="{ minRows: 2, maxRows: 4 }" type="textarea"
                    placeholder="Please input" disabled />
            </el-form-item>
        </el-form>
    </div>
</template>
  
<script setup lang="ts">
import { reactive, ref, watch, computed } from "vue";
import { user_order_detail_post } from "../../../api/paymentManagement";
import { json } from "stream/consumers";

const props = defineProps({
    id: {
        default: null,
    }
});

let id = computed(() => props.id);

let popData = ref([]);
let loading = ref(false);
const popDataRef = ref<FormInstance>();


const firstFormatter = (popData) => {
    if (popData.first_pay == 0) return '否'
    else if (popData.first_pay == 1) return '新用户首充'
    else if (popData.first_pay == 2) return '老用户每日首充'

}



async function getData() {
    popData.value = [];
    loading.value = true;
    let data = null
    data = await user_order_detail_post({ id: id.value });
    console.log(data.data)
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
  