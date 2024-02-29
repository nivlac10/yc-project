<template>
  <div>
    <div class="login_box" v-if="store.state.status.loginShow">
      <div class="tab">
        <div :class="{ active: tabIdx == index, btn_active: tabIdx == index }" v-for="(item, index) in tabList"
          :style="{ width: index == 0 ? '73px' : '91px' }" :key="index" @click="tabClick(index)">
          {{ item.title }}
        </div>
      </div>
      <div class="tab2">
        <div :class="{ btn: true, btnActive: phoneOrEmail == '1' }" @click="phoneOrEmail = '1'">
          {{ t('account.Telefone') }}
        </div>
        <div :class="{ btn: true, btnActive: phoneOrEmail == '2' }" @click="phoneOrEmail = '2'">
          {{ t('account.Email') }}
        </div>
      </div>

      <div class="phoneBox">
        <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="phoneFoucs"
          inputType="Number" :inputRed="phoneTxtRed" :data="validateForm.phone" :isHead="false" :inputName="'phone'"
          :popTxt="t('account.Númerodetelefone')" v-show="phoneOrEmail == '1'" class="RinputHeat">
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

        <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="passwordFoucs"
          inputType="password" :inputRed="passwordTxtRed" :data="validateForm.password" :isHead="false"
          :inputName="'password'" :popTxt="t('account.senha')" :key="`loginPwd`" class="fontP">
          <template #head>
            <div class="pwd">
              <img src="@assets/images/login/Thelock.png" alt="" />
            </div>
          </template>
        </Rinput>

        <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="otpFoucs" inputType="Number"
          :inputRed="otpTxtRed" :data="validateForm.otp" :isHead="false" :inputName="'otp'"
          :popTxt="t('account.CódigodeVerificação')" class="code fontP" :showBottom="true"
          v-show="tabIdx == 1 && phoneOrEmail == '1'">
          <template #head>
            <div class="pwd">
              <img src="@assets/images/login/Código.png" alt="" />
            </div>
          </template>
          <template #append>
            <div v-if="codeTime == 0" @click="getCode()" class="otp">
              <img src="@/assets/images/public/loding.gif" alt="" style="width: 16.2px;" v-show="isLoding">
              <p>{{ t('btnName.ObterCódigo') }}</p>
            </div>
            <el-countdown title="" format="ss" :value="codeTime" @finish="finish" v-else />
          </template>
        </Rinput>

      </div>
      <div class="forget_pwd">
        <span @click="forgetPassword">{{ t('login.Esqueceuasenha') }}</span>
      </div>
      <!-- <el-checkbox v-model="rememberMeChecked" label="Lembre-se da conta" size="large" v-if="tabIdx == 0" /> -->

      <!-- <div class="terms_of_service">
 
      <el-checkbox v-model="checked2" label="" size="large" style="margin-right: 5px;" />
 
      <div>
        {{ t("login.describe") }}
        <span> {{ t("login.TermsOfService") }}</span>
      </div>
    </div> -->

      <div class="submit_btn " @click="submitForm(formRef)">
        <span>{{ tabIdx == 0 ? t("account.LOGIN") : t("login.RegistrareEntrar") }}</span>
      </div>
      <p class="terms_service">
        {{ t("login.Aoacessarosite") }}
        <span @click="toHelp">{{ t("login.TermosdeServiço") }}</span>
      </p>
      <!-- <div class="forget_password" v-if="tabIdx == 0" @click="forgetPassword">
      {{ t("login.ForgetPassword") }}
    </div> -->
    </div>

  </div>
