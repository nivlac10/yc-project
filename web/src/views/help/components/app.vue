<template>
    <div class="app">
        <el-select v-model="value" :placeholder="value" :popper-append-to-body="false" :teleported="false"
            @change="selectChange">
            <el-option-group v-for="group in options" :key="group.label" :label="group.label">
                <el-option v-for="item in group.options" :key="item.value" :label="item.label.value" :value="item.value" />
            </el-option-group>
        </el-select>
        <helpRit></helpRit>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from "vue-i18n";
import { useStore } from '@/store/index';
import helpRit from './ritTxt.vue';
const Store = useStore();
const { t } = useI18n();
const value = ref(t('help.AboutBIGWIN777', { name: Store.state.conf.all_conf.platform['platform_title'] }))

const options = [
    {
        // label: t('help.TERMSPOLICY'),
        options: [
            {
                value: 'Provablyfair',
                label: computed(() => t('footer.SobreNós')),
            },
            {
                value: 'TermsofService',
                label: computed(() => t('footer.CassinoResponsáveis')),
            },
            {
                value: 'PrivacyPolicy',
                label: computed(() => t('footer.TermosdeServiço')),
            },
            {
                value: 'KYCPolicy',
                label: computed(() => t('footer.PolíticadePrivacidade')),
            },
            {
                value: 'Antimoneylaundering',
                label: computed(() => t('footer.PolíticaKYC')),
            },
            {
                value: 'Selfexclusion',
                label: computed(() => t('footer.Contralavagemdedinheiro')),
            },
            {
                value: 'Protectionofminors',
                label: computed(() => t('footer.AutoExclusão')),
            },
            {
                value: 'Responsiblecasino',
                label: computed(() => t('footer.ProteçãodosMenores')),
            },
        ],
    },
]

function selectChange(v) {

    for (let i = 0; i < options.length; i++) {
        const e = options[i];

        for (let j = 0; j < e.options.length; j++) {
            const val = e.options[j];
            if (val.value == v) {
                Store.commit('help/setIndex', [i, j]);
                return null;
            }
        }
    }
}
</script>

<style lang="scss" scoped>
.app {
    margin: 0 12px;
    // width: calc(100% - 40px);
    // margin-left: 20px;

    //下拉框
    :deep(.el-select .el-input.is-focus .el-input__wrapper) {
        box-shadow: none;
    }

    :deep(.el-input__wrapper) {
        background-color: var(--auxiliary-background-6);
        box-shadow: none,
    }

    :deep(.el-select) {
        width: 100%;
    }

    :deep(.el-select__popper.el-popper) {
        background: var(--auxiliary-background-6);
        border: none;
        box-shadow: none;
    }

    :deep(.el-popper__arrow) {
        display: none;
    }

    :deep(.el-select-group__wrap:not(:last-of-type)::after) {
        display: none;
    }

    :deep(.el-select-group__wrap:not(:last-of-type)) {
        padding-bottom: 10px;
    }

    :deep(.el-select-group__title) {
        color: #FFFFFF;
        font-size: 14px;
    }

    :deep(.el-select-dropdown__item) {
        color: #C3CFD8;
        font-size: 13px;
    }

    :deep(.el-select-dropdown__list) {
        padding: 0 0 0 0;
    }

    :deep(.el-select-dropdown__item.hover, .el-select-dropdown__item:hover) {
        background-color: #242936;
        color: #DEA541;
    }

    // :deep(.el-select .el-input.is-focus .el-input__wrapper) {
    //     // box-shadow: 0px 0px 1px 1px #d9ca16 !important;
    // }

    // :deep(.el-select .el-input_wrapper.is-focus) {
    //     // box-shadow: 0px 0px 1px 1px #d9ca16 !important;
    // }

    :deep(.el-select:hover:not(.el-select--disabled) .el-input__wrapper) {
        box-shadow: none;
    }

    :deep(.el-input__inner) {
        color: #DEA541;
    }

}
</style>