import {defineStore} from 'pinia'
import {ref, computed, watchEffect} from 'vue'
import * as userApi from '@/api/user'

/**
 * localStorage 存储键名常量
 */
const STORAGE_KEYS = {
    TOKEN: 'front_token',
    REFRESH: 'front_refresh',
    USER: 'front_user',
    OLD_TOKEN: 'token',
    OLD_REFRESH: 'refresh'
}

/**
 * 用户管理 Store
 * 负责用户认证、令牌管理、用户信息同步等功能
 */
export const useUserStore = defineStore('user', () => {
    // 访问令牌
    const token = ref('')
    // 刷新令牌
    const refreshToken = ref('')
    // 用户信息对象
    const user = ref(null)

    // 计算属性：判断用户是否已登录
    const isLoggedIn = computed(() => !!token.value)

    /**
     * 从 localStorage 初始化用户状态
     * 支持旧版本键名的迁移
     */
    const initFromStorage = () => {
        let savedToken = localStorage.getItem(STORAGE_KEYS.TOKEN)
        let savedRefresh = localStorage.getItem(STORAGE_KEYS.REFRESH)

        // 迁移旧版本的 token 键名
        if (!savedToken) {
            const oldToken = localStorage.getItem(STORAGE_KEYS.OLD_TOKEN)
            if (oldToken) {
                savedToken = oldToken
                localStorage.setItem(STORAGE_KEYS.TOKEN, oldToken)
                localStorage.removeItem(STORAGE_KEYS.OLD_TOKEN)
            }
        }

        // 迁移旧版本的 refresh 键名
        if (!savedRefresh) {
            const oldRefresh = localStorage.getItem(STORAGE_KEYS.OLD_REFRESH)
            if (oldRefresh) {
                savedRefresh = oldRefresh
                localStorage.setItem(STORAGE_KEYS.REFRESH, oldRefresh)
                localStorage.removeItem(STORAGE_KEYS.OLD_REFRESH)
            }
        }

        token.value = savedToken || ''
        refreshToken.value = savedRefresh || ''

        // 解析并验证存储的用户信息
        try {
            const savedUser = localStorage.getItem(STORAGE_KEYS.USER)

            if (savedUser && savedUser !== 'undefined') {
                const parsed = JSON.parse(savedUser)
                // 检查是否是错误的 response 对象（包含 status 字段）
                if (parsed.status && parsed.data) {
                    localStorage.removeItem(STORAGE_KEYS.USER)
                    user.value = null
                } else {
                    // 解析后创建新对象确保响应式
                    user.value = {...parsed}
                }
            } else {
                user.value = null
            }
        } catch (e) {
            console.error('Failed to parse user data from storage:', e)
            user.value = null
            localStorage.removeItem(STORAGE_KEYS.USER)
        }
    }

    /**
     * 将当前用户状态保存到 localStorage
     */
    const saveToStorage = () => {
        if (token.value) {
            localStorage.setItem(STORAGE_KEYS.TOKEN, token.value)
            localStorage.setItem(STORAGE_KEYS.REFRESH, refreshToken.value)
            localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user.value))
        } else {
            localStorage.removeItem(STORAGE_KEYS.TOKEN)
            localStorage.removeItem(STORAGE_KEYS.REFRESH)
            localStorage.removeItem(STORAGE_KEYS.USER)
        }
    }

    /**
     * 清除所有用户状态和存储数据
     */
    const clearStorage = () => {
        token.value = ''
        refreshToken.value = ''
        user.value = null
        localStorage.removeItem(STORAGE_KEYS.TOKEN)
        localStorage.removeItem(STORAGE_KEYS.REFRESH)
        localStorage.removeItem(STORAGE_KEYS.USER)
    }

    // 监听 token 变化，定期同步用户资料
    watchEffect((onCleanup) => {
        if (!token.value) {
            return
        }

        let isActive = true
        let timerId = null

        /**
         * 检查并更新用户资料
         */
        const checkProfile = async () => {
            if (!isActive || !token.value) return

            try {
                const response = await userApi.getProfile()
                // axios 响应拦截器已经将 responseData.data 赋值给 response.data
                const data = response.data || response

                if (isActive && JSON.stringify(user.value) !== JSON.stringify(data)) {
                    // 创建新对象确保响应式更新
                    user.value = {...data}
                    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(data))
                }
            } catch (error) {
                console.error('Profile check error:', error)
            }
        }

        // 立即执行一次检查
        checkProfile()
        // 每 30 秒定期检查一次
        timerId = setInterval(checkProfile, 30000)

        // 清理函数：停止定时器和标记为非活动状态
        onCleanup(() => {
            isActive = false
            if (timerId) {
                clearInterval(timerId)
                timerId = null
            }
        })
    })

    /**
     * 用户登录
     * @param {Object} credentials - 登录凭证（用户名/邮箱和密码）
     * @returns {Promise<Object>} 登录响应数据
     */
    const login = async (credentials) => {
        const response = await userApi.login(credentials)

        // axios 响应拦截器已经将 responseData.data 赋值给 response.data
        const data = response.data

        token.value = data.access
        refreshToken.value = data.refresh
        // 使用 Object.assign 确保响应式更新
        if (data.user) {
            user.value = {...data.user}  // 创建新对象触发响应式
        }
        saveToStorage()
        return data
    }

    /**
     * 用户注册
     * @param {Object} userData - 用户注册信息
     * @returns {Promise<Object>} 注册响应数据
     */
    const register = async (userData) => {
        const data = await userApi.register(userData)
        return data
    }

    /**
     * 用户登出
     * 调用后端 API 使刷新令牌失效，然后清除本地状态
     */
    const logout = async () => {
        try {
            if (refreshToken.value) {
                await userApi.logout({refresh: refreshToken.value})
            }
        } catch (e) {
            console.error(e)
        }
        clearStorage()
    }

    /**
     * 获取并更新用户资料
     */
    const fetchProfile = async () => {
        const response = await userApi.getProfile()

        // axios 响应拦截器已经将 responseData.data 赋值给 response.data
        const data = response.data || response

        // 创建新对象确保响应式更新
        user.value = {...data}
        localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(data))
    }

    /**
     * 刷新访问令牌
     * 使用刷新令牌获取新的访问令牌
     * @throws {Error} 如果没有刷新令牌或刷新失败
     */
    const refreshAccessToken = async () => {
        if (!refreshToken.value) {
            throw new Error('No refresh token')
        }

        try {
            const data = await userApi.refreshToken({refresh: refreshToken.value})
            token.value = data.access
            if (data.refresh) {
                refreshToken.value = data.refresh
            }
            saveToStorage()
        } catch (error) {
            clearStorage()
            throw error
        }
    }

    initFromStorage()

    return {
        token,
        refreshToken,
        user,
        isLoggedIn,
        login,
        register,
        logout,
        fetchProfile,
        refreshAccessToken
    }
})
