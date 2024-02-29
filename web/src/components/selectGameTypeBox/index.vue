<template>
    <div class="selectBox">
        <div class="select_box_column">
            <input :class="{ active: selectActive }" type="text" :value="input" readonly @focus="inputFocus"
                :placeholder="(props.options as any)[0].label" @blur="inputBlur" />
            <div class="icon">
                <van-icon :class="{ active: selectActive }" name="arrow-left" />
            </div>
        </div>
        <ul :class="{ active: selectActive }">
            <li :class="{ active: selectIdx == index }" v-for="(item, index) in (props.options as any)" :key="index"
                @click.stop="selectChange(item, index)">
                {{ item.label }}
            </li>
        </ul>
    </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
export default defineComponent({
    name: "selectBox",
    props: {
        options: {
            type: Array
        }
    },
    setup(props, context) {
        const { proxy } = getCurrentInstance() as any;
        const router = useRouter();
        const store = useStore();
        const state = reactive({
            input: "",
            selectIdx: 0,
            selectActive: false,
        });
        const inputFocus = () => {
            state.selectActive = true;
        };
        const inputBlur = () => {
            setTimeout(() => {
                state.selectActive = false;
            }, 150);
        };
        const selectChange = (item, index: number) => {
            state.input = item.label;
            state.selectIdx = index;
            context.emit('selectChange', item)
        };

        return { ...toRefs(state), store, props, inputFocus, inputBlur, selectChange };
    },
});
</script>
<style  lang="scss" scoped>
.selectBox {
    position: relative;
    height: 100%;

    .select_box_column {
        // position: relative;
        // z-index: 201;
        height: 100%;

        input {
            cursor: pointer;
            padding: 0 24px;
            width: 100%;
            height: 100%;
            box-sizing: border-box;
            border: 1px solid #58657C;
            border-radius: 8px;
            color: #98ABD0;
            // background: transparent;
            background-color: #1B1F29 !important;

            // &.active {
            //     border-color: var(--theme-input-focus-border-color);
            // }   
            &::placeholder {
                color: #58657C;
            }
        }

        .icon {
            position: absolute;
            top: 50%;
            right: 10px;
            transform: translate(-50%, -50%);

            :deep(.van-icon) {
                transform: rotate(270deg);
                color: var(--auxiliary-font-color-2);
                transition: 0.2s all ease;

                &.active {
                    transform: rotate(90deg);
                }
            }
        }
    }

    ul {
        display: none;
        position: absolute;
        transform: translateY(0px);
        right: 0;
        z-index: 200;
        padding: 10px 9px;
        box-sizing: border-box;
        background-color: var(--theme-button-background);
        min-width: 100%;
        border-radius: 8px;
        overflow: hidden;

        &.active {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        li {
            cursor: pointer;
            padding: 10px 0 10px 17px;
            // margin: 5px 0;
            // font-size: 16px;
            font-weight: 500;
            color: var(--auxiliary-font-color-9);
            box-sizing: border-box;
            border-radius: 8px;

            &.active {
                background: var(--auxiliary-background-15);
                // color: var(--auxiliary-font-color-11);
            }

            &:hover {
                background: var(--auxiliary-background-15);
            }
        }
    }
}

@media (max-width: 768px) {
    .selectBox {
        .select_box_column {
            input {
                padding: 0 15px;
                height: 30px;
                border-radius: 8px;
                font-size: 12px;
            }

            .icon {
                right: 0px;
                top: 40% !important;
            }
        }

        ul {
            padding: 10px 9px;
            border-radius: 0px 0px 8px 8px;

            li {
                cursor: pointer;
                padding: 5px 0 5px 9px;
                font-size: 12px;
                border-radius: 4px;
            }
        }
    }
}
</style>
  