<template>
  <div>
    <!-- <el-skeleton :loading="loading">
      <template #template>
        <div class="gameBox">
          <div>
            <div class="factory">
              <div v-for="i in 5" class="factory_box" style="width: 50px;"></div>
            </div>
          </div>
          <div class="game_skeleton">
            <img src="@/assets/images/gamePlay/gamebg.png" v-for="i in pageFrom.limit" />
          </div>
        </div>
      </template>
    </el-skeleton> -->
    <div class="gameOutBox">
      <div class="factory">
        <div
          v-for="(item, index) in factory_list"
          :key="item"
          :class="{ factory_box: true, factory_active: factoryIndex == index }"
          @click="changeFactory(item), (factoryIndex = index)"
        >
          <span>{{ item["game_name"] }}</span>
        </div>
      </div>
      <gameList :gameList="game_list" :count="count" @def="getGamedata()"></gameList>
    </div>
  </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch } from "vue";
import { useStore } from "@/store/index";
import { useRouter, useRoute } from "vue-router";
import gameList from "@/components/gameList/index.vue";
import { get_game_data } from "@/utils/gameUtils";
export default defineComponent({
  name: "gameType",
  components: {
    gameList,
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
        game_type: 0,
        game_id: null,
      },
      factoryIndex: 0,
      loading: true,
    });

    state.pageFrom.game_type = parseInt(route.params.type.toString());
    state.pageFrom.limit = store.state.status.isPc ? 28 : 30;
    // 监听路由
    watch(
      () => route.params.type,
      (newData, oldData) => {
        state.game_list = [];
        state.factory_list = [];
        state.factoryIndex = 0;
        state.pageFrom = {
          page: 1,
          limit: store.state.status.isPc ? 28 : 12,
          gameName: "",
          // @ts-ignore
          game_type: newData || "",
          game_id: null,
        };
        resettingFactory();
        getGamedata();
      }
    );

    // 重置厂商默认选中
    function resettingFactory() {
      let factory_list = store.state.conf.game_list.factory_list;
      for (let index = 0; index < factory_list.length; index++) {
        const element = factory_list[index];
        let fac_game_list = get_game_data(
          element.game_id,
          state.pageFrom.game_type,
          null,
          null,
          null,
          null,
          1,
          1
        );
        if (fac_game_list.count > 0) {
          // @ts-ignore
          state.factory_list.push(element);
        }
      }
      if (state.factory_list[0]) {
        state.pageFrom.game_id = state.factory_list[0]["game_id"];
      }

      // state.loading = true
      // setTimeout(() => {
      //   state.loading = false
      // }, 500);
    }
    resettingFactory();
    function getGamedata() {
      let game_data = get_game_data(
        state.pageFrom.game_id,
        state.pageFrom.game_type,
        null,
        null,
        null,
        null,
        state.pageFrom.page,
        state.pageFrom.limit
      ) as never;
      let game_list = game_data["allGameList"] as any;
      for (let index = 0; index < game_list.length; index++) {
        const element: never = game_list[index] as never;
        state.game_list.push(element);
      }
      // state.game_list = game_data['allGameList']
      state.count = game_data["count"];
      state.pageFrom.page++;
    }
    getGamedata();
    function changeFactory(item) {
      state.game_list = [];
      state.pageFrom.game_id = item.game_id;
      state.pageFrom.page = 1;
      getGamedata();
    }
    return { ...toRefs(state), store, getGamedata, changeFactory };
  },
});
</script>
