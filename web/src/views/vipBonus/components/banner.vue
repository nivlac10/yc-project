<template>
  <div class="vipBonus_banner">
    <div class="title">
      <p>	{{ t('vipBonus.BÔNUSAVANÇODENÍVEL') }}</p> 
      <infoPop :title="	t('vipBonus.nívelanterior') "
        :content="t('vipBonus.nívelanteriorTxt')"></infoPop>
    </div>
    <el-carousel ref="carousel" :autoplay="false" arrow="always" :loop="false" :height="`${bannerHeight}px`">
      <el-carousel-item v-for="(item, index) in arrContent" :key="index">
        <el-row :gutter="10">
          <el-col v-for="(item2, index2) in (item as any)" :key="index2" :xs="24" :sm="8" :md="8" :lg="8" :xl="8">
            <!-- <vip-box :data="item2" />  -->
            <vipBox2 :data="item2" :currentId="currentId" :nextId="nextId" @def="getBounsStatus()"></vipBox2>
          </el-col>
        </el-row>
      </el-carousel-item>
    </el-carousel>
    <div class="bottom" @click="jump">
      <p>{{ t('vipBonus.Vertodasasnotas') }} <img src="@/assets/images/vipBonus/arrow.png" alt=""></p>

    </div>
  </div>
</template>
<script lang="ts">
import {
  reactive,
  computed,
  watch,
  toRefs,
  nextTick,
  getCurrentInstance,
  defineComponent,
  onMounted,
  ref,
} from "vue";
import router from "@/router";
import { useStore } from "@/store/index";
import vipBox from "./vipBox.vue";
import { sliceArr } from "@/utils/baseFun";
import { getImageUrl, levelName } from "@/utils/baseFun";
import vipBox2 from "./vipBox2.vue";
import infoPop from "./infoPop.vue";
import { VipService } from "@/api/vip";
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "vipBonus_banner",
  components: { vipBox, vipBox2, infoPop },
  setup() {
    const store = useStore();
    const {t} = useI18n();
    const state = reactive({
      bannerHeight: store.state.status.isPc ? 532 : 512,
      arr: store.state.conf.all_conf.vip_conf,
      arrContent: [],
      colors: [
        '#E0A685',
        '#E0A685',
        '#C3D3FF',
        '#E4C274',
        '#8BD5F1',
        '#E284D0',
        '#EC5B60',
        '#9EF6EE',
      ],
      imgs: [
        getImageUrl('vipBonus/level_0.png'),
        getImageUrl('vipBonus/level_1.png'),
        getImageUrl('vipBonus/level_2.png'),
        getImageUrl('vipBonus/level_3.png'),
        getImageUrl('vipBonus/level_4.png'),
        getImageUrl('vipBonus/level_5.png'),
        getImageUrl('vipBonus/level_6.png'),
        getImageUrl('vipBonus/level_7.png'),
      ],
      vip_arr: [],
      nextId: 0,
      currentId: 0
    });
    let vip_all_arr = store.state.conf.all_conf.vip_conf
    for (let i = 0; i < vip_all_arr.length; i++) {
      for (let j = 0; j < vip_all_arr[i].vip_low_lv.length; j++) {
        let vip_conf: any = vip_all_arr[i].vip_low_lv[j] as any
        vip_conf.name = levelName(vip_conf.vip_lv)
        vip_conf.pay_fee = vip_all_arr[i].pay_fee
        vip_conf.day_max_withdraw = vip_all_arr[i].day_max_withdraw
        vip_conf.withdraw_num = vip_all_arr[i].withdraw_num
        vip_conf.color = state.colors[vip_all_arr[i].vip_lv]
        vip_conf.img = state.imgs[vip_all_arr[i].vip_lv]
        vip_conf.state = 0
        let rate = vip_conf.need_code_amount / 100
        let vip_up_rate = store.state.user.total_bet / rate

        // console.log(store.state.user.total_bet, vip_conf.need_code_amount, rate, vip_up_rate);
        vip_conf.rate = vip_up_rate.toFixed(2)
        state.vip_arr.push(vip_conf as never)

      }
    }

    const getBounsStatus = () => {
      VipService.get_user_vip_up_bonus_state().then((res) => {
        // console.log(res);
        let data = res.data.data
        for (let i = 0; i < data.length; i++) {
          for (let j = 0; j < state.vip_arr.length; j++) {
            if (data[i].id == state.vip_arr[i]['id']) {
              // @ts-ignore
              state.vip_arr[i].state = data[i].state
            }
          }
        }

        state.nextId = (res.data.data as any)[0].id
        for (let i = 0; i < res.data.data.length; i++) {
          const element: any = res.data.data[i];
          if (store.state.user.vip_lv == element.vip_lv && store.state.user.vip_low_lv == element.lv) {
            state.currentId = element.id
            if (i + 1 >= res.data.data.length) state.nextId = 0
            else state.nextId = (res.data.data as any)[i + 1].id
          }
        }
      })
    }
    getBounsStatus();

    onMounted(() => {
      nextTick(() => {
        // const vipBoxEl: any = document.querySelector(".vipBox");
        // state.bannerHeight = vipBoxEl.clientHeight;
        const carousel__arrow: any = document.querySelector(
          ".el-carousel__arrow"
        );
        // var afterStyle = window.getComputedStyle(carousel__arrow, ":after")
        // afterStyle.height = state.bannerHeight + 'px'
        // console.log(afterStyle.height);
      });
    })
    const carousel = ref(null)
    watch(
      () => store.state.status.isPc,
      (val: boolean) => {
        state.arr.map((v, i) => {
          state.arr[i].color = state.colors[i];
          state.arr[i].img = state.imgs[i];
        })
        state.arrContent = sliceArr(state.vip_arr, val ? 3 : 1);
        for (let i = 0; i < state.arrContent.length; i++) {
          const element: any = state.arrContent[i];
          for (let j = 0; j < element.length; j++) {
            const element2 = element[j];
            if (store.state.user.vip_lv == element2?.vip_lv && store.state.user.vip_low_lv == element2?.lv) {
              nextTick(() => {
                (carousel.value as any).setActiveItem(i)
              })
            }
          }
        }

        // console.log('arrContent', state.arrContent);

      },
      { deep: true, immediate: true }
    );
    const jump = () => {
      router.push('/vipBonus/allLevels')
    }
    return { ...toRefs(state), jump, getBounsStatus, carousel,t };
  },
});

