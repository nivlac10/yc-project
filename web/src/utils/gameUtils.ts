import { useStore } from "@/store/index";
import { store } from '@/store'

export function get_game_data(game_id: any = null, game_type: any = null, game_name: any = null, is_top: any = 0, is_hot: any = 0, is_tag: any = null, page: any = 1, limit: any = 6) {
    let gameList = store.state.conf.game_list.game_list
    let offset = (page - 1) * limit
    is_hot = is_hot ? is_hot : 0
    is_top = is_top ? is_top : 0
    for (let i = 0; i < gameList.length; i++) {
        // 遍历已收藏的游戏
        gameList[i].tag = isTagGame(gameList[i].gid)
        gameList[i].tag_show = true
    }
    if (is_tag == 1) {
        let arr: any = []
        for (let i = 0; i < gameList.length; i++) {
            if (gameList[i].tag == 1) {
                arr.push(gameList[i])
            }
        }
        gameList = arr
    }
    if (game_id != null) {
        let arr: any = []
        for (let i = 0; i < gameList.length; i++) {
            if (gameList[i].game_id == game_id) {
                arr.push(gameList[i])
            }
        }
        gameList = arr
    }
    if (game_type != null) {
        let arr: any = []
        for (let i = 0; i < gameList.length; i++) {
            if (gameList[i].game_type == game_type) {
                arr.push(gameList[i])
            }
        }
        gameList = arr
    }
    // if (game_name != null) {
    //     let arr: any = []
    //     for (let i = 0; i < gameList.length; i++) {
    //         if (gameList[i].game_name.toLowerCase().indexOf(game_name.toLowerCase()) != -1) {
    //             arr.push(gameList[i])
    //         }
    //     }
    //     gameList = arr
    // }
    // 游戏名称
    
    if (game_name != null) {
        let arr: any = []
        for (let i = 0; i < gameList.length; i++) {
            if (gameList[i].game_name.toLowerCase().indexOf(game_name.toLowerCase()) != -1) {
                arr.push(gameList[i])
            }
        }
        gameList = arr
    }
    if (is_top == 1) {
        let arr: any = []
        for (let i = 0; i < gameList.length; i++) {
            if (gameList[i].is_top == 1) {
                arr.push(gameList[i])
            }
        }
        gameList = arr
    }
    if (is_hot == 1) {
        let arr: any = []
        for (let i = 0; i < gameList.length; i++) {
            if (gameList[i].is_hot == 1) {
                arr.push(gameList[i])
            }
        }
        gameList = arr
    }
    // 总条数
    let count = gameList.length
    // 分页
    if (gameList.length > 0) {
        let arr: any = []
        for (let i = 0; i < gameList.length; i++) {
            if (i >= offset && i <= (limit + offset - 1)) {
                arr.push(gameList[i])
            }
        }
        gameList = arr
    }
    // 返回数据
    let backData = {
        allGameList: gameList,
        count: count
    }
    return backData
}
// 根据game_id 获取厂商数据
export function get_factory_list() {
    return store.state.conf.game_list.factory_list
}
// 根据gid 获取游戏数据
export function get_game_data_by_gid(gid) {
    let gameList = store.state.conf.game_list.game_list
    let data = null
    for (let i = 0; i < gameList.length; i++) {
        if (gameList[i].gid == gid) {
            gameList[i].tag = isTagGame(gameList[i].gid)
            gameList[i].tag_show = true
            data = gameList[i]
        }
    }
    return data
}

// 根据game_id 获取厂商数据
export function get_game_data_by_game_id(game_id) {
    let gameList = store.state.conf.game_list.factory_list
    let data = null
    for (let i = 0; i < gameList.length; i++) {
        if (gameList[i].game_id == game_id) {
            data = gameList[i]
        }
    }
    return data
}
//取消或收藏游戏
export function whetherCollectGames(id: number, tag: number) {
    tag = tag == 1 ? 0 : 1
    //@ts-ignore
    let tag_list = localStorage.getItem("user_game_tag_list") ? JSON.parse(localStorage.getItem("user_game_tag_list")) : []
    if (tag) {
        tag_list.unshift(id)
    } else {
        let arr: any = []
        for (let i = 0; i < tag_list.length; i++) {
            if (tag_list[i] != id) {
                arr.push(tag_list[i])
            }
        }
        tag_list = arr
    }
    localStorage.setItem("user_game_tag_list", JSON.stringify(tag_list))
    return tag;
}

// 判断是否为以收藏游戏
function isTagGame(gid: number) {
    //@ts-ignore
    let tag_list = localStorage.getItem("user_game_tag_list") ? JSON.parse(localStorage.getItem("user_game_tag_list")) : []
    if (tag_list.length > 0) {
        for (let i = 0; i < tag_list.length; i++) {
            if (gid == tag_list[i]) {
                return 1
            }
        }
    } else {
        return 0
    }
    return 0
}

//根据厂商获取游戏列表
export function get_game_list_by_f_name(f_name: string) {
    let gameList = store.state.conf.game_list.game_list as any;
    if (gameList && f_name) {
        let data = [] as any;
        for (let i = 0; i < gameList.length; i++) {
            if (gameList[i].f_name == f_name) {
                data.push(gameList[i])
            }
        }
        return data
    }



}