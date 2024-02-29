<template>
    <div class="gameSwiper">
        <div class="game_swiper_head">
            <div class="s_left">
                <!-- <img src="@/assets/images/home/TOP_icon@3x.png" alt="" /> -->
                <svg-icon name="fornecedor_icon"></svg-icon>
                <span>{{ t('sidebar.Fornecedor') }}</span>
            </div>
            <div class="mais_box">
                <!-- @vue-ignore -->
                <div class="mais_font" @click="store.state.status.allGameShow = true, store.state.status.game_id = null">
                    {{ t('btnName.Mais') }}</div>
                <div class="btn">
                    <div class="btn_c" @click="prevSwiper">
                        <svg viewBox="64 64 896 896" focusable="false" data-icon="left" width="1em" height="1em"
                            fill="currentColor" aria-hidden="true">
                            <path
                                d="M724 218.3V141c0-6.7-7.7-10.4-12.9-6.3L260.3 486.8a31.86 31.86 0 000 50.3l450.8 352.1c5.3 4.1 12.9.4 12.9-6.3v-77.3c0-4.9-2.3-9.6-6.1-12.6l-360-281 360-281.1c3.8-3 6.1-7.7 6.1-12.6z">
                            </path>
                        </svg>
                    </div>
                    <div class="btn_c" @click="nextSwiper">
                        <svg viewBox="64 64 896 896" focusable="false" data-icon="right" width="1em" height="1em"
                            fill="currentColor" aria-hidden="true">
                            <path
                                d="M765.7 486.8L314.9 134.7A7.97 7.97 0 00302 141v77.3c0 4.9 2.3 9.6 6.1 12.6l360 281.1-360 281.1c-3.9 3-6.1 7.7-6.1 12.6V883c0 6.7 7.7 10.4 12.9 6.3l450.8-352.1a31.96 31.96 0 000-50.4z">
                            </path>
                        </svg>
                    </div>
                </div>
            </div>
        </div>
        <swiper :loop="true" class="mySwiper" @swiper="onSwiper" @slideChange="onSlideChange" style="" effect="fade">
            <swiper-slide v-for="(item, i) in game_list" class="swper_list_box">
                <div class="factory_img_box" v-for="factory in item" :key="factory" @click="openAllGamePop(factory)">
                    <img :src="factory['cover']" alt="">
                </div>
            </swiper-slide>
        </swiper>
    </div>
