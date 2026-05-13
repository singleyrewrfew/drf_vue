/**
 * 统一日志工具
 *
 * 功能特性：
 * - 开发/生产环境自动切换
 * - 带前缀的分类日志
 * - 错误堆栈自动捕获
 * - 性能计时器
 *
 * 使用方式：
 * import { logger } from '@/utils/logger.js'
 * logger.log('用户登录', user)
 * logger.error('请求失败', error)
 */

const isDev = import.meta.env.DEV

/** 日志级别 */
const LEVELS = {
    LOG: 'LOG',
    WARN: 'WARN',
    ERROR: 'ERROR',
    DEBUG: 'DEBUG',
    INFO: 'INFO'
}

/**
 * 格式化日志参数
 */
const formatArgs = (args) => {
    return args.map(arg => {
        if (arg instanceof Error) {
            return `[Error] ${arg.message}\n${arg.stack}`
        }
        if (typeof arg === 'object') {
            try {
                return JSON.stringify(arg, null, 2)
            } catch {
                return String(arg)
            }
        }
        return arg
    })
}

export const logger = {
    /**
     * 普通日志（仅开发环境）
     */
    log: (...args) => {
        if (isDev) {
            console.log(`[${LEVELS.LOG}]`, ...formatArgs(args))
        }
    },

    /**
     * 信息日志（仅开发环境）
     */
    info: (...args) => {
        if (isDev) {
            console.info(`[${LEVELS.INFO}]`, ...formatArgs(args))
        }
    },

    /**
     * 警告日志（始终输出）
     */
    warn: (...args) => {
        console.warn(`[${LEVELS.WARN}]`, ...formatArgs(args))
    },

    /**
     * 错误日志（始终输出，带堆栈）
     */
    error: (...args) => {
        console.error(`[${LEVELS.ERROR}]`, ...formatArgs(args))
        
        // 可选：上报到错误追踪服务
        // if (errorTrackingService) {
        //     errorTrackingService.capture(args)
        // }
    },

    /**
     * 调试日志（仅开发环境）
     */
    debug: (...args) => {
        if (isDev) {
            console.debug(`[${LEVELS.DEBUG}]`, ...formatArgs(args))
        }
    },

    /**
     * 性能计时器
     *
     * @param {string} label - 计时标签
     * @returns {{ end: Function }} 计时对象
     *
     * @example
     * const timer = logger.time('API 请求')
     * await fetchData()
     * timer.end() // 输出：[PERF] API 请求: 123.45ms
     */
    time: (label) => {
        const start = performance.now()
        return {
            end: () => {
                const duration = (performance.now() - start).toFixed(2)
                console.log(`[PERF] ${label}: ${duration}ms`)
            }
        }
    },

    /**
     * 分组日志（用于复杂调试场景）
     *
     * @param {string} label - 分组标签
     * @param {Function} fn - 回调函数
     *
     * @example
     * logger.group('渲染组件', () => {
     *     logger.log('Props:', props)
     *     logger.log('State:', state)
     * })
     */
    group: (label, fn) => {
        if (isDev) {
            console.group(`[GROUP] ${label}`)
            fn()
            console.groupEnd()
        } else {
            fn()
        }
    }
}

export default logger
