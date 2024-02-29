<template>
    <div class="record">
        <div class="item title">
            <p>{{ t('Bettingbonus.LEVEL') }}</p>
            <p>{{ t('Bettingbonus.FAST') }}</p>
            <p>{{ t('Bettingbonus.SLOT') }}</p>
            <p>{{ t('Bettingbonus.FISH') }}</p>
            <p>{{ t('Bettingbonus.TABLE') }}</p>
        </div>
        <div class="item" v-for="(v, i) in Store.state.conf.all_conf.vip_conf">
            <img :src="vipImgList[i]" alt="">
            <p class="columns">{{ setStringLength(v.fast.toString(), 2) + '%' }}</p>
            <p class="columns">{{ setStringLength(v.slot.toString(), 2) + '%' }}</p>
            <p class="columns">{{ setStringLength(v.fish.toString(), 2) + '%' }}</p>
            <p class="columns">{{ setStringLength(v.table.toString(), 2) + '%' }}</p>
        </div>
    </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { ref } from 'vue';
import { useStore } from '@/store/index';
import { getImageUrl, setStringLength } from "@/utils/baseFun";

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
</script>

<style lang="scss" scoped>
@media (max-width: 768px) {
    .record{
        .title{
            p{
                font-size: 12px !important;
                font-weight: 600;
            }
        }
        .item {
            img{
                width:  28px !important;
                height: 28px !important;
            }
            .columns{
                font-size: 12px !important;
            }
        }
    }
}
.record {
    p {
        margin: 0;
    }

    .item {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        justify-items: center;
        align-items: center;
        background: #202330;
        border-radius: 10.5px;
        height: 48px;
        margin-bottom: 8px;

        img {
            width: 40px;
            height: 40px;
        }

        .columns {
            color: var(--auxiliary-font-color-9);
            font-size: 18px;
        }
    }

    .title {
        p {
            font-size: 18px;
            color: #fff;
        }
    }
}
</style>