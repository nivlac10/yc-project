<template>
  <div class="withdrawalInformation">
    <div class="withdraw_mode">
      <div class="txt_box">
        <div :class="{ l_box: true, boder: !isSeting }">
          <div class="header_box">
            <div>
              <div>{{ t('referPop.ContaPIX') }}</div>
              <div>
                <el-popover :placement="store.state.status.isPc ? 'right' : 'bottom'" trigger="click" width="329px"
                  popper-class="el_popover_style" :teleported="false">
                  <template #reference>
                    <img src="../../../assets/images/refer/query.png" alt="" class="Conta">
                  </template>
                  <div class="popover_content">
                    <div class="popover_content_header">{{ t('referPop.ConfiguraçãodoPIX') }}</div>
                    <div class="popover_content_txt">
                      {{ t('referPop.Opreenchimentoretirada') }} 
                    </div>
                  </div>
                </el-popover>
              </div>
            </div>
            <div class="btn" @click="Mudar" v-if="!isSeting">
              {{ t('referPop.Mudar') }}
            </div>
            <div class="btns" v-if="isSeting && !isOne">
              <div class="btn" @click="isSeting = false">
                {{ t('referPop.Cancelar') }}
              </div>
              <div class="btn" @click="save">
                {{ t('referPop.Salvar') }}
              </div>
            </div>
          </div>

          <div class="c_box" v-if="!isSeting">
            <div>
              <span>{{ t('referPop.TIPO') }}</span>
              <span class="text_hiding">CPF</span>
            </div>

            <div>
              <span>{{t('refer.Nome')}}</span>
              <span class="text_hiding">{{ store.state.user.username }}</span>
            </div>

            <div>
              <span>CPF</span>
              <span class="text_hiding">{{ store.state.user.CPF }}</span>
            </div>
          </div>
          <div v-if="isSeting" class="seting">
            <el-input v-model="type" :disabled="true" class="TIPO">
              <template #prepend>
                <p class="head">{{ t('referPop.TIPO') }}</p>
              </template>
            </el-input>

            <Rinput @changeInputState="changeInputState" @inputChangeData="inputFun" :inputFoucs="inputFoucs"
              :headTxt="t('refer.Nome')" :inputRed="inputTxtRed" :data="name" :isHead="false" :popTxt="t('referPop.Digitenomeverdadeiro')">
            </Rinput>

            <Rinput @changeInputState="changeInputStateCPF" @inputChangeData="inputFunCPF" :inputFoucs="inputFoucsCPF"
              :headTxt="'CPF'" :inputRed="inputTxtRedCPF" :data="CPF" :isHead="false"
              :popTxt="t('referPop.Entrefundoprevidência')">
            </Rinput>
          </div>
          <!-- <div class="setting_btn" @click="settings(1)">{{ t('base.SETTINGS') }} ></div> -->
        </div>

        <div class="r_box">
          <p>{{t('base.currencySymbol')}} {{ store.state.user.commission }}</p>
          <span>{{ t('referPop.MinhasComissões') }}</span>

        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import {
  reactive,
  toRefs,
  getCurrentInstance,
  defineComponent,
  computed,
  nextTick
} from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import Rinput from "./input.vue";
import { UserService } from "@/api/user";
import { getUserInfoNoLoad } from "@/utils/baseFun";
export default defineComponent({
  name: "withdrawalInformation",
  components: { Rinput },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const state = reactive({
      isSeting: false,
      type: 'CPF',
      name: store.state.user.username,
      inputFoucs: false,
      inputTxtRed: 1,
      inputFoucsCPF: false,
      inputTxtRedCPF: 1,
      CPF: store.state.user.CPF,
      isOne: false,
    });

    if (state.name) {
      state.inputFoucs = true;
    }
    if (state.CPF) {
      state.inputFoucsCPF = true;
    }
    nextTick(() => {
      if (!state.CPF && !state.name) {

        state.isSeting = true;

      }
    })


    const Mudar = () => {
      if (state.name) {
        state.inputFoucs = true;
      }
      if (state.CPF) {
        state.inputFoucsCPF = true;
      }
      state.isOne = false;
      state.isSeting = true;
    }

    const settings = (val: number) => {
      proxy.$mitt.emit("depositComShow2", val);
    };

    const changeInputState = (val, data) => {
      if (state.inputTxtRed == 1 && val == 'blur') {
        state.inputTxtRed = 0;
      }
      if (!data) {
        state.inputFoucs = !state.inputFoucs;
      }

      state.isSeting = true;
    }

    const inputFun = (val) => {
      if (val != '') {
        state.inputTxtRed = 2;

      } else {
        state.inputTxtRed = 0;

      }
      state.name = val;
    }

    const changeInputStateCPF = (val, data) => {
      if (state.inputTxtRedCPF == 1 && val == 'blur') {
        state.inputTxtRedCPF = 0;
      }
      if (!data) {
        state.inputFoucsCPF = !state.inputFoucsCPF;
      }
    }

    const inputFunCPF = (val) => {
      if (val != '') {

        state.inputTxtRedCPF = 2;
      } else {
        state.inputTxtRedCPF = 0;
      }
      state.CPF = val;
    }
    function saveUserInfo() {
      UserService.bind_user_withdrawal_info({ cpf: state.CPF, username: state.name }).then((res) => {
        if (res.data.code == 1) {
          getUserInfoNoLoad()
        }
      })
    }
    const save = () => {
      if (state.name != '' && state.CPF != '') {
        UserService.bind_user_withdrawal_info({ cpf: state.CPF, username: state.name }).then((res) => {
          if (res.data.code == 1) {
            getUserInfoNoLoad()

            state.isSeting = false;
          }
        })
      } else {
        const data = {
          cpf: '',
          name: '',
          pix: 'CPF',
        }

      }
    }
    proxy.$mitt.on("err", () => {
      state.inputTxtRed = 0;
    })
    proxy.$mitt.on("save", () => {
      if (state.name != '' && state.CPF != '') {
        UserService.bind_user_withdrawal_info({ cpf: state.CPF, username: state.name }).then((res) => {
          if (res.data.code == 1) {
            getUserInfoNoLoad()
          }
        })
      } else {
        const data = {
          cpf: '',
          name: '',
          pix: 'CPF',
        }
        store.dispatch('saveUserData/setWithdrawalSettings', data);
      }
      if (store.state.user.username && store.state.user.CPF) {
        state.isSeting = false;
      }

    });
    return {
      ...toRefs(state),
      t,
      store,
      settings,
      changeInputState,
      inputFun,
      changeInputStateCPF,
      inputFunCPF,
      save,
      Mudar,
    };
  },
});
</script>
<style  lang="scss" scoped>
.head {
  width: 100%;
  text-align: left;
}