</script>
<style  lang="scss" scoped>
.vipBonus_banner {

  background: #202431;
  box-sizing: border-box;
  padding: 35px 24px 26px 24px;
  border-radius: 12px;

  .title {
    margin-left: 8px;
    display: flex;
    align-items: center;

    p {
      color: #B2B6C5;
      font-size: 24px;
      font-weight: bold;
    }


    div {
      width: 28px;
      height: 28px;
      // background: #C3CFD9;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      font-weight: bold;
      font-size: 20px;
      color: #404958;
      margin-left: 10px;
      cursor: pointer;
    }

    margin-bottom: 31px;
  }

  :deep(.el-carousel) {
    .el-carousel__container {
      // min-height: 646px;

      border-radius: 16px;
      overflow: hidden;
    }

    .el-carousel__arrow {
      background: #2F3445;
      width: 24px;
      height: 57px;
      border-radius: 0;
      top: 128px;

      .el-icon {
        font-size: 21px;
        font-weight: 900;
        color: #C3CFD9;
      }

      background: rgba(0, 0, 0, 0.4);

      &:hover {
        background: #4181EE;

        &::after {
          content: "";
          position: absolute;
          top: -100px;
          height: 532px;
          width: 48px;
          background: rgba($color: #000000, $alpha: 0.1);
        }
      }
    }

    .el-carousel__arrow--left {
      left: 0;
      border-top-right-radius: 12px;
      border-bottom-right-radius: 12px;

    }



    .el-carousel__arrow--right {
      right: 0;
      border-top-left-radius: 12px;
      border-bottom-left-radius: 12px;
    }




    .el-carousel__indicators {
      display: none;
    }
  }


  .bottom {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 15px;
    cursor: pointer;

    p {
      color: #4181EE;
      font-size: 16px;
      font-weight: bold;
      display: flex;
      align-items: center;
    }


    img {
      width: 19px;
      height: 21px;
      margin-top: 2px;
    }
  }
}

@media (max-width: 768px) {
  .vipBonus_banner {
    padding: 19px 12px;
    border-radius: 12px;

    .title {
      margin: 0 0 18px 5px;

      p {
        font-size: 14px;
      }

      div {
        width: 16px;
        height: 16px;
        font-size: 16px;

      }
    }

    :deep(.el-carousel) {
      .el-carousel__container {
        // min-height: 646px;
      }

      .el-carousel__arrow {
        &:hover {
          background: rgba(0, 0, 0, 0.4);

          &::after {
            width: 0;
          }
        }

        &:active {
          background: #4181EE;

          &::after {
            content: "";
            position: absolute;
            top: -100px;
            height: 499px;
            width: 48px;
            background: rgba($color: #000000, $alpha: 0.1);
          }
        }
      }
    }

    .bottom {
      margin: 0;

      p {
        font-size: 13px;
      }

      span {
        font-size: 15px;
      }
    }
  }
}
</style>
