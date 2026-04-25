/**
 * 通用工具函数库
 *
 * 提供媒体 URL 处理、消息提示、加载状态管理、日期格式化、
 * 文件处理、文本处理、函数防抖节流、对象操作等常用工具函数。
 */
import {ElMessage, ElMessageBox} from 'element-plus'

/**
 * 获取媒体资源的基础 URL
 *
 * @returns {string} 媒体基础 URL（去除 /api 后缀）
 */
const getMediaBaseUrl = () => {
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
    return apiBaseUrl.replace(/\/api\/?$/, '')
}

/**
 * 获取用户头像的完整 URL
 *
 * 自动处理相对路径和绝对路径，确保返回完整的媒体资源地址。
 *
 * @param {string} avatar - 头像路径或 URL
 * @returns {string} 完整的头像 URL
 */
export const getAvatarUrl = (avatar) => {
    if (!avatar) return ''
    if (avatar.startsWith('http')) return avatar
    const baseUrl = getMediaBaseUrl()
    if (avatar.startsWith('/media/')) {
        return `${baseUrl}${avatar}`
    }
    return `${baseUrl}/media/${avatar}`
}

/**
 * 获取媒体文件的完整 URL
 *
 * 自动处理相对路径和绝对路径，支持图片和视频等媒体资源。
 *
 * @param {string} url - 媒体文件路径或 URL
 * @returns {string} 完整的媒体文件 URL
 */
export const getMediaUrl = (url) => {
    if (!url) return ''
    if (url.startsWith('http')) return url
    const baseUrl = getMediaBaseUrl()
    if (url.startsWith('/media/')) {
        return `${baseUrl}${url}`
    }
    return `${baseUrl}/media/${url}`
}

/**
 * 显示删除确认对话框
 *
 * @param {string} [message='确定删除该项？此操作不可恢复。'] - 确认消息文本
 * @returns {Promise} 用户确认时 resolve，取消时 reject
 */
export const confirmDelete = async (message = '确定删除该项？此操作不可恢复。') => {
    await ElMessageBox.confirm(message, '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    })
}

/**
 * 显示成功消息
 *
 * @param {string} [message='操作成功'] - 消息文本
 */
export const showSuccess = (message = '操作成功') => {
    ElMessage.success(message)
}

/**
 * 显示错误消息
 *
 * @param {string} [message='操作失败'] - 消息文本
 */
export const showError = (message = '操作失败') => {
    ElMessage.error(message)
}

/**
 * 显示警告消息
 *
 * @param {string} message - 消息文本
 */
export const showWarning = (message) => {
    ElMessage.warning(message)
}

/**
 * 显示信息消息
 *
 * @param {string} message - 消息文本
 */
export const showInfo = (message) => {
    ElMessage.info(message)
}

/**
 * 带加载状态执行的异步函数包装器
 *
 * 自动管理 loading 状态，执行前后切换状态，确保异常时也能正确重置。
 *
 * @param {Function} fn - 要执行的异步函数
 * @param {import('vue').Ref<boolean>} loadingRef - Vue ref 加载状态引用
 * @returns {Promise} 异步函数的执行结果
 */
export const withLoading = async (fn, loadingRef) => {
    if (loadingRef && typeof loadingRef === 'object') {
        loadingRef.value = true
    }
    try {
        return await fn()
    } finally {
        if (loadingRef && typeof loadingRef === 'object') {
            loadingRef.value = false
        }
    }
}

/**
 * 格式化日期时间
 *
 * 支持自定义格式模板，默认格式为 'YYYY-MM-DD HH:mm:ss'。
 *
 * @param {string|Date} date - 日期字符串或 Date 对象
 * @param {string} [format='YYYY-MM-DD HH:mm:ss'] - 格式模板
 * @returns {string} 格式化后的日期字符串，无效日期返回空字符串
 */
export const formatDate = (date, format = 'YYYY-MM-DD HH:mm:ss') => {
    if (!date) return ''
    const d = new Date(date)
    if (isNaN(d.getTime())) return ''

    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const hours = String(d.getHours()).padStart(2, '0')
    const minutes = String(d.getMinutes()).padStart(2, '0')
    const seconds = String(d.getSeconds()).padStart(2, '0')

    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds)
}

/**
 * 格式化文件大小
 *
 * 自动选择合适的单位（B, KB, MB, GB, TB）并保留两位小数。
 *
 * @param {number} bytes - 文件大小（字节）
 * @returns {string} 格式化后的大小字符串，如 "1.5 MB"
 */
