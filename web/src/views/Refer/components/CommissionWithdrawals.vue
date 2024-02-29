<template>
    <div class="deposit" v-if="depositComShow2 == 0">
        <div class="colse_btn">
            <p>{{ t('refer.OpçõesdeSaque') }}</p>
            <img src="@assets/images/public/Shutdownx.png" alt="" @click="closePop" />
        </div>
        <div class="withdrawColumn">

            <withdrawal-information v-if="depositComShow2 == 0" />
            <div class="withdraw_mode">
                <div class="amount_box">

                    <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="inputFoucs"
                        inputType="Number" :inputRed="inputTxtRed" :data="validateForm.money" :isHead="false"
                        class="RinputHeat"
                        :popTxt="`${t('deposit.EnterWithdrawal')}${store.state.conf.all_conf.pay_conf['min_withdraw_commission']}${t('base.currency')}`">
                        <template #head>
                            <div class="country">
                                <img src="@assets/images/language/brazil.png" alt="" />
                                <span>{{ t('base.currency') }}</span>
                            </div>
                        </template>
                    </Rinput>

                </div>
            </div>
            <div class="rate txt_box">
                <div>
                    <span>{{ t('deposit.Taxa') }}： </span>
                    <span> {{ setRate }} </span>
                </div>
                <div>
                    <span>{{ t('deposit.ValoraReceber') }}： </span>
                    <span>{{ setYouwillWin }}</span>
                </div>
            </div>
            <div class="submit_btn" @click="submit">{{ t('deposit.RetirarDinheiro') }}</div>

            <!-- 设置手机号 -->
            <set-phone-number v-if="setPhoneNumberShow" />
            <p class="bottomTxt">{{ t('refer.TempodeProcessamento') }}</p>
        </div>
    </div>
    <withdrawSettings v-if="depositComShow2 == 1"></withdrawSettings>
