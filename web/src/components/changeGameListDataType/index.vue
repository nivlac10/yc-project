<template>
    <div class="changeGameListDataType">
        <div @click="changeIndex(index)" :class="{ for_box: true, active: index == activeIndex }"
            v-for="(item, index) in typeList" :key="item">

            <span>{{ item }}</span>
        </div>
    </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";

export default defineComponent({
    name: "changeGameListDataType",
    props:{
        gameListType:{
            type:Number
        }
    },
    setup(props, { emit }) {
        const store = useStore();
        const state = reactive({
            typeList: [
                "Todo", "Popular", "Topo"
            ],
            activeIndex:props.gameListType || 0
        });
        
        const changeIndex = (index) => {
            state.activeIndex = index
            emit("def", index)
        }
        return { ...toRefs(state), changeIndex };
    },
});
</script>
<style  lang="scss" scoped>
.changeGameListDataType {
    display: flex;
    gap: 20px;
    padding: 5px 0;

    .for_box {
        color: var(--auxiliary-font-color-9);
        padding: 10px 20px;
        border-radius: 100px;
        cursor: pointer;

        &.active {
            color: #fff;
            background-color: var(--auxiliary-background-18);
        }
    }
}
</style>
  