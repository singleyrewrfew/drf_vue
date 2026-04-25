/**
 * 用户状态管理 Store
 *
 * 管理用户认证状态、令牌和用户信息，支持持久化存储和权限判断。
 * 所有状态变更会自动同步到 localStorage，确保页面刷新后状态不丢失。
 */
import {defineStore} from 'pinia'
import {ref} from 'vue'
import {getProfile as getProfileApi, login as loginApi, logout as logoutApi} from '@/api/user'
import { AUTH_CONFIG } from '@/constants/authConfig'

export const useUserStore = defineStore('user', () => {
    /**
     * 响应式状态：从 localStorage 初始化，确保持久化
     */
    const accessToken = ref(localStorage.getItem(AUTH_CONFIG.ACCESS_TOKEN_KEY) || '')
    const refreshToken = ref(localStorage.getItem(AUTH_CONFIG.REFRESH_TOKEN_KEY) || '')
    const user = ref(JSON.parse(localStorage.getItem(AUTH_CONFIG.USER_INFO_KEY) || 'null'))

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
            console.error('Logout API error:', e)
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
     * 获取用户个人信息
     *
     * 支持缓存机制，避免重复请求。可强制刷新以获取最新数据。
     *
     * @param {boolean} [force=false] - 是否强制刷新（忽略缓存）
     * @returns {Promise<Object>} 用户信息对象
     */
    const fetchProfile = async (force = false) => {
        if (!force && user.value) {
            return user.value
        }

        const {data} = await getProfileApi()
        setUser(data)
        return data
    }

    /**
     * 检查用户是否已登录
     *
     * @returns {boolean} 是否存在 access token
     */
    const isLoggedIn = () => !!accessToken.value

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
        isAdmin,
        isEditor,
        canAccessBackend,
        hasPermission,
        hasAnyPermission,
    }
})
