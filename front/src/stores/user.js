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
    
    try {
      const savedUser = localStorage.getItem(STORAGE_KEYS.USER)
      
      if (savedUser && savedUser !== 'undefined') {
        const parsed = JSON.parse(savedUser)
        // 检查是否是错误的 response 对象（包含 status 字段）
        if (parsed.status && parsed.data) {
          localStorage.removeItem(STORAGE_KEYS.USER)
          user.value = null
        } else {
          // 解析后创建新对象确保响应式
          user.value = { ...parsed }
        }
      } else {
        user.value = null
      }
    } catch (e) {
      console.error('Failed to parse user data from storage:', e)
      user.value = null
      localStorage.removeItem(STORAGE_KEYS.USER)
    }
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
        const response = await userApi.getProfile()
        // axios 响应拦截器已经将 responseData.data 赋值给 response.data
        const data = response.data || response
        
        if (isActive && JSON.stringify(user.value) !== JSON.stringify(data)) {
          // 创建新对象确保响应式更新
          user.value = { ...data }
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
    const response = await userApi.login(credentials)
    
    // axios 响应拦截器已经将 responseData.data 赋值给 response.data
    const data = response.data
    
    token.value = data.access
    refreshToken.value = data.refresh
    // 使用 Object.assign 确保响应式更新
    if (data.user) {
      user.value = { ...data.user }  // 创建新对象触发响应式
    }
    saveToStorage()
    return data
  }

  const register = async (userData) => {
    const data = await userApi.register(userData)
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
    const response = await userApi.getProfile()
    
    // axios 响应拦截器已经将 responseData.data 赋值给 response.data
    const data = response.data || response
    
    // 创建新对象确保响应式更新
    user.value = { ...data }
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(data))
  }

  const refreshAccessToken = async () => {
    if (!refreshToken.value) {
      throw new Error('No refresh token')
    }
    
    try {
      const data = await userApi.refreshToken({ refresh: refreshToken.value })
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
