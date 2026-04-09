import axios from 'axios'
import {useUserStore} from '@/stores/user'
import router from '@/router'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
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
        // 统一处理 API 响应格式
        // 后端返回格式：{ code, message, data, error? }
        const responseData = response.data

        // 如果是统一格式（包含 code 和 data 字段）
        if (responseData && typeof responseData.code !== 'undefined' && 'data' in responseData) {
            // 成功响应（code 为 0）
            if (responseData.code === 0) {
                // 将实际数据挂载到 response.data，方便使用
                response.data = responseData.data
                return response
            } else {
                // 错误响应，抛出错误
                const error = new Error(responseData.message || '请求失败')
                error.response = {
                    status: response.status,
                    data: responseData
                }
                return Promise.reject(error)
            }
        }

        // 如果不是统一格式，直接返回（兼容旧接口）
        return response
    },
    async (error) => {
        const userStore = useUserStore()

        // 统一处理 API 错误
        const errorMessage = error.response?.data?.message ||
            error.response?.data?.detail ||
            error.message ||
            '请求失败，请稍后重试'

        if (error.response?.status === 401) {
            // 未授权，清除登录状态并跳转
            userStore.logout()
            router.push('/login')
        } else if (error.response?.status === 403) {
            // 权限不足
            const errorData = error.response?.data

            // 检查是否是因为失去了后台访问权限
            if (errorData?.error === 'no_backend_access') {
                // 立即清除登录状态并跳转
                userStore.logout()
                router.push({
                    name: 'Login',
                    query: {error: 'no_permission', message: errorData.message}
                })
            } else {
                // 其他 403 错误，尝试刷新用户信息
                if (userStore.isLoggedIn()) {
                    try {
                        await userStore.fetchProfile(true)
                        if (!userStore.canAccessBackend()) {
                            userStore.logout()
                            router.push({name: 'Login', query: {error: 'no_permission'}})
                        }
                    } catch (e) {
                        console.error('Failed to fetch user profile:', e)
                    }
                }
            }
        } else if (error.response?.data?.error) {
            // 后端返回的业务错误，由调用方处理
            console.error('API Error:', errorMessage)
        } else if (error.response?.status === 500) {
            console.error('Server Error:', errorMessage)
        } else if (error.code === 'ECONNABORTED') {
            console.error('Request Timeout:', errorMessage)
        } else {
            console.error('Unknown Error:', errorMessage)
        }

        return Promise.reject(error)
    }
)

export default api
