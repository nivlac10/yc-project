import { defineStore } from 'pinia'

const confStore = defineStore('layout', {
  persist: true,
  state: () => {
    return {
      agent_list: [],
      factory_list: [],
      factory_details_list: [],
      external_game_list: [],
      gameType: [],
      imgUrl: 'https://file.bigwin777.io/',
      isPc: true,
      vipLvList: [],
    }
  },
  actions: {

  },
})
export default confStore;
