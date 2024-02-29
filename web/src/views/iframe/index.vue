<template>
    <div class="index">
        <!-- <div class="if_head_box">
            <img src="../../assets/images/public/popover_return.png" alt="" @click="router.go(-1)">
        </div> -->
        <!-- <xuanfu @closeIframe="router.go(-1)"></xuanfu> -->
        <iframe :src="url" frameborder="0" class="if_box"></iframe>
    </div>
</template>
<script setup>
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRoute, useRouter } from "vue-router";
// import xuanfu from "@/components/xuanfu/xuanfu.vue"

const route = useRoute()
const router = useRouter()
const state = reactive({
    url: ''
});
state.url = route.query.src
</script>
<style  lang="scss" scoped>
.index {
    width: 100%;
    height: 100vh;

    .if_head_box {
        padding: 10px;
        background-color: var(--theme-background);

        img {
            width: 45px;
        }
    }

    .if_box {
        padding: 0;
        margin: 0;
        width: 100%;
        height: 100%;
    }
}
</style>
  