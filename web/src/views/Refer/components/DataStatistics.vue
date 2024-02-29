<template>
    <div class="DataStatistics">
        <div class="top">
            <div class="item" @click="getData('all')">{{ t('refer.Tudo') }}</div>
            <div class="item" @click="getData('today')">{{ t('refer.Hoje') }}</div>
            <div class="item" @click="getData('Yesterday')">{{ t('refer.Ontem') }}</div>
            <div class="item" @click="getData('lastWeek')">{{ t('refer.SemanaPassada') }}</div>
            <div class="item">
                <div class="left">
                    <div class="box">
                        <el-date-picker v-model="stateTime" type="date" value-format="YYYY-MM-DD" format="YYYY-MM-DD"
                            :prefix-icon="''" :teleported="false" :editable="false" :placeholder="t('refer.DatadeInício')"
                            :clearable="false" @change="getData('select')" class="leftPicker">

                        </el-date-picker>
                        <div class="txt"> <img src="@/assets/images/refer/Frame.png" alt=""></div>
                        <el-date-picker v-model="endTime" type="date" value-format="YYYY-MM-DD" format="YYYY-MM-DD"
                            :prefix-icon="''" :teleported="false" :editable="false" :cell-class-name="addClass"
                            :placeholder="t('refer.DatadeTérmino')" :clearable="false" @change="getData('select')">
                        </el-date-picker>
                    </div>
                    <!-- <span>Data de Início</span> -->
                    <!-- <img src="@/assets/images/refer/Frame.png" alt=""> -->
                    <!-- <span>Data de Término</span> -->
                </div>
                <div class="rit">
                    <img src="@/assets/images/refer/day.png" alt="">
                </div>
            </div>
        </div>
        <div class="bottom">
            <div class="bottomTitle">
               {{ t('refer.EstatísticasCompletas')}}
            </div>
            <div class="bottomItem">
                <div>
                    <img src="../../../assets/images/refer/newRefer/Equipes.png" alt="">
                    <div class="fontBox">
                        <p>{{t('refer.TotaldeEquipes')}}</p>
                        <span>{{ listData?.total_person_num }}</span>
                    </div>

                </div>
                <div>
                    <img src="../../../assets/images/refer/silver.png" alt="">
                    <div class="fontBox">
                        <p>{{t('refer.ApostasdaEquipe')}}</p>
                        <span>{{ listData?.total_bet }}</span>
                    </div>

                </div>
                <div>
                    <img src="../../../assets/images/refer/gold.png" alt="">
                    <div class="fontBox">
                        <p>{{t('refer.MinhaComissão')}}</p>
                        <span class="checked">{{ listData?.total_brokerage }}</span>
                    </div>

                </div>

            </div>
            <div class="bottomItem2">
                <div v-for="(v, i) in listData?.data" :key="v">
                    <span>{{ t('refer.Nível') }} {{ i + 1 }}</span>
                    <div>
                        <div>
                            <span>{{t('refer.TotaldeEquipes')}}</span>
                            <p>{{ v?.person_num }}</p>
                        </div>
                        <div>
                            <span>{{t('refer.ApostasdaEquipe')}}</span>
                            <p>{{ v?.bet }}</p>
                        </div>
                        <div>
                            <span>{{t('refer.MinhaComissão')}}</span>
                            <p>{{ v?.brokerage }}</p>
                        </div>
                    </div>
                </div>
                <!-- <div>
                    <span>Nível 2</span>
                    <div>
                        <div>
                            <span>{{t('refer.TotaldeEquipes')}}</span>
                            <p>100,000</p>
                        </div>
                        <div>
                            <span>{{t('refer.ApostasdaEquipe')}}</span>
                            <p>{{t('base.currencySymbol')}} 1,000,000</p>
                        </div>
                        <div>
                            <span>{{t('refer.MinhaComissão')}}</span>
                            <p>{{t('base.currencySymbol')}} 1,000,000</p>
                        </div>
                    </div>
                </div>
                <div>
                    <span>Nível 3</span>
                    <div>
                        <div>
                            <span>{{t('refer.TotaldeEquipes')}}</span>
                            <p>100,000</p>
                        </div>
                        <div>
                            <span>{{t('refer.ApostasdaEquipe')}}</span>
                            <p>{{t('base.currencySymbol')}} 1,000,000</p>
                        </div>
                        <div>
                            <span>{{t('refer.MinhaComissão')}}</span>
                            <p>{{t('base.currencySymbol')}} 1,000,000</p>
                        </div>
                    </div>
                </div> -->
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from "vue";
import { getDate, getLastWeekData, moneyFormat } from "@/utils/baseFun";
import { ReferService } from "@/api/refer";
import { useI18n } from "vue-i18n";
const { t } = useI18n();

