<template>
    <div class="helpBox">
        <back-head :back-name-show="false" :title="t('help.CentrodeAjuda')" />
        <!-- <div class="title">
            <img src="@/assets/images/help/HELP_CENTER.png" alt="">
            <span class="sl_font">{{ t('help.HELPCENTER') }}</span>
            <img src="@/assets/images/help/Shut_down.png" alt="" class="close" @click="closeHelp">
        </div> -->
        <div class="body" v-if="Store.state.status.isPc">
            <helpLeft></helpLeft>
            <helpRit></helpRit>
        </div>
        <helpApp v-else></helpApp>
    </div>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { ref } from 'vue';
import helpLeft from './components/left.vue'
import helpRit from './components/ritTxt.vue';
import helpApp from './components/app.vue'
import { useStore } from '@/store/index';
import { useRouter } from "vue-router";
import backHead from "@com/back/index.vue"

const router = useRouter();
const { t } = useI18n();
const Store = useStore();

function closeHelp() {
    router.back();
}
</script>

<style lang="scss" scoped>
@media screen and (max-width: 768px) {
    .helpBox {
        // width: calc(100% - 40px) !important;
        // margin-left: 20px;

        .title {
            position: relative;
            margin-left: 13px;

            .close {
                display: block;
                width: 21px !important;
                height: 21px !important;
                position: absolute;
                right: 20px;
                top: 12px;
            }

            span {
                font-size: 18px !important;
            }

            img {
                width: 39px !important;
                height: 43px !important;
                object-fit: fill;
            }
        }
    }
}

.helpBox {
    width: 100%;

    .close {
        display: none;
    }

    .title {
        display: flex;
        align-items: center;

        span {
            font-size: 38px;
            font-family: DIN Next LT Pro-Bold, DIN Next LT Pro;
            font-weight: bold;
            color: var(--auxiliary-background-9);
            line-height: 58px;
        }
    }

    .body {
        display: grid;
        grid-template-columns: 20% calc(80% - 24px);
        column-gap: 24px;
        margin-top: 24px;
        margin-bottom: 77px;
        min-height: 75vh;
    }
}
</style>