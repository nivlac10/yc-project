import { defineConfig, presetAttributify, presetUno } from "unocss"

export default defineConfig({
  /** 预设 */
  presets: [
    /** 属性化模式 & 无值的属性模式 */
    presetAttributify(),
    /** 默认预设 */
    presetUno()
  ],
  /** 自定义规则 */
  rules: [
    ["uno-padding-20", { padding: "20px" }],
    ["uno-height-full", { height: '100%' }],
    ["uno-margin-top", { margin: "20px 0 0 0" }],
    ["uno-pop-item", { display: 'grid', 'grid-template-columns': '20%1fr' }],
    ["uno-padding-left-20", { padding: "0  0 0 20px" }]
  ],
  /** 自定义快捷方式 */
  shortcuts: {
    "uno-wh-full": "w-full h-full",
    "uno-flex-center": "flex justify-center items-center",
    "uno-flex-x-center": "flex justify-center",
    "uno-flex-y-center": "flex items-center",
  }
})
