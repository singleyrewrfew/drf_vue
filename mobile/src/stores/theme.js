import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('mobileTheme', () => {
    const theme = ref(localStorage.getItem('mobile_theme') || 'light')

    const toggleTheme = () => {
        theme.value = theme.value === 'light' ? 'dark' : 'light'
    }

    const setTheme = newTheme => {
        theme.value = newTheme
    }

    watch(
        theme,
        newTheme => {
            localStorage.setItem('mobile_theme', newTheme)
            document.documentElement.setAttribute('data-theme', newTheme)

            if (newTheme === 'dark') {
                document.documentElement.classList.add('dark')
                document.documentElement.style.backgroundColor = '#121212'
            } else {
                document.documentElement.classList.remove('dark')
                document.documentElement.style.backgroundColor = '#F6F6F6'
            }
        },
        { immediate: true }
    )

    return {
        theme,
        toggleTheme,
        setTheme,
    }
})
