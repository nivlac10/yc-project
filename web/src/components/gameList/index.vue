<template>
    <div>
        <div class="index" v-if="props.gameList.length > 0">
            <div class="gameBox">
                <gameBox v-for="v in props.gameList" :data="v">
                </gameBox>
            </div>
            <div class="loadMore">
                <div v-if="allCount > 0" class="progress_bar">
                    <div class="progress_bar_box">
                        <div>{{ props.gameList.length }}/{{ props.count }}</div>
                        <div class="progress">
                            <div class="progress_item" :style="`width:${progress_width}%;`"></div>
                        </div>
                        <div>{{ progress_bar_percentage }}%</div>
                    </div>
                    <div class="progress_bar_btn" @click="loadMore()" v-if="props.gameList.length != props.count">
                        <p class="progress_bar_btn_p" v-if="!load">
                            {{ t('btnName.CarregarMais') }}
                        </p>
                        <div class="progress_bar_lod" v-if="load">
                            <div class="progress_bar_lod_item"></div>
                            <div class="progress_bar_lod_item"></div>
                            <div class="progress_bar_lod_item"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="np_data" v-else>
            <span>{{ t('noData.SemData') }}</span>
        </div>
    </div>
</template>
<script>
import { reactive, toRefs, getCurrentInstance, defineComponent, watch } from "vue";
import { useStore } from "@/store/index";
import { useRouter, useRoute } from "vue-router";
import gameBox from "@/views/home/components/gameBox.vue"
import { useI18n } from "vue-i18n";

export default defineComponent({
    name: "indexGameList",
    components: {
        gameBox
    },
    props: {
        gameList: {
            type: Array
        },
        count: {

        }
    },
    setup(props, { emit }) {
        const store = useStore();
        const route = useRoute();
        const { t, locale } = useI18n();

        const state = reactive({
            allCount: props.count,
            gameListCount: props.gameList.length,
            progress_bar_percentage: 0,
            //底部按钮是否加载
            load: false,
            //百分比进度条
            progress_width: 0,
        });
        count_progress_bar();
        state.percentage = (state.gameListCount / state.allCount * 100).toFixed(2)
        const loadMore = () => {
            state.load = true
            setTimeout(() => {
                emit("def")
                count_progress_bar();
                state.load = false
            }, 500);
        }
        // 监听
        watch(() => props.gameList, (newData, oldData) => {
            state.load = true
            count_progress_bar();
            state.load = false
        })
        console.log(props.gameList.length);
        //获取百分百
        function count_progress_bar() {
            state.progress_width = (props.gameList.length / props.count) * 100;
            state.progress_bar_percentage = Math.round(state.progress_width);
        }
        return { ...toRefs(state), t, loadMore, props };
    },
});
</script>
<style  lang="scss" scoped>
.np_data {
    width: 100%;

    // background-color: #202431;
    border-radius: 16px 16px 16px 16px;
    height: 50vh;
    display: flex;
    justify-content: center;
    align-items: center;

    span {
        color: #98ABD0;
        font-size: 18px;
    }
}

.loadMore {
    // display: flex;
    // justify-content: center;
    // flex-direction: column;
    margin-top: 36px;

    .percentage {
        // display: flex;
        width: 500px;
    }
}

.gameBox {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    // column-gap: 10px;
    row-gap: 12px;
    column-gap: 12px;
    // margin-top: 30px;
    // margin-bottom: 44px;
}

.progress_bar {
    // margin-top: 0.4rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 36px;
}

.progress_bar_btn {
    background-color: #2F3445;
    border-radius: 8px;
    width: 146px;
    height: 42px;
    // padding: 12px 18px;
    display: flex;
    align-items: center;
    cursor: pointer;
    justify-content: center;

    .progress_bar_btn_p {
        font-size: 16px;
        color: #fff;
    }
}

.progress {
    width: 72px;
    height: 5px;
    border-radius: 16px;
    background: rgb(255, 255, 255);
    margin: 0rem 5px;
    overflow: hidden;
}

.progress_bar_box {
    display: flex;
    -webkit-box-pack: center;
    justify-content: center;
    -webkit-box-align: center;
    align-items: center;
    font-weight: normal;
    font-size: 14px;
    // line-height: 20;
    gap: 9px;
    color: rgb(255, 255, 255);
}

.progress_item {
    height: 5px;
    border-radius: 16px;

    background: #4181EE;
}

.progress_bar_lod {
    // height: 40px;
    margin: 0px auto;
    display: flex;
    -webkit-box-pack: center;
    justify-content: center;
    -webkit-box-align: center;
    align-items: center;
    gap: 10px;

    .progress_bar_lod_item {
        width: 4px;
        height: 4px;
        border-radius: 2px;
        margin: 0px 0.03rem;
        background: #4181EE;
        animation: 1.2s ease 0s infinite normal none running breathe;
    }

    .progress_bar_lod_item:nth-of-type(2) {
        animation-delay: 0.4s;
    }

    .progress_bar_lod_item:nth-of-type(3) {
        animation-delay: 0.8s;
    }
}

@-webkit-keyframes breathe {

    0%,
    to {
        opacity: 0.2;
    }

    50% {
        opacity: 0.8;
    }
}

@keyframes breathe {

    0%,
    to {
        opacity: 0.2;
    }

    50% {
        opacity: 0.8;
    }
}

@media (max-width: 750px) {
    .gameBox {
        grid-template-columns: repeat(3, 1fr);
        column-gap: 10px;
        row-gap: 10px;
    }


    .np_data {
        width: 100%;

        // background-color: #202431;
        border-radius: 8px;
        height: 50vh;
        display: flex;
        justify-content: center;
        align-items: center;

        span {
            color: #98ABD0;
            font-size: 14px;
        }
    }


}
</style>
  