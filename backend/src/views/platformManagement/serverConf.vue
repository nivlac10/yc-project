<template>
    <div class="app-container">
        <el-card class="box-card box-card-top">
            <el-form ref="ruleFormRef" :model="state.ruleForm" :rules="state.rules" label-width="150px"
                class="demo-ruleForm" status-icon uno-padding-left-20>

                <el-tabs v-model="activeName" class="demo-tabs">
                    <el-tab-pane label="参数配置" name="1">
                        <el-form-item label="货币符号" prop="currency">
                            <el-input v-model="state.ruleForm.currency" />
                        </el-form-item>
                        <el-form-item label="游客注册" prop="tmp_user_money">
                            <el-input v-model="state.ruleForm.tmp_user_money" />
                        </el-form-item>
                        <el-form-item label="手机绑定" prop="bind_phone_money">
                            <el-input v-model="state.ruleForm.bind_phone_money" />
                        </el-form-item>
                        <el-form-item label="FB绑定" prop="facebook_user_money">
                            <el-input v-model="state.ruleForm.facebook_user_money" />
                        </el-form-item>
                        <el-form-item label="IP最大注册" prop="user_ip_max_num">
                            <el-input v-model="state.ruleForm.user_ip_max_num" />
                        </el-form-item>
                        <el-form-item label="赠送数据打码倍率" prop="gift_code_rate">
                            <el-input v-model="state.ruleForm.gift_code_rate" />
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="充值提现" name="2">
                        <el-collapse v-model="state.activeNames">
                            <el-collapse-item name="1">
                                <template #title>
                                    <div style="font-size: 24px; font-weight: 600; margin-left: 20px;">充值配置</div>
                                </template>

                                <el-form-item label="默认金额" prop="default_money">
                                    <el-input v-model="state.ruleForm.default_money" />
                                </el-form-item>
                                <el-form-item label="最小充值" prop="min_recharge_money">
                                    <el-input v-model="state.ruleForm.min_recharge_money" />
                                </el-form-item>
                                <el-form-item label="最大充值" prop="max_recharge_money">
                                    <el-input v-model="state.ruleForm.max_recharge_money" />
                                </el-form-item>
                                <el-form-item label="充值列表" prop="pay_money_list">
                                    <el-input v-model="state.ruleForm.pay_money_list" />
                                </el-form-item>
                                <el-form-item label="首充赠送比例(%)" prop="first_charge_give_rate">
                                    <el-input v-model="state.ruleForm.first_charge_give_rate" />
                                </el-form-item>
                                <el-form-item label="每日首充赠送比例(%)" prop="day_charge_give_rate">
                                    <el-input v-model="state.ruleForm.day_charge_give_rate" />
                                </el-form-item>
                            </el-collapse-item>
                            <el-collapse-item name="2">
                                <template #title>
                                    <div style="font-size: 24px; font-weight: 600; margin-left: 20px;">提现配置</div>
                                </template>

                                <el-form-item label="最小佣金提现" prop="min_withdraw_commission">
                                    <el-input v-model="state.ruleForm.min_withdraw_commission" />
                                </el-form-item>
                                <el-form-item label="最小提现" prop="min_withdraw_money">
                                    <el-input v-model="state.ruleForm.min_withdraw_money" />
                                </el-form-item>
                                <el-form-item label="最大提现" prop="max_withdraw_money">
                                    <el-input v-model="state.ruleForm.max_withdraw_money" />
                                </el-form-item>
                                <el-form-item label="账号限制" prop="account_max_num">
                                    <el-input v-model="state.ruleForm.account_max_num" />
                                </el-form-item>
                                <el-form-item label="提现费率" prop="withdraw_poundage">
                                    <el-input v-model="state.ruleForm.withdraw_poundage" />
                                </el-form-item>
                                <el-form-item label="提现审核" prop="auto_withdraw_name">
                                    <el-select v-model="state.ruleForm.auto_withdraw_flag" placeholder="审核" size="large"
                                        clearable>
                                        <el-option v-for="item in state.withdraw_flag_list" :label="item['label']"
                                            :value="item['val']" :key="item" />
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="自动提现金额" prop="auto_min_withdraw_money">
                                    <el-input v-model="state.ruleForm.auto_min_withdraw_money" />
                                </el-form-item>
                                <el-form-item label="自动提现ip数" prop="auto_min_withdraw_ip_num">
                                    <el-input v-model="state.ruleForm.auto_min_withdraw_ip_num" />
                                </el-form-item>
                                <el-form-item label="自动提现设备数" prop="auto_min_withdraw_sb_num">
                                    <el-input v-model="state.ruleForm.auto_min_withdraw_sb_num" />
                                </el-form-item>
                            </el-collapse-item>
                        </el-collapse>
                        <br />
                    </el-tab-pane>
                    <el-tab-pane label="地址配置" name="3">
                        <el-form-item label="资源域名" prop="resource_host">
                            <el-input v-model="state.ruleForm.resource_host" />
                        </el-form-item>
                        <el-form-item label="Android地址" prop="android_url">
                            <el-input v-model="state.ruleForm.android_url" />
                        </el-form-item>
                        <el-form-item label="二维码地址" prop="qrcode_url">
                            <el-input v-model="state.ruleForm.qrcode_url" />
                        </el-form-item>
                        <el-form-item label="Ios地址" prop="ios_url">
                            <el-input v-model="state.ruleForm.ios_url" />
                        </el-form-item>
                        <el-form-item label="服务条款地址" prop="service_terms_url">
                            <el-input v-model="state.ruleForm.service_terms_url" />
                        </el-form-item>
                        <el-form-item label="TG频道地址" prop="tg_channel_url">
                            <el-input v-model="state.ruleForm.tg_channel_url" />
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="短信配置" name="4">

                        <el-form-item label="短信通道" prop="sms_name">
                            <el-select v-model="state.ruleForm.sms_name" placeholder="所有分类" size="large" clearable
                                @change="changeSms">
                                <el-option v-for="item in state.sms_conf" :key="item" :label="item['name']" :value="item" />
                            </el-select>
                        </el-form-item>
                        <el-form-item :label="state.ruleForm.sms_name" prop="template_info">
                            <el-input v-model="state.ruleForm.template_info" />
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="分享配置" name="5">

                        <el-form-item label="分享链接" prop="copy_link">
                            <el-input v-model="state.ruleForm.copy_link" />
                        </el-form-item>

                        <el-form-item label="分享标题" prop="share_title">
                            <el-input v-model="state.ruleForm.share_title" />
                        </el-form-item>

                        <el-form-item label="分享详情" prop="share_detail">
                            <el-input v-model="state.ruleForm.share_detail" />
                        </el-form-item>

                        <el-form-item label="邀请邮件" prop="success_email">
                            <el-input v-model="state.ruleForm.success_email" />
                        </el-form-item>
                        <el-form-item label="联系邮箱" prop="share_contact_email">
                            <el-input v-model="state.ruleForm.share_contact_email" />
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="系统配置" name="6">

                        <el-form-item label="维护开关" prop="maintain_bool">
                            <el-switch v-model="state.ruleForm.maintain_bool" class="ml-2"
                                style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" />
                        </el-form-item>

                        <el-form-item label="维护标题" prop="maintain_title">
                            <el-input v-model="state.ruleForm.maintain_title" />
                        </el-form-item>

                        <el-form-item label="维护内容" prop="maintain_remarks">
                            <el-input v-model="state.ruleForm.maintain_remarks" :autosize="{ minRows: 2, maxRows: 4 }"
                                type="textarea" placeholder="Please input" />
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="平台配置" name="7">

                        <el-form-item label="平台小icon" prop="platform_min_icon_url">
                            <img-upload
                                :img="state.ruleForm.platform_min_icon_url ? state.ruleForm.platform_min_icon_url : ''"
                                @getImgData="get_platform_min_url" />
                        </el-form-item>

                        <el-form-item label="平台图标" prop="platform_title_icon_url">
                            <img-upload
                                :img="state.ruleForm.platform_title_icon_url ? state.ruleForm.platform_title_icon_url : ''"
                                @getImgData="get_platform_title_url" />
                        </el-form-item>

                        <el-form-item label="liveChat适配id" prop="platform_livechat_id">
                            <el-input v-model="state.ruleForm.platform_livechat_id" placeholder="请输入liveChat适配id" />
                        </el-form-item>
                        <el-form-item label="TG机器人播报群组id" prop="platform_telegram_chat_id">
                            <el-input v-model="state.ruleForm.platform_telegram_chat_id" placeholder="请输入TG机器人播报群组id" />
                        </el-form-item>
                        <el-form-item label="TG机器人token" prop="platform_telegram_bot_token">
                            <el-input v-model="state.ruleForm.platform_telegram_bot_token" placeholder="请输入TG机器人token" />
                        </el-form-item>
                        <el-form-item label="平台标题" prop="platform_title">
                            <el-input v-model="state.ruleForm.platform_title" placeholder="请输入平台标题" />
                        </el-form-item>
                        <el-form-item label="平台地址" prop="platform_path">
                            <el-input v-model="state.ruleForm.platform_path" placeholder="请输入平台地址" />
                        </el-form-item>
                        <el-form-item label="平台域名" prop="platform_url">
                            <el-input v-model="state.ruleForm.platform_url" placeholder="请输入平台域名" />
                        </el-form-item>
                    </el-tab-pane>
                </el-tabs>

                <el-form-item>
                    <el-button type="primary" @click="submitForm(ruleFormRef)">立即更新</el-button>
                    <el-button @click="updateRedis">刷新Redis</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>





