import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getProfile, login as loginApi, logout as logoutApi } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUser = (newUser) => {
    user.value = newUser
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  const login = async (credentials) => {
    const { data } = await loginApi(credentials)
    setToken(data.access)
    setUser(data.user)
    return data
  }

  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh')
      if (refreshToken) {
        await logoutApi({ refresh: refreshToken })
      }
    } catch (e) {
      console.error('Logout API error:', e)
    }
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('refresh')
  }

  const fetchProfile = async (force = false) => {
    // 如果不需要强制刷新且有缓存的用户信息，直接返回
    if (!force && user.value) {
      return user.value
    }
    
    const { data } = await getProfile()
    setUser(data)
    return data
  }

  const isLoggedIn = () => !!token.value

  const isAdmin = () => user.value?.role_code === 'admin' || user.value?.is_superuser

  const isEditor = () => ['admin', 'editor'].includes(user.value?.role_code)

  const canAccessBackend = () => !!user.value?.is_staff

  return {
    token,
    user,
    setToken,
    setUser,
    login,
    logout,
    fetchProfile,
    isLoggedIn,
    isAdmin,
    isEditor,
    canAccessBackend,
  }
})
