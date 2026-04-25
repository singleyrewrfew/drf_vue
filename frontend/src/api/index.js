// 统一管理：所有 API 配置集中在一处，便于维护
import axios from 'axios'
import {useUserStore} from '@/stores/user'
import router from '@/router'

// HTTP 状态码常量
const HTTP_STATUS = {
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    SERVER_ERROR: 500,
}

// Axios 错误码常量
const AXIOS_ERROR_CODES = {
    TIMEOUT: 'ECONNABORTED',
}

let isLoggingOut = false
let isRefreshing = false
let refreshSubscribers = []

/**
 * 创建 Axios 实例并配置默认选项
 *
 * 所有通过此实例发送的请求都会自动应用以下配置：
 * - 基础 URL：从环境变量读取，支持不同部署环境
 * - 超时时间：10 秒
 * - 请求头：默认使用 JSON 格式
 */
const api = axios.create({
    // API 基础 URL，从环境变量读取以支持多环境配置
    baseURL: import.meta.env.VITE_API_BASE_URL,
    // 请求超时时间（毫秒）
    timeout: 10000,
    // 默认请求头配置
    headers: {
        // 声明请求体数据格式为 JSON
        'Content-Type': 'application/json',
    },
})

/**
 * 通知所有订阅者 token 已刷新
 *
 * 当 access token 成功刷新后，调用此函数通知所有等待的请求重试。
 * 遍历执行所有订阅的回调函数，并清空订阅队列防止重复调用。
 *
 * @param {string} token - 新刷新的 access token
 */
function onRefreshed(token) {
    refreshSubscribers.forEach(callback => callback(token))
    refreshSubscribers = []
}

/**
 * 添加刷新令牌订阅者
 *
 * 当 access token 过期需要刷新时，将请求回调函数加入队列等待新 token。
 * 多个并发请求会排队等待，token 刷新后统一通知所有订阅者重试请求。
 *
 * @param {Function} callback - 接收新 token 并执行重试请求的回调函数
 * @returns {Promise} 解析为回调函数执行结果的 Promise 对象
 */
function addRefreshSubscriber(callback) {
    return new Promise((resolve) => {
        refreshSubscribers.push((token) => {
            resolve(callback(token))
        })
    })
}

/**
 * 处理 access token 刷新
 *
 * 当 access token 过期时，使用 refresh token 向服务器请求新的 token 对。
 * 刷新成功后更新本地存储并通知所有等待的请求重试。
 *
 * @returns {Promise<string>} 解析为新的 access token
 * @throws {Error} 当没有 refresh token 或刷新失败时抛出错误
 */