</template>
<script lang="ts">
import {
  reactive,
  toRefs,
  ref,
  getCurrentInstance,
  defineComponent,
  computed,
  watch
} from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import type { FormInstance, FormRules } from "element-plus";
import { LoginService } from "@/api/login";
import { UserService } from "@/api/user";
import { debounce } from "@/utils/baseFun";
import { register_adjust, signReport } from "@/utils/Adjust";
import { getImageUrl } from "@/utils/baseFun";
import Rinput from "@/views/Refer/components/input.vue";
import promptPopup from "@/components/promptPopup/index";
export default defineComponent({
  name: "login_box",
  components: { Rinput },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      countryCode: computed(() => t("base.countryCode")),// 国家区号
      tabList: [{ title: computed(() => t("login.Entrar")) }, { title: computed(() => t("login.Registrar")) }],
      tabIdx: 0,
      validateForm: {
        phone: "",
        email: "",
        password: "",
        otp: "",
      },
      codeTime: 0,
      rememberMeChecked: false,
      checked2: true,
      isApp: null,
      phoneOrEmail: '1',
      titleImg: [getImageUrl('login/email.png'), getImageUrl('login/PHONE.png'),],
      phoneFoucs: false,
      phoneTxtRed: 1,
      passwordTxtRed: 1,
      passwordFoucs: false,
      otpTxtRed: 1,
      otpFoucs: false,
      emailTxtRed: 1,
      emailFoucs: false,
      isLoding: false,
    });
    state.isApp = localStorage.getItem("isApp") as any;
    localStorage.setItem('phoneOrEmail', state.phoneOrEmail);
    watch(() => state.phoneOrEmail, (n, o) => {
      localStorage.setItem('phoneOrEmail', n)
    })

    // tab点击
    const tabClick = (index: number) => {
      state.tabIdx = index
      resetForm(formRef.value)
      // defaultAccountFilling()// 默认填写账号
    }
    // 默认填写账号
    // const defaultAccountFilling = () => {
    //   if (
    //     state.tabIdx == 0 &&
    //     store.state.saveUserData.accountNumber["phone"] != ""
    //   ) {
    //     state.rememberMeChecked = true;
    //     state.validateForm.phone =
    //       store.state.saveUserData.accountNumber["phone"];
    //     state.validateForm.password =
    //       store.state.saveUserData.accountNumber["password"];
    //   } else {
    //     state.validateForm.phone = ""
    //     state.validateForm.password = ""
    //   }
    // }

    proxy.$mitt.on("showLoginBox", (val: number) => {
      state.tabIdx = val;
      // defaultAccountFilling() // 默认填写账号
    });

    const forgetPassword = () => {
      proxy.$mitt.emit("showLoginCom", 1);
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
          // validator: validatePhone,
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
    // 登录
    const login = () => {
      const fun = () => {
        const obj = {
          phone: state.countryCode + state.validateForm.phone,
          email: state.validateForm.email,
          password: state.validateForm.password,
        };
        store.dispatch('status/setLoadingShow', true)
        LoginService[`${state.phoneOrEmail == '1' ? 'login' : 'user_email_login'}`]({ ...obj }).then((res) => {
          if (res.data.data.token) {
            store.dispatch('status/setLoginShow', false)
            store.dispatch("user/setData", res.data.data);
            // 保存用户账号
            if (state.rememberMeChecked) {
              store.dispatch("saveUserData/setAccountNumber", {
                phone: state.validateForm.phone,
                password: state.validateForm.password,
              });
            } else {
              store.dispatch("saveUserData/setAccountNumber", {
                phone: "",
                password: "",
              });
            }
            signReport();
            router.push('/')
          }
          store.dispatch('status/setLoadingShow', false)
        });
      };
      debounce(fun);
    };
    // 验证码结束
    const finish = () => {
      state.codeTime = 0;
    };

    // 获取验证码
    const getCode = () => {
      if (state.validateForm.phone == "") {
        promptPopup('notificationPopup', { disappear: true, text: t('promptPopup.Digiteonumerodecelular'), type: 'error' })
      }
      if (
        state.validateForm.phone == "" ||
        state.codeTime != 0 ||
        state.validateForm.password == ""
      )
        return;
      const fun = () => {
        state.isLoding = true;
        UserService.send_phone_code({
          phone: state.countryCode + state.validateForm.phone,
        }).then((res) => {
          if (res.data.code == 1) {

            state.codeTime = Date.now() + 1000 * 60;
          }

        }).finally(() => {
          state.isLoding = false;
        });
      };
      debounce(fun);
    };
    // 注册
    const register = () => {
      const fun = () => {
        store.dispatch('status/setLoadingShow', true)
        const obj = {
          phone: state.countryCode + state.validateForm.phone,
          password: state.validateForm.password,
          email: state.validateForm.email,
          otp: state.validateForm.otp,
          cid: localStorage.getItem("c") || 1,
          code: localStorage.getItem("code") || 0,
        };

        LoginService[`${state.phoneOrEmail == '1' ? 'register' : 'user_email_register'}`]({ ...obj }).then((res) => {
          if (res.data.data.token) {
            promptPopup('notificationPopup', { disappear: true, text: t('promptPopup.Registrobemsucedido'), type: 'success' })
            store.dispatch('status/setLoginShow', false)
            store.dispatch("user/setData", res.data.data);
            register_adjust(obj.email,obj.phone);
            router.push('/')
          }
          store.dispatch('status/setLoadingShow', false)
        });
      };
      debounce(fun);
    };

    const submitForm = (formEl: FormInstance | undefined) => {
      if (state.tabIdx == 0) {
        if (state.phoneOrEmail == '1') {
          if (checkVal(state.validateForm.phone, 'phone') && checkVal(state.validateForm.password, 'password')) {
            login();
          }
        } else {
          if (checkVal(state.validateForm.email, 'email') && checkVal(state.validateForm.password, 'password')) {
            login();
          }
        }
      }
      else {
        if (state.phoneOrEmail == '1') {
          if (checkVal(state.validateForm.phone, 'phone') && checkVal(state.validateForm.password, 'password')) {
            if (!checkVal(state.validateForm.otp, 'otp')) {
              return promptPopup('notificationPopup', { disappear: true, text: t('promptPopup.introduzaocódigodeconfirmação'), type: 'error' });
            } else {
              register();
            }
          }
        } else {
          if (checkVal(state.validateForm.email, 'email') && checkVal(state.validateForm.password, 'password')) {
            register();
          }
        }
      }

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
      if (checkVal(val, key)) {
        state[`${key}TxtRed`] = 2;

      } else {
        state[`${key}TxtRed`] = 1;
      }
      state.validateForm[`${key}`] = val;
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
            promptPopup('notificationPopup', { disappear: true, text: t('promptPopup.Tamanhodasenha6_20'), type: 'error' })
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

    const toHelp = () => {
      store.state.status.loginShow = false;

      router.push({
        path: "/help", query: {
          l_index: 2,
          r_index: 1
        }
      })
    }

    return {
      ...toRefs(state),
      store,
      formRef,
      submitForm,
      resetForm,
      t,
      tabClick,
      rules,
      getCode,
      finish,
      forgetPassword,
      changeInputState,
      inputFun,
      toHelp,
    };
  },
});
</script>
<style  lang="scss" scoped>
:deep(.el-statistic__content) {
  color: #fff;
}

