<template>
    <div class="checkIn">

        <div class="rit">
            <img src="@/assets/images/bonusCabinet/calendar.png" alt="" class="checkInImg">
            <div class="money">
                <p class="check">{{ t('base.currencySymbol') }} {{ store.state.user.sign_bonus }}</p>
                <p>{{ t('signIn.BônusAcumulado') }}</p>
            </div>

        </div>

        <!-- <div class="bouns">
            <p>{{ t('base.currencySymbol') }} {{ data.money }} <span>{{ t('bonusCabinet.BônusEntrada') }}</span></p>
            <p>{{ t('base.currencySymbol') }} {{ store.state.user.sign_bonus }} <span>{{ t('signIn.BônusAcumulado')
            }}</span></p>
        </div> -->
        <div class="rit">
            <img :src="vipImg" alt="" class="vipLvImg">
            <img src="@/assets/images/public/query.png" alt="" class="queryImg" @click="showVipPop">
            <div class="btn">
                <div class="btn2 sl_box_shadow" @click="checkIn">
                    <div v-if="store.state.vipBonusState.sgin_data.state !== 1" class="btn_mask"></div>
                    <div v-if="store.state.vipBonusState.sgin_data.state == 1" style="display: flex;">
                        <img v-if="btn_loading_checkIn" src="@assets/images/public/btn_loading.gif" alt="">
                        <p v-if="store.state.vipBonusState.sgin_data.money == 0">{{ t('btnName.checkin') }}</p>
                        <p v-else>{{ t('base.currencySymbol') }} {{ store.state.vipBonusState.sgin_data.money }}</p>
                    </div>
                    <el-countdown v-else title="" format="HH:mm:ss"
                        :value="Date.now() + (store.state.vipBonusState.sgin_data['time'] * 1000)" @finish="finish" />
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import { reactive, toRefs, computed, onBeforeUnmount } from 'vue'
import { useI18n } from "vue-i18n";
import { UserService } from '@/api/user';
import { useStore } from "@/store/index";
import promptPopup from '@/components/promptPopup';
import { ElNotification } from 'element-plus'
import { debounce, getImageUrl } from "@/utils/baseFun";
export default {
    setup() {
        const store = useStore();
        const { t } = useI18n();
        const state = reactive({
            dialogVisible: false,
            data: { state: 0, money: 0 },
            vipImg: getImageUrl(`vipBonus/level_${store.state.user.vip_lv}.png`),
            hoursTens: 0,
            hoursOnes: 0,
            minutesTens: 0,
            minutesOnes: 0,
            secondsTens: 0,
            secondsOnes: 0,
            time: null,
            btn_loading_checkIn: false,
        
        })

  
        const checkIn = () => {
            if (store.state.vipBonusState.sgin_data.money == 0) {
                ElNotification({
                    message: t('Pleaseincreaseyourviplevel'),
                    type: 'warning',
                    duration: 3000,
                    offset: 65,
                })
                return;
            }

            if (store.state.vipBonusState.sgin_data.state == 1) {
                state.btn_loading_checkIn = true
                const fun = () => {
                    UserService.receive_sign_bonus().then((res) => {
                        console.log('receive_sign_bonus', res);

                        if (res.data.code == 1) {
                            state.btn_loading_checkIn = false;
                            promptPopup('rewardPopup', { title: t('signIn.Checkindiário'), amount: res.data.money, tips: t('signIn.Obônuscontinuaaaumentarà'), btnName: t('btnName.Confirmar') })
                            store.dispatch("vipBonusState/init_sgin_data");
                        }
                    });
                }
                debounce(fun)
            }
        }

        const finish = () => {
            store.dispatch("vipBonusState/init_sgin_data");
        }

        const showVipPop = () => {
        
            store.dispatch("status/setvipCheckIn",true);
            console.log(store.state.status.vipCheckIn);
        }

        return {
            ...toRefs(state),
            checkIn,
            store,
            t,
            finish,
            showVipPop,
        }
    }
}
</script>

