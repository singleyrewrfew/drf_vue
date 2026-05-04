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

/**
 * 多标签页登出状态同步
 *
 * 使用 BroadcastChannel 在同源标签页之间实时广播登出事件。
 * 任一标签页登出 → 所有标签页同步更新 isLoggingOut 状态，
 * 避免重复执行登出逻辑或 token 刷新请求。
 */
const LOGOUT_CHANNEL_NAME = 'auth-logout'
const logoutChannel =
    typeof BroadcastChannel !== 'undefined'
        ? new BroadcastChannel(LOGOUT_CHANNEL_NAME)
        : null

/** 当前标签页的登出锁 */
let isLoggingOut = false

/**
 * 403 防重入标记
 *
 * 问题背景：
 *   403 响应拦截器中会调用 userStore.fetchProfile()，
 *   而 fetchProfile 内部通过 getProfileApi() 发请求，使用的是带拦截器的 api 实例。
 *   如果 getProfileApi 也返回 403，会再次进入同一拦截器 → 无限递归。
 *
 * 解决方案：
 *   在进入 403 处理逻辑前设置标记，退出后清除。
 *   如果检测到已在处理中，直接跳过 fetchProfile 调用，避免递归。
 */
let isHandlingForbidden = false

// 监听其他标签页的登出广播
if (logoutChannel) {
    logoutChannel.onmessage = (event) => {
        if (event.data?.type === 'logging-out' && !isLoggingOut) {
            isLoggingOut = true
        }
    }
}

/**
 * Axios 实例公共默认配置
 *
 * 集中管理 baseURL/timeout/headers，避免多实例重复定义。
 * 后续修改超时时间等只需改此处一处。
 */
const AXIOS_DEFAULT_CONFIG = {
    // API 基础 URL，从环境变量读取以支持多环境配置
    baseURL: import.meta.env.VITE_API_BASE_URL,
    // 请求超时时间（毫秒），从环境变量读取（默认 10 秒）
    timeout: Number(import.meta.env.VITE_API_TIMEOUT) || 10000,
    // 默认请求头配置
    headers: {
        // 声明请求体数据格式为 JSON
        'Content-Type': 'application/json',
    },
}

/**
 * 创建带拦截器的 Axios 实例
 *
 * 所有通过此实例发送的请求都会自动应用以下功能：
 * - 基础 URL / 超时 / Content-Type（来自 AXIOS_DEFAULT_CONFIG）
 * - 请求拦截器：自动添加 JWT 认证头
 * - 响应拦截器：统一错误处理 + 自动 token 刷新
 */
const api = axios.create(AXIOS_DEFAULT_CONFIG)

/**
 * 创建不带拦截器的 Axios 实例（用于登出等特殊场景）
 *
 * 此实例不会添加认证头，也不会处理错误响应，适用于：
 * - 用户登出（Token 可能已失效）
 * - Token 刷新（避免循环依赖）
 * - 其他不需要认证的请求
 *
 * 配置复用 AXIOS_DEFAULT_CONFIG，确保 baseURL/timeout/headers 与 api 实例一致。
 */
const logoutApi = axios.create(AXIOS_DEFAULT_CONFIG)


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
            console.warn('获取用户 store 失败，无法添加认证头:', error)
        }

        return config
    }
)


/**
 * 统一提取错误消息（支持后端所有可能的错误字段格式）
 *
 * 按优先级依次检查以下字段：
 *   1. message      — 标准业务错误（推荐）
 *   2. detail       — DRF REST framework 默认格式
 *   3. error        — 简单错误类型字符串
 *   4. data.message — 嵌套包装格式
 *   5. 表单字段错误 — { username: ['用户名已存在'] } 取第一条
 *   6. error.message — Axios 网络层错误消息
 *   7. 兜底文本
 *
 * @param {Error} error - Axios 错误对象
 * @param {string} [fallback] - 自定义兜底文案
 * @returns {string} 用户友好的错误消息
 */
