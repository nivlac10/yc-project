<template>
    <div class="myInvitations">
        <div class="head">
            <selectBox :options="options" @selectChange=select :popper-append-to-body="false">
            </selectBox>
            <div class="search_box">
                <img src="@assets/images/refer/home_Classification_search_icon.png" alt="" />
                <el-input clearable @blur="getData()" v-model="userId" class="myInvitationsInput"
                    :placeholder="t('refer.DigiteoIDdoUsuário')" />
            </div>
        </div>

        <div class="list_3 list_h">

            <div class="table_head">
                <p>{{ t('refer.Tempoderegistro') }}</p>
                <p>{{ t('account.IDdousuário') }}</p>
                <p>{{ t('refer.Níveis') }}</p>
                <p>{{ t('refer.Nome') }}</p>
            </div>

            <div class="table_body">
                <div v-for="(item, index) in listData?.data" :key="item">
                    <p>{{ item.add_time }}</p>
                    <p>{{ item.uid }}</p>
                    <p>{{ item.level }}</p>
                    <p>{{ item.nickname }}</p>
                </div>
                <p class="noData" v-show="listData?.count == 0">{{ t('refer.NenhumaMensagem') }}</p>
            </div>
        </div>
        <pagination ref="paginationRef" @changePage="getData2" :pageForm="state.pageForm" />
    </div>
</template>

<script setup>
import { ref, computed, reactive } from "vue";
import selectBox from "@/components/selectBox/selectBox.vue";
import { ReferService } from "@/api/refer";
import pagination from "@/components/pagination/index.vue";
import { dateStrChangeTimeTamp, currentTimeChangeStr } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
const { t } = useI18n();

let userId = ref('');
let listData = ref({ count: 0 });
const state = reactive({
    pageForm: {
        page: 1,
        limit: 10,
        count: 0,
    }
})
let options = [
    { label: computed(() => t('refer.Todososníveisdereferência')).value, value: 0 },
    { label: computed(() => t('refer.Nível')).value + '1', value: 1 },
    { label: computed(() => t('refer.Nível')).value + '2', value: 2 },
    { label: computed(() => t('refer.Nível')).value + '3', value: 3 }

]
let level = ref(0)
const getData = async (val) => {
    let data = null
    data = await ReferService.get_member_list({ level: level.value, nickname: userId.value });


    listData.value = data.data;
    state.pageForm.count = listData.value.count
    if (listData.value.length != 0) {
        listData.value.data.map(v => {
            v.add_time = currentTimeChangeStr('mm-dd-hh-ii', dateStrChangeTimeTamp(v.add_time), '-', ':')
        })
    }
}
const getData2 = async (key, val) => {
    let data;
    if (key && val) {
        data = await ReferService.get_member_list({ [key]: val, level: level.value, nickname: userId.value });
    } else {
        data = await ReferService.get_member_list();
    }

    listData.value = data.data;
    if (listData.value?.data?.length != 0) {
        listData.value.data.map(v => {
            v.add_time = currentTimeChangeStr('mm-dd-hh-ii', dateStrChangeTimeTamp(v.add_time), '-', ':')
        })
    }
}
getData();

const select = (v) => {
    level.value = v.value
    // if (v) {
    getData()


}
</script>

<style lang="scss" scoped>
:deep(.selectBox .select_box_column input) {
    border-radius: 8;
    border: none;
    background: #2D3144;


    &::placeholder {
        color: #B2B6C5;
    }
}

:deep(.el-input .el-input__icon) {
    margin-right: 8px;
}


.myInvitations {
    .head {
        width: 676px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        column-gap: 22px;
        margin-bottom: 24px;

    }

    .search_box {
        position: relative;
        border-radius: 8px;
        overflow: hidden;
        min-height: 42px;

        :deep(.el-input) {
            height: 100%;
        }

        img {
            position: absolute;
            top: 50%;
            transform: translate(0, -50%);
            left: 13px;
            z-index: 1;
            width: 28px;
        }

        :deep(.el-input) {
            // width: 276px;
            // height: 42px;
            min-height: 42px;

            .el-input__wrapper {
                padding: 0;
                background: var(--theme-navigationbar-background);
                box-shadow: none;
            }

            .el-input__inner {
                height: 100%;
                padding-left: 50px;
                background: var(--theme-navigationbar-background);
                // border: 2px solid #585e77;
                border-radius: 15px;
                color: var(--theme-font-color-fff);

                &::placeholder {
                    color: #585E77;

                }
            }

            .el-input__suffix {
                display: flex;
                align-items: center;
                justify-content: center;
            }
        }
    }

    .list_3 {
        overflow-x: scroll;
        border-radius: 12px;
        overflow: hidden;
        position: relative;

        .noData {
            color: #b2b6c578;
            font-weight: bold;
            font-size: 32px;
            margin-top: 23vh;
            position: absolute;
            display: flex;
            justify-content: center;
            width: 100%;

        }

        .table_head {
            background: #2F3445;
            display: grid;
            grid-template-columns: repeat(4, 1fr);

            p {
                font-size: 18px;
                font-weight: 500;
                height: 60px;
                color: #B2B6C5;
                text-align: center;
                line-height: 60px;
            }
        }

        .table_body {
            padding: 25px 0px;
            min-height: 50vh;

            div {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                margin-bottom: 25px;

                &:last-child {
                    margin-bottom: 0;
                }

                p {
                    text-align: center;
                    font-size: 18px;
                    color: #B2B6C5
                }

            }
        }



    }

    .list_h {
        // height: 660px;
        background: #202431;
    }
}

@media screen and (max-width: 768px) {
    .myInvitations {

        .search_box {
            min-height: 30px;
            display: flex;
            align-items: center;

            :deep(.el-input) {
                min-height: 30px;
            }


            img {
                width: 24px;
            }

            :deep(.el-input) {

                .el-input__inner {
                    font-size: 12px;

                    &::placeholder {
                        color: #585E77;
                        font-size: 12px;
                    }
                }
            }
        }


    }

    .noData {
        font-size: 14px !important;
        margin-top: 40% !important;
    }



    .myInvitations {
        .head {
            width: 100%;
            grid-template-columns: 1fr;
            row-gap: 12px;
            margin-bottom: 12px;
        }

        .list_h {
            height: auto;
            min-height: 300px;
            background: #202431;
        }



        .list_3 {
            overflow-x: scroll;

            .table_head {


                p {
                    font-size: 12px;
                    height: 45px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    line-height: normal;
                    // line-height: 45px;
                }
            }

            .table_body {
                height: auto;
                min-height: 300px;
                padding: 16px 0;

                div {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    margin-bottom: 16px;

                    p {
                        font-size: 12px;
                        line-height: 24px;
                        font-weight: 500;
                    }

                }
            }

            // table {
            //     width: 100%;

            //     thead {
            //         font-size: 12px;
            //         height: 45px;
            //         line-height: 45px;
            //     }

            //     tbody {
            //         height: auto;
            //         min-height: 300px;

            //         tr {
            //             font-size: 12px;
            //             line-height: 24px;

            //             &:last-child {
            //                 margin-bottom: 10px;
            //             }

            //             font-weight: 500;

            //             td {
            //                 color: #B2B6C5;
            //                 font-weight: 500;

            //                 &:nth-child(1) {
            //                     font-weight: 500;

            //                     img {
            //                         width: 18px;
            //                     }
            //                 }
            //             }
            //         }
            //     }
            // }
        }
    }
}
</style>