/**
 * 用户状态管理 Store
 *
 * 管理用户认证状态、令牌和用户信息，支持持久化存储和权限判断。
 * 所有状态变更会自动同步到 localStorage，确保页面刷新后状态不丢失。
 */
import {defineStore} from 'pinia'
import {ref} from 'vue'
import {getProfile as getProfileApi, login as loginApi, logout as logoutApi} from '@/api/user'
import { AUTH_CONFIG, isTokenExpired } from '@/constants/authConfig'

export const useUserStore = defineStore('user', () => {
    /**
     * 响应式状态：从 localStorage 初始化，确保持久化
     */
    const accessToken = ref(localStorage.getItem(AUTH_CONFIG.ACCESS_TOKEN_KEY) || '')
    const refreshToken = ref(localStorage.getItem(AUTH_CONFIG.REFRESH_TOKEN_KEY) || '')
    const user = ref(JSON.parse(localStorage.getItem(AUTH_CONFIG.USER_INFO_KEY) || 'null'))

    /** fetchProfile 缓存 TTL（毫秒），默认 5 分钟 */
    const PROFILE_CACHE_TTL = 5 * 60 * 1000
    /** 上次成功获取 profile 的时间戳 */
    const _lastFetchTime = ref(0)

    /**
     * 设置令牌并同步到本地存储
     *
     * @param {string} tokenName - 令牌类型 ('access' 或 'refresh')
     * @param {string} newToken - 新的令牌值
     */
    const setToken = (tokenName, newToken) => {
        if (tokenName === AUTH_CONFIG.ACCESS_TOKEN_KEY) {
            accessToken.value = newToken
        } else if (tokenName === AUTH_CONFIG.REFRESH_TOKEN_KEY) {
            refreshToken.value = newToken
        }
        localStorage.setItem(tokenName, newToken)
    }

    /**
     * 设置用户信息并同步到本地存储
     *
     * @param {Object} newUser - 用户信息对象
     */
    const setUser = (newUser) => {
        user.value = newUser
        localStorage.setItem(AUTH_CONFIG.USER_INFO_KEY, JSON.stringify(newUser))
    }

    /**
     * 用户登录
     *
     * 调用登录接口获取令牌和用户信息，并保存到状态和本地存储。
     *
     * @param {Object} credentials - 登录凭证 {username, password}
     * @returns {Promise<Object>} 登录响应数据 {access, refresh, user}
     */
    const login = async (credentials) => {
        const {data} = await loginApi(credentials)
        setToken(AUTH_CONFIG.ACCESS_TOKEN_KEY, data.access)
        setToken(AUTH_CONFIG.REFRESH_TOKEN_KEY, data.refresh)
        setUser(data.user)
        return data
    }

    /**
     * 用户登出
     *
     * 调用后端登出接口使令牌失效，然后清空所有状态和本地存储。
     * 即使后端接口失败，也会清空前端状态以确保安全。
     */
    const logout = async () => {
        try {
            const currentRefreshToken = localStorage.getItem(AUTH_CONFIG.REFRESH_TOKEN_KEY)
            if (currentRefreshToken) {
                // 使用不带拦截器的 axios 实例，避免无限循环
                await logoutApi({ [AUTH_CONFIG.REFRESH_TOKEN_KEY]: currentRefreshToken })
            }
        } catch (e) {
            console.error('登出 API 调用失败:', e)
        }

        // 清空响应式状态
        accessToken.value = ''
        refreshToken.value = ''
        user.value = null

        // 清空本地存储
        localStorage.removeItem(AUTH_CONFIG.ACCESS_TOKEN_KEY)
        localStorage.removeItem(AUTH_CONFIG.USER_INFO_KEY)
        localStorage.removeItem(AUTH_CONFIG.REFRESH_TOKEN_KEY)
    }

    /**
     * 获取用户个人信息（带 TTL 缓存）
     *
     * 缓存逻辑：
     *   - force=true → 无条件重新请求
     *   - user 不存在 → 请求
     *   - user 存在但距上次请求超过 TTL（5 分钟）→ 重新请求
     *   - user 存在且未过期 → 返回缓存
     *
     * @param {boolean} [force=false] - 是否强制刷新（忽略缓存）
     * @returns {Promise<Object>} 用户信息对象
     */
    const fetchProfile = async (force = false) => {
        const now = Date.now()
        if (!force && user.value && now - _lastFetchTime.value < PROFILE_CACHE_TTL) {
            return user.value
        }

        const {data} = await getProfileApi()
        setUser(data)
        _lastFetchTime.value = Date.now()
        return data
    }

    /**
     * 检查用户是否已登录（含 token 过期验证）
     *
     * 不仅检查 token 是否存在，还解析 JWT payload 的 exp 字段
     * 判断是否已过期。过期 token 视为未登录状态。
     *
     * @returns {boolean} token 存在且未过期
     */
    const isLoggedIn = () => {
        if (!accessToken.value) return false
        return !isTokenExpired(accessToken.value)
    }

    /**
     * 检查 access token 是否已过期（不检查是否存在）
     *
     * 供路由守卫等场景判断是否需要提前刷新 token。
     * 即使 token 存在，如果即将过期也返回 true。
     *
     * @param {number} [bufferSeconds=60] - 过期前多少秒即视为过期
     * @returns {boolean} true=已过期或不存在, false=有效
     */
    const isAccessTokenExpired = (bufferSeconds = 60) => {
        if (!accessToken.value) return true
        return isTokenExpired(accessToken.value, bufferSeconds)
    }

    /**
     * 检查用户是否为管理员
     *
     * @returns {boolean} 是否为管理员或超级用户
     */
    const isAdmin = () => user.value?.is_admin || user.value?.is_superuser || false

    /**
     * 检查用户是否为编辑者
     *
     * @returns {boolean} 是否为编辑者或超级用户
     */
    const isEditor = () => user.value?.is_editor || user.value?.is_superuser || false

    /**
     * 检查用户是否可以访问后台管理系统
     *
     * @returns {boolean} 是否具有后台访问权限 (is_staff)
     */
    const canAccessBackend = () => !!user.value?.is_staff

    /**
     * 检查用户是否拥有指定权限
     *
     * 权限判断逻辑：
     * 1. 超级管理员拥有所有权限
     * 2. 无权限列表则拒绝
     * 3. 通配符 '*' 表示拥有所有权限
     * 4. 检查权限码是否在权限列表中
     *
     * @param {string} permissionCode - 权限代码
     * @returns {boolean} 是否拥有该权限
     */
    const hasPermission = (permissionCode) => {
        if (user.value?.is_superuser) return true
        if (!user.value?.permissions) return false
        if (user.value.permissions.includes('*')) return true
        return user.value.permissions.includes(permissionCode)
    }

    /**
     * 检查用户是否拥有多个权限中的任意一个
     *
     * 用于需要满足任一权限即可访问的场景。
     *
     * @param {string[]} permissionCodes - 权限代码数组
     * @returns {boolean} 是否拥有任意一个权限
     */
    const hasAnyPermission = (permissionCodes) => {
        if (user.value?.is_superuser) return true
        if (!user.value?.permissions) return false
        if (user.value.permissions.includes('*')) return true
        return permissionCodes.some(code => user.value.permissions.includes(code))
    }

    return {
        accessToken,
        user,
        setToken,
        setUser,
        login,
        logout,
        fetchProfile,
        isLoggedIn,
        isAccessTokenExpired,
        isAdmin,
        isEditor,
        canAccessBackend,
        hasPermission,
        hasAnyPermission,
    }
})
