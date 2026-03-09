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
      await logoutApi({ refresh: localStorage.getItem('refresh') })
    } catch (e) {
      console.error(e)
    }
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('refresh')
  }

  const fetchProfile = async () => {
    const { data } = await getProfile()
    setUser(data)
    return data
  }

  const isLoggedIn = () => !!token.value

  const isAdmin = () => user.value?.role_code === 'admin'

  const isEditor = () => ['admin', 'editor'].includes(user.value?.role_code)

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
  }
})
