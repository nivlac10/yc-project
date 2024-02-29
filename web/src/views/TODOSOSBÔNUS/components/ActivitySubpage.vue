<template>
    <div class="ActivitySubpage">
        <div class="break" @click="breakToHome">
            <img src="@/assets/images/public/arrow_right.png" alt="">
            <p>voltar</p>
        </div>
        <div class="img">
            <el-image :src="data.img_url" :fit="'fill'" lazy style="width: 100%; height: 100%; ">
                <template #error>
                    <div class="image-slot">
                        <img src="@/assets/images/TODOSOSBÔNUS/imgErr.png" alt="">
                    </div>
                </template>
            </el-image>
        </div>
        <div class="info_box">
            <span style="color: #fff;">➡️ Telegram: </span>
            <a style="color: rgb(66, 144, 247);" :href="store.state.conf.all_conf.tg_channel_url" target="_blanl">{{
                store.state.conf.all_conf.tg_channel_url }}</a>

        </div>
        <div class="info_box">
            <p class="title sl_font">{{ data.title }}</p>
            <div class="font" v-html="data.info"></div>
            <div class="btnBox">
                <div v-show="data.type !== 0" @click="jumpRoute(data)" class="sl_box_shadow btn">{{ data.button_name
                }}</div>
            </div>
        </div>


    </div>
</template>

<script setup>
import { reactive, ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { jumpRoute } from "@/utils/pageUtile";

const router = useRouter();
const route = useRoute();
const store = useStore();

let index = route.params.i;
let data = computed(() => store.state.conf.all_conf.activity[index]);

const breakToHome = () => {
    router.back(-1);
}
</script>

<style lang="scss" scoped>
.info_box {
    margin-top: 20px;
    background-color: #202330;
    padding: 30px 20px;
    border-radius: 10px;
}

.image-slot {

    img {
        width: 90px;
    }
}

.ActivitySubpage {
    margin-bottom: 40px;

    .img {
        width: 100%;
        height: 500px;
        border-radius: 10px;
        overflow: hidden;
    }

    .break {
        border-radius: 12px;
        background: #202330;
        width: 100%;
        height: 58px;
        margin-top: 35px;
        margin-bottom: 32px;
        display: flex;
        align-items: center;
        cursor: pointer;

        img {
            transform: rotate(180deg) scale(0.6);
            margin-left: 10px;
        }

        p {
            color: #C3CFD9;
            font-size: 24px;
            font-weight: bold;
        }
    }

    .title {
        font-size: 42px;
        line-height: 49.22px;
        font-weight: Bold;
        // margin-top: 40px;
        margin-bottom: 23px;
    }

    .font {
        white-space: break-spaces;
        color: #fff;
        font-size: 20px;
        line-height: 36px;


    }

    .btnBox {
        width: 100%;
        display: flex;
        justify-content: center;

        .btn {
            padding: 10px 25px;
            margin-top: 20px;
            font-size: 24px;
            font-weight: 550;
        }
    }



}

:deep(.min_title) {
    font-size: 24px;
    font-weight: bold;
}

@media (max-width: 768px) {
    .ActivitySubpage {
        padding: 0 20px 0 20px;

        .img {
            height: 139.58px;
            border-radius: 12px;
            overflow: hidden;
        }

        .break {
            height: 32px;
            border-radius: 8px;

            img {
                width: 18px;
                transform: rotate(180deg) scale(1);
                margin-right: 10px;
            }

            p {
                font-size: 16px;
            }
        }

        .title {
            font-size: 20px;
        }

        :deep(.min_title) {
            font-size: 14px;
            font-weight: bold;
        }

        .font {
            font-size: 12px;
        }
    }
}
</style>
