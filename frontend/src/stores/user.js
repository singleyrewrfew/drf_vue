import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getProfile, login as loginApi, logout as logoutApi } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  let profileCheckTimer = null

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
    startProfileCheck()
    return data
  }

  const logout = async () => {
    stopProfileCheck()
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
    if (!force && user.value) {
      return user.value
    }
    
    const { data } = await getProfile()
    setUser(data)
    return data
  }

  const startProfileCheck = () => {
    if (profileCheckTimer) {
      clearInterval(profileCheckTimer)
    }
    
    profileCheckTimer = setInterval(async () => {
      if (token.value) {
        try {
          const { data } = await getProfile()
          
          if (JSON.stringify(user.value) !== JSON.stringify(data)) {
            setUser(data)
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

  const isLoggedIn = () => !!token.value

  const isAdmin = () => user.value?.is_admin || user.value?.is_superuser || false

  const isEditor = () => user.value?.is_editor || user.value?.is_superuser || false

  const canAccessBackend = () => !!user.value?.is_staff

  const hasPermission = (permissionCode) => {
    if (user.value?.is_superuser) return true
    if (!user.value?.permissions) return false
    if (user.value.permissions.includes('*')) return true
    return user.value.permissions.includes(permissionCode)
  }

  const hasAnyPermission = (permissionCodes) => {
    if (user.value?.is_superuser) return true
    if (!user.value?.permissions) return false
    if (user.value.permissions.includes('*')) return true
    return permissionCodes.some(code => user.value.permissions.includes(code))
  }

  if (token.value) {
    startProfileCheck()
  }

  return {
    token,
    user,
    setToken,
    setUser,
    login,
    logout,
    fetchProfile,
    startProfileCheck,
    stopProfileCheck,
    isLoggedIn,
    isAdmin,
    isEditor,
    canAccessBackend,
    hasPermission,
    hasAnyPermission,
  }
})
