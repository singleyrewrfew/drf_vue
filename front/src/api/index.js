import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000
})

// 请求拦截设置
api.interceptors.request.use(
  config => {
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
  error => Promise.reject(error)
)

api.interceptors.response.use(
  response => {
    const responseData = response.data

    if (responseData && typeof responseData === 'object' && 'data' in responseData) {
      const hasCode = typeof responseData.code !== 'undefined'
      const isSuccess = !hasCode || responseData.code === 0

      if (isSuccess) {
        response.data = responseData.data
        return response
      } else {
        const error = new Error(responseData.message || '请求失败')
        error.response = {
          status: response.status,
          data: responseData
        }
        return Promise.reject(error)
      }
    }

    return response
  },
  error => {
    // 统一处理 API 错误
    const errorMessage =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message ||
      '请求失败，请稍后重试'

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
    } else if (error.response?.data?.error) {
      // 后端返回的业务错误
      ElMessage.error(errorMessage)
    } else if (error.response?.status === 500) {
      ElMessage.error('服务器错误，请稍后重试')
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请稍后重试')
    } else {
      ElMessage.error(errorMessage)
    }

    return Promise.reject(error)
  }
)

export default api
