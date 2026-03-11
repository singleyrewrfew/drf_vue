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
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export default api
