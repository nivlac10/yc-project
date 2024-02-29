<template>
  <div class="setPhoneNumber">
    <el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
      :width="store.state.status.isPc ? '512px' : '100%'">
      <div class="setPhoneNumber_content">
        <img class="close_img" src="@assets/images/public/popover_error_icon.png" alt="" @click="closeCom" />
        <div class="setPhoneNumber_content_header">
          <span>{{ t('account.Verificaçãodetelefone') }}</span>
        </div>

        <el-form class="el-form_style" ref="formRef" :model="validateForm" :rules="rules">
          <el-form-item label="" prop="phone">
            <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="inputFoucs"
              :inputRed="inputTxtRed" :data="validateForm.phone" :popTxt="t('account.Númerodetelefone')" :isHead="false">
              <template #head>
                <div class="phone">
                  <img src="@/assets/images/refer/phone_icon.png" alt="" style="width: 30px;">
                  <p>+{{ t('base.countryCode') }}</p>
                </div>
              </template>
            </Rinput>

          </el-form-item>
          <el-form-item label="" prop="otp">
            <Rinput @changeInputState="changeInputState2" @inputChangeData="inputFun2" :inputFoucs="inputFoucs2"
              :inputRed="inputTxtRed2" :data="validateForm.phone" :popTxt="t('account.Númerodetelefone')" :isHead="false">
              <template #head>

                <div class="phone">
                  <img src="@/assets/images/refer/Key.png" alt="" style="width: 32px;">

                </div>

              </template>
              <template #bottom>

                <div class="optBtn">
                  <div v-if="codeTime == 0" @click="getCode()">
                    <img src="@/assets/images/public/loding.gif" alt="" style="width: 16.2px;" v-show="isLoding">
                    <p>{{ t('btnName.Obtivermos') }}</p>
                  </div>
                  <p v-else>{{ codeTime }}</p>
                </div>

              </template>
            </Rinput>
          </el-form-item>

        </el-form>
        <div class="btn" @click="submitForm(formRef)">{{ t('btnName.Enviar') }}</div>
      </div>
    </el-dialog>
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
import { fa } from "element-plus/es/locale";
import { stat } from "fs";
export default defineComponent({
  name: "setPhoneNumber",
  components: { Rinput },
  setup() {
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const { proxy } = getCurrentInstance() as any;
    const state = reactive({
      dialogVisible: true,
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
        console.log(state.validateForm.phone);

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

.setPhoneNumber {
  display: flex;
  justify-content: center;

  .setPhoneNumber_content {
    padding: 42px 28px 32px 28px;
    position: relative;
    background: #202330;
    border-radius: 16px;
    width: 440px;
    box-sizing: border-box;

    .close_img {
      cursor: pointer;
      position: absolute;
      top: 24px;
      right: 24px;
      width: 25px;
    }

    .setPhoneNumber_content_header {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 35px;

      span {
        font-size: 20px;
        color: #FFFFFF;
      }
    }

    .el-form_style {
      // padding: 0 28px;

      .phone {
        display: flex;
        align-items: center;
        position: relative;

        p {
          color: #B2B6C5;
          font-size: 14px;
        }


      }

      .input_box_code {
        display: flex;
        gap: 13px;

        // :deep(.el-input__inner) {
        //   padding-left: 60px;
        // }

        .code_btn {
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          width: 110px;
          height: 48px;
          font-size: 20px;
          font-weight: bold;
          color: var(--theme-font-color-fff);
          border-radius: 8px;
          background: var(--auxiliary-background-18);
        }

        // :deep(.el-statistic__number) {
        //   color: var(--theme-font-color-fff);
        // }
      }
    }

    .btn {
      cursor: pointer;
      text-align: center;
      border-radius: 30px;
      font-size: 16px;
      font-weight: bold;
      color: var(--theme-font-color-fff);
      background: #4181EE;
      height: 40px;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-top: 8px;
    }
  }
}

@media (max-width: 768px) {
  .optBtn {
    right: 2px;
    top: 2px;
  }

  .setPhoneNumber {
    .setPhoneNumber_content {
      padding: 50px 20px 37px 20px;
      border-radius: 0;

      .setPhoneNumber_content_header {
        img {
          width: 32px;
        }

        span {
          font-size: 20px;
        }
      }

      .el-form_style {
        margin-bottom: 20px !important;

        // padding: 0 25px;
        .phone {}

        .el-form-item {
          margin-bottom: 20px;
        }

        // :deep(.input_boxP, .el-input, .el-input__wrapper) {
        //   height: 38px !important;

        //   .el-input__inner {
        //     height: 38px !important;
        //   }
        // }

        .input_boxP {
          .input_box_l_phone {
            height: 38px;

            span {
              font-size: 16px;
              color: var(--auxiliary-font-color-9);
            }

            img {
              width: 15.51px;
            }
          }

          >img {
            width: 20px;
          }

          :deep(.el-input__inner) {
            padding-left: 100px;
          }
        }

        .input_box_code {
          display: flex;
          gap: 13px;

          // :deep(.el-input__inner) {
          //   padding-left: 40px;
          // }

          .code_btn {
            height: 38px;
            font-size: 20px;
          }
        }
      }

      .btn {
        height: 38px;
        line-height: 38px;
        font-size: 18px;
      }
    }
  }
}
</style>