</template>
<script lang="ts">
import {
    reactive,
    toRefs,
    getCurrentInstance,
    defineComponent,
    computed,
} from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { DepositAndWithdraw } from "@/api/DepositAndWithdraw";
import { debounce, SuccessNotiFun, getUserInfo, getUserInfoNoLoad } from "@/utils/baseFun";
import withdrawalInformation from "./withdrawalInformation.vue";
import { ElLoading, ElNotification } from 'element-plus'
import { useI18n } from "vue-i18n";
import withdrawColumnAmountInfo from "@views/deposit/components/withdrawColumnAmountInfo.vue"
import setPhoneNumber from "@views/account/components/setPhoneNumber.vue";
import withdrawSettings from "../../deposit/components/withdrawSettings.vue";
import { UserService } from "@/api/user"
import promptPopup from "@/components/promptPopup/index";
import Rinput from "./input.vue";
export default defineComponent({
    name: "CommissionWithdrawals",
    components: { withdrawalInformation, withdrawColumnAmountInfo, setPhoneNumber, withdrawSettings, Rinput },
    setup() {
        const { proxy } = getCurrentInstance() as any;
        const router = useRouter();
        const store = useStore();
        const { t } = useI18n();
        const state = reactive({
            validateForm: {
                money: '',
                name: store.state.user.username,
                cpf: store.state.user.CPF,
                pix: "CPF",
                pix_num: store.state.user.CPF,
                money_type: 0,
            },
            setPhoneNumberShow: false,
            depositComShow2: 0,
            inputFoucs: false,
            inputTxtRed: 1,
        });

        const changeInputState = (val, data) => {
            if (state.inputTxtRed == 1 && val == 'blur') {
                state.inputTxtRed = 0;
            }
            if (!data) {
                state.inputFoucs = !state.inputFoucs;
            }
        }
        const settings = () => {
            proxy.$mitt.emit("depositComShow", 1);
        };
        proxy.$mitt.on("depositComShow2", (val: number) => {
            state.depositComShow2 = val;
        });
        proxy.$mitt.on("showCom", (val: number) => {
            state.setPhoneNumberShow = false;
        });

        getUserInfoNoLoad()
        const setRate = computed(() => {
            const pay_fee =
                store.state.conf.all_conf.vip_conf[store.state.user.vip_lv].pay_fee;
            return pay_fee + "%";
        });

        const setYouwillWin = computed(() => {
            const pay_fee =
                store.state.conf.all_conf.vip_conf[store.state.user.vip_lv].pay_fee;
            let money: number | string = state.validateForm.money;
            money = (money as any) - (money as any) * (pay_fee / 100);
            return money;
        });

        const submit = () => {
            if (!store.state.user.CPF || !store.state.user.username) {
                ElNotification({
                    title: t("Warning"),
                    message: t('promptPopup.Salveasinformações'),
                    type: 'warning',
                    duration: 3000
                })

                // proxy.$mitt.emit('save');
                return
            }
            if (state.validateForm.money == "") return;
            if (!store.state.user.username && !store.state.user.CPF) {
                proxy.$mitt.emit('err');
                return
            }
            if (!store.state.user.phone) return state.setPhoneNumberShow = true

            if (state.validateForm.money < store.state.conf.all_conf.pay_conf['min_withdraw_commission']) return 
            DepositAndWithdraw.withdraw({
                money: state.validateForm.money,
                name: store.state.user.username,
                cpf: store.state.user.CPF,
                pix: "CPF",
                pix_num: store.state.user.CPF,
                money_type: 1,
            }).then(
                (res) => {

                    if (res.data.code == 1) {
                        SuccessNotiFun("SuccessfullySubmitted")
                        store.state.status.depositShow = false
                        getUserInfo();
                        closePop();
                    }

                }
            );
        };


        function closePop() {
            proxy.$mitt.emit('transfershow', false)
        }
        const inputFun = (val) => {
            if (store.state.user.commission == 0 || store.state.user.commission < val) {
                state.inputTxtRed = 0;
                promptPopup('notificationPopup', { disappear: true, text: t('promptPopup.Saldoinsuficiente'), type: 'error' })
            } else {
                if (!val) {
                    state.inputTxtRed = 1;
                }
                if (Number(val) > store.state.user.commission) {
                    (val as any) = store.state.user.commission;
                    state.inputTxtRed = 0;
                } else if (Number(val) < store.state.conf.all_conf.pay_conf['min_withdraw_commission']) {
                    state.inputTxtRed = 0;
                    (val as any) = store.state.conf.all_conf.pay_conf['min_withdraw_commission'];
                }
                else {
                    state.validateForm.money = val;
                    state.inputTxtRed = 2;
                }
            }
        }
        return {
            ...toRefs(state),
            store,
            t,
            settings,
            submit,
            setRate,
            setYouwillWin,
            closePop,
            inputFun,
            changeInputState,
        };
    },
});
</script>
<style  lang="scss" scoped>
.deposit {
    position: relative;
    padding: 30px 28px 58px 28px;
    width: 440px;
    background: #202330;
    border-radius: 12px;
    box-sizing: border-box;

    .colse_btn {
        cursor: pointer;
        // position: absolute;
        // top: 30px;
        // right: 19px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        color: #fff;
        font-weight: bold;

        img {
            width: 25px;
            position: absolute;
            right: 24px;
            top: 24px;
        }
    }

    .bottomTxt {
        font-size: 16px;
        color: #98ABD0;
        text-align: center;
    }
}

@media (max-width: 768px) {
    .deposit {
        width: 100%;
        padding: 0px 12px;
        box-sizing: border-box;

        .colse_btn {
            img {
                width: 18px;
            }

            font-size: 16px;
        }

    }
}