async function handleTokenRefresh() {
    const userStore = useUserStore()
    const currentRefreshToken = localStorage.getItem('refresh')

    // 如果没有 refresh token，说明会话已失效（token 过期或被清除）
    if (!currentRefreshToken) {
        throw new Error('Refresh token not found, session expired')
    }

    try {
        const response = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL}/auth/refresh/`,
            {refresh: currentRefreshToken},
            {headers: {'Content-Type': 'application/json'}}
        )

        const {access, refresh} = response.data

        // 更新本地存储的 token
        userStore.setToken('access', access)
        if (refresh) {
            userStore.setToken('refresh', refresh)
        }

        // 通知所有订阅者 token 已刷新
        onRefreshed(access)
        return access
    } catch (error) {
        // 刷新失败时清空订阅队列，避免后续请求继续等待
        refreshSubscribers = []
        throw error
    }
}


/**
 * 为请求配置添加 JWT 认证头
 *
 * @param {Object} config - Axios 请求配置对象
 * @param {string} token - JWT access token
 * @returns {Object} 添加了认证头的配置对象
 */
function addAuthHeader(config, token) {
    if (!config.headers) {
        config.headers = {}
    }
    config.headers.Authorization = `Bearer ${token}`
    return config
}

/**
 * 请求拦截器：自动添加 JWT 认证头
 *
 * 在每次发送请求前，检查用户是否已登录，如果已登录则自动在请求头中添加
 * Authorization: Bearer <token>，实现统一的身份认证。
 */
api.interceptors.request.use(
    /**
     * 请求发送前的处理函数
     *
     * @param {Object} config - Axios 请求配置对象
     * @returns {Object} 修改后的请求配置对象
     */
    (config) => {
        try {
            const userStore = useUserStore()

            // 如果用户已登录且 token 有效，自动添加 JWT token 到请求头
            if (userStore.accessToken && typeof userStore.accessToken === 'string' && userStore.accessToken.trim()) {
                addAuthHeader(config, userStore.accessToken)
            }
        } catch (error) {
            // 如果获取 store 失败，记录错误但不阻断请求
            console.warn('Failed to get user store for auth header:', error)
        }

        return config
    }
)


/**
 * 提取错误消息
 *
 * @param {Error} error - Axios 错误对象
 * @returns {string} 用户友好的错误消息
 */
function extractErrorMessage(error) {
    return error.response?.data?.message ||
        error.response?.data?.detail ||
        error.message ||
        '请求失败，请稍后重试'
}

/**
 * 处理用户登出和路由跳转
 *
 * @param {Object} userStore - 用户 store 实例
 * @param {Object} routerInstance - 路由器实例
 * @param {Object} [redirectParams] - 跳转参数
 */
async function handleLogoutAndRedirect(userStore, routerInstance, redirectParams = null) {
    if (isLoggingOut) {
        return
    }

    isLoggingOut = true
    try {
        await userStore.logout()
        if (redirectParams) {
            await routerInstance.push(redirectParams)
        } else {
            await routerInstance.push('/login')
        }
    } finally {
        isLoggingOut = false
    }
}

/**
 * 响应拦截器：统一处理 API 响应和错误
 *
 * 成功响应：标准化数据格式，提取 data 字段
 * 错误响应：处理 401/403/500 等常见错误，自动刷新 token，记录日志
 */
api.interceptors.response.use(
    /**
     * 响应成功处理函数
     *
     * @param {Object} response - Axios 响应对象
     * @returns {Object} 处理后的响应对象
     */
    (response) => {
        const responseData = response.data

        // 如果是统一格式（包含 code 和 data 字段）
        if (responseData && typeof responseData.code !== 'undefined' && 'data' in responseData) {
            if (responseData.code === 0) {
                // 成功响应：将实际数据挂载到 response.data
                response.data = responseData.data
                return response
            } else {
                // 错误响应：构造标准错误对象并拒绝 Promise
                const error = new Error(responseData.message || '请求失败')
                error.response = {
                    status: response.status,
                    data: responseData
                }
                return Promise.reject(error)
            }
        }

        // 兼容旧接口：直接返回原始响应
        return response
    },
    /**
     * 响应错误处理函数
     *
     * @param {Error} error - Axios 错误对象
     * @returns {Promise} 拒绝的 Promise，携带处理后的错误信息
     */
    async (error) => {
        const userStore = useUserStore()
        const originalRequest = error.config

        // 处理 401 未授权错误：尝试刷新 token
        if (error.response?.status === HTTP_STATUS.UNAUTHORIZED && !originalRequest._retry) {
            originalRequest._retry = true

            // 如果正在刷新，将请求加入队列等待
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

            // 开始刷新 token
            isRefreshing = true
            try {
                const newAccessToken = await handleTokenRefresh()
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
                isRefreshing = false
                return api(originalRequest)
            } catch (refreshError) {
                isRefreshing = false
                // 刷新失败，执行登出流程
                await handleLogoutAndRedirect(userStore, router)
                return Promise.reject(refreshError)
            }
        }

        // 处理 403 禁止访问错误
        if (error.response?.status === HTTP_STATUS.FORBIDDEN) {
            const errorData = error.response?.data

            // 检查是否是因为失去了后台访问权限
            if (errorData?.error === 'no_backend_access') {
                await handleLogoutAndRedirect(userStore, router, {
                    name: 'Login',
                    query: {error: 'no_permission', message: errorData.message}
                })
                return Promise.reject(error)
            }

            // 其他 403 错误：检查用户权限状态
            if (userStore.isLoggedIn()) {
                try {
                    await userStore.fetchProfile(true)
                    if (!userStore.canAccessBackend()) {
                        await handleLogoutAndRedirect(userStore, router, {
                            name: 'Login',
                            query: {error: 'no_permission'}
                        })
                    }
                } catch (e) {
                    console.error('Failed to fetch user profile:', e)
                }
            }

            return Promise.reject(error)
        }

        // 记录其他类型的错误日志
        const errorMessage = extractErrorMessage(error)

        if (error.response?.data?.error) {
            console.error('API Error:', errorMessage)
        } else if (error.response?.status === HTTP_STATUS.SERVER_ERROR) {
            console.error('Server Error:', errorMessage)
        } else if (error.code === AXIOS_ERROR_CODES.TIMEOUT) {
            console.error('Request Timeout:', errorMessage)
        } else {
            console.error('Unknown Error:', errorMessage)
        }

        return Promise.reject(error)
    }
)

export default api