export const formatFileSize = (bytes) => {
    if (!bytes || bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 截断文本并添加省略号
 *
 * @param {string} text - 原始文本
 * @param {number} [maxLength=50] - 最大长度
 * @returns {string} 截断后的文本
 */
export const truncateText = (text, maxLength = 50) => {
    if (!text) return ''
    if (text.length <= maxLength) return text
    return text.slice(0, maxLength) + '...'
}

/**
 * 函数防抖
 *
 * 在指定延迟时间内只执行最后一次调用，适用于搜索输入等场景。
 *
 * @param {Function} fn - 要防抖的函数
 * @param {number} [delay=300] - 延迟时间（毫秒）
 * @returns {Function} 防抖后的函数
 */
export const debounce = (fn, delay = 300) => {
    let timer = null
    return function (...args) {
        if (timer) clearTimeout(timer)
        timer = setTimeout(() => {
            fn.apply(this, args)
        }, delay)
    }
}

/**
 * 函数节流
 *
 * 在指定延迟时间内只执行一次，适用于滚动、resize 等高频事件。
 *
 * @param {Function} fn - 要节流的函数
 * @param {number} [delay=300] - 延迟时间（毫秒）
 * @returns {Function} 节流后的函数
 */
export const throttle = (fn, delay = 300) => {
    let lastTime = 0
    return function (...args) {
        const now = Date.now()
        if (now - lastTime >= delay) {
            lastTime = now
            fn.apply(this, args)
        }
    }
}

/**
 * 深拷贝对象
 *
 * 支持 Date、Array、Object 类型的递归拷贝。
 *
 * @param {*} obj - 要拷贝的对象
 * @returns {*} 拷贝后的新对象
 */
export const deepClone = (obj) => {
    if (obj === null || typeof obj !== 'object') return obj
    if (obj instanceof Date) return new Date(obj)
    if (obj instanceof Array) return obj.map(item => deepClone(item))
    if (obj instanceof Object) {
        const cloned = {}
        for (const key in obj) {
            if (Object.prototype.hasOwnProperty.call(obj, key)) {
                cloned[key] = deepClone(obj[key])
            }
        }
        return cloned
    }
}

/**
 * 从对象中选取指定键的值
 *
 * @param {Object} obj - 源对象
 * @param {string[]} keys - 要选取的键名数组
 * @returns {Object} 包含指定键的新对象
 */
export const pick = (obj, keys) => {
    const result = {}
    keys.forEach(key => {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
            result[key] = obj[key]
        }
    })
    return result
}

/**
 * 从对象中排除指定键
 *
 * @param {Object} obj - 源对象
 * @param {string[]} keys - 要排除的键名数组
 * @returns {Object} 排除指定键后的新对象
 */
export const omit = (obj, keys) => {
    const result = {...obj}
    keys.forEach(key => {
        delete result[key]
    })
    return result
}

/**
 * 判断值是否为空
 *
 * 支持 null、undefined、空字符串、空数组、空对象的判断。
 *
 * @param {*} value - 要判断的值
 * @returns {boolean} 是否为空
 */
export const isEmpty = (value) => {
    if (value === null || value === undefined) return true
    if (typeof value === 'string') return value.trim() === ''
    if (Array.isArray(value)) return value.length === 0
    if (typeof value === 'object') return Object.keys(value).length === 0
    return false
}

/**
 * 生成唯一 ID
 *
 * 基于时间戳和随机数生成简短的唯一标识符。
 *
 * @returns {string} 唯一 ID 字符串
 */
export const generateId = () => {
    return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

/**
 * 延迟执行（睡眠）
 *
 * @param {number} ms - 延迟时间（毫秒）
 * @returns {Promise} Promise 对象
 */
export const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))

/**
 * 重试执行异步函数
 *
 * 在失败时自动重试指定次数，每次重试之间等待指定延迟时间。
 *
 * @param {Function} fn - 要执行的异步函数
 * @param {number} [retries=3] - 最大重试次数
 * @param {number} [delay=1000] - 重试间隔时间（毫秒）
 * @returns {Promise} 异步函数的执行结果
 * @throws {Error} 所有重试都失败后抛出最后一次错误
 */
export const retry = async (fn, retries = 3, delay = 1000) => {
    for (let i = 0; i < retries; i++) {
        try {
            return await fn()
        } catch (error) {
            if (i === retries - 1) throw error
            await sleep(delay)
        }
    }
}