.google_login_box {
  position: relative;
  cursor: pointer;

  .g_id_signin {
    opacity: 0;
    position: absolute;
    width: 100%;
    height: 100%;
  }
}

.login_box {
  .tab {
    display: flex;
    width: 170px;
    box-sizing: border-box;
    padding: 1px;
    background: var(--auxiliary-background-13);
    border-radius: 8px;
    margin: auto;

    div {
      cursor: pointer;
      // padding: 6px 15px 6px 15px;
      min-width: 73px;
      min-height: 29px;


      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 400;
      color: rgba(152, 171, 208, 1);


      &.active {
        font-size: 14px;
        color: #fff;
        background: none;

      }



    }

    .btn_active {
      background: rgba(65, 129, 238, 0.50) !important;
    }

    div:nth-child(1) {
      margin-right: 4px;
    }
  }

  .tab2 {
    margin-top: 34px;
    display: flex;
    justify-content: center;
    margin-bottom: 29px;

    .btn {
      width: 72px;
      height: 28px;
      color: #fff;
      font-size: 12px;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 31px;
    }

    .btnActive {
      background: #2F3445;
    }

  }

  .title {
    padding: 23px 0 23px 0;
    font-size: 26px;
    font-weight: bold;
    color: var(--theme-font-color-fff);
    // word-spacing: 10px;
    // white-space: pre;
    display: flex;
    gap: 10px;
    align-items: center;
    width: 100%;

    img {
      width: 38px;
      // height: 26px;
    }
  }

  :deep(.el-checkbox) {
    padding-bottom: 5px;
    --el-checkbox-bg-color: var(--auxiliary-font-color-9);

    .el-checkbox__input {
      .el-checkbox__inner {
        border-radius: 50%;

        &::after {
          display: none;
        }
      }

      &.is-checked {
        .el-checkbox__inner {
          background: var(--theme-checkbox-font-color);
          border: 2px solid var(--theme-font-color-fff);

          &::after {
            display: none;
          }
        }
      }
    }

    .el-checkbox__label {
      font-size: 20px;
      font-weight: bold;
      color: var(--theme-checkbox-font-color);
    }
  }

  .terms_of_service {
    display: flex;
    align-items: center;
    padding: 0 0 32px 0;
    font-size: 13px;
    font-weight: 500;
    color: var(--theme-input-placeholder-color);

    div {
      line-height: 22px;

      &:nth-child(1) {
        margin-right: 6px;
      }

      span {
        cursor: pointer;
        color: var(--auxiliary-font-color-8);
      }
    }
  }

  .submit_btn {
    cursor: pointer;
    padding: 14.5px 0;
    text-align: center;
    border-radius: 22px;
    background: #4181EE;

    span {
      font-size: 16px;
      font-weight: 600;
      color: #fff;
    }
  }

  .forget_password {
    cursor: pointer;
    padding-top: 20px;
    font-size: 20px;
    font-weight: bold;
    color: var(--theme-checkbox-font-color);
    text-align: center;
  }

  .phoneBox {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 19px;

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
        width: 119px;
        height: 36px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        margin-right: 1px;
        box-sizing: border-box;
        position: relative;
        z-index: 10;
      }
    }

    .otp {
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
  }

  .forget_pwd {
    font-size: 12px;
    color: #98ABD0;
    margin-bottom: 30px;
    cursor: pointer;
  }

  .terms_service {
    margin-top: 26px;
    font-size: 12px;
    color: #98ABD0;
    padding: 0 20px;
    box-sizing: border-box;

    span {
      cursor: pointer;
      color: #4181EE;
    }
  }

}





