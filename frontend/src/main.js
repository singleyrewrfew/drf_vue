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

import 'md-editor-v3/lib/style.css'
import './styles/md-editor-override.css'

const savedTheme = localStorage.getItem('admin-theme') || 'light'
document.documentElement.setAttribute('data-theme', savedTheme)

const originalConsoleError = console.error
console.error = (...args) => {
    const message = args[0]
    if (typeof message === 'string' && /ERR_ABORTED/i.test(message)) {
        return
    }
    originalConsoleError.apply(console, args)
}

const app = createApp(App)

app.use(ElementPlus, {
  locale: zhCn,
})
app.use(router)
app.use(pinia)
app.mount('#app')