<style lang="scss" scoped>
.checkIn {
    width: 100%;
    height: 76px;
    background: #202431;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
    padding-left: 26px;
    padding-right: 17px;
    margin-bottom: 16px;
    border-radius: 12px;

    .vipLvImg {
        width: 50px;
        height: 50px;
    }

    .queryImg {
        width: 24px;
        height: 24px;
        cursor: pointer;
        margin-left: 4px;
    }

    .checkInImg {
        width: 52px;
        height: 52px;
    }

    .money {
        display: flex;
        align-items: center;
        gap: 7px;
        margin-left: 17px;

        p {
            color: #B2B6C5;
            font-size: 14px;
        }

        .check {
            color: #75ED3D;
            font-size: 20px;
        }
    }

    .bouns {
        display: flex;
        align-items: center;
        gap: 58px;

        p {
            font-size: 20px;
            color: #fff;

            span {
                color: #B2B6C5;
                font-size: 14px;
            }
        }
    }

    .rit {
        display: flex;
        align-items: center;
    }

    .btn {
        width: 130px;

        box-sizing: border-box;
        display: flex;
        align-items: center;
        margin-left: 38px;

        .check {
            color: #75ED3D;
        }

        :deep(.el-button) {
            border: none;
            box-shadow: none;
        }

        :deep(.el-button>span) {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            row-gap: 8px;
        }

        .no_bonus_box {
            // background-color: #222431;
            background: rgba($color: #000000, $alpha: 0);
            // padding: 10px 14px !important;
            display: flex;
            gap: 5px;
            box-sizing: border-box;
            // width: 130px;
            height: 52px;

            .btn_mask {
                display: none !important;
            }

            p {

                color: #B2B6C5 !important;
            }
        }

        .btn2 {
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: row;
            padding: 14px 9px;
            border-radius: 10px;
            position: relative;
            width: 114px;
            height: 48px;
            box-sizing: border-box;

            p {
                color: #1B1D29;
                font-size: 14px;
                font-weight: bold;
            }

            img {
                width: 16px;
                margin-right: 5px;
            }
        }

        .btn2_item_1 {
            flex-direction: column;

            .btn2_item_1_p {
                margin-top: 5px;
            }
        }

        .btn_mask {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(5, 5, 5, 0.432);
            border-radius: 8px;
        }

        .btnMask {
            position: relative;
        }

        .btnMask::after {
            content: "";
            cursor: pointer;
            background: rgba(5, 5, 5, 0.432);
            position: absolute;
            // top: -1px;
            // left: -0.5px;
            width: calc(100%);
            height: calc(100%);
            z-index: 2;
            border: 1px solid;
            // border-radius: 6px;
            // border-radius: 2px;
        }

        .Countdown {
            box-sizing: border-box;
            background-size: 100% 100%;
            font-size: 21px;
            display: flex;
            align-items: center;

            .colon {
                margin-left: 2px;
                margin-right: 2px;
            }
        }
    }

}

@media (max-width:768px) {
    .checkIn {
        padding-left: 7.5px;
        padding-right: 7.5px;
        margin-bottom: 12px;
        border-radius: 8px;
        height: 54px;

        .vipLvImg {
            width: 32px;
            height: 32px;
        }

        .queryImg {
            width: 14px;
            height: 14px;
            cursor: pointer;
            margin-left: 2px;
        }

        .checkInImg {
            width: 40px;
            height: 40px;
        }

        .money {
            flex-direction: column-reverse;
            align-items: flex-start;
            margin-left: 6px;

            p {
                font-size: 12px;
            }

            .check {
                font-size: 14px;
            }
        }

        .bouns {
            display: none;
        }

        .btn {
            width: 91px;
            margin-left: 23px;

            .no_bonus_box {
                width: 105px;
                height: 44px;
            }

            .btn2 {
                padding: 13px 6px;
                height: 40px;

                p {
                    font-size: 12px;
                }

                img {
                    width: 13px;
                    // margin-right: 2px;
                }
            }

            .sl_box_shadow_green {
                padding: 0 15px;
            }
        }

    }
}
</style>