let endTime = ref('');
let stateTime = ref('');
let listData = ref();
const getData = (val) => {
    let LastWeek = getLastWeekData();
    switch (val) {
        case 'today':
            stateTime.value = getDate(0);
            endTime.value = getDate(0);
            select();
            break;
        case 'Yesterday':
            stateTime.value = getDate(-1);
            endTime.value = getDate(-1);
            select();
            break;
        case 'lastWeek':
            stateTime.value = LastWeek.start_day;
            endTime.value = LastWeek.end_day;
            select();
            break;
        case 'all':
            stateTime.value = '';
            endTime.value = '';
            select();
            break;
        case 'select':
            if (stateTime.value && endTime.value) {
                select();
            }
            break;
        default:
            break;
    }



}

nextTick(() => {
    getData('all');
})

const select = async () => {
    try {
        const data = await ReferService.get_user_team_list({
            start_date: stateTime.value,
            end_date: endTime.value
        });

        const formattedData = {
            ...data.data,
            total_brokerage: moneyFormat(data.data.total_brokerage),
            total_bet: moneyFormat(data.data.total_bet),
            total_person_num: data.data.total_person_num,
            data: data.data.data.map((v) => ({
                ...v,
                bet: moneyFormat(v.bet),
                brokerage: moneyFormat(v.brokerage),
                person_num: v.person_num
            }))
        };

        listData.value = formattedData;
        console.log('formattedData',formattedData);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};


const addClass = () => {
    return 'ritDate'
}
</script>

<style scoped lang="scss">
:deep(.el-input__prefix) {
    display: none;
}

:deep(.el-picker__popper.el-popper) {
    background: #1D1D29;
    border: none;
}

:deep(.el-picker-panel) {
    background: #1D1D29;
    color: #fff;
}

:deep(.el-date-table th) {
    color: #fff;
}

:deep(.el-picker-panel__icon-btn) {
    color: #fff;
}

:deep(.el-date-picker__header-label) {
    color: #fff;
}

:deep(.el-popper__arrow::before) {
    display: none;
}

:deep(.el-input__wrapper) {
    cursor: pointer;
    padding: 0;

}

:deep(.el-input__inner::placeholder) {
    color: #C3CFD9;
}

:deep(.el-date-editor.el-input, .el-date-editor.el-input__wrapper) {
    width: auto;
}


:deep(.el-input__inner) {
    text-align: center;
    font-size: 16px;
}



.DataStatistics {
    // background: #202431;
    border-radius: 24px 24px 24px 24px;
    width: 100%;
    padding: 12px;
    box-sizing: border-box;

    .top {
        width: 100%;
        border-radius: 12px;
        padding: 12px 26px 12px 12px;
        background: #202431;
        display: flex;
        // justify-content: center;
        column-gap: 21px;
        box-sizing: border-box;

        .item {
            border-radius: 12px;
            background: #303546;
            box-shadow: 0px 4px 17px 0px #252C37;
            display: flex;
            justify-content: center;
            align-items: center;
            color: rgba(195, 207, 217, 1);
            font-size: 18px;
            line-height: 21.09px;
            padding: 0 19px;
            min-width: 112px;
            height: 48px;
            cursor: pointer;

            .left {
                display: flex;
                align-items: center;
                justify-content: center;
                column-gap: 8px;
                margin-right: 3px;
                img {
                    width: 21px;
                }

                :deep(.el-input__wrapper) {
                    background: transparent;
                    border: none;
                    box-shadow: none;
                }

            }

            .rit {
                img {
                    width: 32.5px;
                }
            }
        }

        .item:last-child {
            width: 375px;
            display: flex;
            justify-content: space-between;
        }
    }

    .bottom {
        margin-top: 16px;
        padding: 23px 26px;
        // background: rgba(44, 51, 63, 1);
        background: #202431;
        border-radius: 12px;
        display: flex;
        flex-direction: column;

        .bottomTitle {
            color: #B2B6C5;
            font-size: 24px;
            line-height: 28px;
            font-weight: bold;
        }

        .bottomItem {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            column-gap: 32px;
            margin: 16px 0 24px 0;

            img {
                width: 58px;
            }

            div {
                background: #2F3444;
                border-radius: 13.44px;
                display: flex;
                flex-direction: row;
                // justify-content: space-around;
                align-items: center;
                height: 84px;
                padding-left: 17px;

                span {
                    color: #fff;
                    font-size: 24px;
                    line-height: 31.5px;
                    margin-top: 6px;
                }

                p {

                    color: rgba(195, 207, 217, 1);
                    font-size: 18px;
                    line-height: 20px;
                    font-weight: bold;
                }

                .fontBox {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: flex-start;
                }
            }

            .checked {
                color: rgba(117, 237, 61, 1);
            }
        }

        .bottomItem2 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            column-gap: 36px;
            // background: rgba(44, 51, 63, 1);
            // padding: 24px 26px;
            box-sizing: border-box;
            border-radius: 24px;
            // height: 160px;

            div {
                display: flex;
                flex-direction: column;

                span {
                    color: rgba(248, 191, 46, 1);
                    font-size: 22px;
                    // line-height: 28px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }

                div {
                    background: #2F3444;
                    border-radius: 12px;
                    padding: 21px 20px;
                    row-gap: 25px;
                    box-sizing: border-box;

                    div {
                        padding: 0;
                        display: flex;
                        flex-direction: row;
                        align-items: center;
                        justify-content: space-between;

                        span {
                            color: #B2B6C5;
                            font-size: 16px;
                            line-height: 21px;
                            margin: 0;
                        }

                        p {
                            color: #B2B6C5;
                            font-size: 16px;
                            // line-height: 21px;
                        }
                    }
                }

            }
        }
    }

    .box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        // background: #232534;
        border-radius: 8px;
        width: 100%;

        div {
            width: 100%;
        }

        .txt {
            width: 5%;
            font-size: 20px;
            font-weight: 500;
            text-align: center;
            display: flex;
            justify-content: center;
            color: var(--auxiliary-font-color-9);
        }
    }

}

