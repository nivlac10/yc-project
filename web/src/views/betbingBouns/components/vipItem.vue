<template>
    <div class="Level">
        <div class="item">
            <div class="head">
                <p class="head_title">{{ t('Bettingbonus.FINISH') }}</p>
            </div>
            <img :src="vipImgList[0]" alt="" class="levelImg">
            <p>{{ t('Bettingbonus.Glory') }}</p>
            <div class="LevelTxt">
                <img src="@/assets/images/bettingBouns/Green_label_strip.png" alt="" class="title2img">
                <p>{{ t('LEAVEL') + ' ' + Store.state.conf.all_conf.vip_conf[0].vip_lv }}</p>
            </div>
            <div class="ratio ">
                <p class="ratio_title">{{ t('Bettingbonus.RATIOOFBETBONUS') }}</p>
                <div class="ratioList">
                    <div>{{ t('Bettingbonus.FAST') }}</div>
                    <div>{{ setStringLength(Store.state.conf.all_conf.vip_conf[0].fast.toString(), 2) + '%' }}</div>
                </div>
                <div class="ratioList">
                    <div>{{ t('Bettingbonus.SLOT') }}</div>
                    <div>{{ setStringLength(Store.state.conf.all_conf.vip_conf[0].slot.toString(), 2) + '%' }}</div>
                </div>
                <div class="ratioList">
                    <div>{{ t('Bettingbonus.FISH') }}</div>
                    <div>{{ setStringLength(Store.state.conf.all_conf.vip_conf[0].fish.toString(), 2) + '%' }}</div>
                </div>
                <div class="ratioList">
                    <div>{{ t('Bettingbonus.TABLE') }}</div>
                    <div>{{ setStringLength(Store.state.conf.all_conf.vip_conf[0].table.toString(), 2) + '%' }}</div>
                </div>
            </div>
        </div>
        <div class="item">
            <div class="head yellow">
                <p class="head_title">{{ t('Bettingbonus.MYLEVEL') }}</p>
            </div>
            <img :src="vipImgList[vipImgListIndex]" alt="" class="levelImg">
            <p>{{ t('Bettingbonus.Silver') }}</p>
            <div class="LevelTxt">
                <img src="@/assets/images/bettingBouns/Yellow_label_bar.png" alt="" class="title2img">
                <p>{{ t('LEAVEL') + ' ' + currentVip?.vip_lv }}</p>
            </div>
            <div class="ratio ">
                <p class="ratio_title">{{ t('Bettingbonus.RATIOOFBETBONUS') }}</p>
                <div class="ratioList">
                    <div>{{ t('Bettingbonus.FAST') }}</div>
                    <div>{{ setStringLength(currentVip.fast.toString(), 2) + '%' }}</div>
                </div>
                <div class="ratioList">
                    <div>{{ t('Bettingbonus.SLOT') }}</div>
                    <div>{{ setStringLength(currentVip.slot.toString(), 2) + '%' }}</div>
                </div>
                <div class="ratioList">
                    <div>{{ t('Bettingbonus.FISH') }}</div>
                    <div>{{ setStringLength(currentVip.fish.toString(), 2) + '%' }}</div>
                </div>
                <div class="ratioList">
                    <div>{{ t('Bettingbonus.TABLE') }}</div>
                    <div>{{ setStringLength(currentVip.table.toString(), 2) + '%' }}</div>
                </div>
            </div>
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

let currentVip = ref({});



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
let vipImgListIndex = ref();

for (let i = 0; i < Store.state.conf.all_conf.vip_conf.length; i++) {
    const e = Store.state.conf.all_conf.vip_conf[i];
    // Store.state.user?.vip_lv
    if (e.vip_lv == 1) {
        currentVip.value = e;
        vipImgListIndex.value = i;
        break;
    }
}

</script>

<style lang="scss" scoped>
@media (max-width: 768px) {
    .Level{
     .item{
            .head{
                height: 24px !important;
                p{
                    font-size:  14px !important;
                }
              
            }
            p{
                font-size: 13px !important;
            }
     }
     .levelImg{
        margin-top: 17px !important;
        width: 61px !important;
        height: 54px !important;
     }
     .ratio {
        width: calc(100% - 14px) !important;
        padding-left: 14px !important;
        .ratio_title{
            font-size: 13px !important;
        }
        .ratioList{
            div{
                font-size: 12px !important;
            }
        }
     }
    }
}
.Level {
    display: grid;
    width: 100%;
    grid-template-columns: 49% 49%;
    column-gap: 2%;

    .item {
        border-radius: 16px;
        background: #212130;
        display: flex;
        flex-direction: column;
        align-items: center;

        .title2img {
            width: 100%;
        }

        p {
            color: var(--auxiliary-font-color-9);
            font-size: 22px;
            font-weight: Bold;
        }

        .yellow {
            background: url(/src/assets/images/bettingBouns/Yellow_label_bar@2x.png) 49% 55% no-repeat !important;
        }

        .head {
            background: url(/src/assets/images/bettingBouns/Green_label_strip@3x.png) 49% 63% no-repeat;
            width: 100%;
            height: 63px;
            border-radius: 16px 16px 0 0;

            .head_title {
                font-size: 23px;
                color: var(--theme-box-background);
                font-weight: bold;
                font-style: italic;
                margin-top: 8px;
                margin-left: 18px;
            }
        }
    }

    .bouns>img:nth-child(1) {
        width: 100%;
    }

    .levelImg {
        margin-top: 35px;
        margin-bottom: 4px;
        width: 100px;
        height: 88px;
    }

    .LevelTxt {
        position: relative;

        p {
            position: absolute;
            top: -5%;
            left: 0px;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--theme-box-background);
        }
    }

    .ratio {
        width: calc(100% - 20px);
        padding-left: 20px;
        margin-bottom: 25px;

        .ratio_title {
            width: 100%;
            text-align: left;
            color: var(--auxiliary-font-color-11);
            font-size: 18px;
            font-weight: 500;
        }

        .ratioList {
            display: flex;
            justify-content: space-between;
            margin-top: 8px;
            width: calc(100% - 20px);
            margin-right: 20px;

            div {
                font-size: 15px;
            }
        }

        .ratioList>div:nth-child(1) {
            color: var(--auxiliary-font-color-9);
        }

        .ratioList>div:nth-child(2) {
            color: var(--auxiliary-font-color-7);
        }
    }
}
</style>