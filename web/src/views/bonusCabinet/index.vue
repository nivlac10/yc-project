<template>
  <div class="bonusCabinet">
    <barckTitle :backNameShow="false" :title="t('bonusCabinet.BônusGabinete')" />
    <div class="box" v-for="(item, index) in list" :key="index">
      <div class="box_column">
        <div class="box_column_l_box">{{ item.columnTitle }}</div>
        <div class="box_column_r_box" v-if="index == 0">
          <img src="@assets/images/bonusCabinet/Group.png" alt="">
          <input v-model="couponCode" type="text" :placeholder="t('bonusCabinet.InserirCódigodeCupom')">
          <div class="sl_box_shadow_green" @click="receive_code">{{ t('btnName.Receber') }}</div>
        </div>
      </div>
      <ul>
        <li v-for="(item2, index2) in (item.arr as any)" :key="item2.title">
          <div class="l_box">
            <img :src="item2.img" alt="">
            <div class="l_box_content">
              <div class="l_box_content_top">
                <span>{{ item2.title }}</span>
                <!-- <img src="@assets/images/public/query.png" alt=""> -->
                <question-popup :id="item2.id" v-if="item2.id != 4 && item2.id != 10 && item2.id != 13" />
                <img class="level_img" v-if="item2.id == 1"
                  :src="getImageUrl(`vipBonus/level_${store.state.user.vip_lv}.png`)" alt="" @click="showLevelDeltas">
              </div>
              <div class="l_box_content_bottom" v-if="item2.title2">
                <span :style="`color: ${item2.id == 4 ? '#75ED3D' : ''}`">{{ item2.title2 }}</span>
                <span style="color: #75ED3D;" v-if="item2.id == 4">{{ moneyFormat(item2.total_money) }}</span>
              </div>
            </div>
          </div>
          <div v-if="item2.id == 1"
            :class="{ r_box: true, [item2.className]: true, sl_box_shadow_mask: item2.state == 0 }"
            @click="btnClick(item2)">
            <el-countdown v-if="item2.state == 0" title="" format="HH:mm:ss"
              :value="Date.now() + (store.state.vipBonusState.sgin_data['time'] * 1000)" @finish="finish" />
            <span v-else>{{ item2.money == 0 ? item2.btnName :
              `${t('base.currencySymbol')}${item2.money}` }}</span>
          </div>
          <div v-else-if="item2.id == 2"
            :class="{ r_box: true, [item2.className]: true, sl_box_shadow_mask: item2.state == 0 }"
            @click="btnClick(item2)">
            <span>{{ item2.btnName }}</span>
          </div>
          <div v-else-if="item2.id == 3"
            :class="{ r_box: true, [item2.className]: true, sl_box_shadow_mask: item2.state == 0 || item2.state == 2 }"
            @click="btnClick(item2)">
            <span>{{ item2.btnName }}</span>
          </div>
          <div v-else-if="item2.id == 4" :class="{
            r_box: true, [item2.className]: true, sl_box_shadow_mask: store.state.vipBonusState.split_bonus.state == 0,
            r_box_flex: store.state.vipBonusState.split_bonus.state == 0 && store.state.vipBonusState.split_bonus.time > 0
          }" @click="router.push('/vipBonus')">
            <p v-if="store.state.vipBonusState.split_bonus.money > 0">{{ t('btnName.Receber') }} {{
              store.state.vipBonusState.split_bonus.money > 0 ?
              store.state.vipBonusState.split_bonus.money < 0.01 ? `<${moneyFormat(0.01)}` :
                moneyFormat(store.state.vipBonusState.split_bonus.money) : '' }}</p>
                <p v-if="store.state.vipBonusState.split_bonus.wait_money > 0">
                  {{ t('btnName.Receber') }} {{ store.state.vipBonusState.split_bonus.wait_money > 0
                    ? store.state.vipBonusState.split_bonus.wait_money < 0.01 ? `<${moneyFormat(0.01)}` :
                      moneyFormat(store.state.vipBonusState.split_bonus.wait_money) : '' }} </p>
                    <p
                      v-if="store.state.vipBonusState.split_bonus.state == 0 && store.state.vipBonusState.split_bonus.time == 0">
                      {{ t('btnName.Receber') }}
                    </p>
                    <p class="btn2_item_1_p"
                      v-if="store.state.vipBonusState.split_bonus.state == 0 && store.state.vipBonusState.split_bonus.time > 0">
                      {{ t('bonusCabinet.Em') }} {{ store.state.vipBonusState.split_time }}
                    </p>
          </div>
          <el-tooltip v-else-if="item2.id == 5" popper-class="el-tooltip_bg" effect="customized"
            :content="'Abriu a fechadura às ' + store.state.vipBonusState.now_time" placement="top"
            :disabled="store.state.vipBonusState.now_bonus.time <= 0">
            <div @click="get_bonus(1)"
              :class="{ r_box: true, [item2.className]: true, sl_box_shadow_mask: store.state.vipBonusState.now_bonus.state == 0, sl_box_shadow_mask_events: true }">
              <p>{{ t('btnName.Adicionar') }} {{ store.state.vipBonusState.now_bonus.money > 0 ?
                moneyFormat(store.state.vipBonusState.now_bonus.money) : '' }}</p>
            </div>
          </el-tooltip>
          <div v-else-if="item2.id == 6"
            :class="{ r_box: true, [item2.className]: store.state.vipBonusState.day_bonus.time == 0, sl_box_shadow_mask: store.state.vipBonusState.day_bonus.state == 0, no_bonus_box: store.state.vipBonusState.day_bonus.time > 0 }"
            @click="get_bonus(2)">
            <img v-if="btn_loading_2" src="@assets/images/public/btn_loading.gif" alt="">
            <img v-if="store.state.vipBonusState.day_bonus.state == 0 && store.state.vipBonusState.day_bonus.time != 0"
              src="@assets/images/header/RETIRADA@2x.png" alt="">
            <!-- <img v-else src="../../../assets/images/refer/RETIRADA.png" alt=""> -->
            <p v-if="store.state.vipBonusState.day_bonus.state == 1">{{ t('btnName.Adicionar') }}</p>
            <p v-if="store.state.vipBonusState.day_bonus.time > 0">{{ store.state.vipBonusState.day_time }}</p>
            <p v-if="store.state.vipBonusState.day_bonus.state == 0 && store.state.vipBonusState.day_bonus.time == 0">
              {{ t('btnName.Adicionar') }}</p>
          </div>
          <div v-else-if="item2.id == 7"
            :class="{ r_box: true, [item2.className]: true, sl_box_shadow_mask: store.state.vipBonusState.week_bonus.state == 0 }"
            @click="get_bonus(3)">
            <img v-if="btn_loading_3" src="@assets/images/public/btn_loading.gif" alt="">
            <p>{{ t('btnName.Adicionar') }}</p>
          </div>
          <div v-else-if="item2.id == 8"
            :class="{ r_box: true, [item2.className]: true, sl_box_shadow_mask: store.state.vipBonusState.month_bonus.state == 0 }"
            @click="get_bonus(4)">
            <img v-if="btn_loading_4" src="@assets/images/public/btn_loading.gif" alt="">
            <p>{{ t('btnName.Adicionar') }}</p>
          </div>
          <div v-else-if="item2.id == 9 || item2.id == 10 || item2.id == 11"
            :class="{ r_box: true, [item2.className]: true, sl_box_shadow_mask: item2.state == 0 }"
            @click="btnClick(item2)">
            <span>{{ item2.btnName }}</span>
          </div>
          <div v-else-if="item2.id == 13"
            :class="{ r_box: true, [item2.className]: true, sl_box_shadow_mask: item2.state > 0 }"
            @click="btnClick(item2)">
            <span>{{ store.state.status.isApk ? item2.btnName : t('btnName.BaixaroAPP') }}</span>
          </div>
          <div v-else :class="{ r_box: true, [item2.className]: true, sl_box_shadow_mask: item2.state == 2 }"
            @click="btnClick(item2)">
            <span>{{ item2.btnName }}</span>
          </div>
        </li>
      </ul>
      <div class="show_more" v-if="item.showMoreName" @click="router.push(item.path)">
        <span>{{ item.showMoreName }}</span><img src="@assets/images/public/arrow_blue.png" alt="">
      </div>
    </div>

    <div v-if="isBonusPop" class="bounsPop_box  mask" @click="isBonusPop = false">
      <div class="pop_box" @click.stop>
        <bounsPop :comIdx="comIdx" :now_bonus="now_bonus_pop" :split_bonus="split_bonus_pop"
          @close-pop="isBonusPop = false"></bounsPop>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import barckTitle from "@/components/back/index.vue";
