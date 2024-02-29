<template>
  <div class="activities">
    <div class="content_box">
      <div class="title">{{ t('signIn.Regras') }}</div>
      <p>{{ t('supplyCrate.p1') }}</p>
      <p>{{ t('supplyCrate.p2') }}</p>
      <p>{{ t('supplyCrate.p3') }}</p>
      <p>{{ t('supplyCrate.p4') }}</p>
      <p>{{ t('supplyCrate.p5') }}</p>
      <ul>
        <li>{{ t('supplyCrate.p6', { data: store.state.conf.all_conf.platform['platform_url'] }) }}</li>
        <li>{{ t('supplyCrate.p7', { data: store.state.conf.all_conf.platform['platform_url'] }) }}</li>
        <li>{{ t('supplyCrate.p8', { data: store.state.conf.all_conf.platform['platform_url'] }) }}</li>
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
  margin-top: 26px;

  .content_box {
    background: #202330;
    border-radius: 24px;
    padding: 23px 28px;
    font-size: 20px;
    font-weight: 500;
    color: #C3CFD9;
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
