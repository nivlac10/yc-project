<template>
    <div class="bettingBouns">
        <p class="title">
            {{ t('Bettingbonus.BETTINGBONUC') }}
        </p>
        <div class="body">
            <div class="left">
                <div class="bouns">
                    <img src="@/assets/images/bettingBouns/nationalflag_icon.png" alt="">
                    <p>{{ bouns + ' ' + Currency }}</p>
                </div>
                <vipItem></vipItem>
                <p class="bottomTitle">
                    {{ t('Bettingbonus.INTRODUCE') }}
                </p>
                <p class="bottomtext">
                    {{ t('Bettingbonus.Beltingbonuses') }}
                </p>
            </div>
            <div class="rit">
                <left></left>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { ref } from 'vue';
import { useStore } from '@/store/index';
import { getImageUrl } from "@/utils/baseFun";
import vipItem from "./vipItem.vue";
import left from "./left.vue";
import { bettingBouns } from "@/api/bettingBouns";
import { debounce } from "@/utils/baseFun";
const { t } = useI18n();
const Store = useStore();


let vipImgList = [
    getImageUrl('vipBonus/level_0.png'),
    getImageUrl('vipBonus/level_1.png'),
    getImageUrl('vipBonus/level_2.png'),
    getImageUrl('vipBonus/level_3.png'),
    getImageUrl('vipBonus/level_4.png'),
    getImageUrl('vipBonus/level_5.png'),
    getImageUrl('vipBonus/level_6.png'),
    getImageUrl('vipBonus/level_7.png'),
    getImageUrl('vipBonus/level_8.png'),
    getImageUrl('vipBonus/level_9.png'),
];

let bouns = ref(0.00);
let Currency = ref('BRL')

const getBouns = async () => {
    let val = await bettingBouns.get_data({ page: 1, limit: 1 });
    bouns.value = val.data.vip_earnings;
}

debounce(getBouns,1000);

</script>

<style lang="scss" scoped>
@media (max-width: 768px) {
    .bettingBouns {
        background: transparent !important;
        width: calc(100% - 40px) !important;
        padding: 14px 20px 0 20px !important;

        .title {
            font-size: 18px !important;
            font-weight: 700 !important;
        }

        .bouns {
            height: 31px !important;

            img {
                width: 32px !important;
                height: 20px !important;
            }

            p {
                font-size: 13px !important;
                font-weight: 700 !important;
            }
        }

        .body {
            display: flex !important;
            flex-direction: column;

            .left {
                .bottomTitle {
                    font-size: 13px !important;
                    margin-top: 15px !important;
                    margin-bottom: 5px !important;
                }

                .bottomtext {
                    font-size: 12px !important;
                    margin-bottom: 11px !important;
                }
            }
        }
    }
}

.bettingBouns {
    background: var(--theme-box-background);
    width: calc(100% - 66px);
    padding: 37px 33px 0 33px;
    border-radius: 24px;
    min-height: 55vh;

    p {
        margin: 0;
    }

    .title {
        font-size: 30px;
        color: #fff;
        margin-bottom: 22px;
    }

    .body {
        display: grid;
        grid-template-columns: calc(50% - 24px) calc(50% - 24px);
        column-gap: 48px;

        .left {
            .bouns {
                width: calc(100% - 30px);
                height: 46.08px;
                border: 1.5px solid var(--theme-input-border-color);
                border-radius: 8px;
                margin-bottom: 29px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 15px 0 15px;

                img {
                    width: 37px;
                    height: 25.65px;
                }

                p {
                    font-size: 20px;
                    color: #fff;
                }
            }

            .bottomTitle {
                color: #F59922;
                font-size: 18px;
                font-weight: 600;
                margin-top: 23px;
                margin-bottom: 13px;
            }

            .bottomtext {
                color: #7992A7;
                font-size: 15px;
                font-weight: 400;
            }
        }
    }
}</style>