import { getImageUrl, moneyFormat, getUserInfoNoLoad, debounce, getUserInfo, downloadAPK, } from "@/utils/baseFun";
import questionPopup from "./components/questionPopup.vue"
import promptPopup from "@/components/promptPopup/index";
import { UserService } from "@/api/user";
import { VipService } from "@/api/vip";
import { giveCode } from "@/api/giveCode"
import bounsPop from '@/views/vipBonus/components/bounsPop.vue';
import { bonusCabinetFun } from "@/utils/startInterface";
import { ElNotification } from "element-plus";

export default defineComponent({
  name: "bonusCabinet",
  components: { barckTitle, questionPopup, bounsPop },
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      couponCode: '',
      list: [
        {
          columnTitle: computed(() => t('bonusCabinet.ATIVIDADESDIÁRIAS')),
          arr: [
            { id: 1, className: 'sl_box_shadow', img: getImageUrl('bonusCabinet/calendar.png'), title: computed(() => t('bonusCabinet.BônusEntrada')), btnName: computed(() => t('btnName.Checkin')), state: 2 },
            { id: 13, className: 'sl_box_shadow', img: getImageUrl('bonusCabinet/Download.png'), title: computed(() => t('bonusCabinet.Bônusdebaixaroapp')), title2: computed(() => t('bonusCabinet.Baixeereceba')), btnName: computed(() => t('btnName.Receber')), state: 1 },
            { id: 3, className: 'sl_box_shadow', img: getImageUrl('bonusCabinet/Chest.png'), title: computed(() => t('bonusCabinet.BônusPerdido')), btnName: computed(() => t('btnName.Receber')), state: 0 },
            { id: 11, className: 'sl_box_shadow', img: getImageUrl('bonusCabinet/Free_slot_machines.png'), title: computed(() => t('bonusCabinet.SlotGrátis')), btnName: computed(() => t('btnName.Rodar')), state: 0 },
          ],
        },
        {
          columnTitle: computed(() => t('bonusCabinet.RECOMPENSASCALENDÁRIO')),
          showMoreName: computed(() => t('bonusCabinet.showMoreName1')),
          path: '/vipBonus',
          arr: [
            { id: 4, className: 'sl_box_shadow_green', img: getImageUrl('bonusCabinet/Chest_1.png'), title: computed(() => t('bonusCabinet.Calendário')), title2: computed(() => t('bonusCabinet.Pendentes')), btnName: computed(() => t('btnName.Receber')) },
            { id: 5, className: 'sl_box_shadow', img: getImageUrl('bonusCabinet/Chest_2.png'), title: computed(() => t('bonusCabinet.BônusCashback')), btnName: computed(() => t('btnName.Adicionar')) },
            { id: 6, className: 'sl_box_shadow', img: getImageUrl('bonusCabinet/Chest_3.png'), title: computed(() => t('bonusCabinet.BônusDiário')), btnName: computed(() => t('btnName.Adicionar')) },
            { id: 7, className: 'sl_box_shadow', img: getImageUrl('bonusCabinet/Chest_4.png'), title: computed(() => t('bonusCabinet.BônusSemanal')), title2: computed(() => t('bonusCabinet.Lançadoàssegundafeiras')), btnName: computed(() => t('btnName.Adicionar')) },
            { id: 8, className: 'sl_box_shadow', img: getImageUrl('bonusCabinet/Chest_5.png'), title: computed(() => t('bonusCabinet.BônusMensal')), title2: computed(() => t('bonusCabinet.Lançadonoiníciodecadamês')), btnName: computed(() => t('btnName.Adicionar')) },
            { id: 9, className: 'sl_box_shadow', img: getImageUrl('bonusCabinet/Platinum.png'), title: computed(() => t('bonusCabinet.BônusDeNível')), btnName: computed(() => t('btnName.Receber')), state: 0 },
          ],
        },
        {
          columnTitle: computed(() => t('bonusCabinet.BônusDiário')),
          showMoreName: computed(() => t('bonusCabinet.showMoreName2')),
          path: '/refer',
          arr: [
            { id: 10, className: 'sl_box_shadow_green', img: getImageUrl('bonusCabinet/Gold_icon.png'), title: computed(() => t('bonusCabinet.BônusDiáriodeConvite')), btnName: computed(() => t('btnName.Receber')), state: 0 },
          ],
        }
      ],
      isBonusPop: false,
      now_bonus_pop: 0,
      split_bonus_pop: 0,
      comIdx: 0,
      btn_loading_2: false,
      btn_loading_3: false,
      btn_loading_4: false,
    });

    // 设置状态
    const get_bonus_cabinet_state = async () => {
      // UserService.get_sign_list().then(resSign => {
      UserService.get_bonus_cabinet_state().then((res) => {
        // await bonusCabinetFun()
        for (let i = 0; i < state.list.length; i++) {
          const element1 = state.list[i];
          for (let j = 0; j < element1.arr.length; j++) {
            const element2 = element1.arr[j];
            if (element2.id == 1) {
              element2['state'] = store.state.vipBonusState.sgin_data['state']
              element2['money'] = store.state.vipBonusState.sgin_data['money']
            }
            else if (element2.id == 3) element2['state'] = res.data.data.loss_bonus_state
            else if (element2.id == 10) element2['state'] = res.data.data.refer_bonus_state
            else if (element2.id == 11) element2['state'] = res.data.data.roller_bonus_state
            else if (element2.id == 12) element2['state'] = res.data.data.de_zhou_bonus_state
            else if (element2.id == 13) {
              if (localStorage.getItem('bonusCabinet_apk_download')) element2['state'] = 1
              else element2['state'] = store.state.user.download_bonus
            }
          }
        }
      })
      // })
    }
    get_bonus_cabinet_state()

    const finish = () => {
      store.dispatch("vipBonusState/init_sgin_data")
    }

    // 
    watch(() => store.state.startData.bonusCabinet.roller_bonus_state, (val: number) => {
      get_bonus_cabinet_state()
    }, { deep: true })

    const showLevelDeltas = () => {
      store.dispatch('status/setvipCheckIn', true);
    }

    // split_bonus
    // now_bonus
    // day_bonus
    // week_bonus
    // month_bonus
    // lv_up_bonus


    // 领取优惠券
    const receive_code = () => {
      if (state.couponCode.trim() == '') return
      const fun = () => {
        giveCode.user_receive_code({ code: state.couponCode }).then((res) => {
          if (res.data.code == 36) {

            promptPopup('depositPopup', { tips: t('promptPopup.tips_Parareceber'), btnName: t('btnName.Depósito') })
          }
          if (res.data.code == 1) promptPopup('rewardPopup', { title: t('promptPopup.title_VOCÊVENCEU'), amount: res.data.money, tips: t('promptPopup.tips_Obônusjá'), btnName: t('btnName.Confirmar') })

        })
      }
      debounce(fun)
    }
    //获取奖金按钮状态
    let btnsStatus = ref();
    const getData = async () => {
      if (store.state.user.token != '') {
        let data = await VipService.get_user_vip_bonus_state({});
        btnsStatus.value = data.data.data;
        const obj = {
          now_bonus: data.data.data.now_bonus,
          week_bonus: data.data.data.week_bonus,
          month_bonus: data.data.data.month_bonus,
          day_bonus: data.data.data.day_bonus,
          split_bonus: data.data.data.split_bonus,
          lv_up_bonus: data.data.data.lv_up_bonus,
          badgeShow: data.data.bonus_num > 0 ? true : false,
          bonus_num: data.data.bonus_num,
        }
        store.dispatch("vipBonusState/setData", obj);
        state.list[1].arr[0] = { ...state.list[1].arr[0], ...store.state.vipBonusState.split_bonus }
        state.list[1].arr[1] = { ...state.list[1].arr[1], ...store.state.vipBonusState.now_bonus }
        state.list[1].arr[2] = { ...state.list[1].arr[2], ...store.state.vipBonusState.day_bonus }
        state.list[1].arr[3] = { ...state.list[1].arr[3], ...store.state.vipBonusState.week_bonus }
        state.list[1].arr[4] = { ...state.list[1].arr[4], ...store.state.vipBonusState.month_bonus }
        state.list[1].arr[5] = { ...state.list[1].arr[5], ...store.state.vipBonusState.lv_up_bonus }
      }
    }
    getData()
    // 领取立即反水
    const get_bonus = (index) => {
      switch (index) {
        case 1:
          if (store.state.vipBonusState.now_bonus.time <= 0 && store.state.vipBonusState.now_bonus.state == 1) {
            VipService.user_get_now_vip_bonus().then((res) => {
              if (res.data.code == 1) {
                getData()
                getUserInfoNoLoad()
                proxy.$mitt.emit('getVipFinish')
                state.isBonusPop = true
                state.now_bonus_pop = res.data.bonus
                state.split_bonus_pop = res.data.split_bonus
                state.comIdx = index
              }
            })
          }
          break;
        case 2:
          if (store.state.vipBonusState.day_bonus.state == 1 && store.state.vipBonusState.day_bonus.money > 0) {
            state.btn_loading_2 = true
            VipService.user_get_day_vip_bonus().then((res) => {
              if (res.data.code == 1) {
                getData()
                getUserInfoNoLoad()
                proxy.$mitt.emit('getVipFinish')
                state.isBonusPop = true
                state.now_bonus_pop = res.data.bonus
                state.split_bonus_pop = res.data.split_bonus
                state.comIdx = index
                state.btn_loading_2 = false
              }
            })
          }
          break;
        case 3:
          if (store.state.vipBonusState.week_bonus.state == 1 && store.state.vipBonusState.week_bonus.money > 0) {
            state.btn_loading_3 = true
            VipService.user_get_week_vip_bonus().then((res) => {
              if (res.data.code == 1) {
                getData()
                getUserInfoNoLoad()
                proxy.$mitt.emit('getVipFinish')
                state.isBonusPop = true
                state.now_bonus_pop = res.data.bonus
                state.split_bonus_pop = res.data.split_bonus
                state.comIdx = index
                state.btn_loading_3 = false
              }
            })
          }
          break;
        case 4:
          if (store.state.vipBonusState.month_bonus.state == 1 && store.state.vipBonusState.month_bonus.money > 0) {
            state.btn_loading_4 = true
            VipService.user_get_month_vip_bonus().then((res) => {
              if (res.data.code == 1) {
                getData()
                getUserInfoNoLoad()
                proxy.$mitt.emit('getVipFinish')
                state.isBonusPop = true
                state.now_bonus_pop = res.data.bonus
                state.split_bonus_pop = res.data.split_bonus
                state.comIdx = index
                state.btn_loading_4 = false
              }
            })
          }
          break;
        default:
          break;
      }
    }

    const btnClick = (item) => {
      switch (item.id) {
        // 签到
        case 1:
          if (item.state == 1) {
            if (item.money == 0) {
              return ElNotification({
                message: t('Pleaseincreaseyourviplevel'),
                type: 'warning',
                duration: 3000,
                offset: 65,
              })
            }
            const fun = () => {
              UserService.receive_sign_bonus().then((res) => {
                if (res.data.code == 1) {
                  promptPopup('rewardPopup', { title: t('promptPopup.title_CheckinSucesso'), amount: res.data.money, tips: t('promptPopup.tips_Obônusjá'), btnName: t('btnName.Confirmar') })
                  // store.state.vipBonusState.sgin_data['state'] = 0
                  item.state = 0
                }
              });
            }
            debounce(fun)
          }
          break;
        // 损失奖金
        case 3:
          const fun = () => {
            UserService.receive_loss_bonus().then(res => {
              getUserInfo()
              item.state = 0
              promptPopup('rewardPopup', { title: t('promptPopup.title_VOCÊVENCEU'), amount: res.data.money, tips: t('promptPopup.tips_Obônusjá'), btnName: t('btnName.Confirmar') })
            })
          }
          debounce(fun)
          break;
        case 9:
          router.push('/vipBonus/allLevels')
          break;
        case 10:
          router.push('/refer')
          break;
        case 11:
          store.dispatch("status/setRollerShow", true)
          break;
        case 13:
          if (!store.state.status.isApk) downloadAPK();
          else {
            const fun_apk_download_bonus = () => {
              UserService.apk_download_bonus().then(res => {
                if (res.data.code == 1) {
                  localStorage.setItem('bonusCabinet_apk_download', 'true')
                  item.state = 1
                  promptPopup('rewardPopup', { title: t('promptPopup.title_VOCÊVENCEU'), amount: res.data.money, tips: t('promptPopup.tips_Obônusjá'), btnName: t('btnName.Confirmar') })
                }
              })
            }
            debounce(fun_apk_download_bonus)
          }
          break;
        default:
          break;
      }
    }
    return { ...toRefs(state), store, t, btnClick, moneyFormat, get_bonus, router, receive_code, getImageUrl, finish, showLevelDeltas };
  },
});
</script>
<style lang="scss" scoped>
.bounsPop_box {
  display: flex !important;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  height: 100%;

  .pop_box {
    position: relative;
  }
}

