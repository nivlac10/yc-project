<template>
  <div class="setPassword">
    <div class="setPassword_content">
      <el-form class="el-form_style" ref="formRef" :model="validateForm" :rules="rules">
        <el-form-item label="" prop="old_pwd">
          <Rinput class="fontP" @changeInputState="changeInputState" @inputChangeData="inputFun"
            :inputFoucs="old_pwdFoucs" inputType="password" :inputRed="old_pwdTxtRed" :data="validateForm.old_pwd"
            :isHead="false" :inputName="'old_pwd'" :popTxt="t('account.SenhaAntiga')">
            <template #head>
              <div class="phone">
                <img src="@assets/images/login/Thelock.png" alt="" style="width: 26px;" />
              </div>
            </template>
          </Rinput>
        </el-form-item>
        <el-form-item label="" prop="new_pwd">
          <Rinput class="fontP" @changeInputState="changeInputState" @inputChangeData="inputFun"
            :inputFoucs="new_pwdFoucs" inputType="password" :inputRed="new_pwdTxtRed" :data="validateForm.new_pwd"
            :isHead="false" :inputName="'new_pwd'" :popTxt="t('account.NovaSenha')">
            <template #head>
              <div class="phone">
                <img src="@assets/images/login/Thelock.png" alt="" style="width: 26px;" />
              </div>
            </template>
          </Rinput>
        </el-form-item>
      </el-form>

      <div class="btn" @click="submitForm(formRef)"><span>{{ t('btnName.salvar') }}</span></div>
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
import { useStore } from "@/store/index";
import type { FormInstance, FormRules } from "element-plus";
import { UserService } from "@/api/user";
import { debounce } from "@/utils/baseFun";
import { useI18n } from "vue-i18n";
import Rinput from "../../Refer/components/input.vue";
import promptPopup from "@/components/promptPopup/index";

export default defineComponent({
  name: "setPassword",
  components: { Rinput },
  setup() {
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const { proxy } = getCurrentInstance() as any;
    const state = reactive({
      validateForm: {
        old_pwd: "",
        new_pwd: "",
      },
      old_pwdTxtRed: 1,
      old_pwdFoucs: false,
      new_pwdTxtRed: 1,
      new_pwdFoucs: false,
    });

    const changeInputState = (val, data, key) => {
      if (state[`${key}TxtRed`] == 1 && val == 'blur') {
        state[`${key}TxtRed`] = 0;
      }
      if (!data) {
        state[`${key}Foucs`] = !state[`${key}Foucs`];
      }
    }

    const inputFun = (val, key?) => {
      if (checkVal(val, key)) {
        state[`${key}TxtRed`] = 2;
        state.validateForm[`${key}`] = val;
      } else {
        state[`${key}TxtRed`] = 1;
      }
    }
    const checkVal = (val, key) => {
      let boo: any = null;
      switch (key) {
        case 'old_pwd':
          boo = val ? true : false;
          break;
        case 'new_pwd':
          boo = val ? true : false;
          break;
        default:
          break;
      }

      return boo;
    }

    const formRef = ref<FormInstance>();
    const rules = reactive<FormRules>({
      old_pwd: [{ required: true, trigger: "blur" }],
      new_pwd: [{ required: true, trigger: "blur" }],
    });

    const submitForm = async (formEl: FormInstance | undefined) => {
      if (!formEl) return;
      await formEl.validate((valid, fields) => {
        if (valid) {
          const fun = () => {
            UserService.change_user_pwd({ ...state.validateForm }).then(
              (res) => {
                if (res.data.code == 1) promptPopup('notificationPopup', { disappear: true, text: t('promptPopup.Configuraçãobemsucedida'), type: 'success' })
              }
            );
          };
          debounce(fun);
        } else {
        }
      });
    };

    return { ...toRefs(state), store, t, formRef, rules, submitForm, changeInputState, inputFun };
  },
});
</script>
<style  lang="scss" scoped>
:deep(.el-form-item__content) {
  line-height: normal;
  display: block;
}

:deep(.el-form-item) {
  display: block;
}

.setPassword {
  .setPassword_content {
    padding: 16px 20px 13px 20px;
    background: #202431;
    border-radius: 12px;
    box-sizing: border-box;

    .el-form_style {
      .el-form-item {
        margin-bottom: 18px;
      }
    }

    .phone {
      width: 100%;
      display: flex;
      justify-content: flex-start;
      align-items: center;
      position: relative;

      p {
        color: #B2B6C5;
        font-size: 14px;
      }
    }

    .fontP {
      :deep(.input_txt) {
        left: 40px;
      }
    }

    .btn {
      text-align: right;

      span {
        cursor: pointer;
        display: inline-block;
        padding: 0 24px;
        line-height: 26px;
        border-radius: 17px;
        border: 1px solid #7EC050;
        font-size: 13px;
        color: #7EC050;
      }
    }
  }
}

@media (max-width: 768px) {
  .setPassword {
    .setPassword_content {
      padding: 16px 9px;
      border-radius: 8px;

      .el-form_style {
        .el-form-item {
          margin-bottom: 18px;
        }
      }

      .phone {
        width: 100%;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        position: relative;

        p {
          color: #B2B6C5;
          font-size: 14px;
        }
      }

      .fontP {
        :deep(.input_txt) {
          left: 40px;
        }
      }

      .btn {
        span {
          line-height: 24px;
          border-radius: 13px;
          font-size: 13px;
        }
      }
    }
  }
}
</style>
