<template>
  <div class="settings">
    <div class="settings_box">
      <div class="settings_title">{{ t('account.ConfiguraçãoDeEMail') }}</div>
      <set-email />
    </div>
    <div class="settings_box">
      <div class="settings_title">{{ t('account.ConfiguraçãoDoTelefone') }}</div>
      <set-phone />
    </div>
    <div class="settings_box">
      <div class="settings_title">{{ t('account.ConfiguraçãoDaSenha') }}</div>
      <set-password />
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { copy, getImageUrl, levelPercent } from "@/utils/baseFun";
import setPassword from "./setPassword.vue";
import setPhone from "./setPhone.vue";
import setEmail from "./setEmail.vue";
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "settings",
  components: { setPassword, setPhone, setEmail },
  setup() {
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const { proxy } = getCurrentInstance() as any;
    const state = reactive({
    });
    return {
      ...toRefs(state),
      store,
      t,
      getImageUrl,
    };
  },
});
</script>
<style  lang="scss" scoped>
.settings {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;

  .settings_box {
    width: 400px;
    flex-shrink: 0;

    .settings_title {
      margin-bottom: 12px;
      font-size: 16px;
      color: #98ABD0;
    }
  }
}

@media (max-width: 768px) {
  .settings {
    flex-direction: column;
    gap: 12px;

    .settings_box {
      width: 100%;
      flex-shrink: 0;

      .settings_title {
        font-size: 14px;
      }
    }
  }
}
</style>
