<template>
  <div>
    <el-table v-loading="loading" :data="popData" style="width: 100%">
      <el-table-column prop="nickname" label="用户名" header-align="center" :align="'center'" />
      <el-table-column prop="game_name" label="游戏" header-align="center" :align="'center'" />
      <el-table-column prop="real_shu_ying" label="实际输赢" header-align="center" :align="'center'" />
      <el-table-column prop="num" label="总次数" header-align="center" :align="'center'" />
      <el-table-column prop="cover_charge" label="服务费" header-align="center" :align="'center'" />
      <el-table-column prop="code_size" label="打码量" header-align="center" :align="'center'" />
      <el-table-column prop="betting" label="投注" header-align="center" :align="'center'" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch, computed } from "vue";
import { user_game_log_list_post } from "../../../api/gameManagement";
import { useId } from "element-plus";

const props = defineProps({
  uid: {
    default: null,
  }
});
let uid = computed(() => props.uid);
let popData = ref([]);
let loading = ref(false);
async function getData() {
  popData.value = [];
  loading.value = true;
  let data = await user_game_log_list_post({ uid:uid.value });
  console.log(data);

  popData.value = data.data;
  loading.value = false;
  console.log(popData.value);
}
getData();
</script>

<style scoped></style>
