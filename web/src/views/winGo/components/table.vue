<template>
    <div class="table">
        <div class="btns">
            <div class="active">
                Histórico do jogo
            </div>
            <div>Gráfico </div>
            <div>Meu histórico </div>
        </div>
        <div class="tabular">
            <div class="tableHead">
                <p>Período</p>
                <p>Número</p>
                <p>Grande Pequeno</p>
                <p>Cor</p>
            </div>
            <div class="tableItem" v-for="v in data">
                v
            </div>
        </div>
    </div>
</template>

<script>
import { reactive, toRefs } from 'vue'

export default {
    setup() {
        const state = reactive({
            count: 0,
            data: [{ Período: 20231215010729, Número: 8, GrandePequeno: 1, Cor: 4 },{ Período: 20231215010729, Número: 8, GrandePequeno: 1, Cor: 4 }]
        })

        return {
            ...toRefs(state),
        }
    }
}
</script>

<style lang="scss" scoped>
%center {
    display: flex;
    justify-content: center;
    align-items: center;
}

%tableFlex{
    display: grid;
}

.table {
    width: 100%;
    margin-top: 36px;

    .btns {
        width: 100%;
        margin-bottom: 24px;
        display: flex;
        gap: 12px;

        div {
            padding: 17.5px 15px;
            background: #2D3144;
            color: #BCBDC1;
            font-size: 16px;
            @extend %center;
            border-radius: 8px;
        }

        .active {
            color: #FFFFFF;
            background: rgba(65, 129, 238, 0.5);
            border: 2px solid rgba(65, 129, 238, 0.8);
        }

    }

    .tabular {
        width: 100%;
        display: flex;
        flex-direction: column;
        .tableHead{
            @extend %tableFlex;
            grid-template-columns: repeat(4,25%);
            justify-items: center;
            p{
                color: #FFFFFF;
                font-size: 16px;
            }
          
        }
    }
}
</style>