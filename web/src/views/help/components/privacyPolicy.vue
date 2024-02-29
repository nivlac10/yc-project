<template>
    <div>
        <div class="privacyPolicy">
            <p class="title2">{{ t('help.Atabelabaixodescreveprocessamosdados') }}</p>
            <div class="tableHded item">
                <p class="">{{ t('help.PropósitoAtividades') }}</p>
                <p class="">{{ t('help.Data') }}</p>
                <p class="">{{ t('help.LegalidadedoProcessamento') }}</p>
            </div>
            <div class="tableBody">
                <div class="item">
                    <p>{{ t('help.Registrarvocêcomo') }}</p>
                    <p>{{ t('help.Contact') }}</p>
                    <p>{{ t('help.Paraumprirnosso') }}</p>
                </div>
                <div class="hr"></div>
                <div class="item">
                    <p>{{ t('help.ParaumprirnossoItem') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem2') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem3') }}</p>
                </div>
                <div class="hr"></div>
                <div class="item">
                    <p>{{ t('help.ParaumprirnossoItem4') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem5') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem6') }}</p>
                </div>
                <div class="hr"></div>
                <div class="item">
                    <p>{{ t('help.ParaumprirnossoItem7') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem8') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem9') }}</p>
                </div>
                <div class="hr"></div>
                <div class="item">
                    <p>{{ t('help.ParaumprirnossoItem10') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem11') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem12') }}</p>
                </div>
                <div class="hr"></div>

                <div class="item">
                    <p>{{ t('help.ParaumprirnossoItem13') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem14') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem15') }}</p>
                </div>
                <div class="hr"></div>

                <div class="item">
                    <p>{{ t('help.ParaumprirnossoItem16') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem17') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem18') }}</p>
                </div>
                <div class="hr"></div>

                <div class="item">
                    <p>{{ t('help.ParaumprirnossoItem19') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem20') }}</p>
                    <p>{{ t('help.ParaumprirnossoItem21') }}</p>
                </div>
                <div class="hr"></div>
            </div>

        </div>
        <div class="bottom_font">
            <p class="font_title">{{ t('help.privacyPolicyBt1') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt2') }}
            </p>
            <p class="font_title" style="margin-top: 20px;">{{ t('help.privacyPolicyBt3') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt4') }}
            </p>
            <p class="font_title" style="margin-top: 20px;">{{ t('help.privacyPolicyBt5') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt6') }}
            </p>
            <p class="font_title" style="margin-top: 20px;">{{ t('help.privacyPolicyBt7') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt8') }}
            </p>

            <p class="font_title" style="margin-top: 20px;">{{ t('help.privacyPolicyBt9') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt10') }}
            </p>

            <p class="font_title" style="margin-top: 20px;">{{ t('help.privacyPolicyBt11') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt12') }}
            </p>

            <p class="font_title" style="margin-top: 20px;">{{ t('help.privacyPolicyBt13') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt14') }}
            </p>

            <p class="font_title" style="margin-top: 20px;">{{ t('help.privacyPolicyBt15') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt16') }}
            </p>

            <p class="font_title" style="margin-top: 20px;">{{ t('help.privacyPolicyBt17') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt18') }}
            </p>
            <p class="font_title" style="margin-top: 20px;">{{ t('help.privacyPolicyBt19') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt20') }}
            </p>
            <p class="font_title" style="margin-top: 20px;">{{ t('help.privacyPolicyBt21') }}</p>
            <p class="font">
                {{ t('help.privacyPolicyBt22') }}
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from "vue-i18n";
const { t } = useI18n();
</script>

<style lang="scss" scoped>
@media (max-width:768px) {
    .font {
        font-size: 12px !important;
        line-height: 18px !important;
        margin-bottom: 9px !important;
    }

    ul {
        margin-top: 20px !important;

        li {
            margin-bottom: 4px !important;
            margin-left: 20px !important;

            p {
                font-size: 14px !important;
                line-height: 20px !important;
            }
        }

        li::marker {
            width: 6px !important;
            height: 6px !important;
        }
    }
}

p {
    margin: 0;
}

.privacyPolicy {
    width: calc(100% - 40px);
    margin-top: 20px;
    background: #788896;
    padding: 20px 20px 20px 20px;
    border-radius: 5px;
    word-wrap: break-word;
    white-space: pre-wrap;
    margin-bottom: 20px;

    .title2 {
        color: #fff;
        font-size: 19px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .tableHded {
        width: calc(100% - 60px) !important;

        background: var(--theme-box-background);
        margin-bottom: 20px;
        border-radius: 5px;
        padding: 10px 30px;

        p {
            font-weight: bold !important;
        }
    }

    .tableBody {
        width: calc(100% - 60px);
        background: var(--theme-box-background);
        padding: 10px 30px;
        border-radius: 5px;
    }

    .item {
        width: 100%;

        display: grid;
        align-items: center;
        grid-template-columns: 35% 20% 35%;
        column-gap: 5%;

        color: #B2B6C5;



        p {
            font-size: 14px;
            line-height: 20px;
            font-weight: 400;
        }
    }

    .item>p:nth-child(2) {
        text-align: left;
    }


    .hr {
        border: 1px solid #788896;
        margin: 20px 0;
    }

}

.bottom_font {
    width: 100%;

    .font_title {
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #B2B6C5;
    }

    ul {
        // margin-top: 39px;

        li {
            list-style-type: disc;
            color: #B2B6C5;
            margin-bottom: 6px;
            margin-left: 25px;

            p {
                line-height: 33px;
                font-size: 20px;
                font-weight: 500;
                word-wrap: break-word;
                white-space: pre-wrap;
            }
        }

        li::marker {
            width: 8px;
            height: 8px;
        }
    }
}

.font {
    color: #B2B6C5;
    font-size: 14px;
    line-height: 20px;
    font-weight: 400;
    margin-bottom: 7px;
    word-wrap: break-word;
    white-space: pre-wrap;
}
</style>