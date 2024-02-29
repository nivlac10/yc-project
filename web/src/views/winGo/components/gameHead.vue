<template>
    <div class="head">
        <div class="item">
            <div class="active">
                {{ publicData.money }}
                <p>Win Go</p>
                <p>1Min</p>
                <div class="item_time">
                    <el-countdown  :value="time1" /> 
                </div>
            </div>
            <div>
                <p>Win Go</p>
                <p>1Min</p>
                <div class="item_time">
                    <el-countdown  :value="60" /> 
                </div>
            </div>
            <div>
                <p>Win Go</p>
                <p>1Min</p>
                <div class="item_time">
                    <el-countdown  :value="60" /> 
                </div>
            </div>
            <div>
                <p>Win Go</p>
                <p>1Min</p>
                <div class="item_time">
                    <el-countdown  :value="60" /> 
                </div>
            </div>
        </div>
        <div class="item">
            <div class="left">
                <div class="jogar">
                    <img src="../imgs/notification.png" alt="">
                    <p>Como jogar</p>
                </div>

                <p class="text">Win Go 1Min</p>

                <div class="balls">
                    <div class="ball greenBall">
                        1
                    </div>
                    <div class="ball greenBall">
                        1
                    </div>
                    <div class="ball greenBall">
                        1
                    </div>
                </div>
            </div>
            <div class="line">

            </div>
            <div class="rit">
                <p class="title">Tempo restante</p>
                <div class="time">
                    <p>{{ minutesTens }}</p>
                    <p>{{ minutesOnes }}</p>
                    <p class="colon">:</p>
                    <p>{{ secondsTens }}</p>
                    <p>{{ secondsOnes }}</p>
                </div>
                <p class="bureauNumber">20231215010729</p>
            </div>
        </div>
    </div>
</template>

<script>
import { reactive, toRefs, computed, onBeforeUnmount } from 'vue'
import  publicData  from '../store/publicVariables'
export default {
    setup() {
        let time = null;
        const state = reactive({
            count: 3600, // 设置初始倒计时时间，单位为秒
            time1: Date.now() + 1000 * 60,
         
        })

        const startCountdown = () => {
            time = setInterval(() => {
                if (state.count > 0) {
                    state.count--;
                }
            }, 1000);
        }

        startCountdown(); // 启动倒计时

        const minutesTens = computed(() => Math.floor(state.count / 600) % 10);
        const minutesOnes = computed(() => Math.floor(state.count / 60) % 10);
        const secondsTens = computed(() => Math.floor((state.count % 60) / 10));
        const secondsOnes = computed(() => state.count % 10);

        onBeforeUnmount(() => {
            clearInterval(time);
        })

        return {
            ...toRefs(state),
            minutesTens,
            minutesOnes,
            secondsTens,
            secondsOnes,
            publicData,
        }
    }
}
</script>

<style lang="scss" scoped>
%center {
    justify-content: center;
    align-items: center;
}

.head {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    transition: 0.5s linear;
    %bgBlack {
        width: 32.91px;
        height: 32.91px;
        background: #12151C;
        position: absolute;
        left: 50%;
        border-radius: 500px;
        z-index: 2;
    }

    .item {
        color: #FFFFFF;
        border-radius: 8px;
        height: 164.42px;

        &:first-child {
            background: #202431;
            box-shadow: inset 0px -4px 5px 0px rgba(0, 8, 18, 0.3);
            display: grid;
            grid-template-columns: repeat(4, 25%);
        }

        &:first-child>div {
            display: flex;
            flex-direction: column;
            @extend %center;
            box-sizing: border-box;
            padding: 17px 0 14px 0;
            cursor: pointer;
            img {
                width: 74px;
                height: 70px;
            }

            p {
                font-size: 20px;
                line-height: 28px;
            }
        }

        &:last-child {
            position: relative;
            background: #5659FB;
            border-radius: 12px;
            padding-bottom: 14px;
            padding-left: 11px;
            padding-right: 18px;
            box-sizing: border-box;
            display: grid;
            grid-template-columns: 50% 50%;

            .line {
                height: 100%;
                border-left: 2.35px dotted #EEEEFF;
                position: absolute;
                left: calc(50% - 1.125px);
                opacity: 0.5;
                z-index: 1;
            }

            &::before {
                content: "";
                top: 0;
                @extend %bgBlack;
                transform: translate(-50%, -50%);
            }

            &::after {
                content: "";
                bottom: 0;
                @extend %bgBlack;
                transform: translate(-50%, 50%);
            }



            .left {
                padding: 14px 0 0 11px;

                .jogar {
                    width: 192.61px;
                    box-sizing: border-box;
                    padding: 10.5px 28.5px;
                    border-radius: 50px;
                    border: 1px solid #FFFFFF;
                    font-size: 18px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;

                    img {
                        width: 22px;
                    }
                }

                .text {
                    margin-top: 19px;
                    margin-bottom: 19px;
                    font-size: 18px;
                    line-height: 20.36px;
                }

                .balls {
                    display: flex;
                    gap: 10px;

                    div {
                        width: 36px;
                        height: 36px;
                        border-radius: 500px;
                        font-size: #fff;
                        display: flex;
                        @extend %center
                    }
                }
            }

            .rit {
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                padding-top: 16px;
                padding-right: 5px;

                .title {
                    font-size: 20px;
                    line-height: 31.32px;
                }

                .time {
                    width: 157px;
                    height: 44.15px;
                    box-sizing: border-box;
                    padding-left: 3px;
                    background: url(../imgs/time.png);
                    background-size: 100% 100%;
                    margin-top: 10px;
                    margin-bottom: 18px;
                    color: #191CC7;
                    font-size: 32px;
                    display: flex;
                    align-items: center;
                    gap: 14px;

                    .colon {
                        margin-left: 5px;
                        margin-right: 5px;
                    }
                }

                .bureauNumber {
                    font-size: 24px;
                }
            }
        }
        .item_time{
            width: 106.52px;
            height: 33.73px;
            background: #12151C;
            border-radius: 30px;
            display: flex;
            @extend %center;
            margin-top: 14px;
            :deep(.el-statistic__number){
                font-size: 20px !important;
                color: #BCBDC1;
                font-weight: 400 !important;
            }
        }
    }

    .active {
        color: #27DFFF;
        position: relative;
       &::after{
        content: '';
        position: absolute;
        bottom: 0px;
        width: 130px;
        height: 3px;
        border-radius: 4.44px;
        background: #27DFFF;
       }
    }
}
</style>