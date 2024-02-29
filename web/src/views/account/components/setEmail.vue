<template>
  <div class="setEmail">
    <div class="setPhoneNumber_content">
      <div class="setPhoneNumber_content_header">
        <span>{{ t('account.Emailatual') }}</span>
      </div>
      <div class="current_info_box">{{ store.state.user['email'] }}</div>
      <div class="binding_success" v-if="store.state.user['email']">{{ t('account.OConteúdoUsado') }}
      </div>
      <el-form class="el-form_style" ref="formRef" :model="validateForm" :rules="rules" v-else>
        <el-form-item prop="email">
          <Rinput class="fontP" @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="emailFoucs"
            :inputRed="emailTxtRed" :data="validateForm.email" :isHead="false" :inputName="'email'" :popTxt="t('account.Email')">
            <template #head>
              <div class="pwd">
                <img src="@assets/images/login/email_ico.png" alt="" />
              </div>
            </template>
          </Rinput>
        </el-form-item>
        <el-form-item prop="otp">
          <Rinput class="fontP" @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="otpFoucs"
            :inputRed="otpTxtRed" :data="validateForm.otp" inputName="otp" :popTxt="t('account.CódigodeVerificação')"
            :isHead="false">
            <template #head>
              <div class="phone">
                <img src="@/assets/images/login/Código.png" alt="" style="width: 26px;">
              </div>
            </template>
            <template #bottom>
              <div class="optBtn">
                <div v-if="codeTime == 0" @click="getCode()">
                  <img src="@/assets/images/public/loding.gif" alt="" style="width: 16.2px;" v-show="isLoding">
                  <p>{{ t('btnName.ObterCódigo') }}</p>
                </div>
                <el-countdown title="" format="ss" :value="codeTime" @finish="finish" v-else />
              </div>
            </template>
          </Rinput>
        </el-form-item>
      </el-form>
      <div class="btn" @click="submitForm(formRef)" v-if="!store.state.user['email']"><span>{{ t('btnName.salvar') }}</span></div>
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
import { useI18n } from "vue-i18n";
import { debounce, getUserInfo } from "@/utils/baseFun";
import Rinput from "@/views/Refer/components/input.vue";

export default defineComponent({
  name: "setEmail",
  components: { Rinput },
  setup() {
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const { proxy } = getCurrentInstance() as any;
    const state = reactive({
      validateForm: {
        email: "",
        otp: "",
      },
      codeTime: 0,
      emailTxtRed: 1,
      emailFoucs: false,
      otpTxtRed: 1,
      otpFoucs: false,
      isLoding: false,
      time: null,
    });

    const formRef = ref<FormInstance>();
    const rules = reactive<FormRules>({
      phone: [{ required: true, trigger: "blur" }],
      otp: [{ required: true, trigger: "blur" }],
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
        case 'phone':
          boo = val ? true : false;
          break;
        case 'password':
          boo = val ? true : false;
          break;
        case 'otp':
          boo = val ? true : false;
          break;
        case 'email':
          boo = val ? true : false;
          break;
        default:
          break;
      }

      return boo;
    }

    const getCode = () => {
      if (state.validateForm.email == "" || state.codeTime != 0) return;
      store.dispatch('status/setLoadingShow', true)
      state.isLoding = true;

      const fun = () => {
        UserService.send_email_code({
          email: state.validateForm.email,
        }).then((res) => {
          if (res.data.code == 1) state.codeTime = Date.now() + 1000 * 60;
        }).finally(() => {
          state.isLoding = false;
        });
      };
      debounce(fun);
      store.dispatch('status/setLoadingShow', false)
    };
    const finish = () => {
      state.codeTime = 0;
    };

    const submitForm = async (formEl: FormInstance | undefined) => {
      if (!formEl) return;
      await formEl.validate((valid, fields) => {
        if (valid) {
          const fun = () => {
            UserService.bind_user_email({ ...state.validateForm }).then((res) => {
              if (res.data.code == 1) getUserInfo(); // 更新用户信息
            });
          };
          debounce(fun);
        } else {
        }
      });
    };

    return {
      ...toRefs(state),
      store,
      t,
      formRef,
      rules,
      submitForm,
      getCode,
      finish,
      changeInputState,
      inputFun
    };
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

.setEmail {
  .setPhoneNumber_content {
    padding: 16px 20px 13px 20px;
    background: #202431;
    border-radius: 12px;
    // box-sizing: border-box;

    .setPhoneNumber_content_header {
      margin-bottom: 12px;

      span {
        font-size: 14px;
        color: #B2B6C5;
      }
    }

    .current_info_box {
      margin-bottom: 18px;
      padding-left: 16px;
      height: 40px;
      line-height: 40px;
      border-radius: 6px;
      border: 1px solid rgba(178, 182, 197, 0.3);
      box-sizing: border-box;
      overflow-x: scroll;
      font-size: 14px;
      color: #FFFFFF;
    }

    .binding_success {
      margin-bottom: 13px;
      font-size: 12px;
      color: #7EC050;
      line-height: 16px;
    }

    .pwd {
      width: 100%;
      display: flex;
      align-items: center;

      img {
        width: 26px;
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

    .optBtn {
      cursor: pointer;
      position: absolute;
      right: 2px;
      top: 4px;
      // width: 121px;
      background: #4181EE;
      border-radius: 6px;
      font-size: 14px;
      color: #fff;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 0px 8px;
      z-index: 10;
      height: 34px;

      p {
        color: #fff;
      }

      img {
        margin-right: 6px;
      }

      div {
        display: flex;
      }
    }

    :deep(.el-statistic) {
      .el-statistic__content {
        font-size: 14px;
        color: #FFFFFF;
      }
    }

    .el-form_style {
      .el-form-item {
        margin-bottom: 18px;
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
  .setEmail {
    .setPhoneNumber_content {
      padding: 16px 9px;
      border-radius: 8px;

      .setPhoneNumber_content_header {
        span {
          font-size: 12px;
        }
      }

      .current_info_box {
        margin-bottom: 18px;
        padding-left: 16px;
        height: 40px;
        line-height: 40px;
        border-radius: 6px;
        border: 1px solid rgba(178, 182, 197, 0.3);
        box-sizing: border-box;
        overflow-x: scroll;
        font-size: 14px;
        color: #FFFFFF;
      }

      .pwd {
        width: 100%;
        display: flex;
        align-items: center;

        img {
          width: 26px;
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

      .optBtn {
        cursor: pointer;
        position: absolute;
        right: 2px;
        top: 4px;
        // width: 121px;
        background: #4181EE;
        border-radius: 6px;
        font-size: 14px;
        color: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0px 8px;
        z-index: 10;
        height: 34px;

        p {
          color: #fff;
        }

        img {
          margin-right: 6px;
        }

        div {
          display: flex;
        }
      }

      :deep(.el-statistic) {
        .el-statistic__content {
          font-size: 14px;
          color: #FFFFFF;
        }
      }

      .binding_success {
        margin-bottom: 13px;
        font-size: 12px;
        color: #7EC050;
      }

      .el-form_style {
        .el-form-item {
          margin-bottom: 18px;
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
