<template>
  <div class="tabbar">
    <van-tabbar v-model="active" :safe-area-inset-bottom="true" placeholder z-index="999">
      <van-tabbar-item v-for="(item, index) in icon" :key="index" @click="tabClick()">
        <span>{{ item.title }}</span>
        <img src="@/assets/images/public/Label.png" alt="" class="moneyLable" v-if="!item?.path">
        <template #icon="props">
          <img :src="props.active ? item.active : item.inactive" />
        </template>
      </van-tabbar-item>
    </van-tabbar>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed, watch } from "vue";
import { useStore } from "@/store/index";
import { getImageUrl } from "@/utils/baseFun";
import router from "@/router";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";
export default defineComponent({
  name: "tabbar_com",
  setup() {
    const store = useStore();
    const { proxy } = getCurrentInstance() as any;
    const { t } = useI18n();
    const route = useRoute()
    const state = reactive({
      active: 0,
      icon: [
        {
          active: getImageUrl("tabbar/Jogos_selected_icon.png"),
          inactive: getImageUrl("tabbar/Jogos_icon.png"),
          title: computed(()=>t('gameText.Jogos')),
          path: '/'
        },
        {
          active: getImageUrl("tabbar/Convite_selected_icon.png"),
          inactive: getImageUrl("tabbar/Convite_icon.png"),
          title: computed(()=>t('gameText.Convite')),
          path: '/refer'
        },
 
        {
          active: getImageUrl("tabbar/deposito.png"),
          inactive: getImageUrl("tabbar/deposito.png"),
          title:  computed(()=>t('gameText.Depósito')),
        },
        {
          active: getImageUrl("tabbar/Bônus_selected_icon.png"),
          inactive: getImageUrl("tabbar/Bônus_icon.png"),
          title:  computed(()=>t('gameText.Bônus')),
          path: '/TodosOsBouns'
        },
        { 
          active: getImageUrl("tabbar/Account_selected_icon.png"),
          inactive: getImageUrl("tabbar/Account_icon.png"),
          title:  computed(()=>t('gameText.Conta')),
          path: 'userHead'
        },
    
      ],
    });
    const tabClick = () => {
      store.state.status.sidebarIsShow = false;
      proxy.$mitt.emit("showInfo", { type: 1, val: false });
      store.state.status.showDeposito = false;
      if (state.active == 0) {
        router.push("/");
      } else if (state.active == 1) {
  
        router.push("/refer");
      } else if (state.active == 2) {
        if (store.state.user.token)
          store.state.status.depositShow = true
        else store.dispatch('status/setLoginShow', true)
      } else if (state.active == 3) {
        router.push("/bonusCabinet");
      } else if (state.active == 4) {
        proxy.$mitt.emit("showInfo", { type: 0, val: "" });
      }
    };

    // tab选中
    const tabActive = (path) => {
      for (let i = 0; i < state.icon.length; i++) {
        const elementI = state.icon[i];
        if (elementI.path) if (path == elementI.path) state.active = i
      }
      if (store.state.status.depositShow) state.active = 2
    }
    watch(() => route, (to, from) => {
      tabActive(to.path)
    }, { deep: true, immediate: true })
    watch(() => [store.state.status.depositShow, store.state.status.loginShow], (val) => {
      tabActive(route.path)
    }, { deep: true, immediate: true })

    return { ...toRefs(state), tabClick };
  },
});
</script>
<style  lang="scss" scoped>
.tabbar {
  display: none;

  :deep(.van-tabbar) {
    height: 70px;

    &::after {
      display: none;
    }

    background: var(--theme-navigationbar-background);

    .van-tabbar-item:nth-child(3) {
      position: relative;

      &::after {
        content: '';
        position: absolute;
        top: -10px;
        background: #D9384E;
        border-radius: 50%;
        width: 75px;
        height: 75px;
      }

      &::before {
        content: '';
        position: absolute;
        top: -17px;
        background: var(--theme-navigationbar-background);
        border-radius: 50%;
        width: 90px;
        height: 90px;
      }

      .van-tabbar-item__icon,
      span {
        position: relative;
        top: -10px;
        z-index: 1;
        color: #fff;
      }

      span {
        top: -20px;
      }
      .moneyLable {
          width: 40px;
          height: 40px;
          position: absolute;
          top: 5px;
          right: -15px;
          animation: zy 3.5s .15s linear infinite;
          transform-origin:50% 0;
          z-index: 10;
        }
    }

    .van-tabbar-item--active {
      background: transparent;

      // span {
      //   color: var(--photoeffect-font-color) !important;
      //   text-shadow: 0px 0px 12px var(--photoeffect-shadow-color),
      //     0px 0px 8px var(--photoeffect-shadow-color),
      //     0px 0px 10px var(--photoeffect-shadow-color) !important;
      // }
    }

    .van-tabbar-item__icon {
      margin-bottom: 10px;

      img {
        width: 30px;
        height: 30px;
      }
    }

    .van-tabbar-item__text {
      text-align: center;

      span {
        position: relative;
        top: -10px;
        font-size: 12px;
        color: #98ABD0;
      }
    }
  }
}

@media screen and (max-width: 768px) {
  .tabbar {
    display: block;
  }
}

@-webkit-keyframes zy {
  10% {
    transform: rotate(20deg);
  }

  20% {
    transform: rotate(-20deg);
  }

  30% {
    transform: rotate(20deg);
  }

  40% {
    transform: rotate(-20deg);
  }

  50%,
  100% {
    transform: rotate(0deg);
  }
}
</style>
