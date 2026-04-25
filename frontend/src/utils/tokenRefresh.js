/**
 * Token 刷新管理工具模块
 * 
 * 负责处理 JWT access token 的自动刷新逻辑，包括：
 * - 使用 refresh token 获取新的 access token
 * - 管理并发请求的排队等待机制
 * - 通知所有等待的请求使用新 token 重试
 * 
 * @module utils/tokenRefresh
 */

import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { buildAuthHeader, AUTH_CONFIG } from '@/constants/authConfig'

/** 是否正在刷新 token 的标志位 */
let isRefreshing = false

/** 等待 token 刷新的请求回调队列 */
let refreshSubscribers = []

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
 * 执行 token 刷新操作
 * 
 * 使用当前的 refresh token 向服务器请求新的 access token。
 * 刷新成功后会自动更新 user store 中的 token。
 * 
 * @async
 * @returns {Promise<Object>} 包含新的 access 和 refresh token 的对象
 * @throws {Error} 当没有 refresh token 或刷新失败时抛出错误
 * 
 * @example
 * const tokens = await refreshToken()
 * console.log(tokens.access) // 新的 access token
 */
async function refreshToken() {
    const userStore = useUserStore()
    const currentRefreshToken = localStorage.getItem('refresh')

    // 如果没有 refresh token，说明会话已失效（token 过期或被清除）
    if (!currentRefreshToken) {
        throw new Error('Refresh token not found, session expired')
    }

    try {
        const response = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL}/auth/refresh/`,
            { [AUTH_CONFIG.REFRESH_TOKEN_KEY]: currentRefreshToken },
            { headers: { 'Content-Type': 'application/json' } }
        )

        const { access, refresh } = response.data

        // 更新本地存储的 token
        userStore.setToken(AUTH_CONFIG.ACCESS_TOKEN_KEY, access)
        if (refresh) {
            userStore.setToken(AUTH_CONFIG.REFRESH_TOKEN_KEY, refresh)
        }

        return { access, refresh }
    } catch (error) {
        // 刷新失败时清空订阅队列，避免后续请求继续等待
        refreshSubscribers = []
        throw error
    }
}

/**
 * 处理 access token 刷新流程
 * 
 * 这是主要的刷新入口函数，负责：
 * 1. 检查是否正在刷新，如果是则将请求加入等待队列
 * 2. 如果未在刷新，则执行刷新操作并通知所有等待的请求
 * 3. 返回新的 access token
 * 
 * @async
 * @param {Object} originalRequest - 原始的 Axios 请求配置对象
 * @param {Function} retryRequest - 重试请求的函数，接收配置对象返回 Promise
 * @returns {Promise} 重试请求的结果
 * @throws {Error} 当刷新失败时抛出错误，调用方应处理登出逻辑
 * 
 * @example
 * // 在响应拦截器中使用
 * try {
 *     return await handleTokenRefresh(originalRequest, (config) => api(config))
 * } catch (error) {
 *     await handleLogoutAndRedirect()
 * }
 */
async function handleTokenRefresh(originalRequest, retryRequest) {
    // 如果正在刷新，将当前请求加入等待队列
    if (isRefreshing) {
        return addRefreshSubscriber((token) => {
            originalRequest.headers[AUTH_CONFIG.AUTH_HEADER_NAME] = buildAuthHeader(token)
            return retryRequest(originalRequest)
        })
    }

    // 开始刷新 token
    isRefreshing = true
    try {
        const { access } = await refreshToken()
        
        // 通知所有等待的请求
        onRefreshed(access)
        
        // 重试原始请求
        originalRequest.headers[AUTH_CONFIG.AUTH_HEADER_NAME] = buildAuthHeader(access)
        return retryRequest(originalRequest)
    } catch (error) {
        // 刷新失败，清空状态
        isRefreshing = false
        refreshSubscribers = []
        throw error
    } finally {
        // 确保刷新标志被重置
        isRefreshing = false
    }
}

/**
 * 重置刷新状态
 * 
 * 在特殊情况下（如用户主动登出），可能需要手动重置刷新状态。
 * 这会清空所有等待的请求队列并重置标志位。
 */
function resetRefreshState() {
    isRefreshing = false
    refreshSubscribers = []
}

export {
    handleTokenRefresh,
    refreshToken,
    addRefreshSubscriber,
    resetRefreshState,
}
