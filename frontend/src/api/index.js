// 统一管理：所有 API 配置集中在一处，便于维护
import axios from 'axios'
import {useUserStore} from '@/stores/user'
import router from '@/router'
import { CLIENT_ERROR_STATUS, SERVER_ERROR_STATUS } from '@/constants/httpStatus'
import { handleTokenRefresh } from '@/utils/tokenRefresh'
import { buildAuthHeader, AUTH_CONFIG } from '@/constants/authConfig'

// Axios 错误码常量
const AXIOS_ERROR_CODES = {
    TIMEOUT: 'ECONNABORTED',
}

let isLoggingOut = false

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
    config.headers[AUTH_CONFIG.AUTH_HEADER_NAME] = buildAuthHeader(token)
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
 * 提取用户友好的错误消息
 *
 * ⚠️⚠️⚠️ 重要依赖说明 ⚠️⚠️⚠️
 * 
 * 此函数依赖于 error.response 对象的存在和结构，该对象由以下两处设置：
 * 
 * 1. 【Axios 自动设置】HTTP 错误（如 401/403/500）
 *    - Axios 会自动填充 error.response.status 和 error.response.data
 *    - 后端返回的数据会直接放在 error.response.data 中
 * 
 * 2. 【手动构造】业务错误（code !== 0）
 *    - 见下方响应成功拦截器第 179-194 行
 *    - 我们手动构造了 error.response = { status, data }
 * 
 * 🔴 如果需要修改错误响应结构，请务必同步更新此函数的取值逻辑！
 * 🔴 当前支持的错误字段优先级：message > detail > 兜底文本
 *
 * 后端统一响应格式：
 *   成功: { code: 0, message: "操作成功", data: {...} }
 *   错误: { code: 400, message: "错误信息", error: "错误类型", data: null }
 *
 * @param {Error} error - Axios 错误对象，必须包含 error.response 或 error.message
 * @returns {string} 用户友好的错误消息
 * 
 * @example
 * // 场景1：后端返回的业务错误
 * error.response.data = { code: 400, message: "用户名已存在", error: "bad_request" }
 * extractErrorMessage(error) // → "用户名已存在"
 * 
 * @example
 * // 场景2：DRF 标准错误格式（兼容旧接口）
 * error.response.data = { detail: "未提供有效的认证凭据" }
 * extractErrorMessage(error) // → "未提供有效的认证凭据"
 * 
 * @example
 * // 场景3：网络错误（无 response 对象）
 * error.message = "Network Error"
 * extractErrorMessage(error) // → "Network Error"
 * 
 * @example
 * // 场景4：所有字段都缺失
 * error = {}
 * extractErrorMessage(error) // → "请求失败，请稍后重试"
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
 * 后端统一响应格式：
 *   成功: { code: 0, message: "操作成功", data: {...} }
 *   错误: { code: HTTP状态码, message: "错误信息", error: "错误类型", data: null }
 *
 * 成功响应：标准化数据格式，提取 data 字段
 * 错误响应：处理 401/403/500 等常见错误，自动刷新 token，记录日志
 */
api.interceptors.response.use(
    /**
     * 响应成功处理函数
     *
     * 处理后端统一响应格式：
     * - code === 0: 成功，提取 data 字段
     * - code !== 0: 业务错误，构造错误对象并拒绝 Promise
     *
     * @param {Object} response - Axios 响应对象
     * @returns {Object} 处理后的响应对象（data 字段为实际业务数据）
     */
    (response) => {
        const responseData = response.data

        // 检查是否为后端统一响应格式（包含 code 和 data 字段）
        if (responseData && typeof responseData.code !== 'undefined' && 'data' in responseData) {
            if (responseData.code === 0) {
                // ✅ 成功响应：将实际业务数据挂载到 response.data
                // 调用方可以直接使用 response.data 获取业务数据
                response.data = responseData.data
                return response
            } else {
                // ❌ 业务错误：构造标准错误对象并拒绝 Promise
                // 
                // 🔴 重要：此处构造的 error.response 结构被 extractErrorMessage 函数依赖
                //    如需修改结构，请同步更新 index.js 第 83-129 行的 extractErrorMessage 函数
                // 
                // 后端错误响应格式：
                //   {
                //       code: HTTP状态码 (如 400, 401, 403, 404, 500),
                //       message: "错误信息",
                //       error: "错误类型" (如 "bad_request", "unauthorized"),
                //       data: null
                //   }
                // 
                // 构造的 error 对象格式：
                //   error.response = {
                //       status: HTTP状态码,
                //       data: { code, message, error, data }  // 后端返回的完整数据
                //   }
                const error = new Error(responseData.message || '请求失败')
                error.response = {
                    status: response.status,
                    data: responseData
                }
                return Promise.reject(error)
            }
        }

        // 兼容旧接口或非标准响应：直接返回原始响应
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
        if (error.response?.status === CLIENT_ERROR_STATUS.UNAUTHORIZED && !originalRequest._retry) {
            originalRequest._retry = true

            try {
                // 使用 token 刷新工具处理刷新逻辑
                return await handleTokenRefresh(originalRequest, (config) => api(config))
            } catch (refreshError) {
                // 刷新失败，执行登出流程
                await handleLogoutAndRedirect(userStore, router)
                return Promise.reject(refreshError)
            }
        }

        // 处理 403 禁止访问错误
        if (error.response?.status === CLIENT_ERROR_STATUS.FORBIDDEN) {
            const errorData = error.response?.data

            // 检查是否是因为失去了后台访问权限
            // 后端返回格式：{ code: 403, message: "...", error: "no_backend_access", data: null }
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
        } else if (error.response?.status === SERVER_ERROR_STATUS.INTERNAL_SERVER_ERROR) {
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
