import {defineStore} from 'pinia'
import {ref, watch} from 'vue'

/**
 * 主题管理 Store
 * 用于管理应用的明暗主题切换，并持久化存储用户偏好
 */
export const useThemeStore = defineStore('theme', () => {
    // 从 localStorage 读取主题设置，默认为 'light'
    const theme = ref(localStorage.getItem('theme') || 'light')

    /**
     * 应用主题到页面
     * @param {string} newTheme - 新主题值 ('light' 或 'dark')
     */
    const applyTheme = (newTheme) => {
        // 设置 HTML 根元素的 data-theme 属性
        document.documentElement.setAttribute('data-theme', newTheme)
        // 将主题设置保存到 localStorage
        localStorage.setItem('theme', newTheme)
    
        // 更新移动端浏览器地址栏颜色
        const metaThemeColor = document.querySelector('meta[name="theme-color"]')
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', newTheme === 'dark' ? '#1A1A1A' : '#FFFFFF')
        }
    }

    /**
     * 切换主题（明暗互换）
     */
    const toggleTheme = () => {
        theme.value = theme.value === 'light' ? 'dark' : 'light'
    }

    /**
     * 设置指定主题
     * @param {string} newTheme - 要设置的主题值 ('light' 或 'dark')
     */
    const setTheme = (newTheme) => {
        theme.value = newTheme
    }

    // 监听主题变化，自动应用新主题
    watch(theme, (newTheme) => {
        applyTheme(newTheme)
    }, {immediate: true})

    return {
        theme,
        toggleTheme,
        setTheme
    }
})