@media (max-width: 768px) {
  // .login_box {
  //   .tab {
  //     // div {
  //     //   padding: 10px 20px;
  //     //   font-size: 14px;

  //     //   &.active {
  //     //     font-size: 14px;
  //     //   }
  //     // }
  //   }

  //   .tab2 {
  //     margin-top: 15px;

  //   }

  //   .title {
  //     padding: 10px 0 16px 0;
  //     font-size: 18px;

  //     img {
  //       width: 29px;
  //       height: 29px;
  //     }

  //     span {
  //       font-size: 17px;
  //     }
  //   }

  //   :deep(.el-checkbox) {
  //     height: auto;

  //     .el-checkbox__input {
  //       .el-checkbox__inner {
  //         border-radius: 50%;

  //         &::after {
  //           display: none;
  //         }
  //       }

  //       &.is-checked {
  //         .el-checkbox__inner {
  //           background: var(--theme-checkbox-font-color);
  //           border: 2px solid var(--theme-font-color-fff);

  //           &::after {
  //             display: none;
  //           }
  //         }
  //       }
  //     }

  //     .el-checkbox__label {
  //       font-size: 10px;
  //       font-weight: bold;
  //       color: var(--theme-checkbox-font-color);
  //     }
  //   }

  //   .submit_btn {
  //     padding: 10px;

  //     span {
  //       font-size: 15px;
  //     }
  //   }

  //   .terms_of_service {
  //     padding: 0 0 20px 0;

  //     div {
  //       line-height: 15px;
  //     }
  //   }

  //   .forget_password {
  //     font-size: 15px;
  //   }


  // }
}
</style>