.bonusCabinet {
  .box {
    margin-bottom: 16px;
    padding: 30px 12px 12px;
    background: #202431;
    border-radius: 12px;

    .box_column {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 30px;

      .box_column_l_box {
        padding-left: 20px;
        font-size: 24px;
        font-weight: 600;
        color: #B2B6C5;
      }

      .box_column_r_box {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 11px 0 25px;
        width: 460px;
        height: 60px;
        box-sizing: border-box;
        background: #2F3445;
        border-radius: 30px;
        border: 1.5px solid transparent;

        &:hover {
          border: 1.5px solid rgba(255, 255, 201, 0.9);
          box-shadow: 0px 0px 4px 0px rgba(255, 119, 68, 0.25);
        }

        img {
          width: 34px;
        }

        input {
          height: 100%;
          width: 100%;
          background: transparent;
          border: 0;
          color: #fff;
          font-size: 18px;

          &::placeholder {
            font-weight: 500;
            color: #78818C;
          }
        }

        .sl_box_shadow_green {
          padding: 12px 21px;
          font-size: 16px;
          font-weight: 600;
          color: #1B1D29;
          border-radius: 20px;
          white-space: nowrap;
        }
      }
    }

    ul {
      padding: 15px 23px 15px 11px;
      background: #2F3445;
      border-radius: 12px;

      li {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;

        &:nth-last-child(1) {
          margin-bottom: 0;
        }

        .l_box {
          display: flex;
          align-items: center;
          justify-content: space-between;

          img {
            margin-right: 22px;
            width: 86px;
          }

          .l_box_content {
            .l_box_content_top {
              display: flex;
              align-items: center;

              div {
                display: inline-block;
                vertical-align: middle;
              }

              span {
                font-size: 20px;
                font-weight: 800;
                color: #B2B6C5;
              }

              .level_img {
                margin: 0 0 0 9px;
                width: 50px;
              }
            }

            .l_box_content_bottom {
              margin-top: 8px;

              span {
                font-size: 16px;
                font-weight: 500;
                color: #686D7B;
              }
            }
          }
        }

        .r_box {
          display: flex;
          align-items: center;
          justify-content: center;
          min-width: 132px;
          padding: 16px;
          box-sizing: border-box;
          border-radius: 10px;
          gap: 4px;
          flex-shrink: 0;

          img {
            margin-right: 5px;
            width: 15px;
          }

          span,
          p {
            font-size: 18px;
            font-weight: 600;
            color: #1B1D29;
          }
        }

        .sl_box_shadow_mask_events {
          pointer-events: all;

          &.sl_box_shadow_mask::after {}
        }

        .r_box_flex {
          padding: 5px 16px;
          flex-direction: column;
          gap: 0;

          p:nth-child(2) {
            margin-top: 5px;
          }
        }

        .no_bonus_box {
          box-shadow: none;
          display: flex;

          // gap: 5px;
          &.sl_box_shadow_mask::after {
            display: none;
          }

          p {
            color: #B2B6C5 !important;
          }
        }
      }
    }

    .show_more {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px 0 12px 0;

      span {
        cursor: pointer;
        margin-right: 8px;
        font-size: 16px;
        font-weight: bold;
        color: #4181EE;
      }

      img {
        width: 19px;
      }
    }
  }

  .box:nth-child(2) {
    padding-top: 12px;

    .box_column {
      margin-bottom: 15px;
    }
  }
}

