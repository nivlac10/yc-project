<template>
  <div class="footballBtn" v-if="store.state.user.token != '' || store.state.status.isPc">
    <div
      :class="{ btnItem: true, check: btnCheck == 'c_home' }"
      @click="btnClick('/clHome')"
    >
      <img v-show="btnCheck == 'c_home'" src="@/assets/images/layout/Jogos.png" alt="" />
      <img
        v-show="btnCheck !== 'c_home'"
        src="@/assets/images/layout/Jogos2.png"
        alt=""
      />
      <p>Cassino</p>
    </div>

    <div
      :class="{ btnItem: true, check: btnCheck == 'ball' }"
      @click="btnClick('/physicalEducation')"
    >
      <img v-show="btnCheck == 'ball'" src="@/assets/images/layout/esporte.png" alt="" />
      <img
        v-show="btnCheck !== 'ball'"
        src="@/assets/images/layout/esporte2.png"
        alt=""
      />
      <p>Esporte</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, toRefs, ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "@/store/index";
const router = useRouter();
const route = useRoute();
let btnCheck = ref("c_home");
const store = useStore();

watch(
  () => route.path,
  (newPath, oldPath) => {
    if (newPath == "/physicalEducation") {
      btnCheck.value = "ball";
    } else if (newPath == "/clHome") {
      btnCheck.value = "c_home";
    } else {
      btnCheck.value = "null";
    }
  },
  { immediate: true }
);

const btnClick = (path) => {
  btnCheck.value = !btnCheck.value;
  router.push(path);
};
</script>

<style lang="scss" scoped>
.footballBtn {
  width: 212px;
  height: 42px;
  background: #151821;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  gap: 4px;
  box-sizing: border-box;
  padding: 4px;

  .btnItem {
    width: 100px;
    height: 34px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 4px;
    color: #98abd0;

    img {
      width: 26px;
      height: 26px;
    }
  }

  .check {
    background: #2e3345;
    border-radius: 6px;
    color: #ffffff;
    transition: all 0.5s ease;
  }
}

@media (max-width: 758px) {
  .footballBtn {
    width: 164px;
    height: 30px;
    gap: 0;
    padding: 2px;

    .btnItem {
      width: 80px;
      height: 28px;
      gap: 2px;

      img {
        width: 16px;
        height: 16px;
      }
      p {
        font-size: 12px;
      }
    }
  }
}
</style>
