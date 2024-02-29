<template>
  <div class="retrievePassword">
    <div class="retrievePassword_header">
      <div class="title">{{ t('login.RecuperarSenha') }}</div>
    </div>
    <div class="phoneBox">
      <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="phoneFoucs" inputType="Number"
        :inputRed="phoneTxtRed" :data="validateForm.phone" :isHead="false" :inputName="'phone'"
        :popTxt="t('account.Númerodetelefone')" :key="`loginPhone`" v-show="phoneOrEmail == '1'" class="RinputHeat">
        <template #head>
          <div class="phone">
            <img src="@assets/images/refer/phone_icon.png" alt="" />
            <span>+{{ t('base.countryCode') }}</span>
          </div>
        </template>
      </Rinput>
      <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="emailFoucs"
        :inputRed="emailTxtRed" :data="validateForm.email" :isHead="false" :inputName="'email'"
        :popTxt="t('account.Email')" class="fontP" v-show="phoneOrEmail == '2'">
        <template #head>
          <div class="pwd">
            <img src="@assets/images/login/email_ico.png" alt="" />
          </div>
        </template>
      </Rinput>

      <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="otpFoucs" inputType="Number"
        :inputRed="otpTxtRed" :data="validateForm.otp" :isHead="false" :inputName="'otp'"
        :popTxt="t('account.CódigodeVerificação')" class="code fontP" :showBottom="true">
        <template #head>
          <div class="pwd">
            <img src="@assets/images/login/Código.png" alt="" />
          </div>
        </template>
        <template #append>
          <!-- <div class="otp" v-if="codeTime == 0" @click="getCode()">
            <img src="@/assets/images/public/loding.gif" alt="" style="width: 16.2px;" v-show="isLoding">
            <p>Obter Código</p>
          </div> -->
          <div v-if="codeTime == 0" @click="getCode()" class="otp">
            <img src="@/assets/images/public/loding.gif" alt="" style="width: 16.2px;" v-show="isLoding">
            <p>Obter Código</p>
          </div>
          <el-countdown title="" format="ss" :value="codeTime" @finish="finish" v-else />
        </template>
      </Rinput>

      <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="passwordFoucs"
        inputType="password" :inputRed="passwordTxtRed" :data="validateForm.password" :isHead="false"
        :inputName="'password'" :popTxt="t('account.senha')" :key="`loginPwd`" class="fontP">
        <template #head>
          <div class="pwd">
            <img src="@assets/images/login/Thelock.png" alt="" />
          </div>
        </template>
      </Rinput>
    </div>

    <div class="submit_btn" @click="submitForm()">
      <span>{{ t("base.confirm") }}</span>
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
  computed,
  watch
} from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import type { FormInstance, FormRules } from "element-plus";
import { useI18n } from "vue-i18n";
import { UserService } from "@/api/user";
import { debounce } from "@/utils/baseFun";
import { LoginService } from "@/api/login";
import Rinput from "@/views/Refer/components/input.vue";
import promptPopup from "@/components/promptPopup/index";
export default defineComponent({
  name: "retrievePassword",
  components: { Rinput },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      countryCode: t("base.countryCode"), // 国家区号
      validateForm: {
        phone: "",
        email: "",
        password: "",
        otp: "",
      },
      codeTime: 0,
      phoneOrEmail: computed(() => localStorage.getItem("phoneOrEmail")),
      phoneFoucs: false,
      phoneTxtRed: 1,
      passwordTxtRed: 1,
      passwordFoucs: false,
      otpTxtRed: 1,
      otpFoucs: false,
      emailTxtRed: 1,
      emailFoucs: false,
      isLoding: false
    });

    const back = () => {
      proxy.$mitt.emit("showLoginCom", 0);
    };
    const formRef = ref<FormInstance>();
    const validatePass = (rule: any, value: any, callback: any) => {
      if (value === "") {
        callback(new Error(t("login.EnterPassword")));
      } else {
        if (state.validateForm.password !== "") {
          if (!formRef.value) return;
          formRef.value.validateField("checkPass", () => null);
        }
        callback();
      }
    };
    const rules = reactive<FormRules>({
      phone: [
        {
          required: true,
          message: t("login.EnterPhoneNumber"),
          trigger: "blur",
        },
      ],
      email: [
        {
          type: 'email',
          message: 'Please input correct email address',
          trigger: ['blur', 'change'],
        },
      ],
      password: [{ validator: validatePass, trigger: "blur" }],
      otp: [
        {
          required: true,
          message: t("login.EnterVerificationCode"),
          trigger: "blur",
        },
      ],
    });

    // 获取验证码
    const getCode = () => {
      if (state.codeTime != 0) return;
      if (state.validateForm.phone == "" && state.phoneOrEmail == '1')

        return promptPopup('notificationPopup', { disappear: true, text: t("promptPopup.Digiteonumerodecelular"), type: 'error' });

      if (state.validateForm.email == "" && state.phoneOrEmail == '2') return promptPopup('notificationPopup', { disappear: true, text: t("promptPopup.Digiteemail"), type: 'error' });;
      state.isLoding = true
      store.dispatch('status/setLoadingShow', true)
      const fun = () => {
        if (state.phoneOrEmail == '1') {
          UserService.send_phone_code({
            phone: state.countryCode + state.validateForm.phone,
          }).then((res) => {
            if (res.data.code == 1) {
              state.codeTime = Date.now() + 1000 * 60;
            }
          }).finally(() => {
            state.isLoding = false
          });
        } else {
          UserService.send_email_code({
            email: state.validateForm.email,
          }).then((res) => {
            if (res.data.code == 1) {
              state.codeTime = Date.now() + 1000 * 60;
            }
          }).finally(() => {
            state.isLoding = false
          });
        }
      };
      debounce(fun);

      store.dispatch('status/setLoadingShow', false)
    };
    // 验证码结束
    const finish = () => {
      state.codeTime = 0;
    };

    const resetPwd = () => {
      const obj = {
        phone: state.countryCode + state.validateForm.phone,
        email: state.validateForm.email,
        password: state.validateForm.password,
        otp: state.validateForm.otp,
      };

      if (state.phoneOrEmail == '1') {
        LoginService.user_forget_password({ ...obj }).then((res) => {
          if (res.data.code == 1) {
            promptPopup('notificationPopup', { disappear: true, text: t("promptPopup.Senhadefinidacomsucesso"), type: 'success' })
            back();
          }
        });
      } else {
        LoginService.user_forget_email_password({ ...obj }).then((res) => {
          if (res.data.code == 1) {
            promptPopup('notificationPopup', { disappear: true, text: t("promptPopup.Senhadefinidacomsucesso"), type: 'success' });
            back();
          }
        });
      }

    };

    const submitForm = () => {

      debounce(resetPwd);
    };
    const resetForm = (formEl: FormInstance | undefined) => {
      if (!formEl) return;
      // formEl.resetFields();
    };

    const changeInputState = (val, data, key) => {
      if (state[`${key}TxtRed`] == 1 && val == 'blur') {
        state[`${key}TxtRed`] = 0;
      }
      if (!data) {
        state[`${key}Foucs`] = !state[`${key}Foucs`];
      }
    }

    const inputFun = (val, key?) => {
      if (checkVal(val, key) as any) {
        state[`${key}TxtRed`] = 2;
        state.validateForm[`${key}`] = val;
      } else {
        state[`${key}TxtRed`] = 1;
      }
    }

    const checkVal = (val, key) => {
      let boo: any = null;

      switch (key) {
        case 'phone':
          boo = val ? true : false;
          break;
        case 'password':
          if (val && val.length >= 6 && val.length <= 20) {
            boo = true;
          } else {
            promptPopup('notificationPopup', { disappear: true, text: t("promptPopup.Tamanhodasenha6_20"), type: 'error' })
            boo = false;
          }

          break;
        case 'otp':
          boo = val ? true : false;
          break;
        case 'email':
          if (val && val.search(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/) != -1) {
            boo = true;
          } else {
            boo = false;
          }

          break;
        default:
          break;
      }
      return boo;
    }

    return {
      ...toRefs(state),
      store,
      back,
      rules,
      formRef,
      submitForm,
      resetForm,
      getCode,
      finish,
      t,
      changeInputState,
      inputFun,
    };
  },
});
</script>
<style  lang="scss" scoped>
.phoneBox {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 23px;

  .phone {
    display: flex;
    align-items: center;

    img {
      width: 26px;
    }
  }

  .pwd {
    width: 100%;
    display: flex;
    align-items: center;

    img {
      width: 26px;
    }

  }

  .fontP {
    :deep(.input_txt) {
      left: 40px;
    }
  }

  .code {
    :deep(.el-input-group__append) {
      background: #4181EE;
      border: none;
      box-shadow: none;
      // width: 119px;
      height: 36px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      margin-right: 1px;
      box-sizing: border-box;
      position: relative;
      z-index: 10;
      padding: 0 10px;
    }
  }

  .otp {
    cursor: pointer;
    color: #fff;
    background: #4181EE;
    display: flex;
    // flex-direction: column;
    align-items: center;

    img {
      margin-right: 1px;
    }
  }

  :deep(.input_box_style) {
    display: inline-flex;
    align-items: center;
  }

  :deep(.el-statistic) {
    .el-statistic__content {
      font-size: 14px;
      color: #FFFFFF;
    }
  }
}

.retrievePassword {
  .retrievePassword_header {
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    justify-content: center;

    img:nth-child(1) {
      cursor: pointer;
      margin-right: 10px;
      width: 25px;
    }

    .title {
      font-size: 18px;
      font-weight: bold;
      color: #fff;
    }

    img:nth-last-child(1) {
      cursor: pointer;
      width: 25px;
    }
  }

  .enter_new_pwd {
    padding: 10px 0 20px 0;
    font-size: 20px;
    font-weight: 500;
    color: var(--auxiliary-font-color-9);
  }

  .submit_btn {
    cursor: pointer;
    padding: 14.5px 0;
    text-align: center;
    border-radius: 22px;
    background: #4181EE;

    span {
      font-size: 16px;
      font-weight: 500;
      color: #fff;
    }
  }
}

@media (max-width: 768px) {
  .retrievePassword {
    .retrievePassword_header {
      img:nth-child(1) {
        width: 20px;
      }

      .title {
        font-size: 18px;
      }

      img:nth-last-child(1) {
        width: 18px;
      }
    }

    .enter_new_pwd {
      font-size: 15px;
    }

    .submit_btn {
      padding: 10px;

      span {
        font-size: 15px;
      }
    }
  }
}
</style>