@media (max-width: 768px) {
  .bonusCabinet {
    padding: 0 12px;

    .box {
      margin-bottom: 12px;
      padding: 19px 6px 6px;
      border-radius: 8px;

      .box_column {
        flex-direction: column;
        align-items: normal;
        gap: 18px;
        margin-bottom: 19px;

        .box_column_l_box {
          padding-left: 10px;
          font-size: 14px;
        }

        .box_column_r_box {
          padding: 0 6px 0 12px;
          width: 100%;
          height: 36px;
          border-radius: 18px;
          border: 1px solid transparent;

          &:hover {
            border: 1px solid rgba(255, 255, 201, 0.9);
          }

          img {
            width: 33px;
          }

          input {
            font-size: 12px;
          }

          .sl_box_shadow_green {
            padding: 8px 13px;
            font-size: 12px;
            border-radius: 26px;
          }
        }
      }

      ul {
        padding: 16px 6px;
        background: #2F3445;
        border-radius: 6px;

        li {
          margin-bottom: 16px;

          &:nth-last-child(1) {
            margin-bottom: 0;
          }

          .l_box {
            img {
              margin-right: 6px;
              width: 40px;
            }

            .l_box_content {
              .l_box_content_top {

                span {
                  font-size: 12px;
                }

                .level_img {
                  margin: 0 0 0 6px;
                  width: 32px;
                }
              }

              .l_box_content_bottom {
                margin-top: 4px;

                span {
                  font-size: 12px;
                }
              }
            }
          }

          .r_box {
            min-width: 95px;
            padding: 13px 14px;
            border-radius: 8px;

            span,
            p {
              font-size: 12px;
              text-align: center;
            }
          }

          .r_box_flex {
            padding: 6px 10px;
            flex-direction: column;
            gap: 4px;

            p:nth-child(2) {
              margin-top: 0px;
            }
          }

          .sl_box_shadow_mask {
            &::after {
              border-radius: 8px;
            }
          }
        }
      }

      .show_more {
        padding: 10px 0 6px 0;

        span {
          margin-right: 5px;
          font-size: 12px;
        }

        img {
          width: 15px;
        }
      }
    }

    .box:nth-child(2) {
      padding-top: 18px;

      .box_column {
        margin-bottom: 6px;
      }
    }
  }
}
</style>
