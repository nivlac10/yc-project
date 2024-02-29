<template>
    <div class="placeBet">
        <div class="bulls">
            <div :class="{ bull: true, redBallBg: v.color == 'red' | 'rp', greenBallBg: v.color == 'green' | 'gp' }"
                v-for="(v, i) in list">
                <div :class="{ bullMask: true, fade: v.show }">

                </div>
                <div
                    :class="{ redToPurpleBall: v.color == 'rp', greenBall: v.color == 'green', redBall: v.color == 'red', greenToPurpleBall: v.color == 'gp' }">
                    {{ i }}
                </div>

            </div>
            <div class="bulls_mask">

            </div>
        </div>
        <div class="bet">
            <div class="colorBtn">
                <div class="Green">Verde</div>
                <div class="Violet">Violet</div>
                <div class="Red"> Vermelho </div>
            </div>

            <div class="money">
                <div class="left">
                    <div>r$</div>
                    <p>{{ money }}</p>
                </div>
                <div class="rit">
                    <div @click="minBet">
                        mín
                    </div>
                    <div @click="maxBet">
                        máx
                    </div>
                    <div @click="doubleBet">
                        2x
                    </div>
                    <div @click="halveBet">
                        1/2
                    </div>
                </div>
            </div>
            <div class="Aposta" @click="play">
                Aposta
            </div>
            <p class="rules"><span>Minhas apostas :</span> Escolha alguns números ou cores para apostar</p>
        </div>
    </div>
</template>
 
<script>
import { reactive, toRefs } from 'vue'
import publicData from '../store/publicVariables'
export default {
    setup() {
        const state = reactive({
            count: 0,
            money: 100,
            list: [
                { color: 'rp', show: false },
                { color: 'green', show: false },
                { color: 'red', show: false },
                { color: 'green', show: false },
                { color: 'red', show: false },
                { color: 'gp', show: false },
                { color: 'green', show: false },
                { color: 'red', show: false },
                { color: 'green', show: false },
                { color: 'red', show: false },
            ],
        })
        const minBet = () => {
            publicData.money = 10;
        }
        const maxBet = () => {
            publicData.money = 100;
        }
        const doubleBet = () => {
            publicData.money = 200;
        }
        const halveBet = () => {
            publicData.money = 400;
        }
        const play = () => {
            for (let i = 0; i < state.list.length; i++) {
                const e = state.list[i];
                if (i == 0) {

                    state.list[i].show = true;
                } else {
                    if (i == (state.list.length - 1)) {
                        setTimeout(() => {
                            state.list[i].show = false;
                        }, (1500 * (i + 1)));
                    }
                    setTimeout(() => {
                        state.list[i - 1].show = false;
                        state.list[i].show = true;
                        console.log(i);
                    }, (1500 * i));

                }

            }
        }

        return {
            minBet,
            maxBet,
            doubleBet,
            halveBet,
            play,
            ...toRefs(state),
        }
    }
}
</script>

<style lang="scss" scoped>
%center {
    display: flex;
    justify-content: center;
    align-items: center;
}

.placeBet {
    margin-top: 16px;
    width: 100%;
    border-radius: 12px;
    background: #202431;
    box-shadow: inset 0px -4px 5px 0px rgba(0, 8, 18, 0.3);
    display: grid;
    grid-template-columns: repeat(2, 50%);
    box-sizing: border-box;
    padding: 16px;

    .bulls {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        row-gap: 32px;
        column-gap: 18px;
        box-sizing: border-box;
        padding: 19px 36px;
        background: #12151C;
        border-radius: 12px;
        position: relative;

        .bull {
            width: 86px;
            height: 86px;
            color: #fff;
            border-radius: 500px;
            font-size: 32px;
            @extend %center;
            cursor: pointer;
            position: relative;
            z-index: 6;

            .bullMask {
                width: 100%;
                height: 100%;
                background: rgba(0, 8, 18, 0.4);
                border-radius: 500px;
                position: absolute;
                top: 0;
            }

            div {
                width: 76.44px;
                height: 76.44px;
                border-radius: 500px;
                @extend %center;
            }
        }

        .bulls_mask {
            width: 100%;
            height: 100%;
            border-radius: 12px;
            background: rgba(0, 8, 18, 0.4);
            position: absolute;
            z-index: 5;
        }

        .showBull {
            z-index: 10;
        }
    }

    .bet {
        padding-left: 25px;
        padding-top: 22px;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        flex-direction: column;

        .colorBtn {
            @extend %center;
            gap: 46px;
            margin-bottom: 20px;

            div {
                color: #fff;
                font-size: 16px;
                width: 140px;
                height: 48px;
                @extend %center;
                cursor: pointer;
            }

            .Green {
                background: #40AD72;
                border-top-right-radius: 12px;
                border-bottom-left-radius: 12px;
            }

            .Violet {
                background: #B659FE;
                border-radius: 12px;
            }

            .Red {
                background: #FD565C;
                border-top-left-radius: 12px;
                border-bottom-right-radius: 12px;
            }
        }

        .money {
            width: 512px;
            height: 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
            border: 1.5px solid #585E77;
            border-radius: 8px;
            padding-left: 17px;
            padding-right: 10px;
            margin-bottom: 20px;

            .left {
                color: #fff;
                display: flex;
                align-items: center;
                gap: 5px;

                div {
                    width: 26px;
                    height: 26px;
                    background: #18AA7C;
                    border-radius: 500px;
                    font-size: 13px;
                    @extend %center;
                }

                p {
                    font-size: 20px;
                }
            }

            .rit {
                display: flex;
                align-items: center;
                gap: 8px;

                div {
                    width: 52px;
                    height: 32px;
                    background: #2E3446;
                    border-radius: 6px;
                    font-size: 14px;
                    color: #BCBDC1;
                    cursor: pointer;
                    @extend %center;
                }
            }
        }

        .Aposta {
            width: 512px;
            height: 48px;
            border-radius: 8px;
            background: #4087FF;
            @extend %center;
            font-size: 18px;
            color: #FFFFFF;
            margin-bottom: 16px;
            cursor: pointer;
        }

        .rules {
            font-size: 14px;
            color: #6E7179;
            width: 512px;
            text-align: left;

            span {
                color: #BCBDC1;
            }
        }
    }
}

.fade {
    -webkit-animation: fade 1.5s ease-out both;
    animation: fade 1.5s ease-out both;
}

@-webkit-keyframes fade {
    0% {
        opacity: 1;
    }

    33% {
        opacity: 0;
    }

    80% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}

@keyframes fade {
    0% {
        opacity: 1;
    }

    33% {
        opacity: 0;
    }

    80% {
        opacity: 0;
    }

    50% {
        opacity: 0;
    }

    100% {
        opacity: 0;
    }
}
</style>