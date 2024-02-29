<template>
    <div>
        <el-dialog v-model="store.state.status.isBônusdepósito" :show-close="false" :close-on-click-modal="false"
            destroy-on-close :close-on-press-escape="false">
            <div class="bounsPop">
                <div class="helpPop_head">
                    {{ t('bounsPop.BônusDepósitoAcumulado') }}
                    <img src="@/assets/images/public/Shutdown.png" alt="" class="helpPop_head_close" @click="closePop">
                </div>
                <div class="body">
                    <div class="item" v-for="v in state.data.bonus_list">
                        <div class="left">
                            <p> {{ t('bounsPop.Depositaaté', { money: v.recharge_money | 0, money2: v.bonus }) }}</p>
                            <div class="progress">
                                <div class="bg" :style="`width:${v.rate}% `">
                                </div>
                                <p> {{ `${state.data.money}/${v.recharge_money | 0}` }}</p>
                            </div>
                        </div>
                        <div class="rit">
                            <div v-if="v.state == 0" class="btn state0">
                                {{ t('bounsPop.Prosseguir') }}
                            </div>
                            <div v-if="v.state == 1" class="btn state1" @click="getBouns(v)">
                                {{ t('bounsPop.Prosseguir') }}
                            </div>
                            <div v-if="v.state == 2" class="btn state0">
                                {{ t('bounsPop.Recebido') }}
                            </div>
                            <div class="money">
                                <img src="@/assets/images/public/R$.png" alt="">
                                {{ v.bonus | 0 }},00
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bottom">
                    <div class="checkbox">
                        <div class="box" @click="isCheack = !isCheack">
                            <img src="@/assets/images/public/Sign_in_successfully.png" alt="" v-if="isCheack">
                        </div>
                        <p> {{ t('bounsPop.Nãoovamentenestasessão') }}</p>
                    </div>
                    <div class="btn" @click="noShow">{{ t('bounsPop.Promoção') }}</div>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script setup>
import { reactive, toRefs, ref } from "vue";
import { useStore } from "@/store/index";
import { achievementsBouns } from "@/api/achievementsBouns";
import { debounce } from "@/utils/baseFun";
import promptPopup from "@/components/promptPopup/index";
import { useI18n } from "vue-i18n";
const { t } = useI18n();
const store = useStore();

let dialogVisible = ref(true);

let isCheack = ref(false)
isCheack.value = store.state.status.noBônusdepósito;
const state = reactive({
    data: {
        bonus_list: [1, 2, 3, 4, 5, 6, 7]
    }
});

const get_data = async () => {
    let data = await achievementsBouns.get_recharge_achieve_state();
    state.data = data.data;
    let money = data.data.money
    for (let i = 0; i < data.data.bonus_list.length; i++) {
        data.data.bonus_list[i].rate = money / (data.data.bonus_list[i].recharge_money / 100)
        if (data.data.bonus_list[i].rate > 100) data.data.bonus_list[i].rate = 100
        console.log(data.data.bonus_list[i].rate);
    }
}
get_data();

const getBouns = (v) => {
    const func = async () => {
        let data = await achievementsBouns.receive_recharge_achieve_bonus({ id: v.id });
        if (data.data.code == 1) {
            promptPopup('rewardPopup', { title: t('promptPopup.title_VOCÊVENCEU'), amount: data.data.money, tips: t('promptPopup.tips_Obônusjá'), btnName: t('btnName.Confirmar') })
            get_data()
        }
    }
    if (v.state = 1) {
        debounce(func)
    }

}

// const btnCLick = (v) => {
//     if (v.state == 1) {
//         debounce(getBouns(v.id));
//     }
// }

const closePop = () => {
    store.dispatch("status/setisBônusdepósito", false)
}
const noShow = () => {
    // store.commit()
    store.dispatch("status/setnoBônusdepósito", isCheack.value);
    closePop();
    console.log(store.state.status.noBônusdepósito);
}

</script>

