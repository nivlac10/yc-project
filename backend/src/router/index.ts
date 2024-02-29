import { type RouteRecordRaw, createRouter, createWebHashHistory, createWebHistory } from "vue-router"

const Layout = () => import("@/layout/index.vue")

/** 常驻路由 */
export const constantRoutes: RouteRecordRaw[] = [
  {
    path: "/redirect",
    component: Layout,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "/redirect/:path(.*)",
        component: () => import("@/views/redirect/index.vue")
      }
    ]
  },
  {
    path: "/403",
    component: () => import("@/views/error-page/403.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/404",
    component: () => import("@/views/error-page/404.vue"),
    meta: {
      hidden: true
    },
    alias: "/:pathMatch(.*)*"
  },
  {
    path: "/templateTabel",
    component: () => import("@/views/table.vue"),
    // meta: {
    //   hidden: true
    // },
  },
  {
    path: "/login",
    component: () => import("@/views/login/index.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/",
    component: Layout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        component: () => import("@/views/dashboard/index.vue"),
        name: "Dashboard",
        meta: {
          title: "首页",
          svgIcon: "dashboard",
          affix: true
        }
      }
    ]
  }
]

/**
 * 动态路由
 * 用来放置有权限 (Roles 属性) 的路由
 * 必须带有 Name 属性
 */
