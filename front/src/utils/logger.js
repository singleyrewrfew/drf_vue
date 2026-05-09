/**
 * 日志工具模块
 * 提供统一的日志输出接口，支持不同级别和格式化
 */

const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
  NONE: 4
}

let currentLogLevel = LOG_LEVELS.DEBUG

/**
 * 设置当前日志级别
 * @param {number} level - 日志级别 (0-4)
 */
export const setLogLevel = (level) => {
  currentLogLevel = level
}

/**
 * 获取当前时间戳字符串
 */
const getTimestamp = () => {
  const now = new Date()
  return now.toLocaleTimeString('zh-CN', { hour12: false }) + '.' + String(now.getMilliseconds()).padStart(3, '0')
}

/**
 * 格式化日志输出
 * @param {string} level - 级别名称
 * @param {string} message - 消息内容
 * @param {*} [data] - 附加数据
 */
const formatLog = (level, message, data) => {
  const timestamp = getTimestamp()
  const prefix = `[${timestamp}] [${level}]`
  
  if (data !== undefined) {
    console.log(prefix, message, data)
  } else {
    console.log(prefix, message)
  }
}

/**
 * 输出调试信息
 * @param {string} message - 消息
 * @param {*} [data] - 数据
 */
export const debug = (message, data) => {
  if (currentLogLevel <= LOG_LEVELS.DEBUG) {
    formatLog('DEBUG', message, data)
  }
}

/**
 * 输出一般信息
 * @param {string} message - 消息
 * @param {*} [data] - 数据
 */
export const info = (message, data) => {
  if (currentLogLevel <= LOG_LEVELS.INFO) {
    formatLog('INFO', message, data)
  }
}

/**
 * 输出警告信息
 * @param {string} message - 消息
 * @param {*} [data] - 数据
 */
export const warn = (message, data) => {
  if (currentLogLevel <= LOG_LEVELS.WARN) {
    console.warn(`[WARN] ${message}`, data)
  }
}

/**
 * 输出错误信息
 * @param {string} message - 消息
 * @param {Error|*} [error] - 错误对象或数据
 */
export const error = (message, error) => {
  if (currentLogLevel <= LOG_LEVELS.ERROR) {
    console.error(`[ERROR] ${message}`, error)
  }
}

/**
 * 创建带上下文的 logger 实例
 * @param {string} context - 上下文名称（如组件名、模块名）
 * @returns {{ debug: Function, info: Function, warn: Function, error: Function }}
 */
export const createLogger = (context) => ({
  debug: (msg, data) => debug(`[${context}] ${msg}`, data),
  info: (msg, data) => info(`[${context}] ${msg}`, data),
  warn: (msg, data) => warn(`[${context}] ${msg}`, data),
  error: (msg, err) => error(`[${context}] ${msg}`, err)
})

export default {
  setLogLevel,
  debug,
  info,
  warn,
  error,
  createLogger,
  LOG_LEVELS
}
