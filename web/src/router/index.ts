import { createRouter, createWebHistory, createWebHashHistory } from "vue-router";
import layout from '@views/layout/index.vue'
import home from '@views/home/index.vue'
import homeIndex from '@views/home/childrens/homeIndex.vue'
import gameList from '@views/home/childrens/factoryList.vue'
import gamePage from '@views/home/childrens/gamePage.vue'
import coupon from '@views/coupon/index.vue'
import bonusCabinet from '@views/bonusCabinet/index.vue'
import refer from '@views/Refer/index.vue'
import vipBonus from '@views/vipBonus/index.vue'
import vipBonusIndex from '@/views/vipBonus/childrens/vipBonus.vue'
import allRanks from '@/views/vipBonus/childrens/allRanks.vue'
import allLevels from '@/views/vipBonus/childrens/allLevels.vue'
import pendingRewards from '@/views/vipBonus/childrens/pendingRewards.vue'
import depositBonus from '@views/depositBonus/index.vue'
import help from '@views/help/index.vue'
import bettingBouns from '@views/betbingBouns/index.vue'
import account from '@views/account/index.vue'
import about from '@views/about.vue'
import game from '@views/home/childrens/gamePage.vue'
import connectionException from '@views/connectionException/index.vue'
import Certificate from "@views/Certificate/index.vue";
import TodosOsBouns from "@/views/TODOSOSBÔNUS/index.vue";
import ActivitySubpage from "@/views/TODOSOSBÔNUS/components/ActivitySubpage.vue";
import vipDetails from "@/views/vipBonus/vipDetails.vue"
import dailyBettingBonus from "@/views/dailyBettingBonus/index.vue";
import supplyCrate from "@/views/supplyCrate/index.vue";
import iframe from "@/views/iframe/index.vue";
import signIn from "@/views/signIn/index.vue";
import clHome from "@/views/home/homeType/home.vue";
import flag from "@/views/home/homeType/flag.vue";
import in_house from "@/views/home/homeType/in-house.vue";
import hot from "@/views/home/homeType/hot.vue";
import gameType from "@/views/home/homeType/gameType.vue";
import spin from "@/views/spin/index.vue";
import physicalEducation from "@/views/physicalEducation/index.vue";
import winGo from "@/views/winGo/game.vue";
//引入在axios暴露出的clearPending函数
import { clearPending } from "../utils/http"
import { store } from "@/store";
const routes = [
	{
		path: "/",
		name: "index",
		component: layout,
		children: [
			{
				path: '/',
				name: 'home',
				component: home,
				children: [
					{
						path: '/',
						name: 'homeIndex',
						component: homeIndex,
						redirect: '/clHome',
						children: [
							{
								path: '/clHome',
								name: 'clHome',
								component: clHome,
							},
							{
								path: '/hot',
								name: 'hot',
								component: hot,
							},
							{
								path: '/flag',
								name: 'flag',
								component: flag,
							},
							{
								path: '/in-house',
								name: 'in-house',
								component: in_house,
							},
							{
								path: '/gameType/:type',
								name: 'gameType',
								component: gameType,
							},
						]
					},
					{
						path: '/gameList/:game_id',
						name: 'gameList',
						component: gameList,
					},
					{
						path: '/gamePage',
						name: 'gamePage',
						component: gamePage,
					},
				]
			},
			{
				path: '/bonusCabinet',
				name: 'bonusCabinet',
				component: bonusCabinet,
			},
			{
				path: '/coupon',
				name: 'coupon',
				component: coupon,
			},
			{
				path: '/refer',
				name: 'refer',
				component: refer,
			},
			{
				path: '/vipBonus',
				name: 'vipBonus_index',
				component: vipBonus,
				children: [
					{
						path: '/vipBonus',
						name: 'vipBonus',
						component: vipBonusIndex,
					},
					{
						path: '/vipBonus/allRanks',
						name: 'allRanks',
						component: allRanks,
					},
					{
						path: '/vipBonus/allLevels',
						name: 'allLevels',
						component: allLevels,
					},
					{
						path: '/vipBonus/pendingRewards',
						name: 'pendingRewards',
						component: pendingRewards,
					},
					{
						path: '/vipBonus/vipDetails',
						name: 'vipDetails',
						component: vipDetails,
					},
				]
			},
			// {
			// 	path: '/depositBonus',
			// 	name: 'depositBonus',
			// 	component: depositBonus,
			// },
			{
				path: '/help',
				name: 'help',
				component: help,
			},
			// {
			// 	path: '/bettingBouns',
			// 	name: 'bettingBouns',
			// 	component: bettingBouns,
			// },
			{
				path: '/account',
				name: 'account',
				component: account,
			},
			{
				path: '/about',
				name: 'about',
				component: about,
			},
			{
				path: '/play/:gid',
				name: 'playGame',
				component: game,
			},
			{
				path: '/TodosOsBouns',
				name: 'TodosOsBouns',
				component: TodosOsBouns,
			},
			{
				path: '/ActivitySubpage/:i',
				name: 'ActivitySubpage',
				component: ActivitySubpage,
			},
			// {
			// 	path: '/dailyBettingBonus',
			// 	name: 'dailyBettingBonus',
			// 	component: dailyBettingBonus,
			// },
			{
				path: '/supplyCrate',
				name: 'supplyCrate',
				component: supplyCrate,
			},
			{
				path: '/signIn',
				name: 'signIn',
				component: signIn,
			},
			{
				path: '/physicalEducation',
				name: 'physicalEducation',
				component: physicalEducation,
			},
			{
				path: "/winGo",
				name: "winGo",
				component: winGo,
			}
		],
	},
	{
		path: "/connectionException",
		name: "connectionException",
		component: connectionException,
	},
	{
		path: "/spin",
		name: "spin",
		component: spin,
	},
	{
		path: "/Certificate",
		name: "Certificate",
		component: Certificate,
	}, {
		path: "/iframe",
		name: "iframe",
		component: iframe,
	}
]

const scrollBehavior = (to, from, savedPosition) => {
	if (savedPosition && to.meta.keepAlive) {
		return savedPosition;
	}
	return { left: 0, top: 0 };
};
const router = createRouter({
	// `${import.meta.env.VITE_RES_URL}`
	// history: createWebHashHistory(),
	history: createWebHistory(),
	routes,
	scrollBehavior
})

// 动态配置favicon
const updateFavicon = () => {
	const link = document.querySelector("link[rel*='icon']") as any;
	link.rel = "icon";
	link.href = store.state.conf.all_conf.platform.platform_min_icon_url
	document.getElementsByTagName("head")[0].appendChild(link);
	document.title = store.state.conf.all_conf.platform.platform_title;
};

const interceptPathList = ['/refer', '/vipBonus', '/bonusCabinet', '/signIn'];
router.beforeEach((to, from, next) => {
	updateFavicon()
	//在跳转路由之前，先清除所有的请求
	if (store.state.user.token) {
		next()
	} else {
		if (interceptPathList.includes(to.path)) {
			router.push('/')
			store.state.status.loginShow = true;
		} else {
			next()
		}
	}

	if (document.getElementById('content_box')) {
		(document.getElementById('content_box') as any).scrollTop = 0;
	}
	clearPending()
	// ...

})

export default router