@media (max-width:768px) {

    :deep(.el-input__inner){
        text-align: center;
        font-size: 12px;
    }
    .DataStatistics {
        padding: 7px 6px;

        .top {
            box-sizing: border-box;
            column-gap: 8px;
            row-gap: 11px;
            flex-wrap: wrap;
            padding: 12px 6px;

            .item {
                height: 28px;
                min-width: auto;
                padding: 10px 14px;
                box-sizing: border-box;
                font-size: 12px;
                border-radius: 6px;

                .left {
                    column-gap: 0px;
                }

                .rit {
                    display: flex;
                    align-items: center;

                    img {
                        margin-left: 2px;
                        width: 20px;
                    }
                }

            }

            .item:last-child {
                padding: 10px 13px 10px 7px;
                width: 100%;
                max-width: 337px;
                justify-content: space-between;
            }
        }

        .bottom {
            padding: 17px 12px 6px 12px;
            margin-top: 12px;

            .bottomTitle {
                font-size: 14px;
                line-height: normal;
            }

            .bottomItem {
                grid-template-columns: 1fr;
                row-gap: 6px;
                margin: 17px 0 12px;

                div {
                    width: 100%;
                    height: 66px;
                    border-radius: 12px;
                    padding-left: 26px;
                    box-sizing: border-box;

                    img {
                        width: 40px;
                    }

                    .fontBox {
                        padding-left: 16px;
                        // flex-direction: column-reverse;

                        span {
                            font-size: 16px;
                            font-weight: bold;
                            line-height: normal;
                        }

                        p {
                            margin-top: 0;
                            font-size: 12px;
                        }
                    }
                }
            }

            .bottomItem2 {
                grid-template-columns: 1fr;

                div {
                    span {
                        font-size: 14px;
                        margin-bottom: 9px;
                        margin-top: 12px;
                    }

                    div {
                        row-gap: 12px;
                        padding: 11px 14px 14px 14px;

                        div {
                            p {
                                font-size: 12px;
                            }

                            span {
                                font-size: 12px;
                                line-height: normal;
                            }
                        }
                    }
                }
            }
        }

        .box {
            height: 30px;
            width: 90%;

            :deep(.el-input__inner::placeholder) {
                font-size: 12px;
            }

            .txt {
                font-size: 12px !important;
                // width: auto;
                margin-right: 20px;

                img {
                    width: 14px;
                }
            }
        }

    }
}
</style>