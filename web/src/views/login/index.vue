<template>
  <div class="login_max_box">
    <el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
      :destroy-on-close="true" :lock-scroll="false" :width="store.state.status.isPc ? '908px' : '100%'">
      <div class="content_box">
        <div class="close_btn" @click="closeLoginBox">
          <img src="@assets/images/public/Shutdown.png" alt="" />
        </div>
        <!-- <div class="l_box">
          <img v-if="store.state.status.isPc" src="@/assets/images/login/banner2L.png" alt="">
          <img v-else src="@assets/images/login/banner2H.png" alt="">
        </div> -->
        <div class="r_box">
          <div v-if="!toFblogin">
            <div v-if="comIdx == 0">
              <login  />

            </div>
<!-- 
            <retrieve-password v-if="comIdx !== 0" /> -->
          </div>
        </div>
      </div>
    </el-dialog>
    <el-dialog v-if="comIdx !== 0" v-model="dialogVisible" :show-close="false" :close-on-click-modal="false"
      :close-on-press-escape="false" :destroy-on-close="true" :lock-scroll="false"
      :width="store.state.status.isPc ? '908px' : '100%'">
      <div class="content_box">
        <div class="close_btn" @click="comIdx = 0">
          <img src="@assets/images/public/Shutdown.png" alt="" />
        </div>
        <!-- <div class="l_box">
          <img v-if="store.state.status.isPc" src="@/assets/images/login/banner2L.png" alt="">
          <img v-else src="@assets/images/login/banner2H.png" alt="">
        </div> -->
        <div class="r_box">
          <div v-if="!toFblogin">
            <retrieve-password  />
          </div>
        </div>
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
  watch,
} from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "@/store/index";
import type { FormInstance, FormRules } from "element-plus";
import { LoginService } from "@/api/login";
import { UserService } from "@/api/user";
import { debounce } from "@/utils/baseFun";
import login from "./components/login.vue";
import retrievePassword from "./components/retrievePassword.vue";
import fbAndGoole from './components/fbAndGoogle.vue'
export default defineComponent({
  name: "index",
  components: { login, retrievePassword, fbAndGoole },
  setup() {
    const store = useStore();
    const { t } = useI18n();
    const { proxy } = getCurrentInstance() as any;
    const state = reactive({
      dialogVisible: true,
      comIdx: 0,
      toFblogin: false,
    });

    proxy.$mitt.on("showLoginCom", (val: number) => {
      console.log(val);

      state.comIdx = val;
    });

    const closeLoginBox = () => {
      if (state.comIdx !== 0) {
        state.comIdx= 0;
      }else{
        store.dispatch('status/setLoginShow', false)
      }
     
    };
    // const toFbAndGoolelogin = (is) => {


    //   state.toFblogin = is;
    // }
    return {
      ...toRefs(state),
      store,
      closeLoginBox,
      t,
    };
  },
});
</script>
<style  lang="scss" scoped>
.login_max_box {
  user-select: none;

  :deep(.el-overlay) {
    z-index: 2300 !important;
  }

  :deep(.el-dialog) {
    .el-dialog__body {
      display: flex;
      justify-content: center;
    }
  }

  .content_box {
    position: relative;
    display: flex;
    flex-shrink: 0;
    width: 368px;
    background: var(--theme-box-background);
    border-radius: 18px;
    overflow: hidden;

    .close_btn {
      cursor: pointer;
      position: absolute;
      top: 34px;
      right: 24px;

      img {
        width: 19px;
      }
    }

    .l_box {
      width: 100%;
      background: #313343;
      border-radius: 18px 0 0 18px;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    .r_box {
      width: 100%;
      padding: 33px 24px 43px 24px;
      // min-height: 680px;
      // max-height: 680px;
      // min-width: 400px;
    }

    :deep(.el-form) {
      .el-form-item {
        margin-bottom: 24px;
      }

      .el-form-item.is-error .el-input__wrapper {
        box-shadow: 0 0 0 2px var(--theme-input-error-border-color) inset !important;
      }

      .input_box {
        position: relative;
        width: 100%;
        height: 48px;

        .el-input {
          .el-input__wrapper {
            background: transparent;
            border-radius: 8px;

            box-shadow: 0 0 0 2px var(--theme-input-border-color, var(--el-border-color)) inset;

            &.is-focus {
              box-shadow: 0 0 0 2px var(--theme-input-focus-border-color) inset;
            }

            .el-input__inner {
              --el-input-inner-height: calc(48px);

              &::placeholder {
                font-size: 16px;
                font-weight: 500;
                color: var(--theme-input-placeholder-color);
              }
            }

            .el-input__icon {
              font-size: 20px;
            }
          }
        }

        .input_box_l {
          position: absolute;
          height: 48px;
          display: flex;
          align-items: center;

          img {
            padding: 0 10px;
            width: 28px;
          }
        }

        .input_box_l_phone {
          display: flex;
          align-items: center;
          padding: 0 10px;
          border-right: 2px solid var(--theme-input-border-color);

          span {
            margin-right: 20px;
            font-size: 22px;
            color: var(--auxiliary-font-color-9);
          }

          img {
            padding: 0;
            width: 15.51px;
          }
        }
      }

      .input_box_phone {
        .el-input__inner {
          padding-left: 110px;
        }
      }

      .input_box_email {
        .el-input__inner {
          padding-left: 35px;
        }
      }

      .input_box_password,
      .input_box_code {
        .el-input__inner {
          padding-left: 35px;
        }
      }

      .input_box_code {
        .sl_box_shadow {
          cursor: pointer;
          display: flex;
          align-items: center;
          padding: 0 15px;
          position: absolute;
          top: 0px;
          right: 0px;
          height: 50px;
          font-size: 17px;
          font-weight: bold;
          color: var(--auxiliary-font-color-10);
          border-radius: 8px;
        }
      }
    }
  }
}

.other_mode {
  padding-top: 40px;
  cursor: pointer;

  .togoogle {
    width: 100%;
    height: 115px;
    background: url(@/assets/images/login/backdrop@2x.png) no-repeat;
    background-size: 100% 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

    p {
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      text-align: center;
      font-size: 12px;
      margin-bottom: 5px;
      padding: 0 15px;
      color: #C3CFD9;
      line-height: 14px;

      span {
        font-size: 14px;
        font-weight: bold;
        color: #DEA541;
        margin-top: 3px;
      }

      img {
        width: 45px;
      }
    }
  }

  .other_mode_title {
    margin-bottom: 17px;
    font-size: 20px;
    font-weight: bold;
    color: var(--auxiliary-font-color-9);
  }

  .img_btn {
    display: flex;
    position: relative;

    img {
      cursor: pointer;
      margin-right: 18px;
      width: 46px;
    }
  }
}

@media screen and (max-width: 768px) {
  .login_max_box {

    :deep(.el-dialog) {
      padding: 0 20px;
    }

    .content_box {
      flex-direction: column;
      width: 100%;
      max-height: 100vh;
      overflow-y: scroll;

      .close_btn {
        img {
          width: 13px;
        }
      }

      .l_box {
        height: 150px;
        border-radius: 0px;
      }

      .r_box {
        padding-right: 24px;
        padding-left: 24px;
        box-sizing: border-box;
        min-height: auto !important;
        min-width: auto !important;
      }

      :deep(.el-form) {
        .el-form-item {
          margin-bottom: 17px;
        }

        .input_box {
          height: 33px;

          .el-input {
            .el-input__wrapper {
              .el-input__inner {
                --el-input-inner-height: calc(33px);

                &::placeholder {
                  font-size: 12px;
                }
              }
            }
          }

          .input_box_l {
            position: absolute;
            height: 33px;
            display: flex;
            align-items: center;

            img {
              padding: 0 10px;
              width: 20px;
            }
          }

          .input_box_l_phone {
            span {
              margin-right: 10px;
              font-size: 16px;
            }

            img {
              padding: 0;
              width: 15.51px;
            }
          }
        }

        .input_box_phone {
          .el-input__inner {
            padding-left: 80px;
          }
        }

        .input_box_password,
        .input_box_code {
          .el-input__inner {
            padding-left: 30px;
          }
        }

        .input_box_code {
          .sl_box_shadow {
            padding: 0 15px;
            height: 33px;
            font-size: 13px;
          }
        }
      }
    }
  }

  .other_mode {
    padding-top: 20px;

    .other_mode_title {
      margin-bottom: 10px;
      font-size: 14px;
    }

    .img_btn {
      img {
        margin-right: 12px;
        width: 32px;
      }
    }
  }
}
</style>
  