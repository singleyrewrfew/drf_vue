/**
 * 统一消息提示工具
 */

import { ElMessage } from 'element-plus'

export const message = {
  success(msg) {
    ElMessage({
      message: msg,
      type: 'success',
      duration: 2000
    })
  },

  warning(msg) {
    ElMessage({
      message: msg,
      type: 'warning',
      duration: 2000
    })
  },

  error(msg) {
    ElMessage({
      message: msg,
      type: 'error',
      duration: 3000,
      showClose: true
    })
  },

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

  networkError(customMsg) {
    ElMessage({
      message: customMsg || '请求失败，请检查网络连接',
      type: 'error',
      duration: 3000,
      showClose: true
    })
  }
}