<script lang="ts" setup >
import { reactive, ref, watch, computed, onMounted } from "vue";
import { useRouter } from "vue-router"
import type { FormInstance } from 'element-plus'
import { ElMessage } from "element-plus"
import type { TabsPaneContext } from 'element-plus'
import { system_conf, system_conf_list_post, system_conf_post, update_redis_conf_post } from '@/api/platformManagement'
import imgUpload from "@/components/imgUpload/index.vue"

const router = useRouter();
const state = reactive({
    loading: false, // table loading
    operationType: 'add', // add || edit
    dialogFormVisible: true,
    tableData: [],
    ruleForm: {
        name: '',
        currency: '',//货币符号  
        tmp_user_money: '',
        bind_phone_money: '',
        facebook_user_money: '',
        user_ip_max_num: '',
        gift_code_rate: '',
        default_money: '',
        min_recharge_money: '',
        max_recharge_money: '',
        pay_money_list: '',
        first_charge_give_rate: '',
        day_charge_give_rate: '',
        min_withdraw_commission: '',
        min_withdraw_money: '',
        max_withdraw_money: '',
        account_max_num: '',
        withdraw_poundage: '',
        auto_withdraw_flag: '',
        auto_withdraw_name: '',
        auto_min_withdraw_money: '',
        auto_min_withdraw_ip_num: '',
        auto_min_withdraw_sb_num: '',
        resource_host: '',
        android_url: '',
        qrcode_url: '',
        ios_url: '',
        service_terms_url: '',
        tg_channel_url: '',
        sms_conf: '',
        sms_name: '',
        copy_link: '',
        share_title: '',
        share_detail: '',
        success_email: '',
        share_contact_email: '',
        is_maintain: '',
        maintain_bool: false,
        maintain_title: '',
        maintain_remarks: '',
        code_template: '',
        template_info: '',
        platform_min_icon_url: '',
        platform_title_icon_url: '',
        platform_path: '',
        platform_url: '',
        platform_title: '',
        platform_livechat_id: '',
        platform_telegram_chat_id: '',
        platform_telegram_bot_token: ''
    },
    rules: {
        name: [{ required: true, message: '', trigger: 'blur' },],
    },
    sms_conf: [],
    withdraw_flag_list: [{ label: '人工审核', val: 0 }, { label: '自动', val: 1 }],
    activeNames: ['1']
})
const ruleFormRef = ref<FormInstance>()
const activeName = ref('1')

