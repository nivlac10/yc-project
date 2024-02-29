<template>
    <div class="depositBonus">
        <div class="title">
            <img src="@/assets/images/sidebar/Deposit_Bonus_Selected.png" alt="">
            <p class="sl_font">BÔNUS DE DEPÓSITO</p>
        </div>
        <div class="break" @click="breakToHome">
            <img src="@/assets/images/public/arrow_right.png" alt="">
            <p>voltar</p>
        </div>

        <img src="@/assets/images/depositBonus/Bônus_de_depósito@2x.png" alt="" class="head">
        <div class="item" v-for="v in fontList">
            <div class="item_title">{{ v.title }}</div>
            <div class="item_title2" v-if="v?.title2">{{ v.title2 }}</div>
            <p v-for="val in v.fonts">{{ val }}</p>
            <p v-if="v?.fonts2" v-for="(val2, i) in v.fonts2" :style="i == 0 ? 'margin-top:20px' : ''">{{ val2 }}</p>
        </div>
    </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { getImageUrl } from "@/utils/baseFun";
export default defineComponent({
    name: "depositBonus",
    setup() {
        const { proxy } = getCurrentInstance() as any;
        const router = useRouter();
        const store = useStore();
        const state = reactive({
            fontList: [
                {
                    title: 'Distribuição de Bônus de Depósito',
                    fonts: [
                        `${store.state.conf.all_conf.platform['platform_title']} oferece bônus de depósito especial.`,
                        `É realmente uma chance perfeita para obter reais extra. Você pode tomar a decisão pelos usos de dinheiro. Por isso, aproveite esta chance a aumentar sua riqueza com o bônus oferecido por ${store.state.conf.all_conf.platform['platform_title']}.`
                    ]
                },
                {
                    title: 'Bônus de Boas-vindas+20%',
                    title2: 'Os novatos podem obter 20% valor de primeiro depósito como bônus',
                    fonts: [
                        'R$ 20 DEPOSITADO, R$ 4 DISTRIBUÍDO',
                        'R$ 50 DEPOSITADO, R$ 10 DISTRIBUÍDO',
                        'R$ 100 DEPOSITADO, R$ 20 DISTRIBUÍDO',
                        'R$ 200 DEPOSITADO, R$ 40 DISTRIBUÍDO',
                        'R$ 500 DEPOSITADO, R$ 100 DISTRIBUÍDO',
                        'R$ 1000 DEPOSITADO, R$ 200 DISTRIBUÍDO',
                        'R$ 1500 DEPOSITADO, R$ 300 DISTRIBUÍDO',
                        'R$ 3000 DEPOSITADO, R$ 600 DISTRIBUÍDO',
                        'R$ 5000 DEPOSITADO, R$ 800 DISTRIBUÍDO',
                    ],
                    fonts2: [
                        '1.  Valor de Depósito≥20 BRL',
                        'Bônus de Depósito=Valor de Depósito*20% (800BRL no máximo)',
                        'Valor de Aposta=(Valor de Depósito+Bônus de Depósito)*10 vezes',
                        '2. Apenas os novos usuários podem participar deste evento depois de fazer o primeiro depósito',
                        '3. Você pode decidir participar de evento ou não.',
                        'Se a decisão é não participar de evento [ Bônus de Boas-vindas+20% ] , Valor de Aposta=Valor de Depósito*1 vez',
                    ]
                },
                {
                    title: 'Valor de Primeiro Depósito Diário+10%',
                    title2: 'Fazer o depósito de valor determinado receberá 10% bônus extra. Cada um pode participar de evento de novo às 00:00 diariamente.',
                    fonts: [
                        'R$ 100 DEPOSITADO, R$ 10 DISTRIBUÍDO',
                        'R$ 200 DEPOSITADO, R$ 20 DISTRIBUÍDO',
                        'R$ 500 DEPOSITADO, R$ 50 DISTRIBUÍDO',
                        'R$ 1000 DEPOSITADO, R$ 100 DISTRIBUÍDO',
                        'R$ 1500 DEPOSITADO, R$ 150 DISTRIBUÍDO',
                        'R$ 3000 DEPOSITADO, R$ 300 DISTRIBUÍDO',
                        'R$ 5000 DEPOSITADO, R$ 500 DISTRIBUÍDO',
                    ],
                    fonts2: [
                        '1.  Valor de Depósito≥20 BRL',
                        'Bônus de Depósito=Valor de Depósito*10%',
                        'Valor de Aposta=(Valor de Depósito+Bônus de Depósito)*5 vezes',
                        '2. Cada usuário pode participar diariamente deste evento por uma vez e pode participar de novo às 00:00',
                        '3. Você pode decidir participar de evento ou não.',
                        'Se a decisão é não participar de evento [ Bônus de Boas-vindas+10% ], Valor de Aposta=Valor de Depósito*1 vez',
                    ]
                }
            ]
        });
        const { t } = useI18n();
        function getBouns() {
            if (store.state.user.token && store.state.user.token !== "") {
                store.state.status.depositShow = true;
            } else {
                store.dispatch('status/setLoginShow', true)
            }

        }
        const breakToHome = () => {
            router.push('/')
        }
        return { ...toRefs(state), store, t, getImageUrl, getBouns, breakToHome };
    },
});
</script>
<style  lang="scss" scoped>
p {
    margin: 0;
    white-space: pre-wrap;
}

.depositBonus {
    width: 100%;
    margin-top: 60px;

    .title {
        display: flex;
        align-items: center;


        p {
            font-size: 38px;
            font-weight: bold;
        }
    }

    .break {
        border-radius: 12px;
        background: #202330;
        width: 100%;
        height: 58px;
        margin-bottom: 32px;
        display: flex;
        align-items: center;
        cursor: pointer;

        img {
            transform: rotate(180deg) scale(0.6);
            margin-left: 10px;
        }

        p {
            color: #C3CFD9;
            font-size: 24px;
            font-weight: bold;
        }
    }

    .head {
        width: 100%;
        object-fit: cover;
        border-radius: 24px;
    }

    .item {
        width: calc(100% - 30px);
        padding: 36px 0 41px 30px;
        margin-top: 40px;
        margin-bottom: 40px;
        background: var(--theme-box-background);
        border-radius: 24px;

        .item_title {
            font-size: 32px;
            color: #F3B343;
            font-weight: bold;
            line-height: 37.5px;
            margin-bottom: 14px;
        }

        .item_title2 {
            color: #fff;
            font-size: 24px;
            line-height: 28px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        p {
            color: #C3CFD9;
            font-size: 24px;
            line-height: 36px;
            text-align: left;
            white-space: pre-wrap;
            font-weight: 500;
        }
    }
}

@media (max-width: 768px) {
    .depositBonus {
        margin-top: 13px;
        width: calc(100% - 40px);
        margin-left: 20px;

        .title {
            img {
                width: 44px !important;
            }

            p {
                font-size: 20px;
            }
        }

        .break {
            height: 32px;
            border-radius: 8px;

            img {
                width: 18px;
                transform: rotate(180deg) scale(1);
                margin-right: 10px;
            }

            p {
                font-size: 16px;
            }
        }

        .head {
            border-radius: 12px;
        }

        .item {
            width: calc(100% - 24px);
            padding: 15px 12px 16px 12px;
            border-radius: 12px;

            .item_title {
                font-size: 16px;
                line-height: 18px;
            }

            .item_title2 {
                font-size: 14px;
                line-height: 16.5px;
            }

            p {
                font-size: 12px;
                line-height: 18px;
            }
        }
    }
}
</style>
  