</template>
<script lang="ts">
import {
    reactive,
    toRefs,
    getCurrentInstance,
    defineComponent,
    ref,
    onMounted,
} from "vue";
import { useStore } from "@/store/index";
import gameBox from "./gameBox.vue";
import { Swiper, SwiperSlide } from 'swiper/vue';
import { get_game_data } from "@/utils/gameUtils";
import 'swiper/css';
import { useI18n } from "vue-i18n";
export default defineComponent({
    name: "gameSwiper",
    components: {
        gameBox,
        Swiper,
        SwiperSlide
    },
    props: {
        listType: {
            type: Number,
            default: 1,
        },
    },

    setup(props, { emit }) {
        const { t } = useI18n();
        const store = useStore();
        const state = reactive({
            setActiveItem: 2,
            game_list: [],
            game_count: 0,
            swiperDom: null,
            swiperIndex: 0,
        });
        // 获取数据  数组切割
        function gameData() {
            let limit = store.state.status.isPc ? 6 : 3;
            let count = store.state.conf.game_list.factory_list.length;
            let factory_list = store.state.conf.game_list.factory_list
            let page = 0;
            for (let i = 0; i < count; i++) {
                let new_arr = [];
                let offset = page * limit;
                for (let j = 0; j < factory_list.length; j++) {
                    if (offset <= j && j < offset + limit) {
                        new_arr.push(factory_list[j] as never);
                    }
                }
                page++;
                if (new_arr.length > 0) {

                    state.game_list.push(new_arr as never);
                }
            }
            console.log(state.game_list);

        }
        gameData();
        let _this: any = "";
        let carousel = ref(null);

        const onSwiper = (swiper) => {
            state.swiperDom = swiper;
            // console.log(swiper);
        };
        const onSlideChange = () => {
        };
        // 上一页
        const nextSwiper = () => {
            // @ts-ignore
            state.swiperDom.slideNext();
        }
        const prevSwiper = () => {
            // @ts-ignore
            state.swiperDom.slidePrev();

        }
        const openAllGamePop = (v) => {
            store.state.status.allGameShow = true
            store.state.status.game_id = v.game_id
        }
        return { ...toRefs(state), onSwiper, onSlideChange, prevSwiper, nextSwiper, props, t, openAllGamePop, store };
    },
});
</script>
<style  lang="scss" scoped>
// }50px
@media (max-width: 750px) {
    .gameSwiper {
        margin: 0 0 !important;
    }

    .mais_box {
        display: flex;
        align-items: center;
        gap: 6px;

        .mais_font {
            font-size: 12px !important;
            border: 1px solid #585E77;
            color: #585E77;
            border-radius: 6px !important;
            padding: 4px 12px !important;
            cursor: pointer;
        }




        .btn {
            display: flex;
            align-items: center;
            gap: 6px;
            justify-content: center;

            .btn_c {
                cursor: pointer;
                display: flex;
                align-items: center;
                padding: 4px !important;
                border: 1px solid #585E77;
                color: #fff;
                font-size: 12px !important;
                border-radius: 6px !important;
                color: #585E77;
            }
        }
    }

    .swper_list_box {
        grid-template-columns: repeat(3, 1fr) !important;
    }

    .game_max_box {
        display: grid;
        grid-template-columns: repeat(3, 1fr) !important;
    }

    .factory_img_box {
        height: 50px !important;
    }

    .s_left {
        display: flex;
        align-items: center;
        gap: 10px;

        svg {
            font-size: 30px !important;
        }

        span {
            font-size: 14px !important;
        }
    }
}

.game_max_box {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    column-gap: 10px;
    width: 100%;
}

:deep(.swiper-wrapper) {
    gap: 1px;
}

.swper_list_box {
    display: inline-grid;
    grid-template-columns: repeat(6, 1fr);
    grid-row-gap: 30px;
    grid-column-gap: 10px;
    width: 100%;

    .factory_img_box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

        background: #202431;
        border: 0px solid rgba(139, 164, 254, 0.2);
        border-radius: 8px;

        height: 78px;

        img {
            // width: 112px;
            // width: 78px;
            width: 80%;
        }
    }

    .factory_img_box:hover {

        background: #2F3445;
    }
}

.gameSwiper {
    font-size: 18px;
    color: #fff;
    font-weight: 600;
    margin: 20px 0;

    .game_swiper_head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 20px 0;

        .s_left {
            display: flex;
            align-items: center;
            gap: 10px;

            svg {
                font-size: 40px;
            }

            span {
                color: #98ABD0;
                font-size: 18px;
            }
        }

        .s_right {
            display: flex;
            align-items: center;
            gap: 10px;

            .btn {
                display: flex;
                align-items: center;
                gap: 10px;

                .btn_c {
                    width: 36px;
                    height: 36px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    background-color: #202431;
                    color: #fff;
                    font-size: 16px;
                    border-radius: 8px;
                    color: #95A0B6;
                }
            }
        }
    }
}

.mais_box {
    display: flex;
    align-items: center;
    gap: 10px;

    .mais_font {
        font-size: 18px;
        border: 1px solid #585E77;
        color: #585E77;
        border-radius: 8px;
        padding: 6px 16px;
        cursor: pointer;
    }

    .mais_font:hover {
        border: 1px solid #98ABD0 !important;
        color: #98ABD0;
    }

    .btn {
        display: flex;
        align-items: center;
        gap: 10px;
        justify-content: center;

        .btn_c {
            cursor: pointer;
            display: flex;
            align-items: center;
            padding: 6px;
            border: 1px solid #585E77;
            color: #fff;
            font-size: 16px;
            border-radius: 5px;
            color: #585E77;
        }

        .btn_c:hover {
            border: 1px solid #98ABD0 !important;
            color: #98ABD0;
        }
    }
}
</style>
    