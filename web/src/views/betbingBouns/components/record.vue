<template>
    <div class="record">
        <div class="appBox">
            <div class="title item">
                <P>{{ t('Bettingbonus.DATE') }}</P>
                <P>{{ t('Bettingbonus.TOTALBOUNS') }}</P>
                <P>{{ t('Bettingbonus.SLOT') }}</P>
                <P>{{ t('Bettingbonus.TABLE') }}</P>
                <P>{{ t('Bettingbonus.LEVEL') }}</P>
                <P>{{ t('Bettingbonus.FISH') }}</P>
                <P>{{ t('Bettingbonus.FAST') }}</P>
            </div>
            <div class="body">
                <p class="noData" v-if="data.length == 0">{{ t('Bettingbonus.NOMORE') }}</p>
                <div v-else class="list">
                    <div class="item" v-for="v in data">
                        <P>{{ (v as any).day }}</P>
                        <P style="color:#75ED3D;">{{ (v as any).vip_earnings }}{{ t('base.currency') }}</P>
                        <P>{{ (v as any).slot_earnings }}{{ t('base.currency') }}</P>
                        <P>{{ (v as any).table_earnings }}{{ t('base.currency') }}</P>
                        <P>{{ (v as any).live_earnings }}{{ t('base.currency') }}</P>
                        <P>{{ (v as any).fish_earnings }}{{ t('base.currency') }}</P>
                        <P>{{ (v as any).fast_earnings }}{{ t('base.currency') }}</P>
                    </div>
                </div>

            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { ref } from 'vue';
import { bettingBouns } from "@/api/bettingBouns";
import { debounce } from "@/utils/baseFun";
const { t } = useI18n();

let data = ref([]);

async function getData() {
    let val = null;
    val = await bettingBouns.get_data({ page: 1, limit: 35 }) as any;
    data.value = (val as any).data.data;

}
debounce(getData, 500);        
</script>

<style lang="scss" scoped>
@media (max-width: 768px) {
    .record {
        width: calc(100% - 30px) !important;
        margin-left: 15px;
        overflow: scroll;

        .appBox {
            width: 140%;
        }

        .title {
            p {
                font-size: 12px !important;
            }
        }
    }
}

.record {
    width: 100%;
    min-height: 55vh;
    border-radius: 24px 24px 0px 0px;
    background: var(--theme-box-background);
    border: 1px solid rgba(239, 202, 202, 0.5);

    // filter: blur(1.8px);
    p {
        margin: 0;
    }



    .item {
        display: grid;
        grid-template-columns: 18% 1fr 1fr 1fr 1fr 1fr 1fr;
        justify-items: center;
        align-items: center;

    }

    .title {
        width: 100%;
        height: 62px;
        border-radius: 24px 24px 0px 0px;
        opacity: 1;
        border: 1px solid rgba(239, 202, 202, 0.5);
        // filter: blur(2px);

        p {
            color: var(--auxiliary-font-color-9);
            font-size: 22px;
        }
    }
}

.body {
    width: 100%;
    min-height: calc(55vh - 62px);
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding-top: 12px;

    .list {
        width: 100%;

        div {
            color: var(--auxiliary-font-color-9);
            font-size: 18px;
            margin-top: 12px;
            line-height: 21px;
        }
    }

    .noData {
        color: var(--auxiliary-font-color-9);
        font-weight: bold;
        font-size: 32px;
        margin-top: 20%;


    }
}
</style>