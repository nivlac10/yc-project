<template>
    <div class="texasPoker">
        <div class="left">
            <p class="title">{{ t('gameText.EntrarnoPôquerdo') }} <span>{{ t('gameText.Texas') }}</span>！</p>
            <p class="text">{{ t('gameText.Participedetorneios') }}</p>
            <div class="btn" @click="jumpgame()">
                {{ t('gameText.Começarojogo') }}
            </div>
        </div>
        <div class="rit">

        </div>

    </div>
</template>

<script>
import { reactive, toRefs } from "vue";
import { useStore } from "@/store/index";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

export default {
    name: "11",
    components: {
    },
    props: {
        data: {
            type: Object,
        },
    },
    setup(props) {
        const store = useStore();
        const router = useRouter();
        const { t } = useI18n();
        //  变量
        const state = reactive({
        });
        const jumpgame = () => {
            if (store.state.user.token) {
                store.state.status.allGameShow = false
                router.push({
                    name: "playGame",
                    params: {
                        gid: 1816,
                    },
                    query: {
                        directGame: true
                    }
                })
            } else {
                store.dispatch('status/setLoginShow', true)
            }
        }
        return { ...toRefs(state), t, store, jumpgame };
    },
};
</script>
<style lang="scss" scoped>
.texasPoker {
    width: 100%;
    height: 300px;
    display: flex;
    box-sizing: border-box;
    padding: 0 53px;
    justify-content: space-between;

    .left {
        padding: 35px 0;
        // padding-left: 54;
        display: flex;
        flex-direction: column;

        justify-content: space-between;

        .title {
            font-size: 36px;
            color: #fff;

            span {
                color: #8BD042;
            }
        }

        .text {
            // margin-top: 32px;
            font-size: 17px;
            line-height: 25.5px;
            color: #FFFFFF;
            white-space: pre-wrap
        }

        .btn {
            background: #F12C4C;
            color: #fff;
            border-radius: 4px;
            width: 220px;
            height: 48px;
            display: flex;
            justify-content: center;
            align-items: center;
            // margin-top: 32px;
        }
    }

    .rit {
        width: 536px;
        height: 298.45px;
        background: url(@/assets/images/home/character.png);
        background-size: 100% 100%;
    }
}

@media (max-width:768px) {
    .texasPoker {
        padding: 0;
        display: flex;
        flex-direction: column;
        flex-direction: column-reverse;
        align-items: center;
        height: auto;
        background: #202431;
        padding-bottom: 24px;

        .rit {
            width: 319px;
            height: 195.44px;

        }

        .left {
            padding: 0;
            padding: 0 34.5px;
            align-items: center;

            .title {
                font-size: 28px;
                line-height: 36px;
                text-align: center;
            }

            .text {
                font-size: 14px;
                white-space: unset
            }

            .btn {
                width: 306px;
                height: 48px;
                font-size: 14px;
            }
        }
    }
}
</style>