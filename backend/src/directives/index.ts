import { type App } from "vue"
import { permission } from "./permission"
import { resize } from "./resize"

/** 挂载自定义指令 */
export function loadDirectives(app: App) {
  app.directive("permission", permission)
  app.directive("resize", resize)
}
