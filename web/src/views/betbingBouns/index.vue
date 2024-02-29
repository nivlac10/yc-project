<template>
    <div class="Box   page_margin_top">
        <div class="title">
            <img src="@/assets/images/bettingBouns/wallet.png" alt="">
            <span class="sl_font">{{ t('Bettingbonus.BETTINGBONUC') }}</span>

        </div>
        <div class="tabs">
            <div class="item" @click="handoff(true)">
                <img src="@/assets/images/bettingBouns/chip_select.png" alt="" v-if="isBetBouns" class="betImg">
                <img src="@/assets/images/bettingBouns/chip_Not_select.png" alt="" v-else>
                <p :class="`${isBetBouns ? 'sl_font' : ''}`">{{ t('Bettingbonus.BETBOUNS') }}</p>
            </div>
            <div class="item" @click="handoff(false)">
                <img src="@/assets/images/bettingBouns/bill_not_select.png" alt="" v-if="isBetBouns">
                <img src="@/assets/images/bettingBouns/bill_not_.png" alt="" v-else class="betImg">
                <p :class="`${!isBetBouns ? 'sl_font' : ''}`">{{ t('Bettingbonus.RECORD') }}</p>
            </div>
        </div>
        <bettingBouns v-if="isBetBouns"></bettingBouns>
        <record v-else></record>
    </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { ref } from 'vue';
import { useStore } from '@/store/index';
import { useRouter } from "vue-router";
import bettingBouns from "./components/bettingBouns.vue";
import record from "./components/record.vue";

const router = useRouter();
const { t } = useI18n();
const Store = useStore();

let isBetBouns = ref(true);

function handoff(v) {
    isBetBouns.value = v;
}
</script>

<style lang="scss" scoped>
@media (max-width: 768px) {
    .Box {
        .title {
            margin-bottom: 24px !important;
            margin-left: 15px !important;
            span {
                font-size: 18px !important;
            }

            img {
                width: 50px;
            }
        }

        .tabs {
            margin-bottom: 14px !important;
            margin-left: 20px !important;
            .item {
                width: 145px !important;
                height: 45px !important;
                img{
                    margin-left: 15px !important;
                }
               .betImg{
                margin-left: -15px !important;
                margin-right: -15px !important;
               }

                p {
                    font-size: 13px !important;
                }
            }
        }
    }
}

.Box {
    width: 100%;

    .title {
        display: flex;
        align-items: center;
        margin-bottom: 44px;

        span {
            font-size: 38px;
            font-family: DIN Next LT Pro-Bold, DIN Next LT Pro;
            font-weight: bold;
            color: var(--auxiliary-background-9);
            line-height: 58px;
        }
    }

    .tabs {
        display: flex;
        margin-bottom: 40px;

        .item {
            background: #2D3144;
            width: 186px;
            height: 50px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            margin-right: 16px;

            .betImg {
                width: 82px;
                object-fit: cover;
                margin-left: -15px;
                margin-right: 0;
            }

            img {
                width: 21px;
                margin-left: 27px;
                margin-right: 11px;
            }

            p {
                margin: 0;
                font-size: 18px;
                color: var(--auxiliary-font-color-9);
            }
        }
    }

}</style>