.withdrawColumn {
    margin-top: 24px;

    .withdraw_info {
        margin-bottom: 24px;
        padding: 15px 15px 15px 15px;
        background: var(--auxiliary-background-14);
        border-radius: 12px;


        div {
            font-size: 20px;
            color: var(--auxiliary-font-color-9);
        }

        :deep(.el_popover_style) {
            background: var(--auxiliary-background-14);
            border: none;
            border-radius: 12px;
            font-size: 20px;

            .popover_content {
                .popover_content_header {
                    margin-bottom: 12px;
                    font-size: 14px !important;
                    font-weight: bold;
                    color: var(--theme-font-color-fff);
                }

                .popover_content_txt {
                    font-size: 14px;
                    font-weight: 400;
                    color: var(--auxiliary-font-color-9);
                    // line-height: 16px;
                    text-indent: 2rem;
                }

                .popover_content_btn {
                    text-align: right;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: 500;
                    color: var(--auxiliary-font-color-27);
                }
            }

            .el-popper__arrow {
                &::before {
                    background: var(--auxiliary-background-14);
                    border: none;
                }
            }
        }
    }

    .withdraw_mode {
        margin-bottom: 0px;
        // padding: 19px 15px;
        // background: var(--auxiliary-background-14);
        border-radius: 6px;

        .red {
            color: #EB4859;
        }

        .amount_box {
            position: relative;
            // display: flex;
            align-items: center;
            margin-top: 10px;

            .country {
                // position: absolute;
                // left: 18px;
                // top: 8px;
                display: flex;
                align-items: center;

                img {
                    margin-right: 10px;
                    width: 37px;
                }

                span {
                    font-size: 14px;
                    font-weight: 500;
                    color: var(--theme-font-color-fff);
                }
            }



            .input_box_style {

                position: relative;

                :deep(.el-input__wrapper) {
                    input {
                        color: #fff;
                        padding-left: 104px !important;
                        --el-input-inner-height: 40px;
                        font-size: 14px;
                        border: #B2B6C5;

                    }



                    &::placeholder {
                        color: #B2B6C5;
                        font-size: 14px;
                    }
                }
            }
        }
    }

    .txt_box {
        display: flex;
        flex-wrap: wrap;
        flex-direction: row;

        >div {
            display: flex;
            margin-bottom: 12px;
            // width: 100%;
            margin-right: 36px;

            span:nth-child(1) {
                font-size: 14px;
                font-weight: 500;
                color: var(--auxiliary-font-color-9);
            }

            span:nth-child(2) {
                font-size: 14px;
                font-weight: 500;
                color: var(--auxiliary-font-color-7);
            }
        }
    }

    .rate {
        // margin-bottom: 5px;
        margin-top: 12PX;
    }

    .submit_btn {
        margin-bottom: 24px;
        cursor: pointer;
        // padding: 15px 0;
        width: 100%;
        height: 40px;
        background: #4181EE;
        border-radius: 30px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        display: flex;
        justify-content: center;
        align-items: center;
        color: var(--theme-font-color-fff);
    }



}

@media (max-width: 768px) {
    .popover_content_txt {
        font-size: 12 !important;
    }

    .deposit {
        padding: 32px 20px 58px 20px;

        .colse_btn {
            img {
                right: 25px;
                top: 23px;
                width: 12px;
            }
        }

        .withdrawColumn {
            margin-top: 36px;

            .withdraw_info {
                margin-bottom: 24px;
                padding: 12px 9px 12px 9px;
                background: var(--auxiliary-background-14);
                border-radius: 12px;

                .setting_btn {
                    padding-bottom: 10px;

                    span {
                        font-size: 12px;
                    }
                }
            }



            .withdraw_mode {
                margin-bottom: 12px;
                // padding: 14px 11px;



                .amount_box {
                    position: relative;
                    // display: flex;
                    // align-items: center;
                    margin-top: 16px;

                    .country {
                        img {
                            margin-right: 7px;
                            width: 28px;
                        }

                        span {
                            font-size: 14px;
                        }
                    }

                    .input_box_style {
                        :deep(.el-input__wrapper) {
                            input {
                                padding-left: 80px !important;
                                --el-input-inner-height: calc(29px);
                                color: #fff !important;

                                &::placeholder {
                                    font-size: 12px;
                                }
                            }
                        }
                    }
                }
            }

            .txt_box {
                >div {
                    margin-bottom: 0;

                    span:nth-child(1) {
                        font-size: 13px;
                    }

                    span:nth-child(2) {
                        font-size: 13px;
                    }
                }
            }

            .rate {
                margin-bottom: 16px;
            }

            .submit_btn {
                margin-bottom: 24px;
                cursor: pointer;
                height: 40px;
                border-radius: 30px;
            }


        }

        .bottomTxt {
            font-size: 12px;
        }
    }

}
</style>
