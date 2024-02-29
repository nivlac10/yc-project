import { UserService } from "@/api/user";
import { store } from "@/store";

// 奖金柜
export const bonusCabinetFun = () => {
	UserService.get_bonus_cabinet_state().then((res) => {
		store.dispatch('startData/setBonusCabinetData', res.data.data)
	})
}