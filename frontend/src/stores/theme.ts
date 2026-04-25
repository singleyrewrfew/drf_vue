/**
 * 主题管理 Store
 *
 * 管理应用的主题模式（亮色/暗色），支持持久化存储和动态切换。
 * 主题状态会自动同步到 DOM 的 data-theme 属性和 localStorage。
 */
import {defineStore} from 'pinia'
import {ref, watch} from 'vue'

export const useThemeStore = defineStore('theme', () => {
    /**
     * 当前主题模式，从 localStorage 初始化
     * @type {import('vue').Ref<string>}
     */
    const theme = ref(localStorage.getItem('admin-theme') || 'light')

    /**
     * 设置主题模式
     *
     * 更新响应式状态、DOM 属性和本地存储，确保主题变更立即生效并持久化。
     *
     * @param {string} newTheme - 新的主题模式 ('light' 或 'dark')
     */
    const setTheme = (newTheme: string) => {
        theme.value = newTheme
        document.documentElement.setAttribute('data-theme', newTheme)
        localStorage.setItem('admin-theme', newTheme)
    }

    /**
     * 切换主题模式
     *
     * 在亮色和暗色主题之间切换。
     */
    const toggleTheme = () => {
        setTheme(theme.value === 'light' ? 'dark' : 'light')
    }

    /**
     * 监听主题变化，自动同步到 DOM
     *
     * 当主题状态改变时，立即更新 documentElement 的 data-theme 属性。
     * immediate: true 确保组件初始化时也执行一次同步。
     */
    watch(theme, (newTheme) => {
        document.documentElement.setAttribute('data-theme', newTheme)
    }, {immediate: true})

    return {
        theme,
        setTheme,
        toggleTheme
    }
})