export const asyncRoutes: RouteRecordRaw[] = [,
  {
    path: "/timePeriodAnalysis",
    component: Layout,
    redirect: "/timePeriodAnalysis",
    children: [
      {
        path: "timePeriodAnalysis",
        component: () => import("@/views/timePeriodAnalysis/index.vue"),
        name: "timePeriodAnalysis",
        meta: {
          title: "时段分析",
          svgIcon: "dashboard",
          roles: ["1"], // 可以在根路由中设置角色
          affix: true
        }
      }
    ]
  },
  {
    path: "/SystemManagement",
    component: Layout,
    redirect: "/SystemManagement/index",
    name: "SystemManagement",
    meta: {
      title: "系统管理",
      elIcon: "Setting",
      roles: ["1"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "UserList",
        component: () => import("@/views/SystemManagement/UserList.vue"),
        name: "UserList",
        meta: {
          title: "管理员列表",
          elIcon: "User",
          roles: ["1"]
        }
      }
    ]
  },
  {
    path: "/:pathMatch(.*)*", // Must put the 'ErrorPage' route at the end, 必须将 'ErrorPage' 路由放在最后
    redirect: "/404",
    name: "ErrorPage",
    meta: {
      hidden: true
    }
  },
  {
    path: "/logManagement",
    component: Layout,
    redirect: "/logManagement/loginRecord",
    name: "logManagement",
    meta: {
      title: "系统日志",
      elIcon: "ChatRound",
      roles: ["1", "3"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "/logManagement/loginRecord",
        component: () => import("@/views/logManagement/loginRecord.vue"),
        name: "loginRecord",
        meta: {
          title: "登陆记录",
          roles: ["1"]
        }
      },
      {
        path: "/logManagement/userBlacklist",
        component: () => import("@/views/logManagement/userBlacklist.vue"),
        name: "userBlacklist",
        meta: {
          title: "用户黑名单",
          roles: ["1", "3"]
        }
      },
      {
        path: "/logManagement/exceptionList",
        component: () => import("@/views/logManagement/exceptionList.vue"),
        name: "exceptionList",
        meta: {
          title: "异常列表",
          roles: ["1", "3"]
        }
      },
      {
        path: "/logManagement/iPBlacklist",
        component: () => import("@/views/logManagement/iPBlacklist.vue"),
        name: "iPBlacklist",
        meta: {
          title: "IP黑名单",
          roles: ["1", "3"]
        }
      },
      {
        path: "/logManagement/cardNumberBlacklist",
        component: () => import("@/views/logManagement/cardNumberBlacklist.vue"),
        name: "cardNumberBlacklist",
        meta: {
          title: "卡号黑名单",
          roles: ["1", "3"]
        }
      },
    ]
  },
  {
    path: "/channelManagement",
    component: Layout,
    redirect: "/channelManagement/proxyList",
    name: "channelManagement",
    meta: {
      title: "渠道管理",
      elIcon: "Share",
      roles: ["1", "3"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "/channelManagement/proxyList",
        component: () => import("@/views/channelManagement/proxyList.vue"),
        name: "proxyList",
        meta: {
          title: "代理列表",
          roles: ["1"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/channelManagement/channelList",
        component: () => import("@/views/channelManagement/channelList.vue"),
        name: "channelList",
        meta: {
          title: "渠道列表",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      }
    ]
  },
  {
    path: "/vipsystemManagement",
    component: Layout,
    redirect: "/vipsystemManagement/vipManage",
    name: "vipsystemManagement",
    meta: {
      title: "vip系统",
      elIcon: "StarFilled",
      roles: ["1", "3"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "/vipsystemManagement/vipManage",
        component: () => import("@/views/vipsystemManagement/vipManage.vue"),
        name: "vipManage",
        meta: {
          title: "vip管理",
          roles: ["1"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/vipsystemManagement/vipBonusManage",
        component: () => import("@/views/vipsystemManagement/vipBonusManage.vue"),
        name: "vipBonusManage",
        meta: {
          title: "vip奖励记录",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/vipsystemManagement/vipSplicBonusManage",
        component: () => import("@/views/vipsystemManagement/vipSplicBonusManage.vue"),
        name: "vipSplicBonusManage",
        meta: {
          title: "vip奖励明细记录",
          roles: ["1"] // 或者在子导航中设置角色
        }
      },
    ]
  },
  {
    path: "/userManagenment",
    component: Layout,
    redirect: "/userManagenment/memberList",
    name: "userManagenment",
    meta: {
      title: "用户管理",
      elIcon: "User",
      roles: ["1", "3"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "/userManagenment/memberList",
        component: () => import("@/views/userManagenment/memberList.vue"),
        name: "memberList",
        meta: {
          title: "会员列表",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/userManagenment/balanceLog",
        component: () => import("@/views/userManagenment/balanceLog.vue"),
        name: "balanceLog",
        meta: {
          title: "余额日志",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/userManagenment/mailManagement",
        component: () => import("@/views/userManagenment/mailManagement.vue"),
        name: "mailManagement",
        meta: {
          title: "邮件管理",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/userManagenment/userInfo/:uid",
        beforeEnter: (to, from, next) => {
          if (to.params.uid) {
            to.meta.title = '用户信息:' + to.params.uid
          } else {
            to.meta.title = '用户信息'
          }
          next()
        },
        component: () => import("@/views/userManagenment/userInfo.vue"),
        name: "userInfo",
        meta: {
          title: "用户信息",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
    ]
  },
  {
    path: "/gameManagement",
    component: Layout,
    redirect: "/gameManagement/integratorList",
    name: "gameManagement",
    meta: {
      title: "游戏管理",
      svgIcon: "game",
      roles: ["1"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "/gameManagement/gameType",
        component: () => import("@/views/gameManagement/gameType.vue"),
        name: "gameType",
        meta: {
          title: "游戏类型",
          svgIcon: ""
        }
      },
      {
        path: "/gameManagement/integratorList",
        component: () => import("@/views/gameManagement/integratorList.vue"),
        name: "integratorList",
        meta: {
          title: "集成商管理",
          svgIcon: ""
        }
      },
      {
        path: "/gameManagement/gamingPlatformManagement",
        component: () => import("@/views/gameManagement/gamingPlatformManagement.vue"),
        name: "gamingPlatformManagement",
        meta: {
          title: "游戏平台管理",
          svgIcon: ""
        }
      },
      {
        path: "/gameManagement/gameManagement",
        component: () => import("@/views/gameManagement/gameManagement.vue"),
        name: "gameManagement_index",
        meta: {
          title: "游戏管理",
          svgIcon: ""
        }
      },
      {
        path: "/gameManagement/gameRecord",
        component: () => import("@/views/gameManagement/gameRecord.vue"),
        name: "gameRecord",
        meta: {
          title: "游戏记录",
          svgIcon: ""
        }
      },
      {
        path: "/gameManagement/subGameSummary",
        component: () => import("@/views/gameManagement/subGameSummary.vue"),
        name: "subGameSummary",
        meta: {
          title: "子游戏汇总",
          svgIcon: ""
        }
      },
      {
        path: "/gameManagement/gamePlatformSummary",
        component: () => import("@/views/gameManagement/gamePlatformSummary.vue"),
        name: "gamePlatformSummary",
        meta: {
          title: "游戏平台汇总",
          svgIcon: ""
        }
      },
      {
        path: "/gameManagement/integratorSummary",
        component: () => import("@/views/gameManagement/integratorSummary.vue"),
        name: "integratorSummary",
        meta: {
          title: "集成商汇总",
          svgIcon: ""
        }
      },
    ]
  },
  {
    path: "/platformManagement",
    component: Layout,
    redirect: "/platformManagement/rechargeActivity",
    name: "platformManagement",
    meta: {
      title: "活动配置",
      svgIcon: "Activity",
      roles: ["1", "3"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "/platformManagement/serverConf",
        component: () => import("@/views/platformManagement/serverConf.vue"),
        name: "serverConf",
        meta: {
          title: "系统配置",
          roles: ["1"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/platformManagement/rechargeActivity",
        component: () => import("@/views/platformManagement/rechargeActivity.vue"),
        name: "rechargeActivity",
        meta: {
          title: "充值活动",
          roles: ["1"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/platformManagement/announcementManagement",
        component: () => import("@/views/platformManagement/announcementManagement.vue"),
        name: "announcementManagement",
        meta: {
          title: "平台公告",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/platformManagement/activeConfiguration",
        component: () => import("@/views/platformManagement/activeConfiguration.vue"),
        name: "activeConfiguration",
        meta: {
          title: "活动公告",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/platformManagement/commissionConfiguration",
        component: () => import("@/views/platformManagement/commissionConfiguration.vue"),
        name: "commissionConfiguration",
        meta: {
          title: "佣金配置",
          roles: ["1"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/platformManagement/carouselManagement",
        component: () => import("@/views/platformManagement/carouselManagement.vue"),
        name: "carouselManagement",
        meta: {
          title: "轮播图管理",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/platformManagement/redemption_code",
        component: () => import("@/views/platformManagement/redemption_code.vue"),
        name: "redemption_code",
        meta: {
          title: "兑换码",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/platformManagement/plateAlertManagement",
        component: () => import("@/views/platformManagement/plateAlertManagement.vue"),
        name: "plateAlertManagement",
        meta: {
          title: "平台功能弹窗",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      // {
      //   path: "/platformManagement/codeAnti-waterRecord",
      //   component: () => import("@/views/platformManagement/codeAnti-waterRecord.vue"),
      //   name: "codeAnti-waterRecord",
      //   meta: {
      //     title: "打码反水",
      //     roles: ["1"] // 或者在子导航中设置角色
      //   }
      // },


    ]
  },
  {
    path: "/paymentManagement",
    component: Layout,
    redirect: "/paymentManagement/paymentChannel",
    name: "paymentManagement",
    meta: {
      title: "支付管理",
      elIcon: "CreditCard",
      roles: ["1", "3"],// 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "/paymentManagement/paymentChannel",
        component: () => import("@/views/paymentManagement/paymentChannel.vue"),
        name: "paymentChannel",
        meta: {
          title: "支付通道",
          roles: ["1"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/paymentManagement/Order_analysis",
        component: () => import("@/views/paymentManagement/Order_analysis.vue"),
        name: "Order_analysis",
        meta: {
          title: "下单分析",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/paymentManagement/withdrawal_Analysis",
        component: () => import("@/views/paymentManagement/withdrawal_Analysis.vue"),
        name: "withdrawal_Analysis",
        meta: {
          title: "提现分析",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/paymentManagement/payList",
        component: () => import("@/views/paymentManagement/payList.vue"),
        name: "payList",
        meta: {
          title: "充值列表",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/paymentManagement/withdrawalList",
        component: () => import("@/views/paymentManagement/withdrawalList.vue"),
        name: "withdrawalList",
        meta: {
          title: "提现列表",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
    ],


  },
  {
    path: "/logrecordManagement",
    component: Layout,
    redirect: "/logrecordManagement/codeAnti-waterRecordLog",
    name: "logrecordManagement",
    meta: {
      title: "日志记录",
      elIcon: "DocumentCopy",
      roles: ["1", "3"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "/logrecordManagement/rechargeBonusLog",
        component: () => import("@/views/logrecordManagement/rechargeBonusLog.vue"),
        name: "rechargeBonusLog",
        meta: {
          title: "充值奖励记录",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/logrecordManagement/codeLog",
        component: () => import("@/views/logrecordManagement/codeLog.vue"),
        name: "codeLog",
        meta: {
          title: "打码清零记录",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/logrecordManagement/codeAnti-waterRecordLog",
        component: () => import("@/views/logrecordManagement/codeAnti-waterRecordLog.vue"),
        name: "codeAnti-waterRecordLog",
        meta: {
          title: "打码反水记录",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/logrecordManagement/loseMoney",
        component: () => import("@/views/logrecordManagement/loseMoney.vue"),
        name: "loseMoney",
        meta: {
          title: "破产补助记录",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/logrecordManagement/rollerMoneyLog",
        component: () => import("@/views/logrecordManagement/rollerMoneyLog.vue"),
        name: "rollerMoneyLog",
        meta: {
          title: "转轮奖励日志",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/logrecordManagement/gameCodeBonusLog",
        component: () => import("@/views/logrecordManagement/gameCodeBonusLog.vue"),
        name: "gameCodeBonusLog",
        meta: {
          title: "下载app奖励日志",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/logrecordManagement/giveCodelog",
        component: () => import("@/views/logrecordManagement/giveCodelog.vue"),
        name: "giveCodelog",
        meta: {
          title: "优惠券领取记录",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/logrecordManagement/rechargeAchieveLog",
        component: () => import("@/views/logrecordManagement/rechargeAchieveLog.vue"),
        name: "rechargeAchieveLog",
        meta: {
          title: "充值成就领取日志",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/logrecordManagement/inviteTaskLog",
        component: () => import("@/views/logrecordManagement/inviteTaskLog.vue"),
        name: "inviteTaskLog",
        meta: {
          title: "佣金邀请任务日志",
          roles: ["1", "3"]// 或者在子导航中设置角色
        }
      },
      {
        path: "/logrecordManagement/dailyLogIn",
        component: () => import("@/views/logrecordManagement/dailyLogIn.vue"),
        name: "dailyLogIn",
        meta: {
          title: "日签到记录",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      }, ,
      {
        path: "/logrecordManagement/dayJumpLog",
        component: () => import("@/views/logrecordManagement/dayJumpLog.vue"),
        name: "dayJumpLog",
        meta: {
          title: "每日活跃记录",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
    ]
  },
  {
    path: "/dataReport",
    component: Layout,
    redirect: "/dataReport/dailyData",
    name: "dataReport",
    meta: {
      title: "数据报表",
      elIcon: "DataLine",
      roles: ["1", "3"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "/dataReport/userReport",
        component: () => import("@/views/dataReport/userReport.vue"),
        name: "userReport",
        meta: {
          title: "用户报表",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/dataReport/RegistrationRatio",
        component: () => import("@/views/dataReport/RegistrationRatio.vue"),
        name: "RegistrationRatio",
        meta: {
          title: "注册占比",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/dataReport/playerRetention",
        component: () => import("@/views/dataReport/playerRetention.vue"),
        name: "playerRetention",
        meta: {
          title: "玩家留存",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/dataReport/paidToKeep",
        component: () => import("@/views/dataReport/paidToKeep.vue"),
        name: "paidToKeep",
        meta: {
          title: "付费留存",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/dataReport/eventSummary",
        component: () => import("@/views/dataReport/eventSummary.vue"),
        name: "eventSummary",
        meta: {
          title: "事件汇总",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/dataReport/userRetention",
        component: () => import("@/views/dataReport/userRetention.vue"),
        name: "userRetention",
        meta: {
          title: "用户留存",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
      {
        path: "/dataReport/paidAnalysis",
        component: () => import("@/views/dataReport/paidAnalysis.vue"),
        name: "paidAnalysis",
        meta: {
          title: "付费分析",
          roles: ["1", "3"] // 或者在子导航中设置角色
        }
      },
    ],

  },


]

const router = createRouter({
  history:
    import.meta.env.VITE_ROUTER_HISTORY === "hash"
      ? createWebHashHistory(import.meta.env.VITE_PUBLIC_PATH)
      : createWebHistory(import.meta.env.VITE_PUBLIC_PATH),
  routes: constantRoutes
})

/** 重置路由 */
export function resetRouter() {
  // 注意：所有动态路由路由必须带有 Name 属性，否则可能会不能完全重置干净
  try {
    router.getRoutes().forEach((route) => {
      const { name, meta } = route
      if (name && meta.roles?.length) {
        router.hasRoute(name) && router.removeRoute(name)
      }
    })
  } catch {
    // 强制刷新浏览器也行，只是交互体验不是很好
    window.location.reload()
  }
}

export default router
