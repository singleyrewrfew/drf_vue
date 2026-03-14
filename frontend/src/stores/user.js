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
    
    console.log('Starting profile check timer')
    
    profileCheckTimer = setInterval(async () => {
      if (token.value) {
        try {
          console.log('Checking profile for updates...')
          const { data } = await getProfile()
          
          // 比较avatar_url字段
          const oldAvatarUrl = user.value?.avatar_url
          const newAvatarUrl = data.avatar_url
          
          console.log('Old avatar_url:', oldAvatarUrl)
          console.log('New avatar_url:', newAvatarUrl)
          console.log('Full old user:', user.value)
          console.log('Full new user:', data)
          
          // 检查是否有任何变化
          if (JSON.stringify(user.value) !== JSON.stringify(data)) {
            console.log('User info changed, updating...')
            setUser(data)
          } else {
            console.log('No changes detected')
          }
        } catch (error) {
          console.error('Profile check error:', error)
        }
      }
    }, 5000)
    console.log('Profile check timer set to run every 5 seconds')
  }

  const stopProfileCheck = () => {
    if (profileCheckTimer) {
      clearInterval(profileCheckTimer)
      profileCheckTimer = null
    }
  }

  const isLoggedIn = () => !!token.value

  const isAdmin = () => user.value?.role_code === 'admin' || user.value?.is_superuser

  const isEditor = () => ['admin', 'editor'].includes(user.value?.role_code)

  const canAccessBackend = () => !!user.value?.is_staff

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
  }
})
