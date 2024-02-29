<template>
    <div class="index">
        <van-notice-bar :text="text">
            <template #left-icon>
                <div class=left_icon>
                    <img src="@/assets/images/home/Notice@2x.png" alt="">
                </div>
            </template>
        </van-notice-bar>
    </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";

export default defineComponent({
    name: "indexNoticVant",
    setup() {
        const store = useStore();
        const state = reactive({
            text: ""
        });
        state.text = store.state.conf.all_conf.activity[0].title
        return { ...toRefs(state) };
    },
});
</script>
<style  lang="scss" scoped>
.index {}

.left_icon {
    // padding: 10px;
    padding-right: 8px;

    img {
        width: 40px;
        // height: 100%;
    }
}

:deep(.van-notice-bar) {
    border-radius: 8px;
    padding: 3px 10px;
    background: var(--theme-navigationbar-background);
    color: var(--auxiliary-font-color-5);
    font-weight: 600;
}
</style>
  