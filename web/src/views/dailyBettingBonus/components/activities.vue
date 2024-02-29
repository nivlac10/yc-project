<template>
  <div class="activities">
    <div class="content_box">
      <div class="title">Regras</div>
      <p>1.Você pode retirar o bônus sem fluxo de transação.</p>
      <p>2.Você pode receber o bônus apenas que os valores apostados acumulativos do dia sejam válidos e atinjam o valor
        determinado</p>
      <p>3.A aposta válida é apenas desigada para todos os jogos de caça-níqueis.</p>
      <p>4.Clique no botão de【Receber】para receber o bônus. Se o bônus daquele dia não foi recebido dentro de prazo, é
        considerado abandonar o bônus</p>
      <p>5.Tempo de Calculação: 00:00-23:59:59 (Tempo de Brasília). Recalcule no dia seguinte.</p>
      <ul>
        <li>
          {{store.state.conf.all_conf.platform['platform_url']}} tem o direito de congelar temporariamente a conta se algum comportamento anormal do membro for
          encontrado durante o evento, e o bônus será enviado quando não há resultado anormal para a investigação
        </li>
        <li>
          As participações de evento dos membros são contadas automaticamente pelo sistema. Se houver alguma dúvida, o
          resultado da consulta de {{store.state.conf.all_conf.platform['platform_url']}} prevalecerá
        </li>
        <li>
          {{store.state.conf.all_conf.platform['platform_url']}} reserva-se o direito de alterar o evento
        </li>
      </ul>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "activities",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
    });

    return { ...toRefs(state), store, t };
  },
});
</script>
<style  lang="scss" scoped>
.activities {
  .content_box {
    background: #202330;
    border-radius: 24px;
    padding: 23px 28px;
    font-size: 20px;
    font-weight: 500;
    color: #FFFFFF;
    line-height: 30px;

    .title {
      margin-bottom: 10px;
      font-size: 22px;
      font-weight: bold;
      color: #DEA541;
    }

    ul {
      padding: 20px 0 0 22px;

      li {
        list-style: disc;
      }
    }
  }
}

@media (max-width: 768px) {
  .activities {
    .content_box {
      border-radius: 8px;
      padding: 16px 12px;
      font-size: 12px;
      line-height: 18px;

      ul {
        padding: 10px 0 0 18px;
      }
    }
  }
}
</style>
