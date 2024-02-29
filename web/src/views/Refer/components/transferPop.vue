<template>
    <div class="withdrawSettings">
        <div class="withdrawSettings_header">

            <div class="title">{{ t('refer.TRANSFERTOHEACCOUNTBALANCE') }}</div>
            <img src="@assets/images/public/popover_error_icon.png" alt="" @click="settings" />
        </div>
        <div>

            <div class="money settings_item">
                <p>{{ t('refer.COMMISSIONS') }}</p>
                <p style="color: #75ED3D;">{{ store.state.user.commission }} {{ t('base.currency') }}</p>
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


            <div class="serBtn" @click="clickTransfer">
                {{ t('refer.TRANSFER') }}
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
} from "vue";
import { useRouter } from "vue-router";
import type { FormInstance, FormRules } from "element-plus";
import { useStore } from "@/store/index";
import { UserService } from "@/api/user";
import { debounce, getUserInfo } from "@/utils/baseFun";

import { useI18n } from "vue-i18n";
export default defineComponent({
    name: "pop ",
    setup() {
        const router = useRouter();
        const store = useStore();
        // i18n 配置
        const { t } = useI18n();
        const { proxy } = getCurrentInstance() as any;
        const state = reactive({
            validateForm: {
                type: "",
                Name: "",
                CPF: "",
                PIX: "",

            },
            ispix: false,
            btnIndex: 0,
            num: 100,
        });



        const formRef = ref<FormInstance>();
        const rules = reactive<FormRules>({
            type: [{ required: true, trigger: "blur" }],
            Name: [{ required: true, trigger: "blur" }],
            CPF: [{ required: true, trigger: "blur" }],
            PIX: [{ required: true, trigger: "blur" }],
        });

        const submitForm = async (formEl: FormInstance | undefined) => {
            if (!formEl) return;
            await formEl.validate((valid, fields) => {
                if (valid) {
                } else {
                }
            });
        };

        function showIspix(data) {
            state.ispix = data;
        }

        const settings = () => {
            proxy.$mitt.emit("transfershow", false);
        };

        function btnClick(index: number, num: number) {
            state.btnIndex = index;
            state.num = num;

        }

        function clickTransfer() {
            debounce(transfer, 1000)
        }
        async function transfer() {
            let res = await UserService.user_transfer_commission({ money: state.num });
            if (res.data.code == 1) { 
                getUserInfo();
            }

        }
        return { ...toRefs(state), store, rules, formRef, submitForm, showIspix, settings, btnClick, clickTransfer, t };
    },
});
</script>
<style  lang="scss" scoped>
.withdrawSettings {
    padding: 30px 27px;
    box-sizing: border-box;
    width: 532px;
    border-radius: 12px;
    background: var(--theme-box-background);

    .withdrawSettings_header {
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;

        img:nth-child(1) {
            cursor: pointer;
            width: 51px;
        }

        .title {
            font-size: 21px;
            font-weight: bold;
            color: #FBD31E;

        }

        img:nth-last-child(1) {
            cursor: pointer;
            width: 25px;
        }
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
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .money {
        margin-top: 33px;
        margin-bottom: 24px;

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
            color: var(--auxiliary-font-color-9);
            background: #313441;
        }

        .hover {
            background: #E8134B;
            color: #fff;

        }
    }



    .serBtn {
        background: #E8134B;
        width: 100%;
        height: 54px;
        margin-top: 30px;
        margin-bottom: 29px;
        border-radius: 14px;
        font-size: 24px;
        font-weight: 600;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #fff;
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
                font-size: 13px !important;

            }

            img:nth-last-child(1) {
                width: 18px;
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

        .money {
            margin-top: 18px;
            margin-bottom: 14px;

            p {
                font-size: 10px !important;
            }
        }

        .btns {
            column-gap: 15px;
            height: 37.25px;
            margin-bottom: 17px;

            div {
                height: 37.25px;

                border-radius: 8px;
            }

            .btn {
                font-size: 12.42px;
            }
        }


        .serBtn {
            height: 31px;
            font-size: 14px;
            border-radius: 6.5px;
            margin-top: 0;
            margin-bottom: 17px;
        }
    }
}
</style>
     