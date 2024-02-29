<template>
    <div class="myInvitations">
        <div class="list_3 list_h">
            <div class="head">
                <p>{{ t('refer.Jogador') }}</p>
                <p>{{ t('refer.RegistroConcluído') }}</p>
                <p>{{ t('btnName.Depósito') }}</p>
            </div>
            <div class="body">
                <div v-for="(item, index) in listData?.data" :key="item" class="pp">
                    <div>
                        <img :src="getImageUrl(`avatar/headsculpture_img_${item.header_img}.png`)" alt="">
                        <span>{{ item.uid }}</span>
                    </div>
                    <div>{{ item.add_time }}</div>
                    <div :class="{ g_color: item.is_recharge == 1, r_color: item.is_recharge == 0 }">{{
                        item.is_recharge
                        == 1 ?
                        t('refer.Depositado') : t('refer.esperandodepósito') }}</div>
                </div>
                <p class="noData" v-show="listData?.count == 0">{{ t('refer.NenhumaMensagem') }}</p>
            </div>


        </div>
        <pagination ref="paginationRef" @changePage="getData" :pageForm="state.pageForm" />
    </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { ReferService } from "@/api/refer";
import { getImageUrl, dateStrChangeTimeTamp, currentTimeChangeStr } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
import pagination from "@/components/pagination/index.vue";

const { t } = useI18n();
let listData = ref();
const state = reactive({
    pageForm: {
        page: 1,
        limit: 10,
        count: 0,
    }
})

const getData = async (key, val) => {
    let data;
    if (key && val) {
        data = await ReferService.get_user_lower_data({ [key]: val });
    } else {
        data = await ReferService.get_user_lower_data();
    }

    listData.value = data.data;
    state.pageForm.count = listData.value.count
    if (listData.value?.data && listData.value?.data?.length !== 0) {
        listData.value.data.map(v => {

            v.add_time = currentTimeChangeStr('mm-dd-hh-ii', dateStrChangeTimeTamp(v.add_time), '-', ':')
        })
    }
}
getData();

</script>

<style lang="scss" scoped>
.myInvitations {
    margin-bottom: 100px;

    .list_3 {
        overflow-x: scroll;
        border-radius: 12px;
        overflow: hidden;
        position: relative;

        .noData {
            color: #b2b6c578;
            font-weight: bold;
            font-size: 32px;
            margin-top: 24vh;
            position: absolute;
            display: flex;
            justify-content: center;
            width: 100%;

        }

        .head {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            background: #2F3445;

            p {
                font-size: 18px;
                font-weight: 500;
                height: 60px;
                color: #B2B6C5;
                text-align: center;
                line-height: 60px;
            }
        }

        .body {
            text-align: center;
            background: #202431;
            padding: 25px 0;
            min-height: 50vh;

            .pp {
                font-size: 18px;
                margin-bottom: 25px;
                display: grid;
                grid-template-columns: repeat(3, 1fr);

                &:last-child {
                    margin-bottom: 0;
                }

                div {
                    color: #B2B6C5;

                    &:nth-child(1) {
                        img {
                            margin-right: 8px;
                            width: 36px;
                            vertical-align: middle;
                        }
                    }

                    &.g_color {
                        color: #75ED3D;
                    }

                    &.r_color {
                        color: #FF7979;
                    }
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

    .noData {
        font-size: 14px !important;
        margin-top: 43% !important;
    }

    .myInvitations {

        .list_h {
            height: auto;
            min-height: 300px;
            background: #202431;
        }

        .list_3 {
            overflow-x: scroll;

            .head {


                p {
                    font-size: 12px;
                    height: 45px;
                    line-height: 45px;
                }
            }

            .body {
                text-align: center;
                background: #202431;
                padding: 16px 0;

                .pp {
                    font-size: 12px;
                    line-height: normal;
                    font-weight: 500;
                    margin-bottom: 16px;

                    div {

                        font-weight: 500;

                        &:nth-child(1) {
                            font-weight: 500;

                            img {
                                width: 18px;
                            }
                        }


                    }
                }

            }


        }
    }
}
</style>