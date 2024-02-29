<template>
    <div class="spinPop">
        <img src="@/assets/images/spin/Colouredribbon.png" alt="" class="topImg">
        <img src="@/assets/images/spin/purse.png" alt="" class="topImg2">
        <img src="@/assets/images/spin/Halo.png" alt="" class="topImg3">
        <span>VOCÊ VENCEU</span>
        <p>R$ 50,00</p>
        <div class="btn" @click="close">Registre-se e reivindique</div>
    </div>
</template>

<script setup>
const emit = defineEmits(['close'])

const close = () => {
    emit('close')
}
</script>

<style lang="scss" scoped>
.spinPop {
    position: relative;
    background: #17181B;
    width: 551px;
    height: 266px;
    padding-top: 103px;
    display: flex;
    flex-direction: column;
    align-items: center;

    .topImg {
        position: absolute;
        top: -60%;
        left: 6%;
        width: 492px;
        -webkit-animation: drawnfloat-s1mafayd 2s infinite both;
        animation: drawnfloat-s1mafayd 2s infinite both;


    }

    .topImg2 {
        width: 258px;
        position: absolute;
        top: 0;
        left: calc(50% - 129px);
        transform: translateY(-70%);
        z-index: 2;
    }

    .topImg3 {
        width: 100%;
        position: absolute;
        transform: translateY(-50%);
        top: 0;
        left: 0;
    }

    span {
        font-size: 41px;
        color: #fff;
        font-weight: 600;
        text-align: center;
        margin-bottom: 29px;
    }

    p {
        color: #65BE3D;
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 12px;
    }

    .btn {
        width: 365px;
        height: 136px;
        background: url('@/assets/images/spin/Yellowbutton.png');
        background-size: 100% 100%;
        font-size: 22px;
        font-weight: 600;
        color: #000000;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
    }
}

@media (max-width:768px) {

    .spinPop {
        width: 351px;
        height: 200px;
        padding-top: 42px;

        .topImg {
            top: -77%;
            left: 6%;
            width: 312px
        }

        .topImg2 {
            width: 164px;
            left: calc(50% - 82px);
        }

        span {
            font-size: 28px;
            margin-top: 17px;
            margin-bottom: 13px;
        }

        p {
            font-size: 32px
        }

        .btn {
            width: 263px;
            height: 86px;
            font-size: 14px;
        }
    }
}

@-webkit-keyframes drawnfloat-s1mafayd {
    0% {
        top: -77%
    }

    50% {
        top: -79%
    }

    to {
        top: -77%
    }
}

@keyframes drawnfloat-s1mafayd {
    0% {
        top: -77%
    }

    50% {
        top: -79%
    }

    to {
        top: -77%
    }
}</style>    