<template>
  <div class="setPhone">
    <div class="setPhone_content">
      <div class="setPhone_content_header">
        <span>{{ t('account.Númerodetelefonenovo') }}</span>
      </div>
      <div class="current_info_box">{{ store.state.user.phone ? '+' : '' }}{{ store.state.user.phone }}</div>
      <div class="binding_success" v-if="store.state.user['phone']">{{ t('account.OConteúdoUsado') }}
      </div>
      <el-form class="el-form_style" ref="formRef" :model="validateForm" :rules="rules" v-else>
        <el-form-item label="" prop="phone">
          <Rinput class="fontP" @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="inputFoucs"
            :inputRed="inputTxtRed" :data="validateForm.phone" :popTxt="t('account.Númerodetelefone')" :isHead="false">
            <template #head>
              <div class="phone">
                <img src="@/assets/images/refer/phone_icon.png" alt="" style="width: 26px;">
                <p>+{{ t('base.countryCode') }}</p>
              </div>
            </template>
          </Rinput>

        </el-form-item>
        <el-form-item label="" prop="otp">
          <Rinput class="fontP2" @changeInputState="changeInputState2" @inputChangeData="inputFun2"
            :inputFoucs="inputFoucs2" :inputRed="inputTxtRed2" :data="validateForm.phone"
            :popTxt="t('account.CódigodeVerificação')" :isHead="false">
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
                <p v-else>{{ codeTime }}</p>
              </div>
            </template>
          </Rinput>
        </el-form-item>

      </el-form>
      <div class="btn" @click="submitForm(formRef)" v-if="!store.state.user['phone']"><span>{{ t('btnName.salvar')
      }}</span></div>
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
import Rinput from "../../Refer/components/input.vue";
export default defineComponent({
  name: "setPhone",
  components: { Rinput },
  setup() {
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const { proxy } = getCurrentInstance() as any;
    const state = reactive({
      validateForm: {
        phone: "",
        otp: "",
      },
      codeTime: 0,
      inputFoucs: false,
      inputTxtRed: 1,
      inputFoucs2: false,
      inputTxtRed2: 1,
      isLoding: false,
      time: null,
    });

    const closeCom = () => {
      proxy.$mitt.emit("showCom", -1);
    };

    const formRef = ref<FormInstance>();
    const rules = reactive<FormRules>({
      phone: [{ required: true, trigger: "blur" }],
      otp: [{ required: true, trigger: "blur" }],
    });

    const getCode = () => {
      if (state.validateForm.phone == "" || state.codeTime !== 0) return;
      state.isLoding = true;
      const fun = () => {
        UserService.send_phone_code({
          phone: t("base.countryCode") + state.validateForm.phone,
        }).then((res) => {
          if (res.data.code == 1) {
            state.codeTime = 60;
            state.time = setInterval(() => {
              state.codeTime -= 1;
              if (state.codeTime == 0) {
                clearInterval(state.time as any);
              }
            }, 1000) as any;
          }
        }).finally(() => {
          state.isLoding = false;
        });
      };
      debounce(fun);

    };
    const finish = () => {
      state.codeTime = 0;
    };

    const submitForm = async (formEl: FormInstance | undefined) => {
      if (!formEl) return;
      await formEl.validate((valid, fields) => {
        if (valid) {
          const fun = () => {
            UserService.bind_user_phone({
              phone: t("base.countryCode") + state.validateForm.phone,
              otp: state.validateForm.otp,
            }).then((res) => {
              if (res.data.code == 1) {
                getUserInfo(); // 更新用户信息
                closeCom();
              }
            });
          };
          debounce(fun);
        } else {
        }
      });
    };
    const changeInputState = (val, data) => {
      if (state.inputTxtRed == 1 && val == 'blur') {
        state.inputTxtRed = 0;
      }
      if (!data) {
        state.inputFoucs = !state.inputFoucs;
      }
    }

    const inputFun = (val) => {
      if (val != '') {
        state.inputTxtRed = 2;
        state.validateForm.phone = val;
      } else {
        state.inputTxtRed = 0;
      }
    }

    const changeInputState2 = (val, data) => {
      if (state.inputTxtRed2 == 1 && val == 'blur') {
        state.inputTxtRed2 = 0;
      }
      if (!data) {
        state.inputFoucs2 = !state.inputFoucs2;
      }
    }

    const inputFun2 = (val) => {
      if (val != '') {
        state.inputTxtRed2 = 2;
        state.validateForm.otp = val;
      } else {
        state.inputTxtRed2 = 0;
      }
    }

    return {
      ...toRefs(state),
      store,
      t,
      closeCom,
      formRef,
      rules,
      submitForm,
      getCode,
      finish,
      changeInputState,
      inputFun,
      changeInputState2,
      inputFun2,
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

:deep(.el-dialog .el-dialog__body) {
  display: flex;
  justify-content: center;
}

.fontP {
  :deep(.input_txt) {
    left: 80px;
  }
}

.fontP2 {
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

.setPhone {
  .setPhone_content {
    padding: 16px 20px 13px 20px;
    background: #202431;
    border-radius: 12px;
    box-sizing: border-box;

    .setPhone_content_header {
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

    .el-form_style {
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
  .setPhone {
    .setPhone_content {
      padding: 16px 9px;
      border-radius: 8px;

      .setPhone_content_header {
        margin-bottom: 12px;

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

      .binding_success {
        margin-bottom: 13px;
        font-size: 12px;
        color: #7EC050;
      }

      .el-form_style {
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
