// import pageStore from "@/store/PageState";
// import depositWithdrawalStore from "@/store/depositWithdrawal";
import { GameService } from "@/api/game";
import router from "@/router";
import { store } from "@/store/index";
// loading 加载
export function resLoadingState(flag: boolean) {
    // const pageState = pageStore()
    // pageState.resLoadingShow = flag
}
// 活动跳转内容
export function jumpRoute(data) {
    // const payState = depositWithdrawalStore()
    let active = data
    if (active.data != 0) {
        switch (active.type) {
            case 1:
                if (active.url == "1") {
                    // 充值弹窗
                    // payState.depositWithdrawalShow = true
                    if (store.state.user.token != "") {
                        store.state.status.depositShow = true
                    } else {
                        store.state.status.loginShow = true
                    }
                } else if (active.url == "2") {
                    if (store.state.user.token != "") {
                        store.state.status.rollerShow = true
                    } else {
                        store.state.status.rollerShow = true
                    }
                } else {
                    // 路由跳转
                    router.push({ path: active.url })
                }

                break;
            // case 2:
            //     if (active.url) {
            //         setTimeout(() => {
            //             resLoadingState(true)
            //         }, 500);
            //         GameService.get_game_play_url({ gid: active.url }).then((res) => {
            //             if (res.data.code == 1) {
            //                 router.push({
            //                     path: '/Iframe',
            //                     query: {
            //                         src: res.data.url
            //                     }
            //                 })
            //             }
            //             resLoadingState(false)
            //         }).catch(() => {
            //             resLoadingState(false)
            //         })
            //     }
            //     break;
            case 3:
                router.push({
                    path: '/Iframe',
                    query: {
                        src: active.url
                    }
                })
                break;
            case 4:
                let isApk = false
                try {
                    //@ts-ignore
                    isApk = window.Native.getMyDeviceId ? true : false
                } catch (error) {
                    // alert(JSON.stringify(error))
                    // console.log(error);
                }
                if (isApk) {
                    try {
                        //@ts-ignore
                        window.Native.openURL(active.url)
                    } catch (error) {
                        // alert(JSON.stringify(error))
                        // console.log(error);
                    }
                } else {

                    window.open(active.url)
                }
                break;
            default:
                break;
        }
    }

}