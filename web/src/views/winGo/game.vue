<template>
    <div class="main">
        <gameHead />
        <placeBet />
        <gameTable />
    </div>
</template>

<script>
import { reactive, toRefs } from 'vue'
import gameHead from './components/gameHead.vue';
import placeBet from './components/placeBet.vue';
import gameTable from './components/table.vue';
export default {
    components: { gameHead, placeBet, gameTable },
    setup() {
        const state = reactive({
            count: 0,
        })

        return {
            ...toRefs(state),
        }
    }
}
</script>

<style lang="scss">
.main {
    padding-top: 24px;
}

.greenBall {
    background: #40AD72;
}

.redBall {
    background: #FD565C;
}

.redToPurpleBall {
    background: linear-gradient(135deg, #FE575D 0%, #FE575D 50%, #B75AFF 50%, #B75AFF 100%);
}

.greenToPurpleBall {
    background: linear-gradient(135deg, #40AD72 0%, #40AD72 50%, #B659FE 50%, #B659FE 100%);
}

.redBallBg {
    background: rgba(253, 86, 92, 0.1);
    border: 0px solid rgba(253, 86, 92, 0.5);
}

.greenBallBg {
    border: 0px solid rgba(64, 173, 114, 0.5);
    background: rgba(64, 173, 114, 0.1);
}
</style>