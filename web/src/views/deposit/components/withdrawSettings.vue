<template>
  <div class="withdrawSettings">
    <div class="withdrawSettings_header">
      <img src="@assets/images/public/popover_return.png" alt="" @click="settings" />
      <div class="title">{{ t('deposit.WITHDRAWALSETTINGS') }}</div>
      <img src="@assets/images/public/popover_error_icon.png" alt="" @click="closeBtn" />
    </div>
    <div class="form_title">*Tipo de PIX</div>
    <el-form class="el-form_style" ref="formRef" :model="validateForm" :rules="rules">
      <el-form-item label="" prop="pix">
        <div class="input_box">
          <el-select v-model="validateForm.pix" placeholder="">
            <el-option v-for="(item, index) in typeList" :key="index" :label="item" :value="item" />
          </el-select>
        </div>
      </el-form-item>
      <el-form-item label="" prop="name">
        <div class="input_box">
          <el-input v-model="validateForm.name" :placeholder="t('refer.Nome')" autocomplete="off" />
        </div>
      </el-form-item>
      <el-form-item label="" prop="cpf">
        <div class="input_box">
          <el-input v-model="validateForm.cpf" placeholder="CPF" autocomplete="off" />
        </div>
      </el-form-item>
      <!-- <el-form-item label="" prop="pix_num">
        <div class="input_box">
          <el-input v-model="validateForm.pix_num" placeholder="PIX" autocomplete="off" />
        </div>
      </el-form-item> -->
      <!-- <el-form-item>
        <el-button type="primary" @click="submitForm(formRef)">Submit</el-button>
        <el-button @click="resetForm(formRef)">Reset</el-button>
      </el-form-item> -->
    </el-form>
    <div class="submit_btn" @click="submitForm(formRef)">{{ t('base.SETTINGS') }}</div>
    <div class="txt">
      <van-icon name="warning" />
      <span>{{ t('deposit.popover_Filling') }}</span>
    </div>
  </div>
</template>
<script lang="ts">
import {
  reactive,
  toRefs,
  getCurrentInstance,
  defineComponent,
  ref,
} from "vue";
import { useRouter } from "vue-router";
import type { FormInstance, FormRules } from "element-plus";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { UserService } from "@/api/user";
import { getUserInfo, getUserInfoNoLoad } from "@/utils/baseFun";
export default defineComponent({
  name: "withdrawSettings",
  setup() {
    const router = useRouter();
    const store = useStore();
    const { proxy } = getCurrentInstance() as any;
    const { t } = useI18n();
    const state = reactive({
      typeList: ["CPF"],
      // typeList: ["CPF", "PHONE", "EMAIL"],
      validateForm: {
        name: store.state.user.username,
        cpf: store.state.user.CPF,
        pix: "CPF",
        pix_num: store.state.user.CPF,
      },
    });
    state.validateForm.pix = state.typeList[0];
    const settings = () => {
      proxy.$mitt.emit("depositComShow", 0);
      proxy.$mitt.emit("depositComShow2", 0);
    };

    const closeBtn = () => {
      store.dispatch('status/setDepositShow', false)
      proxy.$mitt.emit("transfershow", false);

    }

    const formRef = ref<FormInstance>();
    const rules = reactive<FormRules>({
      name: [{ required: true, trigger: "blur" }],
      cpf: [{ required: true, trigger: "blur" }],
      pix: [{ required: true, trigger: "blur" }],
      pix_num: [{ required: true, trigger: "blur" }],
    });

    const submitForm = async (formEl: FormInstance | undefined) => {
      if (!formEl) return;
      await formEl.validate((valid, fields) => {
        if (valid) {
          UserService.bind_user_withdrawal_info({ cpf: state.validateForm.cpf, username: state.validateForm.name }).then((res) => {
            if (res.data.code == 1) {
              getUserInfoNoLoad()
              store.dispatch(
                "saveUserData/setWithdrawalSettings",
                state.validateForm
              );
              settings();
            }
          })
        } else {
        }
      });
    };

    return { ...toRefs(state), t, store, settings, rules, formRef, submitForm, closeBtn };
  },
});
</script>
<style  lang="scss" scoped>
.withdrawSettings {
  padding: 30px 27px;
  box-sizing: border-box;
  width: 512px;
  border-radius: 24px;
  background: var(--theme-box-background);

  .withdrawSettings_header {
    margin-bottom: 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    img:nth-child(1) {
      cursor: pointer;
      width: 51px;
    }

    .title {
      font-size: 24px;
      font-weight: bold;
      color: var(--theme-font-color-fff);
    }

    img:nth-last-child(1) {
      cursor: pointer;
      width: 25px;
    }
  }

  .form_title {
    margin-bottom: 15px;
    font-size: 18px;
    font-weight: bold;
    color: var(--auxiliary-font-color-9);
  }

  .el-form_style {
    .input_box {
      height: 40px;
    }
  }

  .submit_btn {
    cursor: pointer;
    padding: 15px 0;
    background: var(--auxiliary-background-16);
    border-radius: 12px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    color: var(--theme-font-color-fff);
  }

  .txt {
    padding-top: 10px;
    font-size: 20px;
    color: var(--theme-checkbox-font-color);

    span {
      vertical-align: middle;
      margin-left: 5px;
      font-size: 14px;
      font-weight: 500;
      line-height: 22px;
    }
  }
}

@media (max-width: 768px) {
  .withdrawSettings {
    width: 100%;

    .withdrawSettings_header {
      img:nth-child(1) {
        width: 38px;
      }

      .title {
        font-size: 17px;
      }

      img:nth-last-child(1) {
        width: 18px;
      }
    }

    .form_title {
      font-size: 14px;
    }

    .el-form_style {
      .el-form-item {
        margin-bottom: 0px;
      }

      .input_box {
        :deep(.el-input) {
          height: 30px;

          .el-input__wrapper {
            .el-input__inner {
              --el-input-inner-height: calc(30px);

              &::placeholder {
                font-size: 12px !important;
              }
            }
          }
        }
      }
    }

    .submit_btn {
      padding: 8px 0;
      border-radius: 8px;
      font-size: 18px;
    }
  }
}
</style>