export function extractErrorMessage(error, fallback = '请求失败，请稍后重试') {
    const data = error.response?.data
    if (!data) return error.message || fallback

    // 1. 顶层标准字段
    if (data.message) return data.message
    if (data.detail) return data.detail
    if (typeof data.error === 'string') return data.error

    // 2. 嵌套 data.message 格式
    if (data.data?.message) return data.data.message

    // 3. 表单字段级错误（DRF serializer errors）：{ field: ['msg1', 'msg2'] }
    if (typeof data === 'object') {
        for (const key of Object.keys(data)) {
            const val = data[key]
            if (Array.isArray(val) && val.length > 0 && typeof val[0] === 'string') {
                return val[0]
            }
        }
    }

    return error.message || fallback
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
    // 广播给其他标签页，同步登出状态
    logoutChannel?.postMessage({ type: 'logging-out' })
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
 * 后端统一响应格式（使用 HTTP 状态码）：
 *   成功: { message: "操作成功", data: {...} }  (HTTP 2xx)
 *   错误: { message: "错误信息", error: "错误类型", data: null }  (HTTP 4xx/5xx)
 *
 * 成功响应：标准化数据格式，提取 data 字段
 * 错误响应：处理 401/403/500 等常见错误，自动刷新 token，记录日志
 */
api.interceptors.response.use(
    /**
     * 响应成功处理函数
     *
     * 处理后端统一响应格式：
     * - HTTP 2xx: 成功，提取 data 字段
     * - HTTP 4xx/5xx: 错误，构造错误对象并拒绝 Promise
     *
     * @param {Object} response - Axios 响应对象
     * @returns {Object} 处理后的响应对象（data 字段为实际业务数据）
     */
    (response) => {
        const responseData = response.data

        // 检查是否为后端统一响应格式（包含 message 和 data 字段）
        if (responseData && 'message' in responseData && 'data' in responseData) {
            // ✅ 成功响应（HTTP 2xx）：将实际业务数据挂载到 response.data
            // 调用方可以直接使用 response.data 获取业务数据
            response.data = responseData.data
            return response
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
            // 防重入：如果已在处理 403（fetchProfile 可能触发递归），跳过
            if (isHandlingForbidden) {
                return Promise.reject(error)
            }
            isHandlingForbidden = true

            try {
                // 主动检查用户权限状态（单一事实来源）
                if (userStore.isLoggedIn()) {
                    try {
                        // 强制从后端重新获取最新的用户信息
                        await userStore.fetchProfile(true)

                        // 如果没有后台访问权限，执行登出
                        if (!userStore.canAccessBackend()) {
                            console.warn('检测到用户已失去后台访问权限')
                            await handleLogoutAndRedirect(userStore, router, {
                                name: 'Login',
                                query: {
                                    error: 'no_permission',
                                    message: extractErrorMessage(error, '您没有后台访问权限')
                                }
                            })
                            return Promise.reject(error)
                        }
                    } catch (e) {
                        console.error('获取用户信息失败:', e)
                    }
                }

                // 其他 403 错误，正常拒绝
                return Promise.reject(error)
            } finally {
                isHandlingForbidden = false
            }
        }

        // 其他错误直接拒绝，交给调用方处理
        return Promise.reject(error)
    }
)

export default api
export { logoutApi }

/**
 * 统一提取列表数据（兼容 DRF 分页格式与普通数组）
 *
 * DRF 分页响应：{ results: [...], count: 100 }
 * 普通数组/对象：直接返回数据本身
 *
 * @param {Object|Array} responseData - API 响应的 data 字段（即 response.data）
 * @returns {Array} 标准化的列表数组
 *
 * @example
 * // DRF 分页格式
 * normalizeListResponse({ results: [{id:1}], count: 1 }) // → [{id:1}]
 * // 普通数组
 * normalizeListResponse([{id:1}])                       // → [{id:1}]
 */
export function normalizeListResponse(responseData) {
    if (!responseData) return []
    if (Array.isArray(responseData)) return responseData
    return responseData.results || responseData || []
}
