<script lang="ts" setup>
import { ref, watch } from "vue";

let pName = ref();
pName.value = localStorage.getItem("pName")
  ? localStorage.getItem("pName").toUpperCase()
  : "BIGWIN777";
// watch(
//   () => localStorage.getItem("pName"),
//   () => {
//     pName.value = localStorage.getItem("pName").toUpperCase();
//   }
// );
interface Props {
  collapse?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  collapse: true,
});
</script>

<template>
  <div class="sidebar-logo-container" :class="{ collapse: props.collapse }">
    <transition name="sidebar-logo-fade">
      <router-link v-if="props.collapse" key="collapse" to="/">
        <img src="@/assets/layout/logo.png" class="sidebar-logo" />
      </router-link>
      <router-link v-else key="expand" to="/">
        <!-- <img src="@/assets/layout/logo-text-1.png" class="sidebar-logo-text" /> -->
        <span class="cName">{{ pName }}</span>
      </router-link>
    </transition>
  </div>
</template>
<style lang="scss" scoped>
.cName {
  font-size: 30px;
  color: #fff;
  font-weight: 600;
}
.sidebar-logo-container {
  position: relative;
  width: 100%;
  height: var(--v3-header-height);
  line-height: var(--v3-header-height);
  background-color: var(--v3-sidebarlogo-bg-color);
  text-align: center;
  overflow: hidden;
  .sidebar-logo {
    display: none;
  }
  .sidebar-logo-text {
    height: 100%;
    vertical-align: middle;
  }
}

.collapse {
  .sidebar-logo {
    width: 32px;
    height: 32px;
    vertical-align: middle;
    display: inline-block;
  }
  .sidebar-logo-text {
    display: none;
  }
}
</style>
