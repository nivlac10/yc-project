<template>
    <div class="search_box">
        <img src="@assets/images/home/search_icon.png" alt="" />
        <input type="text" :placeholder="t('placeholder.Procurarjogos')" v-model="gameName" class="seacrh_input"
            @input="changeGameName(gameName)">
    </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";

export default defineComponent({
    name: "indexSearchGameName",
    setup(props, { emit }) {
        const store = useStore();
        const { t, locale } = useI18n();
        const state = reactive({ gameName: null });
        const changeGameName = (v) => {
            if (v) {
                v = v
            } else {
                v = null
            }
            emit("def", v)
        }
        return { ...toRefs(state), t, changeGameName };
    },
});
</script>
<style  lang="scss" scoped>
.search_box {
    border-radius: 8px;
    // min-height: 42px;
    // height: 44px;
    max-height: 44px;
    border: 1.3px solid #58657C;
    display: flex;
    background-color: #202431 !important;
    align-items: center;

    img {
        padding: 0 12px;
        width: 28px;
        height: 28px;
    }

    .seacrh_input {
        // height: 100%;
        border: none;
        background-color: rgba($color: #000000, $alpha: 0.0);
        color: #fff;
        font-size: 14px;
        width: 100%;

    }


}

@media (max-width: 750px) {
    .search_box {
        width: 100%;
        height: 32px !important;
        border: none;
        background-color: #202431;
        border-radius: 6px;

        img {
            width: 24px;
            height: 24px;
        }

        .seacrh_input {
            // height: 100%;
            border: none;
            background-color: rgba($color: #000000, $alpha: 0.0);
            color: #fff;
            font-size: 12px;


        }
    }

}

input::-webkit-input-placeholder {
    /* WebKit browsers */

    color: #58657C;

}

input:-moz-placeholder {
    /* Mozilla Firefox 4 to 18 */

    color: #58657C;

}

input::-moz-placeholder {
    /* Mozilla Firefox 19+ */

    color: #58657C;

}

input:-ms-input-placeholder {
    /* Internet Explorer 10+ */

    color: #58657C;

}
</style>
  