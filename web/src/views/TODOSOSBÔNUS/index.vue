<template>
    <div class="TodosOsBouns">
        <div class="title">
            <img src="@/assets/images/TODOSOSBÔNUS/All_bonuses@2x.png" alt="">
            <p class="sl_font">{{ t('sidebar.TodososBônus') }}</p>
        </div>
        <div class="body">
            <div class="item" v-for="(v, i) in data" @click="jumpActivitySubpage(i)">
                <div class="itemTop">
                    <el-image :src="v.img_url" :fit="'fill'" lazy style="width: 100%; height: 100%;">
                        <template #error>
                            <div class="image-slot">
                                <img src="@/assets/images/TODOSOSBÔNUS/imgErr.png" alt="">
                            </div>
                        </template>
                    </el-image>
                </div>
                <div class="itemBottom">
                    {{ v.title }}
                </div>

            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";

const store = useStore();
const router = useRouter();
const { t } = useI18n();

let data = computed(() => store.state.conf.all_conf.activity);

const jumpActivitySubpage = (i) => {
    store.state.status.ActivitySubpageDataIndex = i;
    router.push(
        {
            name: 'ActivitySubpage',
            params: { i: i }
        }

    )
}
</script>

<style lang="scss" scoped>
.image-slot {

    img {
        width: 90px;
    }
}

.TodosOsBouns {
    .title {
        display: flex;
        align-items: center;
        margin: 28px 0;

        img {
            width: 84px;
        }

        p {
            font-size: 38px;
            font-weight: bold;
        }
    }

    .titleList {
        display: flex;
    }

    .body {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        column-gap: 16px;
        row-gap: 16px;
        margin-bottom: 40px;

        .item {
            width: 100%;

            .itemTop {
                height: 158px;
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                background: #272937;
                border-radius: 14px 14px 0 0;
                overflow: hidden;
            }

            .itemBottom {
                height: 80px;
                width: 100%;
                background: #181F2B;
                border-radius: 0 0 14px 14px;
                padding: 0 10px 0 10px;
                font-size: 19px;
                font-weight: bold;
                color: #fff;
                line-height: 22.27px;
                display: flex;
                align-items: center;
                box-sizing: border-box;
            }
        }
    }
}

@media (max-width: 768px) {
    .image-slot {}

    .TodosOsBouns {
        padding: 0 20px 0 20px;
        box-sizing: border-box;

        .title {
            img {
                display: none;
            }

            p {
                font-size: 20px;
            }
        }

        .body {
            grid-template-columns: repeat(1, 1fr);

            .item {
                .itemTop {
                    height: 138px;
                }

                .itemBottom {
                    height: 62px;
                    font-size: 16px;
                }
            }

        }
    }
}
</style>