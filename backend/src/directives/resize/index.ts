import { type Directive } from "vue"

export const resize: Directive = {
  mounted(el, binding) {
    let width = '', height = '';
    function isReize() {
      const style = document.defaultView.getComputedStyle(el);
      if (width !== style.width || height !== style.height) {
        // 关键(这传入的是函数,所以执行此函数)
        binding.value({ width: style.width, height: style.height });
      }
      width = style.width;
      height = style.height;
    }
    el.__vueSetInterval__ = setInterval(isReize, 300);
  }
}
