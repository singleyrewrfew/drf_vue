import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as userApi from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('front_token') || '')
  const user = ref(JSON.parse(localStorage.getItem('front_user') || 'null'))
  let profileCheckTimer = null

  const isLoggedIn = computed(() => !!token.value)

  const login = async (credentials) => {
    const { data } = await userApi.login(credentials)
    token.value = data.access
    user.value = data.user
    localStorage.setItem('front_token', data.access)
    localStorage.setItem('front_refresh', data.refresh)
    localStorage.setItem('front_user', JSON.stringify(data.user))
    startProfileCheck()
    return data
  }

  const register = async (userData) => {
    const { data } = await userApi.register(userData)
    return data
  }

  const logout = async () => {
    stopProfileCheck()
    try {
      const refreshToken = localStorage.getItem('front_refresh')
      if (refreshToken) {
        await userApi.logout({ refresh: refreshToken })
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
    const { data } = await userApi.getProfile()
    user.value = data
    localStorage.setItem('front_user', JSON.stringify(data))
  }

  const startProfileCheck = () => {
    if (profileCheckTimer) {
      clearInterval(profileCheckTimer)
    }
    
    profileCheckTimer = setInterval(async () => {
      if (token.value) {
        try {
          const { data } = await api.get('/auth/profile/')
          
          if (JSON.stringify(user.value) !== JSON.stringify(data)) {
            user.value = data
            localStorage.setItem('front_user', JSON.stringify(data))
          }
        } catch (error) {
          console.error('Profile check error:', error)
        }
      }
    }, 30000)
  }

  const stopProfileCheck = () => {
    if (profileCheckTimer) {
      clearInterval(profileCheckTimer)
      profileCheckTimer = null
    }
  }

  if (token.value) {
    startProfileCheck()
  }

  return {
    token,
    user,
    isLoggedIn,
    login,
    register,
    logout,
    fetchProfile,
    startProfileCheck,
    stopProfileCheck,
  }
})
