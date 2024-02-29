<template>
  <div>
    <div class="gameOutBox">
      <gameList :gameList="game_list" :count="count" @def="getGamedata()"> </gameList>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch } from "vue";
import { useStore } from "@/store/index";
import { useRouter, useRoute } from "vue-router";
import gameList from "@/components/gameList/index.vue"
import { get_game_data } from "@/utils/gameUtils";
import { stat } from "fs";
export default defineComponent({
  name: "gameType",
  components: {
    gameList
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const state = reactive({
      game_list: [],
      count: 0,
      factory_list: [],
      pageFrom: {
        page: 1,
        limit: 28,
        gameName: "",
        game_id: null
      },
      factoryIndex: 0,
      loading: true
    });
    state.pageFrom.limit = store.state.status.isPc ? 28 : 30;
    function getGamedata() {
      let game_data = get_game_data(null, null, null, 1, null, null, state.pageFrom.page, state.pageFrom.limit) as never;
      let game_list = game_data['allGameList'] as any
      for (let index = 0; index < game_list.length; index++) {
        const element: never = game_list[index] as never;
        state.game_list.push(element)
      }
      // state.game_list = game_data['allGameList']
      state.count = game_data['count']
      state.pageFrom.page++
    }
    getGamedata()

    return { ...toRefs(state), store, getGamedata };
  },
});
</script>
  