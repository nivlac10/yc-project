// 使用 defineConfig 帮手函数，这样不用 jsdoc 注解也可以获取类型提示
import { defineConfig, loadEnv } from "vite";
import vue from '@vitejs/plugin-vue';
// 引用path路径导向
import path from "path";
// 引用svg-icon
import { createSvg } from './src/icons/index';
// 实现 UI 按需引入
import styleImport from 'vite-plugin-style-import';
import ViteComponents, { ElementPlusResolver } from 'vite-plugin-components';
// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, __dirname)
  return {
    // 查看 插件 API 获取 Vite 插件的更多细节 https://www.vitejs.net/guide/api-plugin.html
    plugins: [
      vue(),
      // 这里引用了svg-icon
      createSvg('./src/icons/svg/'),
      //按需导入element-plus组件
      ViteComponents({
        customComponentResolvers: [ElementPlusResolver()],
      }),
      styleImport({
        libs: [
          {
            libraryName: 'element-plus',
            esModule: true,
            resolveStyle: (name) => {
              return `element-plus/theme-chalk/${name}.css`;
            },
            // resolveComponent: (name) => {
            //   return `element-plus/lib/components/${name}`;
            // },
          },
          {
            libraryName: 'vant',
            esModule: true,
            resolveStyle: (name) => `vant/es/${name}/style`,
          },
        ],
      }),
    ],
    // 在生产中服务时的基本路径
    base: "../",
    // 配置别名绝对路径  https://webpack.js.org/configuration/resolve/
    resolve: {
      // resolve.alias: 更轻松地为import或require某些模块创建别名
      alias: {
        // 如果报错__dirname找不到，需要安装node,执行npm install @types/node --save-dev
        "@": path.resolve(__dirname, "./src"),
        "@assets": path.resolve(__dirname, "./src/assets"),
        "@com": path.resolve(__dirname, "./src/components"),
        "@views": path.resolve(__dirname, "./src/views"),
        "@store": path.resolve(__dirname, "./src/store"),
        "@api": path.resolve(__dirname, "./src/api"),
        "@utils": path.resolve(__dirname, "./src/utils"),
      },
    },
    // esbuild: {
    //   pure: ['console.log'],
    //   minify: true
    // },
    // 与根相关的目录，构建输出将放在其中，如果目录存在，它将在构建之前被删除
    // @default 'dist'
    build: {
      outDir: env.VITE_OUTPUT_DIR,
      publicDir: 'assets',
    },
    server: {
      https: false, // 是否开启 https
      open: true, // 是否自动在浏览器打开
      port: 8001, // 端口号
      host: "0.0.0.0",
      hmr:true,
      // 跨域代理
      proxy: {
        "/api": {
          target: "http://localhost:3000", // 后台接口
          changeOrigin: true,
          // secure: false, // 如果是https接口，需要配置这个参数
          ws: true, //websocket支持
          // 截取api，并用api代替
          rewrite: (path) => path.replace(/^\/api/, "/api"),
        },
      },
    },
    // 引入第三方的配置
    optimizeDeps: {
      include: [],
    },
    css: {
      preprocessorOptions: {
        scss: {
          charset: false
        }
      },
      postcss: {
        plugins: [
          {
            postcssPlugin: 'internal:charset-removal',
            AtRule: {
              charset: (atRule) => {
                if (atRule.name === 'charset') {
                  atRule.remove();
                }
              }
            }
          }
        ],
      },
    },
  }
})
