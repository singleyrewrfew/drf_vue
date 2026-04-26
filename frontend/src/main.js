import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'
import pinia from './stores'
import './styles/variables.css'
import './styles/main.css'
import './styles/element-override.css'
import './styles/components.css'

/**
 * 初始化主题配置
 * 从本地存储中读取用户之前保存的主题设置，如果不存在则使用默认的浅色主题
 * 将主题设置应用到 HTML 根元素上，以便 CSS 变量能够根据主题切换样式
 */
const savedTheme = localStorage.getItem('admin-theme') || 'light'
document.documentElement.setAttribute('data-theme', savedTheme)

/**
 * 创建 Vue 应用实例并配置全局插件
 * - ElementPlus UI 组件库（使用中文语言包）
 * - Vue Router 路由管理器
 * - Pinia 状态管理库
 * 最后将应用挂载到 DOM 中的 #app 元素上
 */
const app = createApp(App)

app.use(ElementPlus, {
  locale: zhCn,
})
app.use(router)
app.use(pinia)
app.mount('#app')
