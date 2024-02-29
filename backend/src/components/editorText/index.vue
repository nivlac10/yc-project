<template>
    <div style="border: 1px solid #ccc" class="editorText">
        <Toolbar style="border-bottom: 1px solid #ccc" :editor="editorRef" :defaultConfig="toolbarConfig" :mode="mode" />
        <Editor style="height: 500px; overflow-y: hidden;" v-model="valueHtml" :defaultConfig="editorConfig" :mode="mode"
            @onCreated="handleCreated" @onChange="handleChange" />
    </div>
</template>
<script lang="ts">
import '@wangeditor/editor/dist/css/style.css' // 引入 css
import { onBeforeUnmount, ref, shallowRef, defineComponent } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
export default defineComponent({
    components: { Editor, Toolbar },
    props: {
        info: {
            type: String,
        }
    },
    setup(props, { emit }) {
        // 编辑器实例，必须用 shallowRef
        const editorRef = shallowRef()

        // 内容 HTML
        const valueHtml = ref(props.info)

        // 模拟 ajax 异步获取内容
        // onMounted(() => {
        //     setTimeout(() => {
        //         valueHtml.value = '<p>模拟 Ajax 异步设置内容</p>'
        //     }, 1500)
        // })

        const toolbarConfig = {}
        const editorConfig = { placeholder: '请输入内容...' }

        // 组件销毁时，也及时销毁编辑器
        onBeforeUnmount(() => {
            const editor = editorRef.value
            if (editor == null) return
            editor.destroy()
        })

        const handleCreated = (editor) => {
            editorRef.value = editor // 记录 editor 实例，重要！
        }
        const handleChange = (editor) => {
            emit("def", valueHtml.value)
        }
        return {
            editorRef,
            valueHtml,
            mode: 'default', // 或 'simple'
            toolbarConfig,
            editorConfig,
            handleCreated,
            handleChange
        };
    }
})
</script>    
<style  lang="scss" scoped>
.editorText {
    height: auto;
    // overflow-y: scroll;
}
</style>
  