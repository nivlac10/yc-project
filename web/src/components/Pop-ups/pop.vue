<template>
    <div class="withdrawSettings">
        <div class="withdrawSettings_header">
            <img src="@assets/images/public/popover_return.png" alt="" @click="showIspix(false)" v-show="ispix" />
            <div class="title">{{ t('refer.WITHDRAWAL') }} <span v-show="ispix">{{ t('refer.SETTINGSL') }}</span> <span
                    v-show="!ispix">
                    {{ t('refer.OPTIONS') }} </span></div>
            <img src="@assets/images/public/popover_error_icon.png" alt="" @click="settings" />
        </div>
        <div v-if="ispix">
            <div class="form_title">{{ t('refer.TypeofPIX') }}</div>
            <el-form class="el-form_style" ref="formRef" :model="validateForm" :rules="rules">
                <el-form-item label="" prop="pix">
                    <div class="input_box">
                        <el-select v-model="validateForm.pix" placeholder="Please select your type.">
                            <el-option v-for="(item, index) in typeList" :key="index" :label="item" :value="item" />
                        </el-select>
                    </div>
                </el-form-item>
                <el-form-item label="" prop="name">
                    <div class="input_box">
                        <el-input v-model="validateForm.name" placeholder="Name" type="text" autocomplete="off" />
                    </div>
                </el-form-item>
                <el-form-item label="" prop="cpf">
                    <div class="input_box">
                        <el-input v-model="validateForm.cpf" placeholder="CPF" type="text" autocomplete="off" />
                    </div>
                </el-form-item>
                <!-- <el-form-item label="" prop="pix_num">
                    <div class="input_box">
                        <el-input v-model="validateForm.pix_num" placeholder="PIX" type="text" autocomplete="off" />
                    </div>
                </el-form-item> -->
            </el-form>
            <div class="submit_btn" @click="submitForm(formRef)"> {{ t('refer.SETTINGSL') }}</div>
            <div class="bottom">
                <p>{{ t('refer.Pixsettings') }}</p>
                <p>{{ t('refer.Thefirstwithdrawal') }}</p>
                <p>{{ t('refer.whichcanbechangedlater') }}</p>
            </div>
        </div>
        <div v-else>
            <div class="settings">
                <div class="settings_title settings_item">
                    <p>{{ t('refer.TYPEOFPIX2') }}</p>
                    <p @click="showIspix(true)">{{ t('refer.SETTINGSL') }} ></p>
                </div>
                <div class="settings_item">
                    <div class="settings_item_text">
                        <p class="text_hiding">{{ t('refer.TYPE') }}: <span>{{ validateForm.pix }}</span></p>
                        <p class="text_hiding">{{ t('refer.NAME') }}: <span>{{ validateForm.name }}</span></p>
                    </div>
                    <div class="settings_item_text">
                        <p class="text_hiding">{{ t('refer.CPF') }}: <span>{{ validateForm.cpf }}</span></p>
                        <!-- <p>{{ t('refer.PIX') }}: <span class="text_hiding">{{ validateForm.pix_num }}</span></p> -->
                    </div>
                </div>
            </div>
            <div class="money settings_item">
                <p>{{ t('refer.COMMISSIONS') }}</p>
                <p>{{ store.state.user.money }} {{ t('base.currency') }}</p>
            </div>
            <div class="btns">
                <div :class="`btn ${btnIndex == 0 ? 'hover' : ''}`" @click="btnClick(0, 50)">
                    {{ t('base.currency') }} 50
                </div>
                <div :class="`btn ${btnIndex == 1 ? 'hover' : ''}`" @click="btnClick(1, 500)">
                    {{ t('base.currency') }} 500
                </div>
                <div :class="`btn ${btnIndex == 2 ? 'hover' : ''}`" @click="btnClick(2, 1000)">
                    {{ t('base.currency') }} 1000
                </div>
            </div>

            <div class="input_box" style="margin: 10px 0;">
                <el-input v-model="num" :placeholder="t('pay.Pleaseentertheamount')" type="number" autocomplete="off"
                    @input="setMoney" />
            </div>

            <div class="rate">
                <div>
                    <p>{{ t('refer.Rate') }}: <span> {{ rate }}%</span></p>
                </div>
                <div>
                    <p>{{ t('refer.Yauwillwin') }}: <span> {{ winMoney }}</span></p>
                </div>
            </div>

            <div class="serBtn" @click="settingsl">
                {{ t('refer.SETTINGSL') }}
            </div>
            <div class="rules_info">
                <div class="title">{{ t('refer.Withdrawalinstructions') }}</div>
                <p>{{ t('refer.morewithdrawableamount') }}</p>
                <p>
                    {{ t('refer.Whenyobetd') }}
                </p>
                <p>
                    {{ t('refer.Whenyoucompleteyourwithdrawal') }}
                </p>
                <p>{{ t('refer.Paymmenttimefrom5minutesto24hours') }}</p>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import {
    reactive,
    toRefs,
    getCurrentInstance,
    defineComponent,
    ref,
    computed,
    watch
} from "vue";
import { useRouter } from "vue-router";
import { ElLoading, FormInstance, FormRules } from "element-plus";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { DepositAndWithdraw } from "@/api/DepositAndWithdraw";
import { SuccessNotiFun, debounce, getUserInfo } from "@/utils/baseFun";
export default defineComponent({
    name: "pop ",
    setup() {
        const router = useRouter();
        const store = useStore();
        // i18n 配置
        const { t } = useI18n();
        const { proxy } = getCurrentInstance() as any;
        const state = reactive({
            // typeList: ["EMAIL", "PHONE", "CPF"],
            typeList: ["CPF"],
            validateForm: {
                name: store.state.user.username,
                cpf: store.state.user.CPF,
                pix: "CPF",
                pix_num: store.state.user.CPF,
            },
            ispix: false,
            btnIndex: 0,
            num: 50,
            rate: (store.state.conf.all_conf.vip_conf[store.state.user.vip_lv].pay_fee),
            winMoney: 0,
        });


        const settings = () => {
            proxy.$mitt.emit("tabShow", false);
        };

        const formRef = ref<FormInstance>();
        const rules = reactive<FormRules>({
            name: [{ required: true, trigger: "blur" }],
            cpf: [{ required: true, trigger: "blur" }],
            pix: [{ required: true, trigger: "blur" }],
            pix_num: [{ required: true, trigger: "blur" }],
        });

        const submitForm = async (formEl: FormInstance | undefined) => {
            if (!formEl) return;
            await formEl.validate((valid, fields) => {
                if (valid) {

                    store.dispatch('saveUserData/setWithdrawalSettings', state.validateForm);
                    showIspix(false)
                } else {
                    console.log("error submit!", fields);
                }
            });
        };

        function showIspix(data) {
            state.ispix = data;
        }


        function btnClick(index: number, num: number) {
            state.btnIndex = index;
            state.num = num;
            setMoney();

        }

        function setMoney() {
            state.winMoney = state.num - state.num * (state.rate / 100);
        }
        setMoney();
        function settingsl() {

            if (!store.state.user.username || !store.state.user.CPF) return settings();

            debounce(async () => {
                let loading = ElLoading.service({
                    lock: true,
                    text: 'Loading',
                    background: 'rgba(0, 0, 0, 0.7)',
                })
                let res = await DepositAndWithdraw.withdraw({
                    money: state.num,
                    name: store.state.user.username,
                    cpf: store.state.user.CPF,
                    pix: "CPF",
                    pix_num: store.state.user.CPF,
                    money_type: 1,
                })

                loading.close()
                if (res.data.code == 1) {
                    SuccessNotiFun("SuccessfullySubmitted")
                    state.ispix = false
                    getUserInfo()
                }

            });
        }
        return { ...toRefs(state), store, settings, rules, formRef, submitForm, showIspix, t, btnClick, settingsl, setMoney };
    },
});
</script>
<style  lang="scss" scoped>
.withdrawSettings {
    padding: 30px 27px;
    box-sizing: border-box;
    width: 512px;
    border-radius: 24px;
    background: var(--theme-box-background);

    .withdrawSettings_header {
        margin-bottom: 32px;
        display: flex;
        justify-content: space-between;
        align-items: center;

        img:nth-child(1) {
            cursor: pointer;
            width: 51px;
        }

        .title {
            font-size: 24px;
            font-weight: bold;
            color: #FBD31E;

            span {
                font-size: 24px;
                font-weight: bold;
            }
        }

        img:nth-last-child(1) {
            cursor: pointer;
            width: 25px;
        }
    }

    .form_title {
        margin-bottom: 15px;
        font-size: 18px;
        font-weight: bold;
        color: var(--auxiliary-font-color-9);
    }

    .el-form_style {
        .input_box {
            height: 40px;
        }
    }

    .submit_btn {
        cursor: pointer;
        padding: 15px 0;
        background: #855AF6;
        border-radius: 12px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: var(--theme-font-color-fff);
    }

    .bottom {
        margin-top: 35px;
        margin-bottom: 130px;

        p {
            color: var(--auxiliary-font-color-9);
            font-size: 14px;
            line-height: 16px;
        }

    }

    .bottom>p:first-child {
        font-size: 18px;
        font-family: 600;
        margin-bottom: 9px;
    }

    .settings_item {
        display: grid;
        grid-template-columns: 1fr 1fr;
        // align-items: center;
        justify-content: space-between;
        overflow: hidden;
    }

    .settings {
        height: 125px;
        width: calc(100% - 36px);
        padding: 19px 18px 21px 18px;
        background: #313441;
        border-radius: 14px;


        .settings_title {
            align-items: center;
        }

        .settings_title>p:nth-child(1) {
            font-size: 22px;
            color: #F59922;
            font-weight: bold;
        }

        .settings_title>p:nth-child(2) {
            cursor: pointer;
            color: #5663E9;
            font-weight: bold;
            font-size: 16px;
        }

        .settings_item_text:first-child {
            margin-top: 21px;
        }

        .settings_item_text:last-child {
            margin-top: 21px;
            padding-right: 160px;
        }

        .settings_item_text {
            color: var(--auxiliary-font-color-9);
            font-size: 18px;

            p {
                margin-bottom: 12px;
                display: flex;
                overflow: hidden;
            }

            span {
                color: #75ED3D;
                font-weight: 600;
            }
        }
    }

    .money {
        margin-top: 24px;
        margin-bottom: 12px;

        p {
            color: var(--auxiliary-font-color-9);
            font-size: 18px;
            font-weight: bold;
        }

    }

    .btns {

        display: grid;
        grid-template-columns: repeat(3, 1fr);
        column-gap: 26px;
        width: 100%;
        height: 66px;

        div {
            height: 66px;
            border-radius: 14px;
            font-size: 22px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .btn {
            cursor: pointer;
            color: var(--auxiliary-font-color-9);
            background: #313441;
        }

        .hover {
            background: #855AF6;
            color: #fff;

        }
    }

    .rate {
        // width: calc(100% - 225px);
        // margin-right: 225px;
        display: flex;
        align-items: center;

        div {
            font-size: 18px;
            margin-top: 28px;
            margin-bottom: 18px;
            margin-right: 20px;

            p {
                color: var(--auxiliary-font-color-9);
                font-weight: 600;

                span {
                    color: #75ED3D;
                    font-weight: 600;
                }
            }

        }
    }

    .serBtn {
        cursor: pointer;
        background: #855AF6;
        width: 100%;
        height: 54px;
        margin-top: 14px;
        margin-bottom: 29px;
        border-radius: 14px;
        font-size: 24px;
        font-weight: 600;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #fff;
    }

    .rules_info {
        .title {
            margin-bottom: 10px;
            font-size: 20px;
            font-weight: bold;
            color: var(--auxiliary-font-color-9);
        }

        p {
            margin-bottom: 5px;
            line-height: 21px;
            font-weight: 500;
            font-size: 14px;
            color: var(--auxiliary-font-color-9);
        }
    }
}

@media (max-width: 768px) {
    .withdrawSettings {
        width: calc(100% - 30px);
        padding: 22px 15px 17px 15px;
        margin-left: 15px;

        // margin-left: 42px;
        .withdrawSettings_header {
            img:nth-child(1) {
                width: 38px;
            }

            .title {
                font-size: 14px !important;

                span {
                    font-size: 14px !important;
                }
            }

            img:nth-last-child(1) {
                width: 18px;
            }
        }

        .form_title {
            font-size: 14px;
        }

        .el-form_style {
            .el-form-item {
                margin-bottom: 0px;
            }

            .input_box {
                :deep(.el-input) {
                    height: 30px;

                    .el-input__wrapper {
                        .el-input__inner {
                            --el-input-inner-height: calc(30px);

                            &::placeholder {
                                font-size: 12px !important;
                            }
                        }
                    }
                }
            }
        }

        .submit_btn {
            padding: 8px 0;
            border-radius: 8px;
            font-size: 14px;
        }

        .rules_info {
            .title {
                font-size: 12px;
            }

            p {
                font-size: 8px;
                line-height: 12px;
            }
        }

        .bottom {
            margin-top: 20px;
            margin-bottom: 61px;

            p {
                font-size: 8px !important;
            }

            .bottom>p:first {
                font-size: 10px !important;
            }
        }

        .settings {
            height: 76.2px;
            padding: 10px 14px 12px 14px;

            .settings_title>p:nth-child(1) {
                font-size: 12px;
            }

            .settings_title>p:nth-child(2) {
                font-size: 9px;
            }

            .settings_item_text {
                font-size: 10px;


                p {
                    margin-bottom: 12px;

                }
            }

            .settings_item_text:last-child {
                padding-right: 76px;
            }


        }

        .money {
            p {
                font-size: 10px !important;
            }
        }

        .btns {
            column-gap: 15px;
            // height: 37.25px;

            div {
                height: 37.25px;
                margin-top: 16px;
                margin-bottom: 11px;
                border-radius: 8px;
            }

            .btn {
                font-size: 12.42px;
            }
        }

        .rate {
            width: calc(100% - 100px);
            margin-right: 100px;

            div {
                font-size: 10px;

            }
        }

        .serBtn {
            height: 30px;
            font-size: 14px;
            border-radius: 6.5px;
            margin-top: 0;
            margin-bottom: 17px;
        }
    }
}
</style>
     