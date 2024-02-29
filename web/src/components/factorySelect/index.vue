<template>
    <!-- <div class="factory_list" @click="factoryShow = !factoryShow">
        <div style="cursor: pointer;">
            <img class="img1" src="@/assets/images/home/Select_supplier_icon@2x.png" alt="">
            <span>{{ factoryName }}</span>
        </div>
        <img class="img2" src="@/assets/images/header/arrow.png" alt="">
        <div class="factory_select" v-if="factoryShow">
            <div @click.stop="changeFactory(item), factoryIndex = index"
                :class="{ factory_select_box: true, active: factoryIndex == index }" v-for="(item, index) in factorList"
                :key="item.game_id + ''">
                <div>
                    {{ item.game_name }}
                </div>
            </div>
        </div>
    </div> -->

    <div class="demo-collapse">
        <el-collapse v-model="factoryName" accordion>
            <el-collapse-item title="Casion" name="1">
                <template #title>
                    <div class="select_box">
                        <div :class="{ selected_column: true, sl_box_showd_border: factoryShow }"
                            @click="factoryShow = !factoryShow">
                            <div class="l_box">
                                <img class="img1" src="@/assets/images/home/Select_supplier_icon@2x.png" alt="">
                                <span>{{ factorList[factoryIndex].game_name }}</span>
                            </div>
                        </div>
                    </div>
                </template>
                <div class="list">
                    <div class="tab_list">
                        <ul>
                            <li v-for="(item, index) in factorList" :key="index"
                                :class="{ active_tab: factoryIndex == index }"
                                @click="changeFactory(item), factoryName = item.game_name, factoryIndex = index">
                                <!-- <img :src="item.img" alt="" /> -->
                                <span>{{
                                    item.game_name
                                }}</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent ,computed} from "vue";
import { useStore } from "@/store/index";
import { get_factory_list } from "@/utils/gameUtils";

export default defineComponent({
    name: "indexFactorySelect",
    props: {
        maker_name: {
            type: String,
            default: 'Escolher Fornecedores'
        }
    },
    setup(props, { emit }) {
        const store = useStore();
        const Props= computed(()=> props);
        const state = reactive({
            factoryName: "Escolher Fornecedores",
            factoryShow: false,
            factoryIndex: 0,
            factorList: [
                {
                    game_name: "Escolher Fornecedores",
                    game_id: null,
                }
            ],
        });
        state.factoryName = Props.value?.['maker_name']  ?? "Escolher Fornecedores";

        let factory_list = get_factory_list();

        for (let i = 0; i < factory_list.length; i++) {
            let item = factory_list[i];
            if ( Props.value?.['maker_name']) {
                if (item.game_name == Props.value?.['maker_name']) {
                    state.factoryIndex = i+1;
                }
            }
            state.factorList.push(factory_list[i])
        }
        // 切换厂商
        const changeFactory = (item) => {
            state.factoryName = item.game_name;
            state.factoryShow = false;
            emit("def", item)
        }
        return { ...toRefs(state), changeFactory };
    },
});
</script>
<style  lang="scss" scoped>
.demo-collapse {
    // margin-bottom: 12px;
    height: 100%;

    :deep(.el-collapse) {
        border: none;
        background: var(--theme-navigationbar-background);
        border-radius: 8px;
        height: 100%;

        .el-collapse-item__header {
            height: 42px;
            background: transparent;
            border: none;
            font-size: 18px;
            color: var(--theme-font-color-fff);
            align-items: center;

            .el-collapse-item__arrow {
                font-size: 20px;
                font-weight: bold;
                color: var(--auxiliary-font-color-1);
            }
        }

        .el-collapse-item__wrap {
            background: transparent;
            border: none;
        }
    }

    :deep(.el-collapse-item__content) {
        padding-bottom: 0 !important;
        overflow: inherit;
    }

    :deep(.el-collapse-item__wrap) {
        overflow: inherit !important;
    }

    @media (max-width:750px) {
        .tab_list {
            position: relative !important;
            z-index: 1000;
            background-color: var(--theme-button-background);
            margin-top: 10px;
            border-radius: 8px;
            width: 100% !important;
        }
    }

    .list {
        position: relative;
        //     z-index: 10000;
    }

    .tab_list {
        position: absolute;
        z-index: 100000;
        background-color: var(--theme-button-background);
        margin-top: 10px;
        border-radius: 8px;
        width: 100%;
        // min-width: 212.5px;
        // width: 287.5px;

        ul {
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 5px;

            li {
                display: flex;
                align-items: center;
                // width: 100%;
                border-radius: 8px;
                padding: 5px 20px;
                gap: 10px;

                &.active_tab {
                    background-color: var(--theme-box-background);
                }

                img {
                    // margin-right: 9px;
                    // width: 40px;
                    width: 30px;
                }

                span {
                    color: var(--auxiliary-font-color-9);
                }
            }
        }
    }
}



.select_box {
    width: 100%;
    border-radius: 8px;

    .selected_column {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 14px;
        // background: var(--auxiliary-background-6);
        border-radius: 8px;
        height: 100%;
        width: calc(100% - 4px);

        &.active {
            border: 2px solid #fff;
        }

        .l_box {
            display: flex;
            align-items: center;
            height: 42px;
            gap: 10px;

            img {
                width: 30px;
            }

            span {
                font-size: 14px;
                font-weight: 500;
                // margin-bottom: -3px;
            }
        }

    }
}
</style>
  