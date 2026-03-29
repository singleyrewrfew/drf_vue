import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('mobileUser', () => {
    const token = ref(localStorage.getItem('mobile_token') || '')
    const user = ref(JSON.parse(localStorage.getItem('mobile_user') || 'null'))

    const isLoggedIn = computed(() => !!token.value)

    const login = async credentials => {
        const { data } = await api.post('/auth/login/', credentials)
        token.value = data.access
        user.value = data.user
        localStorage.setItem('mobile_token', data.access)
        localStorage.setItem('mobile_refresh', data.refresh)
        localStorage.setItem('mobile_user', JSON.stringify(data.user))
        return data
    }

    const register = async userData => {
        const { data } = await api.post('/auth/', userData)
        return data
    }

    const logout = async () => {
        try {
            const refreshToken = localStorage.getItem('mobile_refresh')
            if (refreshToken) {
                await api.post('/auth/logout/', { refresh: refreshToken })
            }
        } catch (e) {
            console.error(e)
        }
        token.value = ''
        user.value = null
        localStorage.removeItem('mobile_token')
        localStorage.removeItem('mobile_refresh')
        localStorage.removeItem('mobile_user')
    }

    const fetchProfile = async () => {
        const { data } = await api.get('/auth/profile/')
        user.value = data
        localStorage.setItem('mobile_user', JSON.stringify(data))
    }

    return {
        token,
        user,
        isLoggedIn,
        login,
        register,
        logout,
        fetchProfile,
    }
})
