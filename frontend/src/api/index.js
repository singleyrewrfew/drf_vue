import axios from 'axios'
import { useUserStore } from '@/stores/user'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    // 每次成功响应后都检查用户权限
    const userStore = useUserStore()
    if (userStore.isLoggedIn() && !userStore.canAccessBackend()) {
      // 用户失去了后台权限，清除登录状态并跳转
      userStore.logout()
      router.push({ name: 'Login', query: { error: 'no_permission' } })
    }
    return response
  },
  async (error) => {
    const userStore = useUserStore()
    
    if (error.response?.status === 401) {
      // 未授权，清除登录状态并跳转
      userStore.logout()
      router.push('/login')
    } else if (error.response?.status === 403) {
      // 权限不足，检查是否是因为失去了后台访问权限
      if (userStore.isLoggedIn()) {
        try {
          // 重新获取用户信息
          await userStore.fetchProfile()
          // 如果确实没有后台权限，清除登录状态并跳转
          if (!userStore.canAccessBackend()) {
            userStore.logout()
            router.push({ name: 'Login', query: { error: 'no_permission' } })
          }
        } catch (e) {
          console.error('Failed to fetch user profile:', e)
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api
