import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('front_token') || '')
  const user = ref(JSON.parse(localStorage.getItem('front_user') || 'null'))
  let profileCheckTimer = null

  const isLoggedIn = computed(() => !!token.value)

  const login = async (credentials) => {
    const { data } = await api.post('/auth/login/', credentials)
    token.value = data.access
    user.value = data.user
    localStorage.setItem('front_token', data.access)
    localStorage.setItem('front_refresh', data.refresh)
    localStorage.setItem('front_user', JSON.stringify(data.user))
    startProfileCheck()
    return data
  }

  const register = async (userData) => {
    const { data } = await api.post('/auth/', userData)
    return data
  }

  const logout = async () => {
    stopProfileCheck()
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

  const startProfileCheck = () => {
    if (profileCheckTimer) {
      clearInterval(profileCheckTimer)
    }
    
    console.log('前台：Starting profile check timer')
    
    profileCheckTimer = setInterval(async () => {
      if (token.value) {
        try {
          console.log('前台：Checking profile for updates...')
          const { data } = await api.get('/auth/profile/')
          
          console.log('前台：Old user:', user.value)
          console.log('前台：New user:', data)
          
          if (JSON.stringify(user.value) !== JSON.stringify(data)) {
            console.log('前台：User info changed, updating...')
            user.value = data
            localStorage.setItem('front_user', JSON.stringify(data))
          } else {
            console.log('前台：No changes detected')
          }
        } catch (error) {
          console.error('前台：Profile check error:', error)
        }
      }
    }, 5000)
    console.log('前台：Profile check timer set to run every 5 seconds')
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
