import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('front_token') || '')
  const user = ref(JSON.parse(localStorage.getItem('front_user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)

  const login = async (credentials) => {
    const { data } = await api.post('/auth/login/', credentials)
    token.value = data.access
    user.value = data.user
    localStorage.setItem('front_token', data.access)
    localStorage.setItem('front_refresh', data.refresh)
    localStorage.setItem('front_user', JSON.stringify(data.user))
    return data
  }

  const register = async (userData) => {
    const { data } = await api.post('/auth/', userData)
    return data
  }

  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('front_refresh')
      if (refreshToken) {
        await api.post('/auth/logout/', { refresh: refreshToken })
      }
    } catch (e) {
      console.error(e)
    }
    token.value = ''
    user.value = null
    localStorage.removeItem('front_token')
    localStorage.removeItem('front_refresh')
    localStorage.removeItem('front_user')
  }

  const fetchProfile = async () => {
    const { data } = await api.get('/auth/profile/')
    user.value = data
    localStorage.setItem('front_user', JSON.stringify(data))
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
