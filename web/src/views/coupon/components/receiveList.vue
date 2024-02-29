<template>
  <div class="receiveList">
    <div class="list_title">
      <img src="@assets/images/coupon/coupon.png" alt="">
      <span>{{ t('sidebar.TodososBônus') }}</span>
    </div>
    <div class="tab_title">
      <div>{{ t('coupon.Time') }}</div>
      <div>{{ t('coupon.User') }}</div>
      <div>{{ t('coupon.Exchange') }}</div>
    </div>
    <div class="list">
      <ul>
        <li v-for="(v, i) in list" :key="v">
          <div>{{ v['add_time'] }}</div>
          <div>{{ v['nickname'] }}</div>
          <div>+{{ t('base.currencySymbol') }}{{ v['give_money'] }}</div>
        </li>
      </ul>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { giveCode } from "@/api/giveCode";
export default defineComponent({
  name: "receiveList",
  setup() {
    const { proxy } = getCurrentInstance() as any;
    const router = useRouter();
    const { t } = useI18n();
    const store = useStore();
    const state = reactive({
      list: []
    });
    giveCode.get_give_code_list().then((res) => {
      console.log(res.data);
      if (res.data.code == 1) {
        state.list = res.data.data
      }
    })
    return { ...toRefs(state), store, t, };
  },
});
</script>
<style  lang="scss" scoped>
.receiveList {
  width: 100%;

  .list_title {
    display: flex;
    // gap: 20px;
    align-items: center;

    img {
      width: 72px;
    }

    span {
      color: #C3CFD9;
      font-size: 24px;
    }
  }

  .tab_title {
    // display: flex;
    // justify-content: space-between;
    // padding: 14px 0;
    margin-bottom: 6px;
    background: var(--auxiliary-font-color-24);
    border-radius: 12px 12px 0px 0px;

    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    padding: 14px 27px;

    div {
      font-size: 20px;
      font-weight: 500;
      color: var(--auxiliary-font-color-9);

      &:nth-child(1) {
        // width: 40%;
        // text-align: left;

        text-align: left;
      }

      &:nth-child(3) {
        text-align: right;
        // margin-right: 30px;
      }
    }
  }

  .list {
    min-height: 744px;
    background: var(--auxiliary-font-color-24);
    border-radius: 0px 0px 12px 12px;

    ul {
      padding: 24px 27px;
      box-sizing: border-box;

      li {
        display: grid;
        // justify-content: space-between;
        grid-template-columns: 2fr 1fr 1fr;
        margin-bottom: 22px;

        div {
          font-size: 18px;
          font-weight: 500;
          color: var(--auxiliary-font-color-9);

          &:nth-child(1) {
            text-align: left;
            // width: 40%;
          }

          &:nth-child(3) {
            color: var(--auxiliary-font-color-7);

            text-align: right;
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .receiveList {
    .list_title {
      img{
        width: 36px !important;
      }
      span{
        font-size: 14px !important;
        font-weight: 600;
      }
    }

    .tab_title {
      padding: 10px 10px;
      border-radius: 9px 9px 0px 0px;

      div {
        font-size: 14px;

        &:nth-child(1) {
          // width: 40%;
          // text-align: center;
        }

        &:nth-child(3) {
          // margin-right: 30px;
        }
      }
    }

    .list {
      min-height: 489px;
      border-radius: 0px 0px 9px 9px;

      ul {
        padding: 19px 10px;

        li {
          margin-bottom: 16px;

          div {
            font-size: 13px;

            &:nth-child(1) {
              // width: 40%;
            }

            &:nth-child(3) {
              color: var(--auxiliary-font-color-7);
            }
          }
        }
      }
    }
  }
}</style>
