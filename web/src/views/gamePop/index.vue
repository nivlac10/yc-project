<template>
    <div class="login_max_box">
        <el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
            :destroy-on-close="true" :lock-scroll="false" :width="store.state.status.isPc ? '908px' : '100%'">
            <div class="gameOutBox">
                <div class="gameOutBoxHead">
                    <span>{{ t('gameText.TodosOsJogos') }}</span>
                    <div @click="store.state.status.allGameShow = false">
                        <img src="@/assets/images/public/Shutdownx.png" alt="">
                    </div>
                </div>
                <allGameBox class="allGameBox" :game_id="store.state.status.game_id"></allGameBox>
            </div>
        </el-dialog>
    </div>
</template>
<script lang="ts">
import {
    reactive,
    toRefs,
    getCurrentInstance,
    defineComponent,
    ref,
    watch,
} from "vue";
import { useStore } from "@/store/index";
import allGameBox from "@/components/allGameBox/index.vue"
import { useI18n } from "vue-i18n";
export default defineComponent({
    name: "index",
    components: {
        allGameBox,
    },
    setup() {
        const store = useStore();
        const { t } = useI18n();
        const state = reactive({
            dialogVisible: true,
        });
        return {
            ...toRefs(state),
            store,
            t,
        };
    },
});
</script>
<style  lang="scss" scoped>
.gameOutBox {
    gap: 30px;
    padding: 30px;
    box-sizing: border-box;
}

// :deep(.gamePopCss) {
//     overflow-y: scroll;
//     height: 60vh;
// }

.gameOutBoxHead {
    display: flex;
    justify-content: space-between;

    span {
        font-size: 24px;
        color: #fff;
        font-weight: 600;
    }

    img {
        width: 20px;
        height: 20px;
    }
}

@media screen and (max-width: 768px) {
    .gameOutBox {
        width: 100%;
        padding: 15px;
        background: #202431;
    }
}
</style>
    