import { InjectionKey } from 'vue';
import { createStore, useStore as baseUseStore, Store } from 'vuex';
import { RootStateTypes } from './interface/index';
import createPersistedState from 'vuex-persistedstate'; // 数据持久化

// Vite supports importing multiple modules from the file system using the special import.meta.glob function
// see https://cn.vitejs.dev/guide/features.html#glob-import
// 导入模块化里面的文件
const modulesFiles = import.meta.globEager('./modules/*.ts');
const pathList: string[] = [];
for (const path in modulesFiles) {
	pathList.push(path);
}
const modules = pathList.reduce((modules: { [x: string]: any }, modulePath: string) => {
	const moduleName = modulePath.replace(/^\.\/modules\/(.*)\.\w+$/, '$1');
	const value = modulesFiles[modulePath];
	modules[moduleName] = value.default;
	return modules;
}, {});

// 创建一个InjectionKey
export const key: InjectionKey<Store<RootStateTypes>> = Symbol()

export const store = createStore<RootStateTypes>({
	modules,
	plugins: [
		createPersistedState({
			// 本地存储名字
			// key: "bigwin777stros",
			// 指定需要存储的模块
			// paths: ["conf", "user"],
		}),
	]
});

export function useStore() {
	return baseUseStore(key);
}