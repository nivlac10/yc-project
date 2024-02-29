<script lang="ts" setup>
import { get_p_conf } from "@/api/login";
import { Expand, Fold } from "@element-plus/icons-vue";
import { ref } from "vue";

interface Props {
  isActive?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  isActive: false,
});

/** Vue 3.3+ defineEmits 语法 */
const emit = defineEmits<{
  toggleClick: [];
}>();

const toggleClick = () => {
  emit("toggleClick");
};
// 平台数组
let dbList = ref([]);
// 平台名称
let pName = ref("");
get_p_conf().then((res) => {
  for (let i = 0; i < res.data.length; i++) {
    const element = res.data[i];
    let data = {
      value: element.index,
      label: element.p_name,
    };
    dbList.value.push(data);
  }
  if (!localStorage.getItem("pName")) {
    localStorage.setItem("pName", dbList.value[0].label);
  }
  pName.value = localStorage.getItem("pName").toUpperCase();
});
function changeP(params) {
  localStorage.setItem("pIndex", params);
  localStorage.setItem("pName", dbList.value[params].label);
  location.reload();
}
</script>

<template>
  <div>
    <div @click="toggleClick">
      <el-icon :size="20" class="icon">
        <Fold v-if="props.isActive" />
        <Expand v-else />
      </el-icon>
    </div>

    <el-select
      v-model="pName"
      class="m-2"
      placeholder="选择平台"
      size="large"
      @change="changeP"
    >
      <el-option
        v-for="item in dbList"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>
</template>

<style lang="scss" scoped>
.cName {
  font-size: 14px;
  font-weight: 600;
  color: #000;
}
.icon {
  vertical-align: middle;
}
</style>
