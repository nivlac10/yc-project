
<template>
  <div>
    <component :is="Admin" v-if="isAdmin || isEditor" />
    <DeZhou v-if="isDeZhou"></DeZhou>
  </div>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/store/modules/user"
import Admin from "./components/Admin.vue"
import Editor from "./components/Editor.vue"
import DeZhou from "./components/DeZhou.vue";
const userStore = useUserStore()
const isAdmin = userStore.roles.includes("1")
const isEditor = userStore.roles.includes("3")
const isDeZhou = userStore.roles.includes("5")
</script>

