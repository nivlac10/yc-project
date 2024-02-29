<template>
    <div class="record">
        <div class="appBox">
            <div class="title item">
                <P>{{ t('account.DWTAILS') }}</P>
                <P>{{ t('account.DETAILSAMOUNT') }}</P>
                <P>{{ t('account.AMOUNT') }}</P>
                <P>{{ t('account.WITHDRAWFEE') }}</P>
                <P>{{ t('account.STATUS') }}</P>

            </div>
            <div class="body">
                <p class="noData" v-if="data.data.length == 0">{{ t('Bettingbonus.NOMORE') }}</p>
                <div v-else class="list">
                    <div class="item" v-for="v in data.data">
                        <P>{{ v.add_time }}</P>
                        <P style="color:#75ED3D;">{{ v.money }}</P>
                        <P>{{ v.money }}</P>
                        <P>{{ v.first_pay }}</P>
                        <P>{{ v.status == 0 ? 'Fail' : v.status == 1 || v.status == 5 ?
                            'success' : 'Recharging' }}</P>
                    </div>
                </div>

                <div class="pagination">
                    <img src="@/assets/images/account/Leftarrow@2x.png" alt="" @click="toLeftPage">
                    <div class="page">
                        <p>{{ currentPage }}</p>/ <p>{{ page }}</p>
                    </div>
                    <img src="@/assets/images/account/Rightarrow@2x.png" alt="" @click="toRitPage">
                </div>

            </div>
        </div>

    </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { ref, computed } from 'vue';

const props = defineProps({
    data: {
        type: Object
    }
});
let data = computed(() => props.data);
const { t } = useI18n();

const total = ref(data.value.count);

const page = ref(1);

const count = ref(10);

let currentPage = ref(1);

const toPage = () => {
    if (total.value !== 0) {
        if (total.value % count.value == 0) {
            page.value = total.value / count.value;
        } else {
            page.value = ((total.value - (total.value % count.value)) / count.value) + 1;
        }
    }

}
toPage();
const toLeftPage = () => {
    if (currentPage.value !== 1) {
        currentPage.value -= 1;
        proxy.$mitt.emit("getTableData", currentPage.value);
    }

}

const toRitPage = () => {
    if (currentPage.value < page.value) {
        currentPage.value += 1;
        proxy.$mitt.emit("getTableData", currentPage.value);
    }

}

</script>

<style lang="scss" scoped>
@media (max-width: 768px) {
    .record {
        width: calc(100% - 40px) !important;
        // margin-left: 15px;
        overflow: scroll;

        .appBox {
            width: 140%;
        }

        .noData {
            font-size: 18px !important;
        }

        .title {
            p {
                font-size: 12px !important;
            }
        }

        .body {
            margin-bottom: 20%;
        }

        .pagination {
            bottom: -14% !important;
        }

    }
}

.record {
    width: 100%;
    min-height: 55vh;
    border-radius: 24px;
    background: var(--theme-box-background);
    border: 1px solid rgb(40 38 38);

    // filter: blur(1.8px);
    p {
        margin: 0;
    }



    .item {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        justify-items: center;
        align-items: center;

    }

    .title {
        width: 100%;
        height: 62px;
        border-radius: 24px 24px 0px 0px;
        opacity: 1;
        border: 1px solid rgb(40 38 38);
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
    position: relative;

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

.pagination {
    position: absolute;
    bottom: 4%;
    display: flex;
    align-items: center;

    .page {
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--auxiliary-font-color-9);
        margin-left: 18px;
        margin-right: 18px;
    }

    img {
        width: 36px;
        height: 36px;
    }
}
</style>