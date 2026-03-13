import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api',
  timeout: 30000,
})

api.interceptors.request.use(
  (config) => {
    let token = localStorage.getItem('front_token')
    if (!token) {
      token = localStorage.getItem('token')
      if (token) {
        localStorage.setItem('front_token', token)
        localStorage.removeItem('token')
      }
    }
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('front_token')
      localStorage.removeItem('front_user')
      localStorage.removeItem('front_refresh')
      
      if (router.currentRoute.value.meta.requiresAuth) {
        ElMessage.warning('登录已过期，请重新登录')
        router.push('/login')
      }
      return Promise.reject(error)
    } else if (error.response?.status === 403) {
      ElMessage.error('没有权限访问')
    } else if (error.response?.status === 404) {
      ElMessage.error('请求的资源不存在')
    } else if (error.response?.status === 500) {
      ElMessage.error('服务器错误，请稍后重试')
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请稍后重试')
    }
    return Promise.reject(error)
  }
)

export default api
