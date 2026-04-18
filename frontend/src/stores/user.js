import {defineStore} from 'pinia'
import {ref} from 'vue'
import {getProfile, login as loginApi, logout as logoutApi} from '@/api/user'

export const useUserStore = defineStore('user', () => {
    // 登录令牌（从 localStorage 读，刷新不丢失）
    const accessToken = ref(localStorage.getItem('access') || '')
    const refreshToken = ref(localStorage.getItem('refresh') || '')
    // 用户信息对象（JSON 反序列化）
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
    // 定时检查用户信息的定时器（非响应式）
    let profileCheckTimer = null

    // 修改状态 同时同步到 localStorage
    // 保证 内存状态 ↔ 本地存储 始终一致
    const setToken = (tokenName,newToken) => {
        if (tokenName === 'access'){
            accessToken.value = newToken
        }else {
            refreshToken.value = newToken
        }
        localStorage.setItem(tokenName, newToken)
    }

    const removeLocalStorageItem = (filed) => {
        localStorage.removeItem(filed)
    }

    const setUser = (newUser) => {
        user.value = newUser
        localStorage.setItem('user', JSON.stringify(newUser))
    }

    // 异步 async/await 处理登录请求
    const login = async (credentials) => {
        const {data} = await loginApi(credentials)  // 调登录接口
        setToken('access', data.access)  // 存token
        setToken('refresh', data.refresh)  // 存refresh token
        setUser(data.user)     // 存用户信息
        startProfileCheck()   // 开启定时检查
        return data
    }

    // 清理所有状态 + 本地存储 + 停止定时任务
    const logout = async () => {
        stopProfileCheck()   // 先停定时器
        try {
            const refreshToken = localStorage.getItem('refresh')
            if (refreshToken) {
                await logoutApi({refresh: refreshToken})   // 调用后端登出
            }
        } catch (e) {
            console.error('Logout API error:', e)
        }
        // 清空状态 + 本地存储
        removeLocalStorageItem('access')
        removeLocalStorageItem('user')
        removeLocalStorageItem('refresh')
    }

    // 获取用户信息（fetchProfile）
    // 避免重复请求
    // 强制刷新：fetchProfile(true)
    const fetchProfile = async (force = false) => {
        if (!force && user.value) {  // 有缓存直接返回
            return user.value
        }

        const {data} = await getProfile()  // 请求用户信息接口拿数据
        setUser(data)
        return data
    }

    // 定时检查用户状态（重要）
    const startProfileCheck = () => {
        if (profileCheckTimer) {
            clearInterval(profileCheckTimer)
        }

        profileCheckTimer = setInterval(async () => {
            if (accessToken.value) {
                try {
                    const {data} = await getProfile()  // 请求用户信息接口拿数据
                    // 对比新旧用户信息，不一样就更新
                    if (JSON.stringify(user.value) !== JSON.stringify(data)) {
                        setUser(data)
                    }
                } catch (error) {
                    console.error('Profile check error:', error)
                }
            }
        }, 30000)  // 30秒一次
    }

    // 清除定时器
    const stopProfileCheck = () => {
        if (profileCheckTimer) {
            clearInterval(profileCheckTimer)
            profileCheckTimer = null
        }
    }

    const isLoggedIn = () => !!accessToken.value  // 是否登录

    const isAdmin = () => user.value?.is_admin || user.value?.is_superuser || false  // 是否管理员

    const isEditor = () => user.value?.is_editor || user.value?.is_superuser || false  // 是否编辑

    const canAccessBackend = () => !!user.value?.is_staff  // 能否进后台

    // 单权限判断
    const hasPermission = (permissionCode) => {
        if (user.value?.is_superuser) return true  // 超级管理员全过
        if (!user.value?.permissions) return false  // 无权限列表 → 直接拒绝
        if (user.value.permissions.includes('*')) return true  // 拥有通配符 *：全过
        return user.value.permissions.includes(permissionCode)  // 普通判断：是否包含指定权限码
    }

    // 多权限满足任一
    const hasAnyPermission = (permissionCodes) => {
        if (user.value?.is_superuser) return true  // 如果是超级管理员 → 直接放行 ✅
        if (!user.value?.permissions) return false  // 用户没有任何权限列表 → 直接拒绝 ❌
        if (user.value.permissions.includes('*')) return true  // 用户有通配符 * → 拥有所有权限，放行 ✅
        return permissionCodes.some(code => user.value.permissions.includes(code))  // 只要用户拥有数组里【任意一个】权限 → 就返回 true
    }

    if (accessToken.value) {
        startProfileCheck()
    }

    return {
        accessToken,
        user,
        setToken,
        removeLocalStorageItem,
        setUser,
        login,
        logout,
        fetchProfile,
        startProfileCheck,
        stopProfileCheck,
        isLoggedIn,
        isAdmin,
        isEditor,
        canAccessBackend,
        hasPermission,
        hasAnyPermission,
    }
})
