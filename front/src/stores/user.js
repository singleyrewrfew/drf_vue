import { defineStore } from 'pinia'
import { ref, computed, watchEffect } from 'vue'
import * as userApi from '@/api/user'

const STORAGE_KEYS = {
  TOKEN: 'front_token',
  REFRESH: 'front_refresh',
  USER: 'front_user',
  OLD_TOKEN: 'token',
  OLD_REFRESH: 'refresh'
}

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const refreshToken = ref('')
  const user = ref(null)

  const isLoggedIn = computed(() => !!token.value)

  const initFromStorage = () => {
    let savedToken = localStorage.getItem(STORAGE_KEYS.TOKEN)
    let savedRefresh = localStorage.getItem(STORAGE_KEYS.REFRESH)
    
    if (!savedToken) {
      const oldToken = localStorage.getItem(STORAGE_KEYS.OLD_TOKEN)
      if (oldToken) {
        savedToken = oldToken
        localStorage.setItem(STORAGE_KEYS.TOKEN, oldToken)
        localStorage.removeItem(STORAGE_KEYS.OLD_TOKEN)
      }
    }
    
    if (!savedRefresh) {
      const oldRefresh = localStorage.getItem(STORAGE_KEYS.OLD_REFRESH)
      if (oldRefresh) {
        savedRefresh = oldRefresh
        localStorage.setItem(STORAGE_KEYS.REFRESH, oldRefresh)
        localStorage.removeItem(STORAGE_KEYS.OLD_REFRESH)
      }
    }
    
    token.value = savedToken || ''
    refreshToken.value = savedRefresh || ''
    user.value = JSON.parse(localStorage.getItem(STORAGE_KEYS.USER) || 'null')
  }

  const saveToStorage = () => {
    if (token.value) {
      localStorage.setItem(STORAGE_KEYS.TOKEN, token.value)
      localStorage.setItem(STORAGE_KEYS.REFRESH, refreshToken.value)
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user.value))
    } else {
      localStorage.removeItem(STORAGE_KEYS.TOKEN)
      localStorage.removeItem(STORAGE_KEYS.REFRESH)
      localStorage.removeItem(STORAGE_KEYS.USER)
    }
  }

  const clearStorage = () => {
    token.value = ''
    refreshToken.value = ''
    user.value = null
    localStorage.removeItem(STORAGE_KEYS.TOKEN)
    localStorage.removeItem(STORAGE_KEYS.REFRESH)
    localStorage.removeItem(STORAGE_KEYS.USER)
  }

  watchEffect((onCleanup) => {
    if (!token.value) {
      return
    }

    let isActive = true
    let timerId = null

    const checkProfile = async () => {
      if (!isActive || !token.value) return
      
      try {
        const { data } = await userApi.getProfile()
        if (isActive && JSON.stringify(user.value) !== JSON.stringify(data)) {
          user.value = data
          localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(data))
        }
      } catch (error) {
        console.error('Profile check error:', error)
      }
    }

    checkProfile()
    timerId = setInterval(checkProfile, 30000)

    onCleanup(() => {
      isActive = false
      if (timerId) {
        clearInterval(timerId)
        timerId = null
      }
    })
  })

  const login = async (credentials) => {
    const { data } = await userApi.login(credentials)
    token.value = data.access
    refreshToken.value = data.refresh
    user.value = data.user
    saveToStorage()
    return data
  }

  const register = async (userData) => {
    const { data } = await userApi.register(userData)
    return data
  }

  const logout = async () => {
    try {
      if (refreshToken.value) {
        await userApi.logout({ refresh: refreshToken.value })
      }
    } catch (e) {
      console.error(e)
    }
    clearStorage()
  }

  const fetchProfile = async () => {
    const { data } = await userApi.getProfile()
    user.value = data
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(data))
  }

  const refreshAccessToken = async () => {
    if (!refreshToken.value) {
      throw new Error('No refresh token')
    }
    
    try {
      const { data } = await userApi.refreshToken({ refresh: refreshToken.value })
      token.value = data.access
      if (data.refresh) {
        refreshToken.value = data.refresh
      }
      saveToStorage()
    } catch (error) {
      clearStorage()
      throw error
    }
  }

  initFromStorage()

  return {
    token,
    refreshToken,
    user,
    isLoggedIn,
    login,
    register,
    logout,
    fetchProfile,
    refreshAccessToken
  }
})
