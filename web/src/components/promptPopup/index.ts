import { createVNode, render } from 'vue'

const comFiles = import.meta.globEager('./components/*.vue');
const pathList: string[] = [];
for (const path in comFiles) {
	pathList.push(path);
}
const coms = pathList.reduce((coms: { [x: string]: any }, modulePath: string) => {
	const value = comFiles[modulePath];
	coms[value.default.name] = value.default;
	return coms;
}, {});

// component:dom data:数据
export default (componentName, data) => {
	let timer = null;

	// 获取对应的组件
	const getComponent = () => {
		for (const key in coms) {
			if (Object.prototype.hasOwnProperty.call(coms, key)) {
				const element = coms[key];
				if (componentName == key) return element
			}
		}
	}

	const vnode = createVNode(getComponent(), { ...data })

	// 动态创建一个DOM容器
	const div = document.createElement('div')
	// div.setAttribute('class', 'my-message-container')
	document.body.appendChild(div)

	render(vnode, div)

	clearTimeout(timer as any);
	// 希望2s后消失 
	if (data.disappear) {
		timer = setTimeout(() => {
			// 清空div里面的内容
			render(null, div)
		}, 2000) as any
	}
}
