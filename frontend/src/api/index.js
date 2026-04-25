// 统一管理：所有 API 配置集中在一处，便于维护
import axios from 'axios'
import {useUserStore} from '@/stores/user'
import router from '@/router'

let isLoggingOut = false
let isRefreshing = false
let refreshSubscribers = []

// 创建一个 axios 实例，可以预先配置默认设置
// 这样，所有使用这个 api 实例的请求都会自动应用这些配置
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,  // 从环境变量中读取 API 基础 URL，支持不同环境配置
    timeout: 10000,  // 10000ms 超时时间
    // 全局请求头配置，可以根据需要添加更多默认头部字段
    headers: {
        // 声明前端发给后端的数据格式是 JSON
        // 后端看到后会用 JSON 方式解析数据
        'Content-Type': 'application/json',
    },
})

function onRefreshed(token) {
    refreshSubscribers.forEach(callback => callback(token))
    refreshSubscribers = []
}

function addRefreshSubscriber(callback) {
    return new Promise((resolve) => {
        refreshSubscribers.push((token) => {
            resolve(callback(token))
        })
    })
}

async function handleTokenRefresh() {
    const userStore = useUserStore()
    const currentRefreshToken = localStorage.getItem('refresh')

    if (!currentRefreshToken) {
        throw new Error('No refresh token')
    }

    try {
        const response = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL}/auth/refresh/`,
            {refresh: currentRefreshToken},
            {headers: {'Content-Type': 'application/json'}}
        )

        const {access, refresh} = response.data

        userStore.setToken('access', access)
        if (refresh) {
            userStore.setToken('refresh', refresh)
        }

        onRefreshed(access)
        return access
    } catch (error) {
        refreshSubscribers = []
        throw error
    }
}

// 请求拦截设置，发送请求之前拦截
// 给 Axios 实例注册「请求拦截器」
api.interceptors.request.use(
    // 1. 正常请求的处理函数（核心）
    (config) => {
        // 拿到 Pinia 的用户 store
        const userStore = useUserStore()
        // 如果用户已登录（有 token）
        if (userStore.accessToken) {
            // 给请求头加上：Authorization: Bearer xxxxx
            config.headers.Authorization = `Bearer ${userStore.accessToken}`
        }
        // 返回修改后的配置，请求继续发送
        return config
    },
    // 2. 请求出错时的错误处理
    (error) => {
        // 把错误继续抛出，让调用处 catch
        // 把请求的错误继续往外抛，让调用接口的地方能捕获到这个错误。
        return Promise.reject(error)
    }
)

// Axios 响应拦截器
// {code, message, data, error?}
api.interceptors.response.use(
    (response) => {
        // 统一处理 API 响应格式
        const responseData = response.data

        // 如果是统一格式（包含 code 和 data 字段）
        if (responseData && typeof responseData.code !== 'undefined' && 'data' in responseData) {
            // 成功响应 code 为 0
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
                 // 抛出异常，让业务catch捕获处理
                return Promise.reject(error)
            }
        }

        // 如果不是统一格式，直接返回（兼容旧接口）
        return response
    },
    // 统一处理 401/403/500、打印日志、最后抛错
    async (error) => {
        const userStore = useUserStore()
        const originalRequest = error.config

        // 统一处理 API 错误
        const errorMessage = error.response?.data?.message ||
            error.response?.data?.detail ||
            error.message ||
            '请求失败，请稍后重试'

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            if (isRefreshing) {
                try {
                    const newToken = await addRefreshSubscriber((token) => {
                        originalRequest.headers.Authorization = `Bearer ${token}`
                        return api(originalRequest)
                    })
                    return newToken
                } catch (subscribeError) {
                    return Promise.reject(subscribeError)
                }
            }

            isRefreshing = true
            try {
                const newAccessToken = await handleTokenRefresh()
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
                isRefreshing = false
                return api(originalRequest)
            } catch (refreshError) {
                isRefreshing = false
                if (!isLoggingOut) {
                    isLoggingOut = true
                    try {
                        await userStore.logout()
                        await router.push('/login')
                    } finally {
                        isLoggingOut = false
                    }
                }
                return Promise.reject(refreshError)
            }
        } else if (error.response?.status === 401 && isLoggingOut) {
            return Promise.reject(error)
        } else if (error.response?.status === 403) {
            // 权限不足
            const errorData = error.response?.data

            // 检查是否是因为失去了后台访问权限
            if (errorData?.error === 'no_backend_access') {
                // 立即清除登录状态并跳转
                await userStore.logout()
                await router.push({
                    name: 'Login',
                    query: {error: 'no_permission', message: errorData.message}
                })
            } else {
                // 其他 403 错误，尝试刷新用户信息
                /*
                行为（自动修复机制）：
                  用户已登录 → 重新拉取最新权限
                  拉完后：
                  仍无后台权限 → 登出 + 跳登录
                  有权限 → 继续正常使用（页面自动恢复）
                */
                if (userStore.isLoggedIn()) {
                    try {
                        await userStore.fetchProfile(true)
                        if (!userStore.canAccessBackend()) {
                            await userStore.logout()
                            await router.push({name: 'Login', query: {error: 'no_permission'}})
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
