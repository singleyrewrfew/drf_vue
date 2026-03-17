import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'
import pinia from './stores'
import './styles/variables.css'
import './styles/main.css'
import './styles/element-override.css'
import './styles/components.css'

const savedTheme = localStorage.getItem('admin-theme') || 'light'
document.documentElement.setAttribute('data-theme', savedTheme)

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus, {
  locale: zhCn,
})
app.use(router)
app.use(pinia)
app.mount('#app')