// 获取选择数据
const getSelectData = () => {
    // 渠道
    system_conf({}).then((res: any) => {
        state.sms_conf = res['sms_conf']
    })
}

// 获取数据
const getData = async () => {
    state.loading = true
    system_conf_list_post({}).then(res => {
        console.log(res['data'])
        state.ruleForm = res['data']
        state.ruleForm.template_info = state.ruleForm.code_template[state.ruleForm.sms_conf]
        state.ruleForm.sms_name = state.sms_conf[state.ruleForm.sms_conf]['name']
        state.ruleForm.maintain_bool = state.ruleForm.is_maintain == '1' ? true : false
    })
    state.loading = false
    console.log(state.ruleForm);

}


onMounted(() => {

    getSelectData()// 获取选择数据
    getData();// 获取数据
})

// 获取图片数据
const get_platform_min_url = (val: string) => {
    state.ruleForm.platform_min_icon_url = val
    console.log(state.ruleForm.platform_min_icon_url)
}
const get_platform_title_url = (val: string) => {
    state.ruleForm.platform_title_icon_url = val
}


// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            state.ruleForm.code_template[state.ruleForm.sms_conf] = state.ruleForm.template_info
            state.ruleForm.code_template = JSON.stringify(state.ruleForm.code_template)
            if (state.ruleForm.maintain_bool == true || state.ruleForm.maintain_bool == false) {
                state.ruleForm.is_maintain = state.ruleForm.maintain_bool == true ? '1' : '0'
            }
            let data = new FormData();
            for (var i in state.ruleForm) {
                data.append(i, state.ruleForm[i]);
            }
            system_conf_post(data).then(res => {
                if (res['code'] == 1) getData()
            })
        } else {
            console.log('error submit!', fields)
        }
    })
}


// 更新redis
const updateRedis = () => {
    update_redis_conf_post({}).then(res => {
        if (res['code'] == 1) handleRedis()
    })
}



const changeSms = (val) => {
    for (let key in state.sms_conf) {
        if (state.sms_conf[key]["name"] == val.name) {
            state.ruleForm.sms_conf = key
            state.ruleForm.sms_name = val.name
            return;
        }
    }
}
const handleRedis = () => {
    ElMessage.success(`Redis刷新成功！`)
}

// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}

</script>

<style lang="scss" scoped></style>

