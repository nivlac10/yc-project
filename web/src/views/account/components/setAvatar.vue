<template>
  <div class="setAvatar">
    <el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
      :width="store.state.status.isPc ? '335px' : '100%'">
      <div class="setAvatar_content">
        <img class="close_img" src="@assets/images/public/Shutdownx.png" alt="" @click="closeCom" />
        <div class="change_uesrname">
          <div class="label">{{ t('account.ChangeUsername') }}</div>
          <div class="edit_name_input">
            <svg-icon name="edit" color="#B2B6C5" />
            <el-input v-model="nikename" placeholder="" />
          </div>
        </div>
        <div class="avatar_list">
          <div class="label">{{ t('account.ChangeAvatar') }}</div>
          <ul>
            <li :class="{ active: avatarIdx == index }" v-for="(item, index) in 19" :key="index"
              @click="avatarIdx = index">
              <div class="img_mask"></div>
              <img :src="getImageUrl(`avatar/headsculpture_img_${index}.png`)" alt="" />
            </li>
          </ul>
        </div>
        <div class="btn" @click="setInfo">{{ t('btnName.CONFIGURAÇÕES') }}</div>
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
import { debounce, getImageUrl, getUserInfo } from "@/utils/baseFun";
import { UserService } from "@/api/user";
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "setAvatar",
  setup() {
    const router = useRouter();
    const store = useStore();
    const { proxy } = getCurrentInstance() as any;
    const { t } = useI18n();
    const state = reactive({
      dialogVisible: true,
      nikename: store.state.user.nickname,
      avatarIdx: store.state.user.header_img,
    });

    const closeCom = () => {
      proxy.$mitt.emit("showCom", -1);
    };

    const setInfo = () => {
      const fun = () => {
        UserService.change_user_info({
          nickname: state.nikename,
          header_img: state.avatarIdx,
        }).then((res) => {
          if (res.data.code == 1) {
            getUserInfo();
            closeCom();
          }
        });
      };
      debounce(fun);
    };

    return { ...toRefs(state), store, t, getImageUrl, closeCom, setInfo };
  },
});
</script>
<style  lang="scss" scoped>
.setAvatar {
  .setAvatar_content {
    position: relative;
    width: 100%;
    padding: 40px 22px 32px 22px;
    box-sizing: border-box;
    background: #202330;
    border-radius: 16px;

    .close_img {
      cursor: pointer;
      position: absolute;
      top: 18px;
      right: 20px;
      width: 20px;
    }

    .label {
      margin-bottom: 20px;
      font-size: 16px;
      font-weight: 600;
      color: #B2B6C5;
    }

    .change_uesrname {
      margin-bottom: 22px;

      .edit_name_input {
        position: relative;

        .svg-icon {
          position: absolute;
          top: 50%;
          z-index: 1;
          left: 15px;
          transform: translateY(-50%);
          width: 20px;
          height: 20px;
        }

        :deep(.el-input) {
          background: #1B1F29;
          border-radius: 6px;
          border: 1px solid rgba(178, 182, 197, 0.3);

          .el-input__wrapper {
            padding: 9px 0 9px 60px;
            box-shadow: none;
            border-radius: 9px;
            background: transparent;

            input {
              border: none;
              color: var(--theme-font-color-fff);
            }
          }
        }
      }
    }

    .avatar_list {
      ul {
        padding: 0 0 22px 0;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        column-gap: 16px;
        row-gap: 12px;

        li {
          cursor: pointer;
          position: relative;
          box-sizing: border-box;

          &.active {
            .img_mask {
              display: none;
            }
          }

          .img_mask {
            position: absolute;
            width: 61px;
            height: 61px;
            border-radius: 50%;
            background: rgba($color: #000000, $alpha: 0.6);
          }

          img {
            width: 61px;
          }
        }
      }
    }

    .btn {
      cursor: pointer;
      line-height: 42px;
      text-align: center;
      border-radius: 8px;
      font-size: 16px;
      font-weight: bold;
      color: var(--theme-font-color-fff);
      background: #4181EE;

      &:hover {
        background: #6DA3FF;
      }
    }
  }
}

@media (max-width: 768px) {
  .setAvatar {
    .setAvatar_content {
      margin: 0 12px;
      padding: 35px 20px;

      .label {
        font-size: 16px;
      }

      .change_uesrname {
        .edit_name_input {
          img {
            width: 20px;
          }

          :deep(.el-input) {
            .el-input__wrapper {
              padding: 3px 0 3px 50px;
            }
          }
        }
      }

      .avatar_list {
        ul {
          column-gap: 20px;
          row-gap: 10px;

          li {
            .img_mask {
              width: 58px;
              height: 58px;
            }

            img {
              width: 58px;
            }
          }
        }
      }

      .btn {
        height: 38px;
        line-height: 38px;
        font-size: 16px;
      }
    }
  }
}
</style>
