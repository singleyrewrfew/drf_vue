/**
 * 统一消息提示工具
 * 
 * 封装 Element Plus 的 ElMessage，提供一致的用户体验
 */

import { ElMessage } from 'element-plus'

export const message = {
  /**
   * 成功提示
   * @param {string} msg - 提示信息
   */
  success(msg) {
    ElMessage({
      message: msg,
      type: 'success',
      duration: 2000
    })
  },

  /**
   * 警告提示
   * @param {string} msg - 提示信息
   */
  warning(msg) {
    ElMessage({
      message: msg,
      type: 'warning',
      duration: 2000
    })
  },

  /**
   * 错误提示
   * @param {string} msg - 提示信息
   */
  error(msg) {
    ElMessage({
      message: msg,
      type: 'error',
      duration: 3000,
      showClose: true
    })
  },

  /**
   * 需要登录时的提示
   * @param {string} action - 操作名称，如 '点赞'、'评论'
   * @param {Function} onClose - 关闭后的回调（可选）
   */
  authRequired(action = '操作', onClose) {
    ElMessage({
      message: `登录后才能${action}哦~`,
      type: 'warning',
      duration: 2000,
      onClose: () => {
        if (onClose) onClose()
      }
    })
  },

  /**
   * 网络错误提示
   * @param {string} customMsg - 自定义提示信息
   */
  networkError(customMsg) {
    ElMessage({
      message: customMsg || '请求失败，请检查网络连接',
      type: 'error',
      duration: 3000,
      showClose: true
    })
  }
}
