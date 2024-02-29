/***
 *  获取有关游戏公共方法
 */
// import confStore from "@/store/conf";
// import { storeToRefs } from "pinia";

import { store } from "@/store/index"


// 获取游戏列表 参数（type 0 slot 1 table 2 live 3 fish,game_id 厂商id,   page 页码  limit 条数）
export function getGameList(type: number, game_id: number, page: number, limit: number, game_name: string) {
    const game_list = store.state.conf.game_list
    limit = limit || 6
    page = page || 1
    let offset = (page - 1) * limit
    let gameList = game_list.game_list
    // 获取类型
    if (type != null) {
        let arr = []
        for (let i = 0; i < gameList.length; i++) {
            if (gameList[i].game_type == type) {
                // let flag = getGameStatus(gameList[i].game_id)
                // if (flag == 1 || flag == 2) {

                //     arr.push(gameList[i])
                // }
                gameList[i].status = getGameStatus(gameList[i].game_id)
                arr.push(gameList[i] as never)
            }
        }
        gameList = arr
    }
    // 获取厂商
    if (game_id) {
        let arr = []
        for (let i = 0; i < gameList.length; i++) {
            if (gameList[i].game_id == game_id) {
                arr.push(gameList[i] as never)
            }
        }
        gameList = arr
    }

    // 根据游戏name查询
    if (game_name) {
        let arr = []
        for (let i = 0; i < gameList.length; i++) {
            var result = gameList[i].game_name.toLowerCase().indexOf(game_name.toLowerCase());
            if (result > 0) {
                arr.push(gameList[i] as never)
            }
        }
        gameList = arr
    }
    // 总条数
    let count = gameList.length
    // 分页
    if (gameList.length > 0) {
        let arr = []
        for (let i = 0; i < gameList.length; i++) {
            if (i >= offset && i <= (limit + offset - 1)) {
                // 遍历已收藏的游戏
                gameList[i].tag = isTagGame(gameList[i].gid)
                gameList[i].tag_show = true
                arr.push(gameList[i] as never)
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
// 获取游戏厂商列表
export function getFactoryList(type: number, page: number, limit: number) {

    const game_list = store.state.conf.game_list

    limit = limit || 6
    page = page || 1
    let offset = (page - 1) * limit
    let factoryList = game_list.factory_list
    if (type != null) {
        let arr = []
        for (let i = 0; i < factoryList.length; i++) {
            if (factoryList[i].game_type == type) {
                arr.push(factoryList[i] as never)
            }
        }
        factoryList = arr
    }
    // 总条数
    let count = factoryList.length
    // 分页
    if (factoryList.length > 0) {
        let arr = []
        for (let i = 0; i < factoryList.length; i++) {
            if (i >= offset && i <= (limit + offset - 1)) {
                factoryList[i].tag = 0
                arr.push(factoryList[i] as never)
            }
        }
        factoryList = arr
    }
    let backData = {
        allGameList: factoryList,
        count: count
    }
    return backData
}

// 获取收藏游戏列表
export function getCollectGames(page: number, limit: number, game_name: string) {

    const game_list = store.state.conf.game_list

    limit = limit || 24
    page = page || 1
    let offset = (page - 1) * limit
    let tag_list = localStorage.getItem("user_game_tag_list") ? JSON.parse(localStorage.getItem("user_game_tag_list") as any) : []
    let gameList = []
    if (tag_list.length > 0) {
        for (let i = 0; i < tag_list.length; i++) {
            gameList.push(getGameInfo(tag_list[i]) as never)
        }
        if (game_name) {
            let arr = []
            for (let i = 0; i < gameList.length; i++) {
                var result = (gameList[i] as any).game_name.toLowerCase().indexOf(game_name.toLowerCase());
                if (result > 0) {
                    arr.push(gameList[i])
                }
            }
            gameList = arr

        }
    }
    // 总条数
    let count = gameList.length
    // 分页
    if (gameList.length > 0) {
        let arr = []
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
//  获取单游戏数据 
export function getGameInfo(gid: any) {

    const game_list = store.state.conf.game_list

    let gameList = game_list.game_list
    for (let i = 0; i < gameList.length; i++) {
        if (gameList[i].gid == gid) {
            let gameIfon = {
                icon: gameList[i].icon,
                game_name: gameList[i].game_name,
                game_type: gameList[i].game_type,
                game_id: gameList[i].game_id,
                open_type: 1, // 0 跳转厂商  1 直接打开游戏
                gid: gameList[i].gid,
                tag: isTagGame(gameList[i].gid),
                tag_show: true
            };
            return gameIfon
        }
    }
}

// // 根据类型获取游戏列表 或者厂商列表  （厂商数量小于3时获取游戏列表）
// export function getTypeGameList(type: number, page: number, limit: number, name: string, game_id: any) {
//     let arr: any = [];
//     // 厂商列表
//     let factory_list = getFactoryList(
//         type,
//         page,
//         limit
//     );

//     let count: number = 0
//     // 遍历厂商列表
//     for (let i = 0; i < factory_list.allGameList.length; i++) {
//         if (type == factory_list.allGameList[i].game_type) {
//             let game_data = {
//                 icon: factory_list.allGameList[i].cover,
//                 game_name: factory_list.allGameList[i].game_name,
//                 game_type: factory_list.allGameList[i].game_type,
//                 open_type: 0, // 0 跳转厂商  1 直接打开游戏
//                 game_id: factory_list.allGameList[i].game_id,
//                 gid: 0,
//                 tag: 0,
//                 tag_show: false,
//                 status: factory_list.allGameList[i].status,
//             };
//             arr.push(game_data);
//         }
//     }

//     // 如果厂商数量 低于列表渲染值 那么直接遍历游戏
//     if (arr.length < 3) {
//         let new_arr: any = getGameList(
//             type,
//             game_id,
//             page,
//             limit,
//             name
//         );
//         count = new_arr.count;
//         arr = new_arr.allGameList
//     } else {
//         count = factory_list.count;

//     }
//     // 返回数据
//     let backData = {
//         allGameList: arr,
//         count: count
//     }
//     return backData
// }


// 根据类型获取游戏列表 或者厂商列表  （厂商数量小于3时获取游戏列表）
export function getTypeGameList(type: number, page: number, limit: number, name: string, game_id: any) {
    let arr = []
    let count = []
    let new_arr: any = getGameList(
        type,
        game_id,
        page,
        limit,
        name
    );
    count = new_arr.count;
    arr = new_arr.allGameList
    // 返回数据
    let backData = {
        allGameList: arr,
        count: count
    }
    return backData
}


//取消或收藏游戏
export function whetherCollectGames(id: number, tag: number) {
    tag = tag == 1 ? 0 : 1
    let tag_list = localStorage.getItem("user_game_tag_list") ? JSON.parse(localStorage.getItem("user_game_tag_list") as any) : []
    if (tag) {
        tag_list.unshift(id)
    } else {
        let arr = []
        for (let i = 0; i < tag_list.length; i++) {
            if (tag_list[i] != id) {
                arr.push(tag_list[i] as never)
            }
        }
        tag_list = arr
    }
    localStorage.setItem("user_game_tag_list", JSON.stringify(tag_list))
    return tag;
}
// 判断是否为以收藏游戏
function isTagGame(gid: number) {
    let tag_list = localStorage.getItem("user_game_tag_list") ? JSON.parse(localStorage.getItem("user_game_tag_list") as any) : []
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
// 获取游戏厂商状态
function getGameStatus(game_id) {

    const game_list = store.state.conf.game_list

    let factory_list = game_list.factory_list
    let status = 1
    for (let i = 0; i < factory_list.length; i++) {
        if (factory_list[i].game_id == game_id) {
            status = factory_list[i].status
        }
    }
    return status
}