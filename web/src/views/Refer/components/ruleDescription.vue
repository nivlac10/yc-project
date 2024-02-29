<template>
  <div class="ruleDescription">
    <div class="title">Descrição das regras</div>
    <div class="information">
      Cada membros que você convida, completar o primeiro depósito, você pode
      obter R$8.00 a 35.00. Quando você cumpre as condições do V2 e acima,
      Contacte seu serviço exclusivo de clientes para atualizar nível. Seu
      serviço exclusivo de clientes lhe dará alguns comissãos como
      recompensa.(Com base no número de invitado, número de depósito, valor de
      apostas válidas)
    </div>
    <div class="table_header">
      <div>Nível</div>
      <div>Número de Depósito</div>
      <div>Comissões de Primeiro Depósitos</div>
      <!-- <div>TOTAL BONUS</div> -->
    </div>
    <div class="list">
      <ul>
        <li
          v-for="(item, index) in all_conf.invite_recharge_bonus_list"
          :key="index"
        >
          <div>
            <img :src="item.img" alt="" />
            <span>LEVEL{{ item.lv }}</span>
          </div>
          <div>{{ item.number }} <span></span></div>
          <div>{{ item.commission }} BRL</div>
          <!-- <div>{{ item.number * item.commission }} BRL</div> -->
        </li>
      </ul>
    </div>
  </div>
</template> 
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { getImageUrl } from "@/utils/baseFun";
export default defineComponent({
  name: "ruleDescription",
  components: {},
  setup(props) {
    // route 配置
    const route = useRoute();
    // router 配置
    const router = useRouter();
    const store = useStore();

    const state = reactive({});

    const all_conf = store.state.conf.all_conf;

    for (let i = 0; i < all_conf.invite_recharge_bonus_list.length; i++) {
      all_conf.invite_recharge_bonus_list[i].img = getImageUrl(
        `refer/level_${i + 1}.png`
      );
    }
    //  变量
    return { ...toRefs(state), all_conf, getImageUrl };
  },
});
</script>
<style  lang="scss" scoped>
div {
  display: flex;
}

.ruleDescription {
  padding: 30px 20px 53px 20px;
  flex-direction: column;
  border-radius: 28px;
  background: var(--theme-menu-background-color);

  .title {
    font-weight: 500;
    font-size: 30px;
    color: #fff15b;
    line-height: 42px;
  }

  .information {
    padding: 20px 0 60px 0;
    width: 70%;
    font-size: 18px;
    color: var(--auxiliary-font-color-9);
    font-weight: 500;
    line-height: 26px;
  }

  .table_header {
    display: flex;
    margin-bottom: 25px;

    div {
      display: flex;
      justify-content: center;
      width: 100%;
      font-size: 18px;
      color: var(--auxiliary-font-color-9);
      font-weight: 500;
    }
  }

  .list {
    width: 100%;

    ul {
      width: 100%;

      li {
        display: flex;
        margin-bottom: 10px;
        align-items: center;
        padding: 8px 15px;
        background: #232c3a;
        border-radius: 13px;
        div {
          display: flex;
          justify-content: center;
          align-items: center;
          width: 100%;
          align-items: center;
          color: #ffffff;
          font-size: 16px;
          font-weight: 500;
        }
        div:nth-child(1) {
          img {
            width: 51px;
            margin-right: 5px;
          }
        }
        div:nth-child(2) {
          span {
            margin-left: 10px;
            color: #a4a5b5;
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .ruleDescription {
    .title {
      line-height: 10px;
      font-size: 18px;
    }

    .information {
      padding: 20px 0 20px 0;
      width: 100%;
      font-size: 16px;
      line-height: 18px;
    }

    .table_header {
      margin-bottom: 10px;

      div {
        font-size: 14px;
      }
    }

    .list {
      ul {
        li {
          padding: 5px 5px;

          div {
            font-size: 12px;
          }
        }
      }
    }
  }
}
</style>
    