<style lang="scss" scoped>
.bounsPop {
    width: 650px;
    height: 675px;
    background: #202431;
    border-radius: 8px;
    box-sizing: border-box;
    padding: 24px 0 36px 0;

    @media (max-width:758px) {
        width: 100%;
        height: 443px;
    }

    .helpPop_head {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        color: #fff;
        position: relative;

        .helpPop_head_close {
            position: absolute;
            right: 16px;
            width: 20px;
        }

        @media (max-width:758px) {
            font-size: 14px;

            .helpPop_head_close {
                width: 18px;
            }
        }

    }

    .body {
        width: calc(100% - 6px);
        height: 494px;
        font-size: 14px;
        overflow-x: auto;
        margin-top: 25px;
        padding: 0 9px 0 18px;
        box-sizing: border-box;



        .item {
            width: 100%;
            height: 82px;
            background: #2F3445;
            border-radius: 8px;
            display: grid;
            grid-template-columns: 83% 17%;
            margin-bottom: 15px;
            box-sizing: border-box;

            .left {
                display: flex;
                flex-direction: column;
                color: #fff;
                font-size: 16px;
                box-sizing: border-box;
                padding-top: 18px;
                padding-left: 17px;
                justify-content: space-between;
                padding-bottom: 2px;

                p {
                    line-height: 20px;
                }

                .progress {
                    margin-top: 3px;
                    width: 307px;
                    height: 16px;
                    border-radius: 8px;
                    background: #21222B;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 14px;
                    color: #fff;
                    position: relative;

                    p {
                        position: relative;
                        z-index: 2;
                    }

                    .bg {
                        position: absolute;
                        z-index: 1;
                        top: 0;
                        left: 0;
                        width: 10%;
                        height: 100%;
                        border-radius: 8px;
                        background: linear-gradient(90deg, #FDE672 0%, #FFC01E 100%);
                    }
                }
            }

            .rit {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: flex-end;
                box-sizing: border-box;
                padding-right: 12px;

                .btn {
                    width: 92px;
                    height: 32px;
                    color: #000;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    border-radius: 6px;
                    margin-bottom: 8px;
                    cursor: pointer;
                }

                .state0 {
                    background: #707070;
                }

                .state1 {
                    background: #F6C722;
                }

                .money {
                    display: flex;

                    font-size: 20px;
                    color: #FFAA09;
                    // width: 100%;


                    img {
                        width: 20px;
                        height: 20px;
                        margin-right: 6px;
                    }
                }
            }
        }

        @media (max-width:758px) {
            height: 283px;
            padding-left: 16px;

            .item {
                grid-template-columns: 73% 27%;

                .left {
                    padding-left: 9px;

                    p {
                        font-size: 12px;
                    }

                    div {
                        width: 148px;
                        height: 12px;
                        font-size: 12px;
                    }

                    .progress {
                        width: 100% !important;
                    }
                }

                .rit {
                    padding-right: 7px;

                    .btn {
                        width: 72px;
                        height: 24px;
                        font-size: 12px;
                    }

                    .money {
                        img {
                            width: 15px;
                            height: 15px;
                        }

                        align-items: center;
                        font-size: 12px;
                    }
                }
            }
        }

    }

    .body::-webkit-scrollbar {
        display: block;
        width: 4px;
        background: rgb(0 0 0 / 0%);
        margin-right: -18px;
    }

    .body::-webkit-scrollbar-thumb {
        background: #707070;
        width: 4px;
        height: 111px;
        // display: block;
    }

    .bottom {
        margin-top: 35px;
        width: 100%;
        padding: 0 9px 0 18px;
        box-sizing: border-box;
        display: flex;
        justify-content: space-between;

        .checkbox {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 280px;

            .box {
                width: 27px;
                height: 22px;
                background: #373E56;
                display: flex;
                justify-content: center;
                align-items: center;
                margin-right: 12px;
                box-sizing: border-box;
                position: relative;
                cursor: pointer;

                img {
                    width: 28px;
                    height: 28px;
                    position: absolute;
                    left: 3px;
                    bottom: 2px;
                }
            }

            p {
                color: #B2B6C5;
                font-size: 16px;
            }
        }

        .btn {
            background: #04BE02;
            color: #fff;
            height: 32px;
            border-radius: 6px;
            cursor: pointer;
            width: 92px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        @media (max-width: 768px) {

            .checkbox {
                width: 50%;

                p {
                    font-size: 12px;
                }

                .box {
                    width: 22px;
                    height: 17px;

                    img {
                        width: 18px;
                        height: 18px;
                        left: 1px;
                    }
                }

            }

            .btn {
                width: 72px;
                height: 24px;
                font-size: 12px;
                border-radius: 4px;
            }

        }
    }
}

@media (max-width: 768px) {
    :deep(.el-dialog) {
        width: 92%;
    }
}
</style>