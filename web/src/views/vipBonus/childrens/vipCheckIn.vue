<template>
    <div>
        <el-dialog v-model="store.state.status.vipCheckIn" :show-close="false" :close-on-press-escape="false" :close-on-click-modal="false"
            :width="store.state.status.isPc ? '400px' : '100%'" @click="close">
            <div class="dialog_content">
                <div class="dialog_content_title">
                    <span>{{ t('signIn.Checkindiário') }}</span>
                    <img src="@assets/images/public/Shutdownx.png" alt="">
                </div>
                <div class="dialog_content_column">
                    <div>{{ t('refer.Nível') }}:</div>
                    <div>{{ t('refer.Bônus') }}:</div>
                </div>
                <ul>
                    <li v-for="(v, i) in vipBouns">
                        <img :src="v.vipLvImg" alt="">
                        <div>{{ t('base.currencySymbol') }}{{ v.bouns }}</div>
                    </li>
                </ul>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import { reactive, toRefs } from 'vue'
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { getImageUrl } from "@/utils/baseFun";
export default {
    setup () {
        const { t } = useI18n();
        const store = useStore();
        const state = reactive({
            count: 0,
            vipBouns: [],
        })
        const close = ()=>{
         store.dispatch('status/setvipCheckIn',false);
        }
        const setvipBouns = () => {
            if (state.vipBouns.length > 0) {
                    return;
            }   
     
            for (let i = 0; i < store.state.conf.all_conf.vip_conf.length; i++) {
                const e = store.state.conf.all_conf.vip_conf[i];
                let data = {
                    vipLvImg : getImageUrl(`vipBonus/level_${e.vip_lv}.png`),
                    bouns: e.day_bonus,
                }
       
                state.vipBouns.push(data);
            }
      
        }
        setvipBouns();
        return {
            ...toRefs(state),
            store,
            close,
            t
        }
    }
}
</script>

<style lang="scss" scoped>

.dialog_content {
        padding: 14px 0 31px 0;
        width: 100%;
        background: #202431;
        border-radius: 8px;

        .dialog_content_title {
            position: relative;
            margin-bottom: 27px;
            text-align: center;

            span {
                font-size: 16px;
                font-weight: 600;
                color: #FFFFFF;
            }

            img {
                cursor: pointer;
                position: absolute;
                top: 50%;
                right: 12px;
                transform: translateY(-50%);
                width: 21px;
            }
        }

        .dialog_content_column {
            display: flex;
            margin-bottom: 20px;

            div {
                width: 50%;
                font-size: 14px;
                font-weight: 600;
                text-align: center;
                color: #98ABD0;
            }
        }

        ul {
            li {
                display: grid;
                grid-template-columns: 1fr 1fr;
                justify-items: center;
                align-items: center;
                margin-bottom: 20px;

                &:nth-last-child(1) {
                    margin-bottom: 0;
                }

                img {
                    width: 36px;
                    height: 36px;
                }

                div {
                    width: 50%;
                    text-align: center;
                    font-size: 18px;
                    color: #FFFFFF;
                }
            }
        }
    }
    @media (max-width:768px) {
        
        .dialog_content {
            margin: 0 12px;
            padding: 18px 0 29px 0;

            .dialog_content_title {
                margin-bottom: 21px;
            }

            ul {
                li {
                    margin-bottom: 16px;

                    div {
                        font-size: 16px;
                    }
                }
            }
        }
    }
</style>