.withdrawalInformation {
  margin-bottom: 16px;



  :deep(.el-input__wrapper) {

    background: none;
    box-shadow: none;

    input {
      color: #fff;
      --el-input-inner-height: 40px;
      font-size: 14px;
    }

  }

  :deep(.el-input-group__prepend) {
    background: none;
    box-shadow: none;
    padding: 0 0 0 13px;
  }

  .boder {
    border: 1px solid rgba(178, 182, 197, 0.3);
    border-radius: 6px;
    margin-bottom: 12px !important;
    padding-left: 15px !important;
    padding-right: 9px !important;
  }

  .withdraw_mode {
    .txt_box {
      display: flex;
      flex-direction: column;
      // margin-right: 16px;
      // gap: 16px;

      .l_box {
        width: 100%;
        flex-shrink: 0;
        position: relative;
        padding: 12px 0 10px 0;
        // background: var(--auxiliary-background-14);
        // border-radius: 0px 0px 8px 8px;
        box-sizing: border-box;
        margin-bottom: 6px;

        .header_box {
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
          border-radius: 8px 8px 0px 0px;
          box-sizing: border-box;
          color: #B2B6C5;

          >div:nth-child(1) {
            font-size: 17px;
            font-weight: 500;
            display: flex;
          }

          .Conta {
            width: 16px;
            margin-left: 12px;
          }

          &:first-child {
            display: flex;
            align-items: center;
            font-size: 16px;
          }

          .btns {
            display: flex;
            align-items: center;
            gap: 12px;

            &>div:first-child {
              color: #EB4859;
              border: #EB4859 1px solid;
              padding: 0 7px;
            }

            &>div:last-child {
              color: #7EC050;
              border: #7EC050 1px solid;
            }
          }

          .btn {
            width: 52px;
            height: 20px;
            border-radius: 43.5px;
            border: 1px solid #B2B6C5;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 12px;
          }
        }

        .c_box {
          margin-top: 9px;
          height: 100%;
          box-sizing: border-box;
        }

      }

      .l_box {
        .c_box {
          >div {
            display: grid;
            grid-template-columns: 15% 1fr;
            margin-bottom: 12px;

            span:nth-child(1) {
              font-size: 14px;
              font-weight: 500;
              color: #B2B6C5;
            }

            span:nth-child(2) {
              display: inline-block;
              width: 100%;
              font-size: 14px;
              font-weight: 500;
              color: var(--auxiliary-font-color-7);
            }
          }
        }
      }

      .seting {
        margin-top: 13px;
        display: flex;
        flex-direction: column;
        gap: 15px;

        .TIPO {
          box-shadow: 0 0 0 1px #7EC050 inset !important;
          border-radius: 6px;

          // display: grid;
          // grid-template-columns: 20% 1fr;
          :deep(.el-input-group) {

            color: #7EC050 !important;


            input {
              // color: #FFFFFF !important;
            }
          }

          :deep(.el-input__wrapper) {

            // box-shadow: 0 0 0 1px #7EC050 inset !important;
            input {
              color: #7EC050 !important;
              -webkit-text-fill-color: #7ec050;
            }
          }


        }
      }

      .r_box {
        // width: 50%;
        padding: 24.5px 0;
        flex-shrink: 0;
        background: #2F3445;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        p {
          color: #82F44E;
          font-size: 20px;
          margin-bottom: 20px;
        }

        span {
          color: #B2B6C5;
          font-size: 16px;
        }
      }
    }
  }

  :deep(.el_popover_style) {
    background: var(--auxiliary-background-14);
    border: none;
    border-radius: 12px;

    .popover_content {
      // width: 200px;

      .popover_content_header {
        margin-bottom: 12px;
        font-size: 16px;
        font-weight: bold;
        color: var(--theme-font-color-fff);
      }

      .popover_content_txt {
        font-size: 14px;
        font-weight: 400;
        color: var(--auxiliary-font-color-9);
        line-height: 16px;
      }

      .popover_content_btn {
        text-align: right;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        color: var(--auxiliary-font-color-27);
      }
    }

    .el-popper__arrow {
      &::before {
        background: var(--auxiliary-background-14);
        border: none;
      }
    }
  }
}

@media (max-width: 768px) {
  .withdrawalInformation {
    .withdraw_mode {
      .txt_box {
        .l_box {
          padding: 7px 0px 0px 0px;
          border-radius: 6px 6px 6px 6px;
          // border: 1px solid rgba(178, 182, 197, 0.3);
          margin-bottom: 12px;

          .header_box {
            >div:nth-child(1) {
              font-size: 14px;

              img {
                width: 13px;
              }
            }
          }
        }

        .r_box {
          border-radius: 6px;
          // margin-bottom: 16px;

          p {
            font-size: 18px;
            margin-bottom: 21px;
          }

          span {
            font-size: 16px;
          }
        }

      }


    }
  }

}
</style>
  